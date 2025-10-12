"""
Refactored agent router with proper separation of concerns.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from ..models.agent import (
    AgentRegistration, AgentResponse, AgentStatus, AgentHealthStatus,
    AgentListResponse, AgentHealthResponse, AgentMetricsResponse
)
from ..services.agent_service import agent_service

router = APIRouter()


@router.post("/agents", response_model=AgentResponse)
async def create_agent(agent_data: AgentRegistration):
    """Create a new agent."""
    return await agent_service.create_agent(agent_data)


@router.get("/agents", response_model=AgentListResponse)
async def get_agents(
    skip: int = Query(0, ge=0, description="Number of agents to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of agents to return"),
    status: Optional[AgentStatus] = Query(None, description="Filter by agent status"),
    prd_id: Optional[str] = Query(None, description="Filter by PRD ID")
):
    """Get a list of agents with optional filtering and pagination."""
    return await agent_service.get_agents(skip=skip, limit=limit, status=status, prd_id=prd_id)


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get a specific agent by ID."""
    return await agent_service.get_agent(agent_id)


@router.put("/agents/{agent_id}/status", response_model=AgentResponse)
async def update_agent_status(agent_id: str, status: AgentStatus):
    """Update agent status."""
    return await agent_service.update_agent_status(agent_id, status)


@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent."""
    return await agent_service.delete_agent(agent_id)


@router.get("/agents/{agent_id}/health", response_model=AgentHealthResponse)
async def check_agent_health(agent_id: str):
    """Check agent health status."""
    return await agent_service.check_agent_health(agent_id)


@router.get("/agents/{agent_id}/metrics", response_model=AgentMetricsResponse)
async def get_agent_metrics(agent_id: str):
    """Get agent metrics."""
    return await agent_service.get_agent_metrics(agent_id)


@router.get("/agents/by-prd/{prd_id}", response_model=List[AgentResponse])
async def get_agents_by_prd(prd_id: str):
    """Get all agents created from a specific PRD."""
    return await agent_service.get_agents_by_prd(prd_id)
