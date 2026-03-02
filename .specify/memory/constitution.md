<!-- Sync Impact Report:
Version Change: N/A (new constitution)
Modified Principles: N/A
Added Sections: All principles and sections
Removed Sections: N/A
Templates Updated: N/A
Follow-up TODOs: None
-->
# Personal AI Employee Constitution

## Core Principles

### I. Local-First Architecture
All personal and business data must remain local on the user's device. Obsidian serves as the primary knowledge base and dashboard, keeping sensitive information accessible but secure. Data synchronization between devices should use secure protocols and never expose credentials or sensitive data to external systems.

### II. Human-in-the-Loop (HITL) Safety
Critical actions involving finances, personal communications, and sensitive data must require explicit human approval before execution. The AI employee must create approval request files for sensitive actions and wait for human intervention before proceeding. This prevents accidental or unauthorized actions.

### III. Modularity Through Agent Skills (NON-NEGOTIABLE)
All AI functionality must be encapsulated as reusable Agent Skills with clear interfaces and well-defined responsibilities. Each skill should perform a specific function and be independently testable. This ensures maintainability, reusability, and easy modification of individual components.

### IV. Persistent Watcher Architecture
The system must employ continuous monitoring through lightweight Python sentinel scripts that detect changes in external systems (email, messaging, file systems) and create actionable files in designated folders. These watchers must be resilient to network interruptions and continue operating reliably.

### V. Obsidian-Centric Workflow
The entire system must be designed around Obsidian as the central hub for information management. All AI-generated reports, dashboards, and state information must be stored as markdown files in the Obsidian vault. This ensures transparency, searchability, and user control over all AI-generated content.

### VI. Security-First Design

All credential management must follow security best practices: never store credentials in plain text, use environment variables or secure credential managers, implement proper audit logging, and maintain clear separation between development and production environments.

## Additional Constraints

The system must implement proper error handling and graceful degradation. When components fail (API timeouts, network issues, etc.), the system should continue operating where possible and queue actions for later processing. All external integrations must implement appropriate rate limiting and retry logic.

## Development Workflow

All implementations must follow the tiered development approach: Bronze (foundation), Silver (functional assistant), Gold (autonomous employee), Platinum (cloud-local hybrid). Each tier builds upon the previous one and includes comprehensive testing of all components. The system must be developed iteratively with frequent validation of core functionality.

## Governance

This constitution governs all development and implementation decisions for the Personal AI Employee project. All code contributions must comply with these principles. Amendments to this constitution require explicit documentation of the change rationale and impact assessment. All implementations must undergo security review before deployment.

**Version**: 1.0.0 | **Ratified**: 2026-03-02 | **Last Amended**: 2026-03-02
