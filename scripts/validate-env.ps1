#!/usr/bin/env pwsh
# Environment validation script for AI-assisted Kubernetes deployment

Write-Host "Validating environment for AI-assisted Kubernetes deployment..." -ForegroundColor Green

# Check system requirements
Write-Host "`nChecking system requirements..." -ForegroundColor Yellow

# Check OS
$osInfo = Get-CimInstance Win32_OperatingSystem
Write-Host "OS: $($osInfo.Caption) $($osInfo.Version)" -ForegroundColor Cyan

# Check available memory
$totalMemory = [math]::Round($osInfo.TotalVisibleMemorySize / 1MB, 2)
$freeMemory = [math]::Round($osInfo.FreePhysicalMemory / 1MB, 2)
Write-Host "Total Memory: ${totalMemory}GB" -ForegroundColor Cyan
Write-Host "Free Memory: ${freeMemory}GB" -ForegroundColor Cyan

if ($freeMemory -lt 8) {
    Write-Host "⚠️  Warning: Less than 8GB free memory available. Minikube may have performance issues." -ForegroundColor Yellow
} else {
    Write-Host "✓ Sufficient memory available for Minikube" -ForegroundColor Green
}

# Check CPU cores
$cpuInfo = Get-CimInstance Win32_Processor
$cores = ($cpuInfo | Measure-Object -Property NumberOfCores -Sum).Sum
Write-Host "CPU Cores: $cores" -ForegroundColor Cyan

if ($cores -lt 4) {
    Write-Host "⚠️  Warning: Less than 4 CPU cores available. Minikube may have performance issues." -ForegroundColor Yellow
} else {
    Write-Host "✓ Sufficient CPU cores available for Minikube" -ForegroundColor Green
}

# Check disk space
$driveInfo = Get-WmiObject Win32_LogicalDisk | Where-Object {$_.DeviceID -eq "C:"}
$freeSpaceGB = [math]::Round($_.FreeSpace / 1GB, 2)
Write-Host "Free Disk Space (C:): ${freeSpaceGB}GB" -ForegroundColor Cyan

if ($freeSpaceGB -lt 10) {
    Write-Host "⚠️  Warning: Less than 10GB free disk space available." -ForegroundColor Yellow
} else {
    Write-Host "✓ Sufficient disk space available" -ForegroundColor Green
}

# Validate tools
Write-Host "`nValidating required tools..." -ForegroundColor Yellow

$tools = @{
    "Docker" = "docker --version";
    "Docker AI (Gordon)" = "docker ai --help";
    "Minikube" = "minikube version";
    "kubectl" = "kubectl version --client";
    "Helm" = "helm version";
}

foreach ($tool in $tools.GetEnumerator()) {
    try {
        $result = Invoke-Expression $tool.Value 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ $($tool.Key) - Available" -ForegroundColor Green
        } else {
            Write-Host "✗ $($tool.Key) - NOT Available" -ForegroundColor Red
        }
    } catch {
        Write-Host "✗ $($tool.Key) - NOT Available" -ForegroundColor Red
    }
}

# Check for AI tools specifically
Write-Host "`nValidating AI tools..." -ForegroundColor Yellow

$aiTools = @(
    @{Name = "kubectl-ai"; Command = "kubectl-ai --help"},
    @{Name = "kagent"; Command = "kagent --help"}
)

foreach ($aiTool in $aiTools) {
    try {
        $result = Invoke-Expression $aiTool.Command 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ $($aiTool.Name) - Available" -ForegroundColor Green
        } else {
            Write-Host "✗ $($aiTool.Name) - NOT Available" -ForegroundColor Red
        }
    } catch {
        Write-Host "✗ $($aiTool.Name) - NOT Available" -ForegroundColor Red
    }
}

# Check project structure
Write-Host "`nValidating project structure..." -ForegroundColor Yellow

$expectedPaths = @(
    "frontend",
    "backend",
    "k8s",
    "k8s/charts",
    "scripts",
    "docs"
)

foreach ($path in $expectedPaths) {
    if (Test-Path $path) {
        Write-Host "✓ $path - Exists" -ForegroundColor Green
    } else {
        Write-Host "✗ $path - Missing" -ForegroundColor Red
    }
}

Write-Host "`nEnvironment validation complete!" -ForegroundColor Green