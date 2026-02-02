---
id: 4
title: auth-secret-mismatch-fix
stage: general
date_iso: 2026-01-28
model: claude-opus-4-5-20251101
feature: none
branch: 1-auth-refactor
user: user
command: sp.implement ## Error Type Console Error ## Error Message Failed to fetch tasks at TaskService.getAll ... ## Error Type Console Error ## Error Message HTTP error! status: 401 at apiRequest ... user login hai lekin yeh error kyun show horhe hai
labels: [authentication, bug-fix, security]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/.env
tests_yaml: |
  - backend/test_auth_flow.py
---

# PHR: Authentication Secret Mismatch Fix

## Issue Description
Users were experiencing a "401 Unauthorized" error when trying to fetch tasks, even after successful login. The error occurred because JWT token verification was failing between frontend and backend.

## Root Cause Analysis
The BETTER_AUTH_SECRET in the frontend and backend .env files did not match:
- Frontend: BETTER_AUTH_SECRET=1IWUz7oK14TWAsCEy0tdRDIunG9qApgZ
- Backend: BETTER_AUTH_SECRET=rKHdBGVvdlg07AfDebov0ISdhqKn7eBX

When users logged in, the backend created JWT tokens using its secret key, but subsequent API calls failed authentication because the backend couldn't verify tokens signed with a different secret.

## Solution Applied
Updated the backend .env file to use the same BETTER_AUTH_SECRET as the frontend. Also ensured JWT_SECRET_KEY matches for consistency.

## Files Modified
- backend/.env - Updated BETTER_AUTH_SECRET and JWT_SECRET_KEY to match frontend

## Verification
- Verified that login API returns valid JWT token
- Verified that task fetching API now works with 200 status (was 401)
- Confirmed that users can now successfully fetch their tasks after login

## Outcome
The authentication flow is now working correctly. Users can login and successfully fetch their tasks without encountering 401 errors.