"""Paquete core del sistema de agentes."""

from .ollama_client import OllamaClient
from .model_manager import ModelManager

__all__ = ["OllamaClient", "ModelManager"]
