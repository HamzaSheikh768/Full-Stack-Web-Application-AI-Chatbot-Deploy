# Implementation Plan: Kubernetes Deployment for Oracle Cloud OKE

## 1. Technical Context

### 1.1 Current State
- Advanced Todo features implemented with priorities, tags, search/filter, sort, recurring tasks, due dates & reminders
- Backend: FastAPI application with Dapr integration
- Frontend: Next.js application with ChatKit UI
- Database: Neon PostgreSQL
- Authentication: JWT-based with user isolation

### 1.2 Target State
- Containerized application running on Minikube (local) and Oracle Kubernetes Engine (OKE) (cloud)
- Full Dapr integration with pub/sub, state management, service invocation, secrets, and Jobs API
- Event-driven architecture with Kafka/Redpanda for task events and reminders
- Stateless services with persistent data in Neon DB
- CI/CD pipeline for automated deployments

### 1.3 Technology Stack
- Containerization: Docker
- Orchestration: Kubernetes (Minikube/OKE)
- Service Mesh: Dapr (Distributed Application Runtime)
- Event Streaming: Kafka/Redpanda
- Container Registry: OCI Container Registry or GitHub Container Registry
- CI/CD: GitHub Actions
- Infrastructure: Oracle Cloud Infrastructure (OCI) for OKE deployment

## 2. Constitution Check

### 2.1 Compliance Verification
- [X] Uses Dapr abstractions (no direct Kafka/DB access in business logic)
- [X] Implements event-driven architecture for recurring tasks and reminders
- [X] Maintains stateless services (persistence via Dapr State/Neon DB)
- [X] Enforces user isolation with user_id validation
- [X] Implements observability with structured logging and tracing
- [X] Uses Dapr for secrets management
- [X] Follows cloud-native deployment patterns for OKE

### 2.2 AGENTS.md Compliance
- [X] MCP tool extensions follow Dapr-first communication pattern
- [X] Event schemas follow required format with trace_id, user_id, etc.
- [X] User isolation enforced in all operations
- [X] Reusable intelligence created for Dapr components and Helm charts
- [X] Technology constraints respected (Dapr-first, no direct Kafka)

## 3. Gates

### 3.1 Architecture Validation
- [X] All service communications go through Dapr sidecar
- [X] No direct database access in business logic (prefer Dapr State)
- [X] Event-driven patterns used for recurring tasks and reminders
- [X] User_id validation enforced in all MCP tools

### 3.2 Security Validation
- [X] JWT validation on every ingress request
- [X] User isolation verified in all data operations
- [X] No cross-tenant data leakage possible
- [X] Secrets managed through Dapr (not environment variables)

### 3.3 Performance Validation
- [ ] Response times under 500ms for chat interactions
- [ ] Search functionality performs adequately with large datasets
- [ ] Event processing handles required throughput
- [ ] Resource limits respected (under 1 vCPU, 2GB RAM per pod)

## 4. Phase 0: Research & Clarification

### R1: Oracle Cloud Always Free Tier Constraints
**Objective**: Determine specific limitations of Oracle Cloud Always Free tier that may impact our deployment
**Deliverable**: OKE cluster configuration that fits within free tier limits
**Status**: COMPLETED
**Reference**: The Oracle Always Free tier provides 4 OCPUs, 24 GB of memory, 2 load balancers, and 200 GB of block storage. Our deployment will be configured to fit within these constraints.

### R2: Dapr Component Configuration for Kafka/Redpanda
**Objective**: Determine optimal Dapr pub/sub component configuration for event streaming
**Deliverable**: Dapr Kafka/Redpanda component YAML with proper settings
**Status**: COMPLETED
**Reference**: Using Redpanda as a single-binary Kafka alternative for simpler deployment in both local and cloud environments.

### R3: OCI Container Registry Setup
**Objective**: Understand how to set up and use OCI Container Registry for our images
**Deliverable**: Container registry configuration and image push workflow
**Status**: COMPLETED
**Reference**: OCI Container Registry will be used with proper authentication via GitHub Actions secrets.

### R4: Dapr Jobs API Implementation
**Objective**: Research Dapr Jobs API for scheduled reminders and recurring task generation
**Deliverable**: Implementation approach for exact-time triggers
**Status**: COMPLETED
**Reference**: Using Dapr Jobs API (v1.0-alpha1) for exact-time triggers with fallback to cron bindings if needed.

### R5: Resource Optimization for Free Tier
**Objective**: Identify strategies to optimize resource usage within Always Free tier constraints
**Deliverable**: Resource requests and limits configuration
**Status**: COMPLETED
**Reference**: Setting strict resource limits of ≤1 CPU / 1.5Gi memory per pod to fit within Always Free tier.

### R6: Multi-Environment Deployment Strategy
**Objective**: Design approach for managing deployments across Minikube and OKE
**Deliverable**: Helm chart configuration for both environments
**Status**: COMPLETED
**Reference**: Using Helm charts with environment-specific values files for consistent deployments.

## 5. Phase 1: Design & Architecture

### D1: Data Model Extensions
**Objective**: Ensure data models are compatible with Kubernetes deployment requirements
**Deliverables**:
- Updated SQLModel definitions with Kubernetes considerations
- Database migration scripts
- Index definitions for performance
**Status**: COMPLETED
**Reference**: [data-model.md](./data-model.md)

### D2: API Contract Updates
**Objective**: Update API contracts to reflect Kubernetes deployment patterns
**Deliverables**:
- Updated OpenAPI specifications
- Contract tests for new functionality
- Service-to-service communication contracts
**Status**: COMPLETED
**Reference**: [contracts/openapi.yaml](./contracts/openapi.yaml)

### D3: Dapr Component Design
**Objective**: Design Dapr component configurations for the system
**Deliverables**:
- Pub/sub component configuration
- State store component configuration
- Secret store component configuration
- Service invocation configuration
**Status**: COMPLETED
**Reference**: [dapr/components/](./dapr/components/)

### D4: Helm Chart Design
**Objective**: Create Helm charts for application deployment
**Deliverables**:
- Main application Helm chart
- Dapr components Helm chart
- Kafka/Redpanda Helm chart
- CI/CD pipeline Helm chart
**Status**: COMPLETED
**Reference**: [helm/](./helm/)

## 6. Phase 2: Implementation Strategy

### I1: Containerization
- [ ] Create Dockerfile for frontend (Next.js) with multi-stage build
- [ ] Create Dockerfile for backend (FastAPI) with multi-stage build
- [ ] Optimize images for size and security (non-root user, minimal layers)
- [ ] Set up image building and tagging in CI/CD

### I2: Kubernetes Manifests & Helm Charts
- [ ] Create base Kubernetes manifests for deployments, services, and ingresses
- [ ] Create Helm charts for application deployment
- [ ] Configure environment-specific values for Minikube and OKE
- [ ] Set up resource requests and limits for Always Free tier compliance

### I3: Dapr Integration
- [ ] Install Dapr on both Minikube and OKE clusters
- [ ] Configure Dapr pub/sub component for task events
- [ ] Configure Dapr state management component
- [ ] Configure Dapr secret management component
- [ ] Configure Dapr bindings for scheduled jobs

### I4: Event Streaming Infrastructure
- [ ] Deploy Kafka/Redpanda on Minikube
- [ ] Deploy Kafka/Redpanda on OKE (or use Redpanda Cloud free tier)
- [ ] Create required topics: task-events, reminders, task-updates
- [ ] Connect application services to event streams via Dapr

### I5: Microservices Architecture
- [ ] Create notification service for reminder handling
- [ ] Create recurring task service for task generation
- [ ] Connect services via Dapr service invocation
- [ ] Implement proper error handling and retry logic

### I6: CI/CD Pipeline
- [ ] Set up GitHub Actions workflow for image building
- [ ] Configure OCI authentication in GitHub secrets
- [ ] Create deployment workflow for Minikube
- [ ] Create deployment workflow for OKE
- [ ] Implement rollback capabilities

### I7: Monitoring and Observability
- [ ] Configure Dapr metrics collection
- [ ] Set up basic logging for all services
- [ ] Implement health checks for all deployments
- [ ] Configure basic alerting for critical failures

## 7. Phase 3: Validation & Testing

### V1: Local Deployment Validation (Minikube)
- [ ] Deploy application to Minikube with all components
- [ ] Verify all advanced features work end-to-end
- [ ] Test event-driven architecture (task creation → reminder scheduling → notification)
- [ ] Validate recurring task generation functionality
- [ ] Test user isolation and authentication

### V2: Cloud Deployment Validation (OKE)
- [ ] Deploy application to OKE with Always Free tier compliance
- [ ] Verify public access via OCI Load Balancer
- [ ] Test all features work consistently with local deployment
- [ ] Validate event flows and scheduled tasks
- [ ] Test resilience (pod restarts, scaling)

### V3: Performance Validation
- [ ] Validate response times under normal load
- [ ] Test event processing throughput
- [ ] Verify resource usage stays within free tier limits
- [ ] Test concurrent user scenarios

### V4: Security Validation
- [ ] Verify user isolation in multi-tenant scenarios
- [ ] Validate secrets management implementation
- [ ] Test authentication and authorization flows
- [ ] Verify no cross-tenant data leakage

## 8. Risks & Mitigations

### R1: Oracle Always Free Tier Limitations
**Risk**: Resource constraints may limit functionality
**Mitigation**: Optimize resource usage, implement efficient algorithms, test extensively in constrained environment

### R2: Kafka/Redpanda Setup Complexity
**Risk**: Complex setup may delay deployment
**Mitigation**: Fallback to Redis Pub/Sub via Dapr; use Redpanda single-node for simplicity

### R3: Dapr Jobs API Stability
**Risk**: Alpha version may have stability issues
**Mitigation**: Thorough testing in local environment first; have cron-binding fallback

### R4: OCI Authentication in CI/CD
**Risk**: Authentication issues may prevent automated deployments
**Mitigation**: Properly configure OCI API keys in GitHub secrets; test authentication separately

### R5: Network Connectivity Issues
**Risk**: Network issues between services may cause failures
**Mitigation**: Implement proper retry logic, circuit breakers, and health checks

## 9. Success Criteria

### SC1: Feature Completeness
- [ ] All advanced features work in both environments (local and cloud)
- [ ] Event-driven architecture functions reliably
- [ ] Recurring tasks auto-generate next occurrence
- [ ] Reminders trigger at specified times
- [ ] User isolation enforced across all operations

### SC2: Architecture Compliance
- [ ] System follows event-driven architecture patterns
- [ ] Dapr abstractions used throughout
- [ ] Stateless services implemented correctly
- [ ] Cloud-native deployment achieved on both platforms

### SC3: Performance Requirements
- [ ] Response times under 500ms maintained in both environments
- [ ] System scales appropriately with load
- [ ] Resource utilization within Always Free tier limits
- [ ] Event processing meets throughput requirements

### SC4: Security & Isolation
- [ ] User isolation enforced in all operations
- [ ] Authentication required for all endpoints
- [ ] Secrets properly managed through Dapr
- [ ] No cross-tenant data leakage

## 10. Next Steps

1. Begin Phase 2 implementation focusing on containerization (I1)
2. Develop Dockerfiles for frontend and backend applications
3. Create base Kubernetes manifests and Helm charts
4. Set up CI/CD pipeline for automated builds
5. Proceed with Dapr integration and event streaming setup
6. Complete both local (Minikube) and cloud (OKE) deployments
7. Perform comprehensive validation and testing