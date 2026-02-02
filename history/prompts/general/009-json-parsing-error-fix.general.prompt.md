---
id: "009"
title: "JSON Parsing Error Fix"
stage: "general"
date_iso: "2026-01-28"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "1-auth-refactor"
user: "user"
command: "sp.implement"
labels: ["api", "error-handling", "json", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "frontend/src/lib/api.ts"
tests_yaml:
  - "Manual testing of API error responses"
---
# JSON Parsing Error Fix

## Issue
The application was experiencing a SyntaxError: "Unexpected token '<', '<!DOCTYPE '... is not valid JSON" when API endpoints returned HTML error pages instead of JSON responses.

## Root Cause
The frontend's `apiRequest` function was attempting to parse JSON from HTTP responses regardless of content type. When the backend returned HTML error pages (like 500 Internal Server Error pages), the `response.json()` call would fail with a syntax error.

## Solution
Modified the error handling in `frontend/src/lib/api.ts` to:

1. Check the Content-Type header before attempting to parse JSON
2. Only call `response.json()` if the content type is application/json
3. For non-JSON responses, read the text content and provide a meaningful error message
4. Applied the same fix to both the main API request function and the chat API function

## Changes Made
- Updated the error handling in `apiRequest` function to check content type before parsing JSON
- Added proper error logging for debugging non-JSON responses
- Maintained backward compatibility with existing functionality

## Result
- API calls now handle HTML error responses gracefully without crashing
- Better error messages when non-JSON responses are received
- Improved robustness of the frontend API layer