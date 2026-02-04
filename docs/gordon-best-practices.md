# Docker AI (Gordon) Best Practices

## Overview
This document outlines best practices for using Docker AI Agent (Gordon) to generate Dockerfiles and build container images for the Todo Chatbot application.

## General Guidelines

### 1. Clear Prompts
When asking Gordon to generate Dockerfiles, use specific and detailed prompts:
- Mention the specific framework (Next.js for frontend, FastAPI for backend)
- Specify any special requirements (environment variables, build arguments)
- Indicate the target environment (development, production)

### 2. Framework Recognition
Gordon can automatically detect frameworks in your project. Ensure:
- Package.json or requirements.txt files are properly configured
- Project structure follows standard conventions
- Dependencies are clearly defined

### 3. Security Considerations
- Gordon follows security best practices by default (non-root users)
- Verify that generated Dockerfiles use minimal base images
- Check that sensitive data is not hardcoded in Dockerfiles

## Generating Dockerfiles

### For Frontend (Next.js)
```bash
# Navigate to frontend directory
cd frontend

# Generate Dockerfile for Next.js application
docker ai "Create an optimized Dockerfile for a Next.js frontend application in the current directory"
```

### For Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Generate Dockerfile for FastAPI application
docker ai "Create an optimized Dockerfile for a FastAPI backend application in the current directory with proper Python dependencies management"
```

## Building Images

### For Frontend
```bash
# Build the frontend image
docker ai "Build a Docker image for todo-frontend from the current directory with proper tagging"
```

### For Backend
```bash
# Build the backend image
docker ai "Build a Docker image for todo-backend from the current directory with proper tagging"
```

## Verification Steps

### 1. Dockerfile Quality Check
After Gordon generates Dockerfiles, verify:
- Base images are appropriate and up-to-date
- Multi-stage builds are used for optimization
- Non-root users are used for security
- Build arguments and environment variables are properly handled

### 2. Image Build Verification
- Check that images build without errors
- Verify image sizes are reasonable
- Confirm that images can be run successfully

### 3. Security Scanning
- Use Docker Scout or similar tools to scan images for vulnerabilities
- Review any security warnings or recommendations

## Common Commands

### Generate Dockerfile
```bash
docker ai "Create Dockerfile for [application type] in current directory"
```

### Build Image
```bash
docker ai "Build Docker image for [app name] with tag [version]"
```

### Optimize Dockerfile
```bash
docker ai "Optimize this Dockerfile for smaller size and faster builds"
```

### Fix Issues
```bash
docker ai "Fix this Dockerfile to address [specific issue]"
```

## Troubleshooting

### If Gordon Cannot Generate Dockerfile
- Ensure project files are properly structured
- Check if framework can be detected
- Provide more specific instructions in the prompt

### If Image Build Fails
- Review generated Dockerfile for syntax errors
- Verify all required files are present in the build context
- Check for missing dependencies or incorrect paths

### If Image Size is Too Large
- Request Gordon to optimize the Dockerfile for size
- Consider using multi-stage builds
- Remove unnecessary dependencies or files

## Sample Prompts

### Frontend Dockerfile Generation
```
Create an optimized multi-stage Dockerfile for a Next.js 14 application with App Router, Tailwind CSS, and TypeScript. The application is located in the current directory. Use node:18-alpine as the base image. Copy package.json and package-lock.json first, install dependencies, then copy the rest of the code. Create a non-root user for security. Expose port 3000.
```

### Backend Dockerfile Generation
```
Create an optimized Dockerfile for a FastAPI application with SQLModel, PostgreSQL, and Better Auth. The application is in the current directory. Use python:3.11-slim as the base image. Copy requirements.txt first, install dependencies, then copy the application code. Create a non-root user for security. Expose port 8000.
```

## Integration with CI/CD
- Use the same Gordon-generated Dockerfiles in your CI/CD pipeline
- Consider caching Docker layers for faster builds
- Implement security scanning in your pipeline