# Research: JWT Authentication Implementation

**Feature**: 005-jwt-auth
**Date**: 2026-01-22
**Status**: Complete

## Executive Summary

This research document consolidates findings from exploring the existing codebase to inform the JWT authentication implementation plan. The key finding is that **significant auth infrastructure already exists** in both frontend and backend, but is currently bypassed in favor of "public access" mode. The implementation will primarily involve:
1. Re-enabling and enhancing existing auth components
2. Integrating Better Auth properly with JWT issuance
3. Connecting frontend auth flow to backend JWT verification

---

## 1. Existing Backend Auth Infrastructure

### Decision: Leverage Existing Auth Module
**Rationale**: The backend already has a comprehensive auth implementation in `backend/src/auth.py` that includes JWT creation, password hashing, and token verification.

### Findings

**File: `backend/src/auth.py`**
- JWT implementation using PyJWT library
- Password hashing with bcrypt via `passlib`
- Token expiration configuration (default 30 minutes)
- Uses `BETTER_AUTH_SECRET` or `JWT_SECRET_KEY` from environment
- `get_current_user_from_token()` dependency for protected routes
- `create_access_token()` function for JWT issuance

**File: `backend/src/api/auth_routes.py`**
- `/auth/register` - User registration endpoint (working)
- `/auth/login` - Login endpoint returning JWT token (working)
- `/auth/me` - Get current user endpoint (working)

**File: `backend/src/models/user.py`**
- User model with: id (UUID), email (unique), name, password_hash, created_at, updated_at, is_active
- Already linked to Task model via foreign key

**File: `backend/src/models/task.py`**
- Task model already has `user_id` field with foreign key to User
- Index on `user_id` for query optimization

### Gap Analysis
| Component | Status | Action Needed |
|-----------|--------|---------------|
| User model | Complete | None |
| Task model with user_id | Complete | None |
| JWT creation | Complete | Review expiration settings |
| Password hashing | Complete | None |
| Auth routes | Complete | Register in main.py |
| Token verification | Complete | None |

**Critical Gap**: Auth routes are NOT included in `main.py`. The router is defined but not mounted.

---

## 2. Existing Frontend Auth Infrastructure

### Decision: Refactor Existing Pages from Public Mode
**Rationale**: Frontend has auth pages and API client but currently bypassed with "public access" redirects.

### Findings

**File: `frontend/src/app/signin/page.tsx`**
- Currently shows "Public Access" message and redirects to dashboard
- Needs to be converted back to functional login form

**File: `frontend/src/app/signup/page.tsx`**
- Same as signin - currently bypassed
- Needs functional registration form

**File: `frontend/src/lib/backend-auth-api.ts`**
- Complete auth API client implementation
- `authApi.login()` - Calls `/api/auth/login`
- `authApi.register()` - Calls `/api/auth/register`
- `authApi.getCurrentUser()` - Calls `/api/auth/me`
- Token storage in localStorage
- `getAuthToken()` helper function

**File: `frontend/src/lib/auth-client.ts`**
- Wrapper around `backend-auth-api.ts`
- `signIn.email()`, `signUp.email()`, `signOut()`, `getCurrentUser()`

**File: `frontend/src/lib/better-auth.ts`**
- Better Auth server configuration
- Using SQLite in-memory for development, PostgreSQL for production
- JWT secret configured from `BETTER_AUTH_SECRET`
- Session expiration: 7 days

### Gap Analysis
| Component | Status | Action Needed |
|-----------|--------|---------------|
| Better Auth config | Partial | Enable JWT plugin |
| Auth API client | Complete | Verify endpoint URLs |
| Login page | Bypassed | Restore login form |
| Signup page | Bypassed | Restore registration form |
| Token storage | Complete | Review security |
| Protected routes | Missing | Implement middleware |

---

## 3. Database Configuration

### Decision: Use Existing Neon PostgreSQL Setup
**Rationale**: Database connection and models are properly configured.

### Findings

**File: `backend/src/database/db.py`**
- Async SQLAlchemy engine configured
- Supports both Neon PostgreSQL and SQLite fallback
- Connection pooling optimized for serverless
- `create_db_and_tables()` creates schema on startup

**File: `frontend/.env`**
```
DATABASE_URL='postgresql://neondb_owner:...@ep-wispy-salad-adnoqxlk-pooler.c-2.us-east-1.aws.neon.tech/neondb'
BETTER_AUTH_SECRET=1IWUz7oK14TWAsCEy0tdRDIunG9qApgZ
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

### Schema Status
- `user` table: Created and has required fields
- `task` table: Created with `user_id` foreign key
- Migrations: Alembic configured

---

## 4. API Route Analysis

### Decision: Add Auth Routes and Protect Task Routes
**Rationale**: Task routes exist but are currently public; need to add auth middleware.

### Findings

**Current Route Structure in `main.py`**:
```python
app.include_router(task_routes.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(public_task_routes.router, prefix="/api/public", tags=["public-tasks"])
app.include_router(dashboard_routes.router, prefix="/api", tags=["dashboard"])
```

**Missing**: Auth routes not included!
```python
# Needs to be added:
from .api import auth_routes
app.include_router(auth_routes.router, prefix="/api", tags=["authentication"])
```

**File: `backend/routes/tasks.py`** (Old route file at root)
- Has JWT verification with `get_current_user_id()`
- Has `verify_user_owns_resource()` check
- Uses path `/api/v1/{user_id}/tasks`

**File: `backend/src/api/task_routes.py`** (Current active routes)
- Currently "public access" mode - no auth required
- Uses hardcoded `default_user_id = "public-user"`

---

## 5. Environment Configuration

### Decision: Standardize on BETTER_AUTH_SECRET
**Rationale**: Both frontend and backend should use the same secret for JWT signing/verification.

### Required Environment Variables
| Variable | Frontend | Backend | Purpose |
|----------|----------|---------|---------|
| `BETTER_AUTH_SECRET` | Yes | Yes | JWT signing secret (shared) |
| `DATABASE_URL` | Yes | Yes | Neon PostgreSQL connection |
| `NEXT_PUBLIC_API_URL` | Yes | - | Backend API URL |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | - | Yes | Token expiry (default 30) |

---

## 6. Technology Decisions

### Better Auth Integration
**Decision**: Use Better Auth for frontend session management, but rely on custom JWT for backend API auth.

**Rationale**:
- Better Auth is already installed and configured in frontend
- Backend has robust PyJWT implementation
- Shared secret ensures interoperability

**Implementation**:
1. Better Auth handles user sessions on frontend
2. Better Auth issues JWT tokens (or we use backend `/auth/login`)
3. Frontend stores JWT and sends with API requests
4. Backend verifies JWT using shared secret

### Alternatives Considered
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Better Auth only | Single auth system | Complex backend integration | Rejected |
| Custom JWT both | Full control | Duplicated effort | Rejected |
| **Hybrid approach** | Uses existing code | Slight complexity | **Selected** |

---

## 7. Security Considerations

### Password Storage
- bcrypt with passlib (already implemented)
- No changes needed

### JWT Security
- HS256 algorithm (sufficient for shared secret)
- Expiration enforced
- Consider increasing from 30 min to 7 days to match Better Auth session

### Token Storage
- Currently using localStorage
- Consider httpOnly cookies for enhanced security (Phase 2)

### CORS Configuration
- Already configured in main.py for localhost origins
- Production URLs need to be added

---

## 8. Implementation Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing public access | High | Keep public routes for migration period |
| Token expiration mismatch | Medium | Align Better Auth and backend expiry settings |
| Database schema conflicts | Low | Models already aligned |
| CORS issues | Medium | Test thoroughly with frontend/backend split |

---

## Conclusion

The codebase is well-prepared for JWT authentication. The primary work involves:

1. **Backend**: Mount auth routes in main.py, protect task routes
2. **Frontend**: Restore login/signup forms, add route protection
3. **Integration**: Ensure JWT token flows correctly between systems
4. **Testing**: Verify user isolation and token verification

Estimated complexity: **Medium** - Most infrastructure exists, needs integration work.
