# Implementation Plan: Approval Workflow

**Feature**: Human-in-the-Loop Approval Workflow for sensitive actions
**Created**: 2026-03-03
**Status**: Draft
**Branch**: 001-approval-workflow

## Technical Context

### Architecture Overview
The Approval Workflow system implements a file-based human-in-the-loop approval mechanism for sensitive actions. Rather than relying on external services, the system uses a filesystem-based approach where approval requests are created as markdown files in specific directories. The system includes a background handler that monitors for approved actions and executes them accordingly.

### Technology Stack
- **Language**: Python 3.9+
- **File Watching**: watchdog library for monitoring directory changes
- **Configuration**: YAML files for approval request metadata
- **Logging**: Python logging module with configurable levels
- **File Operations**: Standard Python os/pathlib modules for filesystem operations

### Core Components
- **approval_handler.py**: Main background handler that monitors /Approved folder
- **watchdog**: File system event monitoring for detecting file moves
- **/Pending_Approval/**: Directory for pending approval requests
- **/Approved/**: Directory for approved actions to be executed
- **/Rejected/**: Directory for rejected actions
- **/Logs/**: Directory for permanent logs of processed actions

### Dependencies
- watchdog
- PyYAML
- python-dotenv (for environment management)

## Constitution Check

### Local-First Architecture Compliance
✅ All approval requests stored locally as markdown files
✅ No external services required for approval workflow
✅ Data remains under user control at all times

### Human-in-the-Loop Safety
✅ All sensitive actions require explicit human approval
✅ Clear instructions provided in approval request files
✅ Audit trail maintained for all actions taken

### Modularity Through Agent Skills
✅ Approval handler implemented as standalone component
✅ Clear interfaces for integration with Claude reasoning loop
✅ Independent from other system components

### Persistent Watcher Architecture
✅ Continuous monitoring through background Python script
✅ Resilient to system interruptions with restart capability
✅ Lightweight implementation suitable for background operation

### Obsidian-Centric Workflow
✅ Creates markdown files with YAML frontmatter in structured directories
✅ All approval requests stored as Obsidian-compatible markdown
✅ Follows Obsidian conventions for metadata and organization

### Security-First Design
✅ Sensitive actions require explicit approval before execution
✅ File-based approach reduces attack surface
✅ Proper error handling and logging implemented

## Phase 0: Research & Unknown Resolution

### Research Areas Identified
1. **Watchdog Implementation**: Best practices for using watchdog to monitor directory changes
2. **File Operation Safety**: Atomic file operations to prevent corruption during concurrent access
3. **MCP Integration**: Patterns for integrating with Claude reasoning loop and triggering MCP actions
4. **Security Considerations**: Safe handling of sensitive information in approval request files

### Implementation Decisions

#### Decision: File-Based Approval System
**Rationale**: A file-based approach provides simplicity, reliability, and local control without requiring external services. Users can interact with approval requests using familiar file system operations.

**Alternatives Considered**:
- Database-backed approval queue: More complex to set up and maintain
- Web-based approval interface: Requires additional infrastructure and authentication
- Email-based approvals: Less integrated with the local workflow

#### Decision: Watchdog for File Monitoring
**Rationale**: The watchdog library provides efficient, cross-platform file system monitoring with low resource usage, ideal for continuously running background processes.

**Alternatives Considered**:
- Polling-based monitoring: Higher resource usage and potential delays
- Native OS event systems: Less portable across platforms
- Third-party file sync services: Would require external dependencies

#### Decision: Directory-Based State Management
**Rationale**: Using separate directories (/Pending_Approval, /Approved, /Rejected) provides a clear, intuitive workflow that users can interact with using standard file operations.

**Alternatives Considered**:
- File extensions to indicate state: Less visible to users
- Embedded state in filenames: More complex parsing required
- Additional metadata files: Adds complexity without clear benefits

## Phase 1: Design & Contracts

### Data Models

#### Approval Request Entity
- **filename**: String - Unique filename in format [ACTION_TYPE]_[unique_id].md
- **type**: String - Fixed value "approval_request"
- **action**: String - Action type (email_send, linkedin_post, payment_draft, etc.)
- **details**: Object - Contains action-specific details (to, subject, body_preview, amount, reason)
- **created**: DateTime - When the request was created (ISO 8601 format)
- **expires**: DateTime - When the request expires (ISO 8601 format, +24h from created)
- **status**: String - Current status ("pending", "approved", "rejected", "expired")

**Validation Rules**:
- Filename must follow [ACTION_TYPE]_[unique_id].md format
- Type must be "approval_request"
- Action must be one of the defined action types
- Created timestamp must be in the past
- Expiration must be within 24 hours of creation
- Status must be one of the allowed values

#### Action Type Entity
- **name**: String - Name of the action type (email_send, linkedin_post, payment_draft, etc.)
- **handler**: String - Name of the handler function to process this action type
- **required_details**: List<String> - Required detail fields for this action type

**Validation Rules**:
- Name must be unique
- Handler must correspond to an existing handler function
- Required details must be present in approval request details

### API Contracts

#### File System Interface
- **Input**: Approval request files in /Pending_Approval/ directory
- **Output**: Processed action results in /Logs/ directory
- **State**: /Pending_Approval/, /Approved/, /Rejected/ directories for workflow management

#### MCP Integration Points
- **Trigger**: When approval request moved to /Approved/
- **Action**: Execute the requested action via MCP
- **Callback**: Move processed file to /Logs/ with status information

### Code Structure

```
approval_workflow/
├── approval_handler.py          # Main handler implementation
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration management
├── utils/
│   ├── __init__.py
│   ├── file_operations.py      # Safe file operations
│   ├── approval_parser.py      # Parse approval request files
│   └── action_executor.py      # Execute approved actions
├── Pending_Approval/           # Pending approval requests
├── Approved/                   # Approved actions
├── Rejected/                   # Rejected actions
└── Logs/                       # Processed action logs
    └── [ACTION_TYPE]_[id]_processed.md
```

### Example Approval File Template

```
---
type: approval_request
action: email_send
details:
  to: recipient@example.com
  subject: Important Business Proposal
  body_preview: Hello, I'd like to discuss a business opportunity...
  amount: null
  reason: Business development outreach
created: 2026-03-03T10:30:00Z
expires: 2026-03-04T10:30:00Z
---
# Approval Request: Send Email

**Action**: Send Email
**To**: recipient@example.com
**Subject**: Important Business Proposal
**Preview**: Hello, I'd like to discuss a business opportunity...

## Details
- **Reason**: Business development outreach
- **Created**: 2026-03-03 10:30:00 UTC
- **Expires**: 2026-03-04 10:30:00 UTC

## To Approve
Move this file to the `/Approved` folder to execute this action.

## To Reject
Move this file to the `/Rejected` folder to cancel this action.
```

### Integration with Claude Reasoning Loop
- Check /Approved and /Rejected directories before proceeding with sensitive actions
- Create approval request files when sensitive actions are detected
- Monitor for processed files in /Logs/ to track action status

## Phase 2: Implementation Plan

### Task 1: Set up directory structure and configuration
- Create required directories: /Pending_Approval, /Approved, /Rejected, /Logs
- Implement configuration management in config/settings.py
- Set up logging infrastructure

### Task 2: Implement file operations utilities
- Create safe file operations in utils/file_operations.py
- Implement atomic file operations to prevent corruption
- Add file validation functions

### Task 3: Implement approval parser
- Create approval request parser in utils/approval_parser.py
- Validate approval request structure and content
- Extract action details from YAML frontmatter

### Task 4: Implement action executor
- Create action executor in utils/action_executor.py
- Implement handlers for different action types
- Integrate with MCP for executing actions

### Task 5: Create approval handler main loop
- Implement main approval handler in approval_handler.py
- Use watchdog to monitor /Approved directory
- Process approved requests and execute actions
- Move processed files to /Logs directory

### Task 6: Add error handling and security features
- Implement comprehensive error handling
- Add security checks for sensitive information
- Create expiration handling for approval requests

## Security Considerations

### Sensitive Information Protection
- Sanitize sensitive data in approval request files
- Implement proper access controls for approval directories
- Never log sensitive credentials or personal information

### File Operation Security
- Validate file contents before processing
- Implement proper file permission controls
- Prevent path traversal vulnerabilities

### Action Execution Security
- Validate action parameters before execution
- Implement rate limiting for action execution
- Log all executed actions for audit purposes

## Testing Strategy

### Unit Tests
- Test file operation utilities
- Validate approval request parsing
- Verify action execution logic

### Integration Tests
- Test directory monitoring functionality
- Validate approval request processing pipeline
- Verify MCP integration

### Security Tests
- Test for path traversal vulnerabilities
- Validate input sanitization
- Verify access controls