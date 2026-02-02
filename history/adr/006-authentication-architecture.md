# ADR-006: Authentication Architecture with JWT and Refresh Tokens

## Status
Accepted

## Date
2026-01-26

## Context
The system requires a secure, stateless authentication mechanism that supports user registration, login, and session management. The solution must be scalable, secure, and provide a good user experience. With the rise of distributed systems and the need for mobile-friendly authentication, traditional session-based authentication has limitations. We need to implement a token-based solution that addresses security concerns like XSS and CSRF while supporting a modern SPA architecture.

## Decision
We will implement a JWT (JSON Web Token) based authentication system with refresh tokens, featuring:

- Short-lived access tokens (15 minutes) with longer-lived refresh tokens (7 days)
- bcrypt for password hashing with configurable salt rounds
- Email verification during registration
- Password reset functionality via email
- Account lockout mechanism after 5 failed attempts for 15 minutes
- SMTP-based email service for verification and recovery

## Alternatives Considered
1. **Traditional Session-Based Authentication**: Simpler to implement but requires server-side session storage, making it harder to scale and unsuitable for microservices
2. **Long-Lived JWT Tokens**: Reduces server requests but increases security risk if tokens are compromised
3. **OAuth 2.0 with PKCE**: More complex but provides better security for public clients; however, adds external dependencies
4. **Cookie-Based JWT Storage**: Safer against XSS but vulnerable to CSRF; requires additional CSRF protection

## Consequences
### Positive
- Stateless authentication scales well with microservices
- Short-lived access tokens minimize security exposure if compromised
- Refresh tokens provide good user experience without frequent re-authentication
- Built-in expiration reduces need for server-side session management
- Email verification prevents spam registrations

### Negative
- More complex than session-based authentication
- Potential for token theft requires additional security measures
- Refresh token rotation adds complexity
- Need for secure storage of refresh tokens on client devices
- Additional complexity for account lockout implementation

## References
- specs/1-auth-refactor/plan.md
- specs/1-auth-refactor/research.md
- specs/1-auth-refactor/data-model.md
- specs/1-auth-refactor/contracts/auth-api-contract.yaml
- history/adr/002-jwt-authentication-strategy.md (extends and refines JWT approach)
- history/adr/005-security-and-rate-limiting.md (complements security measures)