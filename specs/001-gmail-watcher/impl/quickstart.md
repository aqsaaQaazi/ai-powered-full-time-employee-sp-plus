# Quickstart Guide: Gmail Watcher

## Prerequisites
- Python 3.9 or higher
- Google Account with Gmail access
- Google Cloud Platform project with Gmail API enabled

## Setup

### 1. Install Dependencies
```bash
pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

### 2. Prepare Environment
```bash
# Create the necessary directory structure
mkdir -p Needs_Action
```

### 3. Configure Gmail API Access
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials for desktop application
5. Download `credentials.json` and place in project root

### 4. Initialize the Watcher
```bash
# First run will initiate OAuth flow
python gmail_watcher.py
```

## Configuration

### Environment Variables
```bash
# Optional: Customize polling interval (default: 120 seconds)
export POLL_INTERVAL=120

# Optional: Path to credentials file (default: ./credentials.json)
export CREDENTIALS_PATH="./config/credentials.json"

# Optional: Directory for actionable items (default: ./Needs_Action/)
export ACTION_DIR="./Needs_Action/"
```

### File Locations
- `credentials.json`: OAuth credentials (keep secure)
- `.processed_emails.json`: Tracking log for processed emails
- `gmail_watcher.log`: Log file for monitoring

## Running the Watcher

### Start the Service
```bash
python gmail_watcher.py
```

The watcher will run continuously, polling Gmail every 120 seconds for important emails.

### Stop the Service
Press `Ctrl+C` to gracefully stop the watcher.

## Expected Behavior

### On Startup
- Authenticates with Gmail API
- Loads previously processed email IDs
- Begins polling cycle

### During Operation
- Checks for new important emails every 2 minutes
- Identifies emails with keywords: invoice, urgent, payment, asap, quote, help
- Creates markdown files in `Needs_Action/` directory
- Tracks processed email IDs to prevent duplicates

### Sample Output
When an important email is found, creates a file like:
```
Needs_Action/EMAIL_abcdef123456.md
```

With content:
```yaml
---
type: email
from: John Doe <john@example.com>
subject: Urgent Payment Required
received: 2026-03-03T10:30:00Z
priority: high
snippet: Please process the attached invoice immediately...
---
# Urgent Payment Required

From: John Doe <john@example.com>
Received: 2026-03-03 10:30:00

## Suggested Actions
- [ ] Review invoice details
- [ ] Process payment
- [ ] Respond to sender
- [ ] Update accounting records
```

## Troubleshooting

### Authentication Issues
- Ensure `credentials.json` is properly formatted
- Check that the OAuth consent screen is configured correctly
- Reauthorize if getting access errors

### Rate Limits
- Default 120-second interval should stay within limits
- Reduce polling frequency if hitting rate limits

### Missing Emails
- Verify the Gmail account has the correct filters
- Check that emails are marked as "important" in Gmail
- Ensure keywords match email content