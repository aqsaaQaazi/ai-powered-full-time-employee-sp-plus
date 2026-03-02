# SKILL_TestWatcher

## Purpose
Provides instructions and methodology for testing the File System Watcher functionality.

## Prompt Logic
Use this skill to test the filesystem_watcher.py script to ensure it properly monitors the /Inbox folder, detects new files, copies them to /Needs_Action, and creates appropriate metadata files.

## Testing Instructions

### Prerequisites
- Ensure filesystem_watcher.py is in the vault root
- Ensure /Inbox and /Needs_Action folders exist
- Have a test file ready to drop into /Inbox

### Steps to Test the File System Watcher:

1. **Start the watcher:**
   - Open terminal/command prompt in the vault directory
   - Run: `python filesystem_watcher.py`
   - The script will start monitoring the /Inbox folder

2. **Test file detection:**
   - While the watcher is running, create or copy a test file into the /Inbox folder
   - Example: Copy any text file or create a simple test.txt file in /Inbox

3. **Verify processing:**
   - Check that the file was copied to the /Needs_Action folder
   - Look for a corresponding .md metadata file with YAML frontmatter
   - Verify the metadata file contains proper information about the original file

4. **Check console output:**
   - The watcher should display messages confirming file detection and processing
   - Look for messages like "New file detected: filename" and "Copied filename to Needs_Action"

5. **Validate metadata:**
   - Open the generated .md file to confirm it has proper YAML frontmatter
   - Verify it contains file information like size, timestamps, and processing status

### Expected Results:
- Files dropped into /Inbox are automatically copied to /Needs_Action
- Matching metadata .md files are created with file information
- Console displays appropriate status messages during processing

### Troubleshooting:
- If the watcher doesn't detect files, verify the path settings in the script
- Ensure the script has proper read/write permissions for the folders
- Stop the watcher with Ctrl+C when testing is complete