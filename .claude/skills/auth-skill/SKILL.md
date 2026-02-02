---
name: auth-skill
description: Implements secure user authentication features including signup, signin, password hashing with bcrypt, JWT token generation and validation, and integration with enhanced auth libraries or practices. Use this skill when developing or troubleshooting authentication flows in web applications, APIs, or backend services to ensure secure user management.
---

# Implementing Authentication

## Overview
This skill provides step-by-step guidance for building authentication systems. It assumes basic knowledge of programming languages like Node.js or Python, databases (e.g., MongoDB, SQL), and HTTP concepts. Focus on security best practices: always hash passwords, use secure tokens, and validate inputs.

Key components:
- **Signup**: User registration with email/password validation and storage.
- **Signin**: User login with credential verification.
- **Password Hashing**: Secure one-way hashing to protect passwords.
- **JWT Tokens**: Generation, signing, and verification for session management.
- **Better Auth Integration**: Enhanced practices or library integrations (e.g., using libraries like bcrypt, jsonwebtoken, or frameworks for improved security and scalability).

Use progressive disclosure: Start with high-level steps, then drill down if needed. For code examples, adapt to the target language/framework specified by the user.

## General Workflow
1. **Assess Requirements**: Determine language (e.g., JS, Python), database, and any existing auth setup.
2. **Setup Dependencies**: Install necessary libraries (e.g., bcrypt, jsonwebtoken for Node.js; passlib, pyjwt for Python).
3. **Implement Core Features**: Follow sections below.
4. **Test and Secure**: Validate with unit tests, handle errors, and apply rate limiting/CSRF protection.
5. **Integrate**: Combine into a cohesive system.

Checklist:
- Inputs sanitized?
- Errors handled gracefully (e.g., no leaks of sensitive info)?
- Tokens expire appropriately?
- Compliance with standards (e.g., OWASP guidelines)?

## Signup Workflow
Step-by-step:
1. Receive user data (email, password, optional: name).
2. Validate inputs: Check email format, password strength (min length 8, mix of chars).
3. Hash password (see Password Hashing section).
4. Check for existing user (query DB by email).
5. If unique, store user record in DB.
6. Generate JWT (see JWT section) and return it.
7. Handle errors: Duplicate email → 409 Conflict; Validation fail → 400 Bad Request.

Example (Node.js input → output):
Input: POST /signup { "email": "user@example.com", "password": "StrongPass123" }

Output: { "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "user": { "id": "123", "email": "user@example.com" } } (HTTP 201)

Error Output: { "error": "Email already in use" } (HTTP 409)

## Signin Workflow
Step-by-step:
1. Receive credentials (email, password).
2. Validate inputs: Ensure fields present.
3. Fetch user from DB by email.
4. If found, compare hashed password (see Password Hashing).
5. If match, generate JWT.
6. Return token.
7. Handle errors: Invalid creds → 401 Unauthorized; User not found → 404 Not Found.

Example (Python input → output):
Input: POST /signin { "email": "user@example.com", "password": "StrongPass123" }

Output: { "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9...", "message": "Login successful" } (HTTP 200)

Error Output: { "error": "Invalid credentials" } (HTTP 401)

## Password Hashing
Use bcrypt for salting and hashing. Avoid MD5/SHA1.

Step-by-step:
1. Install library (e.g., npm install bcrypt; pip install bcrypt).
2. Generate salt (rounds: 12 recommended).
3. Hash password with salt.
4. Store hashed value in DB.
5. For verification: Hash input and compare to stored hash.

Example Code Template (Node.js):
```javascript
const bcrypt = require('bcrypt');
async function hashPassword(password) {
  const salt = await bcrypt.genSalt(12);
  return await bcrypt.hash(password, salt);
}
async function verifyPassword(input, storedHash) {
  return await bcrypt.compare(input, storedHash);
}
```

Validation Loop: If hashing fails (e.g., weak password), prompt for stronger input.

## JWT Tokens
Use JSON Web Tokens for stateless auth. Sign with secret key.

Step-by-step:
1. Install library (e.g., npm install jsonwebtoken; pip install pyjwt).
2. Define secret (env var: process.env.JWT_SECRET).
3. Generate: Include payload (user ID, roles, exp: 1h).
4. Sign token.
5. Verify: On protected routes, decode and check signature/expiry.
6. Handle errors: Invalid token → 403 Forbidden.

Example Code Template (Python):
```python
import jwt
SECRET = 'your-secret-key'
def generate_token(user_id):
  payload = {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(hours=1)}
  return jwt.encode(payload, SECRET, algorithm='HS256')
def verify_token(token):
  try:
    return jwt.decode(token, SECRET, algorithms=['HS256'])
  except jwt.ExpiredSignatureError:
    raise ValueError('Token expired')
  except jwt.InvalidTokenError:
    raise ValueError('Invalid token')
```

## Better Auth Integration
Enhance basic auth with libraries/frameworks for scalability (e.g., integrate with Auth0, Firebase Auth, or custom "better-auth" patterns like multi-factor auth, OAuth).

Step-by-step:
1. Evaluate current setup: Identify pain points (e.g., session management).
2. Choose integration: For Node.js, use Passport.js; for better security, add MFA via TOTP.
3. Implement wrappers: Around signup/signin to include OAuth flows.
4. Test interoperability: Ensure JWT works with external providers.
5. Apply best practices: Use HTTPS, rotate secrets, audit logs.

Example: Integrating OAuth2.
- Redirect to provider (e.g., Google).
- Callback: Exchange code for token, link to local user.

See REFERENCE.md for library docs and OWASP resources.

## Error Handling
- Use try-catch for operations.
- Log errors internally, return generic messages to user.
- Rate limit attempts (e.g., 5 per minute).

## Output Format Template
For code generation requests:
```json
{
  "feature": "signup",
  "language": "node.js",
  "code": "// Full function here",
  "explanation": "Step-by-step rationale"
}
```

## Examples
Input: "Generate signup code in Node.js"
Output: [Follow Signup Workflow, provide code template]

Input: "How to verify JWT in Python?"
Output: [JWT verify function with explanation]

For complex queries, loop back: Ask for clarification on language/DB if unspecified.
```
