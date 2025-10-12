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
from ..utils.database import db_manager


class AgentService:
    """Service class for agent operations."""

    def __init__(self):
        """Initialize the agent service."""
        # In-memory storage as fallback
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
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }

        # Try to save to database, fallback to in-memory if database fails
        try:
            if db_manager.is_connected():
                saved_agent = await db_manager.create_agent(agent_dict)
                if saved_agent:
                    # Convert datetime strings back to datetime objects for response
                    saved_agent["created_at"] = datetime.fromisoformat(saved_agent["created_at"].replace('Z', '+00:00'))
                    saved_agent["updated_at"] = datetime.fromisoformat(saved_agent["updated_at"].replace('Z', '+00:00'))
                    if saved_agent.get("last_health_check"):
                        saved_agent["last_health_check"] = datetime.fromisoformat(saved_agent["last_health_check"].replace('Z', '+00:00'))
                    
                    # Update PRD status to "completed" when agent is successfully created
                    if agent_data.prd_id:
                        try:
                            await self._update_prd_status_to_completed(agent_data.prd_id)
                        except Exception as e:
                            print(f"Failed to update PRD status: {e}")
                    
                    return AgentResponse(**saved_agent)
        except Exception as e:
            print(f"Database save failed, using in-memory storage: {e}")
        
        # Fallback to in-memory storage
        self._agents_db[agent_id] = agent_dict
        
        # Update PRD status to "completed" when agent is successfully created (in-memory)
        if agent_data.prd_id:
            try:
                await self._update_prd_status_to_completed(agent_data.prd_id)
            except Exception as e:
                print(f"Failed to update PRD status: {e}")
        
        return AgentResponse(**agent_dict)

    async def _update_prd_status_to_completed(self, prd_id: str):
        """Update PRD status to completed when agent is created."""
        try:
            # Try to update in database first
            if db_manager.is_connected():
                await db_manager.update_prd(prd_id, {"status": "completed"})
                print(f"✅ Updated PRD {prd_id} status to 'completed' in database")
                return
            
            # Fallback to in-memory storage
            from ..services.prd_service import prd_service
            if hasattr(prd_service, '_prds_db') and prd_id in prd_service._prds_db:
                prd_service._prds_db[prd_id]['status'] = 'completed'
                print(f"✅ Updated PRD {prd_id} status to 'completed' in memory")
        except Exception as e:
            print(f"❌ Failed to update PRD status: {e}")

    async def get_agent(self, agent_id: str) -> AgentResponse:
        """Get an agent by ID."""
        # Try to get from database first
        try:
            if db_manager.is_connected():
                agent_data = await db_manager.get_agent(agent_id)
                if agent_data:
                    # Convert datetime strings back to datetime objects
                    agent_data["created_at"] = datetime.fromisoformat(agent_data["created_at"].replace('Z', '+00:00'))
                    agent_data["updated_at"] = datetime.fromisoformat(agent_data["updated_at"].replace('Z', '+00:00'))
                    if agent_data.get("last_health_check"):
                        agent_data["last_health_check"] = datetime.fromisoformat(agent_data["last_health_check"].replace('Z', '+00:00'))
                    return AgentResponse(**agent_data)
        except Exception as e:
            print(f"Database get failed, trying in-memory storage: {e}")
        
        # Fallback to in-memory storage
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
        # Try to get from database first
        try:
            if db_manager.is_connected():
                agents_data = await db_manager.get_agents(skip, limit)
                if agents_data:
                    # Convert datetime strings back to datetime objects
                    for agent in agents_data:
                        agent["created_at"] = datetime.fromisoformat(agent["created_at"].replace('Z', '+00:00'))
                        agent["updated_at"] = datetime.fromisoformat(agent["updated_at"].replace('Z', '+00:00'))
                        if agent.get("last_health_check"):
                            agent["last_health_check"] = datetime.fromisoformat(agent["last_health_check"].replace('Z', '+00:00'))
                    
                    # Apply filters
                    filtered_agents = agents_data
                    if status:
                        filtered_agents = [a for a in filtered_agents if a["status"] == status.value]
                    if prd_id:
                        filtered_agents = [a for a in filtered_agents if a.get("prd_id") == prd_id]
                    
                    return AgentListResponse(
                        agents=[AgentResponse(**agent) for agent in filtered_agents],
                        total=len(filtered_agents),
                        page=skip // limit + 1,
                        size=limit,
                        has_next=len(filtered_agents) == limit
                    )
        except Exception as e:
            print(f"Database get_agents failed, using in-memory storage: {e}")
        
        # Fallback to in-memory storage
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
        # Try to delete from database first
        try:
            if db_manager.is_connected():
                success = await db_manager.delete_agent(agent_id)
                if success:
                    return {"message": "Agent deleted successfully"}
                else:
                    raise HTTPException(status_code=404, detail="Agent not found")
        except Exception as e:
            print(f"Database delete failed, trying in-memory storage: {e}")

        # Fallback to in-memory storage
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
