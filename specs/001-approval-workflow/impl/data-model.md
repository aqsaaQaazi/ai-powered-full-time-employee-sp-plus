# Data Model: Approval Workflow

## Approval Request Entity
Represents a pending approval request for a sensitive action

**Attributes**:
- `filename`: String - Unique filename in format [ACTION_TYPE]_[unique_id].md (immutable)
- `type`: String - Fixed value "approval_request" (immutable)
- `action`: String - Action type (email_send, linkedin_post, payment_draft, etc.)
- `details`: Object - Contains action-specific details:
  - `to`: String - Recipient (for email/social media actions)
  - `subject`: String - Subject/title of action (max 255 chars)
  - `body_preview`: String - Preview of content (max 500 chars)
  - `amount`: Number - Monetary amount (for payment actions, null otherwise)
  - `reason`: String - Justification for the action (max 255 chars)
- `created`: DateTime - When the request was created (ISO 8601 format)
- `expires`: DateTime - When the request expires (ISO 8601 format, +24h from created)
- `status`: String - Current status ("pending", "approved", "rejected", "expired")

**Validation Rules**:
- Filename must follow [ACTION_TYPE]_[unique_id].md format
- Type must be "approval_request"
- Action must be one of the defined action types
- Created timestamp must be in the past
- Expiration must be within 24 hours of creation
- Status must be one of the allowed values
- Required detail fields must be present based on action type

## Action Type Entity
Defines the types of actions that require approval

**Attributes**:
- `name`: String - Name of the action type (email_send, linkedin_post, payment_draft, etc.)
- `handler`: String - Name of the handler function to process this action type
- `required_details`: List<String> - Required detail fields for this action type
- `description`: String - Human-readable description of the action type

**Validation Rules**:
- Name must be unique
- Handler must correspond to an existing handler function
- Required details must be present in approval request details
- Description must be informative and clear

## Approval Directory State
Represents the state of approval workflow through directory placement

**Attributes**:
- `location`: String - Current directory location ("Pending_Approval", "Approved", "Rejected", "Logs")
- `moved_at`: DateTime - When the file was moved to current location
- `processed_result`: String - Result of processing (for files in Logs directory)

**Validation Rules**:
- Location must be one of the defined directories
- Moved timestamp must be current or past
- Processed result must be present for files in Logs directory

## Processed Action Log Entity
Represents a log of processed approval requests

**Attributes**:
- `original_filename`: String - Original filename of the approval request
- `action`: String - Action that was executed
- `result`: String - Result of the action execution ("success", "failed", "cancelled")
- `executed_at`: DateTime - When the action was executed
- `error_message`: String - Error details if action failed (optional)
- `executor`: String - Who executed the action (typically "system" for automated execution)

**Validation Rules**:
- Original filename must match the format of approval requests
- Result must be one of the allowed values
- Executed timestamp must be current or past
- Error message should only be present when result is "failed"

## State Transitions

### Approval Request States
- `pending` → `approved`: When user moves file to /Approved directory
- `pending` → `rejected`: When user moves file to /Rejected directory
- `pending` → `expired`: When current time exceeds expires timestamp
- `approved` → `processed`: When action is successfully executed
- `rejected` → `logged`: When rejection is processed and logged

## Relationships
- One Approval Request entity corresponds to one file in the approval directory system
- One Processed Action Log entity is created for each approved and executed action
- Multiple Approval Request entities can share the same Action Type
- Approval Directory State tracks the movement of Approval Request files through the workflow