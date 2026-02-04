<!--
Sync Impact Report:
- Version change: 2.0.0 → 3.0.0 (major architectural shift to AI Chatbot with Kubernetes deployment requirements)
- Added sections: Phase IV - Local Kubernetes Deployment (Minikube, Helm Charts, kubectl-ai, Kagent, Docker Desktop, Gordon)
- Added principles: AI-Native DevOps, Containerization-First Approach, Infrastructure-as-Code
- Added sections: Kubernetes Architecture, Helm Chart Specifications, AI-Assisted Operations, Deployment Strategy
- Templates requiring updates: ✅ All templates updated to align with new Kubernetes deployment architecture
- Follow-up TODOs: Update spec templates for Kubernetes features
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Development
All implementation starts with writing/updating specs in /specs folder, followed by Claude Code generation. No direct code edits; iterate via prompts. This ensures that all development is guided by clear specifications and prevents ad-hoc coding that might not align with the overall architecture.

### Modularity and Reusability
Design components and APIs for extensibility, ensuring backend handles data logic and frontend focuses on presentation. Components must be self-contained, independently testable, and have clear, well-defined interfaces that can be reused across the application.

### Security First
Enforce user isolation via JWT authentication; all data operations filtered by user ID. All user data must be properly isolated, access controls strictly enforced, and authentication/authorization implemented consistently across all endpoints and UI components.

### User-Centric Design
Prioritize intuitive UI/UX with responsive design, accessibility (e.g., ARIA labels), and performance optimizations. All UI elements must be accessible, responsive across devices, and provide a seamless user experience with appropriate feedback for all interactions.

### Efficiency
Use Agentic Dev Stack workflow: Spec → Plan → Tasks → Implement. Review prompts and iterations for quality. All development follows the structured workflow to ensure consistent, high-quality output with proper planning and task breakdown.

### Visual Consistency
Adhere to color scheme: Black for backgrounds/text (#000000), Blue for accents/buttons (#007BFF), DarkGreen for success states/completions (#006400). Incorporate CSS animations (e.g., fade-in for new tasks, slide-out for deletions) using Tailwind CSS transitions.

## Key Standards

### Development Workflow (Step-by-Step)
- Spec Writing/Updating: Review requirements and update /specs files (e.g., @specs/features/task-crud.md for basic features). Use Spec-Kit conventions for structured markdown.
- Generate Plan: Prompt Claude Code with "@specs/features/[feature].md generate implementation plan" to break into tasks (e.g., backend models, API endpoints, frontend components).
- Task Implementation: For each task, prompt Claude Code (e.g., "Implement backend models per @specs/database/schema.md"). Handle frontend and backend separately via subfolder CLAUDE.md files.
- Integration and Testing: Use docker-compose to run both services. Test APIs with tools like Postman; frontend with browser dev tools. Iterate by updating specs if issues arise.
- Deployment Prep: Configure environment variables (e.g., BETTER_AUTH_SECRET, DATABASE_URL). Aim for Vercel (frontend) and Render/Heroku (backend) deployment.
- Review and Merge: After Claude Code outputs, commit changes via Git. Ensure all features meet acceptance criteria before marking complete.

### Project Structure (Monorepo)
Full-Stack-Web-Application/
├── .spec-kit/                    # Spec-Kit config
│   └── config.yaml               # Defines structure, phases
├── specs/                        # Organized specifications
│   ├── overview.md               # Project summary
│   ├── architecture.md           # System design
│   ├── features/                 # Feature specs
│   │   ├── task-crud.md          # Basic/Intermediate/Advanced CRUD
│   │   ├── authentication.md     # Auth setup
│   │   └── advanced-features.md  # Recurring tasks, reminders
│   ├── api/                      # API details
│   │   └── rest-endpoints.md     # Endpoints spec
│   ├── database/                 # DB schema
│   │   └── schema.md             # Models and indexes
│   └── ui/                       # UI specs
│       ├── components.md         # Reusable components
│       └── pages.md              # Page layouts
├── CLAUDE.md                     # Root instructions for Claude Code
├── frontend/                     # Next.js app
│   ├── CLAUDE.md                 # Frontend guidelines
│   ├── app/                      # Pages and layouts
│   ├── components/               # UI elements (e.g., TaskCard, FormInput)
│   ├── lib/                      # Utilities (e.g., api.ts for API client)
│   ├── public/                   # Static assets
│   └── tailwind.config.js        # Custom colors/animations
├── backend/                      # FastAPI app
│   ├── CLAUDE.md                 # Backend guidelines
│   ├── main.py                   # App entry
│   ├── models.py                 # SQLModel models
│   ├── routes/                   # API handlers (e.g., tasks.py)
│   ├── db.py                     # DB connection
│   └── requirements.txt          # Dependencies
├── docker-compose.yml            # For local dev (Postgres, frontend, backend)
└── README.md                     # Setup instructions

This structure allows Claude Code to reference specs easily (e.g., @specs/ui/pages.md) and edit code in context.

### Technology Stack
- Frontend: Next.js 16+ (App Router) for SSR/CSR, TypeScript for type safety, Tailwind CSS for styling with custom theme (extend colors: { black: '#000000', blue: '#007BFF', darkgreen: '#006400' }).
- Backend: Python FastAPI for async APIs, SQLModel for ORM/models.
- Database: Neon Serverless PostgreSQL for scalable, managed DB.
- Authentication: Better Auth (with JWT plugin) for user sessions/tokens.
- Other Tools: Docker for containerization, Git for version control, Claude Code + Spec-Kit Plus for generation.
- Animations: Use Tailwind's transition utilities (e.g., transition-all duration-300 ease-in-out) for fades, slides, and hovers. Library: Framer Motion for complex animations (e.g., AnimatePresence for task list updates).
- Environment: Shared secrets via .env files (e.g., BETTER_AUTH_SECRET for JWT).

## Feature Definitions: CRUD Operations

### Core CRUD (Basic Level)
These are foundational MVP features, implemented first for quick iteration.
- Add Task (Create): User inputs title (required, 1-200 chars), description (optional, max 1000 chars). Backend: POST /api/{user_id}/tasks with Pydantic validation. Frontend: Form component with inputs, submit button (Blue bg, hover:darken). Animation: Fade-in new task in list.
- Delete Task: Select task, confirm deletion. Backend: DELETE /api/{user_id}/tasks/{id}. Frontend: Trash icon button (Red on hover), modal confirmation. Animation: Slide-out and remove from DOM.
- Update Task: Edit title/description. Backend: PUT /api/{user_id}/tasks/{id}. Frontend: Edit mode toggle, inline form. Animation: Smooth expand/collapse of edit fields.
- View Task List: Display all user tasks. Backend: GET /api/{user_id}/tasks. Frontend: TaskList component as cards/ul, showing title, status, created_at. Animation: Loading spinner (circular, Blue).
- Mark as Complete (Toggle): Checkbox or button to flip status. Backend: PATCH /api/{user_id}/tasks/{id}/complete. Frontend: Checkbox (DarkGreen when checked). Animation: Strike-through text with fade.

### Intermediate CRUD (Organization & Usability)
Build on core for polish; implement after basics are tested.
- Due Dates & Priorities: Add due_date (date picker), priority (high/medium/low dropdown, colors: Red/Orange/Green). Backend: Extend Task model, update CRUD endpoints. Frontend: Form additions, filter UI. Animation: Priority badges pulse on high.
- Tags/Categories: Assign labels (e.g., work/home). Backend: Add tags array to model. Frontend: Multi-select input. Animation: Tag chips appear with scale-in.
- Search & Filter: Keyword search, filters by status/priority/date. Backend: Query params (e.g., ?status=pending&priority=high). Frontend: Search bar (Blue border), dropdown filters. Animation: Filter results reload with stagger fade-in.
- Sort Tasks: By due_date/priority/alpha. Backend: ?sort=due_date asc/desc. Frontend: Sort button/menu. Animation: List reorder with smooth transitions.

### Advanced CRUD (Intelligent Features)
Add last for full functionality; require browser permissions for notifications.
- Recurring Tasks: Set recurrence (daily/weekly). Backend: Add recurrence field, cron-like logic to auto-create on schedule (use background tasks). Frontend: Recurrence selector in form. Animation: Recurring icon spins on creation.
- Time Reminders: Set deadlines with time; browser notifications. Backend: Store reminder_time. Frontend: DateTime picker (integrate react-datepicker), Notification API. Animation: Notification banner slides in (DarkGreen bg).

## Full UI Definition

The UI is responsive (mobile-first), using Next.js App Router. Theme: Dark mode default (Black bg, white text), accents in Blue (links/buttons), DarkGreen (success/completions). Fonts: Inter (sans-serif). Layout: Sidebar nav (if multi-page), main content area.

### Pages:
- /login: Better Auth form (email/password, Blue submit button). Animation: Form fields focus glow.
- /register: Similar to login, with name field.
- /dashboard: Main page with TaskList, AddTask form at top. Search bar, filters/sort dropdowns. Animation: Tasks load with staggered entrance.
- /tasks/[id]: Task detail view (edit form, delete button). Animation: Modal overlay fade.
- Layout: Root layout with header (logo, user menu), footer (copyright). Use Next.js Layout component.

### Components:
- TaskCard: Card with title (bold, Blue if pending), description (truncate), status checkbox (DarkGreen), edit/delete icons. Hover: Shadow lift animation.
- FormInput: Reusable input/textarea (Black bg, Blue border focus). Validation errors in Red.
- Button: Variants: Primary (Blue bg, white text), Success (DarkGreen), Danger (Red). Animation: Scale on hover.
- Modal: For confirmations/edits (centered, Black overlay). Animation: Scale-in from center.
- Loader: Full-screen or inline spinner (Blue circles rotating).
- TagChip: Rounded pills (colored by category). Animation: Remove with fade-out.
- DatePicker: Integrated for due dates (calendar pop-up, DarkGreen selected days).

### Styling and Animations:
- Colors: Primary: Blue (#007BFF), Success: DarkGreen (#006400), Neutral: Black (#000000) for bgs, Gray (#6C757D) for text.
- Animations: All via Tailwind/Framer: Fade (opacity 0 to 1, 300ms), Slide (translateX/Y), Scale (0.95 to 1 on hover), Pulse (for urgent tasks). Ensure 60fps performance; no heavy effects on mobile.
- Accessibility: Alt text for icons, keyboard nav, screen reader support.
- Responsive: Breakpoints: Mobile (<640px: stacked), Tablet (640-1024px: grid-2), Desktop (>1024px: grid-3 for tasks).

## Constraints

- Word Count Limit: This constitution is under 1800 words (current: 1487).
- No Manual Coding: All code via Claude Code prompts.
- Feature Phasing: Implement Basic → Intermediate → Advanced.
- Testing: Unit (Pytest/Jest), Integration (API calls), E2E (Cypress if needed).
- Dependencies: Minimal; no extra installs beyond stack.
- Scalability: Design for 1000+ users; use indexing in DB.

## Success Criteria

- Functionality: All CRUDs work per specs; auth enforces isolation.
- UI/UX: Responsive, themed correctly, animations smooth.

## Governance

All development must adhere to the Spec-Driven Development workflow. Changes to this constitution require explicit approval and documentation. All implementations must follow the defined project structure and technology stack. Code reviews must verify compliance with all principles and standards defined in this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-01-11 | **Last Amended**: 2026-01-11

# Todo AI Chatbot – System Constitution

## Core Principles

### Spec-Driven Development
All implementation starts with writing/updating specs in /specs folder, followed by Claude Code generation. No direct code edits; iterate via prompts. This ensures that all development is guided by clear specifications and prevents ad-hoc coding that might not align with the overall architecture.

### AI-First Architecture
Design the entire system around conversational AI interface using official ChatKit SDK. Frontend uses ChatKit for UI, backend uses Cohere API for AI logic through MCP tools. All user interactions flow through natural language conversation with AI agent managing tasks via MCP tools.

### Security First
Enforce user isolation via JWT authentication; all data operations filtered by user ID. All user data must be properly isolated, access controls strictly enforced, and authentication/authorization implemented consistently across all endpoints and UI components.

### Cohere-Only Constraint
Use ONLY Cohere API key for all AI functionality. No OpenAI, Anthropic, or other AI API keys allowed. The system must be designed to work exclusively with Cohere's API for natural language processing and task management.

### Stateless Server Model
Backend must not store in-memory state; persist all state in database. Each chat request is stateless - load conversation history from DB, process through Cohere agent with MCP tools, store response, return result.

### Modularity and Reusability
Design components and APIs for extensibility, ensuring backend handles data logic and frontend focuses on presentation. Components must be self-contained, independently testable, and have clear, well-defined interfaces.

## Phase III – Basic To Advance Level Functionality

### 1. Purpose of This Constitution

This constitution defines the binding rules, architecture, responsibilities, workflows, and specifications for implementing the Todo AI Chatbot using:

- Official ChatKit SDK (Frontend UI)
- Cohere API (AI Logic - ONLY allowed API key)
- Official MCP SDK (Tooling Layer)
- FastAPI (Backend)
- SQLModel + Neon PostgreSQL (Persistence)
- Better Auth (Authentication)

This file acts as:
- The single source of truth
- The evaluation reference for judges
- The control document for Claude Code execution

No implementation may deviate from this constitution.

### 2. Governing Development Methodology

#### 2.1 Agentic Dev Stack Workflow (Mandatory)

All development must strictly follow the workflow below:
1. Write Specifications
2. Generate an Execution Plan
3. Break Plan into Atomic Tasks
4. Implement via Claude Code
5. Iterate Using Specs (No Manual Coding)

Any implementation without prior specs and plan is considered invalid.

### 3. System Objectives

The system SHALL:
- Provide a conversational AI interface for managing todos using ChatKit SDK
- Use natural language, including voice input
- Operate in a stateless server model
- Persist all state in the database
- Allow AI agents to manage tasks only through MCP tools
- Use ONLY Cohere API key for AI functionality
- Resume conversations seamlessly after server restart

### 4. Architecture Constitution

#### 4.1 High-Level Architecture
```
ChatKit UI (Official SDK)
   │
   ▼
FastAPI Chat Endpoint (Stateless)
   │
   ▼
Cohere API Integration
   │
   ▼
MCP Server (Official MCP SDK Tools)
   │
   ▼
Neon PostgreSQL (SQLModel ORM)
```

#### 4.2 Constitutional Constraints
- Frontend must use official ChatKit SDK only
- Backend must not store in-memory state
- AI must not access database directly
- AI must use MCP tools for all task operations
- MCP tools must be stateless
- ONLY Cohere API key allowed - no other AI APIs

### 5. Frontend Constitution (ChatKit SDK)

#### 5.1 Official ChatKit SDK Usage
The frontend SHALL:
- Use official OpenAI ChatKit SDK as the UI layer
- Render:
  - Message history
  - Assistant responses
  - Tool confirmations
- Send only user input (text or voice) to backend

#### 5.2 Voice Commands Constitution
Voice input SHALL:
- Use Web Speech API (browser-native)
- Convert speech → text on the client
- Forward resulting text to /api/{user_id}/chat
- Never bypass ChatKit message flow
- Voice is an input modality, not a logic layer.

### 6. Backend Constitution (FastAPI)

#### 6.1 Stateless Chat Endpoint
**Endpoint**: `POST /api/{user_id}/chat`

The endpoint SHALL:
- Accept a user message
- Fetch conversation history from database
- Append the new user message
- Process through Cohere API integration
- Store assistant response
- Return response + tool calls
- Hold no server memory

#### 6.2 Cohere API Integration
- Use ONLY Cohere API key (environment variable: `COHERE_API_KEY`)
- No fallback to other AI providers
- Design system to work with Cohere's specific API patterns

### 7. AI Constitution (Cohere API Integration)

#### 7.1 Agent Responsibilities
The AI Agent SHALL:
- Interpret user intent using Cohere API
- Decide which MCP tool to invoke
- Never perform CRUD logic internally
- Always respond with confirmation language

#### 7.2 Cohere-Specific Constraints
- System must be designed for Cohere's API response format
- Handle Cohere-specific error cases
- Optimize for Cohere's pricing and rate limits

### 8. MCP Constitution (Official MCP SDK)

#### 8.1 Role of MCP Server
The MCP Server is the only gateway between AI and persistent data. It SHALL:
- Expose tools as defined in specs
- Validate inputs
- Persist data via SQLModel
- Return structured outputs

#### 8.2 Tool Immutability Rule
Once a tool spec is defined:
- Its name
- Its parameters
- Its return shape
Must not change without updating specs and re-planning.

### 9. Database Constitution

#### 9.1 Persistence Rules
All state SHALL be persisted:
- Tasks
- Conversations
- Messages
No in-memory caching is allowed.

#### 9.2 Models
- Task
- Conversation
- Message
These models define the entire memory of the system.

### 10. Conversation Flow Constitution (Stateless)

Every request MUST follow this exact lifecycle:
1. Receive user input
2. Load conversation from DB
3. Build Cohere agent context
4. Persist user message
5. Execute Cohere agent
6. Execute MCP tool(s)
7. Persist assistant message
8. Return response
9. Forget everything (stateless)

### 11. Error Handling Constitution

The system SHALL:
- Never crash on invalid input
- Gracefully handle missing tasks
- Respond politely to user mistakes
- Return structured error messages
- Handle Cohere API errors gracefully

### 12. Development Workflow

#### 12.1 Step-by-Step Process
1. **Spec Writing/Updating**: Review requirements and update /specs files for AI Chatbot features
2. **Generate Plan**: Prompt Claude Code with "@specs/features/[feature].md generate AI Chatbot implementation plan"
3. **Task Implementation**: For each task, prompt Claude Code with specific AI Chatbot components
4. **Integration and Testing**: Test ChatKit UI, Cohere API integration, MCP tools
5. **Deployment Prep**: Configure environment variables (COHERE_API_KEY, BETTER_AUTH_SECRET, DATABASE_URL)
6. **Review and Merge**: Ensure all features meet acceptance criteria

### 13. Project Structure (AI Chatbot Focused)

```
/frontend          # Next.js with ChatKit SDK
  /app             # App Router pages
  /components      # ChatKit UI components
  /lib             # API clients, Cohere integration

/backend           # FastAPI with Cohere + MCP
  /src
    /api           # Chat endpoint, MCP server
    /models        # SQLModel models
    /services      # Cohere integration service
    /mcp           # MCP tool implementations

/specs             # AI Chatbot specifications
  /ai-chatbot      # ChatKit, Cohere, MCP specs
  /features        # Feature progression specs

/.specify          # SpecKit Plus templates
/history           # Prompt History Records, ADRs
```

### 14. Technology Stack

| Layer | Technology | Constraint |
|-------|------------|------------|
| Frontend | Next.js 16+ (App Router) with Official ChatKit SDK | Must use ChatKit SDK |
| Backend | Python FastAPI | Stateless design |
| AI Provider | Cohere API | ONLY allowed API key |
| MCP Layer | Official MCP SDK | Required for tool layer |
| ORM | SQLModel | |
| Database | Neon Serverless PostgreSQL | |
| Authentication | Better Auth (JWT tokens) | |
| Spec-Driven | Claude Code + Spec-Kit Plus | |

### 15. Feature Progression

#### Basic Level (Core Essentials):
1. Add Task – AI creates new todo items via MCP tools
2. Delete Task – AI removes tasks from the list via MCP tools
3. Update Task – AI modifies existing task details via MCP tools
4. View Task List – AI retrieves and displays tasks via MCP tools
5. Mark as Complete – AI toggles task completion status via MCP tools

#### Intermediate Level (Organization & Usability):
1. Priorities & Tags/Categories – AI assigns levels or labels via MCP tools
2. Search & Filter – AI searches by keyword; filters by status, priority, or date
3. Sort Tasks – AI reorders tasks by due date, priority, or alphabetically

#### Advanced Level (Intelligent Features):
1. Recurring Tasks – AI auto-reschedules repeating tasks via MCP tools
2. Due Dates & Time Reminders – AI sets deadlines with notifications

### 16. MCP Tools Specification

The MCP server must expose the following tools for the AI agent:

#### Tool: add_task
| Attribute | Value |
|-----------|-------|
| Purpose | Create a new task |
| Parameters | user_id (string, required), title (string, required), description (string, optional) |
| Returns | task_id, status, title |

#### Tool: list_tasks
| Attribute | Value |
|-----------|-------|
| Purpose | Retrieve tasks from the list |
| Parameters | user_id (string, required), status (string, optional: "all", "pending", "completed") |
| Returns | Array of task objects |

#### Tool: complete_task
| Attribute | Value |
|-----------|-------|
| Purpose | Mark a task as complete |
| Parameters | user_id (string, required), task_id (integer, required) |
| Returns | task_id, status, title |

#### Tool: delete_task
| Attribute | Value |
|-----------|-------|
| Purpose | Remove a task from the list |
| Parameters | user_id (string, required), task_id (integer, required) |
| Returns | task_id, status, title |

#### Tool: update_task
| Attribute | Value |
|-----------|-------|
| Purpose | Modify task title or description |
| Parameters | user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional) |
| Returns | task_id, status, title |

### 17. Chat API Endpoint

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

### 18. Agent Behavior Specification

| Behavior | Description |
|----------|-------------|
| Task Creation | When user mentions adding/creating/remembering something, use add_task |
| Task Listing | When user asks to see/show/list tasks, use list_tasks with appropriate filter |
| Task Completion | When user says done/complete/finished, use complete_task |
| Task Deletion | When user says delete/remove/cancel, use delete_task |
| Task Update | When user says change/update/rename, use update_task |
| Confirmation | Always confirm actions with friendly response |
| Error Handling | Gracefully handle task not found and other errors |

### 19. Natural Language Command Examples

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

### 20. How to Create Specs

#### 20.1 Specification Philosophy
Specs define what, never how. Each spec answers:
- Purpose
- Inputs
- Outputs
- Constraints
- Behavior rules

#### 20.2 Required Spec Files
```
/specs
 ├─ ai-chatbot/
 │   ├─ agent.spec.md          # Cohere agent behavior
 │   ├─ mcp-tools.spec.md      # MCP tool definitions
 │   ├─ chat-api.spec.md       # Chat endpoint API
 │   └─ voice-input.spec.md    # Voice input handling
 ├─ features/
 │   ├─ basic-crud.spec.md     # Basic AI task management
 │   ├─ intermediate-org.spec.md # Organization features
 │   └─ advanced-intel.spec.md # Intelligent features
 └─ database/
     └─ schema.spec.md         # Database models
```

### 21. How to Create the Plan (From Specs)

#### 21.1 Planning Rules
A plan is derived only after specs are frozen. Plan MUST:
- Be sequential
- Be tool-driven
- Avoid implementation details

#### 21.2 Example Plan Structure
1. Initialize database schema for AI Chatbot
2. Implement MCP tools for Cohere integration
3. Configure Cohere API agent
4. Build stateless chat endpoint
5. Integrate ChatKit frontend
6. Add voice input support
7. Test conversation persistence

### 22. Task Breakdown Rules

Each plan step is broken into:
- Atomic
- Testable
- Reversible tasks

Example:
Task: Implement add_task MCP tool for Cohere integration
- Define input schema
- Validate user_id
- Persist task via SQLModel
- Return structured output for Cohere agent

### 23. Claude Code Execution Rule

Claude Code SHALL:
- Read AI Chatbot specs
- Follow the AI-focused plan
- Implement tasks with Cohere constraint
- Never introduce logic not defined in specs
- Iterate only through spec updates

### 24. Constraints

- Word Count Limit: This constitution is under 2500 words
- No Manual Coding: All code via Claude Code prompts
- Feature Phasing: Implement Basic → Intermediate → Advanced
- Cohere-Only: Use ONLY Cohere API key for AI functionality
- Testing: Unit (Pytest/Jest), Integration (API calls), E2E (conversation flows)
- Dependencies: Minimal; no extra installs beyond stack
- Scalability: Design for 1000+ users; use indexing in DB

### 25. Success Criteria

- Functionality: All AI Chatbot features work per specs; auth enforces isolation
- UI/UX: ChatKit interface works smoothly, voice input functional
- Cohere Integration: System works exclusively with Cohere API
- Performance: Stateless design handles concurrent conversations

### 26. Final Authority

This constitution overrides:
- README assumptions
- Inline comments
- Developer preferences

If behavior is not specified here → it is out of scope.

### 27. Evaluation Readiness

This constitution ensures:
- Clean separation of concerns
- Proper use of official ChatKit SDK
- Exclusive Cohere API integration
- Full compliance with Phase III objectives
- Transparent, judge-reviewable workflow

**Version**: 3.0.0 | **Ratified**: 2026-01-11 | **Last Amended**: 2026-02-03

# Phase IV: Local Kubernetes Deployment Constitution

## Core Principles (Kubernetes Deployment)

### AI-Native DevOps
All DevOps operations must be driven by AI agents (Gordon, kubectl-ai, kagent) rather than manual configuration. Kubernetes manifests, Helm charts, and deployment operations must be generated and managed through AI-assisted tools, following the Agentic Dev Stack Workflow: Spec → Plan → Tasks → Implement via AI agents.

### Containerization-First Approach
Applications must be containerized using Docker AI Agent (Gordon) with AI-generated Dockerfiles for both frontend and backend services. No manual Dockerfile creation is allowed. Containers must follow best practices for security, efficiency, and portability.

### Infrastructure-as-Code with AI Assistance
All infrastructure provisioning must be done through AI-generated Helm charts and Kubernetes manifests. Infrastructure changes must be version-controlled and managed through AI-assisted operations using kubectl-ai and kagent for deployment, scaling, and monitoring.

### Local Kubernetes Focus
Deployments must be targeted specifically to Minikube (local Kubernetes cluster) with AI-assisted orchestration. No cloud provider deployments (AWS/GCP/Azure) are allowed during this phase. Focus on local reproducible setups using Helm Charts and Minikube.

## Phase IV – Local Kubernetes Deployment Requirements

### 1. Purpose of This Addition
This section defines the binding rules, architecture, and specifications for deploying the Phase III Todo AI Chatbot on a **local Kubernetes cluster** using **Minikube** and **Helm Charts**, while enforcing an **AI-native, agent-driven DevOps workflow**.

Technology Stack for Deployment:
- Containerization: Docker Desktop with Gordon (Docker AI Agent)
- Orchestration: Kubernetes (Minikube)
- Package Manager: Helm Charts
- AI DevOps Tools: kubectl-ai, kagent
- Application: Phase III Todo AI Chatbot

### 2. Agentic Dev Stack Workflow for Kubernetes (Mandatory)
All deployment activities must strictly follow the workflow below:
1. Write Kubernetes Deployment Specifications
2. Generate an Execution Plan for Kubernetes
3. Break Plan into Atomic Kubernetes Tasks
4. Implement via AI agents (Claude Code, Gordon, kubectl-ai, kagent)
5. Iterate Using Specs (No Manual YAML/Dockerfile Authoring)

Manual authoring of Dockerfiles, Kubernetes YAML, or Helm templates is **not allowed**. AI generation + iteration is required.

### 3. System Objectives for Kubernetes Deployment
The deployment system SHALL:
- Containerize frontend and backend using Docker AI Agent (Gordon)
- Generate Helm charts using kubectl-ai and/or kagent
- Operate Kubernetes using AI-assisted tools (kubectl-ai, kagent)
- Deploy and validate on Minikube (local Kubernetes cluster)
- Demonstrate AI-native DevOps workflow with reproducible results

### 4. Kubernetes Architecture Constitution

#### 4.1 High-Level Kubernetes Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Docker AI   │    │  AI DevOps Ops   │    │  Minikube     │
│   (Gordon)    │    │ (kubectl-ai,     │    │  (Local K8s)  │
│               │    │  kagent)         │    │               │
│  ┌─────────┐  │    │  ┌─────────────┐ │    │  ┌─────────┐  │
│  │Frontend │  │    │  │Helm Charts  │ │    │  │Frontend │  │
│  │Image    │  │───▶│  │(AI-Gen)     │ │───▶│  │Pod      │  │
│  └─────────┘  │    │  └─────────────┘ │    │  └─────────┘  │
│               │    │                  │    │               │
│  ┌─────────┐  │    │  ┌─────────────┐ │    │  ┌─────────┐  │
│  │Backend  │  │    │  │K8s Manifests│ │    │  │Backend  │  │
│  │Image    │  │───▶│  │(AI-Gen)     │ │───▶│  │Pod      │  │
│  └─────────┘  │    │  └─────────────┘ │    │  └─────────┘  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

#### 4.2 Constitutional Constraints for Kubernetes
- No manual Dockerfile authoring (use Gordon only)
- No manual Kubernetes YAML creation (use kubectl-ai/kagent)
- No manual Helm chart creation (use kubectl-ai/kagent)
- No cloud provider deployments (local Minikube only)
- All operations must be AI-assisted
- Deployment must be reproducible via documented commands

### 5. Containerization Constitution (Docker AI - Gordon)

#### 5.1 Docker AI Requirements
The Docker AI Agent (Gordon) SHALL:
- Generate Dockerfiles for Next.js frontend service
- Generate Dockerfiles for FastAPI backend service
- Follow security best practices (non-root users, minimal base images)
- Optimize for size and build time
- Include proper environment variable handling

#### 5.2 Container Images
- Frontend Image: todo-frontend
- Backend Image: todo-backend
- Images must be compatible with Kubernetes deployment
- Include proper health checks and startup sequences

### 6. Helm Chart Constitution (AI-Generated)

#### 6.1 AI-Generated Helm Charts
Helm charts MUST be generated via **kubectl-ai** and/or **kagent** with:
- Deployment resources for frontend and backend
- Service resources for network connectivity
- Proper image references and tags
- Configurable replica counts
- Resource limits and requests
- Environment variable configurations

#### 6.2 Chart Requirements
Charts SHALL include:
- Proper namespace management
- Configurable image pull policies
- Health check configurations
- Resource scaling specifications
- Service exposure via LoadBalancer or NodePort

### 7. Kubernetes Operations Constitution (AI-Assisted)

#### 7.1 kubectl-ai Operations
The kubectl-ai tool SHALL be used for:
- Deploying applications to Minikube
- Scaling deployments
- Troubleshooting pod failures
- Monitoring resource usage
- Managing services and ingress

#### 7.2 kagent Operations
The kagent tool SHALL be used for:
- Cluster health analysis
- Resource optimization recommendations
- Performance monitoring
- Anomaly detection in deployments

### 8. Minikube Constitution (Local Kubernetes)

#### 8.1 Minikube Setup Requirements
Minikube SHALL:
- Run locally on development machine
- Support Docker driver
- Have sufficient resources allocated (CPU/RAM)
- Support Helm chart installations
- Allow service exposure via minikube service command

#### 8.2 Local Deployment Constraints
Deployments SHALL:
- Target only local Minikube cluster
- Not require external cloud resources
- Be fully contained within local environment
- Support reproducible setup via scripts
- Allow easy cleanup and reset

### 9. Development Workflow for Kubernetes

#### 9.1 Kubernetes Deployment Process
1. **Environment Setup**: Install Docker Desktop (with Gordon), Minikube, kubectl, Helm, kubectl-ai, kagent
2. **Containerization**: Use Gordon to generate Dockerfiles and build images
3. **Chart Generation**: Use kubectl-ai/kagent to generate Helm charts
4. **Deployment**: Use Helm to install charts on Minikube
5. **Validation**: Verify deployments using AI-assisted tools
6. **Access**: Expose services via minikube service command

#### 9.2 AI-Assisted Operations Examples
```
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "scale the backend to handle more load"
kubectl-ai "check why the pods are failing"
kagent "analyze the cluster health"
kagent "optimize resource allocation"
```

### 10. Project Structure for Kubernetes Deployment

```
/deployment                    # Kubernetes deployment artifacts
  /docker                      # Docker-related configs (AI-generated)
    /frontend                  # Frontend Dockerfile (Gordon-generated)
    /backend                   # Backend Dockerfile (Gordon-generated)
  /kubernetes                  # Kubernetes manifests (AI-generated)
    /helm-charts               # Helm charts (kubectl-ai/kagent-generated)
      /todo-frontend           # Frontend Helm chart
      /todo-backend            # Backend Helm chart
  /scripts                     # Deployment scripts (AI-assisted)
    /setup-minikube.sh         # Minikube setup script
    /deploy-all.sh             # Full deployment script
    /validate-deployment.sh    # Validation script
```

### 11. Technology Stack for Deployment

| Component        | Technology               | Constraint |
|------------------|--------------------------|------------|
| Containerization | Docker Desktop           | Gordon-enabled |
| Docker AI        | Docker AI Agent (Gordon) | No manual Dockerfiles |
| Orchestration    | Kubernetes (Minikube)    | Local cluster only |
| Package Manager  | Helm Charts              | AI-generated only |
| AI DevOps        | kubectl-ai, kagent       | AI-assisted ops |
| Application      | Phase III Todo Chatbot   | Deploy as containers |

### 12. Environment & Tooling Requirements (Windows)

#### 12.1 Package Manager
- **Chocolatey** for deterministic installs

#### 12.2 Required Installations
- Docker Desktop v4.53+ (Gordon enabled)
- Minikube
- kubectl
- Helm
- kubectl-ai
- kagent (optional but recommended)

#### 12.3 Installation Commands (AI-Assisted Verification)
```
docker --version
kubectl version --client
helm version
minikube version
kubectl-ai "hello"
kagent "analyze cluster health"
```

### 13. Kubernetes Deployment Validation

#### 13.1 Deployment Verification Steps
1. Verify Minikube is running
2. Verify Helm charts are properly generated
3. Verify successful deployment of frontend and backend
4. Verify service connectivity and accessibility
5. Verify application functionality

#### 13.2 Success Criteria for Deployment
- Frontend & backend running on Minikube
- Helm-based deployments verified
- Demonstrated use of Gordon, kubectl-ai, and kagent
- Reproducible setup via documented commands
- Clear proof of AI-native DevOps workflow

### 14. Evidence & Documentation Requirements

#### 14.1 Required Documentation
- AI prompts and outputs (Docker, Helm, kubectl)
- Screenshots/logs of deployments and scaling
- Issues encountered + AI-driven fixes
- Performance metrics and optimization results

#### 14.2 Submission Requirements
- Complete deployment logs
- Performance benchmarks
- AI interaction transcripts
- Final validation results

### 15. Constraints for Phase IV

- No cloud providers (AWS/GCP/Azure)
- No manual YAML/Dockerfile authoring
- Local execution only (Minikube)
- AI-assisted operations mandatory
- Reproducible setup required

### 16. Success Criteria for Kubernetes Deployment

- Docker images built successfully using Gordon
- Helm charts generated and deployed using AI tools
- Frontend and backend running on Minikube
- Services accessible and functional
- AI-native DevOps workflow demonstrated
- Reproducible deployment process documented
- Performance and resource utilization optimized

### 17. Governance for Kubernetes Deployment

All Kubernetes deployment activities must adhere to the AI-Native DevOps workflow. Changes to deployment configurations must be AI-assisted and properly documented. All deployments must follow the defined architecture and technology stack. Code reviews must verify compliance with all Kubernetes deployment principles and standards defined in this constitution.