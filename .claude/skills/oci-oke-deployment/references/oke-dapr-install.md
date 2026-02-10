# Dapr Installation on OKE

## Install Dapr Runtime

```bash
# Add Dapr Helm repo
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Install Dapr
helm install dapr dapr/dapr \
  --namespace dapr-system \
  --create-namespace \
  --wait

# Verify
kubectl get pods -n dapr-system
```

## Configure Dapr Components

```yaml
# Example: Kafka pub/sub for OKE
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: consumerGroup
    value: "todo-app"
```

Apply with: `kubectl apply -f component.yaml`

See cloud-native-blueprints skill for more Dapr components.