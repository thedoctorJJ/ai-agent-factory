from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import configuration
from .config import config

# Import routers
from .routers import agents, prds, health, devin_integration

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


@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Agent Factory",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
