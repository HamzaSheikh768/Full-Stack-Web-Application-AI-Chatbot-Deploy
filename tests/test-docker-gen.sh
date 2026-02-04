#!/bin/bash
# Test script to verify Dockerfile generation for frontend and backend

echo "Testing Dockerfile generation..."

# Test 1: Check if frontend Dockerfile exists
if [ -f "../frontend/Dockerfile" ]; then
    echo "✓ Frontend Dockerfile exists"
else
    echo "✗ Frontend Dockerfile does not exist"
fi

# Test 2: Check if backend Dockerfile exists
if [ -f "../backend/Dockerfile" ]; then
    echo "✓ Backend Dockerfile exists"
else
    echo "✗ Backend Dockerfile does not exist"
fi

# Test 3: Check if Docker images exist
echo "Checking for Docker images..."
docker images | grep -E "(todo-frontend|todo-backend)" > /dev/null
if [ $? -eq 0 ]; then
    echo "✓ Docker images for todo-frontend and/or todo-backend exist"
else
    echo "✗ Docker images for todo-frontend and todo-backend do not exist"
fi

echo "Dockerfile generation test complete."