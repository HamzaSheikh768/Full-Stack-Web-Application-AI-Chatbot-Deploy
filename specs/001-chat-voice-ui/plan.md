# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement the Chat API, Voice Input, and UI Navigation features for the AI Chatbot. This includes creating the backend chat endpoint that integrates with the Cohere AI agent and MCP tools, implementing voice input functionality using the Web Speech API, and adding navigation elements to access the AI Chat feature from throughout the application. The system will use the official ChatKit SDK for the frontend UI and maintain a stateless server design.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5+ (Next.js 16+)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, Cohere SDK, OpenAI SDK, MCP SDK
- Frontend: Next.js 16+ with App Router, ChatKit SDK, Web Speech API
**Storage**: Neon Serverless PostgreSQL via SQLModel
**Testing**: pytest (Backend), Jest/Vitest (Frontend)
**Target Platform**: Vercel (Frontend), Render/Railway (Backend) - Web Application
**Project Type**: Web application (frontend/backend monorepo)
**Performance Goals**:
- API responses under 500ms (excluding LLM latency)
- UI updates within 2 seconds for task changes
- Chat page loads in under 3 seconds
**Constraints**:
- ONLY Cohere API key allowed for AI functionality
- Stateless server design - no conversation state in memory
- User isolation - all data access filtered by user_id
- All AI interactions via MCP tools only
**Scale/Scope**: <1000 users MVP with real-time updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Spec-Driven Development**: Spec created and validated in `specs/001-chat-voice-ui/spec.md`.
- [x] **AI-First Architecture**: Uses ChatKit SDK and Cohere API as mandated.
- [x] **Security First**: Authentication context required for all chat operations, user isolation maintained.
- [x] **Cohere-Only Constraint**: Plan explicitly configures Cohere as LLM provider (no other AI APIs).
- [x] **Stateless Server Model**: All state persisted to DB immediately, no conversation state in server memory.
- [x] **Modularity**: Tools and UI components are designed as independent modules.
- [x] **Frontend Constitution**: Uses official ChatKit SDK as UI layer.
- [x] **Backend Constitution**: Implements stateless chat endpoint at `POST /api/{user_id}/chat`.
- [x] **MCP Constitution**: All AI operations use MCP tools exclusively.
- [x] **Database Constitution**: All conversation/messages persisted via SQLModel.

## Project Structure

### Documentation (this feature)

```text
specs/001-chat-voice-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Option 2: Web application (frontend/backend monorepo)
backend/
├── src/
│   ├── main.py
│   ├── api/
│   │   ├── chat_routes.py      # New: Chat endpoint implementation
│   │   └── base_routes.py      # Existing: Other API routes
│   ├── models/
│   │   ├── task.py             # Existing: Task model
│   │   ├── user.py             # Existing: User model
│   │   └── conversation.py     # New: Conversation/Message models for chat
│   ├── mcp/
│   │   ├── tools.py            # Existing: MCP tool definitions
│   │   └── handlers.py         # Existing: MCP tool implementations
│   ├── agent/
│   │   ├── core.py             # Existing: Agent configuration
│   │   └── runner.py           # Existing: Agent execution logic
│   ├── database/
│   │   └── db.py               # Existing: Database setup
│   └── services/
│       └── chat_service.py     # New: Chat-specific business logic
└── tests/
    └── test_chat_api.py        # New: Chat API tests

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Existing: Root layout
│   │   ├── page.tsx            # Existing: Home page
│   │   ├── dashboard/
│   │   │   └── page.tsx        # Existing: Dashboard page
│   │   ├── tasks/
│   │   │   └── page.tsx        # Existing: Tasks page
│   │   └── chat/
│   │       └── page.tsx        # New: AI Chat page
│   ├── components/
│   │   ├── Navbar.tsx          # Updated: Add AI Chat button
│   │   ├── Sidebar.tsx         # Updated: Add AI Chat link
│   │   ├── ChatWidget.tsx      # New: ChatKit UI widget with voice input
│   │   ├── VoiceInputWidget.tsx # New: Web Speech API widget
│   │   ├── TaskUpdateNotificationWidget.tsx # New: Real-time task update widget
│   │   ├── QuickChatWidget.tsx # New: Floating quick access widget
│   │   └── TaskList.tsx        # Updated: Real-time updates from chat
│   ├── lib/
│   │   ├── api.ts              # Updated: Chat API client
│   │   └── voice-recognition.ts # New: Web Speech API wrapper
│   └── types/
│       └── chat.ts              # New: Chat-related TypeScript types
```

**Structure Decision**: Monorepo split (`backend/`, `frontend/`) as mandated by Constitution Phase III structure. The existing project structure is extended to include chat functionality with new files for the Chat API, Conversation models, and ChatKit UI components.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple Endpoints | Chat requires both text and voice input handling | Single endpoint insufficient for different input types |
| Real-time Updates | UX requirement for immediate feedback | Delayed updates would degrade user experience |
