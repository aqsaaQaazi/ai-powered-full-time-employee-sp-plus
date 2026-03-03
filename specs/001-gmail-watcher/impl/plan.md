# Implementation Plan: Gmail Watcher

**Feature**: Gmail Watcher as second perception watcher
**Created**: 2026-03-03
**Status**: Draft
**Branch**: 001-gmail-watcher

## Technical Context

### Architecture Overview
The Gmail Watcher will be implemented as a persistent Python script that extends the BaseWatcher pattern. It will periodically poll Gmail for important emails, process them based on predefined keywords, and create actionable items in the Obsidian vault.

### Technology Stack
- **Language**: Python 3.9+
- **Gmail API Client**: google-api-python-client
- **OAuth Library**: google-auth, google-auth-oauthlib, google-auth-httplib2
- **Configuration**: JSON files for processed email tracking
- **Logging**: Python logging module with configurable levels
- **Scheduling**: Built-in time.sleep() for polling interval control

### Core Components
- **gmail_watcher.py**: Main watcher script extending BaseWatcher
- **credentials.json**: OAuth credentials for Gmail API access
- **.processed_emails.json**: Track processed email IDs to prevent duplicates
- **/Needs_Action/**: Directory for created actionable items
- **Configurable polling interval**: Default 120 seconds

### Dependencies
- google-api-python-client
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- python-dotenv (for environment management)

## Constitution Check

### Local-First Architecture Compliance
✅ All email processing results stored locally in Obsidian vault
✅ Credentials managed securely with proper storage outside vault
✅ No external data storage required beyond Gmail API

### Human-in-the-Loop Safety
✅ Important emails flagged for human review before action
✅ Actionable items created as markdown files for human approval
✅ No automated responses sent without human approval

### Modularity Through Agent Skills
✅ Will be implemented as a reusable watcher component
✅ Clear interface following BaseWatcher pattern
✅ Independent from other system components

### Persistent Watcher Architecture
✅ Continuous monitoring through background Python script
✅ Resilient to network interruptions with retry logic
✅ Lightweight implementation suitable for background operation

### Obsidian-Centric Workflow
✅ Creates markdown files with YAML frontmatter in /Needs_Action directory
✅ All actionable items stored as Obsidian-compatible markdown
✅ Follows Obsidian conventions for metadata and linking

### Security-First Design
✅ OAuth 2.0 for secure Gmail API access
✅ Credentials stored separately from source code
✅ Proper error handling and logging implemented

## Phase 0: Research & Unknown Resolution

### Research Areas Identified
1. **Gmail API Setup Process**: OAuth 2.0 configuration steps for Gmail API access
2. **Email Search Parameters**: Best practices for identifying important emails with keywords
3. **Rate Limiting**: Gmail API rate limits and appropriate polling intervals
4. **Authentication Storage**: Secure credential storage patterns for local applications

### Implementation Decisions

#### Decision: Gmail API Client Libraries
**Rationale**: The official google-api-python-client is the recommended library for Gmail API integration, providing proper authentication, error handling, and API access patterns.

**Alternatives Considered**:
- IMAP libraries (python-imaplib): Less reliable, requires SMTP/IMAP access which may be disabled
- Third-party wrappers: Less stable and potentially unmaintained

#### Decision: Authentication Method
**Rationale**: OAuth 2.0 is the only supported authentication method for Gmail API v1, providing secure access with proper scopes.

**Alternatives Considered**:
- Application passwords: No longer supported for Gmail API
- Service accounts: Would require domain-level admin access

#### Decision: Polling Interval
**Rationale**: 120 seconds balances timely notification with API rate limits and resource usage.

**Alternatives Considered**:
- Push notifications: More complex implementation, requires public endpoint
- Real-time notifications: Gmail API supports push, but adds complexity for local-first architecture

#### Decision: Duplicate Prevention
**Rationale**: Local JSON file tracking processed email IDs is the simplest approach for preventing duplicate processing.

**Alternatives Considered**:
- Database storage: Overkill for this use case
- Gmail labels: Would require modifying user's email, could interfere with user workflow

## Phase 1: Design & Contracts

### Data Models

#### Email Entity
- **id**: String - Unique Gmail message ID
- **from**: String - Sender email address and name
- **subject**: String - Email subject line
- **received**: DateTime - Timestamp when email was received
- **priority**: String - Priority level (high/medium/low) based on keywords
- **snippet**: String - Preview text from email body

#### Actionable Item
- **type**: String - Fixed value "email"
- **from**: String - Email sender information
- **subject**: String - Original email subject
- **received**: DateTime - When email was received
- **priority**: String - Determined from keyword analysis
- **snippet**: String - Email preview text
- **actions**: List<String> - Suggested actions for the user

#### Processed Email Log
- **processed_ids**: Array<String> - Collection of processed email IDs
- **last_updated**: DateTime - When the log was last updated

### API Contracts

#### Gmail API Integration
- **Endpoint**: `https://www.googleapis.com/gmail/v1/users/me/messages`
- **Method**: GET with query parameters for search
- **Parameters**:
  - `q`: Search query (e.g., "is:unread is:important after:timestamp")
  - `maxResults`: Maximum number of results to return
- **Response**: List of message objects containing ID and metadata

#### File System Interface
- **Input**: credentials.json in project root
- **Output**: EMAIL_[id].md files in /Needs_Action/ directory
- **State**: .processed_emails.json for tracking processed items

### Code Structure

```
gmail_watcher/
├── gmail_watcher.py          # Main watcher implementation
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration management
├── utils/
│   ├── __init__.py
│   ├── auth.py              # Authentication helpers
│   ├── email_processor.py   # Email processing logic
│   └── file_handler.py      # File creation and management
├── data/
│   ├── .processed_emails.json  # Processed email tracking
│   └── credentials.json        # OAuth credentials
└── Needs_Action/            # Actionable items directory
    └── EMAIL_[id].md
```

### Vault Integration

#### Credentials Management
- Store credentials.json outside of Obsidian vault in a secure location
- Reference credentials path in environment variables or config
- Implement secure credential initialization process

#### Actionable Items Location
- Create /Needs_Action directory in Obsidian vault root
- Use YAML frontmatter for structured metadata
- Include suggested actions as markdown checklist

### Manual Setup Notes for API Credentials

#### Step 1: Enable Gmail API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "Dashboard"
4. Click "+ ENABLE APIS AND SERVICES"
5. Search for "Gmail API" and click on it
6. Click "ENABLE"

#### Step 2: Create OAuth 2.0 Credentials
1. In the Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "CREATE CREDENTIALS" > "OAuth client ID"
3. Choose "Desktop application" as the application type
4. Give it a name like "Gmail Watcher"
5. Download the credentials JSON file
6. Rename the downloaded file to `credentials.json`
7. Place it in your project directory (outside the Obsidian vault)

#### Step 3: Configure OAuth Consent Screen
1. In the Google Cloud Console, go to "APIs & Services" > "OAuth consent screen"
2. Select "External" user type and click "Create"
3. Fill in the app information:
   - App name: Gmail Watcher
   - User support email: your email
   - Developer contact information: your email
4. Add the following scopes under "Scopes for Google APIs":
   - https://www.googleapis.com/auth/gmail.readonly
   - https://www.googleapis.com/auth/gmail.modify
5. Save and continue

#### Step 4: First-time Authentication
1. Run the gmail_watcher.py script for the first time
2. The script will open a browser window for OAuth consent
3. Log in with the Gmail account you want to monitor
4. Grant the requested permissions
5. A token file (token.json) will be created for subsequent use

## Phase 2: Implementation Plan

### Task 1: Set up OAuth authentication
- Create auth module for handling OAuth flow
- Implement credential loading and token refresh
- Handle authentication errors gracefully

### Task 2: Implement email polling mechanism
- Create main watcher loop with configurable interval
- Implement Gmail API calls to fetch unread important emails
- Add error handling for API rate limits and network issues

### Task 3: Develop email processing logic
- Implement keyword detection for important emails
- Create logic to determine email priority based on keywords
- Build email metadata extraction

### Task 4: Create actionable items
- Implement markdown file creation with YAML frontmatter
- Generate suggested action checklists
- Ensure proper file naming convention

### Task 5: Implement duplicate prevention
- Create processed email tracking system
- Implement ID comparison to avoid duplicate processing
- Handle edge cases for tracking persistence

### Task 6: Add logging and error handling
- Implement comprehensive logging
- Add retry mechanisms for transient failures
- Create error reporting for persistent issues

## Security Considerations

### Credential Protection
- Store credentials.json outside of version control
- Implement file permission controls for credential files
- Never log credential information

### Rate Limiting
- Implement exponential backoff for API errors
- Respect Gmail API quotas and limits
- Monitor for rate limit warnings

### Data Privacy
- Only access emails with proper user consent
- Store processed data locally only
- Implement secure deletion patterns when needed

## Testing Strategy

### Unit Tests
- Test email processing logic
- Verify keyword detection algorithms
- Validate file creation and YAML formatting

### Integration Tests
- Mock Gmail API responses
- Test OAuth flow with mock credentials
- Verify end-to-end email-to-actionable-item pipeline

### Performance Tests
- Measure API call frequency vs rate limits
- Test memory usage during extended operation
- Validate polling interval effectiveness

## Deployment & Operations

### Configuration
- Support environment variables for customization
- Provide default configuration values
- Allow runtime configuration adjustments

### Monitoring
- Log operational metrics
- Track processing success/failure rates
- Monitor API quota usage

### Maintenance
- Regular cleanup of processed email logs
- Update handling for API changes
- Credential refresh automation