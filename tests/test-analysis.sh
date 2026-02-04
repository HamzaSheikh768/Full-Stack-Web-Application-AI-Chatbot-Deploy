#!/bin/bash
# Test script to verify kagent cluster analysis

echo "Testing kagent cluster analysis..."

# Test 1: Check if kagent is available
if command -v kagent &> /dev/null; then
    echo "✓ kagent is available"
else
    echo "✗ kagent is not available"
    exit 1
fi

# Test 2: Check if kubectl is available
if command -v kubectl &> /dev/null; then
    echo "✓ kubectl is available"
else
    echo "✗ kubectl is not available"
    exit 1
fi

# Test 3: Check cluster connectivity
if kubectl cluster-info &> /dev/null; then
    echo "✓ Connected to Kubernetes cluster"
else
    echo "✗ Cannot connect to Kubernetes cluster"
    exit 1
fi

# Test 4: Check basic cluster status
echo "Cluster status:"
kubectl cluster-info

# Test 5: List nodes
echo -e "\nCluster nodes:"
kubectl get nodes

# Test 6: List namespaces
echo -e "\nCluster namespaces:"
kubectl get namespaces

# Test 7: List pods across all namespaces
echo -e "\nPods in all namespaces:"
kubectl get pods --all-namespaces

# Test 8: Simulate kagent analysis
echo -e "\nSimulating kagent cluster analysis..."
echo "kagent would analyze the cluster and provide insights such as:"
echo "  - Resource utilization"
echo "  - Pod health status"
echo "  - Potential optimizations"
echo "  - Security recommendations"
echo "  - Performance bottlenecks"

echo "Cluster analysis test complete."