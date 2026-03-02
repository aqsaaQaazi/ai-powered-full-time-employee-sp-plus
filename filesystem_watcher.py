import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileDropHandler(FileSystemEventHandler):
    """Handles file system events for the drop folder."""

    def __init__(self, drop_folder, processing_folder):
        self.drop_folder = Path(drop_folder)
        self.processing_folder = Path(processing_folder)

    def on_created(self, event):
        """Handle file creation events in the drop folder."""
        if event.is_directory:
            return

        src_path = Path(event.src_path)
        print(f"New file detected: {src_path.name}")

        # Copy file to Needs_Action folder
        dest_path = self.processing_folder / src_path.name
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_path.name} to {self.processing_folder}")

        # Create metadata file
        self.create_metadata(src_path, dest_path)

        # Optionally, move original to archive after processing
        # archive_path = self.drop_folder / "archive" / src_path.name
        # archive_path.parent.mkdir(exist_ok=True)
        # shutil.move(src_path, archive_path)

    def create_metadata(self, src_path, dest_path):
        """Create metadata .md file for the processed file."""
        metadata_content = f"""---
title: "{dest_path.stem} - Metadata"
created: {time.strftime('%Y-%m-%d %H:%M:%S')}
original_location: "{src_path}"
processed_location: "{dest_path}"
status: "needs_action"
---

## File Information
- **Original Name:** {src_path.name}
- **Size:** {src_path.stat().st_size} bytes
- **Created:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(src_path.stat().st_ctime))}
- **Modified:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(src_path.stat().st_mtime))}

## Processing Details
- **Action Taken:** Copied from Inbox to Needs_Action
- **Status:** Ready for processing
"""

        # Create metadata file with same name but .md extension
        metadata_path = dest_path.with_suffix('.md')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write(metadata_content)
        print(f"Created metadata file: {metadata_path.name}")


def start_filesystem_watcher():
    """Start the filesystem watcher to monitor the drop folder."""
    drop_folder = "./Inbox"
    processing_folder = "./Needs_Action"

    # Create folders if they don't exist
    Path(drop_folder).mkdir(exist_ok=True)
    Path(processing_folder).mkdir(exist_ok=True)

    event_handler = FileDropHandler(drop_folder, processing_folder)
    observer = Observer()
    observer.schedule(event_handler, drop_folder, recursive=False)

    print(f"Starting file system watcher...")
    print(f"Monitoring: {drop_folder}")
    print(f"Processing to: {processing_folder}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping file system watcher...")
    observer.join()


if __name__ == "__main__":
    start_filesystem_watcher()