# Feature Specification: Chat API, Voice Input & UI Navigation

**Feature Branch**: `001-chat-voice-ui`
**Created**: 2026-01-23
**Status**: Draft
**Input**: User description: "now used Official Chatkit SDK frontend Typescript backend python + fastapi  only /specs/chat-voice-ui.spec.md
# Chat API, Voice Input & UI Navigation Specification

## Chat API

### Endpoint
POST /api/{user_id}/chat

### Request
- conversation_id (optional)
- message (required)

### Server Rules
1. Fetch conversation history
2. Store user message
3. Run agent with MCP tools
4. Store assistant message
5. Return response (conversation_id, response, tool_calls)
6. Stateless – no memory in server

---

## Voice Input

- Input Source: Browser Web Speech API
- Flow:
  1. User clicks mic button
  2. Speech → Text on client
  3. Send text to Chat API
- Constraints:
  - Input only, no audio sent to server
  - Same pipeline as text
- Supported Languages: en-US, ur-PK

---

## UI Navigation

### Navbar
- \"AI Chat\" button visible on all authenticated pages
- Opens AI Chat page

### Sidebar
- Dashboard
- Tasks
- AI Chat

### AI Chat Page
- ChatKit UI
- Display conversation history
- Support text and voice input
- Show tool execution confirmations

### Tool Output Visibility
- Reflect updates in Tasks page
- Update Dashboard metrics
- Persist in database

### UX Rules
- AI Chat does not block navigation
- Task updates appear without page refresh"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Voice-Enabled Task Management (Priority: P1)

User can speak their task commands using the microphone button, and the AI assistant processes the voice input and performs the requested actions (adding tasks, updating tasks, etc.).

**Why this priority**: Critical for accessibility and hands-free task management. Provides alternative input method to text.

**Independent Test**: User clicks microphone, speaks "Add a task to buy groceries", AI assistant confirms task creation without page refresh.

**Acceptance Scenarios**:

1. **Given** user is on AI Chat page with microphone available, **When** user clicks mic and says "Add a task to buy groceries", **Then** speech is converted to text and sent to chat API, task is created and reflected in Tasks page.
2. **Given** user has existing tasks, **When** user says "Mark task 1 as complete", **Then** AI assistant marks task as complete and updates Dashboard metrics immediately.

---

### User Story 2 - Seamless Navigation Between Features (Priority: P2)

User can access the AI Chat feature from any authenticated page via the Navbar AI Chat button, and can navigate between Dashboard, Tasks, and AI Chat through the sidebar.

**Why this priority**: Critical for user experience to maintain context and allow easy switching between different parts of the application.

**Independent Test**: User can click AI Chat button in navbar from any page and land on AI Chat page, then use sidebar to navigate to other sections.

**Acceptance Scenarios**:

1. **Given** user is on Dashboard page, **When** user clicks "AI Chat" in navbar, **Then** user lands on AI Chat page with conversation history displayed.
2. **Given** user is on AI Chat page, **When** user clicks "Tasks" in sidebar, **Then** user lands on Tasks page showing all tasks including those created via AI Chat.

---

### User Story 3 - Real-Time Task Updates (Priority: P3)

When the AI assistant creates, updates, or deletes tasks, these changes are immediately visible in the Tasks page and Dashboard without requiring a page refresh.

**Why this priority**: Enhances user experience by providing immediate feedback and maintaining consistency across the application.

**Independent Test**: User performs task operation via AI Chat, and sees the update reflected in Tasks page without refreshing.

**Acceptance Scenarios**:

1. **Given** user has tasks displayed on Tasks page, **When** user adds a task via AI Chat, **Then** new task appears in Tasks page without page refresh.
2. **Given** user has tasks with completion status, **When** user completes a task via AI Chat, **Then** Dashboard metrics update immediately to reflect new completion status.

---

### Edge Cases

- What happens when voice recognition fails to understand user input? The system should prompt for clarification.
- How does system handle multiple simultaneous voice inputs? Only one voice input should be processed at a time.
- What happens when user navigates away during voice input processing? The input should still be processed and results available when user returns.
- How does system handle unsupported languages? System should fall back to text input or display language support message.

## Requirements *(mandatory)*

### Functional Requirements

**Chat API**
- **FR-001**: System MUST provide endpoint `POST /api/{user_id}/chat` for processing user messages.
- **FR-002**: System MUST accept optional `conversation_id` and required `message` in request body.
- **FR-003**: System MUST fetch conversation history from database before processing new message.
- **FR-004**: System MUST store user message in database before processing.
- **FR-005**: System MUST run agent with MCP tools to process the message.
- **FR-006**: System MUST store assistant response in database after processing.
- **FR-007**: System MUST return response with `conversation_id`, `response`, and `tool_calls`.

**Voice Input Processing**
- **FR-008**: System MUST use Browser Web Speech API for voice recognition.
- **FR-009**: System MUST convert speech to text on the client side before sending to server.
- **FR-010**: System MUST support voice input in en-US and ur-PK languages.
- **FR-011**: System MUST route voice-converted text through the same pipeline as text input.

**UI Navigation**
- **FR-012**: System MUST display "AI Chat" button in navbar on all authenticated pages.
- **FR-013**: System MUST include "AI Chat" option in sidebar navigation alongside Dashboard and Tasks.
- **FR-014**: System MUST provide ChatKit UI on AI Chat page displaying conversation history.
- **FR-015**: System MUST support both text and voice input on AI Chat page.
- **FR-016**: System MUST show tool execution confirmations in the chat interface.

**Real-Time Updates**
- **FR-017**: System MUST update Tasks page when AI assistant creates/updates/deletes tasks.
- **FR-018**: System MUST update Dashboard metrics when task statuses change via AI assistant.
- **FR-019**: System MUST persist all changes in database immediately after AI processing.

**Stateless Operation**
- **FR-020**: System MUST NOT store conversation state in server memory between requests.
- **FR-021**: System MUST fetch complete conversation history from database for each request.

### Key Entities

- **Conversation**: Represents a chat session between user and AI assistant (id, user_id, created_at, updated_at)
- **Message**: Individual chat message (id, conversation_id, role, content, created_at)
- **Task**: User task managed by the system (id, user_id, title, description, completed, created_at, updated_at)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully use voice input to create tasks in at least 90% of attempts with clear speech.
- **SC-002**: Task updates made via AI Chat are reflected in Tasks page within 2 seconds without page refresh.
- **SC-003**: AI Chat page loads and displays conversation history in under 3 seconds.
- **SC-004**: Users can navigate between AI Chat, Dashboard, and Tasks pages without losing context or conversation state.
- **SC-005**: Voice input functionality works in supported browsers (Chrome, Firefox, Safari) with Web Speech API support.
