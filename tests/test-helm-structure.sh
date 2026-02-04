#!/bin/bash
# Test script to verify AI-generated Helm chart structure

echo "Testing Helm chart structure..."

# Test 1: Check if frontend chart directory exists
if [ -d "../k8s/charts/frontend" ]; then
    echo "✓ Frontend Helm chart directory exists"

    # Check for required files in frontend chart
    if [ -f "../k8s/charts/frontend/Chart.yaml" ]; then
        echo "  ✓ Chart.yaml exists"
    else
        echo "  ✗ Chart.yaml missing"
    fi

    if [ -d "../k8s/charts/frontend/templates" ]; then
        echo "  ✓ templates directory exists"
    else
        echo "  ✗ templates directory missing"
    fi

    if [ -f "../k8s/charts/frontend/values.yaml" ]; then
        echo "  ✓ values.yaml exists"
    else
        echo "  ✗ values.yaml missing"
    fi
else
    echo "✗ Frontend Helm chart directory does not exist"
fi

# Test 2: Check if backend chart directory exists
if [ -d "../k8s/charts/backend" ]; then
    echo "✓ Backend Helm chart directory exists"

    # Check for required files in backend chart
    if [ -f "../k8s/charts/backend/Chart.yaml" ]; then
        echo "  ✓ Chart.yaml exists"
    else
        echo "  ✗ Chart.yaml missing"
    fi

    if [ -d "../k8s/charts/backend/templates" ]; then
        echo "  ✓ templates directory exists"
    else
        echo "  ✗ templates directory missing"
    fi

    if [ -f "../k8s/charts/backend/values.yaml" ]; then
        echo "  ✓ values.yaml exists"
    else
        echo "  ✗ values.yaml missing"
    fi
else
    echo "✗ Backend Helm chart directory does not exist"
fi

echo "Helm chart structure test complete."