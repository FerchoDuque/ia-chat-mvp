"""
Agente especializado en programación y desarrollo de software.
Experto en generación, revisión y análisis de código.
"""

from typing import List, Optional
from loguru import logger

from ..base_agent import BaseAgent, AgentConfig
from ...core.ollama_client import OllamaClient


class CoderAgent(BaseAgent):
    """Agente de programación con expertise en múltiples lenguajes."""
    
    DEFAULT_SYSTEM_PROMPT = """Eres un agente de programación experto con conocimiento profundo en múltiples lenguajes y tecnologías.

Tus responsabilidades:
- Generar código limpio, eficiente y bien documentado
- Revisar código y sugerir mejoras
- Explicar conceptos de programación
- Debuggear y resolver problemas
- Seguir best practices y patrones de diseño

Cuando escribas código:
1. Usa nombres descriptivos para variables y funciones
2. Incluye comentarios explicativos cuando sea necesario
3. Sigue las convenciones del lenguaje
4. Considera edge cases y manejo de errores
5. Prioriza legibilidad y mantenibilidad

Lenguajes en los que eres experto: Python, JavaScript, TypeScript, Go, Rust, Java, C++, y más."""
    
    def __init__(
        self,
        client: OllamaClient,
        model: str = "qwen2.5:7b",
        temperature: float = 0.3,  # Temperatura baja para código más determinístico
        custom_system_prompt: str = None
    ):
        """
        Initialize CoderAgent.
        
        Args:
            client: Cliente de Ollama
            model: Modelo a usar (por defecto Qwen 2.5 para coding)
            temperature: Temperatura para generación
            custom_system_prompt: System prompt personalizado
        """
        config = AgentConfig(
            name="Coder",
            model=model,
            system_prompt=custom_system_prompt or self.DEFAULT_SYSTEM_PROMPT,
            temperature=temperature,
            max_tokens=4096,
            description="Agente de programación y desarrollo de software"
        )
        
        super().__init__(config, client)
        logger.info(f"CoderAgent initialized with model {model}")
    
    async def generate_code(
        self,
        description: str,
        language: str,
        requirements: Optional[List[str]] = None
    ) -> str:
        """
        Genera código basado en una descripción.
        
        Args:
            description: Descripción de lo que debe hacer el código
            language: Lenguaje de programación
            requirements: Requisitos adicionales
            
        Returns:
            Código generado
        """
        req_str = ""
        if requirements:
            req_str = "\n\nRequisitos adicionales:\n" + "\n".join([f"- {r}" for r in requirements])
        
        task = f"""Genera código en {language} para:

{description}{req_str}

Proporciona:
1. El código completo
2. Explicación de cómo funciona
3. Ejemplos de uso si es relevante"""
        
        return await self.run(task)
    
    async def review_code(self, code: str, language: str) -> str:
        """
        Revisa código y proporciona feedback.
        
        Args:
            code: Código a revisar
            language: Lenguaje de programación
            
        Returns:
            Revisión con sugerencias
        """
        task = f"""Revisa el siguiente código en {language}:

```{language}
{code}
```

Proporciona:
1. Análisis de calidad general
2. Problemas o bugs potenciales
3. Sugerencias de mejora
4. Consideraciones de rendimiento
5. Código mejorado si es necesario"""
        
        return await self.run(task)
    
    async def explain_code(self, code: str, language: str = "auto") -> str:
        """
        Explica qué hace un fragmento de código.
        
        Args:
            code: Código a explicar
            language: Lenguaje de programación
            
        Returns:
            Explicación detallada
        """
        task = f"""Explica qué hace este código:

```{language if language != 'auto' else ''}
{code}
```

Proporciona:
1. Resumen de alto nivel
2. Explicación línea por línea (para código complejo)
3. Casos de uso
4. Posibles edge cases"""
        
        return await self.run(task)
    
    async def debug_code(self, code: str, error: str, language: str) -> str:
        """
        Ayuda a debuggear código con un error.
        
        Args:
            code: Código con el error
            error: Mensaje de error o descripción del problema
            language: Lenguaje de programación
            
        Returns:
            Análisis del error y solución
        """
        task = f"""Debug el siguiente código en {language}:

Código:
```{language}
{code}
```

Error/Problema:
{error}

Proporciona:
1. Causa del error
2. Solución explicada
3. Código corregido
4. Prevención de errores similares"""
        
        return await self.run(task)
    
    async def refactor_code(self, code: str, language: str, goals: List[str] = None) -> str:
        """
        Refactoriza código para mejorar su calidad.
        
        Args:
            code: Código a refactorizar
            language: Lenguaje de programación
            goals: Objetivos de refactorización
            
        Returns:
            Código refactorizado con explicación
        """
        goals_str = ""
        if goals:
            goals_str = "\n\nObjetivos:\n" + "\n".join([f"- {g}" for g in goals])
        else:
            goals_str = "\n\nObjetivos: Mejorar legibilidad, eficiencia y mantenibilidad"
        
        task = f"""Refactoriza el siguiente código en {language}:

```{language}
{code}
```{goals_str}

Proporciona:
1. Código refactorizado
2. Explicación de cambios realizados
3. Beneficios de la refactorización"""
        
        return await self.run(task)
    
    async def write_tests(self, code: str, language: str, framework: str = None) -> str:
        """
        Genera tests para código dado.
        
        Args:
            code: Código para el cual generar tests
            language: Lenguaje de programación
            framework: Framework de testing (ej: pytest, jest)
            
        Returns:
            Tests generados
        """
        framework_str = f" usando {framework}" if framework else ""
        
        task = f"""Genera tests{framework_str} para el siguiente código en {language}:

```{language}
{code}
```

Proporciona:
1. Tests unitarios completos
2. Test cases que cubran diferentes escenarios
3. Edge cases
4. Explicación de qué testea cada caso"""
        
        return await self.run(task)
    
    def get_capabilities(self) -> List[str]:
        """Retorna las capacidades del agente."""
        return [
            "Generación de código",
            "Revisión de código",
            "Explicación de código",
            "Debugging",
            "Refactorización",
            "Generación de tests",
            "Múltiples lenguajes de programación"
        ]
