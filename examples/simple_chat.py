"""
Ejemplo simple de chat con un modelo de Ollama.
Demuestra el uso básico del sistema.
"""

import asyncio
from loguru import logger

from src.core.ollama_client import OllamaClient
from src.core.model_manager import ModelManager


async def main():
    """Función principal del ejemplo."""
    
    # Configurar logging
    logger.info("=== Chat Simple con Ollama ===")
    
    # Crear cliente
    client = OllamaClient()
    
    # Verificar que Ollama esté corriendo
    logger.info("Verificando conexión con Ollama...")
    is_healthy = await client.check_health()
    
    if not is_healthy:
        logger.error("Ollama no está corriendo!")
        logger.info("Por favor ejecuta: ollama serve")
        return
    
    logger.info("✓ Ollama está corriendo correctamente")
    
    # Listar modelos disponibles
    models = await client.list_models()
    
    if not models:
        logger.warning("No hay modelos instalados")
        logger.info("Ejecuta: .\\scripts\\setup_models.ps1 para descargar modelos")
        return
    
    logger.info(f"Modelos disponibles: {len(models)}")
    for model in models:
        name = model.get("name", "unknown")
        size = model.get("size", 0) / (1024**3)  # Convertir a GB
        logger.info(f"  - {name} ({size:.2f} GB)")
    
    # Seleccionar primer modelo disponible
    selected_model = models[0].get("name", "").split(":")[0]
    logger.info(f"\nUsando modelo: {selected_model}")
    
    # Chat simple
    print("\n" + "="*50)
    print("Chat Simple - Escribe 'salir' para terminar")
    print("="*50 + "\n")
    
    while True:
        # Obtener input del usuario
        user_input = input("Tú: ")
        
        if user_input.lower() in ['salir', 'exit', 'quit']:
            logger.info("Finalizando chat...")
            break
        
        if not user_input.strip():
            continue
        
        # Generar respuesta
        print("Asistente: ", end="", flush=True)
        
        try:
            # Usar streaming para respuesta en tiempo real
            async for chunk in client.generate_stream(
                model=selected_model,
                prompt=user_input,
                temperature=0.7
            ):
                print(chunk, end="", flush=True)
            
            print("\n")
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            print(f"Error: {e}\n")
    
    # Cerrar cliente
    await client.close()
    logger.info("Chat finalizado")


if __name__ == "__main__":
    asyncio.run(main())
