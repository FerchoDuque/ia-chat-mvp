# Guía de Inicio Rápido

## ⚠️ Importante: Primer Paso

Ollama está instalado pero **DEBES CERRAR Y VOLVER A ABRIR PowerShell** para que el PATH se actualice.

## 1. Cerrar y Volver a Abrir PowerShell

1. Cierra TODAS las ventanas de PowerShell
2. Abre una nueva ventana de PowerShell
3. Navega al proyecto:
   ```powershell
   cd D:\Proyectos\WORK\Agentes-practica
   ```

## 2. Verificar Ollama

```powershell
# Verificar versión
ollama --version

# Verificar que el servidor esté corriendo
curl http://localhost:11434
# Deberías ver: "Ollama is running"
```

Si el servidor no está corriendo, se iniciará automáticamente al usar ollama.

## 3. Descargar Modelos

```powershell
# Opción A: Usar el script interactivo (RECOMENDADO)
.\scripts\setup_models.ps1

# Opción B: Descargar manualmente los Tier 1
ollama pull llama3.2
ollama pull mistral
ollama pull deepseek-r1:8b
```

**Nota**: Los modelos son grandes (4-5 GB cada uno). La descarga puede tardar según tu conexión.

## 4. Verificar Modelos Instalados

```powershell
ollama list
```

## 5. Configurar Entorno Python

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

## 6. Probar el Sistema

### Test 1: Chat Simple

```powershell
python examples\simple_chat.py
```

Esto abrirá un chat interactivo con el modelo.

### Test 2: Sistema Multi-Agente de Investigación

```powershell
python examples\multi_agent_research.py --query "Explica machine learning" --depth medium
```

### Test 3: Asistente de Código

```powershell
# Generar código
python examples\code_assistant.py --task generate --language python

# Revisar código
python examples\code_assistant.py --task review --language python

# Explicar código
python examples\code_assistant.py --task explain --language python
```

## 7. Comandos Útiles de Ollama

```powershell
# Ver modelos instalados
ollama list

# Ejecutar un modelo (chat interactivo)
ollama run llama3.2

# Eliminar un modelo
ollama rm nombre_modelo

# Ver info de un modelo
ollama show llama3.2
```

## Troubleshooting

### "ollama no se reconoce como comando"
- **Solución**: Cierra PowerShell completamente y vuelve a abrirlo

### "Ollama is not running"
- **Solución**: Ejecuta cualquier comando de ollama (ej: `ollama list`) y se iniciará automáticamente

### Error al importar módulos Python
- **Solución**: Asegúrate de haber activado el entorno virtual y ejecutado `pip install -r requirements.txt`

### Modelo no encontrado
- **Solución**: Descarga el modelo con `ollama pull nombre_modelo`

## Próximos Pasos

1. ✅ Experimenta con los ejemplos incluidos
2. 📚 Lee la documentación en `docs/ARCHITECTURE.md`
3. 🔧 Crea tus propios agentes personalizados
4. 🚀 Integra el sistema en tus proyectos

## Recursos

- [Documentación de Ollama](https://ollama.com)
- [LangChain Documentation](https://python.langchain.com)
- [README del Proyecto](README.md)
- [Plan de Implementación](../../brain/e5c370db-365c-47a7-8eda-36721b382bc1/implementation_plan.md)

¡Disfruta explorando tu sistema de agentes de IA local! 🚀
