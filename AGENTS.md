# AGENTS.md – Phase V: Advanced Cloud-Native Todo (Detailed Edition)

## 1. Purpose & Scope

This file is the **binding constitution** for every AI agent participating in **Phase V** of the Hackathon II Todo evolution project.

**Phase V goals (recap):**
- Implement **Intermediate** features: Priorities, Tags/Categories, Search & Filter, Sort
- Implement **Advanced** features: Recurring Tasks, Due Dates & Reminders (with notifications)
- Introduce **event-driven architecture** using Kafka (or Redpanda) + Dapr Pub/Sub
- Use **Dapr** sidecars for Pub/Sub, State, Bindings (cron/scheduler), Secrets, Service Invocation
- Deploy to **local Minikube** → **cloud** (preferred: DigitalOcean DOKS, AKS, GKE, OKE)
- Enable **CI/CD** (GitHub Actions), **monitoring/logging**, **AIOps** (kubectl-ai, kagent)
- Maximize **bonus points**: Reusable Intelligence (Agent Skills + Subagents), Cloud-Native Blueprints

**Core development paradigm:**  
**Spec-Driven Development + Reusable Intelligence**  
No agent may write application code, infrastructure manifests, Helm values, Dapr components, or CI/CD workflows unless they are strictly derived from the Spec-Kit lifecycle:

**Constitution → Specify → Plan → Tasks → Implement**

## 2. Non-Negotiable Principles (speckit.constitution)

Agents **must** enforce these rules at all times:

1. **Event-Driven First**  
   All state-changing operations (create/update/complete/delete/recurring spawn/reminder trigger) **must** publish domain events.

2. **Dapr Abstraction Mandatory**  
   - No direct Kafka client libraries (kafka-python, aiokafka, etc.)  
   - No direct database drivers (psycopg, SQLModel session) in business logic  
   - All inter-service and infrastructure communication must go through Dapr sidecar HTTP/gRPC APIs

3. **Stateless Services**  
   - Chat API, Notification Service, Recurring Task Service must be **completely stateless**  
   - All persistent state lives in Neon PostgreSQL (via Dapr State or direct SQLModel – but preferably Dapr)

4. **User Isolation & Security**  
   - Every operation (MCP tool, API, event) must carry and validate `user_id`  
   - JWT verification on every ingress request  
   - No cross-tenant data leakage allowed

5. **Observability & Resilience**  
   - Every service must emit structured logs (JSON)  
   - Every published event must contain `trace_id`, `span_id`, `timestamp`, `user_id`  
   - Use Dapr built-in retries, circuit breakers, timeouts

6. **Reusable Intelligence & Blueprints**  
   - Create **Agent Skills** for:  
     - Generating Dapr component YAML  
     - Creating Helm chart templates for microservices  
     - Producing Kafka event schemas (Avro/JSON)  
     - Generating GitHub Actions CI/CD workflows  
   - These skills should be reusable across future Panaversity projects

7. **AI-Ops Preference**  
   - Prefer generating K8s manifests with **kubectl-ai** or **kagent**  
   - Prefer container analysis & optimization with **Gordon** (Docker AI) when available

8. **Technology Constraints**  
   - Kafka / Redpanda (strongly preferred)  
   - Dapr 1.13+  
   - Helm 3+  
   - Next.js 15 / FastAPI / SQLModel / Neon  
   - OpenAI Agents SDK + Official MCP SDK

## 3. Strict Agent Rules

1. **No code without Task ID**  
   Every file, YAML, or code block **must** start with:

   ```text
   [Task: T-042]
   [From: speckit.specify §4.2.3, speckit.plan §5.1.2]

No architecture change without Plan update
Adding a new Kafka topic, Dapr component, sidecar, or service requires explicit update in speckit.plan.
No new feature without Specify update
Voice commands, multi-language support, audit log viewer, etc. → must first appear in speckit.specify.
Dapr-first communication pattern
Allowed patterns:Python# Good – Dapr Pub/Sub
await httpx.post("http://localhost:3500/v1.0/publish/todo-pubsub/task-events", json=event)

# Good – Dapr State
await httpx.post("http://localhost:3500/v1.0/state/statestore", json=[{"key": f"conv-{id}", "value": data}])

# Bad – direct Kafka
producer.send("task-events", event)
Event Schema Discipline
All domain events must follow at minimum:JSON{
  "event_type": "TASK_CREATED | TASK_COMPLETED | REMINDER_DUE | RECURRING_SPAWNED | ...",
  "event_id": "uuid",
  "timestamp": "2026-02-07T10:12:00Z",
  "trace_id": "otel-trace-id",
  "user_id": "user_abc123",
  "payload": { ... }
}
Reminder & Recurring Engine
Use Dapr Jobs API (preferred) or Dapr Cron Binding for scheduling
Never poll database every minute – use exact-time triggers


4. Recommended Agent Workflow Patterns
Pattern A: Adding a new feature

Update / propose change in speckit.specify
Update / propose change in speckit.plan
Break into atomic tasks in speckit.tasks
Implement one task at a time

Pattern B: Creating reusable intelligence
Example prompt agents should accept:
"Create a reusable Agent Skill that generates a complete Dapr component YAML for pubsub.kafka given broker address, topic list, and consumer group."
→ Output should be saved as a template in /skills/dapr-pubsub-generator.md
Pattern C: Infrastructure generation
"Using kubectl-ai syntax, generate a Helm values file for deploying the Notification Service with 3 replicas, Dapr sidecar, and resource limits."
→ Agent should output command + expected YAML
5. Failure & Escalation Modes (Agents MUST detect & report)
Agents must refuse and report if they encounter:

Request to write direct Kafka producer/consumer code
Request to bypass Dapr for state or pub/sub
Missing user_id validation in proposed code
Stateful service logic without clear justification
No tracing context in events
Helm chart without Dapr annotations
Deployment without readiness/liveness probes

Report format:
textBLOCKED: Violation of speckit.constitution §2.3 (Stateless Services)
Missing: user_id enforcement in proposed MCP tool
Action required: Update speckit.specify or speckit.plan first

6. Quick Reference – Allowed Tools & Preferences
Task Type,Preferred Tool / Method,Fallback
Container build,Gordon (Docker AI),Claude + standard Dockerfile
K8s manifest generation,kubectl-ai / kagent,Claude hand-written YAML
Dapr component YAML,Reusable Agent Skill / Template,Claude generation
Event publishing,Dapr Pub/Sub HTTP,—
State management,Dapr State HTTP,Direct SQLModel (last resort)
Scheduled jobs,Dapr Jobs API,Dapr Cron Binding
CI/CD workflow,GitHub Actions YAML via Agent Skill,Claude generation

7. Final Binding Statement
This AGENTS.md file has higher precedence than any conflicting instruction in CLAUDE.md, project README, or conversation history for Phase V implementation.
Every agent must re-read this file at the beginning of each session.
