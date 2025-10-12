"""
Agent service for business logic operations.
"""
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException

from ..models.agent import (
    AgentRegistration, AgentResponse, AgentStatus, AgentHealthStatus,
    AgentListResponse, AgentHealthResponse, AgentMetricsResponse
)


class AgentService:
    """Service class for agent operations."""

    def __init__(self):
        """Initialize the agent service."""
        # In-memory storage for demo purposes
        # In production, this would be replaced with a database
        self._agents_db: Dict[str, Dict[str, Any]] = {}

    async def create_agent(
            self,
            agent_data: AgentRegistration) -> AgentResponse:
        """Create a new agent."""
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow()

        agent_dict = {
            "id": agent_id,
            "name": agent_data.name,
            "description": agent_data.description,
            "purpose": agent_data.purpose,
            "version": agent_data.version,
            "tools": [],  # Will be populated by Devin AI
            "prompts": [],  # Will be populated by Devin AI
            "status": AgentStatus.PENDING.value,
            "repository_url": agent_data.repository_url,
            "deployment_url": agent_data.deployment_url,
            "health_check_url": agent_data.health_check_url,
            "prd_id": agent_data.prd_id,
            "devin_task_id": agent_data.devin_task_id,
            "capabilities": agent_data.capabilities,
            "configuration": agent_data.configuration,
            "last_health_check": None,
            "health_status": AgentHealthStatus.UNKNOWN.value,
            "created_at": now,
            "updated_at": now
        }

        self._agents_db[agent_id] = agent_dict
        return AgentResponse(**agent_dict)

    async def get_agent(self, agent_id: str) -> AgentResponse:
        """Get an agent by ID."""
        if agent_id not in self._agents_db:
            raise HTTPException(status_code=404, detail="Agent not found")

        return AgentResponse(**self._agents_db[agent_id])

    async def get_agents(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[AgentStatus] = None,
        prd_id: Optional[str] = None
    ) -> AgentListResponse:
        """Get a list of agents with optional filtering."""
        agents = list(self._agents_db.values())

        # Apply filters
        if status:
            agents = [a for a in agents if a["status"] == status.value]
        if prd_id:
            agents = [a for a in agents if a.get("prd_id") == prd_id]

        # Sort by created_at descending
        agents.sort(key=lambda x: x["created_at"], reverse=True)

        # Apply pagination
        total = len(agents)
        agents = agents[skip:skip + limit]

        return AgentListResponse(
            agents=[AgentResponse(**agent) for agent in agents],
            total=total,
            page=skip // limit + 1,
            size=limit,
            has_next=skip + limit < total
        )

    async def update_agent_status(
            self,
            agent_id: str,
            status: AgentStatus) -> AgentResponse:
        """Update agent status."""
        if agent_id not in self._agents_db:
            raise HTTPException(status_code=404, detail="Agent not found")

        agent_dict = self._agents_db[agent_id]
        agent_dict["status"] = status.value
        agent_dict["updated_at"] = datetime.utcnow()

        return AgentResponse(**agent_dict)

    async def delete_agent(self, agent_id: str) -> Dict[str, str]:
        """Delete an agent."""
        if agent_id not in self._agents_db:
            raise HTTPException(status_code=404, detail="Agent not found")

        del self._agents_db[agent_id]
        return {"message": "Agent deleted successfully"}

    async def check_agent_health(self, agent_id: str) -> AgentHealthResponse:
        """Check agent health status."""
        agent = await self.get_agent(agent_id)

        if not agent.health_check_url:
            return AgentHealthResponse(
                agent_id=agent_id,
                agent_name=agent.name,
                health_check_url="",
                status=AgentHealthStatus.UNKNOWN,
                details={"error": "No health check URL configured"}
            )

        # Simulate health check (in production, this would make an actual HTTP
        # request)
        import random
        health_statuses = [
            AgentHealthStatus.HEALTHY,
            AgentHealthStatus.UNHEALTHY,
            AgentHealthStatus.DEGRADED
        ]
        status = random.choice(health_statuses)
        response_time = random.randint(50, 500)

        # Update agent's health status
        agent_dict = self._agents_db[agent_id]
        agent_dict["health_status"] = status.value
        agent_dict["last_health_check"] = datetime.utcnow()

        return AgentHealthResponse(
            agent_id=agent_id,
            agent_name=agent.name,
            health_check_url=agent.health_check_url,
            last_checked=datetime.utcnow(),
            status=status,
            details={
                "response_time_ms": response_time,
                "status_code": 200 if status == AgentHealthStatus.HEALTHY else 500,
                "message": "Health check completed"},
            response_time_ms=response_time)

    async def get_agent_metrics(self, agent_id: str) -> AgentMetricsResponse:
        """Get agent metrics."""
        agent = await self.get_agent(agent_id)

        # Simulate metrics (in production, this would come from monitoring
        # system)
        import random

        return AgentMetricsResponse(
            agent_id=agent_id,
            agent_name=agent.name,
            status=AgentStatus(agent.status),
            health_status=AgentHealthStatus(agent.health_status),
            last_health_check=agent.last_health_check,
            deployment_url=agent.deployment_url,
            repository_url=agent.repository_url,
            version=agent.version,
            capabilities=agent.capabilities,
            uptime_seconds=random.randint(3600, 86400),  # 1-24 hours
            request_count=random.randint(100, 10000),
            error_count=random.randint(0, 50),
            avg_response_time_ms=random.uniform(100, 1000)
        )

    async def get_agents_by_prd(self, prd_id: str) -> List[AgentResponse]:
        """Get all agents created from a specific PRD."""
        agents_response = await self.get_agents(prd_id=prd_id, limit=1000)
        return agents_response.agents


# Global service instance
agent_service = AgentService()
