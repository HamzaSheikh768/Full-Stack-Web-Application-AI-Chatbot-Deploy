# ADR-007: Database Connection Strategy with Neon PostgreSQL

## Status
Accepted

## Date
2026-01-26

## Context
The application requires a reliable, scalable database connection strategy that works well with Neon's serverless PostgreSQL offering. Neon's architecture differs from traditional PostgreSQL installations, with connection pooling and serverless compute considerations. The solution must handle connection lifecycle efficiently while maintaining performance and avoiding connection exhaustion, especially in a serverless or containerized deployment environment.

## Decision
We will implement a connection pooling strategy using SQLModel with psycopg2 that includes:

- Configurable pool size (5-10 for dev, 20-50 for production)
- Connection timeout settings (30 seconds)
- Connection lifetime management (1 hour to accommodate Neon's serverless nature)
- Environment-based configuration for different deployment tiers
- Proper connection cleanup and disposal patterns

## Alternatives Considered
1. **Direct Connections Without Pooling**: Simple but leads to connection overhead and potential exhaustion
2. **External Connection Pooler (PgBouncer)**: More complex setup but offers additional features; however, Neon already provides connection pooling
3. **Connection Multiplexing**: Reduces connection count but adds complexity
4. **Persistent Connections**: Reduces overhead but may conflict with Neon's serverless model

## Consequences
### Positive
- Improved performance through connection reuse
- Reduced connection establishment overhead
- Better resource utilization
- Scalability with varying load patterns
- Compatibility with Neon's serverless architecture

### Negative
- Increased complexity in configuration
- Need to monitor and tune pool sizes
- Potential for connection leaks if not properly managed
- Additional configuration parameters to manage
- Possible issues with long-running transactions blocking pool

## References
- specs/1-auth-refactor/plan.md
- specs/1-auth-refactor/research.md
- specs/1-auth-refactor/data-model.md