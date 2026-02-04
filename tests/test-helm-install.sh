#!/bin/bash
# Test script to verify successful Helm chart installation

echo "Testing Helm chart installation..."

# Test 1: Check if Helm is available
if command -v helm &> /dev/null; then
    echo "✓ Helm is available"
    helm version
else
    echo "✗ Helm is not available"
    exit 1
fi

# Test 2: Check if kubectl is available
if command -v kubectl &> /dev/null; then
    echo "✓ kubectl is available"
else
    echo "✗ kubectl is not available"
    exit 1
fi

# Test 3: Check for running Minikube cluster
if kubectl cluster-info &> /dev/null; then
    echo "✓ Kubernetes cluster is accessible"
else
    echo "✗ Kubernetes cluster is not accessible"
    echo "  Hint: Make sure Minikube is running with 'minikube start'"
    exit 1
fi

# Test 4: Check for Helm releases
echo "Checking Helm releases..."
helm list --all-namespaces

# Test 5: Check for pods in the cluster
echo "Checking running pods..."
kubectl get pods --all-namespaces

echo "Helm installation test complete."