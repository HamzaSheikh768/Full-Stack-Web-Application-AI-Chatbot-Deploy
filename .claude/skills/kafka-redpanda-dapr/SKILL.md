---
name: kafka-redpanda-dapr
description: Event streaming infrastructure with Kafka or Redpanda integrated with Dapr for cloud-native applications. Use when implementing event-driven microservices, pub/sub messaging, event streaming, or async communication. Redpanda is recommended as a Kafka-compatible alternative with better performance and lower resource usage. Covers Redpanda deployment, Dapr Kafka component configuration, topic management, and event streaming patterns for Todo applications.
---

# Kafka/Redpanda with Dapr

Event streaming infrastructure for cloud-native applications with Dapr integration.

# Redpanda + Dapr Pub/Sub for Event-Driven Todo

## Recommended for Oracle Cloud

- **Redpanda Serverless** (free tier) — easiest
- **Self-hosted Redpanda** inside OKE — full control, free compute

## Why Redpanda?

Redpanda is recommended over Apache Kafka for cloud-native deployments:

**Advantages**:
- **No JVM** - Lower memory footprint (10x less than Kafka)
- **No Zookeeper** - Simpler architecture and operations
- **Kafka-compatible** - Drop-in replacement, use existing Kafka tools
- **Better performance** - 10x lower latency
- **Cloud-native** - Designed for Kubernetes from the start
- **Simpler ops** - Single binary, easier to manage

**When to use Kafka instead**:
- Existing Kafka infrastructure
- Need Kafka-specific ecosystem tools
- Team has deep Kafka expertise

## Core Workflows

### 1. Deploy Redpanda on Kubernetes

```bash/powershell
# Add Redpanda Helm repo
helm repo add redpanda https://charts.redpanda.com
helm repo update

# Install Redpanda
helm install redpanda redpanda/redpanda \
  --namespace redpanda \
  --create-namespace \
  --set statefulset.replicas=3 \
  --set resources.limits.memory=2Gi \
  --set resources.limits.cpu=1000m

# Verify deployment
kubectl get pods -n redpanda
```

### 2. Configure Dapr Kafka Component

Dapr works with both Kafka and Redpanda (Kafka-compatible):

```yaml
# dapr-kafka-pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  # Redpanda brokers
  - name: brokers
    value: "redpanda-0.redpanda.redpanda.svc.cluster.local:9092,redpanda-1.redpanda.redpanda.svc.cluster.local:9092,redpanda-2.redpanda.redpanda.svc.cluster.local:9092"
  - name: authType
    value: "none"
  - name: consumerGroup
    value: "todo-app-group"
  - name: clientID
    value: "todo-app"
  - name: initialOffset
    value: "newest"
  - name: version
    value: "2.8.0"
scopes:
- todo-api
- todo-worker
- notification-service
```

Apply with: `kubectl apply -f dapr-kafka-pubsub.yaml`

### 3. Create Redpanda Topics

```bash
# Exec into Redpanda pod
kubectl exec -it redpanda-0 -n redpanda -- /bin/bash

# Create topic
rpk topic create todo-events \
  --partitions 3 \
  --replicas 3

# List topics
rpk topic list

# View topic details
rpk topic describe todo-events
```

### 4. Publish Events with Dapr

```python
from dapr.clients import DaprClient

async def publish_task_created(task_data):
    event = {
        "event_type": "task.created",
        "data": task_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    with DaprClient() as client:
        client.publish_event(
            pubsub_name='kafka-pubsub',
            topic_name='todo-events',
            data=event
        )
```

### 5. Subscribe to Events with Dapr

```python
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI

app = FastAPI()
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub_name='kafka-pubsub', topic='todo-events')
async def handle_todo_events(event):
    event_type = event.get('event_type')
    
    if event_type == 'task.created':
        await handle_task_created(event['data'])
    elif event_type == 'task.updated':
        await handle_task_updated(event['data'])
    elif event_type == 'task.completed':
        await handle_task_completed(event['data'])
    
    return {'success': True}
```

## Redpanda Configuration

### Production Configuration

```yaml
# redpanda-values.yaml
statefulset:
  replicas: 3

resources:
  limits:
    cpu: 1000m
    memory: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi

storage:
  persistentVolume:
    enabled: true
    size: 20Gi
    storageClass: "oci-bv"  # Or do-block-storage, etc.

config:
  cluster:
    auto_create_topics_enabled: false
  node:
    developer_mode: false
```

Deploy with:

```bash
helm install redpanda redpanda/redpanda \
  -f redpanda-values.yaml \
  --namespace redpanda \
  --create-namespace
```

### Topic Configuration

Best practices for topic configuration:

```bash
# Create topic with appropriate partitions and replication
rpk topic create todo-events \
  --partitions 3 \
  --replicas 3 \
  --config retention.ms=604800000 \  # 7 days
  --config cleanup.policy=delete
```

**Partitions**: Number of parallel consumers (3-6 for typical workloads)
**Replicas**: Fault tolerance (3 for production)
**Retention**: How long to keep messages (7 days default)

## Event Streaming Patterns

### Pattern 1: Pub/Sub Messaging

Simple publish-subscribe:

```python
# Publisher (API Service)
publish_event('kafka-pubsub', 'todo-events', {
    'event_type': 'task.created',
    'data': task_data
})

# Subscriber (Worker Service)
@subscribe('kafka-pubsub', 'todo-events')
async def process_event(event):
    await process_task(event['data'])
```

### Pattern 2: Event Sourcing

Use Redpanda as event store:

```python
# Append event to stream
await append_event({
    'event_id': uuid4(),
    'event_type': 'task.created',
    'aggregate_id': task_id,
    'data': task_data,
    'timestamp': datetime.utcnow()
})

# Rebuild state from events
async def rebuild_task_state(task_id):
    events = await get_events_for_aggregate(task_id)
    
    state = {}
    for event in events:
        state = apply_event(state, event)
    
    return state
```

### Pattern 3: CQRS

Separate read and write models:

```python
# Write side - publish events
@app.post('/tasks')
async def create_task(task: TaskCreate):
    # Save to write DB
    task_id = await write_db.save(task)
    
    # Publish event
    publish_event('task.created', {'task_id': task_id, **task.dict()})
    
    return {'id': task_id}

# Read side - consume events and update read model
@subscribe('kafka-pubsub', 'todo-events')
async def update_read_model(event):
    if event['event_type'] == 'task.created':
        # Update read model (e.g., Redis or Elasticsearch)
        await read_db.index_task(event['data'])
```

## Consumer Groups

Multiple services consuming same events:

```yaml
# Worker service consumer group
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub-worker
spec:
  type: pubsub.kafka
  metadata:
  - name: consumerGroup
    value: "worker-group"
---
# Analytics service consumer group
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub-analytics
spec:
  type: pubsub.kafka
  metadata:
  - name: consumerGroup
    value: "analytics-group"
```

Each consumer group processes all messages independently.

## Monitoring Redpanda

### Metrics

Redpanda exposes Prometheus metrics:

```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: redpanda
  namespace: redpanda
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: redpanda
  endpoints:
  - port: metrics
    interval: 30s
```

### Consumer Lag

Check consumer lag:

```bash
rpk group describe todo-app-group
```

## Reference Files

- `redpanda-dapr-config.md` - Detailed configuration examples

## Integration with Other Skills

- Use `cloud-native-blueprints` for event schemas
- Use `dapr-jobs-reminders` for scheduled events
- Use `oci-oke-deployment` for OKE deployment

## Best Practices

1. **Use Redpanda over Kafka** - Better for cloud-native
2. **Configure appropriate partitions** - 3-6 for typical workloads
3. **Use consumer groups** - Parallel processing
4. **Set retention policies** - Don't store forever
5. **Monitor consumer lag** - Detect processing issues
6. **Use idempotent consumers** - Handle duplicate messages
7. **Version event schemas** - Enable evolution
8. **Enable compression** - Reduce storage and network
9. **Configure replication** - 3 replicas for production
10. **Use Dapr for abstraction** - Easy to switch brokers