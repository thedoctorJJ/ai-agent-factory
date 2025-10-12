from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid
import httpx
import asyncio

router = APIRouter()

# Pydantic models


class AgentCreate(BaseModel):
    name: str
    description: str
    purpose: str
    tools: List[str] = []
    prompts: List[str] = []


class AgentRegistration(BaseModel):
    """Model for Devin AI to register deployed agents"""
    name: str
    description: str
    purpose: str
    version: str = "1.0.0"
    repository_url: str
    deployment_url: str
    health_check_url: str
    prd_id: Optional[str] = None
    devin_task_id: Optional[str] = None
    capabilities: List[str] = []
    configuration: dict = {}


class AgentResponse(BaseModel):
    id: str
    name: str
    description: str
    purpose: str
    version: str
    tools: List[str]
    prompts: List[str]
    status: str
    repository_url: Optional[str] = None
    deployment_url: Optional[str] = None
    health_check_url: Optional[str] = None
    prd_id: Optional[str] = None
    devin_task_id: Optional[str] = None
    capabilities: List[str] = []
    configuration: dict = {}
    last_health_check: Optional[datetime] = None
    health_status: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    purpose: Optional[str] = None
    version: Optional[str] = None
    tools: Optional[List[str]] = None
    prompts: Optional[List[str]] = None
    status: Optional[str] = None
    repository_url: Optional[str] = None
    deployment_url: Optional[str] = None
    health_check_url: Optional[str] = None
    capabilities: Optional[List[str]] = None
    configuration: Optional[dict] = None


# In-memory storage for demo (replace with Supabase in production)
agents_db = {}


@router.get("/agents", response_model=List[AgentResponse])
async def get_agents():
    """Get all agents"""
    return list(agents_db.values())


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get a specific agent by ID"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents_db[agent_id]


@router.post("/agents", response_model=AgentResponse)
async def create_agent(agent: AgentCreate):
    """Create a new agent"""
    agent_id = str(uuid.uuid4())
    now = datetime.utcnow()

    new_agent = AgentResponse(
        id=agent_id,
        name=agent.name,
        description=agent.description,
        purpose=agent.purpose,
        tools=agent.tools,
        prompts=agent.prompts,
        status="created",
        created_at=now,
        updated_at=now
    )

    agents_db[agent_id] = new_agent
    return new_agent


@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent_update: AgentUpdate):
    """Update an existing agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")

    existing_agent = agents_db[agent_id]
    update_data = agent_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_agent, field, value)

    existing_agent.updated_at = datetime.utcnow()
    agents_db[agent_id] = existing_agent

    return existing_agent


@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")

    del agents_db[agent_id]
    return {"message": "Agent deleted successfully"}


@router.post("/agents/register", response_model=AgentResponse)
async def register_agent(agent_registration: AgentRegistration):
    """Register an agent created by Devin AI"""
    agent_id = str(uuid.uuid4())
    now = datetime.utcnow()

    # Create new agent from registration data
    new_agent = AgentResponse(
        id=agent_id,
        name=agent_registration.name,
        description=agent_registration.description,
        purpose=agent_registration.purpose,
        version=agent_registration.version,
        tools=[],  # Will be populated from capabilities
        prompts=[],  # Will be populated from configuration
        status="deployed",
        repository_url=agent_registration.repository_url,
        deployment_url=agent_registration.deployment_url,
        health_check_url=agent_registration.health_check_url,
        prd_id=agent_registration.prd_id,
        devin_task_id=agent_registration.devin_task_id,
        capabilities=agent_registration.capabilities,
        configuration=agent_registration.configuration,
        last_health_check=None,
        health_status="unknown",
        created_at=now,
        updated_at=now
    )

    # Store agent
    agents_db[agent_id] = new_agent

    # Perform initial health check
    await perform_health_check(agent_id)

    return new_agent


@router.get("/agents/{agent_id}/health")
async def get_agent_health(agent_id: str):
    """Get health status of a deployed agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = agents_db[agent_id]

    if not agent.health_check_url:
        return {
            "agent_id": agent_id,
            "status": "no_health_check_url",
            "message": "Agent has no health check URL configured"
        }

    # Perform health check
    health_status = await check_agent_health(agent.health_check_url)

    # Update agent health status
    agent.last_health_check = datetime.utcnow()
    agent.health_status = health_status["status"]
    agents_db[agent_id] = agent

    return {
        "agent_id": agent_id,
        "agent_name": agent.name,
        "health_check_url": agent.health_check_url,
        "last_checked": agent.last_health_check,
        "status": health_status["status"],
        "details": health_status.get("details", {}),
        "response_time_ms": health_status.get("response_time_ms", 0)
    }


@router.post("/agents/{agent_id}/health-check")
async def trigger_health_check(agent_id: str):
    """Manually trigger a health check for an agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")

    await perform_health_check(agent_id)
    agent = agents_db[agent_id]

    return {
        "agent_id": agent_id,
        "status": agent.health_status,
        "last_checked": agent.last_health_check
    }


@router.get("/agents/{agent_id}/metrics")
async def get_agent_metrics(agent_id: str):
    """Get metrics for a deployed agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = agents_db[agent_id]

    # This would typically fetch from the agent's metrics endpoint
    # For now, return basic metrics
    return {
        "agent_id": agent_id,
        "agent_name": agent.name,
        "status": agent.status,
        "health_status": agent.health_status,
        "last_health_check": agent.last_health_check,
        "deployment_url": agent.deployment_url,
        "repository_url": agent.repository_url,
        "version": agent.version,
        "capabilities": agent.capabilities,
        "created_at": agent.created_at,
        "updated_at": agent.updated_at
    }


async def perform_health_check(agent_id: str):
    """Perform health check and update agent status"""
    if agent_id not in agents_db:
        return

    agent = agents_db[agent_id]

    if not agent.health_check_url:
        agent.health_status = "no_health_check_url"
        agent.last_health_check = datetime.utcnow()
        agents_db[agent_id] = agent
        return

    health_status = await check_agent_health(agent.health_check_url)

    agent.last_health_check = datetime.utcnow()
    agent.health_status = health_status["status"]
    agents_db[agent_id] = agent


async def check_agent_health(health_check_url: str) -> dict:
    """Check the health of an agent via its health check URL"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            start_time = datetime.utcnow()
            response = await client.get(health_check_url)
            end_time = datetime.utcnow()

            response_time_ms = (end_time - start_time).total_seconds() * 1000

            if response.status_code == 200:
                try:
                    health_data = response.json()
                    return {
                        "status": "healthy",
                        "details": health_data,
                        "response_time_ms": response_time_ms
                    }
                except BaseException:
                    return {
                        "status": "healthy",
                        "details": {"message": "Health check passed"},
                        "response_time_ms": response_time_ms
                    }
            else:
                return {
                    "status": "unhealthy",
                    "details": {
                        "status_code": response.status_code,
                        "message": "Health check failed"},
                    "response_time_ms": response_time_ms}
    except httpx.TimeoutException:
        return {
            "status": "timeout",
            "details": {"message": "Health check timed out"},
            "response_time_ms": 10000
        }
    except Exception as e:
        return {
            "status": "error",
            "details": {"message": str(e)},
            "response_time_ms": 0
        }
