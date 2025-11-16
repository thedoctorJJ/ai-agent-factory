"""
Agent service for business logic operations.
"""
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import HTTPException

from ..models.agent import (
    AgentRegistration, AgentResponse, AgentStatus, AgentHealthStatus,
    AgentListResponse, AgentHealthResponse, AgentMetricsResponse
)
from ..utils.simple_data_manager import data_manager


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
        now = datetime.now(timezone.utc)

        agent_dict = {
            "id": agent_id,
            "name": agent_data.name,
            "description": agent_data.description,
            "purpose": agent_data.purpose,
            "agent_type": agent_data.agent_type,
            "version": agent_data.version,
            "status": AgentStatus.DRAFT.value,
            "repository_url": agent_data.repository_url,
            "deployment_url": agent_data.deployment_url,
            "health_check_url": agent_data.health_check_url,
            "prd_id": agent_data.prd_id,
            "devin_task_id": agent_data.devin_task_id,
            "capabilities": agent_data.capabilities,
            "configuration": agent_data.configuration,
            "metrics": {},
            "last_health_check": None,
            "health_status": AgentHealthStatus.UNKNOWN.value,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }

        # Check if agent with this name already exists
        existing_agent = await data_manager.get_agent_by_name(agent_data.name)
        if existing_agent:
            print(f"⚠️  Agent with name '{agent_data.name}' already exists (ID: {existing_agent.get('id')})")
            print(f"   Updating existing agent instead of creating new one...")
            # Update the existing agent with new data
            agent_id = existing_agent.get('id')
            # Prepare update data (exclude id and timestamps)
            update_data = {k: v for k, v in agent_dict.items() if k not in ['id', 'created_at']}
            update_data['updated_at'] = now.isoformat()
            saved_agent = await data_manager.update_agent(agent_id, update_data)
            if not saved_agent:
                raise HTTPException(status_code=500, detail="Failed to update existing agent")
        else:
            # Use simplified data manager to create new agent
            try:
                saved_agent = await data_manager.create_agent(agent_dict)
            except Exception as e:
                # Check if it's a unique constraint violation (agent name already exists)
                error_str = str(e).lower()
                if "unique" in error_str or "duplicate" in error_str or "already exists" in error_str:
                    # Try to get the existing agent by name
                    print(f"⚠️  Unique constraint violation, attempting to retrieve existing agent...")
                    existing_agent = await data_manager.get_agent_by_name(agent_data.name)
                    if existing_agent:
                        print(f"✅ Found existing agent: {existing_agent.get('id')}")
                        # Update instead
                        agent_id = existing_agent.get('id')
                        update_data = {k: v for k, v in agent_dict.items() if k not in ['id', 'created_at']}
                        update_data['updated_at'] = now.isoformat()
                        saved_agent = await data_manager.update_agent(agent_id, update_data)
                    else:
                        raise HTTPException(
                            status_code=409,
                            detail=f"Agent with name '{agent_data.name}' already exists but could not be retrieved"
                        )
                else:
                    # Re-raise other errors
                    print(f"❌ Error creating agent: {e}")
                    import traceback
                    traceback.print_exc()
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to create agent: {str(e)}"
                    )

        if not saved_agent:
            raise HTTPException(status_code=500, detail="Failed to create agent: No data returned")

        # Update PRD status to "completed" when agent is successfully created
        if agent_data.prd_id:
            try:
                await self._update_prd_status_to_completed(agent_data.prd_id)
            except Exception as e:
                print(f"Failed to update PRD status: {e}")

        # Convert datetime strings back to datetime objects for response
        if saved_agent:
            saved_agent["created_at"] = datetime.fromisoformat(saved_agent["created_at"].replace('Z', '+00:00'))
            saved_agent["updated_at"] = datetime.fromisoformat(saved_agent["updated_at"].replace('Z', '+00:00'))
            if saved_agent.get("last_health_check"):
                saved_agent["last_health_check"] = datetime.fromisoformat(saved_agent["last_health_check"].replace('Z', '+00:00'))

        return AgentResponse(**saved_agent)

    async def _update_prd_status_to_completed(self, prd_id: str):
        """Update PRD status to completed when agent is created."""
        try:
            # Try to update in database first
            if data_manager.is_connected():
                await data_manager.update_prd(prd_id, {"status": "completed"})
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
        # Use data manager to get agent
        agent_data = await data_manager.get_agent(agent_id)

        if not agent_data:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Convert datetime strings back to datetime objects if needed
        if isinstance(agent_data.get("created_at"), str):
            agent_data["created_at"] = datetime.fromisoformat(agent_data["created_at"].replace('Z', '+00:00'))
        if isinstance(agent_data.get("updated_at"), str):
            agent_data["updated_at"] = datetime.fromisoformat(agent_data["updated_at"].replace('Z', '+00:00'))
        if agent_data.get("last_health_check") and isinstance(agent_data["last_health_check"], str):
            agent_data["last_health_check"] = datetime.fromisoformat(agent_data["last_health_check"].replace('Z', '+00:00'))

        return AgentResponse(**agent_data)

    async def get_agents(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[AgentStatus] = None,
        prd_id: Optional[str] = None
    ) -> AgentListResponse:
        """Get a list of agents with optional filtering."""
        try:
            # Use simplified data manager
            agents_data = await data_manager.get_agents(skip, limit)
        except Exception as e:
            print(f"❌ Error fetching agents from data manager: {e}")
            # Return empty list if data fetch fails
            return AgentListResponse(
                agents=[],
                total=0,
                page=1,
                size=limit,
                has_next=False
            )

        # Convert datetime strings and ensure proper formatting
        processed_agents = []
        for agent in agents_data:
            try:
                # Ensure we have required fields with defaults
                if not agent.get("id"):
                    print(f"⚠️ Skipping agent with missing ID: {agent}")
                    continue
                
                # Convert datetime strings to datetime objects if needed
                if isinstance(agent.get("created_at"), str):
                    agent["created_at"] = datetime.fromisoformat(agent["created_at"].replace('Z', '+00:00'))
                elif not agent.get("created_at"):
                    # Default to current time if missing
                    agent["created_at"] = datetime.now(timezone.utc)
                
                if isinstance(agent.get("updated_at"), str):
                    agent["updated_at"] = datetime.fromisoformat(agent["updated_at"].replace('Z', '+00:00'))
                elif not agent.get("updated_at"):
                    # Default to created_at if missing
                    agent["updated_at"] = agent.get("created_at", datetime.now(timezone.utc))
                
                if agent.get("last_health_check") and isinstance(agent["last_health_check"], str):
                    agent["last_health_check"] = datetime.fromisoformat(agent["last_health_check"].replace('Z', '+00:00'))

                # Ensure status and health_status are valid enum values
                if agent.get("status"):
                    try:
                        AgentStatus(agent["status"])
                    except ValueError:
                        agent["status"] = AgentStatus.DRAFT.value
                else:
                    agent["status"] = AgentStatus.DRAFT.value

                if agent.get("health_status"):
                    try:
                        AgentHealthStatus(agent["health_status"])
                    except ValueError:
                        agent["health_status"] = AgentHealthStatus.UNKNOWN.value
                else:
                    agent["health_status"] = AgentHealthStatus.UNKNOWN.value

                # Ensure required string fields have defaults
                if not agent.get("name"):
                    agent["name"] = "Unnamed Agent"
                if not agent.get("description"):
                    agent["description"] = ""
                if not agent.get("purpose"):
                    agent["purpose"] = ""
                if not agent.get("version"):
                    agent["version"] = "1.0.0"
                if not agent.get("agent_type"):
                    agent["agent_type"] = "other"
                
                # Ensure list fields are lists
                if not isinstance(agent.get("capabilities"), list):
                    agent["capabilities"] = agent.get("capabilities") or []
                if not isinstance(agent.get("configuration"), dict):
                    agent["configuration"] = agent.get("configuration") or {}
                if not isinstance(agent.get("metrics"), dict):
                    agent["metrics"] = agent.get("metrics") or {}

                processed_agents.append(agent)
            except Exception as e:
                # Log the error but continue processing other agents
                print(f"❌ Error processing agent {agent.get('id', 'unknown')}: {e}")
                print(f"   Agent data: {agent}")
                import traceback
                traceback.print_exc()
                # Skip this agent and continue
                continue

        # Apply filters
        filtered_agents = processed_agents
        if status:
            filtered_agents = [a for a in filtered_agents if a["status"] == status.value]
        if prd_id:
            filtered_agents = [a for a in filtered_agents if a.get("prd_id") == prd_id]

        # Create AgentResponse objects with error handling
        agent_responses = []
        for agent in filtered_agents:
            try:
                agent_responses.append(AgentResponse(**agent))
            except Exception as e:
                print(f"❌ Error creating AgentResponse for agent {agent.get('id', 'unknown')}: {e}")
                print(f"   Agent data: {agent}")
                import traceback
                traceback.print_exc()
                # Skip this agent and continue
                continue

        return AgentListResponse(
            agents=agent_responses,
            total=len(agent_responses),
            page=skip // limit + 1 if limit > 0 else 1,
            size=limit,
            has_next=len(agent_responses) == limit
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
        agent_dict["updated_at"] = datetime.now(timezone.utc).isoformat()

        return AgentResponse(**agent_dict)

    async def update_agent(
            self,
            agent_id: str,
            agent_data: Dict[str, Any]) -> AgentResponse:
        """Update an agent."""
        # Try to update in database first
        try:
            if data_manager.is_connected():
                # First check if agent exists in database
                existing_agent = await data_manager.get_agent(agent_id)
                if not existing_agent:
                    raise HTTPException(status_code=404, detail="Agent not found")
                
                # Try to update
                updated_agent = await data_manager.update_agent(agent_id, agent_data)
                if updated_agent:
                    # Convert datetime strings back to datetime objects
                    if isinstance(updated_agent.get("created_at"), str):
                        updated_agent["created_at"] = datetime.fromisoformat(updated_agent["created_at"].replace('Z', '+00:00'))
                    if isinstance(updated_agent.get("updated_at"), str):
                        updated_agent["updated_at"] = datetime.fromisoformat(updated_agent["updated_at"].replace('Z', '+00:00'))
                    if updated_agent.get("last_health_check") and isinstance(updated_agent["last_health_check"], str):
                        updated_agent["last_health_check"] = datetime.fromisoformat(updated_agent["last_health_check"].replace('Z', '+00:00'))
                    return AgentResponse(**updated_agent)
                else:
                    # Update returned None but agent exists - this shouldn't happen, but if it does, fetch the agent
                    print(f"⚠️  Update returned None for agent {agent_id}, fetching current state...")
                    current_agent = await data_manager.get_agent(agent_id)
                    if current_agent:
                        # Merge the update data manually
                        current_agent.update(agent_data)
                        # Try update again
                        updated_agent = await data_manager.update_agent(agent_id, agent_data)
                        if updated_agent:
                            if isinstance(updated_agent.get("created_at"), str):
                                updated_agent["created_at"] = datetime.fromisoformat(updated_agent["created_at"].replace('Z', '+00:00'))
                            if isinstance(updated_agent.get("updated_at"), str):
                                updated_agent["updated_at"] = datetime.fromisoformat(updated_agent["updated_at"].replace('Z', '+00:00'))
                            if updated_agent.get("last_health_check") and isinstance(updated_agent["last_health_check"], str):
                                updated_agent["last_health_check"] = datetime.fromisoformat(updated_agent["last_health_check"].replace('Z', '+00:00'))
                            return AgentResponse(**updated_agent)
                    raise HTTPException(status_code=500, detail="Failed to update agent in database")
        except HTTPException:
            raise
        except Exception as e:
            print(f"Database update failed: {e}")
            # Only fall back to in-memory if we're in development mode
            if data_manager.mode == "development":
                if agent_id not in self._agents_db:
                    raise HTTPException(status_code=404, detail="Agent not found")
                agent_dict = self._agents_db[agent_id]
                agent_dict.update(agent_data)
                agent_dict["updated_at"] = datetime.now(timezone.utc).isoformat()
                return AgentResponse(**agent_dict)
            else:
                # In production, if database update fails, raise error
                raise HTTPException(status_code=500, detail=f"Failed to update agent: {str(e)}")

    async def delete_agent(self, agent_id: str) -> Dict[str, str]:
        """Delete an agent."""
        # Try to delete from database first
        try:
            if data_manager.is_connected():
                success = await data_manager.delete_agent(agent_id)
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

    async def clear_all_agents(self) -> Dict[str, str]:
        """Clear all agents from the system."""
        # Use simplified data manager
        success = await data_manager.clear_all_agents()
        if success:
            return {"message": "All agents cleared successfully"}
        else:
            return {"message": "Failed to clear agents"}

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

        # Update agent's health status in the database
        agent_data = {
            "health_status": status.value,
            "last_health_check": datetime.now(timezone.utc).isoformat()
        }
        await data_manager.update_agent(agent_id, agent_data)

        return AgentHealthResponse(
            agent_id=agent_id,
            agent_name=agent.name,
            health_check_url=agent.health_check_url,
            last_checked=datetime.now(timezone.utc),
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
