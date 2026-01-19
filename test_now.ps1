# Script para probar el sistema de agentes
# Uso: .\test_now.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Prueba del Sistema de Agentes" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ruta directa a Ollama
$ollamaPath = "$env:USERPROFILE\AppData\Local\Programs\Ollama\ollama.exe"

# Verificar si Ollama existe
if (-not (Test-Path $ollamaPath)) {
    Write-Host "X Ollama no encontrado" -ForegroundColor Red
    Write-Host "  Cierra y vuelve a abrir PowerShell" -ForegroundColor Yellow
    exit 1
}

Write-Host "OK Ollama encontrado" -ForegroundColor Green
Write-Host ""

# 1. Iniciar servidor Ollama
Write-Host "1. Iniciando servidor Ollama..." -ForegroundColor Yellow

$process = Start-Process -FilePath $ollamaPath -ArgumentList "serve" -WindowStyle Hidden -PassThru
Write-Host "   OK Servidor iniciado (PID: $($process.Id))" -ForegroundColor Green

# Esperar
Write-Host "   Esperando a que el servidor este listo..."
Start-Sleep -Seconds 5

# 2. Verificar conexion
Write-Host ""
Write-Host "2. Verificando conexion..." -ForegroundColor Yellow

$response = Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing -TimeoutSec 5 -ErrorAction SilentlyContinue

if ($response -and $response.Content -match "Ollama is running") {
    Write-Host "   OK Servidor Ollama esta corriendo" -ForegroundColor Green
} else {
    Write-Host "   X No se puede conectar" -ForegroundColor Red
    Write-Host "   Espera unos segundos e intenta de nuevo" -ForegroundColor Yellow
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    exit 1
}

# 3. Verificar modelos
Write-Host ""
Write-Host "3. Verificando modelos..." -ForegroundColor Yellow

$modelList = & $ollamaPath list 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host $modelList
} else {
    Write-Host "   ! No hay modelos instalados" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Descarga modelos con:" -ForegroundColor Cyan
    Write-Host "  $ollamaPath pull llama3.2" -ForegroundColor White
}

# 4. Probar Python
Write-Host ""
Write-Host "4. Probando sistema Python..." -ForegroundColor Yellow
Write-Host ""

$pythonVersion = python --version 2>&1
Write-Host "   Python: $pythonVersion" -ForegroundColor Green

# Verificar entorno virtual
if (Test-Path "venv\Scripts\python.exe") {
    Write-Host "   OK Entorno virtual encontrado" -ForegroundColor Green
    Write-Host ""
    Write-Host "   Ejecutando prueba..." -ForegroundColor Cyan
    Write-Host ""
    
    & "venv\Scripts\python.exe" test_quick.py
    
} else {
    Write-Host "   ! No hay entorno virtual" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Crea el entorno virtual:" -ForegroundColor Cyan
    Write-Host "  python -m venv venv" -ForegroundColor White
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Servidor Ollama corriendo (PID: $($process.Id))" -ForegroundColor Gray
Write-Host "Para detenerlo: Stop-Process -Id $($process.Id)" -ForegroundColor Gray
Write-Host ""
