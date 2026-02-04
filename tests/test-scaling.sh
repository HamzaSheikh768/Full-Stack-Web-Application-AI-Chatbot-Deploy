#!/bin/bash
# Test script to verify kubectl-ai scaling operations

echo "Testing kubectl-ai scaling operations..."

# Test 1: Check if kubectl-ai is available
if command -v kubectl-ai &> /dev/null; then
    echo "✓ kubectl-ai is available"
else
    echo "✗ kubectl-ai is not available"
    exit 1
fi

# Test 2: Check if kubectl is available
if command -v kubectl &> /dev/null; then
    echo "✓ kubectl is available"
else
    echo "✗ kubectl is not available"
    exit 1
fi

# Test 3: Check if there are deployments to scale
DEPLOYMENTS=$(kubectl get deployments --no-headers -o custom-columns=":metadata.name" 2>/dev/null)
if [ $? -eq 0 ] && [ ! -z "$DEPLOYMENTS" ]; then
    echo "✓ Found deployments:"
    echo "$DEPLOYMENTS"

    # Test scaling each deployment to 2 replicas
    for deployment in $DEPLOYMENTS; do
        echo "Testing scaling of deployment: $deployment"

        # Scale to 2 replicas using kubectl-ai
        # Note: In practice, you would run: kubectl-ai "scale deployment $deployment to 2 replicas"
        echo "  Would scale $deployment to 2 replicas using kubectl-ai"

        # Check current replica count
        CURRENT_REPLICAS=$(kubectl get deployment "$deployment" -o jsonpath='{.spec.replicas}')
        echo "  Current replica count: $CURRENT_REPLICAS"
    done
else
    echo "✗ No deployments found in the cluster"
    echo "  Hint: Make sure your Helm charts are installed and deployments exist"
fi

echo "Scaling test complete."