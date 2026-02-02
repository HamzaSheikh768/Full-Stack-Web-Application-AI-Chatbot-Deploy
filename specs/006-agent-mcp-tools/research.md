# Phase 0: Research & Architecture Decisions

**Feature**: Agent & MCP Tools for Todo AI Chatbot
**Branch**: 006-agent-mcp-tools
**Status**: Completed

## 1. Technical Context & Constraints

The project constitution and feature specification establish strict constraints:
- **Frontend**: Next.js 16+ with **Official OpenAI ChatKit SDK**.
- **Backend**: Python FastAPI.
- **AI Agent**: **OpenAI Agents SDK** abstraction.
- **LLM Provider**: **Cohere** (via `COHERE_API_KEY`).
- **Tooling**: **Official MCP SDK** (Model Context Protocol).
- **Persistence**: Neon PostgreSQL via SQLModel.
- **Architecture**: Stateless server; agent state is transient; task state is persistent.

## 2. Decision Record

### Decision 1: OpenAI Agents SDK with Cohere
- **Requirements**: Use OpenAI Agents SDK but allow Cohere as the model provider.
- **Decision**: Use the OpenAI Agents SDK `Runner` and standard Agent structures. Since the SDK defaults to OpenAI models, we will configure it to use a custom client or model adapter compatible with Cohere's API structure, OR use Cohere's OpenAI-compatible endpoint if available.
- **Verification**: Cohere provides an OpenAI-compatible API endpoint (`https://api.cohere.com/v1`). We can use the standard OpenAI client in the Agents SDK but point the `base_url` to Cohere and use the `COHERE_API_KEY`.
- **Constraint Check**: Satisfies "ONLY Cohere API key" and "Official Agents SDK".

### Decision 2: Stateless MCP Tools
- **Requirements**: Tools must valid user_id and persist immediately. No in-memory state.
- **Decision**: Each MCP tool (`add_task`, etc.) will:
  1. Accept `user_id` as a required parameter.
  2. Instantiate a fresh database session (SQLModel).
  3. Perform the DB operation.
  4. Commit and close the session.
  5. Return a JSON outcome.
- **Pattern**: usage of `Depends(get_session)` pattern within the tool implementation or explicit context manager `with Session(engine) as session:`.

### Decision 3: ChatKit Integration
- **Requirements**: Use Official ChatKit SDK.
- **Decision**: Frontend will use `<Chat>` components from ChatKit.
- **Data Flow**: `ChatKit UI -> POST /api/chat -> Backend (Agents SDK) -> MCP -> DB`.
- **Statelessness**: The backend will reconstruct the conversation history from the DB for every request before passing it to the Agents SDK.

## 3. Technology Stack Confirmation

| Component | Choice | Reason |
|-----------|--------|--------|
| Agent SDK | OpenAI Agents SDK | Mandated by User |
| LLM | Cohere | Mandated by User |
| Interface | OpenAI ChatKit | Mandated by User |
| Tool Protocol | MCP (Official SDK) | Mandated by User |
| DB | Neon (SQLModel) | Existing Stack |

## 4. Unknowns Resolved

- **Clarification**: "Implement error handling for tool failures"
  - **Resolution**: Use MCP's standard error reporting. If a tool fails (e.g. DB error), return a structured ToolError result so the model can interpret it and apologize to the user, rather than crashing the HTTP request.

- **Clarification**: "Agent must never access DB directly"
  - **Resolution**: The Agent definition will NOT have direct SQL capabilities. It will ONLY be initialized with the specific list of 5 MCP tools as its available actions.

## 5. Security & Validation

- **User Isolation**: Every tool call MUST include `user_id`. The tool implementation MUST filter SQL queries by this `user_id`.
- **Auth**: The `POST /api/chat` endpoint is protected by Better Auth. The `user_id` is extracted from the verified session/token and passed securely to the agent/tools. The Agent cannot "invent" a user_id.

## 6. Conclusion

The architecture is viable and tightly constrained. We proceed to Data Model design.
