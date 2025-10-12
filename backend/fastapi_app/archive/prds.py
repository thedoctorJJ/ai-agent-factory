from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
import uuid
import re

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
    # business_keywords = [
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
    # ]

    # Count keyword occurrences
    platform_score = sum(
        1 for keyword in platform_keywords if keyword in content_lower)
    agent_score = sum(
        1 for keyword in agent_keywords if keyword in content_lower)
    # business_score = sum(
    #     1 for keyword in business_keywords if keyword in content_lower)

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

    except Exception:
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

    try:
        # Simple markdown generation to avoid errors
        markdown = f"""# Product Requirements Document (PRD)
## {prd.title}

---

### 📋 **Document Information**
- **PRD ID**: `{prd.id}`
- **Status**: {prd.status.title()}
- **Type**: {prd.prd_type.title()}
- **Created**: {prd.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
- **Last Updated**: {prd.updated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}

---

### 🎯 **Project Overview**

**Description:**
{prd.description}

**Requirements:**
"""

        # Add requirements
        for i, requirement in enumerate(prd.requirements, 1):
            markdown += f"{i}. {requirement}\n"

        markdown += "\n---\n\n*Generated by AI Agent Factory*"

        return markdown

    except Exception as e:
        # Return a simple fallback markdown
        return f"""# {prd.title}

**Description:** {prd.description}

**Requirements:**
{chr(10).join(f"- {req}" for req in prd.requirements)}

*Error generating full markdown: {str(e)}*"""


# Roadmap-specific endpoints
@router.get("/roadmap/categories")
async def get_roadmap_categories():
    """Get all roadmap categories"""
    return roadmap_db["categories"]


@router.get("/roadmap/statuses")
async def get_roadmap_statuses():
    """Get all roadmap statuses"""
    return roadmap_db["statuses"]


@router.get("/roadmap/priorities")
async def get_roadmap_priorities():
    """Get all roadmap priorities"""
    return roadmap_db["priorities"]


@router.get("/roadmap")
async def get_roadmap():
    """Get the complete roadmap with all PRDs organized by category and status"""
    return {
        "categories": roadmap_db["categories"],
        "statuses": roadmap_db["statuses"],
        "priorities": roadmap_db["priorities"],
        "prds": prds_db
    }
