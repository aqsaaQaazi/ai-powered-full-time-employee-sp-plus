# SKILL_VaultIO

## Purpose
Provides functionality for reading and writing files in the Obsidian vault, including testing file operations.

## Prompt Logic
Use this skill to test and perform read/write operations in the vault. This includes reading existing files, creating new files in specific locations, and verifying that file operations work correctly.

## Instructions
1. Read existing files by specifying their full path using the Read function
2. Create new files by specifying the full path and content using the Write function
3. Verify operations by reading back the created files
4. Use appropriate folder locations (Inbox, Needs_Action, Done) for file placement

## Template for Testing Read/Write:
1. Read the contents of existing files in the vault
2. Create a test file in a specific folder (e.g., /Done) with test content
3. Read back the created file to confirm successful write operation
4. Output the contents of all relevant files to confirm operations

## Example Operations:
- Read: Use Read function with full file path
- Write: Use Write function with full file path and desired content
- Verify: Read back the written file to confirm content accuracy