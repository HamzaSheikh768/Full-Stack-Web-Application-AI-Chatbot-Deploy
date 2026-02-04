#!/usr/bin/env pwsh
# Script to verify all AI-assisted DevOps tools are accessible

Write-Host "Verifying AI-assisted DevOps toolchain..." -ForegroundColor Green

# Check Docker and Gordon
Write-Host "`nChecking Docker and Gordon..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker: $dockerVersion" -ForegroundColor Green

    # Check Gordon availability
    $gordonHelp = docker ai --help 2>$null
    if ($gordonHelp) {
        Write-Host "✓ Gordon (Docker AI Agent) is available" -ForegroundColor Green
    } else {
        Write-Host "✗ Gordon (Docker AI Agent) is NOT available" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Docker is NOT available" -ForegroundColor Red
}

# Check Minikube
Write-Host "`nChecking Minikube..." -ForegroundColor Yellow
try {
    $minikubeVersion = minikube version
    Write-Host "✓ Minikube: $minikubeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Minikube is NOT available" -ForegroundColor Red
}

# Check kubectl
Write-Host "`nChecking kubectl..." -ForegroundColor Yellow
try {
    $kubectlVersion = kubectl version --client
    Write-Host "✓ kubectl: Client version verified" -ForegroundColor Green
} catch {
    Write-Host "✗ kubectl is NOT available" -ForegroundColor Red
}

# Check Helm
Write-Host "`nChecking Helm..." -ForegroundColor Yellow
try {
    $helmVersion = Helm version
    Write-Host "✓ Helm: $helmVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Helm is NOT available" -ForegroundColor Red
}

# Check kubectl-ai and kagent
Write-Host "`nChecking AI tools (kubectl-ai, kagent)..." -ForegroundColor Yellow
try {
    $kubectlAiResult = kubectl-ai --help 2>$null
    if ($kubectlAiResult) {
        Write-Host "✓ kubectl-ai is available" -ForegroundColor Green
    } else {
        Write-Host "✗ kubectl-ai is NOT available" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ kubectl-ai is NOT available" -ForegroundColor Red
}

try {
    $kagentResult = kagent --help 2>$null
    if ($kagentResult) {
        Write-Host "✓ kagent is available" -ForegroundColor Green
    } else {
        Write-Host "✗ kagent is NOT available" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ kagent is NOT available" -ForegroundColor Red
}

Write-Host "`nToolchain verification complete!" -ForegroundColor Green