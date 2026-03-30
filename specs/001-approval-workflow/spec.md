# Feature Specification: Approval Workflow

**Feature Branch**: `001-approval-workflow`
**Created**: 2026-03-03
**Status**: Draft
**Input**: User description: "Feature: Human-in-the-Loop Approval Workflow for sensitive actions
Requirements:
- When Claude needs to perform a sensitive action (send email, reply to email, post on social media, payment draft, etc.):
  - Create a file in /Pending_Approval/[ACTION_TYPE]_[unique_id].md
  - Unique ID: timestamp or message/email ID
  - File content:
    - YAML frontmatter: type: approval_request, action: email_send / linkedin_post / etc., details (to, subject, body_preview, amount, reason), created: ISO timestamp, expires: +24h
    - Markdown body: human-readable summary of action, "To approve: move this file to /Approved folder", "To reject: move to /Rejected"
- Folders: create /Pending_Approval, /Approved, /Rejected if missing
- Claude reasoning loop must check /Approved and /Rejected before proceeding
- Approval handler: lightweight script (approval_handler.py) that watches /Approved folder using watchdog (like filesystem watcher)
  - When file moved to /Approved: trigger MCP or log "execute action"
  - Move file to permanent log after processing"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Request Sensitive Action Approval (Priority: P1)

As a user, I want Claude to create approval requests for sensitive actions so that I can review and authorize actions like sending emails, making payments, or posting on social media before they occur.

**Why this priority**: Critical for maintaining security and preventing unauthorized actions that could have serious consequences.

**Independent Test**: When Claude needs to perform a sensitive action, it creates an approval request file that can be reviewed and either approved or rejected by a human.

**Acceptance Scenarios**:

1. **Given** Claude needs to send an email, **When** the system detects this sensitive action, **Then** it creates an approval request file in /Pending_Approval with appropriate metadata.
2. **Given** Claude needs to post on social media, **When** the system detects this sensitive action, **Then** it creates an approval request file with appropriate metadata.
3. **Given** Claude needs to draft a payment, **When** the system detects this sensitive action, **Then** it creates an approval request file with appropriate metadata.

---

### User Story 2 - Manage Approval Requests (Priority: P2)

As a user, I want to be able to approve or reject pending actions by moving files between folders so that I have full control over which sensitive actions are executed.

**Why this priority**: Essential for the approval workflow to function as intended.

**Independent Test**: Users can move approval request files between /Pending_Approval, /Approved, and /Rejected folders to control which actions are executed.

**Acceptance Scenarios**:

1. **Given** an approval request file exists in /Pending_Approval, **When** I move it to /Approved, **Then** the associated action is executed.
2. **Given** an approval request file exists in /Pending_Approval, **When** I move it to /Rejected, **Then** the associated action is cancelled.
3. **Given** an approval request file exists in /Pending_Approval, **When** it reaches its expiration time, **Then** it is automatically handled according to default policy.

---

### User Story 3 - Monitor Approval Status (Priority: P3)

As a user, I want to be able to track the status of my approval requests so that I can follow up on actions that have been approved or rejected.

**Why this priority**: Important for accountability and tracking purposes.

**Independent Test**: The system maintains logs of all approval requests and their final status (approved, rejected, expired).

**Acceptance Scenarios**:

1. **Given** an action was approved, **When** I check the logs, **Then** I can see that the action was executed successfully.
2. **Given** an action was rejected, **When** I check the logs, **Then** I can see that the action was cancelled.
3. **Given** an action expired, **When** I check the logs, **Then** I can see that the action was not executed due to expiration.

---

### Edge Cases

- What happens when the approval system is unavailable or fails?
- How does the system handle approval requests that exceed their expiration time?
- What occurs when multiple users attempt to approve or reject the same request?
- How does the system handle malformed approval request files?
- What happens when required directories (/Pending_Approval, /Approved, /Rejected) cannot be created?
- How does the system handle concurrent approval requests?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create approval request files in /Pending_Approval/[ACTION_TYPE]_[unique_id].md format when sensitive actions are detected
- **FR-002**: System MUST include YAML frontmatter in approval request files with: type: approval_request, action: action_type, details (to, subject, body_preview, amount, reason), created: ISO timestamp, expires: +24h
- **FR-003**: System MUST include human-readable markdown content in approval request files with action summary and instructions
- **FR-004**: System MUST automatically create /Pending_Approval, /Approved, and /Rejected directories if they don't exist
- **FR-005**: System MUST monitor /Approved folder for new files using a filesystem watcher
- **FR-006**: System MUST execute the requested action when an approval request file is moved to /Approved
- **FR-007**: System MUST log the execution of approved actions for audit purposes
- **FR-008**: System MUST handle rejection when approval request files are moved to /Rejected
- **FR-009**: System MUST process approval requests in a secure manner without exposing sensitive information
- **FR-010**: System MUST handle file operations atomically to prevent corruption
- **FR-011**: System MUST validate approval request files before processing to ensure they contain required information
- **FR-012**: System MUST provide default handling for expired approval requests

### Key Entities

- **Approval Request**: A markdown file representing a sensitive action that requires human approval, containing YAML metadata and human-readable content
- **Action Type**: Category of sensitive action (email_send, linkedin_post, payment_draft, etc.) that determines how the action is processed
- **Unique ID**: Identifier for approval requests based on timestamp or message/email ID to ensure uniqueness
- **Approval Directories**: Three folders (/Pending_Approval, /Approved, /Rejected) that manage the approval workflow state
- **Approval Handler**: Background process that monitors approval directories and executes actions when requests are approved

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The system successfully creates approval request files for 100% of detected sensitive actions within 1 second of detection
- **SC-002**: The system processes approved actions within 5 seconds of moving an approval request to the /Approved folder
- **SC-003**: The system maintains 99.9% uptime for the approval workflow monitoring service
- **SC-004**: Users report 90% satisfaction with the approval workflow process based on ease of use and clarity of information
- **SC-005**: The system successfully handles 99.5% of approval requests without errors or data corruption

### Assumptions

- Users will have appropriate file system permissions to move files between directories
- The system will have access to MCP (Model Context Protocol) or equivalent to execute actions
- The filesystem watcher will reliably detect file movements between directories
- Users will review approval requests within the 24-hour expiration window

### Dependencies

- File system access for creating and monitoring directories
- MCP (Model Context Protocol) or equivalent for executing approved actions
- File system watcher library for monitoring directory changes

### Constraints

- Approval requests must expire within 24 hours to prevent stale requests
- Sensitive information in approval requests must be handled securely
- The system must not execute actions without explicit approval
- Approval requests must be processed in the order they are approved