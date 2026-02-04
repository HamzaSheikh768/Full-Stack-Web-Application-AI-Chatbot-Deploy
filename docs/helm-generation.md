# AI-Generated Helm Chart Creation Process

## Overview
This document outlines the process for using AI tools (kubectl-ai and kagent) to generate Helm charts for the Todo Chatbot application.

## Prerequisites
- Kubernetes cluster running (e.g., Minikube)
- Helm installed and initialized
- kubectl-ai installed and accessible
- Application Docker images available in local registry

## Generating Helm Charts with kubectl-ai

### Frontend Helm Chart
```bash
# Generate Helm chart for frontend service
kubectl-ai "create a Helm chart for todo frontend with deployment and service, using todo-frontend image"

# Navigate to the generated chart and customize as needed
cd k8s/charts/frontend
```

### Backend Helm Chart
```bash
# Generate Helm chart for backend service
kubectl-ai "create a Helm chart for todo backend with deployment and service, using todo-backend image"

# Navigate to the generated chart and customize as needed
cd k8s/charts/backend
```

## Chart Structure
A typical AI-generated Helm chart will include:

- `Chart.yaml` - Chart metadata
- `values.yaml` - Default configuration values
- `templates/` directory containing:
  - `deployment.yaml` - Kubernetes Deployment resource
  - `service.yaml` - Kubernetes Service resource
  - `configmap.yaml` - Configuration data (if needed)
  - `secret.yaml` - Sensitive data (if needed)
  - `ingress.yaml` - Ingress configuration (if needed)

## Customization

### Values.yaml
Customize the `values.yaml` file to configure:

- Image repository and tag
- Resource limits and requests
- Environment variables
- Service configuration
- Replica count

### Templates
The AI-generated templates may need adjustments for:

- Environment-specific configurations
- Resource requirements
- Health checks
- Service ports and types

## Installation Process

### Frontend
```bash
# Install frontend chart
helm install todo-frontend ./k8s/charts/frontend
```

### Backend
```bash
# Install backend chart
helm install todo-backend ./k8s/charts/backend
```

## Verification

### Check Release Status
```bash
# Verify frontend release
helm status todo-frontend

# Verify backend release
helm status todo-backend
```

### Check Resources
```bash
# Check deployments
kubectl get deployments

# Check services
kubectl get services

# Check pods
kubectl get pods
```

## Best Practices

### 1. Modularity
- Keep frontend and backend charts separate
- Use consistent naming conventions
- Maintain clear separation of concerns

### 2. Configuration Management
- Use values.yaml for configurable parameters
- Avoid hardcoding values in templates
- Use secrets for sensitive information

### 3. Resource Management
- Define appropriate resource requests and limits
- Use Horizontal Pod Autoscaler if needed
- Monitor resource usage after deployment

### 4. Service Discovery
- Ensure proper service names for inter-service communication
- Use DNS names for service-to-service communication
- Consider network policies for security

## Troubleshooting

### If Helm Chart Generation Fails
- Verify kubectl-ai is properly installed
- Check Kubernetes cluster connectivity
- Ensure proper permissions for resource creation

### If Installation Fails
- Check for existing releases with the same name
- Verify image names and tags are correct
- Check resource requirements against cluster capacity

### If Pods Fail to Start
- Check pod logs: `kubectl logs <pod-name>`
- Describe pod: `kubectl describe pod <pod-name>`
- Verify image pull secrets if using private registries

## Common kubectl-ai Commands for Helm

```bash
# Generate Helm chart
kubectl-ai "generate Helm chart for [app-name] with deployment and service"

# Explain Helm chart structure
kubectl-ai "explain the components of a Kubernetes Helm chart"

# Troubleshoot Helm deployment
kubectl-ai "why is my Helm deployment not starting pods"

# Upgrade Helm release
kubectl-ai "upgrade Helm release [name] with new image [tag]"
```

## Integration with CI/CD

- Use the same AI-generated Helm charts in your CI/CD pipeline
- Implement Helm linting and testing in your pipeline
- Consider using Helm repository for storing charts
- Implement proper versioning and tagging strategies