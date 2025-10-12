from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Pydantic models for Devin AI integration


class DevinTask(BaseModel):
    id: str
    prd_id: str
    title: str
    description: str
    requirements: List[str]
    devin_prompt: str
    status: str  # pending, in_devin, completed, failed
    created_at: datetime
    updated_at: datetime
    devin_output: Optional[str] = None
    agent_code: Optional[str] = None


class DevinTaskCreate(BaseModel):
    prd_id: str
    title: str
    description: str
    requirements: List[str]


# In-memory storage for demo (replace with Supabase in production)
devin_tasks_db = {}


@router.get("/devin/tasks", response_model=List[DevinTask])
async def get_devin_tasks():
    """Get all Devin AI tasks"""
    return list(devin_tasks_db.values())


@router.get("/devin/tasks/{task_id}", response_model=DevinTask)
async def get_devin_task(task_id: str):
    """Get a specific Devin AI task"""
    if task_id not in devin_tasks_db:
        raise HTTPException(status_code=404, detail="Devin task not found")
    return devin_tasks_db[task_id]


@router.post("/devin/tasks", response_model=DevinTask)
async def create_devin_task(task: DevinTaskCreate):
    """Create a new Devin AI task from PRD"""
    try:
        task_id = str(uuid.uuid4())
        now = datetime.utcnow()

        # Generate optimized prompt for Devin AI
        devin_prompt = generate_devin_prompt(
            task.title,
            task.description,
            task.requirements,
            task.prd_id,
            task_id)

        new_task = DevinTask(
            id=task_id,
            prd_id=task.prd_id,
            title=task.title,
            description=task.description,
            requirements=task.requirements,
            devin_prompt=devin_prompt,
            status="pending",
            created_at=now,
            updated_at=now
        )

        devin_tasks_db[task_id] = new_task
        return new_task
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating Devin task: {
                str(e)}")


@router.get("/devin/tasks/{task_id}/prompt")
async def get_devin_prompt(task_id: str):
    """Get the formatted prompt for copying to Devin AI"""
    if task_id not in devin_tasks_db:
        raise HTTPException(status_code=404, detail="Devin task not found")

    task = devin_tasks_db[task_id]
    return {
        "prompt": task.devin_prompt,
        "formatted_for_copy": format_for_devin_copy(task.devin_prompt)
    }


class TaskCompletionRequest(BaseModel):
    agent_code: str
    deployment_method: Optional[str] = "mcp_automatic"


@router.put("/devin/tasks/{task_id}/complete")
async def complete_devin_task(task_id: str, request: TaskCompletionRequest):
    """Mark a Devin AI task as completed with the generated code"""
    if task_id not in devin_tasks_db:
        raise HTTPException(status_code=404, detail="Devin task not found")

    task = devin_tasks_db[task_id]
    task.status = "completed"
    task.agent_code = request.agent_code
    task.updated_at = datetime.utcnow()

    devin_tasks_db[task_id] = task

    # Create an actual agent from the completed task
    await create_agent_from_task(task)

    return task


@router.post("/devin/tasks/{task_id}/execute")
async def execute_devin_task(task_id: str):
    """Execute a Devin AI task via MCP integration"""
    if task_id not in devin_tasks_db:
        raise HTTPException(status_code=404, detail="Devin task not found")

    task = devin_tasks_db[task_id]

    try:
        # Update task status to in_progress
        task.status = "in_devin"
        task.updated_at = datetime.utcnow()
        devin_tasks_db[task_id] = task

        # TODO: Implement actual MCP integration with Devin AI
        # This would involve:
        # 1. Connecting to Devin AI via MCP servers
        # 2. Sending the PRD data directly
        # 3. Monitoring the agent creation progress
        # 4. Auto-deploying the created agent

        # For now, return a success response
        return {
            "message": "Devin AI task execution initiated",
            "task_id": task_id,
            "status": "in_devin",
            "note": "MCP integration with Devin AI will be implemented to handle automatic agent creation and deployment"
        }

    except Exception as e:
        task.status = "failed"
        task.updated_at = datetime.utcnow()
        devin_tasks_db[task_id] = task
        raise HTTPException(
            status_code=500,
            detail=f"Error executing Devin task: {
                str(e)}")


def generate_devin_prompt(
        title: str,
        description: str,
        requirements: List[str],
        prd_id: str,
        task_id: str) -> str:
    """Generate an optimized prompt for Devin AI with MCP server integration"""
    prompt = f"""# Agent Development Task: {title}

## Description
{description}

## Requirements
{chr(10).join(f"- {req}" for req in requirements)}

## Task for Devin AI with MCP Integration

**IMPORTANT**: You are receiving a **completed, formatted PRD** from the AI Agent Factory platform. This PRD has already been created, validated, and is ready for implementation. Your role is to implement the agent based on these specifications.

Please create a complete AI agent implementation and deploy it automatically using your MCP servers:

### 1. **Agent Development**
- Create a modular, reusable agent structure
- Implement all requirements listed above
- Include comprehensive error handling and logging
- Add unit tests for core functionality
- Follow PEP 8 coding standards with proper type hints

### 2. **Automatic Deployment via MCP Servers**
Please use your MCP servers to:

**GitHub MCP Server:**
- **Base Repository:** `thedoctorJJ/end-cap-agent-factory` (https://github.com/thedoctorJJ/end-cap-agent-factory)
- **Create new repository:** `thedoctorJJ/end-cap-agent-{title.lower().replace(' ', '-').replace('🧠', '').replace('(', '').replace(')', '').replace(' ', '-')}`
- **Use base repository as template** for structure and configuration
- Commit the agent code to the new repository
- Set up proper branch protection and workflows

**Supabase MCP Server:**
- Create agent metadata in the database
- Set up necessary tables and relationships
- Configure authentication and permissions

**Deployment MCP Server:**
- Deploy the agent to the AI Agent Factory platform
- Configure environment variables and secrets
- Set up monitoring and logging

### 3. **Integration Specifications**
- **Platform**: AI Agent Factory
- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Next.js (TypeScript)
- **Deployment**: Google Cloud Run

### 4. **Repository Structure**
```
end-cap-agent-{title.lower().replace(' ', '-').replace('🧠', '').replace('(', '').replace(')', '').replace(' ', '-')}/
├── agent/
│   ├── main.py
│   ├── requirements.txt
│   └── config.py
├── tests/
│   └── test_agent.py
├── docs/
│   └── README.md
└── deployment/
    ├── Dockerfile
    └── cloud-run.yaml
```

### 5. **Database Schema**
Create the following tables in Supabase:
- `agents` - Agent metadata and configuration
- `agent_executions` - Execution logs and results
- `agent_metrics` - Performance and usage metrics

### 6. **API Endpoints**
Create FastAPI endpoints:
- `POST /api/v1/agents/{{agent_id}}/execute` - Execute agent
- `GET /api/v1/agents/{{agent_id}}/status` - Get agent status
- `GET /api/v1/agents/{{agent_id}}/metrics` - Get agent metrics
- `GET /health` - Health check endpoint (required for platform integration)

### 7. **Agent Registration with Platform**
After successful deployment, register the agent with the AI Agent Factory platform:

**Registration Endpoint:** `POST /api/v1/agents/register`

**Required Registration Data:**
```json
{{
  "name": "{title}",
  "description": "{description}",
  "purpose": "Agent purpose from PRD",
  "version": "1.0.0",
  "repository_url": "https://github.com/thedoctorJJ/end-cap-agent-{title.lower().replace(' ', '-').replace('🧠', '').replace('(', '').replace(')', '').replace(' ', '-')}",
  "deployment_url": "https://end-cap-agent-{title.lower().replace(' ', '-').replace('🧠', '').replace('(', '').replace(')', '').replace(' ', '-')}-hash.run.app",
  "health_check_url": "https://end-cap-agent-{title.lower().replace(' ', '-').replace('🧠', '').replace('(', '').replace(')', '').replace(' ', '-')}-hash.run.app/health",
  "prd_id": "{prd_id}",
  "devin_task_id": "{task_id}",
  "capabilities": ["capability1", "capability2"],
  "configuration": {{
    "environment": "production",
    "scaling": "auto"
  }}
}}
```

**Registration Steps:**
1. **Call Registration Endpoint** with agent metadata
2. **Verify Registration** - Check that agent appears in platform dashboard
3. **Test Health Checks** - Ensure health monitoring is working
4. **Update PRD Status** - Mark PRD as completed with deployed agent

## Expected Outcome
After completion, the agent should be:
1. ✅ **Fully deployed** and accessible via API
2. ✅ **Registered** with the AI Agent Factory platform
3. ✅ **Monitored** with proper logging and metrics
4. ✅ **Tested** with comprehensive test coverage
5. ✅ **Documented** with clear usage instructions
6. ✅ **Visible** in the platform dashboard with health status

## MCP Server Configuration
Please ensure your MCP servers are configured with:
- **GitHub**: Access to the AI Agent Factory organization
- **Supabase**: Connection to the platform database
- **Google Cloud**: Deployment permissions for Cloud Run

**Please use your MCP servers to handle the entire deployment process automatically.**"""

    return prompt


def format_for_devin_copy(prompt: str) -> str:
    """Format the prompt for easy copying to Devin AI"""
    return f"""
--- COPY THIS TO DEVIN AI ---

{prompt}

--- END COPY ---
"""


async def create_agent_from_task(task: DevinTask):
    """Create an actual agent from a completed Devin task"""
    from ..routers.agents import agents_db, AgentResponse
    from ..routers.prds import prds_db

    agent_id = str(uuid.uuid4())
    now = datetime.utcnow()

    # Generate agent name from PRD title
    agent_name = task.title.replace(" PRD", "").replace("PRD", "").strip()
    if not agent_name:
        agent_name = f"Agent-{agent_id[:8]}"

    # Create the agent
    new_agent = AgentResponse(
        id=agent_id,
        name=agent_name,
        description=task.description or "AI agent created from PRD",
        purpose=task.description or "Automated agent created by Devin AI",
        version="1.0.0",
        tools=[],  # Will be populated from requirements
        prompts=[],  # Will be populated from agent code
        status="deployed",
        repository_url=f"https://github.com/your-org/{
            agent_name.lower().replace(
                ' ', '-')}",
        deployment_url=f"https://{
            agent_name.lower().replace(
                ' ', '-')}.run.app",
        health_check_url=f"https://{
            agent_name.lower().replace(
                ' ', '-')}.run.app/health",
        prd_id=task.prd_id,
        devin_task_id=task.id,
        capabilities=task.requirements or [],
        configuration={"devin_generated": True, "task_id": task.id},
        last_health_check=None,
        health_status="unknown",
        created_at=now,
        updated_at=now
    )

    # Store the agent
    agents_db[agent_id] = new_agent

    # Update PRD status to "processed"
    if task.prd_id and task.prd_id in prds_db:
        prd = prds_db[task.prd_id]
        prd.status = "processed"
        prd.updated_at = now
        prds_db[task.prd_id] = prd

    return new_agent
