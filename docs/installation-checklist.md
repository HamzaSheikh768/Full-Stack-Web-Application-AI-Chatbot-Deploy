# AI Tool Installation Checklist

## Pre-requisites
- [ ] Windows 10/11 (x64)
- [ ] Administrative access for installing packages
- [ ] At least 16GB RAM (8GB allocated to Minikube)
- [ ] At least 4 CPU cores
- [ ] Internet connection for initial setup
- [ ] Virtualization enabled in BIOS/UEFI

## Core Tool Installation

### 1. Package Manager
- [ ] Install Chocolatey (Windows)
  - [ ] Run PowerShell as Administrator
  - [ ] Execute installation command:
    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```

### 2. Core DevOps Tools
- [ ] Install Docker Desktop
  - [ ] Verify installation: `docker --version`
  - [ ] Ensure Docker Desktop is running
- [ ] Install Gordon (Docker AI Agent)
  - [ ] Enable in Docker Desktop settings (Features in development → Gordon)
  - [ ] Verify: `docker ai --help`
- [ ] Install Minikube
  - [ ] Install via Chocolatey: `choco install minikube -y`
  - [ ] Verify: `minikube version`
- [ ] Install kubectl
  - [ ] Install via Chocolatey: `choco install kubernetes-cli -y`
  - [ ] Verify: `kubectl version --client`
- [ ] Install Helm
  - [ ] Install via Chocolatey: `choco install kubernetes-helm -y`
  - [ ] Verify: `helm version`

### 3. AI Tools
- [ ] Install kubectl-ai
  - [ ] Install via pip: `pip install kubectl-ai`
  - [ ] Verify: `kubectl-ai --help`
- [ ] Install kagent
  - [ ] Install via pip: `pip install kagent`
  - [ ] Verify: `kagent --help`

## Post-Installation Verification

### 1. Environment Validation
- [ ] Run environment validation script: `.\scripts\validate-env.ps1`
- [ ] Verify all tools are accessible
- [ ] Confirm sufficient system resources

### 2. Minikube Setup
- [ ] Start Minikube cluster: `minikube start --driver=docker --cpus=4 --memory=8192`
- [ ] Verify cluster status: `kubectl get nodes`
- [ ] Confirm cluster is ready

### 3. Application Code Verification
- [ ] Verify frontend directory exists with application code
- [ ] Verify backend directory exists with application code
- [ ] Confirm application code is compatible with containerization

## Troubleshooting

- [ ] If Gordon is not available, check Docker Desktop version and AI features
- [ ] If Minikube fails to start, verify virtualization is enabled
- [ ] If AI tools fail to install, check pip repositories or use alternative installation methods
- [ ] If insufficient resources, adjust Minikube allocation settings