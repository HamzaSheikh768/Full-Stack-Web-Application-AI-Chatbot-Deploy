# Data Model: Local Kubernetes Deployment for Cloud-Native Todo Chatbot

**Feature**: 1-k8s-deployment
**Date**: 2026-02-03
**Status**: Reference (No changes from Phase III)

## Overview

This feature focuses on deployment infrastructure rather than data model changes. The underlying data model remains unchanged from Phase III of the Todo Chatbot application.

## Existing Data Models (Inherited from Phase III)

### Task Entity
**Purpose**: Represents individual todo items for users

**Fields**:
- `user_id`: String - Unique identifier for the user who owns the task
- `id`: Integer - Unique identifier for the task
- `title`: String - Task title (required, 1-200 characters)
- `description`: String - Optional task description (max 1000 characters)
- `completed`: Boolean - Task completion status
- `created_at`: DateTime - Timestamp of task creation
- `updated_at`: DateTime - Timestamp of last update

**Relationships**:
- Belongs to one User
- Part of one Conversation (indirectly through messages)

### Conversation Entity
**Purpose**: Represents chat sessions between users and the AI assistant

**Fields**:
- `user_id`: String - Unique identifier for the user
- `id`: Integer - Unique identifier for the conversation
- `created_at`: DateTime - Timestamp of conversation creation
- `updated_at`: DateTime - Timestamp of last update

**Relationships**:
- Belongs to one User
- Has many Messages

### Message Entity
**Purpose**: Represents individual messages in a conversation

**Fields**:
- `user_id`: String - Unique identifier for the user
- `id`: Integer - Unique identifier for the message
- `conversation_id`: Integer - Reference to parent conversation
- `role`: String - Message role (user/assistant)
- `content`: String - Message content
- `created_at`: DateTime - Timestamp of message creation

**Relationships**:
- Belongs to one Conversation
- Belongs to one User

## Deployment-Related Configuration Models

### Kubernetes Pod Configuration
**Purpose**: Runtime configuration for application pods

**Fields**:
- `image`: String - Container image name (todo-frontend or todo-backend)
- `replicas`: Integer - Number of pod replicas
- `resources.requests.cpu`: String - CPU request (e.g., "100m")
- `resources.requests.memory`: String - Memory request (e.g., "128Mi")
- `resources.limits.cpu`: String - CPU limit (e.g., "500m")
- `resources.limits.memory`: String - Memory limit (e.g., "512Mi")
- `env`: Array - Environment variables for the pod

### Service Configuration
**Purpose**: Network configuration for exposing application services

**Fields**:
- `name`: String - Service name
- `type`: String - Service type (NodePort, ClusterIP)
- `port`: Integer - Service port
- `target_port`: Integer - Target port in pods
- `selector`: Map - Labels to select target pods

### Helm Values Configuration
**Purpose**: Parameterized configuration for Helm chart deployments

**Fields**:
- `image.repository`: String - Container image repository
- `image.tag`: String - Container image tag
- `image.pullPolicy`: String - Image pull policy
- `service.type`: String - Kubernetes service type
- `service.port`: Integer - Service port
- `resources.limits`: Map - Resource limits configuration
- `resources.requests`: Map - Resource requests configuration
- `nodeSelector`: Map - Node selection constraints
- `tolerations`: Array - Taint tolerations
- `affinity`: Map - Pod affinity/anti-affinity rules

## Validation Rules

### Task Validation
- Title must be 1-200 characters
- Description must be 0-1000 characters
- Completed status must be boolean
- User ID must match authenticated user

### Message Validation
- Role must be either "user" or "assistant"
- Content must not be empty
- Conversation ID must reference existing conversation

### Deployment Configuration Validation
- Resource requests must be less than or equal to limits
- Image repository must be accessible
- Service ports must be valid (1-65535)
- Environment variables must follow naming conventions

## State Transitions

### Task State Transitions
- `pending` → `completed`: When user marks task as complete
- `completed` → `pending`: When user unmarks task as complete

### Pod Lifecycle States
- `Pending` → `Running`: When pod is scheduled and containers start
- `Running` → `Terminated`: When pod completes or is terminated
- `Running` → `Failed`: When pod encounters unrecoverable error

## Relationships

### User → Task (One-to-Many)
A user can have multiple tasks, but each task belongs to only one user.

### Conversation → Message (One-to-Many)
A conversation can have multiple messages, but each message belongs to only one conversation.

### User → Conversation (One-to-Many)
A user can have multiple conversations, but each conversation belongs to only one user.

### Service → Pod (One-to-Many)
A service can route traffic to multiple pods, but each pod is associated with specific services via selectors.

## Constraints

### Data Integrity
- Foreign key constraints ensure referential integrity
- Unique constraints on user-task combinations
- Not-null constraints on required fields

### Deployment Constraints
- Resource quotas enforced by Kubernetes
- Network policies restrict inter-service communication
- Image pull secrets for private registries
- Security contexts limit container privileges

## Migration Considerations

Since this is a deployment feature, no database schema changes are required. The existing Phase III data models remain unchanged and continue to function as designed.

The deployment infrastructure will interact with the existing database through the backend service, maintaining the same data access patterns as Phase III.