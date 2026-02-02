# Implementation Plan: Agent & MCP Tools for Todo AI Chatbot

**Branch**: `006-agent-mcp-tools` | **Date**: 2026-01-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-agent-mcp-tools/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement the core AI Agent behavior and stateless MCP tools for the Todo Chatbot. The Agent will use the OpenAI Agents SDK configured with Cohere as the LLM provider. The backend will expose 5 MCP tools (add, list, complete, delete, update) that persist data to Neon PostgreSQL via SQLModel. All operations are strictly authenticated and isolated by user_id.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5+ (Next.js)
**Primary Dependencies**:
- Backend: FastAPI, OpenAI Agents SDK, MCP Official SDK, SQLModel
- Frontend: OpenAI ChatKit SDK
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (Backend), Jest (Frontend if applicable)
**Target Platform**: Vercel (Frontend), Render/Railway (Backend)
**Project Type**: Monorepo (frontend/backend)
**Performance Goals**: <500ms API response (excluding LLM latency)
**Constraints**:
- ONLY Cohere API key allowed
- NO Agent memory persistence (Stateless)
- NO direct DB access by Agent
**Scale/Scope**: <1000 users MVP

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Spec-Driven Development**: Spec created and validated.
- [x] **AI-First Architecture**: Uses ChatKit and Agents SDK.
- [x] **Security First**: Authentication context required for all tools.
- [x] **Cohere-Only Constraint**: Plan explicitly configures Cohere as provider.
- [x] **Stateless Server Model**: All state persisted to DB immediately.
- [x] **Modularity**: Tools are defined as independent functions.

## Project Structure

### Documentation (this feature)

```text
specs/006-agent-mcp-tools/
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
│   ├── models/
│   │   ├── task.py          # Existing + Update
│   │   └── conversation.py  # New
│   ├── mcp/                 # NEW DIRECTORY
│   │   ├── tools.py         # MCP Tool definitions
│   │   ├── server.py        # MCP Server setup
│   │   └── handlers.py      # Implementation logic
│   ├── agent/               # NEW DIRECTORY
│   │   ├── core.py          # Agent initialization (Cohere config)
│   │   └── runner.py        # Stateless execution logic
│   └── api/
│       └── chat_routes.py   # Chat endpoint
└── tests/
    └── test_agent_mcp.py    # Integration tests

frontend/
├── src/
│   ├── components/
│   │   └── Chat.tsx         # Updated with ChatKit
│   └── lib/
│       └── chat-api.ts      # API client for ChatKit
```

**Structure Decision**: Monorepo split (`backend/`, `frontend/`) as mandated by Constitution Phase III structure.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| MCP SDK | User mandate | Direct function calling is simpler but less standard |
| Agents SDK | User mandate | Custom LLM loop is simpler but less robust |
