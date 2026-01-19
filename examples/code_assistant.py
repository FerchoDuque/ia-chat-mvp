"""
Ejemplo de asistente de programación.
Demuestra las capacidades del CoderAgent.
"""

import asyncio
import argparse
from loguru import logger

from src.core.ollama_client import OllamaClient
from src.agents.types.coder_agent import CoderAgent


async def main():
    """Función principal del ejemplo."""
    
    # Parse argumentos
    parser = argparse.ArgumentParser(description="Asistente de programación")
    parser.add_argument(
        "--task",
        type=str,
        choices=["generate", "review", "explain", "debug"],
        default="generate",
        help="Tipo de tarea"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="python",
        help="Lenguaje de programación"
    )
    args = parser.parse_args()
    
    logger.info("=== Asistente de Programación ===")
    logger.info(f"Tarea: {args.task}")
    logger.info(f"Lenguaje: {args.language}\n")
    
    # Crear cliente y agente
    client = OllamaClient()
    
    # Verificar conexión
    is_healthy = await client.check_health()
    if not is_healthy:
        logger.error("Ollama no está corriendo!")
        return
    
    logger.info("✓ Conectado a Ollama")
    
    try:
        # Crear agente de programación
        coder = CoderAgent(client=client)
        logger.info(f"✓ CoderAgent inicializado ({coder.config.model})\n")
        
        if args.task == "generate":
            # Ejemplo de generación de código
            logger.info("📝 Generando código...")
            
            description = """Crea una función que:
1. Reciba una lista de números
2. Filtre los números pares
3. Calcule el cuadrado de cada número par
4. Retorne la suma total"""
            
            code = await coder.generate_code(
                description=description,
                language=args.language,
                requirements=["Incluir docstring", "Manejar casos edge"]
            )
            
            print("\n" + "="*60)
            print("CÓDIGO GENERADO")
            print("="*60)
            print(code)
            print("="*60 + "\n")
        
        elif args.task == "review":
            # Ejemplo de revisión de código
            logger.info("🔍 Revisando código...")
            
            sample_code = """
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total / len(numbers)
"""
            
            review = await coder.review_code(
                code=sample_code,
                language=args.language
            )
            
            print("\n" + "="*60)
            print("REVISIÓN DE CÓDIGO")
            print("="*60)
            print(review)
            print("="*60 + "\n")
        
        elif args.task == "explain":
            # Ejemplo de explicación de código
            logger.info("💡 Explicando código...")
            
            sample_code = """
@dataclass
class Node:
    value: int
    children: List['Node'] = field(default_factory=list)

def dfs(node: Node, visited: set) -> List[int]:
    if node in visited:
        return []
    visited.add(node)
    result = [node.value]
    for child in node.children:
        result.extend(dfs(child, visited))
    return result
"""
            
            explanation = await coder.explain_code(
                code=sample_code,
                language=args.language
            )
            
            print("\n" + "="*60)
            print("EXPLICACIÓN DEL CÓDIGO")
            print("="*60)
            print(explanation)
            print("="*60 + "\n")
        
        elif args.task == "debug":
            # Ejemplo de debugging
            logger.info("🐛 Debuggeando código...")
            
            buggy_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-3)
"""
            
            error = "La función genera números incorrectos. fibonacci(5) debería ser 5 pero retorna un valor incorrecto."
            
            debug_help = await coder.debug_code(
                code=buggy_code,
                error=error,
                language=args.language
            )
            
            print("\n" + "="*60)
            print("ANÁLISIS DE DEBUG")
            print("="*60)
            print(debug_help)
            print("="*60 + "\n")
        
        logger.info("✓ Tarea completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
