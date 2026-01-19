from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
from loguru import logger

from src.core.ollama_client import OllamaClient
from src.core.model_manager import ModelManager
from src.agents.types.researcher_agent import ResearcherAgent
from src.agents.types.coder_agent import CoderAgent
from src.agents.types.coordinator_agent import CoordinatorAgent

app = FastAPI(title="Agent System API", version="1.0.0")

# CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
ollama_client: Optional[OllamaClient] = None
model_manager: Optional[ModelManager] = None
agents: Dict[str, Any] = {}

class ChatRequest(BaseModel):
    agent_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

class TaskRequest(BaseModel):
    task: str
    requirements: Optional[List[str]] = None

class AgentInfo(BaseModel):
    id: str
    name: str
    description: str
    capabilities: List[str]
    model: str

@app.on_event("startup")
async def startup_event():
    global ollama_client, model_manager, agents
    
    logger.info("Starting up Agent System API...")
    ollama_client = OllamaClient()
    
    # Verify connection
    if not await ollama_client.check_health():
        logger.warning("Could not connect to Ollama. Ensure it is running.")
    
    model_manager = ModelManager(ollama_client)
    
    # Initialize Agents
    # Note: In a real app, we might load these dynamically or on demand
    agents["researcher"] = ResearcherAgent(ollama_client)
    agents["coder"] = CoderAgent(ollama_client)
    agents["coordinator"] = CoordinatorAgent(ollama_client)
    
    # Register agents to coordinator
    agents["coordinator"].register_agent(agents["researcher"])
    agents["coordinator"].register_agent(agents["coder"])
    
    logger.info("Agents initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    if ollama_client:
        await ollama_client.close()
    logger.info("Agent System API shutdown complete")

@app.get("/api/health")
async def health_check():
    ollama_status = await ollama_client.check_health() if ollama_client else False
    return {"status": "ok", "ollama_connected": ollama_status}

@app.get("/api/agents", response_model=List[AgentInfo])
async def list_agents():
    return [
        AgentInfo(
            id=aid,
            name=agent.config.name,
            description=agent.config.description,
            capabilities=agent.get_capabilities(),
            model=agent.config.model
        )
        for aid, agent in agents.items()
    ]

@app.post("/api/chat")
async def chat_with_agent(request: ChatRequest):
    agent_id = request.agent_id.lower()
    
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    try:
        agent = agents[agent_id]
        response = await agent.chat(request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/task")
async def submit_task(request: TaskRequest):
    """
    Submits a complex task to the Coordinator Agent.
    """
    if "coordinator" not in agents:
        raise HTTPException(status_code=503, detail="Coordinator agent not available")
    
    try:
        coordinator = agents["coordinator"]
        
        # Determine if we should Plan or Execution directly based on task complexity
        # For simplicity, we'll ask the coordinator to plan and then execute, 
        # but for now let's just use the 'run' method which is generic.
        # Ideally, we would expose plan_task and delegate_and_synthesize specific endpoints,
        # but the single 'run' entry point is easier for specific simple interactions.
        
        # However, for a generic task, we can wrap it in a planning prompt or just pass it.
        # Let's assume the user wants the result.
        
        response = await coordinator.run(request.task)
        return {"response": response}
        
    except Exception as e:
        logger.error(f"Error in task endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.server.app:app", host="0.0.0.0", port=8000, reload=True)
