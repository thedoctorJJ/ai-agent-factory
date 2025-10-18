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
from ..utils.database import db_manager


class DevinService:
    """Service class for Devin AI operations."""

    def __init__(self):
        """Initialize the Devin service."""
        # In-memory storage as fallback
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
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "devin_output": None,
            "agent_code": None
        }

        # Try to save to database, fallback to in-memory if database fails
        try:
            if db_manager.is_connected():
                saved_task = await db_manager.create_devin_task(task_dict)
                if saved_task:
                    # Convert datetime strings back to datetime objects for response
                    saved_task["created_at"] = datetime.fromisoformat(saved_task["created_at"].replace('Z', '+00:00'))
                    saved_task["updated_at"] = datetime.fromisoformat(saved_task["updated_at"].replace('Z', '+00:00'))
                    if saved_task.get("started_at"):
                        saved_task["started_at"] = datetime.fromisoformat(saved_task["started_at"].replace('Z', '+00:00'))
                    if saved_task.get("completed_at"):
                        saved_task["completed_at"] = datetime.fromisoformat(saved_task["completed_at"].replace('Z', '+00:00'))
                    return DevinTaskResponse(**saved_task)
        except Exception as e:
            print(f"Database save failed, using in-memory storage: {e}")
        
        # Fallback to in-memory storage
        self._tasks_db[task_id] = task_dict
        return DevinTaskResponse(**task_dict)

    async def get_task(self, task_id: str) -> DevinTaskResponse:
        """Get a Devin task by ID."""
        # Try to get from database first
        try:
            if db_manager.is_connected():
                task_data = await db_manager.get_devin_task(task_id)
                if task_data:
                    # Convert datetime strings back to datetime objects
                    task_data["created_at"] = datetime.fromisoformat(task_data["created_at"].replace('Z', '+00:00'))
                    task_data["updated_at"] = datetime.fromisoformat(task_data["updated_at"].replace('Z', '+00:00'))
                    if task_data.get("started_at"):
                        task_data["started_at"] = datetime.fromisoformat(task_data["started_at"].replace('Z', '+00:00'))
                    if task_data.get("completed_at"):
                        task_data["completed_at"] = datetime.fromisoformat(task_data["completed_at"].replace('Z', '+00:00'))
                    return DevinTaskResponse(**task_data)
        except Exception as e:
            print(f"Database get failed, trying in-memory storage: {e}")
        
        # Fallback to in-memory storage
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
        # Try to get from database first
        try:
            if db_manager.is_connected():
                tasks_data = await db_manager.get_devin_tasks(skip, limit)
                if tasks_data:
                    # Convert datetime strings back to datetime objects
                    for task in tasks_data:
                        task["created_at"] = datetime.fromisoformat(task["created_at"].replace('Z', '+00:00'))
                        task["updated_at"] = datetime.fromisoformat(task["updated_at"].replace('Z', '+00:00'))
                        if task.get("started_at"):
                            task["started_at"] = datetime.fromisoformat(task["started_at"].replace('Z', '+00:00'))
                        if task.get("completed_at"):
                            task["completed_at"] = datetime.fromisoformat(task["completed_at"].replace('Z', '+00:00'))
                    
                    # Apply filters
                    filtered_tasks = tasks_data
                    if status:
                        filtered_tasks = [t for t in filtered_tasks if t["status"] == status.value]
                    if prd_id:
                        filtered_tasks = [t for t in filtered_tasks if t["prd_id"] == prd_id]
                    
                    return DevinTaskListResponse(
                        tasks=[DevinTaskResponse(**task) for task in filtered_tasks],
                        total=len(filtered_tasks),
                        page=skip // limit + 1,
                        size=limit,
                        has_next=len(filtered_tasks) == limit
                    )
        except Exception as e:
            print(f"Database get_tasks failed, using in-memory storage: {e}")
        
        # Fallback to in-memory storage
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
        """Execute a Devin task using MCP integration."""
        task = await self.get_task(task_id)

        if task.status != DevinTaskStatus.PENDING.value:
            raise HTTPException(
                status_code=400,
                detail=f"Task is not in pending status. Current status: {task.status}")

        # Update task status to in_devin
        task_dict = self._tasks_db[task_id]
        task_dict["status"] = DevinTaskStatus.IN_DEVIN.value
        task_dict["updated_at"] = datetime.utcnow()

        # Load PRD data into MCP server cache
        await self._load_prd_to_mcp(task_dict.get("prd_id"))
        
        # Generate the Devin prompt with MCP instructions
        devin_prompt = self._generate_devin_mcp_prompt(task_dict)

        return DevinTaskExecuteResponse(
            message="Task ready for Devin AI with MCP integration",
            task_id=task_id,
            status=DevinTaskStatus.IN_DEVIN,
            note=f"PRD data loaded into MCP server. Copy the following prompt to Devin AI:\n\n{devin_prompt}")

    async def _auto_complete_task(self, task_id: str):
        """Auto-complete a task after a delay (mock implementation)."""
        import asyncio
        await asyncio.sleep(10)  # Wait 10 seconds
        
        # Try to update in database first
        try:
            if db_manager.is_connected():
                task_data = await db_manager.get_devin_task(task_id)
                if task_data and task_data["status"] == DevinTaskStatus.IN_DEVIN.value:
                    # Mock completion
                    update_data = {
                        "status": DevinTaskStatus.COMPLETED.value,
                        "updated_at": datetime.utcnow().isoformat(),
                        "completed_at": datetime.utcnow().isoformat(),
                        "devin_output": f"Mock agent created for task {task_id}",
                        "agent_code": f"# Mock agent code for {task_data['title']}\n# This is a placeholder implementation"
                    }
                    await db_manager.update_devin_task(task_id, update_data)
                    
                    # Create a mock agent
                    try:
                        from ..models.agent import AgentRegistration
                        agent_data = AgentRegistration(
                            name=f"Agent-{task_data['title'][:20]}",
                            description=task_data["description"],
                            purpose="Mock agent created from PRD",
                            version="1.0.0",
                            repository_url=f"https://github.com/thedoctorJJ/agent-{task_id[:8]}",
                            deployment_url=f"https://agent-{task_id[:8]}-uc.a.run.app",
                            health_check_url=f"https://agent-{task_id[:8]}-uc.a.run.app/health",
                            prd_id=task_data["prd_id"],
                            devin_task_id=task_id,
                            capabilities=["task_management", "notifications", "reporting"],
                            configuration={"mock": True, "auto_generated": True}
                        )
                        await agent_service.create_agent(agent_data)
                    except Exception as e:
                        print(f"Error creating mock agent: {e}")
                    return
        except Exception as e:
            print(f"Database update failed, trying in-memory storage: {e}")
        
        # Fallback to in-memory storage
        if task_id in self._tasks_db:
            task_dict = self._tasks_db[task_id]
            if task_dict["status"] == DevinTaskStatus.IN_DEVIN.value:
                # Mock completion
                task_dict["status"] = DevinTaskStatus.COMPLETED.value
                task_dict["updated_at"] = datetime.utcnow()
                task_dict["devin_output"] = f"Mock agent created for task {task_id}"
                task_dict["agent_code"] = f"# Mock agent code for {task_dict['title']}\n# This is a placeholder implementation"
                
                # Create a mock agent
                try:
                    from ..models.agent import AgentRegistration
                    agent_data = AgentRegistration(
                        name=f"Agent-{task_dict['title'][:20]}",
                        description=task_dict["description"],
                        purpose="Mock agent created from PRD",
                        version="1.0.0",
                        repository_url=f"https://github.com/thedoctorJJ/agent-{task_id[:8]}",
                        deployment_url=f"https://agent-{task_id[:8]}-uc.a.run.app",
                        health_check_url=f"https://agent-{task_id[:8]}-uc.a.run.app/health",
                        prd_id=task_dict["prd_id"],
                        devin_task_id=task_id,
                        capabilities=["task_management", "notifications", "reporting"],
                        configuration={"mock": True, "auto_generated": True}
                    )
                    await agent_service.create_agent(agent_data)
                except Exception as e:
                    print(f"Error creating mock agent: {e}")

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
        """Create an agent from a completed Devin task with hybrid repository strategy."""
        task = await self.get_task(task_id)

        # Get the associated PRD
        prd = await prd_service.get_prd(task.prd_id)

        # Determine repository strategy based on PRD type
        if prd.prd_type == "platform":
            # Platform PRDs: Use main repository structure
            repository_url = (
                f"https://github.com/thedoctorJJ/ai-agent-factory/tree/main/agents/"
                f"{self._clean_title(prd.title)}"
            )
            repository_strategy = "main_repository"
        else:
            # Agent PRDs: Create separate repository
            repository_url = (
                f"https://github.com/thedoctorJJ/ai-agents-"
                f"{self._clean_title(prd.title)}"
            )
            repository_strategy = "separate_repository"

        # Create agent registration data
        agent_data = {
            "name": prd.title,
            "description": prd.description,
            "purpose": f"AI agent created from PRD: {prd.title}",
            "version": "1.0.0",
            "repository_url": repository_url,
            "deployment_url": (
                f"https://ai-agent-{self._clean_title(prd.title)}"
                f"-hash.run.app"
            ),
            "health_check_url": (
                f"https://ai-agent-{self._clean_title(prd.title)}"
                f"-hash.run.app/health"
            ),
            "prd_id": prd.id,
            "devin_task_id": task_id,
            # Use first 5 requirements as capabilities
            "capabilities": prd.requirements[:5],
            "configuration": {
                "environment": "production",
                "scaling": "auto",
                "repository_strategy": repository_strategy,
                "prd_type": prd.prd_type
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

    def _generate_devin_mcp_prompt(self, task_dict: Dict[str, Any]) -> str:
        """Generate a Devin AI prompt with MCP integration instructions."""
        prd_id = task_dict.get("prd_id")
        title = task_dict.get("title")
        description = task_dict.get("description")
        requirements = task_dict.get("requirements", [])
        
        prompt = f"""
# AI Agent Creation Task with MCP Integration

## Task Information:
- **Task ID**: {task_dict.get('id')}
- **PRD ID**: {prd_id}
- **Title**: {title}
- **Description**: {description}

## MCP Integration Available:
You have access to the AI Agent Factory MCP server with the following tools:

### Available MCP Tools:
1. **get_prd_details** - Get detailed PRD information
2. **list_available_prds** - List all available PRDs
3. **create_agent_from_prd** - Create agent record in the platform
4. **get_agent_library_info** - Access agent libraries and tools
5. **update_agent_status** - Update agent status when complete

### Recommended Workflow:
1. **First, get the full PRD details**:
   ```
   Use MCP tool: get_prd_details
   Parameters: {{"prd_id": "{prd_id}"}}
   ```

2. **Review agent library information**:
   ```
   Use MCP tool: get_agent_library_info
   ```

3. **Create the agent record**:
   ```
   Use MCP tool: create_agent_from_prd
   Parameters: {{
     "prd_id": "{prd_id}",
     "agent_name": "Your Agent Name",
     "agent_description": "Your agent description",
     "repository_name": "your-repo-name"
   }}
   ```

4. **Implement the agent** based on the PRD requirements

5. **Update agent status** when complete:
   ```
   Use MCP tool: update_agent_status
   Parameters: {{
     "agent_id": "agent_id_from_step_3",
     "status": "active",
     "repository_url": "https://github.com/thedoctorJJ/your-repo",
     "deployment_url": "https://your-agent-uc.a.run.app"
   }}
   ```

## Requirements from PRD:
{chr(10).join([f"- {req}" for req in requirements])}

## Technical Stack:
- **Backend**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Google Cloud Run
- **Repository**: GitHub (thedoctorJJ organization)
- **Monitoring**: Built-in health checks and logging

## Next Steps:
1. Use the MCP tools to access the full PRD details
2. Create the agent record in the platform
3. Implement the agent according to the PRD requirements
4. Deploy and update the status

Start by calling the MCP tools to get the complete PRD information!
"""
        return prompt

    async def _load_prd_to_mcp(self, prd_id: str):
        """Load PRD data into the MCP server cache"""
        try:
            import requests
            
            # Call our MCP integration endpoint
            response = requests.post(
                "http://localhost:8000/api/v1/mcp/load-prd",
                json={"prd_id": prd_id}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ PRD data loaded into MCP server: {result.get('message')}")
            else:
                print(f"⚠️ Failed to load PRD to MCP server: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Error loading PRD to MCP server: {e}")


# Global service instance
devin_service = DevinService()
