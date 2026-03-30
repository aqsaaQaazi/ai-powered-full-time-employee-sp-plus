#!/usr/bin/env python3
"""
Approval Handler - Monitors approval workflow directories and processes requests

This script implements a file-based approval workflow system that monitors
directories for approval requests and executes actions when requests are approved.
"""

import os
import sys
import time
import logging
import signal
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config.settings import (
    APPROVED_DIR,
    REJECTED_DIR,
    LOGS_DIR,
    PENDING_APPROVAL_DIR,
    APPROVAL_EXPIRATION_HOURS
)
from utils.approval_parser import parse_approval_request
from utils.action_executor import execute_approved_action, log_execution_result
from utils.file_operations import atomic_move


class ApprovalHandler(FileSystemEventHandler):
    """
    File system event handler that monitors the Approved directory for new files
    and processes them as approval requests.
    """

    def __init__(self):
        """
        Initialize the approval handler
        """
        self.running = True

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('approval_handler.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Register signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """
        Handle shutdown signals gracefully
        """
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False

    def on_created(self, event):
        """
        Handle file creation events in monitored directories
        """
        if event.is_directory:
            return

        # Only process markdown files
        if not event.src_path.endswith('.md'):
            return

        file_path = Path(event.src_path)

        # If file is created in Approved directory, process it
        if APPROVED_DIR in file_path.parents:
            self._process_approved_request(file_path)
        # If file is created in Rejected directory, log it
        elif REJECTED_DIR in file_path.parents:
            self._process_rejected_request(file_path)

    def on_moved(self, event):
        """
        Handle file move events in monitored directories
        """
        if event.is_directory:
            return

        # Only process markdown files
        if not event.dest_path.endswith('.md'):
            return

        file_path = Path(event.dest_path)

        # If file is moved to Approved directory, process it
        if APPROVED_DIR in file_path.parents:
            self._process_approved_request(file_path)
        # If file is moved to Rejected directory, log it
        elif REJECTED_DIR in file_path.parents:
            self._process_rejected_request(file_path)

    def _process_approved_request(self, file_path: Path):
        """
        Process an approval request that has been moved to the Approved directory

        Args:
            file_path: Path to the approval request file
        """
        try:
            self.logger.info(f"Processing approved request: {file_path}")

            # Parse the approval request
            approval_data = parse_approval_request(file_path)

            if not approval_data:
                self.logger.error(f"Invalid approval request: {file_path}")
                return

            # Execute the approved action
            execution_result = execute_approved_action(approval_data)

            # Log the execution result
            log_success = log_execution_result(approval_data, execution_result, LOGS_DIR)

            if log_success:
                # Move the processed file to the logs directory
                log_file_name = f"{approval_data['action']}_{int(time.time())}_processed.md"
                log_file_path = LOGS_DIR / log_file_name

                # Rename the original file to the log directory with new name
                success = atomic_move(file_path, log_file_path)

                if success:
                    self.logger.info(f"Processed request moved to logs: {log_file_path}")
                else:
                    self.logger.error(f"Failed to move processed request: {file_path}")
            else:
                self.logger.error(f"Failed to log execution result for: {file_path}")

        except Exception as e:
            self.logger.error(f"Error processing approved request {file_path}: {e}")

    def _process_rejected_request(self, file_path: Path):
        """
        Process an approval request that has been moved to the Rejected directory

        Args:
            file_path: Path to the rejected approval request file
        """
        try:
            self.logger.info(f"Processing rejected request: {file_path}")

            # Parse the approval request to get basic info
            approval_data = parse_approval_request(file_path)

            if approval_data:
                self.logger.info(f"Request rejected: {approval_data.get('action')} - {file_path}")
            else:
                self.logger.warning(f"Could not parse rejected request: {file_path}")

            # Move the rejected file to the logs directory
            timestamp = int(time.time())
            log_file_name = f"rejected_{timestamp}_{file_path.name}"
            log_file_path = LOGS_DIR / log_file_name

            success = atomic_move(file_path, log_file_path)

            if success:
                self.logger.info(f"Rejected request moved to logs: {log_file_path}")
            else:
                self.logger.error(f"Failed to move rejected request: {file_path}")

        except Exception as e:
            self.logger.error(f"Error processing rejected request {file_path}: {e}")

    def _check_expired_requests(self):
        """
        Check for and handle expired approval requests in the pending directory
        """
        try:
            current_time = datetime.now()

            for file_path in PENDING_APPROVAL_DIR.glob("*.md"):
                approval_data = parse_approval_request(file_path)

                if approval_data and 'expires' in approval_data:
                    try:
                        expires_time = datetime.fromisoformat(
                            approval_data['expires'].replace('Z', '+00:00')
                        )

                        if current_time > expires_time:
                            self.logger.info(f"Found expired request: {file_path}")

                            # Move expired request to logs
                            timestamp = int(time.time())
                            log_file_name = f"expired_{timestamp}_{file_path.name}"
                            log_file_path = LOGS_DIR / log_file_name

                            success = atomic_move(file_path, log_file_path)

                            if success:
                                self.logger.info(f"Expired request moved to logs: {log_file_path}")
                            else:
                                self.logger.error(f"Failed to move expired request: {file_path}")

                    except ValueError:
                        self.logger.error(f"Invalid timestamp in approval request: {file_path}")

        except Exception as e:
            self.logger.error(f"Error checking for expired requests: {e}")

    def run(self):
        """
        Run the approval handler continuously
        """
        self.logger.info("Starting Approval Handler")
        self.logger.info(f"Monitoring: {APPROVED_DIR}")
        self.logger.info(f"Approved actions will move to: {LOGS_DIR}")
        self.logger.info(f"Rejected actions will move to: {LOGS_DIR}")

        # Create observer
        observer = Observer()
        observer.schedule(self, str(APPROVED_DIR), recursive=False)

        # Start the observer
        observer.start()

        self.logger.info("Approval Handler started successfully")

        try:
            while self.running:
                # Check for expired requests periodically
                self._check_expired_requests()

                # Sleep for a bit to avoid excessive CPU usage
                time.sleep(30)  # Check for expired requests every 30 seconds

        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received, shutting down...")
        finally:
            observer.stop()
            observer.join()
            self.logger.info("Approval Handler stopped")


def main():
    """
    Main entry point for the approval handler
    """
    handler = ApprovalHandler()
    handler.run()


if __name__ == "__main__":
    main()