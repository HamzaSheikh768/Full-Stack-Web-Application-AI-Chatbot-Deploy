# Implementation Tasks: Database Integration for Todo AI Chatbot

**Branch**: `007-database-integration`
**Feature**: Database Integration for Todo AI Chatbot
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Phase 1: Setup & Project Initialization
**Goal**: Prepare the development environment and project structure for database integration.

- [x] T001 Create backend/src/database directory structure
- [x] T002 [P] Install SQLModel and Neon PostgreSQL dependencies in backend/requirements.txt
- [x] T003 [P] Add COHERE_API_KEY to environment configuration
- [x] T004 [P] Update backend/src/models/__init__.py to include new models

## Phase 2: Foundational Components (Blocking)
**Goal**: Implement core database models and connection setup required by all user stories.

- [x] T005 [P] Implement Task model with SQLModel in backend/src/models/task.py
- [x] T006 [P] Create Conversation model with SQLModel in backend/src/models/conversation.py
- [x] T007 [P] Create Message model with SQLModel in backend/src/models/message.py
- [x] T008 [P] Set up database connection pool with Neon-optimized settings in backend/src/database/db.py
- [x] T009 [P] Create database session management in backend/src/database/session.py
- [x] T010 [P] Implement database migration for new tables in backend/alembic/versions/

## Phase 3: User Story 1 - Persistent Task Management (Priority: P1)
**Goal**: Enable users to create, update, complete, or delete tasks through the AI assistant with permanent storage.
**Test**: User adds a task via AI Chat, closes browser, returns the next day, and finds the task still exists in their list.

- [x] T011 [US1] Implement add_task MCP tool with DB persistence in backend/src/mcp/handlers.py
- [x] T012 [US1] Implement list_tasks MCP tool with user isolation in backend/src/mcp/handlers.py
- [x] T013 [US1] Implement complete_task MCP tool with DB update in backend/src/mcp/handlers.py
- [x] T014 [US1] Implement delete_task MCP tool with DB removal in backend/src/mcp/handlers.py
- [x] T015 [US1] Implement update_task MCP tool with DB update in backend/src/mcp/handlers.py
- [x] T016 [US1] Create MCP server configuration in backend/src/mcp/server.py
- [x] T017 [US1] Implement Cohere agent configuration with MCP tools in backend/src/agent/core.py
- [x] T018 [US1] Update chat API endpoint to use stateless agent in backend/src/api/chat_routes.py

## Phase 4: User Story 2 - Conversation History Persistence (Priority: P2)
**Goal**: Store user's chat conversations and allow resumption from where they left off.
**Test**: User has a conversation with the AI, closes browser, returns later, and can see the previous conversation history.

- [x] T019 [US2] Implement conversation history loading from DB in backend/src/services/chat_service.py
- [x] T020 [US2] Update agent runner to fetch conversation history before processing in backend/src/agent/runner.py
- [x] T021 [US2] Implement conversation creation/management in backend/src/services/chat_service.py
- [x] T022 [US2] Update ChatWidget to load conversation history from API in frontend/src/components/ChatWidget.tsx
- [x] T023 [US2] Add conversation history display to ChatKit UI in frontend/src/components/ChatWidget.tsx

## Phase 5: User Story 3 - Secure Data Isolation (Priority: P3)
**Goal**: Ensure User A can only access their own tasks and conversations, never those belonging to User B.
**Test**: User A logs in and verifies they cannot see any tasks or conversations belonging to User B.

- [x] T024 [US3] Add user_id validation to all MCP tools in backend/src/mcp/handlers.py
- [x] T025 [US3] Implement user_id filtering in all database queries in backend/src/mcp/handlers.py
- [x] T026 [US3] Add authentication validation to chat endpoint in backend/src/api/chat_routes.py
- [x] T027 [US3] Test cross-user data access prevention in backend/tests/test_security.py

## Phase 6: Polish & Cross-Cutting Concerns
**Goal**: Final integration, error handling, and documentation.

- [x] T028 Add error handling for database connection failures in backend/src/database/db.py
- [x] T029 [P] Implement voice input fallback for unsupported browsers in frontend/src/lib/voice-recognition.ts
- [x] T030 [P] Add loading states and user feedback to ChatWidget in frontend/src/components/ChatWidget.tsx
- [x] T031 [P] Create integration tests for chat API in backend/tests/test_chat_api.py
- [x] T032 [P] Update frontend API client for chat functionality in frontend/src/lib/api.ts
- [x] T033 [P] Document API usage in backend/README.md and frontend/README.md

## Implementation Strategy

1. **MVP (Phase 1-3)**: Focus on getting the task CRUD operations working end-to-end first (P1 priority).
2. **Expansion (Phase 4)**: Add conversation history persistence.
3. **Refinement (Phase 5)**: Implement security enhancements.
4. **Polish (Phase 6)**: Add error handling, fallbacks, and documentation.

## Dependencies

- Phase 3 requires Phase 2 (MCP tools need models and DB connection)
- Phase 4 requires Phase 3 (conversation features build on task management)
- Phase 5 requires Phase 2 (security checks need models)

## Parallel Execution Opportunities

- [P] Tasks T002-T004 can run in parallel (setup tasks)
- [P] Tasks T005-T007 can run in parallel (model creation)
- [P] Tasks T008-T010 can run in parallel (database setup)
- [P] Tasks T011-T015 can run in parallel (MCP tool implementations)
- [P] Tasks T029-T032 can run in parallel (polish tasks)