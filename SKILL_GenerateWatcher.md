# SKILL_GenerateWatcher

## Purpose
Generates a Python script for a File System Watcher that monitors a drop folder, detects new files, copies them to a processing folder, and adds metadata.

## Prompt Logic
Use this skill to generate a complete filesystem watcher script that implements the following functionality:
- Monitors a specified drop folder (typically /Inbox)
- Detects new file creations
- Copies new files to a processing folder (typically /Needs_Action)
- Creates metadata .md files with information about the copied files
- Uses the watchdog library for file system monitoring

## Template Code Structure
The generated script should include:

1. Imports:
   - from watchdog.observers import Observer
   - from watchdog.events import FileSystemEventHandler
   - pathlib and shutil for file operations

2. A FileDropHandler class that extends FileSystemEventHandler with:
   - on_created event handler
   - create_metadata method

3. A start_filesystem_watcher function to initialize and run the watcher

## Implementation Details
- Monitor the /Inbox folder for new files
- Copy detected files to /Needs_Action folder
- Create accompanying .md metadata files with YAML frontmatter
- Include file information like size, timestamps, and processing status
- Handle file system events appropriately

## Instructions
1. Define the FileDropHandler class with event handling logic
2. Implement the on_created method to handle new file detection
3. Implement the create_metadata method to generate metadata files
4. Create a main function to start the observer
5. Include proper error handling and graceful shutdown