---
id: 002
title: JWT Auth Implementation Plan
stage: plan
date: 2026-01-22
surface: agent
model: claude-opus-4-5-20251101
feature: 005-jwt-auth
branch: 005-jwt-auth
user: developer
command: /sp.plan
labels: ["authentication", "jwt", "planning", "implementation", "better-auth"]
links:
  spec: specs/005-jwt-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-jwt-auth/plan.md
  - specs/005-jwt-auth/research.md
  - specs/005-jwt-auth/data-model.md
  - specs/005-jwt-auth/contracts/auth-api.yaml
  - specs/005-jwt-auth/quickstart.md
tests:
  - null
---

## Prompt

/sp.plan now check frontend folder all files, backend folder all file then create plan.md file, Implementation Plan: Authentication Integration

Overview: This plan outlines the steps to implement authentication based on the specification, using the Agentic Dev Stack workflow. Since the technology stack is complete except for auth, focus on integration without disrupting existing code. Break into phases with tasks; each task will be implemented via Claude Code prompts (no manual coding). Review iterations for each phase.

Prerequisites:
- Verify existing setup: Next.js frontend with App Router, FastAPI backend, SQLModel ORM, Neon PostgreSQL connection.
- Shared JWT_SECRET in .env files for frontend and backend.
- Install dependencies if missing (e.g., better-auth for frontend, pyjwt for backend).

Phase 1: Database Updates - Define User model, add user_id to Task model, generate migrations
Phase 2: Frontend Authentication Setup - Configure Better Auth, create signup/signin pages
Phase 3: JWT Integration in Frontend - Configure JWT issuance, add Authorization headers
Phase 4: Backend Authorization - Verify JWT, filter data by user_id

## Response snapshot

Created comprehensive implementation plan for JWT Authentication feature:

**Key Finding**: Research revealed ~80% of auth infrastructure already exists but is bypassed. Focus shifted from building new to integrating existing components.

**Artifacts Created**:
1. `research.md` - Technical findings showing existing auth in backend (PyJWT, bcrypt, auth routes) and frontend (Better Auth, auth-client, signin/signup pages in public mode)
2. `data-model.md` - Entity definitions for User and Task (already implemented), JWT token structure
3. `contracts/auth-api.yaml` - OpenAPI 3.0 specification for auth and protected task endpoints
4. `quickstart.md` - Setup verification guide with curl commands
5. `plan.md` - 7-phase implementation plan with specific tasks and prompts

**Implementation Phases**:
- Phase 1: Backend Auth Route Mounting (mount existing auth_routes.py)
- Phase 2: Backend Protected Task Routes (add JWT verification)
- Phase 3: Frontend Auth Forms (restore login/signup forms)
- Phase 4: Frontend Route Protection (middleware.ts, AuthGuard)
- Phase 5: Frontend Token Handling (Authorization headers)
- Phase 6: Session Management (logout, expiry handling)
- Phase 7: Testing & Verification (E2E auth flows)

**Constitution Check**: All 6 principles PASS

## Outcome

- Impact: Complete implementation plan enabling team to execute JWT auth without ambiguity
- Tests: N/A (planning phase - test plan defined for Phase 7)
- Files: 5 files created (plan.md, research.md, data-model.md, auth-api.yaml, quickstart.md)
- Next prompts: `/sp.tasks` to generate detailed task list, then implement Phase 1
- Reflection: Research-first approach revealed existing infrastructure, significantly reducing scope

## Evaluation notes (flywheel)

- Failure modes observed: None - plan created successfully following workflow
- Graders run and results (PASS/FAIL): Constitution check PASS (all 6 principles)
- Prompt variant (if applicable): Standard /sp.plan with explicit file exploration request
- Next experiment (smallest change to try): Proceed to task generation with /sp.tasks
