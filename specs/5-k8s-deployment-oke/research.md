# Research Findings: Kubernetes Deployment for Oracle Cloud OKE

## Overview

This document captures research findings to resolve the unknowns and clarify technical decisions for deploying the Todo Chatbot application to both Minikube (local) and Oracle Kubernetes Engine (OKE) in Oracle Cloud.

## R1: Oracle Cloud Always Free Tier Constraints

### Decision: Use OKE with Resource-Conscious Configuration
**Rationale**: Oracle Cloud's Always Free tier provides 4 OCPUs and 24 GB of memory, which is sufficient for our application with proper resource management.

**Implementation Details**:
- OKE cluster: Use flexible shapes that fit within free tier limits
- Resource limits: Configure ≤1 CPU / 1.5Gi memory per pod to stay within limits
- Replicas: Use minimal replica counts (1-2) for free tier compliance
- Storage: Utilize the 200 GB block storage allocation efficiently

**Constraints**:
- Maximum 4 OCPUs total
- Maximum 24 GB RAM total
- 2 load balancers limit
- 200 GB block storage limit

## R2: Dapr Component Configuration for Kafka/Redpanda

### Decision: Use Redpanda for Simpler Deployment
**Rationale**: Redpanda is a drop-in Kafka-compatible alternative that's easier to deploy and manage, especially in resource-constrained environments like the free tier.

**Configuration Approach**:
- Deploy Redpanda as a single-node cluster for simplicity
- Configure Dapr pub/sub component to use Redpanda
- Create required topics: task-events, reminders, task-updates
- Implement proper partitioning and replication settings

**Alternative Considered**: 
- Strimzi Kafka operator: More complex but feature-rich
- Redis Pub/Sub: Simpler but less feature-complete than Kafka

## R3: OCI Container Registry Setup

### Decision: Use OCI Container Registry with GitHub Actions
**Rationale**: OCI Container Registry provides secure, scalable image storage that integrates well with OKE and GitHub Actions.

**Implementation Steps**:
- Create repositories in OCI Container Registry
- Configure OCI authentication via API keys stored in GitHub secrets
- Set up GitHub Actions workflow for image building and pushing
- Implement proper image tagging and versioning

**Authentication Method**:
- Use OCI API keys for authentication
- Store private key in GitHub secrets
- Use OCI CLI for authentication in CI/CD pipeline

## R4: Dapr Jobs API Implementation

### Decision: Use Dapr Jobs API with Cron Binding Fallback
**Rationale**: Dapr Jobs API provides exact-time scheduling capabilities that are ideal for reminder notifications and recurring task generation.

**Implementation Approach**:
- Use Dapr Jobs API (v1.0-alpha1) for scheduled tasks
- Implement fallback to cron bindings if Jobs API proves unstable
- Create job definitions for reminder triggers and recurring task generation
- Include proper error handling and retry logic

**Fallback Plan**:
- If Jobs API is unstable, use Dapr cron bindings
- Implement custom scheduling service if needed

## R5: Resource Optimization for Free Tier

### Decision: Implement Strict Resource Management
**Rationale**: To stay within Oracle Always Free tier limits, strict resource management is essential.

**Optimization Strategies**:
- Set resource requests and limits for all deployments
- Use minimal replica counts (1-2)
- Optimize container images for size
- Implement efficient algorithms to reduce resource usage
- Monitor resource usage continuously

**Resource Allocation**:
- Frontend: 0.5 CPU, 0.5Gi memory
- Backend: 0.5 CPU, 0.75Gi memory
- Notification service: 0.25 CPU, 0.25Gi memory
- Recurring task service: 0.25 CPU, 0.25Gi memory
- Dapr sidecars: Minimal overhead per service

## R6: Multi-Environment Deployment Strategy

### Decision: Use Helm Charts with Environment-Specific Values
**Rationale**: Helm provides a consistent deployment mechanism across both Minikube and OKE while allowing environment-specific configurations.

**Implementation Approach**:
- Create base Helm charts for the application
- Use environment-specific values files for Minikube and OKE
- Parameterize differences like service types, resource limits, and ingress configurations
- Implement CI/CD pipeline to deploy to both environments

**Environment Differences**:
- Minikube: NodePort services, local ingress
- OKE: LoadBalancer services, OCI Load Balancer

## C1: Oracle Cloud Infrastructure Setup

### Decision: Use Terraform for Infrastructure as Code
**Rationale**: Terraform provides consistent, version-controlled infrastructure provisioning for OKE.

**Implementation Details**:
- Create Terraform scripts for OKE cluster creation
- Configure networking components (VCNs, subnets, security lists)
- Set up proper IAM policies for the cluster
- Implement state management with remote backend

## C2: Networking and Security

### Decision: Implement Network Policies and Service Mesh Security
**Rationale**: Proper security configuration is essential for protecting the application and data.

**Security Measures**:
- Implement Kubernetes Network Policies
- Use Dapr service invocation for mTLS communication
- Configure proper RBAC for services
- Implement secrets management through Dapr

## C3: Monitoring and Observability

### Decision: Use OCI Monitoring and Dapr Metrics
**Rationale**: Leverage Oracle Cloud's built-in monitoring capabilities while supplementing with Dapr-specific metrics.

**Monitoring Stack**:
- OCI Monitoring for infrastructure metrics
- Dapr metrics for service mesh observability
- Structured logging for application insights
- Basic alerting for critical failures

## C4: Backup and Disaster Recovery

### Decision: Rely on Neon DB Backup Capabilities
**Rationale**: Since our state is primarily in Neon PostgreSQL, we rely on Neon's backup and recovery features.

**Approach**:
- Use Neon's built-in backup and point-in-time recovery
- Implement application-level safeguards against data loss
- Regular testing of backup restoration procedures

## C5: Scaling and Performance

### Decision: Implement Horizontal Pod Autoscaling with Resource Limits
**Rationale**: To handle varying loads while staying within free tier limits, implement intelligent scaling.

**Scaling Strategy**:
- Configure HPA based on CPU and memory usage
- Set resource limits to prevent overconsumption
- Implement efficient algorithms to minimize resource usage
- Monitor performance metrics continuously

## Conclusion

This research provides the foundation for implementing the Kubernetes deployment to both Minikube and Oracle Cloud OKE. The decisions made balance functionality with the constraints of the Oracle Always Free tier while maintaining security, reliability, and scalability.