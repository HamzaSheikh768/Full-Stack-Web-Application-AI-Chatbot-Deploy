#!/usr/bin/env pwsh
# Installation script for pip packages (AI tools)

Write-Host "Installing AI DevOps tools via pip..." -ForegroundColor Green

# Attempt to install kubectl-ai
Write-Host "Installing kubectl-ai..." -ForegroundColor Yellow
try {
    pip install kubectl-ai
    Write-Host "✓ kubectl-ai installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install kubectl-ai" -ForegroundColor Red
    Write-Host "  This may be because kubectl-ai is not available in standard pip repositories" -ForegroundColor Yellow
    Write-Host "  Please follow installation instructions from the official source" -ForegroundColor Yellow
}

# Attempt to install kagent
Write-Host "`nInstalling kagent..." -ForegroundColor Yellow
try {
    pip install kagent
    Write-Host "✓ kagent installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install kagent" -ForegroundColor Red
    Write-Host "  This may be because kagent is not available in standard pip repositories" -ForegroundColor Yellow
    Write-Host "  Please follow installation instructions from the official source" -ForegroundColor Yellow
}

Write-Host "`nPip package installation complete!" -ForegroundColor Green