# Implementation Plan: Advanced Todo Features

**Feature**: Advanced Todo Features
**Spec**: [spec.md](./spec.md)
**Created**: 2026-02-08
**Status**: In Progress
**Author**: Claude Code

## Technical Context

This plan outlines the implementation of advanced todo features including priorities, tags, search & filter, sort, recurring tasks, and due dates & reminders. The implementation will follow the AGENTS.md constitution for Phase V, emphasizing Dapr abstractions, event-driven architecture, and cloud-native deployment patterns.

The system will extend the existing Todo application with:
- Enhanced database schema for new attributes (priority, tags, due_at, remind_at, recurrence_pattern)
- Extended MCP tools to support new functionality
- Updated chatbot behavior to interpret natural language for new features
- Event-driven architecture for recurring tasks and reminders using Dapr Pub/Sub
- Kubernetes deployment with Dapr sidecars on OKE

### Current State
- Basic Todo CRUD operations functional
- ChatKit UI integrated
- MCP tools for basic operations (add_task, list_tasks, complete_task, delete_task, update_task)
- Better Auth for authentication
- Neon PostgreSQL for persistence

### Target State
- All intermediate features (priorities, tags, search/filter, sort) implemented
- All advanced features (recurring tasks, due dates & reminders) implemented
- Event-driven architecture for recurring tasks and reminders
- Dapr integration for pub/sub, state management, and secrets
- Deployed on OKE with proper scaling and resilience

### Unknowns (NEEDS CLARIFICATION)
None - all unknowns have been addressed in the research phase.

### Dependencies
- Dapr runtime environment with proper component configurations
- Kafka/Redpanda cluster for event streaming (or Redis as fallback)
- Neon PostgreSQL with proper indexing for search/filter operations
- Cohere API for natural language processing
- Better Auth for user isolation

### Integrations
- MCP tools with Dapr pub/sub for event-driven architecture
- Database schema extensions with existing models
- Cohere AI natural language understanding with new MCP parameters
- Frontend UI with new filtering/sorting capabilities

## Constitution Check

### Phase V Compliance
- [x] Uses Dapr abstractions (no direct Kafka/DB access in business logic)
- [x] Implements event-driven architecture for recurring tasks and reminders
- [x] Maintains stateless services (persistence via Dapr State/Neon DB)
- [x] Enforces user isolation with user_id validation
- [x] Implements observability with structured logging and tracing
- [x] Uses Dapr for secrets management
- [x] Follows cloud-native deployment patterns for OKE

### AGENTS.md Compliance
- [x] MCP tool extensions follow Dapr-first communication pattern
- [x] Event schemas follow required format with trace_id, user_id, etc.
- [x] User isolation enforced in all operations
- [x] Reusable intelligence created for Dapr components and Helm charts
- [x] Technology constraints respected (Dapr-first, no direct Kafka)

## Gates

### Gate 1: Architecture Validation
- [x] All service communications go through Dapr sidecar
- [x] No direct database access in business logic (prefer Dapr State)
- [x] Event-driven patterns used for recurring tasks and reminders
- [x] User_id validation enforced in all MCP tools

### Gate 2: Security Validation
- [x] JWT validation on every ingress request
- [x] User isolation verified in all data operations
- [x] No cross-tenant data leakage possible
- [x] Secrets managed through Dapr (not environment variables)

### Gate 3: Performance Validation
- [ ] Response times under 500ms for chat interactions
- [ ] Search functionality performs adequately with large datasets
- [ ] Event processing handles required throughput
- [ ] Resource limits respected (under 1 vCPU, 2GB RAM per pod)

## Phase 0: Research & Clarification

### Research Tasks

#### R1: Dapr Component Configuration for Kafka/Redpanda
**Objective**: Determine optimal Dapr pub/sub component configuration for event streaming
**Deliverable**: Dapr Kafka/Redpanda component YAML with proper settings
**Status**: COMPLETED
**Reference**: [research.md](./research.md#r1-dapr-component-configuration-for-kafkaredpanda)

#### R2: Recurrence Pattern Data Structure
**Objective**: Define the optimal data structure for storing and processing recurrence patterns
**Deliverable**: Schema definition for recurrence_pattern field with examples
**Status**: COMPLETED
**Reference**: [research.md](./research.md#r2-recurrence-pattern-data-structure)

#### R3: Notification Service Architecture
**Objective**: Design the architecture for handling reminders and notifications
**Deliverable**: Service design for notification handling with Dapr integration
**Status**: COMPLETED
**Reference**: [research.md](./research.md#r3-notification-service-architecture)

#### R4: Natural Language Date/Time Parsing
**Objective**: Research approaches for parsing complex date/time expressions in natural language
**Deliverable**: Recommended approach for handling expressions like "next Friday 5pm"
**Status**: COMPLETED
**Reference**: [research.md](./research.md#r4-natural-language-datetime-parsing)

#### R5: Search Performance Optimization
**Objective**: Identify performance considerations for search functionality with large datasets
**Deliverable**: Database indexing strategy and potential caching approaches
**Status**: COMPLETED
**Reference**: [research.md](./research.md#r5-search-performance-optimization)

#### R6: Dapr State Management Patterns
**Objective**: Determine best practices for using Dapr State Management with conversation history
**Deliverable**: Pattern recommendations for state management in the chatbot service
**Status**: COMPLETED
**Reference**: [research.md](./research.md#r6-dapr-state-management-patterns)

### Clarification Tasks

#### C1: Oracle Cloud Always Free Tier Constraints
**Question**: What are the specific limitations of Oracle Cloud Always Free tier that may impact our deployment?
**Status**: RESOLVED
**Resolution**: OKE Always Free Tier provides up to 2 OCPU and 15 GB of memory for Worker Nodes, up to 2 Load Balancer instances, and 20 GB of Block Volume storage.

#### C2: MCP Tool Parameter Limits
**Question**: Are there any constraints on the size or complexity of parameters that can be passed to MCP tools?
**Status**: RESOLVED
**Resolution**: MCP tools should keep parameter sizes reasonable (under 1MB), with complex objects stored in database and referenced by ID. Large arrays like tags should have reasonable limits (10 tags as per spec).

#### C3: Event Processing SLA Requirements
**Question**: What are the specific SLA requirements for event processing (e.g., reminders must trigger within X seconds)?
**Status**: RESOLVED
**Resolution**: Reminders should trigger within 1 minute of scheduled time. Recurring task generation should occur within 30 seconds of completion. Critical events should have higher priority in queue.

#### C4: Search Performance Requirements
**Question**: What are the performance requirements for search functionality with large datasets?
**Status**: RESOLVED
**Resolution**: System should maintain response times under 2 seconds for search operations, even with up to 10,000 tasks per user. Implement proper indexing and pagination for large datasets.
**Reference**: [research.md](./research.md#r5-search-performance-optimization)

## Phase 1: Design & Contracts

### D1: Data Model Extensions
**Objective**: Extend existing Task model with new attributes for advanced features
**Deliverables**:
- Updated SQLModel definitions
- Database migration scripts
- Index definitions for performance
**Status**: COMPLETED
**Reference**: [data-model.md](./data-model.md)

### D2: MCP Tool Extensions
**Objective**: Extend existing MCP tools with parameters for new functionality
**Deliverables**:
- Updated add_task tool with priority/tags/due_at/recurrence parameters
- Updated list_tasks tool with filter/sort capabilities
- Updated update_task tool with new field support
**Status**: COMPLETED
**Reference**: [contracts/todo-cohere-api.md](./contracts/todo-cohere-api.md)

### D3: Event Schema Design
**Objective**: Define event schemas for event-driven architecture
**Deliverables**:
- TaskCreated event schema
- TaskCompleted event schema
- ReminderDue event schema
- RecurringSpawned event schema
**Status**: COMPLETED
**Reference**: [research.md](./research.md#technology-stack-recommendations)

### D4: API Contract Updates
**Objective**: Update API contracts to reflect new functionality
**Deliverables**:
- Updated OpenAPI specifications
- Contract tests for new functionality
**Status**: COMPLETED
**Reference**: [contracts/todo-cohere-api.md](./contracts/todo-cohere-api.md)

### D5: Dapr Component Design
**Objective**: Design Dapr component configurations for the system
**Deliverables**:
- Pub/sub component configuration
- State store component configuration
- Secret store component configuration
- Service invocation configuration
**Status**: COMPLETED
**Reference**: [research.md](./research.md#r1-dapr-component-configuration-for-kafkaredpanda)

## Phase 2: Implementation Strategy

### I1: Database Schema Extension
- [ ] Extend Task model with new fields (priority, tags, due_at, etc.)
- [ ] Create database migration for schema changes
- [ ] Add proper indexes for search and filter operations

### I2: MCP Tool Implementation
- [ ] Extend add_task with new parameters
- [ ] Extend list_tasks with filtering and sorting
- [ ] Extend update_task with new field support
- [ ] Implement recurring task generation logic
- [ ] Implement due date and reminder logic

### I3: Event-Driven Architecture
- [ ] Set up Dapr pub/sub for task events
- [ ] Implement event publishers for task operations
- [ ] Implement event subscribers for recurring tasks
- [ ] Implement event subscribers for reminders

### I4: Chatbot Enhancement
- [ ] Update natural language processing for new features
- [ ] Enhance agent behavior to use extended MCP tools
- [ ] Add confirmation messages for new operations

### I5: Frontend Updates
- [ ] Add UI elements for priority selection
- [ ] Add tag input functionality
- [ ] Add due date/time picker
- [ ] Add recurrence pattern configuration
- [ ] Add search and filter UI
- [ ] Add sorting controls

### I6: Dapr Integration
- [ ] Configure Dapr sidecars for services
- [ ] Implement Dapr state management
- [ ] Configure Dapr pub/sub components
- [ ] Set up Dapr secret management

### I7: Kubernetes Deployment
- [ ] Create Helm charts for services
- [ ] Configure OKE deployment manifests
- [ ] Set up resource limits and scaling
- [ ] Configure service networking

## Phase 3: Validation & Testing

### V1: Functional Testing
- [ ] Test all intermediate features (priorities, tags, search/filter, sort)
- [ ] Test all advanced features (recurring tasks, due dates, reminders)
- [ ] Test MCP tool extensions
- [ ] Test natural language processing for new features

### V2: Integration Testing
- [ ] Test event-driven architecture
- [ ] Test Dapr component interactions
- [ ] Test user isolation and authentication
- [ ] Test database performance with new indexes

### V3: Performance Testing
- [ ] Validate response times under load
- [ ] Test search performance with large datasets
- [ ] Validate event processing throughput
- [ ] Test resource utilization

### V4: Security Testing
- [ ] Verify user isolation
- [ ] Test authentication enforcement
- [ ] Validate secret management
- [ ] Test for data leakage between tenants

## Risks & Mitigations

### R1: Dapr Learning Curve
**Risk**: Team unfamiliarity with Dapr may slow implementation
**Mitigation**: Start with simple Dapr integrations and gradually increase complexity

### R2: Event Processing Complexity
**Risk**: Event-driven architecture may introduce complexity and potential race conditions
**Mitigation**: Use Dapr's built-in reliability features (retry, circuit breaker) and implement proper error handling

### R3: Performance Degradation
**Risk**: New features may impact system performance
**Mitigation**: Implement proper indexing, caching, and monitor performance throughout development

### R4: Oracle Cloud Constraints
**Risk**: Oracle Cloud Always Free tier limitations may restrict functionality
**Mitigation**: Design system to work within constraints and document limitations

## Success Criteria

### SC1: Feature Completeness
- [ ] All intermediate features implemented and functional
- [ ] All advanced features implemented and functional
- [ ] MCP tools extended with new functionality
- [ ] Natural language processing enhanced for new features

### SC2: Architecture Compliance
- [ ] System follows event-driven architecture patterns
- [ ] Dapr abstractions used throughout
- [ ] Stateless services implemented correctly
- [ ] Cloud-native deployment achieved

### SC3: Performance Requirements
- [ ] Response times under 500ms maintained
- [ ] System scales appropriately with load
- [ ] Resource utilization within limits
- [ ] Event processing meets throughput requirements

### SC4: Security & Isolation
- [ ] User isolation enforced in all operations
- [ ] Authentication required for all endpoints
- [ ] Secrets properly managed through Dapr
- [ ] No cross-tenant data leakage

## Next Steps

1. Begin Phase 2 implementation of core features following the phased approach
2. Implement database schema extensions and migrations
3. Develop extended MCP tools with advanced functionality
4. Implement event-driven architecture for recurring tasks and reminders
5. Enhance chatbot with Cohere integration for new features
6. Update frontend UI to support new functionality
7. Complete Dapr integration and Kubernetes deployment
8. Perform comprehensive testing and validation