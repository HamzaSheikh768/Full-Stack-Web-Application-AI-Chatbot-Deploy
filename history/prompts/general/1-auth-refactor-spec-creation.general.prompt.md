---
id: 1
title: "auth-refactor-spec-creation"
stage: "spec"
date_iso: "2026-01-26"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "auth-refactor"
branch: "1-auth-refactor"
user: "user"
command: "sp.specify"
labels: ["specification", "authentication", "refactor", "security"]
links:
  spec: "specs/1-auth-refactor/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/1-auth-refactor/spec.md
  - specs/1-auth-refactor/checklists/requirements.md
tests_yaml: |
  - "Specification quality validation"
prompt_text: |
  now before check files and detect all auth-related files then create specs file auth-related files name add. # SP.SPECIFY

  ## TASKAPP – Full‑Stack Todo Application (Auth, Tasks, AI, Neon DB)

  ---

  ## 1. Purpose

  This specification defines the **authoritative requirements** to build and refine **TASKAPP**, a production‑grade full‑stack Todo application. It enforces:

  * Complete **authentication refactor** with CTAs aligned on the **full right‑hand side** of the UI
  * Real‑time task management (add, edit, delete, list)
  * AI‑powered natural‑language task creation
  * **Neon Serverless PostgreSQL as the only data source** (no dummy, fake, or mock data)
  * Strict **frontend–backend API parity**
  * Modern **Tailwind CSS UI** (dark mode by default)

  This document is the **single source of truth** and must be followed without deviation.

  ---

  ## 2. Non‑Negotiable Constraints

  * ❌ No dummy, fake, seeded, or mock data in production or tests

  * ❌ No mismatched API paths between frontend and backend

  * ❌ No legacy authentication code remains

  * ✅ All data persisted and read from **Neon PostgreSQL**

  * ✅ Authentication state is secure and server‑validated

  * ✅ Frontend and backend share identical endpoint paths

  ---

  ## 3. Technology Stack (Locked)

  ### Monorepo Structure

  ```
  /
  ├── frontend/   (Next.js 16+)
  ├── backend/    (FastAPI)
  ├── shared/     (shared types & contracts)
  └── README.md
  ```

  ### Frontend

  * Next.js 16+
  * TypeScript
  * Tailwind CSS
  * React Hook Form
  * Zustand or Context API

  ### Backend

  * Python 3.12+
  * FastAPI
  * SQLModel
  * Alembic
  * JWT‑based auth (secure handling)

  ### Database

  * Neon Serverless PostgreSQL

  ---

  ## 4. Step 1 – Read & Structure Existing Files

  ### Requirements

  * Scan the **entire repository**
  * Read all files (frontend, backend, root)
  * Categorize into:

    * `/frontend`
    * `/backend`
    * `/shared`
    * Root config files

  ### Output Artifact

  * `project_structure.md`

    * Lists **every file** with a brief description

  ---

  ## 5. Step 2 – Detect, Remove & Recreate Authentication

  ### 5.1 Detection Rules

  Identify any file related to:

  * Auth (login/signup/logout)
  * JWT, sessions, Better Auth (legacy)
  * Auth middleware or hooks

  Examples:

  * `auth.ts`
  * `auth.router.py`
  * `login/page.tsx`

  ---

  ### 5.2 Removal Rules

  * Remove all detected auth files
  * Optionally move to `/archive` (read‑only)
  * Application must boot **without auth** before recreation

  ---

  ### 5.3 Recreated Authentication (Authoritative)

  #### Backend

  * Endpoints:

    * `POST /api/auth/signup`
    * `POST /api/auth/login`
    * `POST /api/auth/logout`
  * Users stored in Neon
  * Passwords hashed
  * Secure token handling

  #### Frontend

  * `useAuth` hook
  * Login & Signup pages
  * Form validation
  * Auth state synced with backend

  ---

  ## 6. Step 3 – Neon Database Integration

  ### Database Models (SQLModel)

  #### User

  * id (UUID)
  * email (unique)
  * password_hash
  * role (admin | user | guest)
  * created_at

  #### Task

  * id (UUID)
  * title
  * description
  * completed
  * user_id (FK)
  * created_at

  ---

  ### Rules

  * Alembic migrations only
  * All CRUD operations hit Neon in real time
  * No local or in‑memory stores

  ---

  ## 7. Step 4 – Shared API Contracts

  ### Required Artifact

  * `shared/api-contract.md`
  * `shared/types.ts`

  ### Task Endpoints (Locked)

  * `POST /api/tasks`
  * `GET /api/tasks`
  * `PUT /api/tasks/{id}`
  * `DELETE /api/tasks/{id}`

  Auth endpoints must follow the same `/api` namespace.

  ---

  ## 8. Step 5 – UI / UX Specification (Tailwind)

  ### Global Theme

  * Dark mode default
  * Background: black
  * Text: white
  * Accent: blue `#3B82F6`

  ---

  ### Navbar (Critical Requirement)

  * Fixed top navbar
  * Left: **TASKAPP logo**
  * Right (FULL RIGHT‑HAND SIDE):

    * Sign Up CTA
    * Sign In CTA
    * Logout (when authenticated)
    * Dark/Light mode toggle

  Buttons must be visually aligned and prominent.

  ---

  ### Components

  * Auth Forms: rounded inputs, blue CTA buttons
  * Tasks: card‑based layout, hover animations
  * AI Chat: chat bubbles (user blue, AI gray)

  Use Tailwind transitions and subtle animations.

  ---

  ## 9. Step 6 – Completion & Testing

  ### Backend Tests

  * Pytest
  * Real Neon DB connection
  * Auth + Task CRUD validation

  ### Frontend Tests

  * Unit tests (components/hooks)
  * E2E tests (signup → create task → logout)

  ### Output

  * `test_report.md`

  ---

  ## 10. Step 7 – Create 3 Real Users in Neon

  ### Users (Mandatory)

  1. [user1@example.com](mailto:user1@example.com) / SecurePass123! / admin
  2. [user2@example.com](mailto:user2@example.com) / SecurePass123! / user
  3. [user3@example.com](mailto:user3@example.com) / SecurePass123! / guest

  ### Rules

  * Insert via backend logic or setup script
  * Passwords hashed
  * Verified via frontend login

  ---

  ## 11. Deliverables

  * Clean monorepo (no legacy auth)
  * Fully working auth + tasks + AI features
  * Neon‑backed real data
  * Modern Tailwind UI
  * Shared API contracts
  * Test reports
  * Setup & run instructions

  ---

  ## 12. Status

  * Document Type: **SP.SPECIFY (Authoritative)**
  * Project: TASKAPP
  * Status: **APPROVED FOR EXECUTION**
  * Date: 2026‑01‑26
response_text: |
  Successfully created specification for the authentication refactor feature. The specification includes:

  1. User scenarios for registration, login, logout, and protected task access
  2. 14 functional requirements covering secure authentication, data protection, and session management
  3. Key entities (User, Session, Authentication Token)
  4. 7 measurable success criteria

  Created files:
  - specs/1-auth-refactor/spec.md: Complete feature specification
  - specs/1-auth-refactor/checklists/requirements.md: Quality validation checklist

  The specification covers all requirements from the original request including JWT-based authentication, Neon database integration, proper data isolation, and API parity between frontend and backend.
outcome: "spec_created_successfully"
evaluation: "The specification comprehensively covers the authentication refactor requirements with clear user stories, functional requirements, and success criteria. All validation checklist items passed."
---
