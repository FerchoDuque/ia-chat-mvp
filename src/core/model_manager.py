"""
Gestor de modelos de IA.
Maneja carga/descarga, caché y selección de modelos.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from loguru import logger
import asyncio

from .ollama_client import OllamaClient


class ModelTier(Enum):
    """Tier de modelos disponibles."""
    TIER_1 = "tier_1"  # Uso general
    TIER_2 = "tier_2"  # Especialización
    TIER_3 = "tier_3"  # Ultra-ligeros


@dataclass
class ModelInfo:
    """Información sobre un modelo."""
    name: str
    size_gb: float
    vram_usage_gb: float
    tier: ModelTier
    description: str
    strengths: List[str]
    use_cases: List[str]
    ollama_name: str


class ModelManager:
    """Gestor centralizado de modelos de IA."""
    
    # Catálogo de modelos recomendados
    MODELS_CATALOG = {
        "llama3.2": ModelInfo(
            name="Llama 3.2 8B",
            size_gb=4.7,
            vram_usage_gb=5.5,
            tier=ModelTier.TIER_1,
            description="Excelente balance rendimiento/velocidad, multilingüe",
            strengths=["Razonamiento sólido", "Multilingüe", "Uso general"],
            use_cases=["Agente general", "Chatbot", "Análisis de texto"],
            ollama_name="llama3.2"
        ),
        "mistral": ModelInfo(
            name="Mistral 7B",
            size_gb=4.1,
            vram_usage_gb=4.5,
            tier=ModelTier.TIER_1,
            description="Rápido y eficiente",
            strengths=["Velocidad", "Eficiencia", "Seguimiento de instrucciones"],
            use_cases=["Procesamiento rápido", "Batch processing", "Clasificación"],
            ollama_name="mistral"
        ),
        "deepseek-r1": ModelInfo(
            name="DeepSeek-R1 8B",
            size_gb=4.9,
            vram_usage_gb=5.5,
            tier=ModelTier.TIER_1,
            description="Razonamiento lógico avanzado",
            strengths=["Chain-of-thought", "Razonamiento", "Lógica"],
            use_cases=["Análisis complejo", "Resolución de problemas", "Investigación"],
            ollama_name="deepseek-r1:8b"
        ),
        "phi4": ModelInfo(
            name="Phi-4 14B",
            size_gb=8.0,
            vram_usage_gb=9.0,
            tier=ModelTier.TIER_2,
            description="Razonamiento lógico intensivo",
            strengths=["Análisis legal", "Lógica estructurada", "Investigación"],
            use_cases=["Análisis de documentos", "Investigación profunda"],
            ollama_name="phi4"
        ),
        "qwen2.5": ModelInfo(
            name="Qwen 2.5 7B",
            size_gb=4.7,
            vram_usage_gb=5.5,
            tier=ModelTier.TIER_2,
            description="Excelente multilingüe y coding",
            strengths=["Multilingüe", "Programación", "Razonamiento"],
            use_cases=["Coding assistant", "Traducción", "Soporte multilingüe"],
            ollama_name="qwen2.5:7b"
        ),
        "gemma2": ModelInfo(
            name="Gemma 2 9B",
            size_gb=5.4,
            vram_usage_gb=6.5,
            tier=ModelTier.TIER_2,
            description="Rápido, by Google",
            strengths=["Velocidad", "Eficiencia", "Calidad"],
            use_cases=["Respuesta rápida", "Clasificación", "Análisis"],
            ollama_name="gemma2:9b"
        ),
        "phi3-mini": ModelInfo(
            name="Phi-3 Mini",
            size_gb=2.3,
            vram_usage_gb=2.5,
            tier=ModelTier.TIER_3,
            description="Ultra rápido y ligero",
            strengths=["Velocidad extrema", "Bajo consumo", "Sorprendentemente capaz"],
            use_cases=["Pre-procesamiento", "Clasificación simple", "Routing"],
            ollama_name="phi3:mini"
        ),
        "tinyllama": ModelInfo(
            name="TinyLlama 1.1B",
            size_gb=0.637,
            vram_usage_gb=0.8,
            tier=ModelTier.TIER_3,
            description="Extremadamente ligero",
            strengths=["Mínimo consumo", "Velocidad máxima"],
            use_cases=["Clasificación básica", "Routing de agentes", "Filtrado"],
            ollama_name="tinyllama"
        ),
    }
    
    def __init__(self, client: OllamaClient):
        """
        Initialize ModelManager.
        
        Args:
            client: Cliente de Ollama configurado
        """
        self.client = client
        self._loaded_models: Dict[str, ModelInfo] = {}
        self._available_models: List[str] = []
        logger.info("ModelManager initialized")
    
    async def refresh_available_models(self) -> List[str]:
        """
        Actualiza la lista de modelos disponibles localmente.
        
        Returns:
            Lista de nombres de modelos disponibles
        """
        models = await self.client.list_models()
        self._available_models = [m.get("name", "").split(":")[0] for m in models]
        logger.info(f"Available models refreshed: {len(self._available_models)} found")
        return self._available_models
    
    def get_model_info(self, model_key: str) -> Optional[ModelInfo]:
        """
        Obtiene información de un modelo del catálogo.
        
        Args:
            model_key: Clave del modelo en el catálogo
            
        Returns:
            ModelInfo o None si no existe
        """
        return self.MODELS_CATALOG.get(model_key)
    
    def list_models_by_tier(self, tier: ModelTier) -> List[ModelInfo]:
        """
        Lista modelos por tier.
        
        Args:
            tier: Tier a filtrar
            
        Returns:
            Lista de ModelInfo para el tier especificado
        """
        return [
            info for info in self.MODELS_CATALOG.values()
            if info.tier == tier
        ]
    
    def get_recommended_model(self, use_case: str) -> Optional[ModelInfo]:
        """
        Recomienda un modelo basado en el caso de uso.
        
        Args:
            use_case: Caso de uso (ej: "coding", "research", "chat")
            
        Returns:
            ModelInfo recomendado o None
        """
        use_case_lower = use_case.lower()
        
        # Mapeo de casos de uso a modelos
        use_case_mapping = {
            "coding": "qwen2.5",
            "code": "qwen2.5",
            "programming": "qwen2.5",
            "research": "deepseek-r1",
            "reasoning": "deepseek-r1",
            "analysis": "deepseek-r1",
            "chat": "llama3.2",
            "general": "llama3.2",
            "conversation": "llama3.2",
            "fast": "mistral",
            "quick": "mistral",
            "speed": "mistral",
            "lightweight": "phi3-mini",
            "minimal": "tinyllama",
        }
        
        model_key = use_case_mapping.get(use_case_lower)
        if model_key:
            return self.MODELS_CATALOG.get(model_key)
        
        # Default a Llama 3.2 si no hay match
        logger.warning(f"No specific model for use case '{use_case}', defaulting to llama3.2")
        return self.MODELS_CATALOG.get("llama3.2")
    
    async def ensure_model_available(self, model_key: str) -> bool:
        """
        Asegura que un modelo esté disponible, descargándolo si es necesario.
        
        Args:
            model_key: Clave del modelo en el catálogo
            
        Returns:
            True si el modelo está disponible
        """
        model_info = self.get_model_info(model_key)
        if not model_info:
            logger.error(f"Model {model_key} not found in catalog")
            return False
        
        # Verificar si ya está descargado
        await self.refresh_available_models()
        
        # Buscar por nombre de Ollama
        if any(model_info.ollama_name in m for m in self._available_models):
            logger.info(f"Model {model_key} already available")
            return True
        
        # Descargar el modelo
        logger.info(f"Model {model_key} not found, downloading...")
        success = await self.client.pull_model(model_info.ollama_name)
        
        if success:
            await self.refresh_available_models()
        
        return success
    
    def get_tier_1_models(self) -> List[ModelInfo]:
        """Retorna todos los modelos Tier 1 (recomendados para empezar)."""
        return self.list_models_by_tier(ModelTier.TIER_1)
    
    def get_all_models(self) -> Dict[str, ModelInfo]:
        """Retorna el catálogo completo de modelos."""
        return self.MODELS_CATALOG.copy()
    
    async def get_model_stats(self, model_key: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene estadísticas de un modelo desde Ollama.
        
        Args:
            model_key: Clave del modelo
            
        Returns:
            Estadísticas del modelo o None
        """
        model_info = self.get_model_info(model_key)
        if not model_info:
            return None
        
        return await self.client.get_model_info(model_info.ollama_name)
