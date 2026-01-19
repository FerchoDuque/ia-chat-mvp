# Guía de Ingeniería de Prompts

Esta guía te ayudará a obtener los mejores resultados posibles al interactuar con los agentes de IA del sistema.

## Principios Fundamentales

Para obtener respuestas precisas y útiles, sigue el principio **CCC**:

1.  **Contexto**: ¿Quién eres? ¿Cuál es tu objetivo? ¿Qué información previa es relevante?
2.  **Claridad**: Sé específico sobre lo que quieres. Evita ambigüedades.
3.  **Restricciones**: Define el formato, la longitud, el estilo y lo que **no** quieres.

## Estructura Recomendada (CO-STAR)

Una de las mejores estructuras para prompts complejos es **CO-STAR**:

-   **C (Context)**: Contexto de la situación.
-   **O (Objective)**: Qué quieres lograr.
-   **S (Style)**: Estilo de redacción (formal, técnico, creativo).
-   **T (Tone)**: Tono emocional (serio, humorístico, empático).
-   **A (Audience)**: Para quién es la respuesta.
-   **R (Response)**: Formato de salida deseado (tabla, lista, código).

---

## Patrones por Agente

### 1. Researcher Agent (Investigador)
Este agente usa `DeepSeek-R1`, optimizado para razonamiento profundo.

**Consejos:**
-   Pídele explícitamente que "piense paso a paso".
-   Especifica la profundidad (`shallow`, `medium`, `deep`).
-   Pide citas o evidencias si son necesarias.

**Plantilla:**
> "Actúa como un experto en [TEMA]. Investiga sobre [SUBTEMA].
>
> **Objetivo**: Proporcionar un análisis exhaustivo de [ASPECTO ESPECÍFICO].
> **Formato**: Reporte estructurado con Resumen Ejecutivo, Puntos Clave y Conclusión.
> **Profundidad**: Deep (usa Chain-of-Thought).
> **Restricción**: Cita fuentes o principios teóricos cuando sea posible."

### 2. Coder Agent (Programador)
Este agente usa `Qwen 2.5`, excelente para generación de código.

**Consejos:**
-   Especifica el lenguaje y la versión (ej. Python 3.10+, React 18).
-   Indica qué librerías usar o evitar.
-   Pide manejo de errores explícito.

**Plantilla:**
> "Eres un Ingeniero de Software Senior. Escribe un script en [LENGUAJE] para [TAREA].
>
> **Requisitos Técnicos**:
> - Usa la librería [XYZ].
> - Implementa manejo de errores robusto con try/catch.
> - Sigue principios SOLID.
>
> **Salida**: Código comentado + Breve explicación de la lógica."

### 3. Coordinator Agent (Coordinador)
Este agente usa `Llama 3.2` para orquestación.

**Consejos:**
-   Úsalo para tareas que requieren múltiples pasos o habilidades.
-   Define claramente el "Definition of Done".

**Plantilla:**
> "Tengo un proyecto complejo: [DESCRIPCIÓN PROYECTO].
>
> **Tu tarea**:
> 1. Desglosa este proyecto en pasos manejables.
> 2. Identifica qué agente (Researcher o Coder) debe hacer cada paso.
> 3. Crea un plan de ejecución secuencial.
>
> **Salida**: Lista de tareas numerada con asignacion de agentes."

---

## Cheatsheet de Mejoras Rápidas

| Problema | Solución en Prompt |
| :--- | :--- |
| **Respuesta muy vaga** | "Sé específico y detalla X, Y, Z." |
| **Alucina información** | "Responde solo basándote en el contexto provisto. Si no sabes, di 'No lo sé'." |
| **Formato incorrecto** | "Responde estrictamente en formato JSON/Markdown sin texto adicional." |
| **Código con bugs** | "Revisa tu código, considera los casos borde A y B, y asegúrate de que compile." |
| **Muy verboso** | "Sé conciso. Limítate a 100 palabras." |

## Ejemplo "Meta-Prompt"
*Usa este prompt para que el agente te ayude a escribir un mejor prompt:*

> "Quiero pedirle a una IA que haga [TAREA], pero no sé cómo estructurarlo para obtener el mejor resultado. Actúa como un experto en Prompt Engineering y escribe el mejor prompt posible para esta tarea, usando la estructura CO-STAR."
