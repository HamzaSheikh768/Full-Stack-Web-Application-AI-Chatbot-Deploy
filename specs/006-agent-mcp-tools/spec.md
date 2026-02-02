# Feature Specification: Agent & MCP Tools for Todo AI Chatbot

**Feature Branch**: `006-agent-mcp-tools`
**Created**: 2026-01-23
**Status**: Draft
**Input**: User description: "Agent & MCP Tools Specification – Todo AI Chatbot"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE.
-->

### User Story 1 - Natural Language Task Management (Priority: P1)

Users can manage their tasks (add, list, update, delete, complete) using natural language commands either via text or voice. The AI agent interprets the intent and executes the appropriate MCP tool.

**Why this priority**: Core functionality of the AI Chatbot. Without this, the system is just a standard web app.

**Independent Test**: Send commands like "Add buy milk", "Show tasks", "Complete buy milk" and veirfy tasks are modified in DB only via MCP tool calls.

**Acceptance Scenarios**:

1. **Given** user says "I need to buy milk", **When** processed by agent, **Then** `add_task` tool is called with title "Buy milk" and returns success.
2. **Given** user says "Show my tasks", **When** processed by agent, **Then** `list_tasks` tool is called and agent summarizes the results.
3. **Given** user says "Delete task 5", **When** processed by agent, **Then** `delete_task` tool is called with ID 5.
4. **Given** user says "Mark task 1 as done", **When** processed by agent, **Then** `complete_task` tool is called with ID 1.

---

### User Story 2 - Helpful AI Assistant Persona (Priority: P2)

The AI agent acts as a helpful assistant, confirming actions, maintaining context, and handling errors gracefully without exposing technical details.

**Why this priority**: Essential for user experience (UX). Ensures the interaction feels like a conversation, not a CLI.

**Independent Test**: Verify agent responses are friendly ("I've added that for you") vs robotic ("Task 123 created"). Test undefined inputs.

**Acceptance Scenarios**:

1. **Given** a successful tool execution, **When** agent responds, **Then** it uses friendly confirmation language (e.g., "Sure, I've added 'Buy milk' to your list.").
2. **Given** a tool failure (e.g., ID not found), **When** agent responds, **Then** it apologizes and suggests corrective action (e.g., "I couldn't find task 5. Did you mean task 3?").
3. **Given** an ambiguous request, **When** agent responds, **Then** it asks for clarification instead of guessing or failing.

---

### Edge Cases

- **Task Not Found**: User asks to delete/update a task ID that doesn't exist. Agent should check `list_tasks` or handle the 404 error from the tool gracefully.
- **Ambiguous Intent**: User says "Update the task" without specifying which one. Agent should ask clarifying questions (e.g., "Which task would you like to update?").
- **Permission Denial**: User tries to access tasks belonging to another user_id. Tools must assume the `user_id` context is enforced boundaries.
- **Empty List**: User asks to list tasks but has none. Agent should respond encouragingly (e.g., "You have no tasks. Would you like to add one?").
- **Cohere API Outage**: If the LLM service fails, the system should return a standard error message to the frontend.

## Requirements *(mandatory)*

### Functional Requirements

**Agent Framework**
- **FR-001**: System MUST use OpenAI Agents SDK for the agent abstraction.
- **FR-002**: System MUST use Cohere as the LLM Provider.
- **FR-003**: System MUST NOT use any other LLM provider (OpenAI, Anthropic, etc.).
- **FR-004**: API Keys MUST be loaded from environment variables (`COHERE_API_KEY`) and never hardcoded.

**Agent Responsibilities**
- **FR-005**: Agent MUST interpret user natural language (text or voice input converted to text).
- **FR-006**: Agent MUST invoke MCP tools for ALL task operations (CRUD).
- **FR-007**: Agent MUST generate friendly, conversational confirmations.
- **FR-008**: Agent MUST NEVER access the database directly; it must go through MCP tools.

**Prohibited Behavior**
- **FR-009**: Agent MUST NOT perform CRUD logic internally (in-memory or non-MCP logic).
- **FR-010**: Agent MUST NOT bypass MCP tools for data persistence.
- **FR-011**: Agent MUST NOT store conversation state in memory between requests (Stateless).

**MCP Tools Specification**
- **FR-012**: System MUST implement `add_task` tool:
  - Input: `user_id` (string), `title` (string), `description` (optional string)
  - Output: `task_id`, `status`, `title`
- **FR-013**: System MUST implement `list_tasks` tool:
  - Input: `user_id` (string), `status` (optional: "all", "pending", "completed")
  - Output: Array of task objects
- **FR-014**: System MUST implement `complete_task` tool:
  - Input: `user_id` (string), `task_id` (integer)
  - Output: `task_id`, `status`, `title`
- **FR-015**: System MUST implement `delete_task` tool:
  - Input: `user_id` (string), `task_id` (integer)
  - Output: `task_id`, `status`, `title`
- **FR-016**: System MUST implement `update_task` tool:
  - Input: `user_id` (string), `task_id` (integer), `title` (optional), `description` (optional)
  - Output: `task_id`, `status`, `title`

**Tool-Level Logic**
- **FR-017**: All MCP tools MUST validate `user_id` ownership (User A cannot touch User B's tasks).
- **FR-018**: All MCP tools MUST be stateless and persist changes to SQLModel/Neon DB immediately.
- **FR-019**: All MCP tools MUST return structured JSON.

**Error Handling**
- **FR-020**: Agent MUST apologize on tool failure.
- **FR-021**: Agent MUST suggest corrective actions when tools return errors (e.g. "Task not found").

### Key Entities *(include if feature involves data)*

- **Task**: The unit of work managed by MCP tools (id, title, status, user_id).
- **Conversation**: The stateless interaction context passed to the agent.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of task operations (Create, Read, Update, Delete) are performed via MCP tools.
- **SC-002**: Agent successfully interprets >90% of standard natural language intents for CRUD operations.
- **SC-003**: System solely uses Cohere API for intelligence; zero usage of OpenAI/Anthropic APIs for inference.
- **SC-004**: All tool schemas match the specification exactly (parameters and return types).
