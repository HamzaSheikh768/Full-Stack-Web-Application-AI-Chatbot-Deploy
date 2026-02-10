# Research Findings: Advanced Todo Features

**Date**: 2026-02-08
**Feature**: Advanced Todo Features
**Plan**: [plan.md](./plan.md)

## Overview

This document captures research findings to resolve the unknowns and clarifications identified in the implementation plan for advanced todo features. The research addresses technical decisions, best practices, and integration patterns required for successful implementation.

## R1: Dapr Component Configuration for Kafka/Redpanda

### Decision: Use Dapr Pub/Sub with Apache Kafka
**Rationale**: Kafka provides robust event streaming capabilities that align with the requirement for event-driven architecture. Dapr's Kafka component provides a clean abstraction layer.

**Implementation Details**:
- Dapr Kafka component configuration includes:
  - Broker addresses
  - Consumer group settings
  - Topic configurations
  - Authentication mechanisms

**Alternatives Considered**:
- Redis Streams: Simpler but less scalable for complex event patterns
- Azure Service Bus: Vendor-specific, not aligned with multi-cloud approach
- RabbitMQ: Additional infrastructure complexity

**Configuration Example**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-broker:9092"
  - name: consumerGroup
    value: "todo-consumers"
  - name: authRequired
    value: "false"
```

### Decision: Fallback to Redis Pub/Sub if Kafka unavailable
**Rationale**: In case of Kafka access issues, Redis provides a viable alternative for pub/sub functionality with simpler setup.

## R2: Recurrence Pattern Data Structure

### Decision: Use RFC 5545-inspired JSON structure
**Rationale**: RFC 5545 (iCalendar) provides a well-established standard for recurrence patterns that is both human-readable and machine-processable.

**Structure**:
```json
{
  "type": "daily|weekly|monthly|yearly",
  "interval": 1,
  "days_of_week": ["monday", "wednesday", "friday"],
  "day_of_month": 15,
  "month_of_year": 1,
  "end_date": "2026-12-31",
  "occurrence_count": 10,
  "exceptions": ["2026-11-25"] // holidays or special cases
}
```

**Alternatives Considered**:
- Cron expressions: Less readable, harder to parse for natural language
- Simple enums: Insufficient flexibility for complex patterns
- Custom string format: Would require custom parsing logic

## R3: Notification Service Architecture

### Decision: Event-Driven Notification Service with Dapr
**Rationale**: Maintain loose coupling between task completion and notification delivery using event-driven architecture.

**Architecture**:
- Task service publishes "reminder_due" events to Dapr pub/sub
- Notification service subscribes to reminder events
- Notification service handles delivery via appropriate channels (web push, email, etc.)

**Components**:
- Reminder scheduler (triggers events at appropriate times)
- Notification processor (handles delivery logic)
- Channel adapters (web push, email, SMS)

## R4: Natural Language Date/Time Parsing

### Decision: Use spaCy NLP with duckling for date parsing
**Rationale**: Duckling is specifically designed for parsing time expressions and handles complex natural language date/time expressions effectively.

**Implementation**:
- Use Duckling API for parsing expressions like "next Friday 5pm"
- Preprocess natural language with spaCy for entity recognition
- Map parsed dates to ISO 8601 format for consistency

**Alternative Approaches**:
- Chrono.js: Client-side only, not suitable for server processing
- Custom regex patterns: Too rigid for natural language variations
- OpenAI Functions: Higher cost, less predictable results

## R5: Search Performance Optimization

### Decision: Combine database indexing with full-text search
**Rationale**: For optimal search performance with large datasets, combine traditional indexes with PostgreSQL's full-text search capabilities.

**Strategy**:
- Create GIN indexes on tags and text fields
- Use PostgreSQL's tsvector for full-text search on title/description
- Implement pagination for large result sets
- Consider caching for frequently searched terms

**Database Indexes**:
```sql
CREATE INDEX idx_tasks_title_gin ON tasks USING gin(to_tsvector('english', title));
CREATE INDEX idx_tasks_tags_gin ON tasks USING gin(tags);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_at ON tasks(due_at);
```

## R6: Dapr State Management Patterns

### Decision: Use Dapr State Store for transient conversation data, Neon DB for persistent data
**Rationale**: Dapr State Management provides abstraction and reliability, while Neon DB handles complex queries and relationships.

**Patterns**:
- Short-term conversation state: Dapr State Store
- Persistent task data: Neon PostgreSQL
- User session data: Better Auth JWT with database lookup

## C1: Oracle Cloud Always Free Tier Constraints

### Finding: OKE Always Free Tier Limitations
**Details**:
- Up to 2 OCPU and 15 GB of memory for Worker Nodes
- Up to 2 Load Balancer instances
- 20 GB of Block Volume storage
- 100 GB of Archive Storage
- Standard bandwidth allowance

**Impact on Implementation**:
- Limited to smaller cluster sizes
- May need to optimize resource usage
- Monitor resource consumption closely
- Consider horizontal scaling within limits

## C2: MCP Tool Parameter Limits

### Finding: MCP Tool Parameter Considerations
**Details**:
- MCP tools should avoid excessively large payloads
- Recommended to keep parameter sizes reasonable (under 1MB)
- Complex objects should be stored in database, referenced by ID
- Large arrays (like tags) should have reasonable limits (10 tags as per spec)

## C3: Event Processing SLA Requirements

### Finding: Reasonable SLA for Reminders
**Recommendation**:
- Reminders should trigger within 1 minute of scheduled time
- Recurring task generation should occur within 30 seconds of completion
- Critical events (high-priority reminders) should have higher priority in queue
- Non-critical events can tolerate up to 5-minute delays

## Technology Stack Recommendations

### Dapr Components
1. **pubsub.kafka**: For event streaming
2. **state.postgresql**: For state management (alternative to Neon direct access)
3. **secretstores.kubernetes**: For secret management in OKE
4. **bindings.cron**: For scheduled tasks using Dapr Jobs API

### Event Schema Design
```json
{
  "event_type": "TASK_CREATED | TASK_COMPLETED | REMINDER_DUE | RECURRING_SPAWNED",
  "event_id": "uuid",
  "timestamp": "2026-02-07T10:12:00Z",
  "trace_id": "otel-trace-id",
  "user_id": "user_abc123",
  "correlation_id": "related_event_id",
  "payload": { ... }
}
```

## Implementation Best Practices

### 1. Dapr Integration Patterns
- Use Dapr service invocation for inter-service communication
- Implement proper error handling and retries
- Use Dapr's built-in tracing capabilities
- Follow Dapr's security best practices

### 2. Event-Driven Architecture
- Design idempotent event processors
- Implement dead letter queues for failed events
- Use event versioning for backward compatibility
- Monitor event processing lag

### 3. Performance Optimization
- Implement proper database indexing
- Use pagination for large result sets
- Cache frequently accessed data
- Optimize queries for common access patterns

## Conclusion

This research provides the foundation for implementing the advanced todo features with proper architecture decisions. The solutions address all identified unknowns and provide clear implementation paths for the various components of the system.

Key architectural decisions:
1. Use Dapr as the primary abstraction layer for infrastructure concerns
2. Implement event-driven architecture for recurring tasks and reminders
3. Use RFC 5545-inspired recurrence patterns for flexibility
4. Apply PostgreSQL full-text search for optimal performance
5. Maintain proper separation of concerns between state management systems