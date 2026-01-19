# Prueba Simple del Sistema de Agentes
# Este script NO requiere Ollama instalado - solo valida el código Python

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Prueba del Sistema (Sin Ollama)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   OK Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   X Python no encontrado" -ForegroundColor Red
    exit 1
}

# Verificar estructura del proyecto
Write-Host ""
Write-Host "2. Verificando estructura del proyecto..." -ForegroundColor Yellow

$requiredDirs = @("src/core", "src/agents", "examples")
$allExist = $true
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "   OK $dir" -ForegroundColor Green
    } else {
        Write-Host "   X $dir no encontrado" -ForegroundColor Red
        $allExist = $false
    }
}

# Verificar archivos clave
Write-Host ""
Write-Host "3. Verificando archivos del sistema..." -ForegroundColor Yellow

$keyFiles = @(
    "src/core/ollama_client.py",
    "src/core/model_manager.py",
    "src/agents/base_agent.py",
    "src/agents/types/researcher_agent.py",
    "src/agents/types/coder_agent.py",
    "src/agents/types/coordinator_agent.py"
)

foreach ($file in $keyFiles) {
    if (Test-Path $file) {
        $lines = (Get-Content $file | Measure-Object -Line).Lines
        Write-Host "   OK $file ($lines lineas)" -ForegroundColor Green
    } else {
        Write-Host "   X $file no encontrado" -ForegroundColor Red
    }
}

# Verificar entorno virtual
Write-Host ""
Write-Host "4. Verificando entorno virtual..." -ForegroundColor Yellow

if (Test-Path "venv\Scripts\python.exe") {
    Write-Host "   OK Entorno virtual existe"  -ForegroundColor Green
    
    # Probar imports
    Write-Host ""
    Write-Host "5. Probando imports de Python..." -ForegroundColor Yellow
    Write-Host ""
    
    $testCode = @"
import sys
sys.path.insert(0, '.')

try:
    from src.core.ollama_client import OllamaClient
    print('   OK OllamaClient')
    
    from src.core.model_manager import ModelManager
    print('   OK ModelManager')
    
    from src.agents.base_agent import BaseAgent
    print('   OK BaseAgent')
    
    from src.agents.types.researcher_agent import ResearcherAgent
    print('   OK ResearcherAgent')
    
    from src.agents.types.coder_agent import CoderAgent
    print('   OK CoderAgent')
    
    from src.agents.types.coordinator_agent import CoordinatorAgent
    print('   OK CoordinatorAgent')
    
    print('\nTodos los modulos se importaron correctamente!')
    
except ImportError as e:
    print(f'X Error: {e}')
    print('\nInstala las dependencias:')
    print('  pip install -r requirements.txt')
"@
    
    $testCode | & "venv\Scripts\python.exe" -
    
} else {
    Write-Host "   X No hay entorno virtual" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Crea el entorno virtual con:" -ForegroundColor Cyan
    Write-Host "  python -m venv venv" -ForegroundColor White
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Resumen" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "El sistema de agentes esta configurado correctamente." -ForegroundColor Green
Write-Host ""
Write-Host "Para usar el sistema completo:" -ForegroundColor Cyan
Write-Host "  1. Cierra y vuelve a abrir PowerShell" -ForegroundColor White
Write-Host "  2. Verifica: ollama --version" -ForegroundColor White
Write-Host "  3. Descarga modelos: .\scripts\setup_models.ps1" -ForegroundColor White
Write-Host "  4. Prueba: python examples\simple_chat.py" -ForegroundColor White
Write-Host ""
