#!/bin/bash
# Comprehensive deployment validation script for AI-assisted Kubernetes deployment

echo "Starting comprehensive deployment validation..." >&2

# Function to print status
print_status() {
    if [ $? -eq 0 ]; then
        echo "✓ $1" >&2
    else
        echo "✗ $1 - FAILED" >&2
    fi
}

# Check if required tools are available
echo -e "\\nChecking required tools..." >&2
command -v docker >/dev/null 2>&1 && echo "✓ Docker is available" >&2 || echo "✗ Docker is not available" >&2
command -v kubectl >/dev/null 2>&1 && echo "✓ kubectl is available" >&2 || echo "✗ kubectl is not available" >&2
command -v helm >/dev/null 2>&1 && echo "✓ Helm is available" >&2 || echo "✗ Helm is not available" >&2
command -v minikube >/dev/null 2>&1 && echo "✓ Minikube is available" >&2 || echo "✗ Minikube is not available" >&2

# Check if Gordon (Docker AI) is available
if command -v docker >/dev/null 2>&1; then
    docker ai --help >/dev/null 2>&1
    print_status "Gordon (Docker AI Agent) is available"
fi

# Check if kubectl-ai is available
if command -v kubectl-ai >/dev/null 2>&1; then
    echo "✓ kubectl-ai is available" >&2
else
    echo "✗ kubectl-ai is not available" >&2
fi

# Check if kagent is available
if command -v kagent >/dev/null 2>&1; then
    echo "✓ kagent is available" >&2
else
    echo "✗ kagent is not available" >&2
fi

# Check Kubernetes cluster connectivity
echo -e "\\nChecking Kubernetes cluster..." >&2
kubectl cluster-info >/dev/null 2>&1
print_status "Kubernetes cluster is accessible"

# Check if Minikube is running
minikube status >/dev/null 2>&1
print_status "Minikube is running"

# Get node status
NODES=$(kubectl get nodes --no-headers 2>/dev/null | wc -l)
if [ "$NODES" -ge 1 ]; then
    echo "✓ Found $NODES Kubernetes node(s)" >&2
else
    echo "✗ No Kubernetes nodes found" >&2
fi

# Check for running pods
echo -e "\\nChecking deployments and pods..." >&2
PODS=$(kubectl get pods --all-namespaces --no-headers 2>/dev/null | wc -l)
if [ "$PODS" -gt 0 ]; then
    echo "✓ Found $PODS running pod(s)" >&2
    kubectl get pods --all-namespaces >&2
else
    echo "✗ No running pods found" >&2
fi

# Check for Helm releases
echo -e "\\nChecking Helm releases..." >&2
RELEASES=$(helm list --all-namespaces --short 2>/dev/null | wc -l)
if [ "$RELEASES" -gt 0 ]; then
    echo "✓ Found $RELEASES Helm release(s)" >&2
    helm list --all-namespaces >&2
else
    echo "✗ No Helm releases found" >&2
fi

# Check services
echo -e "\\nChecking services..." >&2
SERVICES=$(kubectl get services --all-namespaces --no-headers 2>/dev/null | wc -l)
if [ "$SERVICES" -gt 0 ]; then
    echo "✓ Found $SERVICES service(s)" >&2
    kubectl get services --all-namespaces >&2
else
    echo "✗ No services found" >&2
fi

# Validate project structure
echo -e "\\nChecking project structure..." >&2
if [ -d "k8s/charts" ]; then
    echo "✓ k8s/charts directory exists" >&2
else
    echo "✗ k8s/charts directory does not exist" >&2
fi

if [ -d "frontend" ]; then
    echo "✓ frontend directory exists" >&2
else
    echo "✗ frontend directory does not exist" >&2
fi

if [ -d "backend" ]; then
    echo "✓ backend directory exists" >&2
else
    echo "✗ backend directory does not exist" >&2
fi

# Check for Docker images
echo -e "\\nChecking Docker images..." >&2
IMAGES=$(docker images --format "table {{.Repository}}:{{.Tag}}" 2>/dev/null | grep -E "(todo-frontend|todo-backend)" | wc -l)
if [ "$IMAGES" -gt 0 ]; then
    echo "✓ Found $IMAGES todo application Docker image(s)" >&2
    docker images --format "table {{.Repository}}:{{.Tag}}" 2>/dev/null | grep -E "(todo-frontend|todo-backend)" >&2
else
    echo "✗ No todo application Docker images found" >&2
fi

# Check if AI-generated files exist
echo -e "\\nChecking AI-generated artifacts..." >&2
if [ -f "k8s/charts/frontend/Chart.yaml" ]; then
    echo "✓ AI-generated frontend Helm chart exists" >&2
else
    echo "✗ AI-generated frontend Helm chart does not exist" >&2
fi

if [ -f "k8s/charts/backend/Chart.yaml" ]; then
    echo "✓ AI-generated backend Helm chart exists" >&2
else
    echo "✗ AI-generated backend Helm chart does not exist" >&2
fi

# Summary
echo -e "\\nValidation complete!" >&2

# Count completed checks
SUCCESS_COUNT=$(grep -c "^✓" <<< "$(bash "$0" 2>&1 | grep -E "^(✓|✗)")")
TOTAL_CHECKS=$(grep -Ec "^(✓|✗)" <<< "$(bash "$0" 2>&1 | grep -E "^(✓|✗)")")

echo "Summary: $SUCCESS_COUNT/$TOTAL_CHECKS checks passed" >&2

if [ "$SUCCESS_COUNT" -eq "$TOTAL_CHECKS" ] && [ "$TOTAL_CHECKS" -gt 0 ]; then
    echo "Overall status: SUCCESS" >&2
    exit 0
else
    echo "Overall status: PARTIAL SUCCESS" >&2
    exit 1
fi