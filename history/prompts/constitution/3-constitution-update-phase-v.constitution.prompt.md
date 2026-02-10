---
id: 3
title: constitution-update-phase-v
stage: constitution
date: 2026-02-07
surface: agent
model: claude-opus-4-5-20251101
feature: advanced-todo-features
branch: 1-advanced-todo-features
user: user
command: constitution update
labels:
  - constitution
  - phase-v
  - cloud-native
  - todo
links:
  spec: specs/1-advanced-todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
prompt: |
  Project Overview and Purpose
  This constitution defines the foundational principles, constraints, and non-negotiable rules for Phase V of the "Evolution of Todo" Hackathon II project. Phase V focuses on implementing advanced and intermediate features, integrating event-driven architecture with Kafka (or alternative Pub/Sub via Dapr if Kafka access issues arise), and deploying the AI-powered Todo Chatbot to a cloud-native environment.

  The project evolves the Todo app into a distributed, scalable system emphasizing spec-driven development (SDD), reusable intelligence, and cloud-native best practices. All development must adhere to the Agentic Dev Stack: AGENTS.md + Spec-Kit Plus + Claude Code. No manual coding is permitted; all implementations must derive from refined specifications generated via Claude Code.

  Core Goal: Achieve a production-grade deployment on Oracle Cloud Infrastructure (OCI) using Oracle Kubernetes Engine (OKE), with Dapr for runtime abstractions, ensuring scalability, resilience, and loose coupling. This phase prioritizes event-driven patterns for features like recurring tasks and reminders, while maintaining stateless services for horizontal scaling.

  Non-Negotiable Principles (WHY):

  Spec-Driven Development First: Every feature, component, and deployment step must start with a Markdown specification (speckit.specify). Refine specs iteratively until Claude Code generates correct outputs. No code or infrastructure changes without linked specs, plans, and tasks.
  Cloud-Native and AI-Native Focus: The system must be designed for Kubernetes orchestration, emphasizing portability, observability, and AI-assisted operations (e.g., using kubectl-ai and kagent for deployments). Prioritize AI-driven blueprints for spec-driven deployment, drawing from research on spec-driven infrastructure automation.
  Security and Compliance:
  Enforce JWT-based authentication via Better Auth for all APIs.
  Use Dapr Secrets Management (backed by Kubernetes Secrets) for credentials (e.g., database URLs, API keys).
  All data must be encrypted in transit (TLS) and at rest (Neon DB defaults).
  User isolation: Tasks and conversations must be scoped to authenticated user_ids; no cross-user data leakage.
  Compliance: Adhere to basic data privacy (e.g., no logging of sensitive PII beyond necessities).

  Performance and Scalability Expectations:
  Services must be stateless where possible, with state managed via Dapr State Management or Neon DB.
  Target < 500ms response times for chat interactions and task operations under load.
  Horizontal scaling: Design for at least 3 replicas per service in OKE.
  Resource limits: Pods must not exceed 1 vCPU and 2GB RAM per instance (aligned with Oracle Always Free tier: 4 OCPUs, 24GB RAM total).
  Event processing: Kafka (or Dapr Pub/Sub alternative) must handle at least 100 events/minute with no loss.

  Reliability and Resilience:
  Implement retries, circuit breakers, and timeouts via Dapr Service Invocation.
  Use health checks and liveness probes in Kubernetes manifests.
  Error handling: Graceful degradation for tool calls; always confirm actions in chatbot responses.
  Backup: Database snapshots via Neon; Kafka topics with replication factor >=1.

  Sustainability and Cost Efficiency:
  Leverage Oracle Cloud Always Free tier exclusively (OKE with 4 OCPUs, 24GB RAM; no paid upgrades).
  No vendor lock-in: Use Dapr to abstract Pub/Sub (Kafka preferred; fallback to other components like Redis if needed) and state stores.
  Minimize resource waste: Auto-scale deployments based on load; use ephemeral storage where possible.

  Tech Stack Constraints (WHAT NOT TO CHANGE):

  Frontend: Next.js 16+ (App Router), OpenAI ChatKit for chatbot UI.
  Backend: Python FastAPI, SQLModel for ORM, OpenAI Agents SDK for AI logic, Official MCP SDK for tools.
  Database: Neon Serverless PostgreSQL (external to cluster; connection via Dapr State if applicable).
  Event Streaming: Kafka (self-hosted via Strimzi on OKE or Redpanda Cloud free tier). If access issues, swap to another Dapr Pub/Sub component (e.g., Redis) without code changes.
  Distributed Runtime: Dapr (full usage: Pub/Sub, State, Bindings (Jobs API for cron/reminders), Secrets, Service Invocation).
  Containerization: Docker (use Gordon AI agent for operations if available; fallback to standard CLI).
  Orchestration: Oracle Kubernetes Engine (OKE) on OCI Always Free tier. No other clouds (e.g., DigitalOcean, GKE, AKS) permitted.
  Deployment Tools: Helm Charts for packaging; kubectl-ai and kagent for AI-assisted ops; GitHub Actions for CI/CD.
  Monitoring/Logging: Basic Kubernetes metrics + OCI Monitoring (free tier); integrate Dapr observability.
  Authentication: Better Auth with JWT tokens.
  AI Tools: Claude Code for all implementations; Spec-Kit Plus for specs; MCP for agent prompts.

  Prohibited Changes:

  No deviation from Python 3.13+ or Next.js without spec update.
  No direct library integrations (e.g., kafka-python); use Dapr abstractions only.
  No manual infrastructure provisioning; generate via Claude Code and AI ops tools.

  Patterns Allowed (HOW):

  Architecture Patterns:
  Microservices: Separate pods for Frontend, Backend (with MCP), Notification Service, Recurring Task Service.
  Event-Driven: Publish events to Kafka topics (task-events, reminders, task-updates) for decoupling.
  Stateless Design: Store conversation history and tasks in Neon DB or Dapr State; no in-memory state.

  Feature Implementation Patterns:
  Intermediate Features (Priorities, Tags, Search, Filter, Sort): Extend MCP tools with parameters; use SQLModel for queries.
  Advanced Features (Recurring Tasks, Due Dates, Reminders): Use Dapr Jobs API for scheduling (exact-time callbacks, not polling); chain MCP tools in agent flows.
  Natural Language Handling: Agent must parse intents and invoke tools (e.g., list_tasks with filters).

  Deployment Patterns:
  CI/CD: GitHub Actions workflows for build, test, deploy to OKE.
  Blueprints: Use spec-driven blueprints via Claude Code Agent Skills for OKE manifests.
  Local Testing: Minikube with Dapr before OKE deployment.
  OCI-Specific: Use OCI CLI for cluster setup; kubectl for management.

  Coding and Spec Patterns:
  Atomic Tasks: Every speckit.tasks entry must be testable independently.
  References: All code must link back to spec sections (e.g., [From: speckit.specify §3.2]).
  Iteration: Refine specs if Claude Code outputs fail; log iterations in specs history folder.
response: |
  Successfully updated the constitution file to include Phase V Cloud-Native Todo requirements while preserving all existing content. The new section outlines the foundational principles, constraints, and non-negotiable rules for implementing advanced features with event-driven architecture and cloud-native deployment on Oracle Cloud Infrastructure.
outcome: |
  Updated .specify/memory/constitution.md with Phase V requirements including cloud-native architecture, event-driven patterns, Oracle Cloud Infrastructure deployment, Dapr runtime, Kafka/Redpanda event streaming, and all related constraints and patterns. All existing constitution content was preserved.
evaluation: |
  The constitution update successfully incorporates Phase V requirements while maintaining all previous content. The new section clearly defines the cloud-native architecture, event-driven patterns, and Oracle Cloud Infrastructure deployment requirements with appropriate constraints and patterns for the advanced Todo features implementation.
---