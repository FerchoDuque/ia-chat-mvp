# Sistema de Ejecución Local de Modelos de IA

Sistema para ejecutar modelos de lenguaje grandes (LLMs) localmente y crear arquitecturas de agentes diversos usando Ollama + LangChain.

## 🚀 Inicio Rápido

### 1. Instalar Ollama

```powershell
.\scripts\install_ollama.ps1
```

Cierra y vuelve a abrir PowerShell después de la instalación.

### 2. Descargar Modelos

```powershell
.\scripts\setup_models.ps1
```

Selecciona los modelos que deseas (recomendado: opción A para Tier 1).

### 3. Configurar Entorno Python

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Probar el Sistema

```powershell
# Chat simple con un modelo
python examples\simple_chat.py

# Sistema multi-agente de investigación
python examples\multi_agent_research.py
```

## 📁 Estructura del Proyecto

```
Agentes-practica/
├── src/
│   ├── core/              # Motor core del sistema
│   │   ├── model_manager.py    # Gestión de modelos
│   │   └── ollama_client.py    # Cliente Ollama
│   ├── agents/            # Agentes especializados
│   │   ├── base_agent.py
│   │   └── types/
│   │       ├── researcher_agent.py
│   │       ├── coder_agent.py
│   │       └── coordinator_agent.py
│   ├── orchestration/     # Orquestación multi-agente
│   │   └── agent_graph.py
│   ├── tools/             # Herramientas para agentes
│   │   └── tool_registry.py
│   └── monitoring/        # Monitoreo y logging
│       ├── resource_monitor.py
│       └── logger.py
├── config/                # Configuraciones
│   └── agents.yaml
├── scripts/               # Scripts de instalación
│   ├── install_ollama.ps1
│   └── setup_models.ps1
├── examples/              # Ejemplos de uso
├── tests/                 # Tests automatizados
├── models/                # Modelos descargados (Ollama)
├── docs/                  # Documentación
└── logs/                  # Archivos de log
```

## 🤖 Modelos Recomendados

### Tier 1: Uso General (Empezar aquí)
- **Llama 3.2 8B**: Excelente balance, multilingüe
- **Mistral 7B**: Rápido y eficiente
- **DeepSeek-R1 8B**: Razonamiento avanzado

### Tier 2: Especialización
- **Phi-4 14B**: Análisis lógico intensivo
- **Qwen 2.5 7B**: Coding y multilingüe
- **Gemma 2 9B**: Rápido, by Google

### Tier 3: Ultra-Ligeros
- **Phi-3 Mini**: Ultra rápido (2.3 GB)
- **TinyLlama**: Extremadamente ligero (637 MB)

## 🛠️ Hardware Requerido

- **Mínimo**: 8 GB RAM, CPU moderno
- **Recomendado**: 16+ GB RAM, GPU con 4+ GB VRAM
- **Tu Sistema**: i7-8700, 32GB RAM, GTX 1660 (6GB) ✅ EXCELENTE

## 📚 Documentación

- [Guía de Arquitectura](docs/ARCHITECTURE.md)
- [Guía de Modelos](docs/MODELS_GUIDE.md)
- [Plan de Implementación](../../brain/e5c370db-365c-47a7-8eda-36721b382bc1/implementation_plan.md)

## 🔧 Comandos Útiles de Ollama

```powershell
# Ver modelos instalados
ollama list

# Ejecutar un modelo
ollama run llama3.2

# Eliminar un modelo
ollama rm modelo_name

# Ver info del sistema
ollama show llama3.2
```

## 📝 Licencia

Este proyecto es de código abierto para uso educativo y de desarrollo.
