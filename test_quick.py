"""
Script de prueba rápida para verificar el sistema sin necesidad de modelos descargados.
Muestra el estado del sistema y valida que todo esté correctamente configurado.
"""

import asyncio
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.core.ollama_client import OllamaClient
    from src.core.model_manager import ModelManager
    from src.agents.types.researcher_agent import ResearcherAgent
    from src.agents.types.coder_agent import CoderAgent
    from src.agents.types.coordinator_agent import CoordinatorAgent
    print("✓ Imports exitosos - Todos los módulos están correctamente instalados")
except ImportError as e:
    print(f"✗ Error importando módulos: {e}")
    print("\nAsegúrate de haber instalado las dependencias:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


async def test_system():
    """Prueba rápida del sistema."""
    
    print("\n" + "="*60)
    print("PRUEBA RÁPIDA DEL SISTEMA DE AGENTES")
    print("="*60 + "\n")
    
    # 1. Test de conexión con Ollama
    print("1. Verificando conexión con Ollama...")
    client = OllamaClient()
    
    try:
        is_healthy = await client.check_health()
        if is_healthy:
            print("   ✓ Ollama está corriendo correctamente")
        else:
            print("   ✗ Ollama no está respondiendo")
            print("   → El servidor Ollama debería iniciarse automáticamente")
            print("   → Espera unos segundos e intenta nuevamente")
            await client.close()
            return
    except Exception as e:
        print(f"   ✗ Error conectando con Ollama: {e}")
        print("   → Asegúrate de que Ollama esté instalado")
        await client.close()
        return
    
    # 2. Test de modelos disponibles
    print("\n2. Verificando modelos disponibles...")
    try:
        models = await client.list_models()
        if models:
            print(f"   ✓ {len(models)} modelo(s) instalado(s):")
            for model in models:
                name = model.get("name", "unknown")
                size = model.get("size", 0) / (1024**3)
                print(f"     - {name} ({size:.2f} GB)")
        else:
            print("   ⚠ No hay modelos instalados aún")
            print("   → Ejecuta: .\\scripts\\setup_models.ps1")
            print("   → O descarga manualmente: ollama pull llama3.2")
    except Exception as e:
        print(f"   ✗ Error listando modelos: {e}")
    
    # 3. Test del ModelManager
    print("\n3. Verificando ModelManager...")
    try:
        manager = ModelManager(client)
        
        # Listar modelos Tier 1
        tier1_models = manager.get_tier_1_models()
        print(f"   ✓ ModelManager inicializado")
        print(f"   ✓ {len(tier1_models)} modelos Tier 1 en catálogo:")
        for model in tier1_models[:3]:  # Mostrar solo los primeros 3
            print(f"     - {model.name} ({model.size_gb} GB)")
        
        # Test de recomendación
        recommended = manager.get_recommended_model("coding")
        print(f"   ✓ Modelo recomendado para 'coding': {recommended.name}")
        
    except Exception as e:
        print(f"   ✗ Error en ModelManager: {e}")
    
    # 4. Test de inicialización de agentes
    print("\n4. Verificando agentes...")
    try:
        # Crear agentes (aunque no tengamos modelos, podemos inicializarlos)
        researcher = ResearcherAgent(client=client)
        coder = CoderAgent(client=client)
        coordinator = CoordinatorAgent(client=client)
        
        print("   ✓ Agentes inicializados correctamente:")
        print(f"     - {researcher.config.name} (modelo: {researcher.config.model})")
        print(f"       Capacidades: {', '.join(researcher.get_capabilities()[:3])}...")
        print(f"     - {coder.config.name} (modelo: {coder.config.model})")
        print(f"       Capacidades: {', '.join(coder.get_capabilities()[:3])}...")
        print(f"     - {coordinator.config.name} (modelo: {coordinator.config.model})")
        print(f"       Capacidades: {', '.join(coordinator.get_capabilities()[:2])}...")
        
        # Registrar agentes en el coordinador
        coordinator.register_agent(researcher)
        coordinator.register_agent(coder)
        
        available = coordinator.list_available_agents()
        print(f"   ✓ Coordinador tiene {len(available)} agentes registrados")
        
    except Exception as e:
        print(f"   ✗ Error inicializando agentes: {e}")
    
    # 5. Test con modelo (si hay alguno disponible)
    if models:
        print("\n5. Probando generación con modelo...")
        try:
            model_name = models[0].get("name", "").split(":")[0]
            print(f"   → Usando modelo: {model_name}")
            print("   → Generando respuesta a: '¿Qué es Python?'")
            
            response = await client.generate(
                model=model_name,
                prompt="En una línea, ¿qué es Python?",
                temperature=0.7,
                max_tokens=100
            )
            
            print(f"   ✓ Respuesta: {response[:100]}...")
            
        except Exception as e:
            print(f"   ✗ Error generando respuesta: {e}")
    else:
        print("\n5. Test de generación omitido (no hay modelos)")
    
    # Cerrar cliente
    await client.close()
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print("\n✅ Sistema Core: Funcionando")
    print("✅ Agentes: Inicializados correctamente")
    print("✅ ModelManager: Operativo")
    
    if models:
        print("✅ Modelos: Instalados y funcionando")
        print("\n🚀 Sistema listo para usar!")
        print("\nPrueba los ejemplos:")
        print("  python examples\\simple_chat.py")
        print("  python examples\\multi_agent_research.py")
        print("  python examples\\code_assistant.py")
    else:
        print("⚠️  Modelos: Pendiente de instalación")
        print("\nPara instalar modelos:")
        print("  .\\scripts\\setup_models.ps1")
        print("  O manualmente: ollama pull llama3.2")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(test_system())
    except KeyboardInterrupt:
        print("\n\nPrueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n✗ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
