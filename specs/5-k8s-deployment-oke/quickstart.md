# Quickstart Guide: Kubernetes Deployment for Oracle Cloud OKE

## Overview

This quickstart guide provides instructions for deploying the Todo Chatbot application to both Minikube (local) and Oracle Kubernetes Engine (OKE) in Oracle Cloud. The guide follows the AGENTS.md constitution for Phase V, emphasizing Dapr abstractions, event-driven architecture, and cloud-native deployment patterns.

## Prerequisites

### Local Development
- Docker Desktop or Docker Engine
- Minikube (latest version)
- kubectl
- Dapr CLI
- Node.js 18+ and npm
- Python 3.11+

### Oracle Cloud Deployment
- Oracle Cloud account with Always Free tier eligibility
- OCI CLI installed and configured
- kubectl
- Dapr CLI
- GitHub account for CI/CD

## Setup Instructions

### 1. Environment Variables

Create a `.env` file with the following variables for local development:

```env
# Database
DATABASE_URL="your_neon_postgres_connection_string"

# Authentication
BETTER_AUTH_SECRET="your_jwt_secret_here"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"

# Cohere API
COHERE_API_KEY="your_cohere_api_key"

# Dapr Configuration
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001

# Application
NEXTAUTH_URL="http://localhost:3000"
NODE_ENV="development"
```

For Oracle Cloud deployment, these will be configured in GitHub secrets.

### 2. Local Setup (Minikube)

1. Start Minikube:
```bash
minikube start --cpus=2 --memory=4096
```

2. Install Dapr:
```bash
dapr init -k
```

3. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

4. Build and deploy to Minikube:
```bash
# Build Docker images
docker build -t todo-frontend -f frontend/Dockerfile .
docker build -t todo-backend -f backend/Dockerfile .

# Deploy to Minikube
kubectl apply -f k8s/manifests/
```

### 3. Oracle Cloud Setup (OKE)

1. Create OKE cluster using Terraform or OCI Console:
```bash
# Using Terraform
cd terraform/oke
terraform init
terraform apply
```

2. Configure kubectl to connect to OKE:
```bash
oci ce cluster create-kubeconfig --cluster-id <cluster-id> --file $HOME/.kube/config
```

3. Install Dapr on OKE:
```bash
dapr init -k
```

## Implementation Steps

### Step 1: Containerization

Create Dockerfiles for both frontend and backend:

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM nginx:alpine AS production
COPY --from=builder /app/out /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```dockerfile
# backend/Dockerfile
FROM python:3.13-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM base AS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
COPY --from=dependencies /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY backend/ .
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Dapr Configuration

Create Dapr component configurations:

```yaml
# dapr/components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379
  - name: redisPassword
    secretKeyRef:
      name: redis
      key: password
auth:
  secretStore: kubernetes
```

```yaml
# dapr/components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379
  - name: redisPassword
    secretKeyRef:
      name: redis
      key: password
  - name: actorStateStore
    value: "true"
auth:
  secretStore: kubernetes
```

### Step 3: Kubernetes Manifests

Create deployment manifests:

```yaml
# k8s/manifests/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  labels:
    app: todo-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
        dapr.io/app-protocol: "http"
        dapr.io/log-level: "info"
        dapr.io/config: "tracing-config"
    spec:
      containers:
      - name: todo-backend
        image: todo-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: COHERE_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: cohere
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: auth-secret
              key: secret
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend-svc
spec:
  selector:
    app: todo-backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```

### Step 4: CI/CD Pipeline

Create GitHub Actions workflow:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Kubernetes

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to OCI Registry
      uses: docker/login-action@v2
      with:
        registry: <your-oci-registry>
        username: <your-tenancy>/oracleidentitycloudservice/<your-email>
        password: ${{ secrets.OCI_AUTH_TOKEN }}

    - name: Build and push frontend
      uses: docker/build-push-action@v4
      with:
        context: ./frontend
        file: ./frontend/Dockerfile
        push: true
        tags: <your-oci-registry>/todo-frontend:${{ github.sha }}

    - name: Build and push backend
      uses: docker/build-push-action@v4
      with:
        context: ./backend
        file: ./backend/Dockerfile
        push: true
        tags: <your-oci-registry>/todo-backend:${{ github.sha }}

    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'

    - name: Configure kubectl for OKE
      uses: oracle-actions/setup-oke@v1
      with:
        tenancy-id: ${{ secrets.OCI_TENANCY_ID }}
        user-id: ${{ secrets.OCI_USER_ID }}
        region: ${{ secrets.OCI_REGION }}
        fingerprint: ${{ secrets.OCI_FINGERPRINT }}
        private-key: ${{ secrets.OCI_PRIVATE_KEY }}
        cluster-name: ${{ secrets.OCI_CLUSTER_NAME }}

    - name: Update image in deployment
      run: |
        kubectl set image deployment/todo-frontend frontend=<your-oci-registry>/todo-frontend:${{ github.sha }} -n todo-app
        kubectl set image deployment/todo-backend backend=<your-oci-registry>/todo-backend:${{ github.sha }} -n todo-app
```

## Running the Application

### Local Development

1. Start Minikube:
```bash
minikube start
```

2. Install Dapr:
```bash
dapr init -k
```

3. Deploy the application:
```bash
kubectl apply -f k8s/manifests/
```

4. Access the application:
```bash
minikube service todo-frontend-svc --url
```

### Production (OKE)

The application will be automatically deployed via the CI/CD pipeline when changes are pushed to the main branch.

## Troubleshooting

### Common Issues

1. **Dapr not starting**: Ensure Dapr runtime is installed with `dapr init -k`
2. **Image pull errors**: Verify OCI registry authentication and image tags
3. **Database connection**: Confirm your Neon PostgreSQL connection string is correct
4. **Authentication failures**: Check that Better Auth is properly configured
5. **Resource limits**: Monitor resource usage to stay within Always Free tier limits

### Useful Commands

```bash
# Check Dapr status
dapr status -k

# View logs
kubectl logs -l app=todo-backend
kubectl logs -l app=todo-frontend

# Check service invocation
dapr invoke --app-id todo-backend --method healthz

# Port forward for local testing
kubectl port-forward svc/todo-frontend-svc 3000:80
kubectl port-forward svc/todo-backend-svc 8000:80
```

## Next Steps

1. Implement the complete event-driven architecture for recurring tasks
2. Add comprehensive error handling and validation
3. Set up monitoring and observability with Dapr
4. Optimize database queries for search and filter operations
5. Add proper testing for all new features