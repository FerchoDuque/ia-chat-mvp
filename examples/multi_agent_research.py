"""
Ejemplo de sistema multi-agente para investigación.
Demuestra coordinación entre agentes especializados.
"""

import asyncio
import argparse
from loguru import logger

from src.core.ollama_client import OllamaClient
from src.agents.types.researcher_agent import ResearcherAgent
from src.agents.types.coordinator_agent import CoordinatorAgent


async def main():
    """Función principal del ejemplo."""
    
    # Parse argumentos
    parser = argparse.ArgumentParser(description="Sistema multi-agente de investigación")
    parser.add_argument(
        "--query",
        type=str,
        default="¿Qué es la computación cuántica y cuáles son sus aplicaciones?",
        help="Pregunta o tema a investigar"
    )
    parser.add_argument(
        "--depth",
        type=str,
        choices=["shallow", "medium", "deep"],
        default="medium",
        help="Profundidad del análisis"
    )
    args = parser.parse_args()
    
    logger.info("=== Sistema Multi-Agente de Investigación ===")
    logger.info(f"Query: {args.query}")
    logger.info(f"Depth: {args.depth}\n")
    
    # Crear cliente
    client = OllamaClient()
    
    # Verificar conexión
    is_healthy = await client.check_health()
    if not is_healthy:
        logger.error("Ollama no está corriendo! Ejecuta: ollama serve")
        return
    
    logger.info("✓ Conectado a Ollama\n")
    
    try:
        # Crear agentes
        logger.info("Inicializando agentes...")
        
        coordinator = CoordinatorAgent(client=client)
        researcher = ResearcherAgent(client=client)
        
        # Registrar agentes en el coordinador
        coordinator.register_agent(researcher)
        
        logger.info("✓ Agentes inicializados")
        logger.info(f"  - {coordinator.config.name} ({coordinator.config.model})")
        logger.info(f"  - {researcher.config.name} ({researcher.config.model})\n")
        
        # Planificar la tarea
        logger.info("📋 Generando plan de investigación...")
        plan = await coordinator.plan_task(args.query)
        
        print("\n" + "="*60)
        print("PLAN DE INVESTIGACIÓN")
        print("="*60)
        print(plan["plan"])
        print("="*60 + "\n")
        
        # Ejecutar investigación
        logger.info("🔍 Ejecutando investigación...")
        result = await researcher.research(args.query, depth=args.depth)
        
        print("\n" + "="*60)
        print("RESULTADO DE INVESTIGACIÓN")
        print("="*60)
        print(result)
        print("="*60 + "\n")
        
        # Síntesis final del coordinador
        logger.info("📊 Generando síntesis final...")
        synthesis = await coordinator.delegate_and_synthesize(
            task=args.query,
            agent_tasks={
                "Researcher": [args.query]
            }
        )
        
        print("\n" + "="*60)
        print("SÍNTESIS FINAL")
        print("="*60)
        print(synthesis)
        print("="*60 + "\n")
        
        logger.info("✓ Investigación completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error durante la investigación: {e}")
        raise
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
