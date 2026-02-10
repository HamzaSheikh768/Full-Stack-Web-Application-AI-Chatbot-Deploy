# Specification: Kubernetes Deployment for Oracle Cloud OKE

## Feature Description

Complete the cloud-native evolution of the Todo Chatbot by deploying the full application (including advanced features from Part A) in two environments:
- **Part B**: Local Kubernetes cluster (Minikube) with full Dapr integration
- **Part C**: Production-grade cloud Kubernetes cluster using **Oracle Cloud Infrastructure (OCI)** with **Oracle Kubernetes Engine (OKE)** – Always Free tier only

Both environments must support:
- Containerized frontend and backend
- Event-driven architecture (Kafka or Dapr Pub/Sub compatible)
- Full Dapr usage: Pub/Sub, State Management, Service Invocation, Secrets, Jobs API (for reminders & recurring tasks)
- Stateless services with persistent data in Neon DB
- Observability basics (logs, metrics)

**Strict Constraint**: Cloud deployment must use **Oracle Cloud (OKE)** exclusively – no DigitalOcean, GKE, AKS, or other providers.

## User Scenarios & Testing

### Scenario 1: Developer Deploys Locally on Minikube
- As a developer, I want to deploy the full Todo Chatbot application on my local Minikube cluster so that I can test all features in a Kubernetes environment before pushing to production
- Given I have Minikube running locally
- When I run the deployment script
- Then the application should be deployed with all services (frontend, backend, Dapr sidecars) running
- And I should be able to access the ChatKit UI and use all advanced features

### Scenario 2: Admin Deploys to Oracle Cloud OKE
- As a DevOps engineer, I want to deploy the Todo Chatbot to Oracle Kubernetes Engine using only Always Free tier resources so that the application runs cost-effectively in production
- Given I have Oracle Cloud account with Always Free tier eligibility
- When I execute the cloud deployment process
- Then the application should be deployed to OKE cluster
- And all services should be running with appropriate resource limits
- And the application should be accessible via public URL

### Scenario 3: User Interacts with Cloud-Deployed Application
- As an end user, I want to access the Todo Chatbot application deployed in Oracle Cloud so that I can use all advanced features (priorities, tags, recurring tasks, reminders)
- Given the application is deployed in Oracle Cloud
- When I access the public URL and interact with the ChatKit UI
- Then all features should work consistently with the local deployment
- And events should flow properly (task creation → reminders → notifications)

## Functional Requirements

### FR-1: Containerization
- The application must be packaged in Docker containers for both frontend (Next.js) and backend (FastAPI)
- Containers must use multi-stage builds for optimization
- Images must run as non-root users for security
- Container images must be compatible with both Minikube and OKE

### FR-2: Local Kubernetes Deployment (Minikube)
- The application must deploy successfully to a local Minikube cluster
- Deployments must include appropriate resource requests and limits
- Services must be exposed via appropriate service types (NodePort for local access)
- Ingress must be configurable for local access

### FR-3: Cloud Kubernetes Deployment (OKE)
- The application must deploy successfully to Oracle Kubernetes Engine
- Deployment must utilize Oracle Cloud Always Free tier resources only
- Resource limits must be set to comply with free tier constraints (4 OCPUs, 24 GB RAM)
- Services must be exposed via OCI Load Balancer (free tier eligible)

### FR-4: Dapr Integration
- Dapr must be installed and configured on both environments
- Dapr pub/sub component must be configured for event-driven architecture
- Dapr state management must be configured to work with Neon DB
- Dapr service invocation must be enabled between services
- Dapr secrets management must be implemented for credential handling

### FR-5: Event-Driven Architecture
- Kafka or compatible pub/sub system must be deployed in both environments
- Required topics must be created: task-events, reminders, task-updates
- Event producers and consumers must be properly connected via Dapr
- Recurring task generation must be triggered via events

### FR-6: CI/CD Pipeline
- GitHub Actions workflow must build and push Docker images to registry
- Pipeline must deploy to both Minikube (for testing) and OKE (for production)
- Rollback capabilities must be available through the CI/CD process
- Pipeline must validate deployment success before marking completion

### FR-7: Monitoring and Observability
- Basic logging must be available for all services
- Dapr metrics must be accessible for monitoring
- Health checks must be implemented for all services
- Basic alerting must be configured for critical failures

## Non-Functional Requirements

### NFR-1: Scalability
- Application must support minimum 2-3 replicas per service in production
- Horizontal Pod Autoscaler should be configured where appropriate
- System must handle load increases gracefully

### NFR-2: Availability
- Application must maintain 99% uptime in production environment
- Services must automatically recover from failures
- Data must persist independently of service lifecycles

### NFR-3: Security
- All inter-service communication must be secured
- Secrets must not be hardcoded in configuration
- User isolation must be maintained at database level
- Authentication must be verified for all API endpoints

### NFR-4: Performance
- API responses must be served within 500ms under normal load
- Frontend must load within 3 seconds
- Event processing must complete within 10 seconds

## Success Criteria

### Quantitative Metrics
- Application successfully deploys to Minikube with all services running (100% success rate)
- Application successfully deploys to OKE using only Always Free tier resources (100% compliance)
- All advanced features work consistently across both environments (100% feature parity)
- Deployment process completes within 10 minutes (both local and cloud)
- System supports 100 concurrent users without performance degradation

### Qualitative Measures
- Developers can seamlessly switch between local and cloud deployments
- Event-driven architecture functions reliably with no message loss
- User experience is consistent between local and cloud deployments
- System is maintainable and extensible for future features
- Deployment process is repeatable and reliable

## Key Entities

### Kubernetes Resources
- Deployments for frontend and backend services
- Services for internal and external communication
- ConfigMaps and Secrets for configuration
- Ingress resources for external access
- Horizontal Pod Autoscalers for scaling

### Dapr Components
- Pub/Sub component for event messaging
- State management component for persistent state
- Secret store component for credential management
- Bindings/Jobs API component for scheduled tasks

### Infrastructure Components
- Oracle Kubernetes Engine cluster
- OCI Container Registry for images
- OCI Load Balancer for traffic distribution
- Neon PostgreSQL database for persistent data
- Kafka/Redpanda for event streaming

## Assumptions

- Oracle Cloud account with Always Free tier eligibility is available
- Minikube is properly installed and configured locally
- Docker is available for containerization
- Dapr is compatible with the current application architecture
- Neon database provides sufficient performance for the application needs

## Dependencies

- Oracle Cloud Infrastructure account
- Minikube for local Kubernetes
- Docker for containerization
- Dapr for distributed application runtime
- Neon for database services
- Kafka or Redpanda for event streaming

## Scope

### In Scope
- Containerization of frontend and backend services
- Kubernetes deployment configurations for Minikube
- Oracle Cloud OKE deployment with Always Free tier
- Dapr integration for all required components
- Event-driven architecture implementation
- CI/CD pipeline setup
- Basic monitoring and observability

### Out of Scope
- Voice commands implementation
- Multi-language support (Urdu)
- Paid cloud resources beyond Always Free tier
- Advanced ML model training
- Third-party integrations beyond what's specified