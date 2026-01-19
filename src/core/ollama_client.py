"""
Cliente para interactuar con Ollama.
Wrapper sobre la API HTTP de Ollama para facilitar la comunicación con modelos.
"""

import httpx
import json
from typing import AsyncIterator, Dict, Any, Optional, List
from loguru import logger


class OllamaClient:
    """Cliente para interactuar con el servidor Ollama."""
    
    def __init__(
        self, 
        host: str = "http://localhost:11434",
        timeout: int = 60
    ):
        """
        Initialize Ollama client.
        
        Args:
            host: URL del servidor Ollama
            timeout: Timeout para requests en segundos
        """
        self.host = host.rstrip('/')
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)
        logger.info(f"Ollama client initialized: {self.host}")
    
    async def check_health(self) -> bool:
        """Verifica que el servidor Ollama esté corriendo."""
        try:
            response = await self._client.get(self.host)
            return "Ollama is running" in response.text
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """Lista todos los modelos disponibles localmente."""
        try:
            response = await self._client.get(f"{self.host}/api/tags")
            response.raise_for_status()
            data = response.json()
            models = data.get("models", [])
            logger.info(f"Found {len(models)} models")
            return models
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    async def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> str:
        """
        Genera una respuesta del modelo dado un prompt.
        
        Args:
            model: Nombre del modelo a usar
            prompt: Prompt para el modelo
            system: System prompt opcional
            temperature: Temperatura para generación (0.0 - 1.0)
            max_tokens: Máximo de tokens a generar
            stream: Si retornar respuesta streaming
            
        Returns:
            Respuesta completa del modelo
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature
            }
        }
        
        if system:
            payload["system"] = system
            
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        try:
            response = await self._client.post(
                f"{self.host}/api/generate",
                json=payload
            )
            response.raise_for_status()
            
            if stream:
                # TODO: Implementar streaming
                pass
            else:
                data = response.json()
                return data.get("response", "")
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def generate_stream(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncIterator[str]:
        """
        Genera una respuesta en streaming del modelo.
        
        Args:
            model: Nombre del modelo a usar
            prompt: Prompt para el modelo
            system: System prompt opcional
            temperature: Temperatura para generación
            max_tokens: Máximo de tokens a generar
            
        Yields:
            Chunks de texto de la respuesta
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature
            }
        }
        
        if system:
            payload["system"] = system
            
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        try:
            async with self._client.stream(
                "POST",
                f"{self.host}/api/generate",
                json=payload
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
                            
        except Exception as e:
            logger.error(f"Error in streaming generation: {e}")
            raise
    
    async def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Chat completion usando el endpoint /api/chat de Ollama.
        
        Args:
            model: Nombre del modelo
            messages: Lista de mensajes con formato [{"role": "user", "content": "..."}]
            temperature: Temperatura para generación
            max_tokens: Máximo de tokens a generar
            
        Returns:
            Respuesta del modelo
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        try:
            response = await self._client.post(
                f"{self.host}/api/chat",
                json=payload
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise
    
    async def pull_model(self, model: str) -> bool:
        """
        Descarga un modelo desde el registro de Ollama.
        
        Args:
            model: Nombre del modelo a descargar
            
        Returns:
            True si se descargó exitosamente
        """
        try:
            logger.info(f"Pulling model: {model}")
            
            async with self._client.stream(
                "POST",
                f"{self.host}/api/pull",
                json={"name": model}
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        if "status" in data:
                            logger.debug(f"Pull status: {data['status']}")
            
            logger.info(f"Model {model} pulled successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error pulling model: {e}")
            return False
    
    async def get_model_info(self, model: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información sobre un modelo específico.
        
        Args:
            model: Nombre del modelo
            
        Returns:
            Información del modelo o None si no existe
        """
        try:
            response = await self._client.post(
                f"{self.host}/api/show",
                json={"name": model}
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return None
    
    async def close(self):
        """Cierra el cliente HTTP."""
        await self._client.aclose()
        logger.info("Ollama client closed")
