# Research Document: Gmail Watcher Implementation

## Decision: Gmail API Setup Process
**Rationale**: OAuth 2.0 is the only supported authentication method for Gmail API v1. The setup requires creating a Google Cloud Project, enabling the Gmail API, and configuring OAuth 2.0 credentials.

**Implementation Steps**:
1. Create Google Cloud Project
2. Enable Gmail API
3. Configure OAuth consent screen with required scopes
4. Create OAuth 2.0 client credentials
5. Download credentials.json
6. Implement initial authentication flow

## Decision: Email Search Parameters
**Rationale**: Gmail API supports rich query syntax for finding emails. Using `is:unread is:important` combined with keyword searches efficiently identifies important emails.

**Query Patterns**:
- `is:unread is:important` - Unread important emails
- `is:unread subject:(invoice OR urgent OR payment OR asap OR quote OR help)` - Keyword search in subjects
- Combined query for optimal filtering

## Decision: Rate Limiting Strategy
**Rationale**: Gmail API has quotas that vary by user type. Understanding these limits prevents service disruptions.

**Limits**:
- Standard users: 1,000 requests per day
- Google Workspace users: Higher quotas depending on license
- Polling every 120 seconds uses ~720 requests/day, staying within limits

## Decision: Authentication Storage
**Rationale**: For local applications, storing credentials securely while maintaining usability is critical.

**Pattern**:
- Store credentials.json outside Obsidian vault
- Use token.json for access tokens (created after first auth)
- Implement proper file permissions