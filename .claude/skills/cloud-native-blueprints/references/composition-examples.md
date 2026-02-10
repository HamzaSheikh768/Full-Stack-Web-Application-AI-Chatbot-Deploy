# Multi-Service Composition Examples

Complete examples for deploying multi-service cloud-native applications.

## Example 1: Todo App Microservices Stack

Complete Todo application with event-driven architecture.

### Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Frontend  │────▶│   API        │────▶│   Worker        │
│   (Next.js) │     │   (FastAPI)  │     │   (Python)      │
└─────────────┘     └──────┬───────┘     └────────┬────────┘
                           │                      │
                           ▼                      ▼
                    ┌─────────────┐      ┌────────────────┐
                    │  PostgreSQL │      │  Kafka/Redpanda│
                    │  (State)    │      │  (Events)      │
                    └─────────────┘      └────────────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │  Notification   │
                                        │  Service        │
                                        └─────────────────┘
```

### Kustomization File

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: todo-app

resources:
  - namespace.yaml
  - postgresql.yaml
  - redpanda.yaml
  - dapr-components/
  - frontend-deployment.yaml
  - api-deployment.yaml
  - worker-deployment.yaml
  - notification-deployment.yaml
  - ingress.yaml

configMapGenerator:
  - name: app-config
    literals:
      - APP_ENV=production
      - LOG_LEVEL=info
      - ENABLE_METRICS=true

secretGenerator:
  - name: app-secrets
    envs:
      - secrets.env

images:
  - name: todo-frontend
    newName: registry.digitalocean.com/todo-registry/frontend
    newTag: v1.0.0
  - name: todo-api
    newName: registry.digitalocean.com/todo-registry/api
    newTag: v1.0.0
  - name: todo-worker
    newName: registry.digitalocean.com/todo-registry/worker
    newTag: v1.0.0
  - name: notification-service
    newName: registry.digitalocean.com/todo-registry/notification
    newTag: v1.0.0
```

### Namespace

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
  labels:
    app: todo-app
    environment: production
```

### PostgreSQL Deployment

```yaml
# postgresql.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgresql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: do-block-storage
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: tododb
        - name: POSTGRES_USER
          value: todouser
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_PASSWORD
        volumeMounts:
        - name: postgresql-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: postgresql-storage
        persistentVolumeClaim:
          claimName: postgresql-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgresql
spec:
  selector:
    app: postgresql
  ports:
  - port: 5432
    targetPort: 5432
```

### Redpanda Deployment

```yaml
# redpanda.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redpanda
spec:
  serviceName: redpanda-headless
  replicas: 3
  selector:
    matchLabels:
      app: redpanda
  template:
    metadata:
      labels:
        app: redpanda
    spec:
      containers:
      - name: redpanda
        image: docker.redpanda.com/redpandadata/redpanda:v23.3.1
        command:
        - /usr/bin/rpk
        - redpanda
        - start
        - --smp=1
        - --memory=1G
        - --reserve-memory=0M
        - --overprovisioned
        - --node-id=$(POD_NAME##*-)
        - --kafka-addr=PLAINTEXT://0.0.0.0:9092
        - --advertise-kafka-addr=PLAINTEXT://$(POD_NAME).redpanda-headless.$(NAMESPACE).svc.cluster.local:9092
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        ports:
        - containerPort: 9092
          name: kafka
        - containerPort: 8082
          name: admin
        - containerPort: 9644
          name: metrics
        volumeMounts:
        - name: datadir
          mountPath: /var/lib/redpanda/data
        resources:
          requests:
            cpu: 100m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 2Gi
  volumeClaimTemplates:
  - metadata:
      name: datadir
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: redpanda-headless
spec:
  clusterIP: None
  selector:
    app: redpanda
  ports:
  - port: 9092
    name: kafka
  - port: 8082
    name: admin
  - port: 9644
    name: metrics
---
apiVersion: v1
kind: Service
metadata:
  name: redpanda
spec:
  selector:
    app: redpanda
  ports:
  - port: 9092
    name: kafka
  - port: 8082
    name: admin
```

### Dapr Components

```yaml
# dapr-components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: redpanda-0.redpanda-headless.todo-app.svc.cluster.local:9092,redpanda-1.redpanda-headless.todo-app.svc.cluster.local:9092
  - name: consumerGroup
    value: todo-app-group
  - name: clientID
    value: todo-app
  - name: initialOffset
    value: newest
scopes:
- todo-api
- todo-worker
- notification-service
---
# dapr-components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: app-secrets
      key: DB_CONNECTION_STRING
scopes:
- todo-api
```

### API Deployment

```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todo-api
  template:
    metadata:
      labels:
        app: todo-api
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-api"
        dapr.io/app-port: "8000"
        dapr.io/enable-metrics: "true"
        dapr.io/metrics-port: "9090"
    spec:
      containers:
      - name: todo-api
        image: todo-api
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_CONNECTION_STRING
        - name: PORT
          value: "8000"
        envFrom:
        - configMapRef:
            name: app-config
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: todo-api
spec:
  selector:
    app: todo-api
  ports:
  - port: 80
    targetPort: 8000
```

### Worker Deployment

```yaml
# worker-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-worker
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-worker
  template:
    metadata:
      labels:
        app: todo-worker
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-worker"
        dapr.io/app-port: "8001"
    spec:
      containers:
      - name: todo-worker
        image: todo-worker
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_CONNECTION_STRING
        envFrom:
        - configMapRef:
            name: app-config
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 200m
            memory: 256Mi
```

### Notification Service

```yaml
# notification-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: notification-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: notification-service
  template:
    metadata:
      labels:
        app: notification-service
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "notification-service"
        dapr.io/app-port: "8002"
    spec:
      containers:
      - name: notification-service
        image: notification-service
        ports:
        - containerPort: 8002
        env:
        - name: SMTP_HOST
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: SMTP_HOST
        - name: SMTP_USER
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: SMTP_USER
        - name: SMTP_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: SMTP_PASSWORD
        envFrom:
        - configMapRef:
            name: app-config
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 200m
            memory: 256Mi
```

### Frontend Deployment

```yaml
# frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
    spec:
      containers:
      - name: todo-frontend
        image: todo-frontend
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://todo-api.todo-app.svc.cluster.local"
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
spec:
  selector:
    app: todo-frontend
  ports:
  - port: 80
    targetPort: 3000
```

### Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-app-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - todo.example.com
    secretName: todo-tls
  rules:
  - host: todo.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: todo-api
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-frontend
            port:
              number: 80
```

## Deployment Commands

```bash
# Create namespace and secrets
kubectl create namespace todo-app
kubectl create secret generic app-secrets \
  --from-env-file=secrets.env \
  -n todo-app

# Deploy with Kustomize
kubectl apply -k .

# Verify deployment
kubectl get all -n todo-app

# Check Dapr components
kubectl get components -n todo-app

# View logs
kubectl logs -n todo-app -l app=todo-api -c todo-api
kubectl logs -n todo-app -l app=todo-api -c daprd
```

## Example 2: Helm Chart Composition

Using Helm for the same stack:

```yaml
# Chart.yaml
apiVersion: v2
name: todo-app
version: 1.0.0
dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
  - name: redpanda
    version: 5.x.x
    repository: https://charts.redpanda.com
```

```yaml
# values.yaml
global:
  namespace: todo-app

postgresql:
  enabled: true
  auth:
    database: tododb
    username: todouser
  primary:
    persistence:
      size: 10Gi

redpanda:
  enabled: true
  statefulset:
    replicas: 3
  resources:
    limits:
      memory: 2Gi

dapr:
  enabled: true
  components:
    pubsub:
      type: kafka
      brokers: "{{ .Release.Name }}-redpanda:9092"
    statestore:
      type: postgresql
      connectionString: "{{ .Values.postgresql.connectionString }}"

services:
  api:
    enabled: true
    replicas: 3
    image:
      repository: registry.digitalocean.com/todo-registry/api
      tag: v1.0.0
    dapr:
      enabled: true
      appId: todo-api
      appPort: 8000
    
  worker:
    enabled: true
    replicas: 2
    image:
      repository: registry.digitalocean.com/todo-registry/worker
      tag: v1.0.0
    dapr:
      enabled: true
      appId: todo-worker
      appPort: 8001
  
  notification:
    enabled: true
    replicas: 2
    image:
      repository: registry.digitalocean.com/todo-registry/notification
      tag: v1.0.0
    dapr:
      enabled: true
      appId: notification-service
      appPort: 8002
  
  frontend:
    enabled: true
    replicas: 3
    image:
      repository: registry.digitalocean.com/todo-registry/frontend
      tag: v1.0.0

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: todo.example.com
      paths:
        - path: /api
          service: api
        - path: /
          service: frontend
  tls:
    - secretName: todo-tls
      hosts:
        - todo.example.com
```

Deploy with Helm:

```bash
helm install todo-app . -n todo-app --create-namespace
```

## Example 3: ArgoCD GitOps

```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: todo-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/yourorg/todo-app-manifests
    targetRevision: main
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: todo-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## Best Practices

1. **Use Kustomize for overlays** - Different configs per environment
2. **Separate concerns** - Database, messaging, app services
3. **Enable Dapr selectively** - Only services that need it
4. **Configure resource limits** - Prevent resource exhaustion
5. **Use secrets properly** - Never hardcode credentials
6. **Enable monitoring** - Prometheus metrics on all services
7. **Configure health checks** - Liveness and readiness probes
8. **Use persistent storage** - For databases and stateful services
9. **Enable auto-scaling** - HPA for dynamic load
10. **Implement GitOps** - ArgoCD or Flux for CD