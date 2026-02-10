# Redpanda with Dapr Configuration

Complete configuration examples for Redpanda and Dapr integration.

## Redpanda Helm Values

```yaml
# redpanda-production.yaml
statefulset:
  replicas: 3
  updateStrategy:
    type: RollingUpdate

image:
  repository: docker.redpanda.com/redpandadata/redpanda
  tag: v23.3.1

resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 1000m
    memory: 2Gi

storage:
  persistentVolume:
    enabled: true
    size: 50Gi
    storageClass: "oci-bv"

config:
  cluster:
    auto_create_topics_enabled: false
    default_topic_partitions: 3
    default_topic_replications: 3
  node:
    developer_mode: false
  tunable:
    log_segment_size: 536870912
    compacted_log_segment_size: 67108864
```

## Dapr Component Configuration

### Basic Kafka Component

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
    value: "redpanda-0.redpanda.redpanda.svc.cluster.local:9092,redpanda-1.redpanda.redpanda.svc.cluster.local:9092,redpanda-2.redpanda.redpanda.svc.cluster.local:9092"
  - name: consumerGroup
    value: "todo-app"
  - name: clientID
    value: "todo-app"
  - name: authType
    value: "none"
  - name: initialOffset
    value: "newest"
  - name: version
    value: "2.8.0"
```

### Production Kafka Component

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
    value: "redpanda:9092"
  - name: consumerGroup
    value: "todo-app"
  - name: clientID
    value: "todo-app"
  - name: authType
    value: "none"
  - name: initialOffset
    value: "newest"
  - name: version
    value: "2.8.0"
  # Performance tuning
  - name: maxMessageBytes
    value: "1048576"
  - name: consumeRetryInterval
    value: "200ms"
  # Reliability
  - name: acks
    value: "all"
  - name: idempotent
    value: "true"
  - name: retryBackoff
    value: "100ms"
  - name: maxRetries
    value: "3"
scopes:
- todo-api
- todo-worker
- notification-service
```

## Topic Creation

```bash
# Create topics with rpk
kubectl exec -it redpanda-0 -n redpanda -- rpk topic create \
  todo-events \
  --partitions 3 \
  --replicas 3 \
  --config retention.ms=604800000 \
  --config cleanup.policy=delete \
  --config compression.type=lz4
```

## Consumer Configuration

Different consumer groups for different services:

```yaml
# Worker service
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub-worker
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda:9092"
  - name: consumerGroup
    value: "worker-group"
  - name: initialOffset
    value: "earliest"  # Process all messages
scopes:
- todo-worker

# Analytics service
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub-analytics
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda:9092"
  - name: consumerGroup
    value: "analytics-group"
  - name: initialOffset
    value: "newest"  # Only new messages
scopes:
- analytics-service
```

## Monitoring Setup

```yaml
# Prometheus ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: redpanda-metrics
  namespace: redpanda
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: redpanda
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
---
# Grafana Dashboard ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: redpanda-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  redpanda.json: |
    {
      "dashboard": {
        "title": "Redpanda Metrics",
        "panels": [
          {
            "title": "Message Rate",
            "targets": [
              {
                "expr": "rate(redpanda_kafka_request_bytes_total[5m])"
              }
            ]
          }
        ]
      }
    }
```

See SKILL.md for complete details.