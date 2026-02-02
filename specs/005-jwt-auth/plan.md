# Implementation Plan: JWT Authentication Integration

**Branch**: `005-jwt-auth` | **Date**: 2026-01-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-jwt-auth/spec.md`

## Summary

Transform the Todo application from public access mode to a secure multi-user system using JWT authentication. The implementation leverages **existing auth infrastructure** in both frontend and backend, requiring primarily integration work rather than new development.

**Key Finding**: Research revealed that ~80% of auth infrastructure already exists but is bypassed. The plan focuses on:
1. Mounting existing auth routes in backend
2. Restoring login/signup forms in frontend
3. Protecting task routes with JWT verification
4. Adding frontend route protection middleware

---

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/Next.js 16+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, PyJWT, passlib[bcrypt], asyncpg
- Frontend: Next.js App Router, Better Auth, React
**Storage**: Neon Serverless PostgreSQL (production), SQLite (development)
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web application (Linux server backend, modern browsers frontend)
**Project Type**: Web (monorepo with backend/ and frontend/ directories)
**Performance Goals**: Auth operations < 500ms, API response < 200ms
**Constraints**: Serverless-optimized, stateless JWT tokens, 7-day token expiry
**Scale/Scope**: Multi-user application, ~1000+ users

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| Spec-Driven Development | PASS | Spec completed before plan |
| Modularity and Reusability | PASS | Using existing auth modules |
| Security First | PASS | JWT + bcrypt + user isolation |
| User-Centric Design | PASS | Responsive forms, clear errors |
| Efficiency | PASS | Following Agentic Dev Stack workflow |
| Visual Consistency | PASS | Using existing UI components |

**Constitution Compliance**: All principles satisfied. No violations.

---

## Project Structure

### Documentation (this feature)

```text
specs/005-jwt-auth/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (complete)
├── research.md          # Technical research findings (complete)
├── data-model.md        # Entity definitions (complete)
├── quickstart.md        # Setup guide (to be created)
├── contracts/
│   └── auth-api.yaml    # OpenAPI contract (complete)
├── checklists/
│   └── requirements.md  # Quality checklist (complete)
└── tasks.md             # Implementation tasks (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── auth_routes.py      # Auth endpoints (EXISTS - needs mounting)
│   │   ├── task_routes.py      # Task endpoints (EXISTS - needs protection)
│   │   └── protected_routes.py # New protected task routes
│   ├── auth.py                 # JWT utilities (EXISTS - complete)
│   ├── database/
│   │   └── db.py               # Database connection (EXISTS)
│   ├── models/
│   │   ├── user.py             # User model (EXISTS)
│   │   └── task.py             # Task model (EXISTS)
│   ├── main.py                 # FastAPI app (EXISTS - needs auth routes)
│   └── middleware.py           # Request middleware (EXISTS)
├── tests/
│   ├── test_auth.py            # Auth endpoint tests
│   └── test_protected_tasks.py # Protected route tests
└── .env                        # Environment variables

frontend/
├── src/
│   ├── app/
│   │   ├── signin/
│   │   │   └── page.tsx        # Login page (EXISTS - needs form)
│   │   ├── signup/
│   │   │   └── page.tsx        # Register page (EXISTS - needs form)
│   │   ├── dashboard/
│   │   │   └── page.tsx        # Protected dashboard (EXISTS)
│   │   └── layout.tsx          # Root layout (EXISTS)
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx   # Login form component (NEW)
│   │   │   ├── SignupForm.tsx  # Signup form component (NEW)
│   │   │   └── AuthGuard.tsx   # Route protection (NEW)
│   │   └── ui/                 # UI components (EXISTS)
│   ├── lib/
│   │   ├── auth.ts             # Auth helpers (EXISTS)
│   │   ├── auth-client.ts      # Auth client (EXISTS)
│   │   ├── backend-auth-api.ts # Backend API client (EXISTS)
│   │   ├── better-auth.ts      # Better Auth config (EXISTS)
│   │   └── api.ts              # API utilities (EXISTS)
│   └── middleware.ts           # Next.js middleware (NEW)
├── tests/
│   ├── auth.test.ts            # Auth flow tests
│   └── protected.test.ts       # Route protection tests
└── .env                        # Environment variables (EXISTS)
```

**Structure Decision**: Web application with existing monorepo structure. Minimal new files needed - primarily updating existing code.

---

## Complexity Tracking

> No violations - implementation uses existing patterns.

---

## Implementation Phases

### Phase 1: Backend Auth Route Mounting (Priority: P1)

**Goal**: Enable existing auth endpoints by mounting them in main.py.

**Tasks**:
1. Import auth_routes in `backend/src/main.py`
2. Mount router with `/api` prefix
3. Verify endpoints are accessible via Swagger UI
4. Test registration and login flows

**Files Modified**:
- `backend/src/main.py` - Add router import and mounting

**Estimated Effort**: 1 task, low complexity

**Prompt for Claude Code**:
```
In backend/src/main.py, import auth_routes from .api and include the router:
from .api import auth_routes
app.include_router(auth_routes.router, prefix="/api", tags=["authentication"])
```

---

### Phase 2: Backend Protected Task Routes (Priority: P1)

**Goal**: Create protected versions of task routes that require JWT authentication.

**Tasks**:
1. Create `protected_routes.py` with JWT-protected task endpoints
2. Add `get_current_user` dependency to task routes
3. Filter queries by authenticated user_id
4. Verify task ownership on update/delete operations

**Files Modified**:
- `backend/src/api/protected_routes.py` (NEW)
- `backend/src/main.py` - Mount protected routes

**Key Implementation**:
```python
from ..auth import get_current_user_from_token

@router.get("/{user_id}/tasks")
async def get_user_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    # Verify user_id matches authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    # Query filtered by user_id
    ...
```

**Estimated Effort**: 2 tasks, medium complexity

---

### Phase 3: Frontend Auth Forms (Priority: P1)

**Goal**: Restore functional login and signup forms.

**Tasks**:
1. Create `LoginForm.tsx` component with email/password fields
2. Create `SignupForm.tsx` component with email/password/name fields
3. Update `signin/page.tsx` to use LoginForm
4. Update `signup/page.tsx` to use SignupForm
5. Handle form validation and error display
6. Integrate with `auth-client.ts` for API calls

**Files Modified**:
- `frontend/src/components/auth/LoginForm.tsx` (NEW)
- `frontend/src/components/auth/SignupForm.tsx` (NEW)
- `frontend/src/app/signin/page.tsx` (UPDATE)
- `frontend/src/app/signup/page.tsx` (UPDATE)

**UI Specifications** (from constitution):
- Blue submit button (#007BFF)
- Form fields with Blue border on focus
- Error messages in Red
- Animation: Form fields focus glow

**Estimated Effort**: 4 tasks, medium complexity

---

### Phase 4: Frontend Route Protection (Priority: P2)

**Goal**: Protect dashboard and task routes, redirect unauthenticated users.

**Tasks**:
1. Create `AuthGuard.tsx` wrapper component
2. Create Next.js `middleware.ts` for route protection
3. Update dashboard layout to check authentication
4. Implement redirect to signin for protected routes
5. Redirect authenticated users away from auth pages

**Files Created**:
- `frontend/src/components/auth/AuthGuard.tsx` (NEW)
- `frontend/src/middleware.ts` (NEW)

**Protected Routes**:
- `/dashboard` - Requires auth
- `/tasks` - Requires auth
- `/profile` - Requires auth

**Public Routes**:
- `/` - Landing page
- `/signin` - Login (redirect if authed)
- `/signup` - Register (redirect if authed)

**Estimated Effort**: 3 tasks, medium complexity

---

### Phase 5: Frontend Token Handling (Priority: P2)

**Goal**: Ensure JWT token is included in all API requests.

**Tasks**:
1. Verify `backend-auth-api.ts` token storage works correctly
2. Update API client to include Authorization header
3. Handle 401 responses with redirect to signin
4. Implement token refresh or re-login on expiry

**Files Modified**:
- `frontend/src/lib/backend-auth-api.ts` (VERIFY/UPDATE)
- `frontend/src/lib/api.ts` (UPDATE)

**Estimated Effort**: 2 tasks, low complexity

---

### Phase 6: Session Management (Priority: P2)

**Goal**: Implement logout and session expiration handling.

**Tasks**:
1. Add logout button to navigation/header
2. Clear token on logout
3. Handle expired token gracefully
4. Show "Session expired" message when token invalid

**Files Modified**:
- `frontend/src/components/navigation/Navbar.tsx` (UPDATE)
- `frontend/src/lib/auth-client.ts` (VERIFY)

**Estimated Effort**: 2 tasks, low complexity

---

### Phase 7: Testing & Verification (Priority: P2)

**Goal**: Verify all authentication flows work correctly.

**Tasks**:
1. Test user registration flow end-to-end
2. Test user login flow end-to-end
3. Test protected route access (with/without token)
4. Test user isolation (User A cannot see User B's tasks)
5. Test session expiration handling

**Test Scenarios**:
- Register new user → Verify user created → Login → Access dashboard
- Login with invalid credentials → Verify error message
- Access /dashboard without token → Verify redirect to /signin
- Create task as User A → Login as User B → Verify task not visible

**Estimated Effort**: 5 test scenarios

---

## Environment Configuration

### Backend `.env`

```env
# Database
DATABASE_URL=postgresql://...@neon.tech/neondb

# Authentication
BETTER_AUTH_SECRET=<shared-secret-min-32-chars>
JWT_SECRET_KEY=<same-as-better-auth-secret>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

### Frontend `.env`

```env
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Auth
BETTER_AUTH_SECRET=<same-secret-as-backend>
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

**Critical**: `BETTER_AUTH_SECRET` must be identical in both frontend and backend for JWT verification to work.

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking existing public tasks | Medium | High | Keep public routes during transition |
| CORS issues | Medium | Medium | Verify allowed origins include frontend |
| Token verification failures | Low | High | Test with same secret in both services |
| Database connection issues | Low | High | Use connection pooling, test connectivity |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Registration time | < 30 sec | Form submission to dashboard |
| Login time | < 15 sec | Form submission to dashboard |
| Auth API latency | < 500 ms | Backend response time |
| Token verification | < 100 ms | Middleware execution time |
| User isolation | 100% | No cross-user data leakage |

---

## Next Steps

1. Run `/sp.tasks` to generate detailed task list
2. Implement Phase 1 (Backend Auth Route Mounting) first
3. Verify auth endpoints via Swagger UI before proceeding
4. Implement phases 2-6 in order
5. Run full test suite in Phase 7

---

## Related Documents

- [Specification](./spec.md) - Feature requirements
- [Research](./research.md) - Technical findings
- [Data Model](./data-model.md) - Entity definitions
- [API Contract](./contracts/auth-api.yaml) - OpenAPI specification
- [Constitution](../../.specify/memory/constitution.md) - Project principles
