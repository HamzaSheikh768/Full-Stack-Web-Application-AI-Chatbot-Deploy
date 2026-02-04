# Quickstart Guide: Local Kubernetes Deployment for Cloud-Native Todo Chatbot

## Prerequisites

- Windows 10/11 (x64)
- Administrative access for installing packages
- At least 16GB RAM (8GB allocated to Minikube)
- At least 4 CPU cores
- Internet connection for initial setup

## Installation Steps

### 1. Install Package Managers and Core Tools

Open PowerShell as Administrator and run:

```powershell
# Install Chocolatey (if not already installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = `
[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install core DevOps tools
choco install docker-desktop -y
choco install minikube -y
choco install kubernetes-cli -y
choco install kubernetes-helm -y
```

### 2. Install AI DevOps Tools

```powershell
pip install kubectl-ai
pip install kagent
```

### 3. Enable Gordon (Docker AI Agent)

After Docker Desktop installation:
1. Open Docker Desktop
2. Go to Settings → Features in development
3. Enable "Gordon (AI features)"
4. Restart Docker Desktop

### 4. Verify All Tools

```bash
# Verify tool installations
docker --version
minikube version
kubectl version --client
helm version
kubectl-ai "hello"
kagent "analyze cluster health"
```

## Deployment Steps

### 1. Start Minikube

```bash
# Start Minikube with Docker driver and appropriate resources
minikube start --driver=docker --cpus=4 --memory=8192
```

### 2. Generate Dockerfiles with Gordon

Navigate to your frontend directory and run:

```bash
# Generate Dockerfile for frontend
docker ai "Create Dockerfile for Next.js frontend application in current directory"
docker ai "Build Docker image for todo-frontend"
```

Navigate to your backend directory and run:

```bash
# Generate Dockerfile for backend
docker ai "Create Dockerfile for FastAPI backend application in current directory"
docker ai "Build Docker image for todo-backend"
```

### 3. Generate Helm Charts with kubectl-ai

```bash
# Generate Helm chart for frontend
kubectl-ai "create helm chart for todo frontend with deployment and service"

# Generate Helm chart for backend
kubectl-ai "create helm chart for todo backend with deployment and service"
```

### 4. Deploy to Minikube

```bash
# Install frontend chart
helm install todo-frontend ./frontend-chart

# Install backend chart
helm install todo-backend ./backend-chart
```

### 5. Verify Deployment

```bash
# Check if pods are running
kubectl get pods

# Check services
kubectl get svc

# Check deployment status
kubectl get deployments
```

### 6. Access the Application

```bash
# Get the frontend service URL
minikube service todo-frontend --url
```

## AI-Assisted Operations

### Scale Deployments

```bash
kubectl-ai "scale the frontend deployment to 2 replicas"
kubectl-ai "scale the backend deployment to 3 replicas"
```

### Troubleshoot Issues

```bash
kubectl-ai "show me the logs for the frontend pod"
kubectl-ai "why are the pods failing"
```

### Analyze Cluster Health

```bash
kagent "analyze the cluster health"
kagent "optimize resource allocation"
```

## Validation Steps

1. Confirm both frontend and backend pods are running:
   ```bash
   kubectl get pods
   ```

2. Verify services are accessible:
   ```bash
   kubectl get svc
   ```

3. Test application functionality by accessing the frontend URL:
   ```bash
   minikube service todo-frontend --url
   ```

4. Use kubectl-ai to verify deployment status:
   ```bash
   kubectl-ai "describe the status of all deployments"
   ```

## Cleanup

To stop and delete the Minikube cluster:

```bash
minikube stop
minikube delete
```

## Troubleshooting

### Common Issues

1. **Gordon not available**: Verify Docker Desktop version and ensure AI features are enabled
2. **Insufficient resources**: Ensure your machine has enough RAM and CPU allocated to Minikube
3. **Image pull errors**: Verify the container images were built correctly with Gordon
4. **Service not accessible**: Check that the service is running and use `minikube service` command to get the correct URL

### Useful Commands

```bash
# Check Minikube status
minikube status

# Get detailed pod information
kubectl describe pods

# Stream logs from a pod
kubectl logs -f deployment/todo-frontend

# SSH into Minikube
minikube ssh
```

## Next Steps

1. Experiment with more complex kubectl-ai commands
2. Use kagent for cluster optimization recommendations
3. Modify Helm chart values to customize the deployment
4. Add ingress configuration for easier access