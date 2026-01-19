"""
Agente especializado en investigación y análisis profundo.
Utiliza razonamiento avanzado para analizar información compleja.
"""

from typing import List
from loguru import logger

from ..base_agent import BaseAgent, AgentConfig
from ...core.ollama_client import OllamaClient


class ResearcherAgent(BaseAgent):
    """Agente de investigación con capacidades de razon amiento profundo."""
    
    DEFAULT_SYSTEM_PROMPT = """Eres un agente de investigación experto con capacidades avanzadas de análisis y razonamiento.

Tus responsabilidades:
- Analizar información compleja y extraer insights clave
- Realizar investigación exhaustiva sobre temas dados
- Proporcionar razonamiento paso a paso (chain-of-thought)
- Sintetizar información de múltiples fuentes
- Identificar patrones, tendencias y relaciones

Cuando investigues:
1. Descompón el problema en partes manejables
2. Analiza cada aspecto sistemáticamente
3. Proporciona evidencia para tus conclusiones
4. Presenta resultados de forma clara y estructurada

Sé riguroso, objetivo y exhaustivo en tus análisis."""
    
    def __init__(
        self,
        client: OllamaClient,
        model: str = "deepseek-r1:8b",
        temperature: float = 0.7,
        custom_system_prompt: str = None
    ):
        """
        Initialize ResearcherAgent.
        
        Args:
            client: Cliente de Ollama
            model: Modelo a usar (por defecto DeepSeek-R1 para razonamiento)
            temperature: Temperatura para generación
            custom_system_prompt: System prompt personalizado
        """
        config = AgentConfig(
            name="Researcher",
            model=model,
            system_prompt=custom_system_prompt or self.DEFAULT_SYSTEM_PROMPT,
            temperature=temperature,
            max_tokens=4096,  # Más tokens para análisis extensos
            description="Agente de investigación y análisis profundo"
        )
        
        super().__init__(config, client)
        logger.info(f"ResearcherAgent initialized with model {model}")
    
    async def research(self, topic: str, depth: str = "medium") -> str:
        """
        Realiza investigación sobre un tema.
        
        Args:
            topic: Tema a investigar
            depth: Profundidad del análisis ("shallow", "medium", "deep")
            
        Returns:
            Reporte de investigación
        """
        depth_instructions = {
            "shallow": "Proporciona un resumen breve y conciso.",
            "medium": "Proporciona un análisis moderadamente detallado con puntos clave.",
            "deep": "Realiza un análisis exhaustivo con razonamiento paso a paso."
        }
        
        instruction = depth_instructions.get(depth, depth_instructions["medium"])
        
        task = f"""Investiga el siguiente tema: {topic}

{instruction}

Estructura tu respuesta:
1. Resumen ejecutivo
2. Análisis detallado
3. Conclusiones clave
4. Implicaciones"""
        
        return await self.run(task)
    
    async def analyze_document(self, document: str, questions: List[str] = None) -> str:
        """
        Analiza un documento y responde preguntas.
        
        Args:
            document: Texto del documento
            questions: Preguntas específicas sobre el documento
            
        Returns:
            Análisis del documento
        """
        if questions:
            questions_str = "\n".join([f"- {q}" for q in questions])
            task = f"""Analiza el siguiente documento y responde las preguntas:

Documento:
{document}

Preguntas:
{questions_str}

Proporciona análisis detallado para cada pregunta."""
        else:
            task = f"""Analiza el siguiente documento:

{document}

Proporciona:
1. Resumen del contenido
2. Ideas principales
3. Puntos clave para recordar
4. Implicaciones o aplicaciones"""
        
        return await self.run(task)
    
    async def compare_and_contrast(self, item1: str, item2: str, criteria: List[str] = None) -> str:
        """
        Compara y contrasta dos elementos.
        
        Args:
            item1: Primer elemento
            item2: Segundo elemento
            criteria: Criterios específicos de comparación
            
        Returns:
            Análisis comparativo
        """
        if criteria:
            criteria_str = "\n".join([f"- {c}" for c in criteria])
            task = f"""Compara y contrasta:

Elemento 1: {item1}
Elemento 2: {item2}

Criterios de comparación:
{criteria_str}

Analiza las similitudes, diferencias y proporciona conclusiones."""
        else:
            task = f"""Compara y contrasta:

Elemento 1: {item1}
Elemento 2: {item2}

Analiza las similitudes, diferencias, ventajas y desventajas de cada uno."""
        
        return await self.run(task)
    
    def get_capabilities(self) -> List[str]:
        """Retorna las capacidades del agente."""
        return [
            "Investigación profunda",
            "Análisis de documentos",
            "Razonamiento chain-of-thought",
            "Comparación y contraste",
            "Síntesis de información",
            "Identificación de patrones"
        ]
