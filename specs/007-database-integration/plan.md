# Implementation Plan: Database Integration for Todo AI Chatbot

**Branch**: `007-database-integration` | **Date**: 2026-01-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-database-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement persistent storage and full database-backed conversation & task management for the Todo AI Chatbot. This includes creating SQLModel database entities (Task, Conversation, Message), connecting the FastAPI backend to Neon Serverless PostgreSQL, ensuring all user messages, assistant responses, and MCP tool outputs are persisted, and enforcing UI reads only from API-backed database with proper user isolation and Cohere API key access via environment variable.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5+ (Next.js 16+)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel 0.0.22+, Cohere SDK, OpenAI SDK, MCP SDK
- Frontend: Next.js 16+ with App Router, ChatKit SDK, Web Speech API
**Storage**: Neon Serverless PostgreSQL via SQLModel ORM
**Testing**: pytest (Backend), Jest/Vitest (Frontend)
**Target Platform**: Vercel (Frontend), Render/Railway (Backend) - Web Application
**Project Type**: Web application (frontend/backend monorepo)
**Performance Goals**:
- API responses under 500ms (excluding LLM latency)
- Database queries under 200ms for standard operations
- UI updates within 2 seconds for task changes
- Chat page loads in under 3 seconds
**Constraints**:
- ONLY Cohere API key allowed for AI functionality (via COHERE_API_KEY env var)
- Stateless server design - no conversation state in memory
- User isolation - all data access filtered by user_id
- All AI interactions via MCP tools only
- No direct database access by Agent
**Scale/Scope**: <1000 users MVP with real-time updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Spec-Driven Development**: Spec created and validated in `specs/007-database-integration/spec.md`.
- [x] **AI-First Architecture**: Uses ChatKit SDK and Cohere API as mandated.
- [x] **Security First**: Authentication context required for all chat operations, user isolation maintained.
- [x] **Cohere-Only Constraint**: Plan explicitly configures Cohere as LLM provider (no other AI APIs).
- [x] **Stateless Server Model**: All state persisted to DB immediately, no conversation state in server memory.
- [x] **Modularity**: Tools and UI components are designed as independent modules.
- [x] **Frontend Constitution**: Uses official ChatKit SDK as UI layer.
- [x] **Backend Constitution**: Implements stateless chat endpoint at `POST /api/{user_id}/chat`.
- [x] **MCP Constitution**: All AI operations use MCP tools exclusively.
- [x] **Database Constitution**: All conversation/messages persisted via SQLModel.
- [x] **Conversation Flow Constitution**: Stateless lifecycle implemented with DB persistence.

## Project Structure

### Documentation (this feature)

```text
specs/007-database-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── chat-api-contracts.json
│   └── mcp-tools-contracts.json
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Option 2: Web application (frontend/backend monorepo)
backend/
├── src/
│   ├── main.py
│   ├── models/
│   │   ├── task.py          # Updated: Add database fields
│   │   ├── conversation.py  # NEW: Conversation model
│   │   └── message.py       # NEW: Message model
│   ├── mcp/
│   │   ├── tools.py         # MCP Tool definitions
│   │   ├── handlers.py      # MCP Tool implementations (with DB persistence)
│   │   └── server.py        # MCP Server setup
│   ├── agent/
│   │   ├── core.py          # Agent configuration (Cohere integration)
│   │   └── runner.py        # Stateless agent execution
│   ├── api/
│   │   ├── chat_routes.py   # Chat endpoint with DB integration
│   │   └── base_routes.py   # Existing: Other API routes
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py            # Database connection setup
│   │   └── session.py       # Session management
│   └── services/
│       └── chat_service.py  # Chat-specific business logic
└── tests/
    ├── test_chat_api.py     # API integration tests
    └── test_mcp_tools.py    # MCP tools tests

frontend/
├── src/
│   ├── app/
│   │   ├── chat/
│   │   │   └── page.tsx    # AI Chat page
│   │   └── layout.tsx      # Root layout with navigation
│   ├── components/
│   │   ├── ChatWidget.tsx  # ChatKit UI component
│   │   ├── VoiceInputWidget.tsx # Voice input component
│   │   └── TaskUpdateNotificationWidget.tsx # Real-time updates
│   ├── lib/
│   │   ├── api.ts          # API client
│   │   ├── chat-api.ts     # Chat-specific API client
│   │   └── voice-recognition.ts # Voice recognition service
│   └── types/
│       └── chat.ts          # Chat-related TypeScript types
```

**Structure Decision**: Monorepo split (`backend/`, `frontend/`) as mandated by Constitution Phase III structure. The existing project structure is extended to include database integration with new models, MCP tools, and chat-specific components.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple Endpoints | Chat requires both text and voice input handling | Single endpoint insufficient for different input types |
| Database Transactions | Required for data consistency during MCP tool operations | Simpler direct DB operations risk inconsistency |
| MCP Protocol | User requirement for standardized tooling interface | Direct function calling is simpler but less standard |
