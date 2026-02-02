# ADR-008: Rate Limiting and Security Approach

## Status
Accepted

## Date
2026-01-26

## Context
The authentication system requires protection against various attack vectors including brute force, credential stuffing, and denial of service attacks. With increasing security threats targeting authentication endpoints, we need a robust rate limiting strategy that balances user experience with security. The solution must work in a distributed environment and be configurable for different types of rate limits (per IP, per account).

## Decision
We will implement a Redis-based rate limiting system that includes:

- Per-IP and per-account rate limiting for authentication endpoints
- Account lockout after 5 failed login attempts for 15 minutes
- Distributed rate limiting across multiple application instances
- Configurable limits based on environment (development vs production)
- Separate counters for IP and account to prevent circumvention
- Support for temporary lockouts rather than permanent bans

## Alternatives Considered
1. **In-Memory Rate Limiting**: Faster but not distributed; resets on application restart
2. **Database-Based Rate Limiting**: Persistent but adds database load and latency
3. **IP-Only Rate Limiting**: Simpler but allows account-specific attacks
4. **Account-Only Rate Limiting**: Allows IP-based attacks
5. **Fixed Window Counters**: Simpler but allows traffic bursts at window boundaries
6. **Sliding Window Log**: More accurate but more complex to implement

## Consequences
### Positive
- Distributed consistency across multiple instances
- Efficient rate limiting with low latency
- Protection against brute force and credential stuffing attacks
- Configurable limits for different environments
- Separate IP and account tracking prevents circumvention
- Temporary lockouts balance security with user experience

### Negative
- Additional dependency on Redis infrastructure
- Complexity in deployment and maintenance
- Potential for Redis becoming a single point of failure
- Memory usage for storing rate limit counters
- Complexity in monitoring and tuning rate limits
- Potential for legitimate users to be locked out

## References
- specs/1-auth-refactor/plan.md
- specs/1-auth-refactor/research.md
- specs/1-auth-refactor/data-model.md
- history/adr/005-security-and-rate-limiting.md (extends rate limiting approach)