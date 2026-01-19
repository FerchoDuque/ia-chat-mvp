"""
Clase base para todos los agentes del sistema.
Proporciona funcionalidad común y estructura para agentes especializados.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from loguru import logger

from ..core.ollama_client import OllamaClient


@dataclass
class AgentConfig:
    """Configuración de un agente."""
    name: str
    model: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: Optional[int] = 2048
    description: str = ""


class BaseAgent(ABC):
    """Clase base para todos los agentes."""
    
    def __init__(
        self,
        config: AgentConfig,
        client: OllamaClient
    ):
        """
        Initialize el agente.
        
        Args:
            config: Configuración del agente
            client: Cliente de Ollama
        """
        self.config = config
        self.client = client
        self.conversation_history: List[Dict[str, str]] = []
        logger.info(f"Agent initialized: {self.config.name} using model {self.config.model}")
    
    async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Ejecuta el agente con una tarea.
        
        Args:
            task: Tarea a ejecutar
            context: Contexto adicional opcional
            
        Returns:
            Resultado de la ejecución
        """
        logger.info(f"Agent {self.config.name} starting task")
        
        # Preparar el prompt
        prompt = self._prepare_prompt(task, context)
        
        # Ejecutar generación
        try:
            response = await self.client.generate(
                model=self.config.model,
                prompt=prompt,
                system=self.config.system_prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Guardar en historial
            self.conversation_history.append({
                "role": "user",
                "content": task
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            logger.info(f"Agent {self.config.name} completed task")
            return response
            
        except Exception as e:
            logger.error(f"Agent {self.config.name} failed: {e}")
            raise
    
    async def chat(self, message: str) -> str:
        """
        Conversación con el agente manteniendo historial.
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Respuesta del agente
        """
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        try:
            response_data = await self.client.chat(
                model=self.config.model,
                messages=self.conversation_history,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Extraer el mensaje de la respuesta
            if "message" in response_data:
                response = response_data["message"].get("content", "")
            else:
                response = str(response_data)
            
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Chat error in {self.config.name}: {e}")
            raise
    
    def _prepare_prompt(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Prepara el prompt para el modelo.
        Puede ser sobrescrito por subclases para personalización.
        
        Args:
            task: Tarea principal
            context: Contexto adicional
            
        Returns:
            Prompt completo
        """
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            return f"Context:\n{context_str}\n\nTask:\n{task}"
        return task
    
    def reset_conversation(self):
        """Limpia el historial de conversación."""
        self.conversation_history = []
        logger.info(f"Conversation history reset for {self.config.name}")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Retorna el historial de conversación."""
        return self.conversation_history.copy()
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Retorna las capacidades del agente.
        Debe ser implementado por cada subclase.
        
        Returns:
            Lista de capacidades
        """
        pass
