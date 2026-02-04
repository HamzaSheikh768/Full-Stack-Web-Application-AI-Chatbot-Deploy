#!/bin/bash
# Test script to verify successful Docker image builds

echo "Testing Docker image builds..."

# Test 1: Check if todo-frontend image exists
FRONTEND_EXISTS=$(docker images -q todo-frontend:latest)
if [ ! -z "$FRONTEND_EXISTS" ]; then
    echo "✓ todo-frontend image exists"
else
    echo "✗ todo-frontend image does not exist"
fi

# Test 2: Check if todo-backend image exists
BACKEND_EXISTS=$(docker images -q todo-backend:latest)
if [ ! -z "$BACKEND_EXISTS" ]; then
    echo "✓ todo-backend image exists"
else
    echo "✗ todo-backend image does not exist"
fi

# Test 3: Check image sizes (basic validation)
if [ ! -z "$FRONTEND_EXISTS" ]; then
    FRONTEND_SIZE=$(docker inspect --format='{{.Size}}' todo-frontend:latest)
    echo "  todo-frontend size: $(($FRONTEND_SIZE / 1024 / 1024)) MB"
fi

if [ ! -z "$BACKEND_EXISTS" ]; then
    BACKEND_SIZE=$(docker inspect --format='{{.Size}}' todo-backend:latest)
    echo "  todo-backend size: $(($BACKEND_SIZE / 1024 / 1024)) MB"
fi

echo "Image build test complete."