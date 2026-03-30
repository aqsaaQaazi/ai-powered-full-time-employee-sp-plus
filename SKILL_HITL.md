# Human-in-the-Loop Approval (HITL) Skill

## Overview
The HITL Approval Workflow enables human oversight for sensitive actions by creating a file-based approval system. When Claude needs to perform sensitive actions, it creates approval request files that users can review and approve or reject by moving them between directories.

## Directory Structure
- `/Pending_Approval/` - Contains approval requests awaiting review
- `/Approved/` - Contains requests that have been approved for execution
- `/Rejected/` - Contains requests that have been rejected
- `/Logs/` - Contains logs of processed requests

## Usage

### Creating Approval Requests
When Claude needs to perform a sensitive action, create an approval request file in the `/Pending_Approval/` directory with the following structure:

```markdown
---
type: approval_request
action: email_send  # Supported: email_send, linkedin_post, payment_draft, social_media_post, file_share, api_call
details:
  to: recipient@example.com  # For email_send
  subject: Subject of email
  body_preview: Preview of the email body...
  amount: 100.00  # For payment_draft
  reason: Why this action is needed
created: 2026-03-03T10:30:00Z  # ISO 8601 format
expires: 2026-03-04T10:30:00Z  # Expires in 24 hours
---
# Approval Request: [Action Type]

**Action**: [Action Type]
**To**: [Recipient if applicable]
**Subject**: [Subject if applicable]
**Preview**: [Brief preview of content...]

## Details
- **Reason**: [Explanation of why action is needed]
- **Created**: [Creation timestamp]
- **Expires**: [Expiration timestamp]

## To Approve
Move this file to the `/Approved` folder to execute this action.

## To Reject
Move this file to the `/Rejected` folder to cancel this action.
```

### Processing Requests
1. **To Approve**: Move the approval request file from `/Pending_Approval/` to `/Approved/`
2. **To Reject**: Move the approval request file from `/Pending_Approval/` to `/Rejected/`
3. **Automatic Expiration**: Requests in `/Pending_Approval/` that exceed 24 hours will be automatically moved to `/Logs/` with an "expired" status

### Running the Approval Handler
Start the approval handler to monitor for approved/rejected requests:

```bash
python approval_handler.py
```

The handler will:
- Monitor the `/Approved/` directory for new files
- Execute approved actions when files are detected
- Move processed files to the `/Logs/` directory
- Maintain logs of all executed actions

## Supported Action Types

### email_send
- **Required Details**: `to`, `subject`, `body_preview`
- **Execution**: Simulates sending an email (in full implementation, would connect to email service)

### linkedin_post
- **Required Details**: `content_preview`, `audience`
- **Execution**: Simulates creating a LinkedIn post

### payment_draft
- **Required Details**: `amount`, `recipient`, `reason`
- **Execution**: Simulates drafting a payment

### social_media_post
- **Required Details**: `platform`, `content_preview`
- **Execution**: Simulates creating a social media post

### file_share
- **Required Details**: `recipient`, `file_path`, `permissions`
- **Execution**: Simulates sharing a file

### api_call
- **Required Details**: `endpoint`, `method`, `payload_preview`
- **Execution**: Simulates making an API call

## Integration with Claude Reasoning Loop

### Checking Approval Status
Before performing sensitive actions, Claude should check the approval directories:

```python
from pathlib import Path

def check_pending_approvals():
    """Check for processed approvals and rejections"""
    approved_files = list(Path("Approved").glob("*.md"))
    rejected_files = list(Path("Rejected").glob("*.md"))

    # Process completed requests as needed
    for file_path in approved_files:
        # Handle approved action
        pass

    for file_path in rejected_files:
        # Handle rejected action
        pass
```

### Creating Approval Requests
When Claude needs to perform a sensitive action:

```python
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import yaml

def create_approval_request(action_type, details, markdown_body):
    """Create an approval request file"""
    # Calculate expiration (24 hours from now)
    created_time = datetime.now()
    expires_time = created_time + timedelta(hours=24)

    # Create the approval request data
    approval_data = {
        'type': 'approval_request',
        'action': action_type,
        'details': details,
        'created': created_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'expires': expires_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    # Create the file content
    content = f"""---
{yaml.dump(approval_data, default_flow_style=False)}
---
{markdown_body}
"""

    # Generate unique filename
    unique_id = str(uuid.uuid4())
    filename = f"{action_type}_{unique_id}.md"
    file_path = Path("Pending_Approval") / filename

    # Write the file
    with open(file_path, 'w') as f:
        f.write(content)

    return file_path
```

## Configuration
The system can be configured using environment variables:

- `PENDING_APPROVAL_DIR`: Directory for pending approvals (default: ./Pending_Approval)
- `APPROVED_DIR`: Directory for approved requests (default: ./Approved)
- `REJECTED_DIR`: Directory for rejected requests (default: ./Rejected)
- `LOGS_DIR`: Directory for processed logs (default: ./Logs)
- `APPROVAL_EXPIRATION_HOURS`: Hours before approval requests expire (default: 24)
- `WATCHDOG_TIMEOUT`: Timeout for file system monitoring (default: 1.0)

## Security Considerations
- Approval requests may contain sensitive information; handle with care
- The system validates file paths to prevent directory traversal
- All actions are logged for audit purposes
- Expired requests are automatically handled to prevent stale approvals