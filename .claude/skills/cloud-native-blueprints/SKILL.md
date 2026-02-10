---
name: cloud-native-blueprints
description: Create, version, maintain and apply reusable cloud-native deployment blueprints for Kubernetes + Dapr + event-driven systems (Kafka/Redpanda, Pub/Sub, State, Jobs). Use this skill when: (1) generating Helm charts, Dapr components, Kubernetes manifests from specifications, (2) creating spec-driven infrastructure templates for Todo/Chatbot apps, (3) implementing reusable deployment patterns for Phase V of the Evolution of Todo hackathon (DigitalOcean DOKS, Minikube, AKS/GKE, recurring tasks, reminders via Jobs + Pub/Sub), (4) governing AI agents during cloud-native deployments with blueprints as versioned artifacts. Triggers on phrases like "create blueprint", "deployment blueprint", "reusable Helm + Dapr pattern", "spec-driven infrastructure", "cloud-native blueprint for todo".
---

# Cloud-Native Blueprints Skill

This skill enables **spec-driven creation and usage of reusable cloud-native deployment blueprints** — versioned, composable templates that package Helm charts, Dapr components, Kubernetes manifests, configuration patterns, and validation rules for event-driven Todo/Chatbot systems.

## Overview

This skill provides comprehensive blueprints for:
- **Kubernetes Deployment** - Helm charts, manifests, deployment strategies
- **Event-Driven Architecture** - Kafka/Redpanda + Dapr integration
- **Service Orchestration** - Multi-service coordination and communication
- **AI-Powered Operations** - kubectl-ai and intelligent automation
- **Multi-Cloud Support** - Works with OKE, DOKS, EKS, GKE, AKS

## When to Use This Skill

Use automatically when the goal involves:

- Turning application specs (/specs/*) into reusable infrastructure (Helm + Dapr + K8s)
- Creating versioned deployment patterns for Phase V (advanced features + cloud deployment)
- Reusing blueprints across Minikube → DigitalOcean DOKS → AKS/GKE
- Governing AI agents to avoid ad-hoc YAML — enforce blueprint-based consistency
- Implementing recurring tasks/reminders via Dapr Jobs + Pub/Sub + Kafka
- Generating event-driven architecture artifacts (task-events, reminders, task-updates topics)

## Core Principles

- **Spec-Driven Only** — Every blueprint starts from @specs/ files or Constitution
- **Reusability First** — Blueprints are versioned artifacts (v1, v2, …) that can be referenced/inherited
- **Minimal & Composable** — Prefer small, focused blueprints over monoliths
- **Validation Built-In** — Include kubeconform / datree / OPA-style rules when possible
- **Progressive Disclosure** — Keep core workflow here; move large examples to references/

## Core Workflows

### 1. Deploy Application with Helm

Use AI-enhanced Helm patterns for intelligent deployments:

```bash
# Generate Helm chart with AI assistance
helm create my-app

# Customize using AI patterns from references/helm-ai-patterns.md
# - Dynamic scaling based on predicted load
# - Intelligent health check configuration
# - Auto-generated monitoring dashboards
```

See `references/helm-ai-patterns.md` for AI-enhanced Helm chart patterns.

### 2. Configure Dapr Components

Deploy Dapr building blocks for microservices:

```bash
# State management
kubectl apply -f dapr-components/state-store.yaml

# Pub/Sub messaging
kubectl apply -f dapr-components/pubsub.yaml

# Service invocation with retries
kubectl apply -f dapr-components/resiliency.yaml
```

See `references/dapr-components.md` for complete component catalog and configuration patterns.

### 3. Define Event Schemas

Establish event contracts for cross-service communication:

```yaml
# Example from references/event-schemas.md
task.created:
  version: "1.0"
  schema:
    task_id: string (uuid)
    title: string (max 200)
    description: string (optional)
    status: enum [pending, in_progress, completed]
    priority: enum [low, medium, high]
    created_at: timestamp (ISO 8601)
    created_by: string (user_id)
```

See `references/event-schemas.md` for versioned event schema definitions.

### 4. Compose Multi-Service Applications

Orchestrate complex microservices deployments:

```bash
# Use composition patterns from references/composition-examples.md
kubectl apply -f compositions/todo-app-stack.yaml
```

This deploys:
- Frontend service
- API service with Dapr sidecar
- Worker service subscribing to events
- Database with persistent storage
- Kafka/Redpanda for messaging

See `references/composition-examples.md` for complete composition patterns.

## Deployment Strategies

### Rolling Update with AI Prediction
Use AI to predict optimal rollout speed based on traffic patterns.

### Blue-Green with Automated Testing
Automated canary analysis before traffic switch.

### Canary with Progressive Delivery
ML-driven progressive rollout based on metrics.

See `references/helm-ai-patterns.md` for AI-enhanced deployment strategies.

## Event-Driven Patterns

### Pub/Sub Messaging
Services publish events, subscribers consume asynchronously.

### Event Sourcing
Events as source of truth, state derived from event log.

### CQRS
Separate read and write models with event synchronization.

See `references/event-schemas.md` for event pattern implementations.

## Dapr Integration

### State Management
Distributed state with pluggable backends (Redis, PostgreSQL, DynamoDB).

### Pub/Sub
Cloud-agnostic messaging (Kafka, Redpanda, RabbitMQ, Azure Service Bus).

### Service Invocation
Service-to-service calls with retries, timeouts, circuit breakers.

### Bindings
Input/output bindings to external systems.

See `references/dapr-components.md` for component configurations.

## Multi-Service Composition

### Microservices Stack
Deploy interconnected services with proper dependencies.

### Shared Resources
ConfigMaps, Secrets, and PersistentVolumes shared across services.

### Service Mesh Integration
Integrate with Istio/Linkerd for advanced traffic management.

See `references/composition-examples.md` for complete examples.

## AI-Enhanced Operations

### Intelligent Scaling
Use kubectl-ai for natural language scaling: "scale frontend to handle 10k requests/sec"

### Automated Troubleshooting
AI-powered root cause analysis for failures.

### Cost Optimization
ML-driven resource right-sizing recommendations.

See other skills: `aiops-kubectl` for AI operations.

## Reference Files

- `dapr-components.md` - Complete Dapr component catalog with configurations
- `helm-ai-patterns.md` - AI-enhanced Helm chart patterns and best practices
- `event-schemas.md` - Versioned event schema definitions and patterns
- `composition-examples.md` - Multi-service application composition patterns

## Integration with Other Skills

This skill works with:
- `oci-oke-deployment` - For Oracle Cloud Kubernetes
- `dapr-jobs-reminders` - For scheduled tasks and reminders
- `kafka-redpanda-dapr` - For event streaming infrastructure

## Workflow: Create a New Blueprint

1. **Read Specification**
   - Start with @specs/features/*, @specs/api/*, @specs/database/*
   - Read Constitution & Phase V requirements (Dapr full, Kafka/Redpanda, Jobs for reminders)

2. **Decide Blueprint Scope**
   Common blueprint types for this hackathon:

   | Blueprint Type              | Purpose                                          | Key Contents                              |
   |-----------------------------|--------------------------------------------------|-------------------------------------------|
   | todo-core                   | FastAPI + MCP + Neon DB (state)                  | Deployment, Service, Secret, Dapr state   |
   | todo-chat                   | Chat endpoint + OpenAI Agents SDK                | Deployment, Ingress/Service, Dapr invoke  |
   | dapr-eventing               | Kafka/Redpanda Pub/Sub + task-events topic       | Dapr pubsub component, Kafka cluster opt  |
   | reminders-engine            | Dapr Jobs + cron/scheduler for due date checks   | Jobs API usage, Dapr component, Binding   |
   | recurring-tasks             | Consumer of task-events → create next occurrence | Deployment + Dapr pubsub subscription     |
   | full-todo-stack             | Umbrella / composition of above                  | Helm chart with subcharts                 |
