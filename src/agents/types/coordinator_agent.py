"""
Agente coordinador para orquestar múltiples agentes.
Delega tareas y sintetiza resultados.
"""

from typing import List, Dict, Any
from loguru import logger

from ..base_agent import BaseAgent, AgentConfig
from ...core.ollama_client import OllamaClient


class CoordinatorAgent(BaseAgent):
    """Agente coordinador para sistemas multi-agente."""
    
    DEFAULT_SYSTEM_PROMPT = """Eres un agente coordinador experto en gestión de tareas complejas y delegación.

Tus responsabilidades:
- Analizar tareas complejas y dividirlas en subtareas
- Determinar qué agente especializado es mejor para cada subtarea
- Coordinar múltiples agentes para lograr objetivos
- Sintetizar resultados de diferentes agentes
- Asegurar coherencia y calidad en el resultado final

Cuando coordines:
1. Desglose la tarea principal en pasos manejables
2. Identifica las habilidades necesarias para cada paso
3. Asigna tareas a los agentes apropiados
4. Integra los resultados de forma coherente
5. Verifica que se cumplan todos los objetivos

Agentes disponibles:
- Researcher: Investigación y análisis profundo
- Coder: Programación y desarrollo de software
- ...otros pueden ser añadidos

Sé estratégico, eficiente y orientado a resultados."""
    
    def __init__(
        self,
        client: OllamaClient,
        model: str = "llama3.2",
        temperature: float = 0.5,
        custom_system_prompt: str = None
    ):
        """
        Initialize CoordinatorAgent.
        
        Args:
            client: Cliente de Ollama
            model: Modelo a usar (por defecto Llama 3.2 para coordinación)
            temperature: Temperatura para generación
            custom_system_prompt: System prompt personalizado
        """
        config = AgentConfig(
            name="Coordinator",
            model=model,
            system_prompt=custom_system_prompt or self.DEFAULT_SYSTEM_PROMPT,
            temperature=temperature,
            max_tokens=3072,
            description="Agente coordinador para orquestación multi-agente"
        )
        
        super().__init__(config, client)
        self.available_agents: Dict[str, BaseAgent] = {}
        logger.info(f"CoordinatorAgent initialized with model {model}")
    
    def register_agent(self, agent: BaseAgent):
        """
        Registra un agente disponible para coordinación.
        
        Args:
            agent: Agente a registrar
        """
        self.available_agents[agent.config.name] = agent
        logger.info(f"Agent {agent.config.name} registered with coordinator")
    
    async def plan_task(self, task: str) -> Dict[str, Any]:
        """
        Planifica cómo abordar una tarea compleja.
        
        Args:
            task: Tarea compleja a planificar
            
        Returns:
            Plan de ejecución con subtareas y agentes asignados
        """
        available = list(self.available_agents.keys())
        capabilities = {}
        for name, agent in self.available_agents.items():
            capabilities[name] = agent.get_capabilities()
        
        planning_task = f"""Analiza la siguiente tarea compleja y genera un plan de ejecución:

Tarea: {task}

Agentes disponibles y sus capacidades:
{self._format_capabilities(capabilities)}

Genera un plan estructurado que incluya:
1. Desglose de la tarea en subtareas
2. Agente recomendado para cada subtarea
3. Orden de ejecución
4. Cómo integrar los resultados

Formato de respuesta:
SUBTAREA 1: [descripción]
AGENTE: [nombre del agente]
RAZON: [por qué este agente]

SUBTAREA 2: ...
"""
        
        result = await self.run(planning_task)
        
        # TODO: Parsear el resultado en una estructura
        return {
            "plan": result,
            "task": task
        }
    
    async def delegate_and_synthesize(
        self,
        task: str,
        agent_tasks: Dict[str, List[str]]
    ) -> str:
        """
        Delega subtareas a agentes y sintetiza resultados.
        
        Args:
            task: Tarea principal
            agent_tasks: Diccionario de {nombre_agente: [lista de subtareas]}
            
        Returns:
            Resultado sintetizado
        """
        results = {}
        
        # Ejecutar tareas en cada agente
        for agent_name, subtasks in agent_tasks.items():
            if agent_name not in self.available_agents:
                logger.warning(f"Agent {agent_name} not available, skipping")
                continue
            
            agent = self.available_agents[agent_name]
            agent_results = []
            
            for subtask in subtasks:
                logger.info(f"Delegating to {agent_name}: {subtask[:50]}...")
                result = await agent.run(subtask)
                agent_results.append(result)
            
            results[agent_name] = agent_results
        
        # Sintetizar resultados
        synthesis_task = f"""Sintetiza los siguientes resultados de diferentes agentes:

Tarea Original: {task}

Resultados por agente:
{self._format_results(results)}

Genera un resultado final coherente y completo que integre toda la información."""
        
        final_result = await self.run(synthesis_task)
        return final_result
    
    def _format_capabilities(self, capabilities: Dict[str, List[str]]) -> str:
        """Formatea las capacidades de los agentes para el prompt."""
        formatted = []
        for agent, caps in capabilities.items():
            caps_str = ", ".join(caps)
            formatted.append(f"- {agent}: {caps_str}")
        return "\n".join(formatted)
    
    def _format_results(self, results: Dict[str, List[str]]) -> str:
        """Formatea los resultados de los agentes para el prompt."""
        formatted = []
        for agent, agent_results in results.items():
            formatted.append(f"\n=== {agent.upper()} ===")
            for i, result in enumerate(agent_results, 1):
                formatted.append(f"\nSubtarea {i}:\n{result}\n")
        return "\n".join(formatted)
    
    def get_capabilities(self) -> List[str]:
        """Retorna las capacidades del agente."""
        return [
            "Planificación de tareas complejas",
            "Delegación a agentes especializados",
            "Síntesis de resultados",
            "Coordinación multi-agente",
            "Optimización de flujos de trabajo"
        ]
    
    def list_available_agents(self) -> List[str]:
        """Retorna lista de agentes disponibles."""
        return list(self.available_agents.keys())
