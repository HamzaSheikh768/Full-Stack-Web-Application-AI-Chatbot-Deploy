---
id: "010"
title: "Database Channel Binding Fix"
stage: "general"
date_iso: "2026-01-28"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "1-auth-refactor"
user: "user"
command: "sp.implement"
labels: ["database", "connection", "channel-binding", "psycopg3"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/src/database/db.py"
  - "backend/src/api/auth_routes.py"
  - "frontend/src/contexts/AuthContext.tsx"
  - "frontend/src/components/navigation/Navbar.tsx"
  - "frontend/src/app/layout.tsx"
  - "frontend/src/components/auth/LoginForm.tsx"
  - "frontend/src/components/auth/SignupForm.tsx"
  - "frontend/src/app/auth/login/page.tsx"
  - "frontend/src/app/auth/signup/page.tsx"
tests_yaml:
  - "Manual testing of database connection"
  - "Manual testing of authentication flows"
---
# Database Channel Binding Parameter Fix

## Issue
The application was failing to start with a TypeError: "connect() got an unexpected keyword argument 'channel_binding'" when trying to connect to the Neon PostgreSQL database. This occurred because the connection string included `channel_binding=require` which is not supported by the asyncpg/psycopg3 drivers.

## Root Cause
The database connection string in the .env file contained `channel_binding=require` parameter, which is not supported by the PostgreSQL connector being used. This caused the SQLAlchemy engine to fail during startup.

## Solution
Modified the database connection logic in `backend/src/database/db.py` to:

1. Detect and remove the `channel_binding` parameter from the connection string before creating the engine
2. Properly handle URL query separators after parameter removal
3. Maintain all other connection parameters including sslmode=require
4. Updated authentication components to work with the new sync database approach
5. Created proper auth context and routes to handle user authentication

## Changes Made
- Updated database connection logic to strip unsupported channel_binding parameter
- Created authentication context provider for frontend state management
- Implemented login and signup forms with proper error handling
- Updated navbar to include auth functionality
- Created proper auth routes in the backend

## Result
- Application now starts successfully without database connection errors
- Authentication flows work properly with token management
- Channel binding parameter is safely removed from connection string
- All authentication endpoints are properly implemented and secured