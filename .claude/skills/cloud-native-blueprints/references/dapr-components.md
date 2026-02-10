# Dapr Components Reference

Complete catalog of Dapr components with configuration patterns for cloud-native applications.

## State Management Components

### Redis State Store

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.default.svc.cluster.local:6379
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key: password
  - name: enableTLS
    value: "false"
  - name: actorStateStore
    value: "true"
```

**Use cases**: Session storage, distributed cache, actor state

### PostgreSQL State Store

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgresql-statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: postgres-secret
      key: connectionString
  - name: tableName
    value: state
  - name: keyLength
    value: "200"
```

**Use cases**: Persistent state, transactional data, SQL querying

## Pub/Sub Components

### Kafka Pub/Sub

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-0.kafka-headless.kafka.svc.cluster.local:9092,kafka-1.kafka-headless.kafka.svc.cluster.local:9092"
  - name: authType
    value: "none"
  - name: consumerGroup
    value: "todo-app-group"
  - name: clientID
    value: "todo-app"
  - name: initialOffset
    value: "newest"
  - name: maxMessageBytes
    value: "1048576"
  - name: version
    value: "2.8.0"
scopes:
- todo-api
- todo-worker
- notification-service
```

**Use cases**: Event streaming, async messaging, microservices communication

### Redpanda Pub/Sub

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: redpanda-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda-0.redpanda.redpanda.svc.cluster.local:9092"
  - name: authType
    value: "none"
  - name: consumerGroup
    value: "todo-app-group"
  - name: initialOffset
    value: "newest"
```

**Use cases**: Kafka-compatible streaming with better performance, lower resource usage

### Redis Pub/Sub

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: redis-pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.default.svc.cluster.local:6379
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key: password
  - name: consumerID
    value: "todo-app-consumer"
```

**Use cases**: Simple pub/sub, low latency messaging, caching + messaging

## Service Invocation

### HTTP Service Invocation

Dapr automatically handles service discovery and invocation:

```python
# Python SDK example
from dapr.clients import DaprClient

with DaprClient() as client:
    # Invoke another service
    response = client.invoke_method(
        app_id='notification-service',
        method_name='send-notification',
        data={'message': 'Task created'},
        http_verb='POST'
    )
```

**Configuration** (automatic, no component needed):

```yaml
# In deployment annotations
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "todo-api"
  dapr.io/app-port: "8000"
```

## Bindings

### Cron Binding (Input)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: daily-backup-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "0 2 * * *"  # 2 AM daily
  - name: direction
    value: "input"
```

**Use cases**: Scheduled tasks, periodic jobs, batch processing

### AWS S3 Binding (Output)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: s3-backup
spec:
  type: bindings.aws.s3
  version: v1
  metadata:
  - name: bucket
    value: "todo-backups"
  - name: region
    value: "us-east-1"
  - name: accessKey
    secretKeyRef:
      name: aws-secret
      key: accessKey
  - name: secretKey
    secretKeyRef:
      name: aws-secret
      key: secretKey
  - name: direction
    value: "output"
```

**Use cases**: File uploads, backups, archiving

## Configuration Store

### Redis Configuration Store

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: configstore
spec:
  type: configuration.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.default.svc.cluster.local:6379
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key: password
```

**Use cases**: Feature flags, dynamic configuration, A/B testing

## Resiliency Policies

### Retry Policy

```yaml
apiVersion: dapr.io/v1alpha1
kind: Resiliency
metadata:
  name: default-resiliency
spec:
  policies:
    retries:
      DefaultRetryPolicy:
        policy: constant
        duration: 5s
        maxRetries: 3
      
      ExponentialBackoff:
        policy: exponential
        maxInterval: 60s
        maxRetries: 5
    
    timeouts:
      DefaultTimeout:
        timeout: 30s
      
      LongTimeout:
        timeout: 300s
    
    circuitBreakers:
      DefaultCircuitBreaker:
        maxRequests: 1
        interval: 30s
        timeout: 60s
        trip: consecutiveFailures > 5
  
  targets:
    apps:
      notification-service:
        retry: DefaultRetryPolicy
        timeout: DefaultTimeout
        circuitBreaker: DefaultCircuitBreaker
    
    components:
      statestore:
        outbound:
          retry: ExponentialBackoff
          timeout: LongTimeout
```

**Use cases**: Service resilience, failure handling, circuit breaking

## Secret Stores

### Kubernetes Secret Store

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

**Use cases**: Access Kubernetes secrets from Dapr applications

### HashiCorp Vault

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: vault-secrets
spec:
  type: secretstores.hashicorp.vault
  version: v1
  metadata:
  - name: vaultAddr
    value: "http://vault.vault.svc.cluster.local:8200"
  - name: vaultToken
    secretKeyRef:
      name: vault-token
      key: token
  - name: enginePath
    value: "secret"
```

**Use cases**: Centralized secret management, rotation, auditing

## Lock Component

### Redis Lock

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: distributed-lock
spec:
  type: lock.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.default.svc.cluster.local:6379
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key: password
```

**Use cases**: Distributed locks, leader election, singleton processing

## Workflow Component (Alpha)

### Dapr Workflow

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: dapr-workflow
spec:
  type: workflow.dapr
  version: v1
  metadata: []
```

**Use cases**: Long-running processes, orchestration, saga patterns

## Component Scopes

Restrict components to specific apps:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: sensitive-statestore
spec:
  type: state.redis
  version: v1
  metadata: [...]
scopes:
- admin-service
- audit-service
# Not accessible by other apps
```

## Best Practices

### 1. Use Secrets for Sensitive Data

```yaml
metadata:
- name: password
  secretKeyRef:
    name: redis-secret
    key: password
```

### 2. Configure Resiliency Policies

Always configure retries, timeouts, and circuit breakers for production.

### 3. Scope Components Appropriately

Limit component access to only the apps that need them.

### 4. Version Your Components

Use version-specific configurations for compatibility.

### 5. Monitor Component Health

Check Dapr sidecar logs for component initialization:

```bash
kubectl logs <pod> -c daprd
```

## Common Patterns

### Pattern 1: Event-Driven Microservices

```
API Service (Dapr) → Kafka Pub/Sub → Worker Services (Dapr)
      ↓                                      ↓
  Redis State                           PostgreSQL State
```

**Components needed**:
- kafka-pubsub (pub/sub)
- redis-statestore (API caching)
- postgresql-statestore (persistent data)

### Pattern 2: CQRS with Event Sourcing

```
Command Handler → Events → Kafka → Event Processors
      ↓                              ↓
  Write DB                        Read Models
```

**Components needed**:
- kafka-pubsub (events)
- postgresql-statestore (write model)
- redis-statestore (read models)

### Pattern 3: Scheduled Background Jobs

```
Cron Binding → Job Processor (Dapr) → S3 Binding
                    ↓
                State Store
```

**Components needed**:
- cron-binding (scheduler)
- s3-binding (output)
- statestore (job state)

## Troubleshooting

### Component Not Loading

Check Dapr sidecar logs:

```bash
kubectl logs <pod> -c daprd | grep "component loaded"
```

### Connection Issues

Verify network connectivity to backend (Redis, Kafka, etc.):

```bash
kubectl exec <pod> -c daprd -- wget -O- http://redis:6379
```

### Secret Not Found

Ensure secret exists and is in the same namespace:

```bash
kubectl get secret redis-secret
```

## Component Compatibility Matrix

| Component Type | Kubernetes | Docker | Azure | AWS | GCP |
|---------------|-----------|--------|-------|-----|-----|
| State (Redis) | ✅ | ✅ | ✅ | ✅ | ✅ |
| State (PostgreSQL) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pub/Sub (Kafka) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pub/Sub (Redis) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Bindings (Cron) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Secrets (K8s) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Secrets (Vault) | ✅ | ✅ | ✅ | ✅ | ✅ |

For complete component catalog, see: https://docs.dapr.io/reference/components-reference/