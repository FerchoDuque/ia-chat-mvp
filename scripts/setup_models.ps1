# Script para descargar modelos recomendados de Ollama
# Autor: Sistema de Agentes IA
# Fecha: 2026-01-06

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuración de Modelos de IA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Ollama está instalado
try {
    $ollamaVersion = ollama --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Ollama no está instalado o no está en el PATH" -ForegroundColor Red
        Write-Host "  Por favor, ejecuta primero: .\\scripts\\install_ollama.ps1" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✓ Ollama detectado: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Error al verificar Ollama: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verificar que el servicio está corriendo
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($response.Content -match "Ollama is running") {
        Write-Host "✓ Servicio de Ollama está activo" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ El servicio de Ollama no está corriendo" -ForegroundColor Red
    Write-Host "  Espera unos segundos e intenta nuevamente" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Modelos disponibles para descargar" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Definir modelos recomendados con información
$models = @(
    @{
        Name = "llama3.2"
        Size = "~4.7 GB"
        Description = "Uso general, excelente balance"
        Tier = "Tier 1 - RECOMENDADO"
        Color = "Green"
    },
    @{
        Name = "mistral"
        Size = "~4.1 GB"
        Description = "Rápido y eficiente"
        Tier = "Tier 1 - RECOMENDADO"
        Color = "Green"
    },
    @{
        Name = "deepseek-r1:8b"
        Size = "~4.9 GB"
        Description = "Razonamiento avanzado"
        Tier = "Tier 1 - RECOMENDADO"
        Color = "Green"
    },
    @{
        Name = "phi4"
        Size = "~8.0 GB"
        Description = "Análisis lógico intensivo"
        Tier = "Tier 2"
        Color = "Cyan"
    },
    @{
        Name = "qwen2.5:7b"
        Size = "~4.7 GB"
        Description = "Multilingüe, coding"
        Tier = "Tier 2"
        Color = "Cyan"
    },
    @{
        Name = "gemma2:9b"
        Size = "~5.4 GB"
        Description = "Rápido, by Google"
        Tier = "Tier 2"
        Color = "Cyan"
    },
    @{
        Name = "phi3:mini"
        Size = "~2.3 GB"
        Description = "Ultra rápido, ligero"
        Tier = "Tier 3"
        Color = "Yellow"
    },
    @{
        Name = "tinyllama"
        Size = "~637 MB"
        Description = "Extremadamente ligero"
        Tier = "Tier 3"
        Color = "Yellow"
    }
)

# Mostrar modelos
$index = 1
foreach ($model in $models) {
    Write-Host "[$index] " -NoNewline -ForegroundColor White
    Write-Host "$($model.Name) " -NoNewline -ForegroundColor $model.Color
    Write-Host "($($model.Size))" -ForegroundColor Gray
    Write-Host "    $($model.Description) - $($model.Tier)" -ForegroundColor Gray
    $index++
}

Write-Host ""
Write-Host "Opciones especiales:" -ForegroundColor Cyan
Write-Host "[A] Descargar todos los modelos Tier 1 (recomendado para empezar)" -ForegroundColor Green
Write-Host "[B] Descargar todos los modelos" -ForegroundColor Yellow
Write-Host "[0] Salir" -ForegroundColor White
Write-Host ""

$selection = Read-Host "Selecciona una opción (número, A, B, o 0)"

$modelsToDownload = @()

switch ($selection.ToUpper()) {
    "A" {
        $modelsToDownload = $models | Where-Object { $_.Tier -match "Tier 1" }
        Write-Host "→ Descargando todos los modelos Tier 1..." -ForegroundColor Green
    }
    "B" {
        $modelsToDownload = $models
        Write-Host "→ Descargando todos los modelos..." -ForegroundColor Yellow
    }
    "0" {
        Write-Host "Saliendo..." -ForegroundColor Gray
        exit 0
    }
    default {
        try {
            $index = [int]$selection - 1
            if ($index -ge 0 -and $index -lt $models.Count) {
                $modelsToDownload = @($models[$index])
                Write-Host "→ Descargando $($models[$index].Name)..." -ForegroundColor Cyan
            } else {
                Write-Host "✗ Opción inválida" -ForegroundColor Red
                exit 1
            }
        } catch {
            Write-Host "✗ Opción inválida" -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Descargando modelos..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$totalModels = $modelsToDownload.Count
$currentModel = 0
$successCount = 0
$failCount = 0

foreach ($model in $modelsToDownload) {
    $currentModel++
    Write-Host "[$currentModel/$totalModels] Descargando: " -NoNewline -ForegroundColor White
    Write-Host "$($model.Name)" -ForegroundColor $model.Color
    Write-Host "              Tamaño: $($model.Size)" -ForegroundColor Gray
    Write-Host ""
    
    try {
        # Ejecutar ollama pull
        $process = Start-Process -FilePath "ollama" -ArgumentList "pull", $model.Name -Wait -NoNewWindow -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-Host "✓ $($model.Name) descargado exitosamente!" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "✗ Error al descargar $($model.Name)" -ForegroundColor Red
            $failCount++
        }
    } catch {
        Write-Host "✗ Error: $_" -ForegroundColor Red
        $failCount++
    }
    
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Resumen de descarga" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ Exitosos: $successCount" -ForegroundColor Green
if ($failCount -gt 0) {
    Write-Host "✗ Fallidos: $failCount" -ForegroundColor Red
}
Write-Host ""

# Listar modelos instalados
Write-Host "→ Modelos actualmente instalados:" -ForegroundColor Cyan
Write-Host ""
ollama list

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✓ Configuración completada!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Cyan
Write-Host "  1. Prueba un modelo: ollama run llama3.2" -ForegroundColor White
Write-Host "  2. O ejecuta los ejemplos Python del proyecto" -ForegroundColor White
Write-Host ""
