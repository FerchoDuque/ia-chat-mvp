# Script de instalación de Ollama para Windows
# Autor: Sistema de Agentes IA
# Fecha: 2026-01-06

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Instalador de Ollama para Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# URL de descarga de Ollama
$ollamaUrl = "https://ollama.com/download/OllamaSetup.exe"
$downloadPath = "$env:TEMP\OllamaSetup.exe"

Write-Host "=> Descargando Ollama desde $ollamaUrl..." -ForegroundColor Yellow
Write-Host ""

# Descargar Ollama
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri $ollamaUrl -OutFile $downloadPath -UseBasicParsing
$ProgressPreference = 'Continue'

Write-Host "✓ Descarga completada!" -ForegroundColor Green
Write-Host ""

Write-Host "=> Ejecutando instalador de Ollama..." -ForegroundColor Yellow
Write-Host "   (La ventana del instalador puede aparecer y desaparecer automaticamente)" -ForegroundColor Gray
Write-Host ""

# Ejecutar el instalador
Start-Process -FilePath $downloadPath -Wait

Write-Host "✓ Instalacion completada!" -ForegroundColor Green
Write-Host ""

# Limpiar archivos temporales
Remove-Item $downloadPath -ErrorAction SilentlyContinue

# Configurar variable de entorno OLLAMA_MODELS
$modelsPath = "D:\Proyectos\WORK\Agentes-practica\models"
[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $modelsPath, "User")
Write-Host "✓ Variable OLLAMA_MODELS configurada: $modelsPath" -ForegroundColor Green
Write-Host ""

# Esperar a que Ollama se inicie
Write-Host "=> Esperando a que Ollama se inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✓ Instalacion completada!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Cyan
Write-Host "  1. CIERRA y vuelve a abrir PowerShell (IMPORTANTE!)" -ForegroundColor White
Write-Host "  2. Ejecuta: ollama --version" -ForegroundColor White
Write-Host "  3. Ejecuta: .\scripts\setup_models.ps1" -ForegroundColor White
Write-Host ""
