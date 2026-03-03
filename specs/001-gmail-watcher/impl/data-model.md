# Data Model: Gmail Watcher

## Email Entity
Represents a Gmail message retrieved from the API

**Attributes**:
- `id`: String - Unique Gmail message ID (immutable)
- `from`: String - Sender email address and name (e.g., "John Doe <john@example.com>")
- `subject`: String - Email subject line (max 255 chars)
- `received`: DateTime - Timestamp when email was received (ISO 8601 format)
- `priority`: String - Priority level ("high", "medium", "low") determined by keyword analysis
- `snippet`: String - Preview text from email body (max 500 chars)
- `keywords_found`: List<String> - Keywords that triggered the alert

**Validation Rules**:
- ID must be unique within the system
- From field must contain valid email format
- Received timestamp must be in the past
- Priority must be one of the allowed values

## Actionable Item Entity
Represents a markdown file created for human review and action

**Attributes**:
- `type`: String - Fixed value "email" (immutable)
- `from`: String - Email sender information (copied from Email entity)
- `subject`: String - Original email subject (copied from Email entity)
- `received`: DateTime - When email was received (copied from Email entity)
- `priority`: String - Determined from keyword analysis (copied from Email entity)
- `snippet`: String - Email preview text (copied from Email entity)
- `actions`: List<String> - Suggested actions for the user
- `created_at`: DateTime - When the actionable item was created
- `status`: String - Current status ("pending", "in_progress", "completed")

**Validation Rules**:
- Type must be "email"
- All email fields must match the original Email entity
- Actions list must contain at least one item
- Status must be one of the allowed values

## Processed Email Log Entity
Tracks processed email IDs to prevent duplicate processing

**Attributes**:
- `processed_ids`: Array<String> - Collection of processed email IDs
- `last_updated`: DateTime - When the log was last updated (ISO 8601 format)
- `version`: String - Schema version for the log format

**Validation Rules**:
- Processed IDs must be unique within the collection
- Last updated timestamp must be current or past
- Version must follow semantic versioning

## State Transitions

### Actionable Item States
- `pending` → `in_progress`: When user begins working on the item
- `in_progress` → `completed`: When user marks the item as done
- `pending` → `completed`: When user directly marks as completed

## Relationships
- One Email entity creates one Actionable Item entity
- Many Email entities can be tracked in one Processed Email Log entity
- Processed Email Log ensures uniqueness of Email processing