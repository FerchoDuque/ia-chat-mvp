# Guía de Despliegue con Docker

Esta guía detalla cómo ejecutar el sistema de agentes utilizando Docker y Docker Compose.
Esto permite levantar la aplicación y el servidor Ollama en un entorno aislado y controlado.

## Archivos Necesarios

Para dockerizar la aplicación, debes crear los siguientes archivos en la raíz del proyecto.

### 1. Dockerfile

Crea un archivo llamado `Dockerfile` en la raíz con el siguiente contenido:

```dockerfile
# Usar imagen base ligera de Python
FROM python:3.11-slim

# Evitar archivos .pyc y buffering de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema, incluyendo curl para healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Comando por defecto (ajustar según necesidad, ej: ejecutar un script de prueba o wait loop)
CMD ["tail", "-f", "/dev/null"]
```

### 2. docker-compose.yml

Crea un archivo llamado `docker-compose.yml` en la raíz con el siguiente contenido:

```yaml
services:
  # Servicio de Ollama (Backend LLM)
  ollama:
    image: ollama/ollama:latest
    container_name: agentes_ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    # Descomentar para soporte GPU (requiere NVIDIA Container Toolkit)
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]
    restart: always

  # Aplicación Python
  app:
    build: .
    container_name: agentes_app
    depends_on:
      - ollama
    volumes:
      # Montar código local para desarrollo
      - .:/app
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - LOG_LEVEL=INFO
    # Mantener el contenedor vivo
    command: tail -f /dev/null

volumes:
  ollama_data:
```

## Instrucciones de Uso

1.  **Construir y levantar los servicios:**
    ```bash
    docker-compose up -d --build
    ```

2.  **Verificar que los servicios estén corriendo:**
    ```bash
    docker-compose ps
    ```

3.  **Descargar modelos en Ollama:**
    Como el contenedor de Ollama inicia vacío, necesitas descargar los modelos (esto se guarda en el volumen `ollama_data`).
    ```bash
    docker exec -it agentes_ollama ollama pull llama3.2
    ```

4.  **Ejecutar pruebas dentro del contenedor:**
    ```bash
    docker exec -it agentes_app python examples/simple_chat.py
    ```

## Notas Importantes

*   **Persistencia:** Los modelos descargados se guardan en el volumen de Docker `ollama_data` y persisten entre reinicios.
*   **Networking:** La aplicación se comunica con Ollama a través de la red interna de Docker usando el hostname `ollama` (configurado en `OLLAMA_HOST`).
*   **GPU:** Para inferencia rápida, se recomienda configurar el soporte de GPU descomentando la sección `deploy` en el `docker-compose.yml` (solo Linux/WSL2 con drivers NVIDIA).
