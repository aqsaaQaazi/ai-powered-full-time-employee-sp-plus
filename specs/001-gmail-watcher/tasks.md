# Task List: Gmail Watcher

**Feature**: Gmail Watcher as second perception watcher
**Created**: 2026-03-03
**Status**: Draft
**Branch**: 001-gmail-watcher

## Phase 1: Setup

### Project Initialization
- [x] T001 Create project directory structure in gmail_watcher/
- [x] T002 [P] Create requirements.txt with dependencies: google-api-python-client, google-auth, google-auth-oauthlib, google-auth-httplib2
- [x] T003 [P] Create initial directory structure: config/, utils/, data/, Needs_Action/
- [x] T004 [P] Create __init__.py files in config/ and utils/ directories
- [x] T005 Create .gitignore with credentials.json, token.json, .processed_emails.json exclusions

## Phase 2: Foundational Components

### Base Infrastructure
- [x] T006 Create base configuration module in config/settings.py
- [x] T007 [P] Create authentication utilities in utils/auth.py
- [x] T008 [P] Create email processing utilities in utils/email_processor.py
- [x] T009 [P] Create file handling utilities in utils/file_handler.py
- [x] T010 Create BaseWatcher pattern implementation

## Phase 3: User Story 1 - Monitor Important Emails (Priority: P1)

### Goal: System can monitor an email account and identify important emails based on predefined keywords, creating actionable items without requiring manual checking.

### Independent Test: The system can monitor an email account and identify important emails containing keywords like "invoice", "urgent", "payment", "asap", "quote", or "help", creating actionable items without requiring manual checking.

### Implementation Tasks:
- [x] T011 [US1] Create main gmail_watcher.py file with basic structure
- [x] T012 [US1] Implement OAuth authentication flow in gmail_watcher.py
- [x] T013 [US1] Implement email polling mechanism with 120-second interval
- [x] T014 [US1] Implement Gmail API call to fetch unread important emails
- [x] T015 [US1] Create keyword detection algorithm for important emails (invoice, urgent, payment, asap, quote, help)
- [x] T016 [US1] Implement email metadata extraction (id, from, subject, received, snippet)
- [x] T017 [US1] Create priority determination based on keyword analysis
- [x] T018 [US1] Add error handling for API rate limits and network issues

## Phase 4: User Story 2 - Track Email Processing Status (Priority: P2)

### Goal: System maintains a record of processed email IDs and avoids reprocessing emails that have already been handled.

### Independent Test: The system maintains a record of processed email IDs and avoids reprocessing emails that have already been handled.

### Implementation Tasks:
- [x] T019 [US2] Create processed email tracking system in data/.processed_emails.json
- [x] T020 [US2] Implement loading of previously processed email IDs at startup
- [x] T021 [US2] Create function to check if email ID has been processed
- [x] T022 [US2] Update email processing to skip already processed emails
- [x] T023 [US2] Implement saving of processed email IDs after processing
- [x] T024 [US2] Add timestamp tracking for when log was last updated

## Phase 5: User Story 3 - Create Actionable Email Items (Priority: P3)

### Goal: System can convert important emails into structured markdown files with YAML metadata and suggested actions.

### Independent Test: The system can convert important emails into structured markdown files with YAML metadata and suggested actions.

### Implementation Tasks:
- [x] T025 [US3] Create markdown file creation function with YAML frontmatter
- [x] T026 [US3] Implement structured metadata inclusion: type: email, from, subject, received, priority, snippet
- [x] T027 [US3] Generate suggested actions checklist based on email content
- [x] T028 [US3] Create proper file naming convention: EMAIL_[id].md
- [x] T029 [US3] Implement creation of actionable items in /Needs_Action directory
- [x] T030 [US3] Validate markdown file format and YAML structure

## Phase 6: Cross-cutting Features

### Logging and Error Handling
- [x] T031 Implement comprehensive logging in gmail_watcher.py
- [x] T032 Add retry mechanisms for transient API failures
- [x] T033 Create error reporting for persistent issues
- [x] T034 Implement exponential backoff for API errors
- [x] T035 Add monitoring of API quota usage

### Security and Configuration
- [ ] T036 Implement file permission controls for credential files
- [ ] T037 Add environment variable support for configuration
- [ ] T038 Create secure credential initialization process
- [ ] T039 Implement validation for credential files
- [ ] T040 Add protection against logging credential information

### Testing and Validation
- [ ] T041 Create unit tests for email processing logic
- [ ] T042 Create unit tests for keyword detection algorithms
- [ ] T043 Create unit tests for file creation and YAML formatting
- [ ] T044 Create integration tests for end-to-end email processing
- [ ] T045 Validate that all user stories work independently

## Dependencies

### User Story Completion Order:
- User Story 1 (Monitor Important Emails) must be completed before User Story 3 (Create Actionable Email Items)
- User Story 2 (Track Email Processing Status) can be developed in parallel with User Story 1
- User Story 3 depends on both User Story 1 and User Story 2

### Blocking Dependencies:
- T001-T005 must be completed before any other tasks
- T006-T010 foundational components must be completed before user story tasks
- T011 requires foundational components to be completed
- T019-T024 (duplicate tracking) should be completed before T025-T030 (creating actionable items)

## Parallel Execution Opportunities

### Within User Story 1:
- T012 (authentication) and T013-T014 (polling/mechanism) can be developed in parallel
- T015 (keyword detection) and T016-T017 (metadata extraction/priority) can be developed in parallel

### Across User Stories:
- User Story 2 (tracking) can be developed in parallel with User Story 1 (monitoring)
- User Story 3 (actionable items) requires completion of User Story 1 and 2 but components can be developed once those are available

## Implementation Strategy

### MVP Approach:
- Focus on User Story 1 first to deliver core functionality
- Implement basic email monitoring and keyword detection
- Create simple markdown files without advanced features
- Add duplicate tracking (User Story 2) as second increment
- Complete actionable items with proper structure (User Story 3) as third increment

### Incremental Delivery:
- MVP: Basic email monitoring with keyword detection and simple file creation
- v1.1: Add duplicate tracking to prevent reprocessing
- v1.2: Enhance actionable items with proper YAML structure and suggested actions
- v1.3: Add comprehensive logging, error handling, and security features