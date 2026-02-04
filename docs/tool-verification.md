# Tool Verification Procedures

This document outlines the procedures for verifying that all required AI-assisted DevOps tools are properly installed and accessible.

## Verification Steps

### 1. Docker and Gordon (Docker AI Agent)

Verify Docker is working:
```bash
docker --version
```

Verify Gordon (Docker AI Agent) is accessible:
```bash
docker ai --help
```

### 2. Kubernetes Tools

Verify kubectl is accessible:
```bash
kubectl version --client
```

Verify Helm is accessible:
```bash
helm version
```

Verify Minikube is accessible:
```bash
minikube version
```

### 3. AI Tools

Verify kubectl-ai is accessible:
```bash
kubectl-ai "hello"
```

Verify kagent is accessible:
```bash
kagent "analyze cluster health"
```

## Automated Verification

Run the verification script:
```bash
# On Windows
.\scripts\verify-tools.ps1
```

## Expected Output

All tools should return version information or help text without errors. If any tool is not accessible, it may need to be installed or added to the system PATH.

## Troubleshooting

- If Docker commands fail, ensure Docker Desktop is running
- If Gordon is not accessible, verify AI features are enabled in Docker Desktop settings
- If kubectl-ai or kagent are not found, ensure they are properly installed via pip
- If Minikube fails, ensure virtualization is enabled in BIOS and hypervisor is available