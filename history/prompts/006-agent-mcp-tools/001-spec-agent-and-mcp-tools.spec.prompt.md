---
id: 001
title: Spec Agent and MCP Tools
stage: spec
date: 2026-01-23
surface: agent
model: claude-opus-4-5-20251101
feature: agent-mcp-tools
branch: 006-agent-mcp-tools
user: anonymous
command: sp.specify
labels: [spec, agent, mcp, chatkit, cohere]
links:
  spec: specs/006-agent-mcp-tools/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/006-agent-mcp-tools/spec.md
  - specs/006-agent-mcp-tools/checklists/requirements.md
tests:
  - Validated spec quality checklist
---

## Prompt

now create sp.specify very details and dont used any api key used only i will provide your text important used only official Chatkit SDK And Agent SDK /specs/agent-and-mcp.spec.md
# Agent & MCP Tools Specification – Todo AI Chatbot

## Purpose
Define the AI agent behavior and all stateless MCP tools for task management.

---

## Agent Framework
- OpenAI Agents SDK (agent abstraction)
- LLM Provider: Cohere (API key via environment variable only)

## Agent Responsibilities
- Interpret user natural language (text or voice)
- Invoke MCP tools for all task operations
- Generate friendly confirmations
- Never access DB directly

## Prohibited Agent Behavior
- Performing CRUD internally
- Storing memory
- Bypassing MCP tools
- Assuming task IDs

## Tool Usage Mapping
| User Intent | MCP Tool |
|------------|-----------|
| Add / Create | add_task |
| List / Show | list_tasks |
| Complete / Done | complete_task |
| Delete / Remove | delete_task |
| Update / Change | update_task |

## Error Handling
- Apologize on failure
- Suggest corrective actions

---

## MCP Tools – Todo Operations

### General Rules
- Stateless, persistent via DB
- Validate user_id ownership
- Return structured JSON

### add_task
- Purpose: create a new task
- Parameters: user_id, title, description (optional)
- Returns: task_id, status, title

### list_tasks
- Purpose: fetch tasks
- Parameters: user_id, status (all/pending/completed)
- Returns: array of task objects

### complete_task
- Purpose: mark a task completed
- Parameters: user_id, task_id
- Returns: task_id, status, title

### delete_task
- Purpose: delete a task
- Parameters: user_id, task_id
- Returns: task_id, status, title

### update_task
- Purpose: update task title/description
- Parameters: user_id, task_id, title (opt), description (opt)
- Returns: task_id, status, title

## Response snapshot

Created detailed feature specification for Agent & MCP Tools.

- Branch: `006-agent-mcp-tools`
- Spec File: `specs/006-agent-mcp-tools/spec.md`
- Quality Checklist: `specs/006-agent-mcp-tools/checklists/requirements.md` (Passed)

Key Definition:
- **Framework**: Official OpenAI Agents SDK + ChatKit SDK + Cohere LLM (only).
- **Architecture**: Stateless agent using MCP tools for all persistence.
- **Constraints**: No unauthorized API keys, strict user_id validation, no internal CRUD.

## Outcome

- ✅ Impact: Established strict architectural blueprint for Phase III AI integration.
- 🧪 Tests: Validated against SDD checklist; all requirements testable.
- 📁 Files: Created spec.md and checklist.
- 🔁 Next prompts: Run `/sp.plan` to generate implementation architecture.
- 🧠 Reflection: User provided detailed constraints which were successfully mapped to Functional Requirements (FRs) and prohibited behaviors.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS.
- Prompt variant (if applicable): N/A.
- Next experiment (smallest change to try): N/A.
