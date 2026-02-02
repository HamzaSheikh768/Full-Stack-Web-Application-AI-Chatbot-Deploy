# Quickstart: JWT Authentication Implementation

**Feature**: 005-jwt-auth
**Date**: 2026-01-22

## Prerequisites

Before implementing JWT authentication, ensure:

1. **Backend Running**: FastAPI server accessible at `http://localhost:8000`
2. **Frontend Running**: Next.js app accessible at `http://localhost:3000`
3. **Database Connected**: Neon PostgreSQL or SQLite configured
4. **Environment Variables**: Both `.env` files properly configured

## Environment Setup

### Backend (`backend/.env`)

```env
# Database (use your Neon connection string)
DATABASE_URL=postgresql://user:pass@host/db

# Authentication - MUST MATCH FRONTEND
BETTER_AUTH_SECRET=your-secure-secret-min-32-characters
JWT_SECRET_KEY=your-secure-secret-min-32-characters
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### Frontend (`frontend/.env`)

```env
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Auth - MUST MATCH BACKEND
BETTER_AUTH_SECRET=your-secure-secret-min-32-characters
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## Quick Verification Steps

### Step 1: Verify Backend Auth Routes

```bash
# Start backend
cd backend
uvicorn src.main:app --reload --port 8000

# Open Swagger UI
# Navigate to: http://localhost:8000/docs
# Look for: /api/auth/register, /api/auth/login, /api/auth/me
```

### Step 2: Test Registration

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'
```

Expected response:
```json
{"id":"uuid-here","email":"test@example.com","name":"Test User"}
```

### Step 3: Test Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Expected response:
```json
{"access_token":"eyJ...","token_type":"bearer"}
```

### Step 4: Test Protected Route

```bash
# Use the access_token from login
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <your-access-token>"
```

### Step 5: Verify Frontend

```bash
# Start frontend
cd frontend
npm run dev

# Navigate to:
# - http://localhost:3000/signup - Should show registration form
# - http://localhost:3000/signin - Should show login form
# - http://localhost:3000/dashboard - Should redirect to signin if not logged in
```

## Common Issues & Solutions

### Issue: "User with this email already exists"
**Solution**: Use a different email or clear the database

### Issue: 401 Unauthorized on protected routes
**Solution**:
1. Verify token is being sent in Authorization header
2. Check BETTER_AUTH_SECRET matches in both services
3. Verify token hasn't expired

### Issue: CORS errors
**Solution**: Verify `http://localhost:3000` is in the allowed origins in `backend/src/main.py`

### Issue: "Could not validate credentials"
**Solution**:
1. Verify JWT_SECRET_KEY matches BETTER_AUTH_SECRET
2. Check token format: `Bearer <token>`
3. Verify token hasn't been modified

## Testing User Isolation

```bash
# Create User A
curl -X POST http://localhost:8000/api/auth/register \
  -d '{"email":"usera@test.com","password":"password123","name":"User A"}'

# Login as User A, get token
TOKEN_A=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -d '{"email":"usera@test.com","password":"password123"}' | jq -r '.access_token')

# Create task as User A
curl -X POST "http://localhost:8000/api/$USER_A_ID/tasks" \
  -H "Authorization: Bearer $TOKEN_A" \
  -d '{"title":"User A Task"}'

# Create User B and login
# Try to access User A's tasks with User B's token
# Should receive 403 Forbidden
```

## Next Steps

After verification:
1. Run `/sp.tasks` to generate implementation task list
2. Follow tasks in priority order (P1 first)
3. Test each phase before moving to next
