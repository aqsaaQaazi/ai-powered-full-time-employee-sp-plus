# Quickstart Guide: Approval Workflow

## Overview
The Approval Workflow system enables human-in-the-loop approval for sensitive actions by creating a file-based approval process. When Claude needs to perform sensitive actions, it creates approval request files that users can review and approve or reject by moving them between directories.

## Prerequisites
- Python 3.9 or higher
- pip package manager

## Setup

### 1. Install Dependencies
```bash
pip install watchdog PyYAML python-dotenv
```

### 2. Create Directory Structure
The system will automatically create the required directories, but you can create them manually:
```bash
mkdir -p Pending_Approval Approved Rejected Logs
```

### 3. Configure Settings (Optional)
Create a `.env` file to customize settings:
```env
APPROVAL_EXPIRATION_HOURS=24
PENDING_DIR=Pending_Approval
APPROVED_DIR=Approved
REJECTED_DIR=Rejected
LOGS_DIR=Logs
WATCHDOG_TIMEOUT=1.0
```

## Usage

### Starting the Approval Handler
```bash
python approval_handler.py
```

The handler will start monitoring the Approved directory for new approval requests.

### Creating Approval Requests
When Claude needs to perform a sensitive action, it should create a markdown file in the Pending_Approval directory with the following structure:

```markdown
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

### Approving Requests
To approve an action, simply move the approval request file from Pending_Approval to Approved:
```bash
mv Pending_Approval/email_send_12345.md Approved/
```

### Rejecting Requests
To reject an action, move the approval request file from Pending_Approval to Rejected:
```bash
mv Pending_Approval/email_send_12345.md Rejected/
```

## Expected Behavior

### When Approval Handler Runs
- Monitors the Approved directory for new files
- Executes approved actions when files are detected
- Moves processed files to the Logs directory
- Maintains logs of all executed actions

### During Normal Operation
- Files in Pending_Approval await user review
- Files moved to Approved trigger action execution
- Files moved to Rejected are logged as cancelled
- Processed files are archived in Logs directory

## Integration with Claude Reasoning Loop

To integrate with Claude's reasoning loop:

1. Before performing sensitive actions, check the Approved and Rejected directories for completed requests
2. Create approval request files when sensitive actions are detected
3. Monitor for processed files in the Logs directory to track action status

Example integration code:
```python
# Before performing sensitive action
def check_pending_approvals():
    # Scan Approved and Rejected directories
    # Process completed requests
    pass

def request_approval(action_type, details):
    # Create approval request file in Pending_Approval directory
    pass
```

## Troubleshooting

### Handler Not Responding
- Check that the handler script is running
- Verify directory paths are correct
- Check file permissions on approval directories

### Files Not Being Processed
- Ensure files are moved to the correct directories
- Verify YAML frontmatter is properly formatted
- Check handler logs for error messages

### Permission Errors
- Ensure the handler has read/write access to all approval directories
- Check that the user has appropriate permissions to move files between directories