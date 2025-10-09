from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
import uuid
import os

router = APIRouter()

# Pydantic models
class PRDCreate(BaseModel):
    title: str
    description: str
    requirements: List[str]
    voice_input: Optional[str] = None
    text_input: Optional[str] = None
    
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

class PRDResponse(BaseModel):
    id: str
    title: str
    description: str
    requirements: List[str]
    voice_input: Optional[str]
    text_input: Optional[str]
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

class PRDUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    status: Optional[str] = None
    github_repo_url: Optional[str] = None

# In-memory storage for demo (replace with Supabase in production)
prds_db = {}

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
        
        new_prd = PRDResponse(
            id=prd_id,
            title=prd.title,
            description=prd.description,
            requirements=prd.requirements,
            voice_input=prd.voice_input,
            text_input=prd.text_input,
            status="draft" if completion_data["completion_percentage"] < 100 else "submitted",
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
            missing_sections=completion_data["missing_sections"]
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
    
    # Determine input source
    input_source = "Voice Input" if prd.voice_input else "Text Input"
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
    
    # Add original input
    markdown += f"""### 📝 **Original Input**
*This section contains the original voice or text input that generated this PRD*

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
- **Target Platform**: END_CAP Agent Factory
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
- Integrate with END_CAP platform APIs

#### **Phase 5: Integration**
- Register agent with END_CAP platform
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
- [ ] **Integration is complete** with END_CAP platform
- [ ] **Tests are passing** with comprehensive coverage
- [ ] **Documentation is complete** with usage examples
- [ ] **Monitoring is active** with proper logging and metrics

---

### 🔗 **Related Resources**

- **END_CAP Agent Factory**: https://github.com/thedoctorJJ/end-cap-agent-factory
- **MCP Server**: https://end-cap-mcp-server-http-fdqqqinvyq-uc.a.run.app
- **API Documentation**: http://localhost:8000/docs (when running locally)
- **Platform Dashboard**: http://localhost:3000 (when running locally)

---

### 📞 **Support & Questions**

For questions about this PRD or implementation:
- **Platform Issues**: Check END_CAP Agent Factory documentation
- **MCP Integration**: Refer to MCP server documentation
- **Deployment Issues**: Check Google Cloud Run logs
- **Database Issues**: Check Supabase dashboard

---

*This PRD was generated by the END_CAP Agent Factory platform and is ready for implementation by Devin AI.*
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
