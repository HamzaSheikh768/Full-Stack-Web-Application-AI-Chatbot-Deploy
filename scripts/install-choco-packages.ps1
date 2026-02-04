#!/usr/bin/env pwsh
# Installation script for Chocolatey packages

Write-Host "Installing core DevOps tools via Chocolatey..." -ForegroundColor Green

# Install Docker Desktop (if not already installed)
Write-Host "Checking Docker Desktop..." -ForegroundColor Yellow
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✓ Docker is already installed" -ForegroundColor Green
    $dockerVersion = docker --version
    Write-Host "  Version: $dockerVersion" -ForegroundColor Cyan
} else {
    Write-Host "Installing Docker Desktop..." -ForegroundColor Yellow
    choco install docker-desktop -y
}

# Install Minikube (if not already installed)
Write-Host "`nChecking Minikube..." -ForegroundColor Yellow
if (Get-Command minikube -ErrorAction SilentlyContinue) {
    Write-Host "✓ Minikube is already installed" -ForegroundColor Green
    $minikubeVersion = minikube version
    Write-Host "  Version: $minikubeVersion" -ForegroundColor Cyan
} else {
    Write-Host "Installing Minikube..." -ForegroundColor Yellow
    choco install minikube -y
}

# Install kubectl (if not already installed)
Write-Host "`nChecking kubectl..." -ForegroundColor Yellow
if (Get-Command kubectl -ErrorAction SilentlyContinue) {
    Write-Host "✓ kubectl is already installed" -ForegroundColor Green
    $kubectlVersion = kubectl version --client
    Write-Host "  Version: $kubectlVersion" -ForegroundColor Cyan
} else {
    Write-Host "Installing kubectl..." -ForegroundColor Yellow
    choco install kubernetes-cli -y
}

# Install Helm (if not already installed)
Write-Host "`nChecking Helm..." -ForegroundColor Yellow
if (Get-Command helm -ErrorAction SilentlyContinue) {
    Write-Host "✓ Helm is already installed" -ForegroundColor Green
    $helmVersion = helm version
    Write-Host "  Version: $helmVersion" -ForegroundColor Cyan
} else {
    Write-Host "Installing Helm..." -ForegroundColor Yellow
    choco install kubernetes-helm -y
}

Write-Host "`nChocolatey package installation complete!" -ForegroundColor Green