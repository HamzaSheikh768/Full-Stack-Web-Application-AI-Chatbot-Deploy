# Implementation Tasks: Agent & MCP Tools for Todo AI Chatbot

**Branch**: `006-agent-mcp-tools`
**Feature**: Agent & MCP Tools for Todo AI Chatbot
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Phase 1: Setup & Project Initialization
**Goal**: Prepare the development environment and project structure for AI Chatbot implementation.

- [x] T001 [P] Set up backend directory structure for chat features in `backend/src/`
- [x] T002 [P] Set up frontend directory structure for chat features in `frontend/src/`
- [x] T003 [P] Install required dependencies for ChatKit SDK and Cohere in `frontend/package.json`
- [x] T004 [P] Install required dependencies for FastAPI, SQLModel, OpenAI/MCP in `backend/requirements.txt`
- [x] T005 Create environment variable documentation for `COHERE_API_KEY` in `.env`

## Phase 2: Foundational Components (Blocking)
**Goal**: Implement core models, database setup, and MCP tools required by all user stories.

- [x] T006 [P] Verify/Update `Task` model in `backend/src/models/task.py` to match data-model.md
- [x] T007 [P] Create `Conversation` and `Message` models in `backend/src/models/conversation.py`
- [x] T008 [P] Create database migration for new conversation/message tables
- [x] T009 [P] Implement MCP tools for task management in `backend/src/mcp/tools.py`
- [x] T010 [P] Create MCP tool handlers in `backend/src/mcp/handlers.py`
- [x] T011 [P] Set up MCP server configuration in `backend/src/mcp/server.py`
- [x] T012 Create Cohere agent configuration in `backend/src/agent/core.py`
- [x] T013 Implement stateless agent runner in `backend/src/agent/runner.py`

## Phase 3: User Story 1 - Voice-Enabled Task Management (Priority: P1)
**Goal**: Enable users to manage tasks via voice commands using Web Speech API.
**Test**: User clicks microphone, speaks "Add a task to buy groceries", AI assistant confirms task creation without page refresh.

- [x] T014 [US1] Implement voice input widget component in `frontend/src/components/VoiceInputWidget.tsx`
- [x] T015 [US1] Integrate Web Speech API for voice recognition in `frontend/src/lib/voice-recognition.ts`
- [x] T016 [US1] Implement add_task MCP tool in `backend/src/mcp/handlers.py`
- [x] T017 [US1] Create chat endpoint POST /api/{user_id}/chat in `backend/src/api/chat_routes.py`
- [x] T018 [US1] Implement chat history persistence in `backend/src/services/chat_service.py`
- [x] T019 [US1] Create ChatWidget component with ChatKit in `frontend/src/components/ChatWidget.tsx`
- [x] T020 [US1] Connect voice input to chat API in `frontend/src/components/ChatWidget.tsx`
- [x] T021 [US1] Test voice-enabled task creation flow

## Phase 4: User Story 2 - Seamless Navigation Between Features (Priority: P2)
**Goal**: Allow users to access AI Chat from any page via navbar and navigate between features via sidebar.
**Test**: User clicks AI Chat button in navbar from Dashboard and lands on AI Chat page with conversation history.

- [x] T022 [US2] Add AI Chat button to Navbar component in `frontend/src/components/navigation/Navbar.tsx`
- [x] T023 [US2] Add AI Chat link to navigation in `frontend/src/components/ui/mobile-nav.tsx`
- [x] T024 [US2] Create AI Chat page in `frontend/src/app/chat/page.tsx`
- [x] T025 [US2] Implement conversation history loading in `frontend/src/components/ChatWidget.tsx`
- [x] T026 [US2] Create QuickChatWidget for floating access in `frontend/src/components/QuickChatWidget.tsx`
- [x] T027 [US2] Test navigation between Dashboard, Tasks, and AI Chat pages

## Phase 5: User Story 3 - Real-Time Task Updates (Priority: P3)
**Goal**: Ensure task changes made via AI Chat are immediately visible in Tasks page and Dashboard.
**Test**: User adds task via AI Chat, and new task appears in Tasks page without page refresh.

- [x] T028 [US3] Implement list_tasks MCP tool in `backend/src/mcp/handlers.py`
- [x] T029 [US3] Implement complete_task MCP tool in `backend/src/mcp/handlers.py`
- [x] T030 [US3] Implement delete_task MCP tool in `backend/src/mcp/handlers.py`
- [x] T031 [US3] Implement update_task MCP tool in `backend/src/mcp/handlers.py`
- [x] T032 [US3] Create TaskUpdateNotificationWidget in `frontend/src/components/TaskUpdateNotificationWidget.tsx`
- [x] T033 [US3] Implement real-time updates in TaskList component in `frontend/src/components/TaskList.tsx`
- [x] T034 [US3] Test real-time task updates across UI components

## Phase 6: Polish & Cross-Cutting Concerns
**Goal**: Final integration, testing, and documentation.

- [x] T035 Add error handling for MCP tool failures in `backend/src/mcp/handlers.py`
- [x] T036 Implement voice input fallback for unsupported browsers in `frontend/src/lib/voice-recognition.ts`
- [x] T037 Add loading states and user feedback in `frontend/src/components/ChatWidget.tsx`
- [x] T038 Write integration tests for chat API in `backend/tests/test_chat_api.py`
- [x] T039 Document API usage in `frontend/README.md` and `backend/README.md`
- [x] T040 Run end-to-end tests for all user stories

## Implementation Strategy

1. **MVP (Phase 1-3)**: Focus on getting the `add_task` loop working end-to-end first.
2. **Expansion (Phase 4)**: Add navigation integration.
3. **Refinement (Phase 5)**: Implement real-time updates.
4. **Polish (Phase 6)**: Add error handling, fallbacks, and documentation.

## Dependencies

- Phase 3 requires Phase 2 (MCP tools must exist before Chat API can use them)
- Phase 2 requires Phase 1 (Project structure must be ready)

## Parallel Execution Opportunities

- [P] Tasks T001-T005 can run in parallel (setup tasks)
- [P] Tasks T006-T012 can run in parallel (foundational components)
- [P] Tasks T014-T020 can run in parallel (US1 frontend and backend components)
- [P] Tasks T022-T026 can run in parallel (US2 navigation components)
- [P] Tasks T028-T033 can run in parallel (US3 MCP tools and frontend updates)