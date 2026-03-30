# Agent Context Update: Approval Workflow

## Technologies Added
- watchdog: For efficient file system monitoring
- PyYAML: For parsing YAML frontmatter in approval requests
- File system operations: For managing approval workflow directories

## New Patterns
- File-based approval workflow pattern
- Directory-state management pattern
- Human-in-the-loop action approval pattern
- Watchdog-based file monitoring pattern

## Key Integrations
- Claude reasoning loop integration points
- MCP (Model Context Protocol) action execution
- File system-based state management

## File Locations
- approval_handler.py: Main approval workflow handler
- Pending_Approval/: Directory for pending approval requests
- Approved/: Directory for approved actions
- Rejected/: Directory for rejected actions
- Logs/: Directory for processed action logs
- utils/: Utility modules for file operations, parsing, and execution
- config/: Configuration management