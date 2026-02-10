# Qwen Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

---

@AGENTS.md

## Project Overview: Todo AI Chatbot Application

A full-stack multi-user Todo application with AI-powered chatbot interface for managing tasks through natural language using MCP (Model Context Protocol) server architecture.

### Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+ (App Router) with OpenAI ChatKit |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth (JWT tokens) |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| Spec-Driven | Claude Code + Spec-Kit Plus |

### Feature Progression

**Basic Level (Core Essentials):**
1. Add Task – Create new todo items
2. Delete Task – Remove tasks from the list
3. Update Task – Modify existing task details
4. View Task List – Display all tasks
5. Mark as Complete – Toggle task completion status

**Intermediate Level (Organization & Usability):**
1. Priorities & Tags/Categories – Assign levels (high/medium/low) or labels (work/home)
2. Search & Filter – Search by keyword; filter by status, priority, or date
3. Sort Tasks – Reorder by due date, priority, or alphabetically

**Advanced Level (Intelligent Features):**
1. Recurring Tasks – Auto-reschedule repeating tasks
2. Due Dates & Time Reminders – Set deadlines with date/time pickers; browser notifications

### Database Models

| Model | Fields | Description |
|-------|--------|-------------|
| Task | user_id, id, title, description, completed, created_at, updated_at | Todo items |
| Conversation | user_id, id, created_at, updated_at | Chat session |
| Message | user_id, id, conversation_id, role (user/assistant), content, created_at | Chat history |

### Authentication Flow (JWT)

1. User logs in on Frontend → Better Auth creates session and issues JWT token
2. Frontend makes API call → Includes JWT in `Authorization: Bearer <token>` header
3. Backend receives request → Extracts token, verifies signature using shared secret
4. Backend identifies user → Decodes token to get user ID
5. Backend filters data → Returns only tasks belonging to that user

**Shared Secret:** Both frontend (Better Auth) and backend (FastAPI) use `BETTER_AUTH_SECRET` environment variable.

---

## Specialized Agent Configuration

Use the following agents for specific tasks:

### Authentication
- **better-auth-integrator**: For implementing Better Auth features, JWT configuration, protected routes, session management, and auth security reviews.

### Frontend Development
- **frontend-architect**: For Next.js App Router architecture, server components, server actions, data fetching, and Tailwind UI components.
- **nextjs-frontend-optimizer**: For code splitting, image optimization, Server/Client Component boundaries, responsive design, and performance optimization.
- **ui-editor**: For modifying UI components, layouts, styling changes, and responsive design fixes.

### Backend Development
- **fastapi-auth-architect**: For FastAPI authentication infrastructure, multiple auth schemes (JWT, API keys), protected endpoints, and dependency injection patterns.
- **backend-architect**: For error handling, dependency injection, and Pydantic schema design.
- **fastapi-routes-agent**: For implementing CRUD endpoints with user-based isolation and Pydantic validation.

### Database
- **neon-db-operator**: For Neon PostgreSQL operations, schema changes, migrations, query optimization, connection management, and credential retrieval.
- **database-architect**: For database schema design, SQLModel configuration, and migration planning.
- **sqlmodel-schema-architect**: For defining SQLModel models with relationships and constraints.

### Specifications & Planning
- **technical-spec-writer**: For creating detailed specs with Gherkin acceptance criteria, REST API definitions, and database schemas.
- **project-architect**: For architectural planning, establishing standards, and coordinating complex implementations.
- **api-designer**: For RESTful API design, OpenAPI standards, and endpoint specifications.

### Testing & Security
- **integration-tester**: For end-to-end user flows, authentication protection verification, and user isolation testing.
- **data-access-guardian**: For verifying data ownership and access controls (IDOR prevention).
- **authentication-specialist**: For security-critical implementations and vulnerability prevention.

---

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

---

## MCP Tools Specification

The MCP server must expose the following tools for the AI agent:

### Tool: add_task
| Attribute | Value |
|-----------|-------|
| Purpose | Create a new task |
| Parameters | user_id (string, required), title (string, required), description (string, optional) |
| Returns | task_id, status, title |

### Tool: list_tasks
| Attribute | Value |
|-----------|-------|
| Purpose | Retrieve tasks from the list |
| Parameters | user_id (string, required), status (string, optional: "all", "pending", "completed") |
| Returns | Array of task objects |

### Tool: complete_task
| Attribute | Value |
|-----------|-------|
| Purpose | Mark a task as complete |
| Parameters | user_id (string, required), task_id (integer, required) |
| Returns | task_id, status, title |

### Tool: delete_task
| Attribute | Value |
|-----------|-------|
| Purpose | Remove a task from the list |
| Parameters | user_id (string, required), task_id (integer, required) |
| Returns | task_id, status, title |

### Tool: update_task
| Attribute | Value |
|-----------|-------|
| Purpose | Modify task title or description |
| Parameters | user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional) |
| Returns | task_id, status, title |

---

## Chat API Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/{user_id}/chat | Send message & get AI response |

**Request:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| conversation_id | integer | No | Existing conversation ID (creates new if not provided) |
| message | string | Yes | User's natural language message |

**Response:**
| Field | Type | Description |
|-------|------|-------------|
| conversation_id | integer | The conversation ID |
| response | string | AI assistant's response |
| tool_calls | array | List of MCP tools invoked |

---

## Agent Behavior Specification

| Behavior | Description |
|----------|-------------|
| Task Creation | When user mentions adding/creating/remembering something, use add_task |
| Task Listing | When user asks to see/show/list tasks, use list_tasks with appropriate filter |
| Task Completion | When user says done/complete/finished, use complete_task |
| Task Deletion | When user says delete/remove/cancel, use delete_task |
| Task Update | When user says change/update/rename, use update_task |
| Confirmation | Always confirm actions with friendly response |
| Error Handling | Gracefully handle task not found and other errors |

---

## Natural Language Command Examples

| User Says | Agent Should |
|-----------|--------------|
| "Add a task to buy groceries" | Call add_task with title "Buy groceries" |
| "Show me all my tasks" | Call list_tasks with status "all" |
| "What's pending?" | Call list_tasks with status "pending" |
| "Mark task 3 as complete" | Call complete_task with task_id 3 |
| "Delete the meeting task" | Call list_tasks first, then delete_task |
| "Change task 1 to 'Call mom tonight'" | Call update_task with new title |
| "I need to remember to pay bills" | Call add_task with title "Pay bills" |
| "What have I completed?" | Call list_tasks with status "completed" |

---

## Conversation Flow (Stateless Request Cycle)

1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
9. Server holds NO state (ready for next request)

---

## Project Directory Structure

```
/frontend          – Next.js App Router with OpenAI ChatKit UI
/backend           – Python FastAPI with MCP server
/specs             – Feature specifications
/history/prompts   – Prompt History Records
/history/adr       – Architecture Decision Records
/.specify          – SpecKit Plus templates and scripts
```

---

## Security Requirements

- All endpoints require valid JWT token
- Requests without token receive 401 Unauthorized
- Each user only sees/modifies their own tasks
- Task ownership is enforced on every operation
- Never hardcode secrets; use `.env` files
- BETTER_AUTH_SECRET shared between frontend and backend

---

## Available Skills

The following skills are available for use in this project:

### Architecture & Planning Skills
- **architecture-planning**: Designs a clean, scalable, and maintainable monorepo architecture using proven patterns (feature-sliced + layered hybrid), strict dependency enforcement, boundary rules, and comprehensive visualizations.
- **monorepo-setup**: Provides a comprehensive, framework-agnostic guide to initialize a scalable monorepo project, covering initial structure, workspace configuration, shared tooling, dependency management, performance considerations, and long-term maintainability best practices.
- **root-level-guidance**: Provides detailed guidance on configuring essential root-level files for consistency, performance, and maintainability across any monorepo setup.
- **spec-kit-configuration**: Establishes a centralized design token and component specification system for visual and thematic consistency across all applications.

### Authentication & Security Skills
- **auth-skill**: Implements secure user authentication features including signup, signin, password hashing with bcrypt, JWT token generation and validation, and integration with enhanced auth libraries or practices. Use this skill when developing or troubleshooting authentication flows in web applications, APIs, or backend services to ensure secure user management.
- **better-auth-configuration**: Configures a secure, modern authentication system with best practices for registration, login, password handling, email verification, social logins, and security hardening.
- **auth-protection-testing**: Verifies that authentication and authorization protections are enforced across all protected routes, APIs, and server actions with comprehensive unauthorized access tests.
- **jwt-plugin-enable**: Enables and configures JWT authentication plugin (like fastapi-jwt-auth or Authlib) with proper secret management, token expiry, refresh routes, and revocation support.
- **jwt-token-management**: Implements secure JWT token creation, signing, verification, refresh token rotation, and blacklisting with short-lived access tokens and long-lived refresh tokens.
- **session-handling**: Manages user sessions with logout, concurrent session limits, session revocation, single sign-out, and audit logging.
- **shared-secret-setup**: Properly generates, stores, rotates, and manages shared secrets for JWT signing, database encryption, and external API keys with secure practices.
- **shared-secret-management**: Manages secure storage, rotation, and usage of secrets (API keys, JWT secrets, database credentials) using environment variables, secret managers, and rotation strategies.
- **token-verification-middleware**: Implements reusable token verification middleware using JWT, HttpOnly cookies, or headers with proper error handling and user object injection.

### Backend Development Skills
- **backend-skill**: Generates backend routes for web applications, handles HTTP requests and responses, and manages database connections. Use this skill when users request assistance with creating or modifying server-side endpoints, integrating data persistence, or building RESTful APIs in frameworks like Express.js, Flask, or Django.
- **backend-hosting**: Recommends and configures reliable hosting for FastAPI backend with options for Render, Railway, Fly.io, AWS, focusing on scalability, logs, metrics, and zero-downtime deploys.
- **dependency-injection**: Leverages FastAPI's powerful Depends system for reusable authentication, database sessions, rate limiting, and business logic injection.
- **error-handling**: Implements consistent global and custom error handling with standardized responses, logging, and proper HTTP status codes.
- **fastapi-routing**: Organizes FastAPI routes using APIRouter for modular, versioned, tagged endpoints with proper prefixes, dependencies, and response models.
- **rest-endpoint-design**: Designs clean, consistent, RESTful endpoints following industry standards with proper HTTP methods, status codes, versioning, naming conventions, and OpenAPI documentation.
- **ownership-enforcement**: Strictly enforces resource ownership on update/delete operations by verifying current user owns the resource before allowing modifications.
- **path-parameter-handling**: Safely handles path parameters with validation, type conversion, existence checks, and proper error responses for invalid or missing resources.
- **user-id-filtering**: Automatically filters query results by current user ID for list endpoints to prevent data leakage while allowing admin overrides.
- **user-isolation-verification**: Ensures strict data isolation between users in multi-tenant applications by testing that users can only access their own data across all endpoints and features.

### Database Skills
- **database-schema-design**: Designs relational database schemas, creates table definitions, and generates migration scripts. Use this skill when users need help with database structure planning, SQL table creation, or versioned schema changes in frameworks like SQLAlchemy, Rails, or raw SQL.
- **database-schema-spec**: Designs and documents database schema changes with tables, columns, indexes, relationships, migration strategy, and backward compatibility considerations.
- **migration-planning**: Plans safe, reversible database migrations with zero-downtime strategies, backfill plans, rollback procedures, and coordination with application releases.
- **schema-design**: Designs normalized, performant, and future-proof PostgreSQL database schemas with proper normalization, indexing strategy, constraints, partitioning considerations, and scalability planning.
- **neon-connection**: Configures secure, performant connection to Neon serverless PostgreSQL with connection pooling, prepared statements, branching workflow, and environment-specific settings.
- **sqlmodel-orm**: Defines database models using SQLModel (SQLAlchemy + Pydantic) for type-safe tables, relationships, and seamless integration with FastAPI schemas.
- **sqlmodel-model**: Creates advanced SQLModel models with relationships, indexes, constraints, enums, JSONB fields, computed columns, and migration-friendly patterns.
- **relationship-mapping**: Properly defines one-to-one, one-to-many, many-to-many relationships in SQLModel with back_populates, cascade rules, and lazy/eager loading considerations.
- **model-definition**: Defines clean, reusable SQLModel models with proper field types, defaults, constraints, indexes, and separation of concerns between table models and schemas.

### Frontend Development Skills
- **client-component**: Properly marks and implements Client Components for interactivity, state management, and browser APIs while keeping bundle size minimal.
- **server-component**: Maximizes use of React Server Components for data fetching, reduced bundle size, and improved performance in Next.js App Router.
- **server-components**: Leverages React Server Components for optimal performance by fetching data on the server, reducing client bundle size, and enabling streaming.
- **frontend-building-components-skill**: This Skill equips Claude to construct frontend web elements including pages, reusable components, layouts, and styling. It provides structured guidance for generating HTML, CSS, and JavaScript code. Use this Skill when users request help with creating, modifying, or troubleshooting frontend UI elements, such as building a webpage layout, styling components, or implementing interactive features without backend integration.
- **responsive-design**: Implements mobile-first responsive design using Tailwind's responsive utilities, proper breakpoints, flexible layouts, and accessibility considerations.
- **responsive-component-design**: Designs reusable, mobile-first responsive components using Tailwind CSS with proper breakpoints, flexible layouts, grid/flex systems, and accessibility considerations.
- **form-handling**: Implements robust form handling with validation, error display, loading states, server actions, and accessibility features.
- **client-side-api-calling**: Implements secure, efficient client-side data fetching using React Server Actions, SWR, or tanstack-query with proper error handling, loading states, authentication, and caching.
- **nextjs-app-router**: Sub-agent skill for setting up and enforcing best practices in a Next.js 14+ project using the App Router. Ensures correct folder structure, route groups, layouts, parallel routes, intercepting routes, and metadata handling.
- **tailwind-css-styling**: Implements clean, consistent, reusable Tailwind CSS styling with design tokens from spec-kit, dark mode support, custom components, and utility best practices.
- **vercel-deployment**: Configures optimal Vercel deployment for Next.js App Router projects with preview branches, environment variables, serverless functions, edge runtime, and performance optimizations.

### Testing & Quality Assurance Skills
- **end-to-end-flow-testing**: Designs and implements comprehensive end-to-end tests covering critical user journeys using Playwright for browser automation and direct API calls for backend flows.
- **crud-route-implementation**: Implements complete CRUD operations across Next.js routes and FastAPI endpoints with proper validation, error handling, and optimistic updates.

### API & Documentation Skills
- **api-specification**: Creates clear, versioned REST/GraphQL API specifications with endpoints, request/response schemas, authentication, error handling, and examples.
- **environment-variables**: Manages secure environment variables across development, preview, staging, and production with secret handling, validation, and documentation.
- **header-attachment**: Properly attaches custom headers to responses including CORS, security headers, rate limit info, request IDs, and caching directives.

### UI/UX & Task Management Skills
- **task-list-ui**: Implements interactive task/todo list UI with add, complete, edit, delete, filtering, sorting, and persistence features.
- **user-story-creation**: Converts requirements and specifications into well-written, INVEST-compliant user stories with clear titles, descriptions, and actionable tasks.
- **acceptance-criteria**: Writes comprehensive, unambiguous Given-When-Then acceptance criteria that fully define when a user story is considered complete.

### Documentation & Specification Skills
- **markdown-spec-writing**: Writes clear, professional, well-structured Markdown specifications for features, components, modules, or any technical documentation with consistent formatting, headings, tables, code blocks, and diagrams.

### Cloud-Native-Blueprint & Advanced Skills
- **dapr-jobs-reminders**: Dapr Jobs API for scheduled tasks, recurring jobs, and due-date reminders in cloud-native applications. Use when implementing scheduled background jobs, task reminders, recurring tasks, cron-like scheduling, or time-based automation with Dapr. Covers Dapr Jobs API configuration, reminder patterns, scheduling workflows, and integration with event-driven architectures for Todo applications.
- **kafka-redpanda-dapr**: Event streaming infrastructure with Kafka or Redpanda integrated with Dapr for cloud-native applications. Use when implementing event-driven microservices, pub/sub messaging, event streaming, or async communication. Redpanda is recommended as a Kafka-compatible alternative with better performance and lower resource usage. Covers Redpanda deployment, Dapr Kafka component configuration, topic management, and event streaming patterns for Todo applications.
- **oci-oke-deployment**: Oracle Cloud Infrastructure (OCI) Kubernetes Engine (OKE) deployment and management for cloud-native applications. Use when deploying to Oracle Cloud Kubernetes, creating OKE clusters, configuring OCI networking, managing node pools, setting up OCI load balancers, or implementing cloud-native applications on Oracle Cloud. Covers OCI CLI usage, cluster provisioning, VCN configuration, Dapr installation on OKE, and Oracle Cloud best practices.
- **cloud-native-blueprints**: Comprehensive cloud-native architecture blueprints including containerization, orchestration, service mesh, observability, and deployment strategies for modern applications.

### Claude Code Skills
- **claude-md-generation**: Generates a comprehensive CLAUDE.md file documenting the entire project structure, architecture, available skills, and recommended workflow.
