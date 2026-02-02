# Phase 0: Research & Architecture Decisions

**Feature**: Chat API, Voice Input & UI Navigation
**Branch**: 001-chat-voice-ui
**Status**: Completed

## 1. Technical Context & Constraints

The project constitution and feature specification establish strict constraints:
- **Frontend**: Next.js 16+ with **Official ChatKit SDK**.
- **Backend**: Python FastAPI.
- **AI Agent**: Cohere API (via environment variable only).
- **Tooling**: **Official MCP SDK** (Model Context Protocol).
- **Persistence**: Neon PostgreSQL via SQLModel.
- **Architecture**: Stateless server; agent state is transient; task and conversation state is persistent.

## 2. Decision Record

### Decision 1: Web Speech API Implementation
- **Requirements**: Implement voice input using Browser Web Speech API.
- **Decision**: Use the `webkitSpeechRecognition` API (available in Chrome/Edge) and standard `SpeechRecognition` for other browsers.
- **Verification**: The Web Speech API is supported in modern browsers (Chrome, Edge, Safari) but not Firefox. We'll implement graceful fallback to text input for unsupported browsers.
- **Constraint Check**: Satisfies "Browser Web Speech API" requirement from spec.

### Decision 2: Real-time UI Updates
- **Requirements**: Task updates made via AI Chat must reflect immediately in Tasks page and Dashboard without page refresh.
- **Decision**: Use React state management combined with event emitters to update related components when tasks change. Since the frontend already uses Next.js with React, we can leverage React's state management and potentially React Query/SWR for real-time updates.
- **Alternative Considered**: WebSockets for real-time updates, but this adds complexity for a simple use case.
- **Chosen Approach**: Propagate state changes from the chat component to parent components using callbacks or a state management solution.

### Decision 3: ChatKit UI Integration
- **Requirements**: Use Official ChatKit SDK for the UI.
- **Decision**: Integrate ChatKit components for message display and input handling. The ChatKit SDK will handle message threading, typing indicators, and other UI elements.
- **Data Flow**: `ChatKit UI -> POST /api/{user_id}/chat -> Backend (Cohere + MCP) -> DB`.
- **Statelessness**: The backend will reconstruct the conversation history from the DB for every request before passing it to the Cohere agent.

### Decision 4: Navigation Integration
- **Requirements**: Add AI Chat access to existing navigation (navbar and sidebar).
- **Decision**: Add "AI Chat" link to the existing navbar and sidebar components following the same styling patterns as other navigation items.
- **Implementation**: Update `Navbar.tsx` and `Sidebar.tsx` to include the new route.

## 3. Technology Stack Confirmation

| Component | Choice | Reason |
|-----------|--------|--------|
| Voice Input | Web Speech API | Browser-native, meets requirement |
| Chat UI | ChatKit SDK | Mandated by User |
| AI Logic | Cohere API | Mandated by User |
| Tool Protocol | MCP (Official SDK) | Mandated by User |
| DB | Neon (SQLModel) | Existing Stack |

## 4. Unknowns Resolved

- **Clarification**: "How does real-time update work across components?"
  - **Resolution**: Updates happen at the database level. When the AI agent modifies tasks via MCP tools, the changes are persisted immediately. The UI components can listen for changes or refresh data when navigating between views.

- **Clarification**: "How to handle unsupported languages in voice recognition?"
  - **Resolution**: The Web Speech API supports multiple languages. For en-US and ur-PK, we'll configure the recognition appropriately. For unsupported languages, the system will fall back to text input with an appropriate message to the user.

## 5. Security & Validation

- **User Isolation**: Every chat request is protected by Better Auth. The `user_id` is extracted from the verified session/token and passed securely to the agent/tools. The Agent cannot "invent" a user_id.
- **Voice Input Security**: Only converts speech to text on the client side; no audio is sent to the server.

## 6. Browser Compatibility

- **Web Speech API Support**: Available in Chrome, Edge, Safari but limited in Firefox
- **Fallback Strategy**: Graceful degradation to text input for browsers without Web Speech API support

## 7. Conclusion

The architecture is viable and tightly constrained. We proceed to Data Model design with confidence that the voice input, chat API, and navigation integration can be implemented within the specified constraints.