from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import configuration
from .config import config

# Import routers
from .routers import agents, prds, health, devin_integration, mcp_integration

# Import services for clear all endpoint
from .services.agent_service import agent_service
from .services.prd_service import prd_service

app = FastAPI(
    title="AI Agent Factory",
    description="A repeatable, voice-first, AI-driven platform for creating modular agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(agents.router, prefix="/api/v1", tags=["agents"])
app.include_router(prds.router, prefix="/api/v1", tags=["prds"])
app.include_router(devin_integration.router, prefix="/api/v1", tags=["devin"])
app.include_router(mcp_integration.router, prefix="/api/v1", tags=["mcp"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Agent Factory",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.delete("/api/v1/clear-all")
async def clear_all_data():
    """Clear all agents and PRDs from the system."""
    try:
        # Clear agents first (to avoid foreign key constraints)
        agents_result = await agent_service.clear_all_agents()
        
        # Then clear PRDs
        prds_result = await prd_service.clear_all_prds()
        
        return {
            "message": "All data cleared successfully",
            "agents": agents_result,
            "prds": prds_result
        }
    except Exception as e:
        return {
            "message": f"Error clearing data: {str(e)}",
            "error": True
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
