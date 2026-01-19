"""
Configuración centralizada de la aplicación usando Pydantic Settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # Ollama Configuration
    ollama_host: str = Field(default="http://127.0.0.1:11434", env="OLLAMA_HOST")
    ollama_models_dir: Path = Field(
        default=Path("D:/Proyectos/WORK/Agentes-practica/models"),
        env="OLLAMA_MODELS"
    )
    ollama_num_parallel: int = Field(default=2, env="OLLAMA_NUM_PARALLEL")
    ollama_max_loaded_models: int = Field(default=2, env="OLLAMA_MAX_LOADED_MODELS")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_dir: Path = Field(
        default=Path("D:/Proyectos/WORK/Agentes-practica/logs"),
        env="LOG_DIR"
    )
    
    # Application Settings
    project_root: Path = Field(default=Path("D:/Proyectos/WORK/Agentes-practica"))
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Singleton instance
settings = Settings()
