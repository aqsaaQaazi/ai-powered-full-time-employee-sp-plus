# Task List: Approval Workflow

**Feature**: Human-in-the-Loop Approval Workflow for sensitive actions
**Created**: 2026-03-03
**Status**: Draft
**Branch**: 001-approval-workflow

## Phase 1: Setup

### Project Initialization
- [x] T001 Create project directory structure for approval workflow
- [x] T002 [P] Create requirements.txt with dependencies: watchdog, PyYAML, python-dotenv
- [x] T003 [P] Create initial directory structure: config/, utils/, Pending_Approval/, Approved/, Rejected/, Logs/
- [x] T004 [P] Create __init__.py files in config/ and utils/ directories
- [x] T005 Create .gitignore with sensitive files exclusions

## Phase 2: Foundational Components

### Base Infrastructure
- [x] T006 Create base configuration module in config/settings.py
- [x] T007 [P] Create file operations utilities in utils/file_operations.py
- [x] T008 [P] Create approval request parser in utils/approval_parser.py
- [x] T009 [P] Create action executor in utils/action_executor.py

## Phase 3: User Story 1 - Request Sensitive Action Approval (Priority: P1)

### Goal: When Claude needs to perform a sensitive action, it creates an approval request file that can be reviewed and either approved or rejected by a human.

### Independent Test: When Claude needs to perform a sensitive action (send email, post on social media, draft payment, etc.), it creates an approval request file in /Pending_Approval with appropriate metadata that can be reviewed by a human.

### Implementation Tasks:
- [x] T010 [US1] Create main approval_handler.py file with basic structure
- [x] T011 [US1] Implement directory creation for Pending_Approval, Approved, Rejected, Logs if missing
- [x] T012 [US1] Implement approval request file creation with proper naming [ACTION_TYPE]_[unique_id].md
- [x] T013 [US1] Create YAML frontmatter with required fields: type, action, details, created, expires
- [x] T014 [US1] Implement human-readable markdown content with action summary and instructions
- [x] T015 [US1] Implement unique ID generation using timestamp or message/email ID
- [x] T016 [US1] Validate approval request structure and content before creation
- [x] T017 [US1] Add 24-hour expiration logic to approval requests

## Phase 4: User Story 2 - Manage Approval Requests (Priority: P2)

### Goal: Users can move approval request files between /Pending_Approval, /Approved, and /Rejected folders to control which actions are executed.

### Independent Test: Users can move approval request files between the three directories, and the system responds appropriately when files are moved to /Approved or /Rejected.

### Implementation Tasks:
- [x] T018 [US2] Implement watchdog monitoring for /Approved directory
- [x] T019 [US2] Create file event handler for when approval requests are moved to /Approved
- [x] T020 [US2] Implement action execution when approval request is moved to /Approved
- [x] T021 [US2] Create file event handler for when approval requests are moved to /Rejected
- [x] T022 [US2] Implement rejection handling and logging
- [x] T023 [US2] Add validation to ensure only properly formatted approval requests are processed
- [x] T024 [US2] Implement default handling for expired approval requests

## Phase 5: User Story 3 - Monitor Approval Status (Priority: P3)

### Goal: The system maintains logs of all approval requests and their final status (approved, rejected, expired).

### Independent Test: The system creates log entries in the /Logs directory for all approval requests, showing their final status and outcome.

### Implementation Tasks:
- [x] T025 [US3] Implement processed action logging in /Logs directory
- [x] T026 [US3] Create log file naming convention: [ACTION_TYPE]_[id]_processed.md
- [x] T027 [US3] Log execution results (success, failure, cancellation) for approved actions
- [x] T028 [US3] Include executor information and timestamp in processed logs
- [x] T029 [US3] Implement audit trail for all approval request lifecycle events
- [x] T030 [US3] Add search and retrieval functionality for processed action logs

## Phase 6: Cross-cutting Features

### Security and Error Handling
- [ ] T031 Implement comprehensive error handling throughout the approval workflow
- [ ] T032 Add security validation for approval request content to prevent injection attacks
- [ ] T033 Implement atomic file operations to prevent corruption during concurrent access
- [ ] T034 Add input sanitization for sensitive information in approval requests
- [ ] T035 Implement rate limiting for action execution

### Integration and Validation
- [ ] T036 Create integration with Claude reasoning loop to check approval directories
- [ ] T037 Add MCP integration for executing approved actions
- [ ] T038 Implement file validation functions to verify approval request integrity
- [ ] T039 Add comprehensive logging for monitoring and debugging
- [ ] T040 Validate that all user stories work independently and together

## Dependencies

### User Story Completion Order:
- User Story 1 (Request Approval) must be completed before User Story 2 (Manage Requests)
- User Story 2 must be completed before User Story 3 (Monitor Status)
- User Story 3 depends on both User Story 1 and User Story 2

### Blocking Dependencies:
- T001-T005 must be completed before any other tasks
- T006-T009 foundational components must be completed before user story tasks
- T010 requires foundational components to be completed
- T018-T024 (approval handling) should be completed before T025-T030 (logging)

## Parallel Execution Opportunities

### Within User Story 1:
- T011 (directory creation) and T012-T017 (approval request creation) can be developed in parallel

### Within User Story 2:
- T018-T020 (approval handling) and T021-T024 (rejection handling) can be developed in parallel

### Across User Stories:
- Security features (T031-T035) can be implemented in parallel with user story development
- Integration tasks (T036-T040) can be developed once core functionality is in place

## Implementation Strategy

### MVP Approach:
- Focus on User Story 1 first to enable approval request creation
- Implement basic approval request files with YAML frontmatter
- Add directory monitoring for approved actions (User Story 2)
- Complete logging functionality (User Story 3) as final increment

### Incremental Delivery:
- v1.0: Basic approval request creation with proper file structure
- v1.1: Directory monitoring and action execution when approved
- v1.2: Rejection handling and expiration management
- v1.3: Comprehensive logging, security features, and Claude integration