"""
Devin AI service for business logic operations.
"""
import uuid
import re
from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException

from ..models.devin import (
    DevinTaskCreate, DevinTaskResponse, DevinTaskStatus,
    DevinTaskListResponse, DevinTaskComplete, DevinTaskExecuteResponse
)
from ..services.agent_service import agent_service
from ..services.prd_service import prd_service


class DevinService:
    """Service class for Devin AI operations."""

    def __init__(self):
        """Initialize the Devin service."""
        # In-memory storage for demo purposes
        # In production, this would be replaced with a database
        self._tasks_db: Dict[str, Dict[str, Any]] = {}

    async def create_task(
            self,
            task_data: DevinTaskCreate) -> DevinTaskResponse:
        """Create a new Devin task."""
        task_id = str(uuid.uuid4())
        now = datetime.utcnow()

        # Generate Devin prompt
        devin_prompt = self._generate_devin_prompt(task_data, task_id)

        task_dict = {
            "id": task_id,
            "prd_id": task_data.prd_id,
            "title": task_data.title,
            "description": task_data.description,
            "requirements": task_data.requirements,
            "devin_prompt": devin_prompt,
            "status": DevinTaskStatus.PENDING.value,
            "created_at": now,
            "updated_at": now,
            "devin_output": None,
            "agent_code": None
        }

        self._tasks_db[task_id] = task_dict
        return DevinTaskResponse(**task_dict)

    async def get_task(self, task_id: str) -> DevinTaskResponse:
        """Get a Devin task by ID."""
        if task_id not in self._tasks_db:
            raise HTTPException(status_code=404, detail="Devin task not found")

        return DevinTaskResponse(**self._tasks_db[task_id])

    async def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[DevinTaskStatus] = None,
        prd_id: Optional[str] = None
    ) -> DevinTaskListResponse:
        """Get a list of Devin tasks with optional filtering."""
        tasks = list(self._tasks_db.values())

        # Apply filters
        if status:
            tasks = [t for t in tasks if t["status"] == status.value]
        if prd_id:
            tasks = [t for t in tasks if t["prd_id"] == prd_id]

        # Sort by created_at descending
        tasks.sort(key=lambda x: x["created_at"], reverse=True)

        # Apply pagination
        total = len(tasks)
        tasks = tasks[skip:skip + limit]

        return DevinTaskListResponse(
            tasks=[DevinTaskResponse(**task) for task in tasks],
            total=total,
            page=skip // limit + 1,
            size=limit,
            has_next=skip + limit < total
        )

    async def execute_task(self, task_id: str) -> DevinTaskExecuteResponse:
        """Execute a Devin task (simulate API call to Devin AI)."""
        task = await self.get_task(task_id)

        if task.status != DevinTaskStatus.PENDING.value:
            raise HTTPException(
                status_code=400,
                detail=f"Task is not in pending status. Current status: {
                    task.status}")

        # Update task status to in_devin
        task_dict = self._tasks_db[task_id]
        task_dict["status"] = DevinTaskStatus.IN_DEVIN.value
        task_dict["updated_at"] = datetime.utcnow()

        return DevinTaskExecuteResponse(
            message="Task submitted to Devin AI successfully",
            task_id=task_id,
            status=DevinTaskStatus.IN_DEVIN,
            note="Devin AI is now processing your request. This usually takes 2-3 minutes.")

    async def complete_task(
            self,
            task_id: str,
            completion_data: DevinTaskComplete) -> DevinTaskResponse:
        """Mark a Devin task as completed."""
        task = await self.get_task(task_id)

        if task.status not in [
                DevinTaskStatus.IN_DEVIN.value,
                DevinTaskStatus.PENDING.value]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot complete task in status: {task.status}"
            )

        # Update task
        task_dict = self._tasks_db[task_id]
        task_dict["status"] = DevinTaskStatus.COMPLETED.value
        task_dict["devin_output"] = completion_data.devin_output
        task_dict["agent_code"] = completion_data.agent_code
        task_dict["updated_at"] = datetime.utcnow()

        # Create agent from completed task
        if completion_data.deployment_method == "mcp_automatic":
            await self._create_agent_from_task(task_id)

        return DevinTaskResponse(**task_dict)

    async def _create_agent_from_task(self, task_id: str) -> None:
        """Create an agent from a completed Devin task."""
        task = await self.get_task(task_id)

        # Get the associated PRD
        prd = await prd_service.get_prd(task.prd_id)

        # Create agent registration data
        agent_data = {
            "name": prd.title,
            "description": prd.description,
            "purpose": f"AI agent created from PRD: {prd.title}",
            "version": "1.0.0",
            "repository_url": (
                f"https://github.com/thedoctorJJ/end-cap-agent-"
                f"{self._clean_title(prd.title)}"
            ),
            "deployment_url": (
                f"https://end-cap-agent-{self._clean_title(prd.title)}"
                f"-hash.run.app"
            ),
            "health_check_url": (
                f"https://end-cap-agent-{self._clean_title(prd.title)}"
                f"-hash.run.app/health"
            ),
            "prd_id": prd.id,
            "devin_task_id": task_id,
            # Use first 5 requirements as capabilities
            "capabilities": prd.requirements[:5],
            "configuration": {
                "environment": "production",
                "scaling": "auto"
            }
        }

        # Create the agent
        from ..models.agent import AgentRegistration
        agent_registration = AgentRegistration(**agent_data)
        await agent_service.create_agent(agent_registration)

        # Update PRD status to processed
        from ..models.prd import PRDUpdate, PRDStatus
        prd_update = PRDUpdate(status=PRDStatus.PROCESSED)
        await prd_service.update_prd(prd.id, prd_update)

    def _clean_title(self, title: str) -> str:
        """Clean title for use in URLs and repository names."""
        # Remove emojis and special characters
        cleaned = re.sub(r'[^\w\s-]', '', title)
        # Replace spaces with hyphens and convert to lowercase
        cleaned = re.sub(r'[-\s]+', '-', cleaned).lower()
        # Remove leading/trailing hyphens
        return cleaned.strip('-')

    def _generate_devin_prompt(
            self,
            task_data: DevinTaskCreate,
            task_id: str) -> str:
        """Generate a comprehensive prompt for Devin AI."""
        return f"""# Devin AI Task: {task_data.title}

## Task ID: {task_id}
## PRD ID: {task_data.prd_id}

## Objective
Create a fully functional AI agent based on the following requirements:

## Description
{task_data.description}

## Requirements
{chr(10).join(f"- {req}" for req in task_data.requirements)}

## Implementation Instructions

### 1. Agent Architecture
- Create a modular, scalable agent architecture
- Implement proper error handling and logging
- Use FastAPI for the agent's API endpoints
- Include health check endpoints

### 2. Core Functionality
- Implement the main agent logic based on requirements
- Add proper input validation and sanitization
- Include comprehensive error handling
- Implement logging and monitoring

### 3. API Endpoints
- Create RESTful API endpoints
- Include proper HTTP status codes
- Add request/response validation
- Implement rate limiting if needed

### 4. Database Integration
- Set up Supabase database connection
- Create necessary tables and schemas
- Implement CRUD operations
- Add data validation

### 5. Deployment
- Create Dockerfile for containerization
- Set up Google Cloud Run deployment
- Configure environment variables
- Implement health checks

### 6. Testing
- Add unit tests for core functionality
- Include integration tests
- Add API endpoint tests
- Implement test coverage reporting

### 7. Documentation
- Create comprehensive README
- Document API endpoints
- Include setup and deployment instructions
- Add usage examples

## Deliverables
1. Complete agent codebase
2. Dockerfile for deployment
3. Database schema and migrations
4. Comprehensive tests
5. Documentation
6. Deployment configuration

## Success Criteria
- Agent is fully functional and deployed
- All requirements are implemented
- Code follows best practices
- Tests pass with good coverage
- Documentation is complete

Please create this agent and provide the complete codebase ready for deployment."""


# Global service instance
devin_service = DevinService()
