#!/usr/bin/env python3
"""
Gmail Watcher - Monitors Gmail for important emails and creates actionable items

This script extends the BaseWatcher pattern to monitor Gmail accounts for
emails containing specific keywords and creates structured markdown files
in the Obsidian vault for human review and action.
"""

import os
import sys
import time
import logging
import signal
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from googleapiclient.errors import HttpError

from utils.auth import authenticate_gmail, validate_credentials
from utils.email_processor import (
    extract_email_metadata,
    detect_keywords,
    determine_priority,
    generate_suggested_actions
)
from utils.file_handler import (
    create_actionable_item,
    is_email_processed,
    mark_email_as_processed,
    load_processed_emails,
    save_processed_emails
)
from config.settings import (
    DEFAULT_POLL_INTERVAL,
    PROCESSED_EMAILS_PATH,
    KEYWORDS
)


class GmailWatcher:
    """
    Gmail Watcher implementation that monitors for important emails
    and creates actionable items based on predefined keywords.
    """

    def __init__(self, poll_interval: int = DEFAULT_POLL_INTERVAL):
        """
        Initialize the Gmail Watcher

        Args:
            poll_interval: Time in seconds between email checks (default: 120)
        """
        self.poll_interval = poll_interval
        self.service = None
        self.running = True
        self.processed_emails_path = PROCESSED_EMAILS_PATH

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gmail_watcher.log'),
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

    def initialize(self):
        """
        Initialize the Gmail Watcher by authenticating and loading state
        """
        self.logger.info("Initializing Gmail Watcher...")

        # Validate credentials
        if not validate_credentials():
            raise Exception("Failed to validate Gmail credentials")

        # Authenticate with Gmail API
        self.service = authenticate_gmail()
        self.logger.info("Successfully authenticated with Gmail API")

        # Load previously processed emails
        self.logger.info(f"Loading processed emails from {self.processed_emails_path}")

    def _fetch_new_emails(self) -> List[Dict[str, Any]]:
        """
        Fetch new important emails from Gmail

        Returns:
            List of email message objects
        """
        try:
            # Build search query for important, unread emails
            # We'll look for emails with our target keywords
            keyword_query = ' OR '.join(KEYWORDS)
            query = f'is:unread is:important ({keyword_query})'

            # Fetch messages
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=50  # Limit to prevent too many results at once
            ).execute()

            messages = results.get('messages', [])
            email_objects = []

            for msg in messages:
                try:
                    # Get full message details
                    message_detail = self.service.users().messages().get(
                        userId='me',
                        id=msg['id']
                    ).execute()

                    email_objects.append(message_detail)
                except HttpError as e:
                    self.logger.error(f"Error fetching message {msg['id']}: {e}")
                    continue

            self.logger.info(f"Fetched {len(email_objects)} new important emails")
            return email_objects

        except HttpError as e:
            self.logger.error(f"Gmail API error: {e}")
            # Implement retry logic for transient errors
            if e.resp.status in [429, 500, 503]:  # Rate limit or server errors
                self.logger.info(f"Waiting before retry due to API error: {e.resp.status}")
                time.sleep(30)  # Wait 30 seconds before retry
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error fetching emails: {e}")
            return []

    def _process_email(self, message_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single email message and return actionable data

        Args:
            message_data: Raw email data from Gmail API

        Returns:
            Processed email data or None if email should be skipped
        """
        try:
            # Extract metadata
            email_meta = extract_email_metadata(message_data)
            email_id = email_meta['id']

            # Check if email has already been processed
            if is_email_processed(email_id, self.processed_emails_path):
                self.logger.debug(f"Email {email_id} already processed, skipping")
                return None

            # Combine subject and snippet for keyword detection
            combined_text = f"{email_meta['subject']} {email_meta['snippet']}"

            # Detect keywords
            keywords_found = detect_keywords(combined_text)

            # Skip if no target keywords found
            if not keywords_found:
                self.logger.debug(f"No target keywords found in email {email_id}, skipping")
                return None

            # Determine priority
            priority = determine_priority(email_meta['snippet'], email_meta['subject'])

            # Generate suggested actions
            actions = generate_suggested_actions(priority, keywords_found)

            # Prepare processed email data
            processed_data = {
                **email_meta,
                'priority': priority,
                'keywords_found': keywords_found,
                'actions': actions
            }

            return processed_data

        except Exception as e:
            self.logger.error(f"Error processing email {message_data.get('id', 'unknown')}: {e}")
            return None

    def _create_actionable_item(self, email_data: Dict[str, Any]):
        """
        Create an actionable item from processed email data

        Args:
            email_data: Processed email data
        """
        try:
            file_path = create_actionable_item(email_data)
            self.logger.info(f"Created actionable item: {file_path}")

            # Mark email as processed
            mark_email_as_processed(email_data['id'], self.processed_emails_path)
            self.logger.debug(f"Marked email {email_data['id']} as processed")

        except Exception as e:
            self.logger.error(f"Error creating actionable item for email {email_data['id']}: {e}")

    def run_once(self):
        """
        Run a single iteration of email monitoring
        """
        try:
            # Fetch new emails
            emails = self._fetch_new_emails()

            # Process each email
            processed_count = 0
            for email in emails:
                if not self.running:
                    break

                processed_data = self._process_email(email)

                if processed_data:
                    self._create_actionable_item(processed_data)
                    processed_count += 1

            if processed_count > 0:
                self.logger.info(f"Processed {processed_count} new emails")
            else:
                self.logger.debug("No new emails to process")

        except Exception as e:
            self.logger.error(f"Error during email processing: {e}")

    def run(self):
        """
        Run the Gmail Watcher continuously
        """
        self.logger.info(f"Starting Gmail Watcher (poll interval: {self.poll_interval}s)")

        # Initialize the watcher
        try:
            self.initialize()
        except Exception as e:
            self.logger.error(f"Failed to initialize Gmail Watcher: {e}")
            return

        # Main monitoring loop
        iteration = 0
        while self.running:
            try:
                iteration += 1
                self.logger.info(f"Starting iteration #{iteration}")

                # Run a single monitoring cycle
                self.run_once()

                # Wait for the next polling interval
                if self.running:  # Only sleep if still running
                    self.logger.debug(f"Waiting {self.poll_interval} seconds until next check")
                    time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt received, shutting down...")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {e}")

                # Implement exponential backoff for errors
                retry_delay = min(300, 60 * (iteration % 10))  # Max 5 minutes
                self.logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

        self.logger.info("Gmail Watcher stopped")


def main():
    """
    Main entry point for the Gmail Watcher
    """
    # Check if configuration is provided via environment variables
    poll_interval_str = os.environ.get('POLL_INTERVAL', str(DEFAULT_POLL_INTERVAL))

    try:
        poll_interval = int(poll_interval_str)
        if poll_interval < 30:  # Minimum 30 seconds to respect API limits
            print("Warning: Poll interval too low, setting to minimum 30 seconds")
            poll_interval = 30
    except ValueError:
        print(f"Invalid POLL_INTERVAL value '{poll_interval_str}', using default {DEFAULT_POLL_INTERVAL}")
        poll_interval = DEFAULT_POLL_INTERVAL

    # Create and run the watcher
    watcher = GmailWatcher(poll_interval=poll_interval)

    try:
        watcher.run()
    except Exception as e:
        print(f"Fatal error running Gmail Watcher: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()