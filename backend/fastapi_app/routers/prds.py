from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
import re
from ..config import config

router = APIRouter()

# Pydantic models


class PRDCreate(BaseModel):
    title: str
    description: str
    requirements: List[str]
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

    # Roadmap-specific fields
    category: Optional[str] = None
    priority_score: Optional[int] = None
    effort_estimate: Optional[str] = None
    business_value: Optional[int] = None
    technical_complexity: Optional[int] = None
    dependencies_list: Optional[List[str]] = None
    assignee: Optional[str] = None
    target_sprint: Optional[str] = None

    # File upload fields
    original_filename: Optional[str] = None
    file_content: Optional[str] = None


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


@router.get("/prds", response_model=List[PRDResponse])
async def get_prds():
    """Get all PRDs"""
    try:
        return list(prds_db.values())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve PRDs: {
                str(e)}")


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

        new_prd = PRDResponse(
            id=prd_id,
            title=prd.title,
            description=prd.description,
            requirements=prd.requirements,
            prd_type=(prd.prd_type or "agent"),
            status="queue",
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
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create PRD: {
                str(e)}")


@router.post("/prds/upload", response_model=PRDResponse)
async def upload_prd_file(file: UploadFile = File(...)):
    """Upload a PRD file and automatically parse its content"""

    # Validate file type
    if not file.filename.lower().endswith(('.md', '.txt')):
        raise HTTPException(status_code=400,
                            detail="Only .md and .txt files are supported")

    try:
        # Read file content
        content = await file.read()

        # Decode content
        text_content = content.decode('utf-8')

        # Parse the content
        parsed_data = parse_prd_content(text_content)

        # Create PRD from parsed data
        prd_id = str(uuid.uuid4())
        now = datetime.utcnow()

        new_prd = PRDResponse(
            id=prd_id,
            title=parsed_data["title"] or file.filename.replace(
                '.md', '').replace('.txt', ''),
            description=parsed_data["description"],
            requirements=parsed_data["requirements"],
            prd_type=parsed_data["prd_type"],
            status="queue",
            github_repo_url=None,
            created_at=now,
            updated_at=now,

            # Enhanced PRD sections
            problem_statement=parsed_data["problem_statement"],
            target_users=parsed_data["target_users"],
            user_stories=parsed_data["user_stories"],
            acceptance_criteria=parsed_data["acceptance_criteria"],
            technical_requirements=parsed_data["technical_requirements"],
            performance_requirements=parsed_data["performance_requirements"],
            security_requirements=parsed_data["security_requirements"],
            integration_requirements=parsed_data["integration_requirements"],
            deployment_requirements=parsed_data["deployment_requirements"],
            success_metrics=parsed_data["success_metrics"],
            timeline=parsed_data["timeline"],
            dependencies=parsed_data["dependencies"],
            risks=parsed_data["risks"],
            assumptions=parsed_data["assumptions"],

            # Roadmap-specific fields with defaults
            category="core_functionality",
            priority_score=5,
            effort_estimate="medium",
            business_value=5,
            technical_complexity=5,
            dependencies_list=[],
            assignee="System",
            target_sprint="Sprint 1",

            # Store original file info
            original_filename=file.filename,
            file_content=text_content
        )

        prds_db[prd_id] = new_prd

        return new_prd

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File encoding not supported. Please use UTF-8 encoded files.")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {
                str(e)}")


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


def detect_prd_type(content: str) -> str:
    """Detect if PRD is for platform or agent based on content analysis"""
    content_lower = content.lower()

    # Platform indicators (higher weight)
    platform_keywords = [
        'platform', 'infrastructure', 'architecture', 'system', 'framework',
        'api', 'backend', 'frontend', 'database', 'deployment', 'scaling',
        'microservices', 'kubernetes', 'docker', 'cloud', 'aws', 'azure',
        'google cloud', 'monitoring', 'logging', 'security', 'authentication',
        'authorization', 'middleware', 'service mesh', 'load balancing',
        'ci/cd', 'devops', 'container', 'orchestration', 'networking',
        'storage', 'caching', 'message queue', 'event streaming'
    ]

    # Agent indicators (higher weight)
    agent_keywords = [
        'agent',
        'bot',
        'chatbot',
        'assistant',
        'ai assistant',
        'conversational',
        'nlp',
        'natural language',
        'voice',
        'speech',
        'text processing',
        'machine learning',
        'ml model',
        'training',
        'inference',
        'prediction',
        'classification',
        'recommendation',
        'personalization',
        'automation',
        'workflow',
        'task',
        'action',
        'decision',
        'reasoning',
        'knowledge',
        'intelligence',
        'cognitive',
        'neural',
        'deep learning',
        'llm',
        'language model',
        'gpt',
        'openai',
        'anthropic',
        'claude']

    # Business/domain indicators (medium weight)
    business_keywords = [
        'customer',
        'user',
        'client',
        'business',
        'service',
        'product',
        'application',
        'software',
        'tool',
        'utility',
        'feature',
        'functionality']

    # Count keyword occurrences
    platform_score = sum(
        1 for keyword in platform_keywords if keyword in content_lower)
    agent_score = sum(
        1 for keyword in agent_keywords if keyword in content_lower)
    business_score = sum(
        1 for keyword in business_keywords if keyword in content_lower)

    # Additional heuristics
    # Check for specific patterns
    if any(pattern in content_lower for pattern in [
        'prd type', 'platform prd', 'agent prd', 'type:', 'category:'
    ]):
        if 'platform' in content_lower and 'agent' not in content_lower:
            return 'platform'
        elif 'agent' in content_lower and 'platform' not in content_lower:
            return 'agent'

    # Check title and description for clues
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).lower()
        if any(
            keyword in title for keyword in [
                'platform',
                'system',
                'infrastructure',
                'framework']):
            platform_score += 3
        elif any(keyword in title for keyword in ['agent', 'bot', 'assistant', 'ai']):
            agent_score += 3

    # Check requirements for technical vs business focus
    requirements_match = re.search(
        r'(?i)requirements?[:\s]*\n((?:[-*]\s*.+\n?)+)',
        content,
        re.MULTILINE)
    if requirements_match:
        requirements_text = requirements_match.group(1).lower()
        if any(keyword in requirements_text for keyword in [
            'api', 'database', 'deployment', 'scaling', 'infrastructure'
        ]):
            platform_score += 2
        elif any(keyword in requirements_text for keyword in [
            'nlp', 'ml', 'training', 'model', 'intelligence'
        ]):
            agent_score += 2

    # Decision logic
    if platform_score > agent_score:
        return 'platform'
    elif agent_score > platform_score:
        return 'agent'
    else:
        # Default to agent if scores are equal or very low
        return 'agent'


def parse_prd_content(content: str) -> Dict:
    """Parse PRD content from uploaded file and extract structured data"""
    try:
        # Initialize the parsed data structure
        parsed_data = {
            "title": "",
            "description": "",
            "requirements": [],
            "problem_statement": "",
            "target_users": [],
            "user_stories": [],
            "acceptance_criteria": [],
            "technical_requirements": [],
            "performance_requirements": {},
            "security_requirements": [],
            "integration_requirements": [],
            "deployment_requirements": [],
            "success_metrics": [],
            "timeline": "",
            "dependencies": [],
            "risks": [],
            "assumptions": [],
            "prd_type": "agent"
        }

        # Extract title (look for # Title or similar patterns)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            parsed_data["title"] = title_match.group(1).strip()

        # Extract description (look for description section)
        desc_match = re.search(
            r'(?i)description[:\s]*\n(.+?)(?=\n\n|\n#|\n##|\n###|\Z)',
            content,
            re.DOTALL)
        if desc_match:
            parsed_data["description"] = desc_match.group(1).strip()

        # Extract problem statement
        problem_match = re.search(
            r'(?i)problem\s+statement[:\s]*\n(.+?)(?=\n\n|\n#|\n##|\n###|\Z)',
            content,
            re.DOTALL)
        if problem_match:
            parsed_data["problem_statement"] = problem_match.group(1).strip()

        # Extract requirements (look for bullet points or numbered lists)
        requirements_match = re.search(
            r'(?i)requirements?[:\s]*\n((?:[-*]\s*.+\n?)+)',
            content,
            re.MULTILINE)
        if requirements_match:
            requirements_text = requirements_match.group(1)
            parsed_data["requirements"] = [line.strip(
                '- *').strip() for line in requirements_text.split('\n') if line.strip()]

        # Extract user stories
        stories_match = re.search(
            r'(?i)user\s+stories?[:\s]*\n((?:[-*]\s*.+\n?)+)',
            content,
            re.MULTILINE)
        if stories_match:
            stories_text = stories_match.group(1)
            parsed_data["user_stories"] = [
                line.strip('- *').strip() for line in stories_text.split('\n') if line.strip()]

        # Extract acceptance criteria
        criteria_match = re.search(
            r'(?i)acceptance\s+criteria[:\s]*\n((?:[-*]\s*.+\n?)+)',
            content,
            re.MULTILINE)
        if criteria_match:
            criteria_text = criteria_match.group(1)
            parsed_data["acceptance_criteria"] = [
                line.strip('- *').strip() for line in criteria_text.split('\n') if line.strip()]

        # Extract technical requirements
        tech_match = re.search(
            r'(?i)technical\s+requirements?[:\s]*\n((?:[-*]\s*.+\n?)+)',
            content,
            re.MULTILINE)
        if tech_match:
            tech_text = tech_match.group(1)
            parsed_data["technical_requirements"] = [
                line.strip('- *').strip() for line in tech_text.split('\n') if line.strip()]

        # Extract target users
        users_match = re.search(
            r'(?i)target\s+users?[:\s]*\n(.+?)(?=\n\n|\n#|\n##|\n###|\Z)',
            content,
            re.DOTALL)
        if users_match:
            users_text = users_match.group(1).strip()
            parsed_data["target_users"] = [user.strip()
                                           for user in users_text.split(',') if user.strip()]

        # Extract timeline
        timeline_match = re.search(
            r'(?i)timeline[:\s]*\n(.+?)(?=\n\n|\n#|\n##|\n###|\Z)',
            content,
            re.DOTALL)
        if timeline_match:
            parsed_data["timeline"] = timeline_match.group(1).strip()

        # Determine PRD type based on content analysis
        parsed_data["prd_type"] = detect_prd_type(content)

        # If no title found, try to extract from filename or first line
        if not parsed_data["title"]:
            first_line = content.split('\n')[0].strip()
            if first_line and not first_line.startswith('#'):
                parsed_data["title"] = first_line[:100]  # Limit title length

        return parsed_data

    except Exception as e:
        # Return basic structure if parsing fails
        return {
            "title": "Uploaded PRD",
            "description": content[:500] + "..." if len(content) > 500 else content,
            "requirements": [],
            "problem_statement": "",
            "target_users": [],
            "user_stories": [],
            "acceptance_criteria": [],
            "technical_requirements": [],
            "performance_requirements": {},
            "security_requirements": [],
            "integration_requirements": [],
            "deployment_requirements": [],
            "success_metrics": [],
            "timeline": "",
            "dependencies": [],
            "risks": [],
            "assumptions": [],
            "prd_type": "agent"
        }


def generate_prd_markdown(prd: PRDResponse) -> str:
    """Generate standardized markdown PRD for Devin AI"""

    # Determine input source (legacy field - now all PRDs are completed and
    # formatted)
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
        priority_prds = [prd for prd in prds if hasattr(
            prd, 'priority_score') and prd.priority_score]
        if priority_prds:
            avg_priority = sum(
                prd.priority_score for prd in priority_prds) / len(priority_prds)
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
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get roadmap overview: {
                str(e)}")


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
            prds = [
                prd for prd in prds if getattr(
                    prd,
                    'category',
                    None) == category]

        if status:
            prds = [
                prd for prd in prds if getattr(
                    prd,
                    'status',
                    'backlog') == status]

        if effort:
            prds = [
                prd for prd in prds if getattr(
                    prd,
                    'effort_estimate',
                    None) == effort]

        if prd_type:
            prds = [
                prd for prd in prds if getattr(
                    prd,
                    'prd_type',
                    'agent') == prd_type]

        # Apply sorting
        if sort_by == "priority_score":
            prds.sort(
                key=lambda x: getattr(
                    x, 'priority_score', 0), reverse=(
                    sort_order == "desc"))
        elif sort_by == "created_at":
            prds.sort(
                key=lambda x: x.created_at,
                reverse=(
                    sort_order == "desc"))
        elif sort_by == "title":
            prds.sort(key=lambda x: x.title, reverse=(sort_order == "desc"))

        return prds
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get roadmap PRDs: {
                str(e)}")


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
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get prioritization matrix: {
                str(e)}")
