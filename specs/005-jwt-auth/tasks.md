# Tasks: JWT Authentication Implementation

**Input**: Design documents from `/specs/005-jwt-auth/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/auth-api.yaml

**Tests**: Not explicitly requested - test verification included in final phase.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify environment and mount existing auth infrastructure

- [x] T001 Verify BETTER_AUTH_SECRET matches in both backend/.env and frontend/.env
- [x] T002 Verify PyJWT and passlib[bcrypt] are installed in backend/requirements.txt
- [x] T003 [P] Verify better-auth package is installed in frontend/package.json
- [x] T004 Import and mount auth_routes in backend/src/main.py with `/api` prefix

**Checkpoint**: Auth routes accessible at `/api/auth/register`, `/api/auth/login`, `/api/auth/me`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core auth infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Verify User model exists with id, email, password_hash in backend/src/models/user.py
- [x] T006 [P] Verify Task model has user_id foreign key in backend/src/models/task.py
- [x] T007 [P] Verify JWT utilities exist in backend/src/auth.py (create_access_token, get_current_user_from_token)
- [x] T008 Update JWT token expiration to 7 days (10080 minutes) in backend/src/auth.py
- [x] T009 [P] Verify auth API client exists in frontend/src/lib/backend-auth-api.ts
- [x] T010 Create protected task routes file backend/src/api/protected_routes.py with JWT dependency
- [x] T011 Mount protected routes in backend/src/main.py with `/api` prefix for user-scoped endpoints

**Checkpoint**: Foundation ready - Protected routes mounted, JWT verification working

---

## Phase 3: User Story 1 - New User Registration (Priority: P1)

**Goal**: Allow new users to create accounts with email/password, receive JWT token, access dashboard

**Independent Test**: Navigate to `/signup`, enter valid email/password/name, verify redirect to dashboard

### Implementation for User Story 1

- [x] T012 [P] [US1] Create SignupForm.tsx component in frontend/src/components/auth/SignupForm.tsx with email, password, name fields
- [x] T013 [US1] Add form validation for email format and password length (min 8 chars) in SignupForm.tsx
- [x] T014 [US1] Integrate SignupForm with authApi.register() from frontend/src/lib/auth-client.ts
- [x] T015 [US1] Update frontend/src/app/signup/page.tsx to render SignupForm instead of redirect message
- [x] T016 [US1] Add error handling for "Email already registered" response in SignupForm.tsx
- [x] T017 [US1] Implement redirect to /dashboard after successful registration in signup/page.tsx
- [x] T018 [US1] Apply UI styling: Blue submit button (#007BFF), focus glow animation in SignupForm.tsx

**Checkpoint**: User can register at /signup, token stored, redirected to dashboard

---

## Phase 4: User Story 2 - Existing User Sign In (Priority: P1)

**Goal**: Allow returning users to sign in with email/password, receive JWT token, access dashboard

**Independent Test**: Navigate to `/signin`, enter valid credentials, verify redirect to dashboard

### Implementation for User Story 2

- [x] T019 [P] [US2] Create LoginForm.tsx component in frontend/src/components/auth/LoginForm.tsx with email, password fields
- [x] T020 [US2] Add form validation for required fields in LoginForm.tsx
- [x] T021 [US2] Integrate LoginForm with authApi.login() from frontend/src/lib/auth-client.ts
- [x] T022 [US2] Update frontend/src/app/signin/page.tsx to render LoginForm instead of redirect message
- [x] T023 [US2] Add error handling for "Invalid credentials" response in LoginForm.tsx
- [x] T024 [US2] Implement redirect to /dashboard after successful login in signin/page.tsx
- [x] T025 [US2] Apply UI styling: Blue submit button (#007BFF), focus glow animation in LoginForm.tsx

**Checkpoint**: User can sign in at /signin, token stored, redirected to dashboard

---

## Phase 5: User Story 3 - Protected API Access (Priority: P1)

**Goal**: Ensure API endpoints verify JWT and only return user's own data

**Independent Test**: Make API request with valid token, verify only user's tasks returned; request without token returns 401

### Implementation for User Story 3

- [x] T026 [P] [US3] Implement GET /{user_id}/tasks in backend/src/api/protected_routes.py with JWT verification
- [x] T027 [P] [US3] Implement POST /{user_id}/tasks in backend/src/api/protected_routes.py with JWT verification
- [x] T028 [P] [US3] Implement GET /{user_id}/tasks/{task_id} in backend/src/api/protected_routes.py
- [x] T029 [P] [US3] Implement PUT /{user_id}/tasks/{task_id} in backend/src/api/protected_routes.py
- [x] T030 [P] [US3] Implement DELETE /{user_id}/tasks/{task_id} in backend/src/api/protected_routes.py
- [x] T031 [US3] Implement PATCH /{user_id}/tasks/{task_id}/complete in backend/src/api/protected_routes.py
- [x] T032 [US3] Add user_id verification (token user_id must match path user_id) returning 403 if mismatch
- [x] T033 [US3] Filter all task queries by user_id from authenticated token in protected_routes.py
- [x] T034 [US3] Update frontend/src/lib/api.ts to include Authorization header with Bearer token
- [x] T035 [US3] Handle 401 responses in frontend API client with redirect to /signin

**Checkpoint**: API endpoints protected, user isolation enforced, frontend sends token

---

## Phase 6: User Story 4 - User Session Management (Priority: P2)

**Goal**: Allow users to logout, handle session expiration gracefully

**Independent Test**: Click logout button, verify token cleared, redirected to signin

### Implementation for User Story 4

- [x] T036 [P] [US4] Create AuthGuard.tsx wrapper component in frontend/src/components/auth/AuthGuard.tsx
- [x] T037 [US4] Implement authentication check in AuthGuard using authApi.isAuthenticated()
- [x] T038 [US4] Create Next.js middleware.ts in frontend/src/middleware.ts for route protection
- [x] T039 [US4] Configure protected routes (/dashboard, /tasks, /profile) in middleware.ts
- [x] T040 [US4] Configure redirect to /dashboard for authenticated users on /signin and /signup
- [x] T041 [US4] Add logout button to frontend/src/components/navigation/Navbar.tsx
- [x] T042 [US4] Implement logout handler calling authApi.logout() and redirecting to /signin
- [x] T043 [US4] Show "Session expired" message when 401 received on protected page

**Checkpoint**: Logout works, protected routes redirect unauthenticated users, session expiry handled

---

## Phase 7: User Story 5 - Task Ownership Enforcement (Priority: P2)

**Goal**: Ensure all task CRUD operations enforce ownership - users can only modify their own tasks

**Independent Test**: Create task as User A, attempt to modify as User B, verify 403 response

### Implementation for User Story 5

- [x] T044 [US5] Verify task ownership check in GET /{user_id}/tasks/{task_id} (task.user_id == current_user.id)
- [x] T045 [US5] Verify task ownership check in PUT /{user_id}/tasks/{task_id} before update
- [x] T046 [US5] Verify task ownership check in DELETE /{user_id}/tasks/{task_id} before delete
- [x] T047 [US5] Verify task ownership check in PATCH /{user_id}/tasks/{task_id}/complete
- [x] T048 [US5] Return 404 (not 403) for non-existent tasks to prevent user enumeration
- [x] T049 [US5] Auto-set user_id from authenticated token on task creation (not from request body)
- [x] T050 [US5] Update frontend task service to use authenticated user's ID from token

**Checkpoint**: Full user isolation - no cross-user data access possible

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and improvements

- [x] T051 [P] Update frontend/src/app/dashboard/page.tsx to fetch tasks using protected API
- [x] T052 [P] Update task creation form to use protected POST endpoint
- [x] T053 [P] Update task update/delete operations to use protected endpoints
- [x] T054 Verify CORS configuration in backend/src/main.py allows frontend origin
- [x] T055 Manual test: Full registration flow (signup → dashboard → create task)
- [x] T056 Manual test: Full login flow (signin → dashboard → view tasks)
- [x] T057 Manual test: User isolation (User A creates task, User B cannot see it)
- [x] T058 Manual test: Session management (logout → protected route redirects)
- [x] T059 Run quickstart.md verification steps
- [x] T060 Update frontend/src/app/page.tsx (landing page) with login/signup links

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ─────────────────┐
                                 │
Phase 2 (Foundational) ──────────┼─── BLOCKS ALL USER STORIES
                                 │
         ┌───────────────────────┴───────────────────────┐
         │                                               │
         ▼                                               ▼
Phase 3 (US1: Registration)              Phase 4 (US2: Sign In)
         │                                               │
         └───────────────┬───────────────────────────────┘
                         │
                         ▼
              Phase 5 (US3: Protected API)
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
Phase 6 (US4: Session Mgmt)   Phase 7 (US5: Ownership)
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼
              Phase 8 (Polish)
```

### User Story Dependencies

| Story | Can Start After | Notes |
|-------|-----------------|-------|
| US1 (Registration) | Phase 2 | Independent |
| US2 (Sign In) | Phase 2 | Independent, can parallel with US1 |
| US3 (Protected API) | Phase 2 | Requires backend routes from Phase 2 |
| US4 (Session) | US1, US2 | Needs working auth forms |
| US5 (Ownership) | US3 | Needs protected routes |

### Within Each User Story

- Models before services
- Backend before frontend (for API endpoints)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 2 (Foundational)**:
```
T005, T006, T007 can run in parallel (different files)
T009 can run in parallel with backend tasks
```

**Phase 3 + 4 (Registration + Sign In)**:
```
US1 and US2 can run in parallel (independent forms)
T012 and T019 can start simultaneously
```

**Phase 5 (Protected API)**:
```
T026, T027, T028, T029, T030 can run in parallel (different endpoints)
```

**Phase 6 + 7 (Session + Ownership)**:
```
US4 and US5 can run in parallel once US3 complete
```

---

## Parallel Example: Protected Routes

```bash
# Launch all endpoint implementations together:
Task T026: "Implement GET /{user_id}/tasks in backend/src/api/protected_routes.py"
Task T027: "Implement POST /{user_id}/tasks in backend/src/api/protected_routes.py"
Task T028: "Implement GET /{user_id}/tasks/{task_id} in backend/src/api/protected_routes.py"
Task T029: "Implement PUT /{user_id}/tasks/{task_id} in backend/src/api/protected_routes.py"
Task T030: "Implement DELETE /{user_id}/tasks/{task_id} in backend/src/api/protected_routes.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Registration)
4. Complete Phase 4: User Story 2 (Sign In)
5. Complete Phase 5: User Story 3 (Protected API)
6. **STOP and VALIDATE**: Test registration, login, and API access
7. Deploy/demo if ready - this is a functional MVP!

### Full Implementation

1. Complete MVP (Phases 1-5)
2. Add Phase 6: User Story 4 (Session Management)
3. Add Phase 7: User Story 5 (Ownership Enforcement)
4. Complete Phase 8: Polish
5. Full auth system complete with all security features

### Suggested Execution Order

```
Day 1: T001-T011 (Setup + Foundational)
Day 2: T012-T018 (Registration) + T019-T025 (Sign In) in parallel
Day 3: T026-T035 (Protected API)
Day 4: T036-T050 (Session + Ownership)
Day 5: T051-T060 (Polish + Verification)
```

---

## Summary

| Phase | Task Count | Parallel Tasks | Description |
|-------|------------|----------------|-------------|
| 1. Setup | 4 | 1 | Environment verification |
| 2. Foundational | 7 | 4 | Core auth infrastructure |
| 3. US1 (Registration) | 7 | 1 | Signup form and flow |
| 4. US2 (Sign In) | 7 | 1 | Login form and flow |
| 5. US3 (Protected API) | 10 | 5 | JWT-protected endpoints |
| 6. US4 (Session) | 8 | 1 | Logout and route protection |
| 7. US5 (Ownership) | 7 | 0 | Task ownership verification |
| 8. Polish | 10 | 3 | Final verification |
| **Total** | **60** | **16** | |

**MVP Scope**: Phases 1-5 (35 tasks) delivers functional registration, login, and protected API
**Full Scope**: All phases (60 tasks) delivers complete auth system with session management and ownership enforcement
