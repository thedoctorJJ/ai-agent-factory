from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
from ..config import config

router = APIRouter()

# Pydantic models
class PRDCreate(BaseModel):
    title: str
    description: str
    requirements: List[str]
    voice_input: Optional[str] = None
    text_input: Optional[str] = None
    prd_type: Optional[str] = "agent"  # "platform" | "agent"
    
    # Enhanced PRD sections
    problem_statement: Optional[str] = None
    target_users: Optional[List[str]] = None
    user_stories: Optional[List[str]] = None
    acceptance_criteria: Optional[List[str]] = None
    technical_requirements: Optional[List[str]] = None
    performance_requirements: Optional[Dict[str, str]] = None
    security_requirements: Optional[List[str]] = None
    integration_requirements: Optional[List[str]] = None
    deployment_requirements: Optional[List[str]] = None
    success_metrics: Optional[List[str]] = None
    timeline: Optional[str] = None
    dependencies: Optional[List[str]] = None
    risks: Optional[List[str]] = None
    assumptions: Optional[List[str]] = None
    
    # Roadmap-specific fields
    category: Optional[str] = None
    priority_score: Optional[int] = None
    effort_estimate: Optional[str] = None  # "small", "medium", "large", "epic"
    business_value: Optional[int] = None  # 1-10 scale
    technical_complexity: Optional[int] = None  # 1-10 scale
    dependencies_list: Optional[List[str]] = None
    assignee: Optional[str] = None
    target_sprint: Optional[str] = None

class PRDResponse(BaseModel):
    id: str
    title: str
    description: str
    requirements: List[str]
    voice_input: Optional[str]
    text_input: Optional[str]
    prd_type: str
    status: str
    github_repo_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Enhanced PRD sections
    problem_statement: Optional[str] = None
    target_users: Optional[List[str]] = None
    user_stories: Optional[List[str]] = None
    acceptance_criteria: Optional[List[str]] = None
    technical_requirements: Optional[List[str]] = None
    performance_requirements: Optional[Dict[str, str]] = None
    security_requirements: Optional[List[str]] = None
    integration_requirements: Optional[List[str]] = None
    deployment_requirements: Optional[List[str]] = None
    success_metrics: Optional[List[str]] = None
    timeline: Optional[str] = None
    dependencies: Optional[List[str]] = None
    risks: Optional[List[str]] = None
    assumptions: Optional[List[str]] = None
    
    # Completion tracking
    completion_percentage: Optional[int] = None
    missing_sections: Optional[List[str]] = None
    
    # Roadmap-specific fields
    category: Optional[str] = None
    priority_score: Optional[int] = None
    effort_estimate: Optional[str] = None
    business_value: Optional[int] = None
    technical_complexity: Optional[int] = None
    dependencies_list: Optional[List[str]] = None
    assignee: Optional[str] = None
    target_sprint: Optional[str] = None

class PRDUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    prd_type: Optional[str] = None
    status: Optional[str] = None
    github_repo_url: Optional[str] = None

# In-memory storage for demo (replace with Supabase in production)
prds_db = {}

# Roadmap-specific storage
roadmap_db = {
    "categories": {
        "core_functionality": {
            "name": "Core Functionality",
            "description": "Essential features for basic platform operation",
            "color": "#ef4444",
            "priority": 1
        },
        "production_readiness": {
            "name": "Production Readiness", 
            "description": "Features needed for production deployment",
            "color": "#f97316",
            "priority": 2
        },
        "performance_scale": {
            "name": "Performance & Scale",
            "description": "Optimization and scalability improvements",
            "color": "#eab308",
            "priority": 3
        },
        "user_experience": {
            "name": "User Experience",
            "description": "UI/UX improvements and user-facing features",
            "color": "#22c55e",
            "priority": 4
        },
        "platform_features": {
            "name": "Platform Features",
            "description": "Advanced platform capabilities and integrations",
            "color": "#3b82f6",
            "priority": 5
        }
    },
    "statuses": {
        "backlog": {"name": "Backlog", "color": "#6b7280", "order": 1},
        "planned": {"name": "Planned", "color": "#3b82f6", "order": 2},
        "in_progress": {"name": "In Progress", "color": "#f59e0b", "order": 3},
        "review": {"name": "Review", "color": "#8b5cf6", "order": 4},
        "completed": {"name": "Completed", "color": "#10b981", "order": 5},
        "cancelled": {"name": "Cancelled", "color": "#ef4444", "order": 6}
    }
}

@router.get("/prds/schema")
async def get_prd_schema():
    """Return JSON schema for PRDCreate to enforce standard format"""
    try:
        return PRDCreate.model_json_schema()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PRD schema: {str(e)}")

@router.get("/prds", response_model=List[PRDResponse])
async def get_prds():
    """Get all PRDs"""
    try:
        return list(prds_db.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve PRDs: {str(e)}")

@router.get("/prds/{prd_id}", response_model=PRDResponse)
async def get_prd(prd_id: str):
    """Get a specific PRD by ID"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    return prds_db[prd_id]

@router.post("/prds", response_model=PRDResponse)
async def create_prd(prd: PRDCreate):
    """Create a new PRD"""
    try:
        prd_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        # Calculate completion percentage and missing sections
        completion_data = calculate_prd_completion(prd)
        
        # Strict validation of required sections
        if config.strict_prd:
            required_sections = [
                "title",
                "description",
                "problem_statement",
                "target_users",
                "user_stories",
                "requirements",
                "acceptance_criteria",
                "technical_requirements",
                "success_metrics",
                "timeline",
            ]
            missing_required = []
            for section in required_sections:
                value = getattr(prd, section, None)
                if value is None or value == [] or value == {} or (isinstance(value, str) and not value.strip()):
                    missing_required.append(section)
            if missing_required:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "message": "PRD missing required sections",
                        "missing_sections": missing_required
                    }
                )
        
        new_prd = PRDResponse(
            id=prd_id,
            title=prd.title,
            description=prd.description,
            requirements=prd.requirements,
            voice_input=prd.voice_input,
            text_input=prd.text_input,
            prd_type=(prd.prd_type or "agent"),
            status="ready_for_agent_creation" if completion_data["completion_percentage"] >= 80 else "needs_review",
            github_repo_url=None,
            created_at=now,
            updated_at=now,
            
            # Enhanced PRD sections
            problem_statement=prd.problem_statement,
            target_users=prd.target_users,
            user_stories=prd.user_stories,
            acceptance_criteria=prd.acceptance_criteria,
            technical_requirements=prd.technical_requirements,
            performance_requirements=prd.performance_requirements,
            security_requirements=prd.security_requirements,
            integration_requirements=prd.integration_requirements,
            deployment_requirements=prd.deployment_requirements,
            success_metrics=prd.success_metrics,
            timeline=prd.timeline,
            dependencies=prd.dependencies,
            risks=prd.risks,
            assumptions=prd.assumptions,
            
            # Completion tracking
            completion_percentage=completion_data["completion_percentage"],
            missing_sections=completion_data["missing_sections"],
            
            # Roadmap-specific fields
            category=prd.category,
            priority_score=prd.priority_score,
            effort_estimate=prd.effort_estimate,
            business_value=prd.business_value,
            technical_complexity=prd.technical_complexity,
            dependencies_list=prd.dependencies_list,
            assignee=prd.assignee,
            target_sprint=prd.target_sprint
        )
    
        prds_db[prd_id] = new_prd
        
        # TODO: Trigger MCP service to create GitHub repo
        # TODO: Trigger Devin AI orchestration
        
        return new_prd
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create PRD: {str(e)}")

@router.put("/prds/{prd_id}", response_model=PRDResponse)
async def update_prd(prd_id: str, prd_update: PRDUpdate):
    """Update an existing PRD"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    
    existing_prd = prds_db[prd_id]
    update_data = prd_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing_prd, field, value)
    
    # Prevent setting status=submitted unless completion is 100%
    if config.strict_prd and getattr(existing_prd, "status", "").lower() == "submitted":
        # Re-evaluate completion using current fields
        temp_create = PRDCreate(
            title=existing_prd.title,
            description=existing_prd.description,
            requirements=existing_prd.requirements,
            voice_input=existing_prd.voice_input,
            text_input=existing_prd.text_input,
            problem_statement=existing_prd.problem_statement,
            target_users=existing_prd.target_users,
            user_stories=existing_prd.user_stories,
            acceptance_criteria=existing_prd.acceptance_criteria,
            technical_requirements=existing_prd.technical_requirements,
            performance_requirements=existing_prd.performance_requirements,
            security_requirements=existing_prd.security_requirements,
            integration_requirements=existing_prd.integration_requirements,
            deployment_requirements=existing_prd.deployment_requirements,
            success_metrics=existing_prd.success_metrics,
            timeline=existing_prd.timeline,
            dependencies=existing_prd.dependencies,
            risks=existing_prd.risks,
            assumptions=existing_prd.assumptions,
            category=getattr(existing_prd, "category", None),
            priority_score=getattr(existing_prd, "priority_score", None),
            effort_estimate=getattr(existing_prd, "effort_estimate", None),
            business_value=getattr(existing_prd, "business_value", None),
            technical_complexity=getattr(existing_prd, "technical_complexity", None),
            dependencies_list=getattr(existing_prd, "dependencies_list", None),
            assignee=getattr(existing_prd, "assignee", None),
            target_sprint=getattr(existing_prd, "target_sprint", None),
        )
        completion_data = calculate_prd_completion(temp_create)
        if completion_data["completion_percentage"] < 100:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Cannot submit PRD until 100% complete",
                    "completion_percentage": completion_data["completion_percentage"],
                    "missing_sections": completion_data["missing_sections"]
                }
            )
        existing_prd.completion_percentage = completion_data["completion_percentage"]
        existing_prd.missing_sections = completion_data["missing_sections"]
    
    existing_prd.updated_at = datetime.utcnow()
    prds_db[prd_id] = existing_prd
    
    return existing_prd

@router.delete("/prds/{prd_id}")
async def delete_prd(prd_id: str):
    """Delete a PRD"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    
    del prds_db[prd_id]
    return {"message": "PRD deleted successfully"}

@router.get("/prds/{prd_id}/markdown")
async def get_prd_markdown(prd_id: str):
    """Get PRD as markdown for sharing with Devin AI"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    
    prd = prds_db[prd_id]
    markdown_content = generate_prd_markdown(prd)
    
    return {
        "prd_id": prd_id,
        "markdown": markdown_content,
        "filename": f"PRD_{prd.title.replace(' ', '_')}_{prd_id[:8]}.md"
    }

@router.get("/prds/{prd_id}/markdown/download")
async def download_prd_markdown(prd_id: str):
    """Download PRD as markdown file"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    
    prd = prds_db[prd_id]
    markdown_content = generate_prd_markdown(prd)
    filename = f"PRD_{prd.title.replace(' ', '_')}_{prd_id[:8]}.md"
    
    return Response(
        content=markdown_content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

def generate_prd_markdown(prd: PRDResponse) -> str:
    """Generate standardized markdown PRD for Devin AI"""
    
    # Determine input source (legacy field - now all PRDs are completed and formatted)
    input_source = "Completed PRD"
    original_input = prd.voice_input or prd.text_input or "No original input provided"
    
    markdown = f"""# Product Requirements Document (PRD)
## {prd.title}

---

### 📋 **Document Information**
- **PRD ID**: `{prd.id}`
- **Status**: {prd.status.title()}
- **Completion**: {prd.completion_percentage}%
- **Created**: {prd.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
- **Input Method**: {input_source}
- **Last Updated**: {prd.updated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}

---

### 🎯 **Project Overview**

**Description:**
{prd.description}

"""
    
    # Add problem statement if available
    if prd.problem_statement:
        markdown += f"""### 🎯 **Problem Statement**

{prd.problem_statement}

"""
    
    # Add target users if available
    if prd.target_users:
        markdown += f"""### 👥 **Target Users**

"""
        for user in prd.target_users:
            markdown += f"- {user}\n"
        markdown += "\n"
    
    # Add user stories if available
    if prd.user_stories:
        markdown += f"""### 📖 **User Stories**

"""
        for story in prd.user_stories:
            markdown += f"- {story}\n"
        markdown += "\n"
    
    # Add original input (if available)
    if original_input and original_input != "No original input provided":
        markdown += f"""### 📝 **Original Input**
*This section contains the original input that generated this PRD*

```
{original_input}
```

---

### ✅ **Requirements**

The following requirements must be implemented:

"""
    
    # Add requirements as numbered list
    for i, requirement in enumerate(prd.requirements, 1):
        markdown += f"{i}. {requirement}\n"
    
    # Add acceptance criteria if available
    if prd.acceptance_criteria:
        markdown += f"""
---

### ✅ **Acceptance Criteria**

The following criteria must be met for successful completion:

"""
        for i, criteria in enumerate(prd.acceptance_criteria, 1):
            markdown += f"{i}. {criteria}\n"
    
    # Add technical requirements if available
    if prd.technical_requirements:
        markdown += f"""
---

### 🔧 **Technical Requirements**

"""
        for i, req in enumerate(prd.technical_requirements, 1):
            markdown += f"{i}. {req}\n"
    
    # Add performance requirements if available
    if prd.performance_requirements:
        markdown += f"""
---

### ⚡ **Performance Requirements**

"""
        for key, value in prd.performance_requirements.items():
            markdown += f"- **{key}**: {value}\n"
    
    # Add security requirements if available
    if prd.security_requirements:
        markdown += f"""
---

### 🔒 **Security Requirements**

"""
        for i, req in enumerate(prd.security_requirements, 1):
            markdown += f"{i}. {req}\n"
    
    # Add integration requirements if available
    if prd.integration_requirements:
        markdown += f"""
---

### 🔗 **Integration Requirements**

"""
        for i, req in enumerate(prd.integration_requirements, 1):
            markdown += f"{i}. {req}\n"
    
    # Add deployment requirements if available
    if prd.deployment_requirements:
        markdown += f"""
---

### 🚀 **Deployment Requirements**

"""
        for i, req in enumerate(prd.deployment_requirements, 1):
            markdown += f"{i}. {req}\n"
    
    # Add success metrics if available
    if prd.success_metrics:
        markdown += f"""
---

### 📊 **Success Metrics**

The following metrics will be used to measure success:

"""
        for i, metric in enumerate(prd.success_metrics, 1):
            markdown += f"{i}. {metric}\n"
    
    # Add timeline if available
    if prd.timeline:
        markdown += f"""
---

### ⏰ **Timeline**

{prd.timeline}

"""
    
    # Add dependencies if available
    if prd.dependencies:
        markdown += f"""
---

### 📦 **Dependencies**

The following dependencies are required:

"""
        for i, dep in enumerate(prd.dependencies, 1):
            markdown += f"{i}. {dep}\n"
    
    # Add risks if available
    if prd.risks:
        markdown += f"""
---

### ⚠️ **Risks**

The following risks have been identified:

"""
        for i, risk in enumerate(prd.risks, 1):
            markdown += f"{i}. {risk}\n"
    
    # Add assumptions if available
    if prd.assumptions:
        markdown += f"""
---

### 💭 **Assumptions**

The following assumptions are being made:

"""
        for i, assumption in enumerate(prd.assumptions, 1):
            markdown += f"{i}. {assumption}\n"
    
    markdown += f"""
---

### 🏗️ **Technical Specifications**

#### **Platform Requirements**
- **Target Platform**: AI Agent Factory
- **Backend Framework**: FastAPI (Python 3.11+)
- **Frontend Framework**: Next.js 14 (TypeScript)
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Google Cloud Run
- **Authentication**: JWT-based auth system

#### **Integration Requirements**
- **MCP Server Integration**: Must work with existing MCP server at `https://end-cap-mcp-server-http-fdqqqinvyq-uc.a.run.app`
- **GitHub Integration**: Automatic repository creation and management
- **Supabase Integration**: Database schema and metadata management
- **Google Cloud Integration**: Deployment and monitoring setup

#### **Repository Structure**
```
end-cap-agent-{prd.title.lower().replace(' ', '-')}/
├── agent/
│   ├── main.py                 # Main agent logic
│   ├── requirements.txt        # Python dependencies
│   ├── config.py              # Configuration management
│   └── utils.py               # Utility functions
├── tests/
│   ├── test_agent.py          # Unit tests
│   └── test_integration.py    # Integration tests
├── docs/
│   ├── README.md              # Agent documentation
│   ├── API.md                 # API documentation
│   └── DEPLOYMENT.md          # Deployment guide
├── deployment/
│   ├── Dockerfile             # Container configuration
│   ├── cloud-run.yaml         # Google Cloud Run config
│   └── .env.example           # Environment variables template
└── .github/
    └── workflows/
        └── deploy.yml         # CI/CD pipeline
```

---

### 🚀 **Devin AI Implementation Instructions**

**IMPORTANT**: This is a **completed, formatted PRD** from the AI Agent Factory platform. This PRD has already been created, validated, and is ready for implementation. Your role is to implement the agent based on these specifications.

#### **Phase 1: Agent Development**
1. **Create Agent Structure**
   - Implement modular, reusable agent architecture
   - Add comprehensive error handling and logging
   - Include type hints and follow PEP 8 standards
   - Create unit tests with >80% coverage

2. **Core Functionality**
   - Implement all requirements listed above
   - Add configuration management system
   - Include health check endpoints
   - Implement proper logging and monitoring

#### **Phase 2: Database Setup**
Use the Supabase MCP server to:
- Create agent metadata tables
- Set up proper relationships and constraints
- Configure authentication and permissions
- Add vector storage for AI capabilities (if needed)

#### **Phase 3: Repository Creation**
Use the GitHub MCP server to:
- Create repository: `thedoctorJJ/end-cap-agent-{prd.title.lower().replace(' ', '-')}`
- Use `thedoctorJJ/end-cap-agent-factory` as template
- Set up proper branch protection
- Configure GitHub Actions workflows

#### **Phase 4: Deployment**
Use the Deployment MCP server to:
- Deploy to Google Cloud Run
- Configure environment variables
- Set up monitoring and alerting
- Integrate with AI Agent Factory platform APIs

#### **Phase 5: Agent Registration**
After successful deployment, register the agent with the AI Agent Factory platform:

**Registration Endpoint:** `POST /api/v1/agents/register`

**Required Registration Data:**
```json
{
  "name": "{prd.title}",
  "description": "{prd.description}",
  "purpose": "Agent purpose from PRD",
  "version": "1.0.0",
  "repository_url": "https://github.com/thedoctorJJ/end-cap-agent-{prd.title.lower().replace(' ', '-')}",
  "deployment_url": "https://end-cap-agent-{prd.title.lower().replace(' ', '-')}-hash.run.app",
  "health_check_url": "https://end-cap-agent-{prd.title.lower().replace(' ', '-')}-hash.run.app/health",
  "prd_id": "{prd.id}",
  "devin_task_id": "{task_id_from_platform}",
  "capabilities": ["capability1", "capability2"],
  "configuration": {
    "environment": "production",
    "scaling": "auto"
  }
}
```

**Registration Steps:**
1. **Call Registration Endpoint** with agent metadata
2. **Verify Registration** - Check that agent appears in platform dashboard
3. **Test Health Checks** - Ensure health monitoring is working
4. **Update PRD Status** - Mark PRD as completed with deployed agent

#### **Phase 6: Integration**
- Test all API endpoints
- Verify MCP server integration
- Complete end-to-end testing

---

### 📊 **Success Criteria**

The implementation will be considered successful when:

- [ ] **Agent is fully functional** and meets all requirements
- [ ] **Repository is created** with proper structure and documentation
- [ ] **Database is configured** with all necessary tables and relationships
- [ ] **Deployment is live** and accessible via Google Cloud Run
- [ ] **Integration is complete** with AI Agent Factory platform
- [ ] **Tests are passing** with comprehensive coverage
- [ ] **Documentation is complete** with usage examples
- [ ] **Monitoring is active** with proper logging and metrics

---

### 🔗 **Related Resources**

- **AI Agent Factory**: https://github.com/thedoctorJJ/end-cap-agent-factory
- **MCP Server**: https://end-cap-mcp-server-http-fdqqqinvyq-uc.a.run.app
- **API Documentation**: http://localhost:8000/docs (when running locally)
- **Platform Dashboard**: http://localhost:3000 (when running locally)

---

### 📞 **Support & Questions**

For questions about this PRD or implementation:
- **Platform Issues**: Check AI Agent Factory documentation
- **MCP Integration**: Refer to MCP server documentation
- **Deployment Issues**: Check Google Cloud Run logs
- **Database Issues**: Check Supabase dashboard

---

*This PRD was generated by the AI Agent Factory platform and is ready for implementation by Devin AI.*
"""
    
    return markdown

def calculate_prd_completion(prd: PRDCreate) -> dict:
    """Calculate PRD completion percentage and identify missing sections"""
    
    # Define all required sections with their weights
    sections = {
        "title": 5,
        "description": 10,
        "problem_statement": 15,
        "target_users": 10,
        "user_stories": 10,
        "requirements": 15,
        "acceptance_criteria": 10,
        "technical_requirements": 10,
        "success_metrics": 10,
        "timeline": 5
    }
    
    # Define optional but recommended sections
    optional_sections = {
        "performance_requirements": 3,
        "security_requirements": 3,
        "integration_requirements": 3,
        "deployment_requirements": 3,
        "dependencies": 2,
        "risks": 2,
        "assumptions": 2
    }
    
    total_weight = sum(sections.values()) + sum(optional_sections.values())
    completed_weight = 0
    missing_sections = []
    
    # Check required sections
    for section, weight in sections.items():
        value = getattr(prd, section, None)
        if value is not None and value != [] and value != {}:
            completed_weight += weight
        else:
            missing_sections.append(section)
    
    # Check optional sections
    for section, weight in optional_sections.items():
        value = getattr(prd, section, None)
        if value is not None and value != [] and value != {}:
            completed_weight += weight
        else:
            missing_sections.append(f"{section} (optional)")
    
    completion_percentage = int((completed_weight / total_weight) * 100)
    
    return {
        "completion_percentage": completion_percentage,
        "missing_sections": missing_sections
    }

@router.get("/prds/{prd_id}/completion")
async def get_prd_completion(prd_id: str):
    """Get PRD completion status and missing sections"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    
    prd = prds_db[prd_id]
    return {
        "prd_id": prd_id,
        "completion_percentage": prd.completion_percentage,
        "missing_sections": prd.missing_sections,
        "status": prd.status
    }

@router.get("/prds/{prd_id}/guided-questions")
async def get_guided_questions(prd_id: str):
    """Get guided questions for missing PRD sections"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    
    prd = prds_db[prd_id]
    questions = generate_guided_questions(prd)
    
    return {
        "prd_id": prd_id,
        "title": prd.title,
        "completion_percentage": prd.completion_percentage,
        "questions": questions
    }

def generate_guided_questions(prd: PRDResponse) -> List[dict]:
    """Generate guided questions for missing PRD sections"""
    questions = []
    
    question_templates = {
        "problem_statement": {
            "question": "What specific problem does this agent solve?",
            "sub_questions": [
                "What pain point are you addressing?",
                "Why is this problem important to solve?",
                "What happens if this problem isn't solved?"
            ],
            "example": "Users currently spend 2 hours daily manually processing emails, leading to missed opportunities and decreased productivity."
        },
        "target_users": {
            "question": "Who will use this agent?",
            "sub_questions": [
                "What is their role or job title?",
                "What is their technical skill level?",
                "What are their main goals and motivations?"
            ],
            "example": "Customer service representatives, sales managers, busy executives"
        },
        "user_stories": {
            "question": "How will users interact with this agent?",
            "sub_questions": [
                "What is the typical user workflow?",
                "What actions will users take?",
                "What outcomes do they expect?"
            ],
            "example": "As a customer service rep, I want to automatically categorize incoming emails so I can prioritize urgent requests."
        },
        "acceptance_criteria": {
            "question": "How will you know the agent is working correctly?",
            "sub_questions": [
                "What specific behaviors should the agent demonstrate?",
                "What outputs or responses are expected?",
                "What error conditions should be handled?"
            ],
            "example": "The agent should correctly categorize 95% of emails within 2 seconds and provide confidence scores for each classification."
        },
        "technical_requirements": {
            "question": "What technical capabilities does the agent need?",
            "sub_questions": [
                "What APIs or services must it integrate with?",
                "What data processing capabilities are required?",
                "What performance or scalability needs exist?"
            ],
            "example": "Must integrate with Gmail API, process 1000 emails/hour, support real-time streaming"
        },
        "success_metrics": {
            "question": "How will you measure the agent's success?",
            "sub_questions": [
                "What quantitative metrics matter?",
                "What qualitative outcomes are important?",
                "How will you track user satisfaction?"
            ],
            "example": "Reduce email processing time by 80%, achieve 95% accuracy rate, maintain 4.5+ user satisfaction score"
        },
        "timeline": {
            "question": "When do you need this agent completed?",
            "sub_questions": [
                "What is your target launch date?",
                "Are there any critical milestones or deadlines?",
                "What is the minimum viable version timeline?"
            ],
            "example": "MVP by end of Q1, full feature set by end of Q2"
        },
        "performance_requirements": {
            "question": "What performance standards must the agent meet?",
            "sub_questions": [
                "What response time is acceptable?",
                "How many concurrent users should it support?",
                "What uptime requirements exist?"
            ],
            "example": "Response time < 2 seconds, support 100 concurrent users, 99.9% uptime"
        },
        "security_requirements": {
            "question": "What security measures are needed?",
            "sub_questions": [
                "What data protection requirements exist?",
                "What authentication or authorization is needed?",
                "Are there compliance requirements?"
            ],
            "example": "Encrypt all data in transit and at rest, implement OAuth 2.0, comply with GDPR"
        },
        "integration_requirements": {
            "question": "What systems must the agent integrate with?",
            "sub_questions": [
                "What existing tools or platforms?",
                "What data sources or APIs?",
                "What notification or alerting systems?"
            ],
            "example": "Slack for notifications, Salesforce for CRM data, Zapier for workflow automation"
        },
        "deployment_requirements": {
            "question": "How should the agent be deployed and managed?",
            "sub_questions": [
                "What hosting environment is preferred?",
                "What monitoring and logging is needed?",
                "What backup and recovery requirements exist?"
            ],
            "example": "Deploy to Google Cloud Run, use CloudWatch for monitoring, daily automated backups"
        },
        "dependencies": {
            "question": "What external dependencies does this agent have?",
            "sub_questions": [
                "What third-party services or APIs?",
                "What data sources or databases?",
                "What other systems or agents?"
            ],
            "example": "OpenAI API for language processing, PostgreSQL database, existing user authentication system"
        },
        "risks": {
            "question": "What risks could impact this project?",
            "sub_questions": [
                "What technical risks exist?",
                "What business or user adoption risks?",
                "What external dependencies could fail?"
            ],
            "example": "API rate limits, user resistance to automation, third-party service outages"
        },
        "assumptions": {
            "question": "What assumptions are you making about this project?",
            "sub_questions": [
                "What do you assume about user behavior?",
                "What technical assumptions are you making?",
                "What business or market assumptions?"
            ],
            "example": "Users will trust automated responses, API costs will remain stable, target users have basic technical skills"
        }
    }
    
    for section in prd.missing_sections:
        # Remove "(optional)" suffix if present
        clean_section = section.replace(" (optional)", "")
        if clean_section in question_templates:
            questions.append({
                "section": clean_section,
                "is_optional": "(optional)" in section,
                **question_templates[clean_section]
            })
    
    return questions

# Roadmap-specific endpoints
@router.get("/roadmap/categories")
async def get_roadmap_categories():
    """Get all roadmap categories"""
    return roadmap_db["categories"]

@router.get("/roadmap/statuses")
async def get_roadmap_statuses():
    """Get all roadmap statuses"""
    return roadmap_db["statuses"]

@router.get("/roadmap/overview")
async def get_roadmap_overview():
    """Get roadmap overview with statistics"""
    try:
        prds = list(prds_db.values())
        
        # Calculate statistics
        total_prds = len(prds)
        by_status = {}
        by_category = {}
        by_effort = {}
        
        for prd in prds:
            # Status breakdown
            status = prd.status if hasattr(prd, 'status') else 'backlog'
            by_status[status] = by_status.get(status, 0) + 1
            
            # Category breakdown
            category = getattr(prd, 'category', 'uncategorized')
            by_category[category] = by_category.get(category, 0) + 1
            
            # Effort breakdown
            effort = getattr(prd, 'effort_estimate', 'unknown')
            by_effort[effort] = by_effort.get(effort, 0) + 1
        
        # Calculate priority scores
        priority_prds = [prd for prd in prds if hasattr(prd, 'priority_score') and prd.priority_score]
        if priority_prds:
            avg_priority = sum(prd.priority_score for prd in priority_prds) / len(priority_prds)
        else:
            avg_priority = 0
        
        return {
            "total_prds": total_prds,
            "by_status": by_status,
            "by_category": by_category,
            "by_effort": by_effort,
            "average_priority_score": round(avg_priority, 2),
            "categories": roadmap_db["categories"],
            "statuses": roadmap_db["statuses"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roadmap overview: {str(e)}")

@router.get("/roadmap/prds")
async def get_roadmap_prds(
    category: Optional[str] = None,
    status: Optional[str] = None,
    effort: Optional[str] = None,
    prd_type: Optional[str] = None,
    sort_by: Optional[str] = "priority_score",
    sort_order: Optional[str] = "desc"
):
    """Get PRDs with roadmap filtering and sorting"""
    try:
        prds = list(prds_db.values())
        
        # Apply filters
        if category:
            prds = [prd for prd in prds if getattr(prd, 'category', None) == category]
        
        if status:
            prds = [prd for prd in prds if getattr(prd, 'status', 'backlog') == status]
        
        if effort:
            prds = [prd for prd in prds if getattr(prd, 'effort_estimate', None) == effort]
        
        if prd_type:
            prds = [prd for prd in prds if getattr(prd, 'prd_type', 'agent') == prd_type]
        
        # Apply sorting
        if sort_by == "priority_score":
            prds.sort(key=lambda x: getattr(x, 'priority_score', 0), reverse=(sort_order == "desc"))
        elif sort_by == "created_at":
            prds.sort(key=lambda x: x.created_at, reverse=(sort_order == "desc"))
        elif sort_by == "title":
            prds.sort(key=lambda x: x.title, reverse=(sort_order == "desc"))
        
        return prds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roadmap PRDs: {str(e)}")

@router.put("/roadmap/prds/{prd_id}/priority")
async def update_prd_priority(prd_id: str, priority_data: dict):
    """Update PRD priority and roadmap fields"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    
    prd = prds_db[prd_id]
    
    # Update roadmap fields
    if 'priority_score' in priority_data:
        prd.priority_score = priority_data['priority_score']
    if 'category' in priority_data:
        prd.category = priority_data['category']
    if 'effort_estimate' in priority_data:
        prd.effort_estimate = priority_data['effort_estimate']
    if 'business_value' in priority_data:
        prd.business_value = priority_data['business_value']
    if 'technical_complexity' in priority_data:
        prd.technical_complexity = priority_data['technical_complexity']
    if 'assignee' in priority_data:
        prd.assignee = priority_data['assignee']
    if 'target_sprint' in priority_data:
        prd.target_sprint = priority_data['target_sprint']
    if 'status' in priority_data:
        prd.status = priority_data['status']
    
    prd.updated_at = datetime.utcnow()
    prds_db[prd_id] = prd
    
    return prd

@router.get("/roadmap/prioritization-matrix")
async def get_prioritization_matrix():
    """Get PRDs organized by business value vs technical complexity"""
    try:
        prds = list(prds_db.values())
        
        matrix = {
            "high_value_low_complexity": [],  # Quick wins
            "high_value_high_complexity": [],  # Major projects
            "low_value_low_complexity": [],  # Fill-ins
            "low_value_high_complexity": []  # Question marks
        }
        
        for prd in prds:
            business_value = getattr(prd, 'business_value', 5)
            technical_complexity = getattr(prd, 'technical_complexity', 5)
            
            if business_value >= 7 and technical_complexity <= 4:
                matrix["high_value_low_complexity"].append(prd)
            elif business_value >= 7 and technical_complexity >= 7:
                matrix["high_value_high_complexity"].append(prd)
            elif business_value <= 4 and technical_complexity <= 4:
                matrix["low_value_low_complexity"].append(prd)
            else:
                matrix["low_value_high_complexity"].append(prd)
        
        return matrix
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get prioritization matrix: {str(e)}")

@router.post("/prds/{prd_id}/chat")
async def chat_with_prd(prd_id: str, request: dict):
    """Chat with agent creation assistant"""
    try:
        if prd_id not in prds_db:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        prd = prds_db[prd_id]
        user_message = request.get("message", "")
        context = request.get("context", {})
        
        # Get current completion status
        completion_data = calculate_prd_completion(prd)
        missing_sections = completion_data["missing_sections"]
        
        # Analyze user input and provide agent creation guidance
        response = generate_agent_creation_response(prd, user_message, missing_sections, context)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process chat: {str(e)}")

def generate_agent_creation_response(prd, user_message: str, missing_sections: list, context: dict) -> dict:
    """Generate intelligent, contextual responses for agent creation guidance"""
    
    message_lower = user_message.lower()
    
    # First, provide agent creation analysis if user asks for it
    if any(phrase in message_lower for phrase in ["analyze", "review", "what do you think", "feedback", "assessment", "evaluation", "create agent", "generate agent"]):
        return generate_agent_creation_analysis(prd, missing_sections)
    
    # Determine what section the user is likely working on
    current_section = None
    updated_content = None
    
    # Smart section detection based on user input
    if any(word in message_lower for word in ["problem", "issue", "challenge", "solve", "address"]):
        current_section = "problem_statement"
        if not prd.problem_statement or prd.problem_statement.strip() == "":
            updated_content = user_message
    elif any(word in message_lower for word in ["user", "customer", "audience", "who", "people"]):
        current_section = "target_users"
        if not prd.target_users or len(prd.target_users) == 0:
            updated_content = [user_message]
    elif any(word in message_lower for word in ["requirement", "need", "must", "should", "feature"]):
        current_section = "requirements"
        if not prd.requirements or len(prd.requirements) == 0:
            updated_content = [user_message]
    elif any(word in message_lower for word in ["success", "metric", "measure", "kpi", "goal"]):
        current_section = "success_metrics"
        if not prd.success_metrics or len(prd.success_metrics) == 0:
            updated_content = [user_message]
    elif any(word in message_lower for word in ["timeline", "schedule", "deadline", "when", "time"]):
        current_section = "timeline"
        if not prd.timeline or prd.timeline.strip() == "":
            updated_content = user_message
    elif any(word in message_lower for word in ["story", "scenario", "as a", "i want"]):
        current_section = "user_stories"
        if not prd.user_stories or len(prd.user_stories) == 0:
            updated_content = [user_message]
    elif any(word in message_lower for word in ["criteria", "acceptance", "test", "verify"]):
        current_section = "acceptance_criteria"
        if not prd.acceptance_criteria or len(prd.acceptance_criteria) == 0:
            updated_content = [user_message]
    elif any(word in message_lower for word in ["technical", "tech", "api", "system", "architecture"]):
        current_section = "technical_requirements"
        if not prd.technical_requirements or len(prd.technical_requirements) == 0:
            updated_content = [user_message]
    
    # Generate contextual response
    if current_section and updated_content:
        # Update the PRD with new content
        if current_section == "problem_statement":
            prd.problem_statement = updated_content
        elif current_section == "target_users":
            prd.target_users = updated_content
        elif current_section == "requirements":
            prd.requirements = updated_content
        elif current_section == "success_metrics":
            prd.success_metrics = updated_content
        elif current_section == "timeline":
            prd.timeline = updated_content
        elif current_section == "user_stories":
            prd.user_stories = updated_content
        elif current_section == "acceptance_criteria":
            prd.acceptance_criteria = updated_content
        elif current_section == "technical_requirements":
            prd.technical_requirements = updated_content
        
        # Recalculate completion
        completion_data = calculate_prd_completion(prd)
        
        # Generate smart follow-up
        if current_section == "problem_statement":
            response_text = f"Perfect! I've captured your problem statement: **{user_message}**\n\nNow let's think about who this problem affects. Who are the main users or customers that experience this issue?"
            suggestions = [
                "Who are the primary users?",
                "What types of customers face this problem?",
                "Who would benefit from this solution?"
            ]
        elif current_section == "target_users":
            response_text = f"Great! I've noted your target users: **{user_message}**\n\nNow let's define what this agent needs to do. What are the main requirements or features it should have?"
            suggestions = [
                "What are the core features needed?",
                "What should the agent be able to do?",
                "What are the main requirements?"
            ]
        elif current_section == "requirements":
            response_text = f"Excellent! I've added that requirement: **{user_message}**\n\nNow let's think about how we'll know if this agent is successful. What metrics or outcomes would indicate success?"
            suggestions = [
                "How will we measure success?",
                "What are the key performance indicators?",
                "What outcomes indicate the agent is working?"
            ]
        elif current_section == "success_metrics":
            response_text = f"Perfect! I've captured your success metric: **{user_message}**\n\nNow let's think about the timeline. When do you need this agent to be ready?"
            suggestions = [
                "What's the target completion date?",
                "When do you need this deployed?",
                "What's the project timeline?"
            ]
        elif current_section == "timeline":
            response_text = f"Great! I've noted your timeline: **{user_message}**\n\nLet's think about the technical aspects. What technical requirements or constraints should we consider?"
            suggestions = [
                "What technical requirements are needed?",
                "Are there any system constraints?",
                "What APIs or integrations are required?"
            ]
        else:
            response_text = f"Thanks! I've captured that information for the {current_section.replace('_', ' ')} section.\n\nWhat would you like to work on next?"
            suggestions = [
                "What's the next section to complete?",
                "What else needs to be defined?",
                "Are there other requirements?"
            ]
    else:
        # Generic but helpful response
        if "complete" in message_lower or "missing" in message_lower or "what" in message_lower:
            completion_data = calculate_prd_completion(prd)
            if missing_sections:
                missing_list = ", ".join([s.replace("_", " ").replace(" (optional)", "") for s in missing_sections[:3]])
                response_text = f"I can see you're at {completion_data['completion_percentage']}% completion. The main sections still needed are: **{missing_list}**\n\nLet's start with the most important one. What would you like to focus on first?"
                suggestions = [
                    f"Work on {missing_sections[0].replace('_', ' ').replace(' (optional)', '')}",
                    "Tell me about the problem this solves",
                    "Who are the target users?",
                    "What are the main requirements?"
                ]
            else:
                response_text = "Great! Your PRD looks complete. Is there anything specific you'd like to refine or add?"
                suggestions = [
                    "Review the problem statement",
                    "Add more user stories",
                    "Refine the requirements",
                    "Update the timeline"
                ]
        else:
            response_text = f"I understand you're discussing: **{user_message}**\n\nLet me help you think through this. Can you provide more specific details about what you're trying to achieve?"
            suggestions = [
                "Can you provide more details?",
                "What's the main goal here?",
                "Who would benefit from this?",
                "What are the key requirements?"
            ]
    
    return {
        "response": response_text,
        "suggestions": suggestions,
        "updated_section": current_section,
        "completion_percentage": completion_data["completion_percentage"] if 'completion_data' in locals() else calculate_prd_completion(prd)["completion_percentage"]
    }

def generate_agent_creation_analysis(prd, missing_sections: list) -> dict:
    """Generate intelligent analysis for agent creation from the PRD"""
    
    # Analyze what's strong
    strong_sections = []
    if prd.problem_statement and len(prd.problem_statement.strip()) > 50:
        strong_sections.append("Problem Statement - Clear and specific")
    if prd.success_metrics and len(prd.success_metrics) > 0:
        strong_sections.append("Success Metrics - Measurable and actionable")
    if prd.user_stories and len(prd.user_stories) > 0:
        strong_sections.append("User Stories - Well-defined personas and use cases")
    if prd.requirements and len(prd.requirements) > 0:
        strong_sections.append("Requirements - Detailed and specific")
    if prd.technical_requirements and len(prd.technical_requirements) > 0:
        strong_sections.append("Technical Requirements - Detailed and specific")
    
    # Analyze what could be enhanced
    enhancement_areas = []
    if not prd.target_users or len(prd.target_users) == 0:
        enhancement_areas.append("Target Users - Could be more explicit about primary users")
    if not prd.acceptance_criteria or len(prd.acceptance_criteria) == 0:
        enhancement_areas.append("Acceptance Criteria - Could add specific testable criteria for each feature")
    if not prd.timeline or prd.timeline.strip() == "":
        enhancement_areas.append("Timeline - No specific dates or milestones mentioned")
    
    # Check for risk assessment
    has_risk_assessment = any(word in (prd.description or "").lower() for word in ["risk", "mitigation", "assumption", "constraint"])
    if not has_risk_assessment:
        enhancement_areas.append("Risk Assessment - What could go wrong and mitigation strategies")
    
    # Check for dependencies
    has_dependencies = any(word in (prd.technical_requirements or [] + [prd.description or ""]).lower() for word in ["dependency", "api", "integration", "access"])
    if not has_dependencies:
        enhancement_areas.append("Dependencies - API access, infrastructure requirements")
    
    # Build response
    response_text = "## **Agent Creation Analysis:**\n\n"
    
    if strong_sections:
        response_text += "**✅ Strong Sections:**\n"
        for section in strong_sections:
            response_text += f"- {section}\n"
        response_text += "\n"
    
    if enhancement_areas:
        response_text += "**🔍 Areas We Could Enhance:**\n"
        for area in enhancement_areas:
            response_text += f"- {area}\n"
        response_text += "\n"
    
    # Add agent creation recommendations
    response_text += "**🤖 Agent Creation Recommendations:**\n"
    
    if not prd.target_users or len(prd.target_users) == 0:
        response_text += "- **Define Primary Users**: Who are the main people who will use this agent? This helps determine the agent's personality and interaction style.\n"
    
    if not prd.acceptance_criteria or len(prd.acceptance_criteria) == 0:
        response_text += "- **Add Acceptance Criteria**: Define specific, testable criteria for agent behavior and performance.\n"
    
    if not prd.timeline or prd.timeline.strip() == "":
        response_text += "- **Set Timeline**: Add specific milestones for agent development and deployment.\n"
    
    if missing_sections:
        response_text += f"- **Complete Missing Sections**: Focus on {missing_sections[0].replace('_', ' ').replace(' (optional)', '')} first for better agent creation.\n"
    
    response_text += "\n**Ready to create your agent? Let's start the generation process!**"
    
    suggestions = []
    if not prd.target_users or len(prd.target_users) == 0:
        suggestions.append("Define the primary users for the agent")
    if not prd.acceptance_criteria or len(prd.acceptance_criteria) == 0:
        suggestions.append("Add agent behavior criteria")
    if not prd.timeline or prd.timeline.strip() == "":
        suggestions.append("Set agent development timeline")
    if missing_sections:
        suggestions.append(f"Complete {missing_sections[0].replace('_', ' ').replace(' (optional)', '')} for agent creation")
    
    # Add agent creation specific suggestions
    suggestions.extend([
        "Start agent generation process",
        "Review agent specifications",
        "Configure agent deployment settings"
    ])
    
    return {
        "response": response_text,
        "suggestions": suggestions,
        "updated_section": None,
        "completion_percentage": calculate_prd_completion(prd)["completion_percentage"]
    }
    
    # Generate contextual response
    if current_section and updated_content:
        # Update the PRD with new content
        if current_section == "problem_statement":
            prd.problem_statement = updated_content
        elif current_section == "target_users":
            prd.target_users = updated_content
        elif current_section == "requirements":
            prd.requirements = updated_content
        elif current_section == "success_metrics":
            prd.success_metrics = updated_content
        elif current_section == "timeline":
            prd.timeline = updated_content
        elif current_section == "user_stories":
            prd.user_stories = updated_content
        elif current_section == "acceptance_criteria":
            prd.acceptance_criteria = updated_content
        elif current_section == "technical_requirements":
            prd.technical_requirements = updated_content
        
        # Recalculate completion
        completion_data = calculate_prd_completion(prd)
        
        # Generate smart follow-up
        if current_section == "problem_statement":
            response_text = f"Perfect! I've captured your problem statement: **{user_message}**\n\nNow let's think about who this problem affects. Who are the main users or customers that experience this issue?"
            suggestions = [
                "Who are the primary users?",
                "What types of customers face this problem?",
                "Who would benefit from this solution?"
            ]
        elif current_section == "target_users":
            response_text = f"Great! I've noted your target users: **{user_message}**\n\nNow let's define what this agent needs to do. What are the main requirements or features it should have?"
            suggestions = [
                "What are the core features needed?",
                "What should the agent be able to do?",
                "What are the main requirements?"
            ]
        elif current_section == "requirements":
            response_text = f"Excellent! I've added that requirement: **{user_message}**\n\nNow let's think about how we'll know if this agent is successful. What metrics or outcomes would indicate success?"
            suggestions = [
                "How will we measure success?",
                "What are the key performance indicators?",
                "What outcomes indicate the agent is working?"
            ]
        elif current_section == "success_metrics":
            response_text = f"Perfect! I've captured your success metric: **{user_message}**\n\nNow let's think about the timeline. When do you need this agent to be ready?"
            suggestions = [
                "What's the target completion date?",
                "When do you need this deployed?",
                "What's the project timeline?"
            ]
        elif current_section == "timeline":
            response_text = f"Great! I've noted your timeline: **{user_message}**\n\nLet's think about the technical aspects. What technical requirements or constraints should we consider?"
            suggestions = [
                "What technical requirements are needed?",
                "Are there any system constraints?",
                "What APIs or integrations are required?"
            ]
        else:
            response_text = f"Thanks! I've captured that information for the {current_section.replace('_', ' ')} section.\n\nWhat would you like to work on next?"
            suggestions = [
                "What's the next section to complete?",
                "What else needs to be defined?",
                "Are there other requirements?"
            ]
    else:
        # Generic but helpful response
        if "complete" in message_lower or "missing" in message_lower or "what" in message_lower:
            if missing_sections:
                missing_list = ", ".join([s.replace("_", " ").replace(" (optional)", "") for s in missing_sections[:3]])
                response_text = f"I can see you're at {completion_data['completion_percentage']}% completion. The main sections still needed are: **{missing_list}**\n\nLet's start with the most important one. What would you like to focus on first?"
                suggestions = [
                    f"Work on {missing_sections[0].replace('_', ' ').replace(' (optional)', '')}",
                    "Tell me about the problem this solves",
                    "Who are the target users?",
                    "What are the main requirements?"
                ]
            else:
                response_text = "Great! Your PRD looks complete. Is there anything specific you'd like to refine or add?"
                suggestions = [
                    "Review the problem statement",
                    "Add more user stories",
                    "Refine the requirements",
                    "Update the timeline"
                ]
        else:
            response_text = f"I understand you're discussing: **{user_message}**\n\nLet me help you think through this. Can you provide more specific details about what you're trying to achieve?"
            suggestions = [
                "Can you provide more details?",
                "What's the main goal here?",
                "Who would benefit from this?",
                "What are the key requirements?"
            ]
    
    return {
        "response": response_text,
        "suggestions": suggestions,
        "updated_section": current_section,
        "completion_percentage": completion_data["completion_percentage"]
    }

# -----------------------------
# Interactive PRD completion
# -----------------------------

INTERACTIVE_REQUIRED_ORDER = [
    "title",
    "description",
    "problem_statement",
    "target_users",
    "user_stories",
    "requirements",
    "acceptance_criteria",
    "technical_requirements",
    "success_metrics",
    "timeline",
]

def _first_missing_required(prd: PRDResponse) -> Optional[str]:
    for section in INTERACTIVE_REQUIRED_ORDER:
        value = getattr(prd, section, None)
        if value is None or value == [] or value == {} or (isinstance(value, str) and not value.strip()):
            return section
    return None

@router.post("/prds/interactive", response_model=PRDResponse)
async def create_prd_interactive(payload: Dict[str, Optional[str]]):
    """Create a draft PRD for interactive completion (bypasses strict create)."""
    try:
        prd_id = str(uuid.uuid4())
        now = datetime.utcnow()
        title = (payload.get("title") or "Untitled PRD").strip() or "Untitled PRD"
        description = (payload.get("description") or "").strip()
        requirements = payload.get("requirements") or []
        if isinstance(requirements, str):
            requirements = [r.strip() for r in requirements.split("\n") if r.strip()]
        temp_create = PRDCreate(title=title, description=description or "", requirements=requirements or [])
        completion_data = calculate_prd_completion(temp_create)
        # Determine PRD type if provided; default to 'agent' for backwards compatibility
        prd_type = (payload.get("prd_type") or "agent")

        new_prd = PRDResponse(
            id=prd_id,
            title=title,
            description=description or "",
            requirements=requirements or [],
            voice_input=None,
            text_input=None,
            prd_type=prd_type,
            status="draft",
            github_repo_url=None,
            created_at=now,
            updated_at=now,
            completion_percentage=completion_data["completion_percentage"],
            missing_sections=completion_data["missing_sections"]
        )
        prds_db[prd_id] = new_prd
        return new_prd
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create interactive PRD: {str(e)}")

@router.get("/prds/{prd_id}/next-question")
async def get_next_question(prd_id: str):
    """Return the next missing section with a guided question prompt."""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    prd = prds_db[prd_id]
    # Determine next required missing section first
    next_required = _first_missing_required(prd)
    target_sections = [next_required] if next_required else []
    # If no required sections missing, include first optional missing (nice-to-have)
    if not target_sections and prd.missing_sections:
        # pick first optional if exists
        for s in prd.missing_sections:
            clean = s.replace(" (optional)", "")
            if clean not in INTERACTIVE_REQUIRED_ORDER:
                target_sections.append(clean)
                break
    if not target_sections:
        return {
            "done": True,
            "message": "PRD is complete",
            "completion_percentage": prd.completion_percentage,
            "missing_sections": prd.missing_sections or []
        }
    # Build question from templates
    questions = generate_guided_questions(prd)
    by_section = {q["section"]: q for q in questions}
    section = target_sections[0]
    q = by_section.get(section) or {
        "section": section,
        "question": f"Please provide content for '{section}'.",
        "sub_questions": [],
        "example": None
    }
    # Expected input type
    list_fields = {"target_users", "user_stories", "requirements", "acceptance_criteria", "technical_requirements", "security_requirements", "integration_requirements", "deployment_requirements", "success_metrics", "dependencies", "risks", "assumptions"}
    dict_fields = {"performance_requirements"}
    expected_type = "string"
    if section in list_fields:
        expected_type = "list"
    elif section in dict_fields:
        expected_type = "object"
    return {
        "done": False,
        "section": section,
        "prompt": q,
        "expected_type": expected_type
    }


@router.post("/prds/parse-completed-prd")
async def parse_completed_prd_endpoint(request: dict):
    """Parse completed PRD markdown and extract structured information for agent creation"""
    try:
        markdown_content = request.get("markdown_content", "")
        if not markdown_content.strip():
            raise HTTPException(status_code=400, detail="Markdown content is required")
        
        # Parse the completed PRD to extract structured information
        parsed_prd = parse_completed_prd(markdown_content)
        
        return {
            "success": True,
            "parsed_prd": parsed_prd,
            "message": "PRD parsed successfully and ready for agent creation"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse PRD: {str(e)}")

def parse_completed_prd(markdown_content: str) -> dict:
    """Parse completed PRD markdown and extract structured information for agent creation"""
    lines = markdown_content.split('\n')
    prd_data = {}
    
    # Enhanced parsing for completed PRDs with proper structure
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        
        # Look for section headers (## format)
        if line.startswith('##'):
            # Save previous section
            if current_section and current_content:
                _save_section_data(prd_data, current_section, current_content)
            
            # Start new section
            section_name = line.replace('##', '').strip().lower()
            current_section = _normalize_section_name(section_name)
            current_content = []
            
        elif line.startswith('#'):
            # Main title
            if not prd_data.get('title'):
                prd_data['title'] = line.replace('#', '').strip()
                
        elif line.startswith('-') or line.startswith('*'):
            # List item
            if current_section and current_content is not None:
                current_content.append(line[1:].strip())
                
        elif line and current_section and current_content is not None:
            # Regular content
            current_content.append(line)
    
    # Save last section
    if current_section and current_content:
        _save_section_data(prd_data, current_section, current_content)
    
    # Ensure required fields are present
    if 'title' not in prd_data:
        prd_data['title'] = 'AI Agent from Completed PRD'
    if 'description' not in prd_data:
        prd_data['description'] = 'Generated from completed PRD'
    if 'requirements' not in prd_data:
        prd_data['requirements'] = ['Requirements extracted from PRD']
    
    # Set PRD type based on content analysis
    prd_data['prd_type'] = _determine_prd_type(prd_data)
    
    return prd_data

def _normalize_section_name(section_name: str) -> str:
    """Normalize section names to match our data model"""
    section_mapping = {
        'problem statement': 'problem_statement',
        'target users': 'target_users',
        'user stories': 'user_stories',
        'requirements': 'requirements',
        'acceptance criteria': 'acceptance_criteria',
        'technical requirements': 'technical_requirements',
        'performance requirements': 'performance_requirements',
        'security requirements': 'security_requirements',
        'integration requirements': 'integration_requirements',
        'deployment requirements': 'deployment_requirements',
        'success metrics': 'success_metrics',
        'timeline': 'timeline',
        'dependencies': 'dependencies',
        'risks': 'risks',
        'assumptions': 'assumptions',
        'business value': 'business_value',
        'technical complexity': 'technical_complexity',
        'effort estimate': 'effort_estimate',
        'priority score': 'priority_score',
        'category': 'category',
        'assignee': 'assignee',
        'target sprint': 'target_sprint'
    }
    return section_mapping.get(section_name, section_name.replace(' ', '_'))

def _save_section_data(prd_data: dict, section: str, content: list):
    """Save section data in appropriate format"""
    if not content:
        return
        
    # List fields that should be arrays
    list_fields = {
        'target_users', 'user_stories', 'requirements', 'acceptance_criteria',
        'technical_requirements', 'security_requirements', 'integration_requirements',
        'deployment_requirements', 'success_metrics', 'dependencies', 'risks', 'assumptions'
    }
    
    if section in list_fields:
        prd_data[section] = content
    else:
        prd_data[section] = ' '.join(content)

def _determine_prd_type(prd_data: dict) -> str:
    """Determine if this is an agent or platform PRD based on content"""
    content = ' '.join(str(v) for v in prd_data.values()).lower()
    
    platform_keywords = ['platform', 'infrastructure', 'system', 'architecture', 'framework']
    if any(keyword in content for keyword in platform_keywords):
        return 'platform'
    return 'agent'

@router.post("/prds/{prd_id}/answer", response_model=PRDResponse)
async def submit_answer(prd_id: str, payload: Dict[str, Optional[object]]):
    """Submit answer for a section, update PRD, and return updated PRD."""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    prd = prds_db[prd_id]
    section = payload.get("section")
    value = payload.get("value")
    if not section:
        raise HTTPException(status_code=400, detail="Missing 'section' in payload")
    # Normalize simple conversions (split multiline string to list for list sections)
    list_fields = {"target_users", "user_stories", "requirements", "acceptance_criteria", "technical_requirements", "security_requirements", "integration_requirements", "deployment_requirements", "success_metrics", "dependencies", "risks", "assumptions"}
    if section in list_fields and isinstance(value, str):
        value = [item.strip() for item in value.split("\n") if item.strip()]
    # Set on PRD
    if not hasattr(prd, section):
        raise HTTPException(status_code=400, detail=f"Unknown section '{section}'")
    setattr(prd, section, value)
    # Recalculate completion
    temp_create = PRDCreate(
        title=prd.title,
        description=prd.description,
        requirements=prd.requirements,
        voice_input=prd.voice_input,
        text_input=prd.text_input,
        problem_statement=getattr(prd, "problem_statement", None),
        target_users=getattr(prd, "target_users", None),
        user_stories=getattr(prd, "user_stories", None),
        acceptance_criteria=getattr(prd, "acceptance_criteria", None),
        technical_requirements=getattr(prd, "technical_requirements", None),
        performance_requirements=getattr(prd, "performance_requirements", None),
        security_requirements=getattr(prd, "security_requirements", None),
        integration_requirements=getattr(prd, "integration_requirements", None),
        deployment_requirements=getattr(prd, "deployment_requirements", None),
        success_metrics=getattr(prd, "success_metrics", None),
        timeline=getattr(prd, "timeline", None),
        dependencies=getattr(prd, "dependencies", None),
        risks=getattr(prd, "risks", None),
        assumptions=getattr(prd, "assumptions", None)
    )
    completion = calculate_prd_completion(temp_create)
    prd.completion_percentage = completion["completion_percentage"]
    prd.missing_sections = completion["missing_sections"]
    # Auto-transition to submitted if complete
    if prd.completion_percentage == 100:
        prd.status = "submitted"
    prd.updated_at = datetime.utcnow()
    prds_db[prd_id] = prd
    return prd
