import asyncio
from src.core.ollama_client import OllamaClient

async def main():
    print("Conectando a Ollama...")
    client = OllamaClient()
    
    print("Generando respuesta con llama3.2...")
    try:
        response = await client.generate(
            model="llama3.2", 
            prompt="Reply with exactly 'OK SYSTEM WORKING' if you can read this.",
            temperature=0.1
        )
        print(f"Respuesta del modelo: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
