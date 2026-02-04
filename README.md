# TASKAPP - Professional Full-Stack Todo Application with AI Integration

A professional full-stack todo application with Next.js frontend featuring public access without authentication, local storage persistence, dark-first theme with blue accents, AI-powered task management, and comprehensive task management features.

## Kubernetes Deployment with AI Tools

This project demonstrates an AI-native DevOps approach using AI tools for containerization, orchestration, and operations.

### Prerequisites

- Windows 10/11 (x64)
- Administrative access for installing packages
- At least 16GB RAM (8GB allocated to Minikube)
- At least 4 CPU cores
- Internet connection for initial setup
- Virtualization enabled in BIOS/UEFI

### AI-Assisted Deployment Process

#### 1. Install AI-DevOps Toolchain

First, install the required tools using the provided scripts:

```powershell
# Run as Administrator
.\scripts\install-choco-packages.ps1
.\scripts\install-pip-packages.ps1
```

#### 2. Enable Gordon (Docker AI Agent)

Enable Gordon in Docker Desktop settings:
- Open Docker Desktop
- Go to Settings → Features in development
- Enable "Gordon (AI features)"
- Restart Docker Desktop

#### 3. Verify Toolchain

Verify all tools are accessible:

```powershell
.\scripts\verify-tools.ps1
.\scripts\validate-env.ps1
```

#### 4. Start Minikube Cluster

Start a Minikube cluster with appropriate resources:

```bash
minikube start --driver=docker --cpus=4 --memory=8192
```

#### 5. Generate Dockerfiles with Gordon

Use Gordon to generate optimized Dockerfiles for both frontend and backend:

```bash
# Navigate to frontend directory
cd frontend
docker ai "Create an optimized Dockerfile for a Next.js frontend application in the current directory"

# Navigate to backend directory
cd ../backend
docker ai "Create an optimized Dockerfile for a FastAPI backend application in the current directory with proper Python dependencies management"
```

#### 6. Build Container Images

Use Gordon to build container images:

```bash
# From backend directory
docker ai "Build a Docker image for todo-backend from the current directory with proper tagging"

# From frontend directory
cd ../frontend
docker ai "Build a Docker image for todo-frontend from the current directory with proper tagging"
```

#### 7. Generate Helm Charts with kubectl-ai

Use kubectl-ai to generate Helm charts:

```bash
kubectl-ai "create a Helm chart for todo frontend with deployment and service, using todo-frontend image"
kubectl-ai "create a Helm chart for todo backend with deployment and service, using todo-backend image"
```

#### 8. Deploy to Minikube

Install the Helm charts to your Minikube cluster:

```bash
helm install todo-frontend ./k8s/charts/frontend
helm install todo-backend ./k8s/charts/backend
```

#### 9. Access the Application

Get the frontend service URL:

```bash
minikube service todo-frontend --url
```

#### 10. AI-Assisted Operations

Use AI tools for ongoing operations:

```bash
# Scale deployments
kubectl-ai "scale the frontend deployment to 2 replicas"

# Analyze cluster health
kagent "analyze the cluster health"

# Troubleshoot issues
kubectl-ai "why are the pods failing"
```

### Validation

Run the validation script to ensure everything is working:

```bash
.\scripts\validate-deployment.sh
```

### Cleanup

To stop and delete the Minikube cluster:

```bash
minikube stop
minikube delete
```

## Architecture

The deployment follows an AI-native DevOps approach:

```
┌─────────────────────────────────────────────────────────────┐
│                Phase III Application                        │
│  ┌─────────────┐     ┌─────────────┐                      │
│  │   Frontend  │     │   Backend   │                      │
│  │ (Next.js)   │     │ (FastAPI)   │                      │
│  └─────────────┘     └─────────────┘                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                Docker AI (Gordon)                           │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │ Frontend Dockerfile     │  │ Backend Dockerfile      │  │
│  │ (AI-generated)          │  │ (AI-generated)          │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │ todo-frontend image     │  │ todo-backend image      │  │
│  │ (AI-built)              │  │ (AI-built)              │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Helm Charts (AI-generated)                     │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │ frontend-chart          │  │ backend-chart           │  │
│  │ (via kubectl-ai)        │  │ (via kubectl-ai)      │  │
│  │ - Deployment            │  │ - Deployment            │  │
│  │ - Service               │  │ - Service               │  │
│  │ - ConfigMap             │  │ - ConfigMap             │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Kubernetes (Minikube)                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Cluster: 4 CPU, 8GB RAM                                 ││
│  │ Pods: todo-frontend, todo-backend                       ││
│  │ Services: NodePort                                      ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│            AI Operations Layer                              │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │ kubectl-ai              │  │ kagent                  │  │
│  │ (natural language      │  │ (cluster analysis &     │  │
│  │  operations)           │  │  optimization)         │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Security Considerations

- Gordon follows security best practices by default (non-root users, minimal base images)
- RBAC configuration for service accounts
- Network policies to control traffic between services
- Secrets management for sensitive data
- Minikube runs in isolated environment
- Local-only deployment reduces attack vectors

## Troubleshooting

Refer to the documentation in the `docs/` directory for detailed troubleshooting guides:

- [Tool Verification Procedures](docs/tool-verification.md)
- [Docker AI (Gordon) Best Practices](docs/gordon-best-practices.md)
- [Helm Generation Process](docs/helm-generation.md)
- [AI Operations Guide](docs/ai-ops.md)
- [Installation Checklist](docs/installation-checklist.md)

## Original Application Features

A professional full-stack todo application with Next.js frontend featuring public access without authentication, local storage persistence, dark-first theme with blue accents, AI-powered task management, and comprehensive task management features.

## Features

- 🚀 Next.js 16+ with App Router for modern web development
- 🔓 Public access - no login required to use the application
- 💾 Local storage persistence for tasks and preferences
- 🎨 Dark-first theme with #000000 background, #2563EB blue accents, and #FFFFFF white text
- 🌙 Smooth dark/light theme switching with next-themes
- 📱 Responsive design for all device sizes
- ♿ WCAG 2.1 AA accessibility compliant
- 🔁 Recurring tasks with daily/weekly patterns
- 🏷️ Tag-based task categorization
- 📊 Task filtering, sorting, and search capabilities
- ✨ Smooth animations and loading states

## Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript, Tailwind CSS, next-themes
- **State Management**: Zustand with persistence
- **Animations**: Framer Motion
- **Drag & Drop**: dnd-kit
- **Styling**: Tailwind CSS with custom dark-first theme

## Prerequisites

- Node.js v20+
- Git

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   # Frontend
   cd frontend
   npm install
   ```
3. Run the application:
   ```bash
   # Frontend
   cd frontend
   npm run dev
   ```

## Project Structure

```
monorepo root
├── .env                          # Environment variables
├── .env.example                  # Example environment variables
├── frontend/                     # Next.js frontend application
│   ├── app/                      # App Router pages
│   ├── components/               # React components
│   ├── lib/                      # Utilities and store
│   ├── styles/                   # Global styles
│   └── ...
├── backend/                      # FastAPI backend with AI Chatbot
│   ├── src/                      # Source code
│   │   ├── main.py               # Application entry point
│   │   ├── api/                  # API route definitions
│   │   ├── models/               # SQLModel database models
│   │   ├── mcp/                  # Model Context Protocol tools
│   │   └── agent/                # AI Agent implementation
│   └── ...
```

## AI Chatbot API

The backend includes an AI-powered chatbot that allows users to manage tasks through natural language.

### Chat API Endpoint

- **Endpoint**: `POST /api/{user_id}/chat`
- **Description**: Send a message to the AI assistant and receive a response
- **Headers**:
  - `Content-Type: application/json`
  - Authentication cookie (Better Auth session)
- **Request Body**:
  ```json
  {
    "message": "string",
    "conversation_id": "number (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": "number",
    "response": "string",
    "tool_calls": "array"
  }
  ```

### Supported Commands

The AI assistant can handle various task management commands:

- **Add tasks**: "Add a task to buy groceries", "Create a task to call mom"
- **List tasks**: "Show my tasks", "What do I have to do?", "Show completed tasks"
- **Complete tasks**: "Mark task 1 as complete", "Finish the shopping task"
- **Delete tasks**: "Delete task 1", "Remove the meeting task"
- **Update tasks**: "Change task 1 to 'Call dad'", "Update the grocery task description"

### Environment Variables

Make sure to set the following environment variables:

- `COHERE_API_KEY`: Your Cohere API key for AI processing
- `DATABASE_URL`: Database connection string
- `BETTER_AUTH_SECRET`: Secret for authentication