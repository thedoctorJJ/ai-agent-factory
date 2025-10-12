"""
PRD (Product Requirements Document) data models.
"""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class PRDType(str, Enum):
    """PRD type enumeration."""
    PLATFORM = "platform"
    AGENT = "agent"


class PRDStatus(str, Enum):
    """PRD status enumeration."""
    QUEUE = "queue"
    PROCESSED = "processed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class PRDPriority(str, Enum):
    """PRD priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PRDEffort(str, Enum):
    """PRD effort estimation enumeration."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EPIC = "epic"


class PRDCreate(BaseModel):
    """Model for creating a new PRD."""
    title: str = Field(..., min_length=1, max_length=200,
                       description="PRD title")
    description: str = Field(..., min_length=1, description="PRD description")
    requirements: List[str] = Field(
        default_factory=list,
        description="List of requirements")
    prd_type: PRDType = Field(default=PRDType.AGENT, description="Type of PRD")

    # Enhanced PRD sections
    problem_statement: Optional[str] = Field(
        None, description="Problem statement")
    target_users: Optional[List[str]] = Field(None, description="Target users")
    user_stories: Optional[List[str]] = Field(None, description="User stories")
    acceptance_criteria: Optional[List[str]] = Field(
        None, description="Acceptance criteria")
    technical_requirements: Optional[List[str]] = Field(
        None, description="Technical requirements")
    performance_requirements: Optional[Dict[str, str]] = Field(
        None, description="Performance requirements")
    security_requirements: Optional[List[str]] = Field(
        None, description="Security requirements")
    integration_requirements: Optional[List[str]] = Field(
        None, description="Integration requirements")
    deployment_requirements: Optional[List[str]] = Field(
        None, description="Deployment requirements")
    success_metrics: Optional[List[str]] = Field(
        None, description="Success metrics")
    timeline: Optional[str] = Field(None, description="Timeline")
    dependencies: Optional[List[str]] = Field(None, description="Dependencies")
    risks: Optional[List[str]] = Field(None, description="Risks")
    assumptions: Optional[List[str]] = Field(None, description="Assumptions")

    # Roadmap-specific fields
    category: Optional[str] = Field(None, description="PRD category")
    priority: Optional[PRDPriority] = Field(None, description="PRD priority")
    effort_estimate: Optional[PRDEffort] = Field(
        None, description="Effort estimate")
    business_value: Optional[int] = Field(
        None, ge=1, le=10, description="Business value (1-10)")
    technical_complexity: Optional[int] = Field(
        None, ge=1, le=10, description="Technical complexity (1-10)")
    dependencies_list: Optional[List[str]] = Field(
        None, description="Dependencies list")
    assignee: Optional[str] = Field(None, description="Assignee")
    target_sprint: Optional[str] = Field(None, description="Target sprint")

    # File upload fields
    original_filename: Optional[str] = Field(
        None, description="Original filename")
    file_content: Optional[str] = Field(None, description="File content")

    @validator('requirements')
    def validate_requirements(cls, v):
        """Validate requirements list."""
        if v is None:
            return []
        return [req.strip() for req in v if req.strip()]

    @validator('title')
    def validate_title(cls, v):
        """Validate title."""
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        """Validate description."""
        return v.strip()


class PRDUpdate(BaseModel):
    """Model for updating an existing PRD."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    requirements: Optional[List[str]] = None
    prd_type: Optional[PRDType] = None
    status: Optional[PRDStatus] = None

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
    priority: Optional[PRDPriority] = None
    effort_estimate: Optional[PRDEffort] = None
    business_value: Optional[int] = Field(None, ge=1, le=10)
    technical_complexity: Optional[int] = Field(None, ge=1, le=10)
    dependencies_list: Optional[List[str]] = None
    assignee: Optional[str] = None
    target_sprint: Optional[str] = None


class PRDResponse(BaseModel):
    """Model for PRD API responses."""
    id: str = Field(..., description="PRD ID")
    title: str = Field(..., description="PRD title")
    description: str = Field(..., description="PRD description")
    requirements: List[str] = Field(..., description="List of requirements")
    prd_type: PRDType = Field(..., description="Type of PRD")
    status: PRDStatus = Field(..., description="PRD status")
    github_repo_url: Optional[str] = Field(
        None, description="GitHub repository URL")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

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
    priority: Optional[PRDPriority] = None
    effort_estimate: Optional[PRDEffort] = None
    business_value: Optional[int] = None
    technical_complexity: Optional[int] = None
    dependencies_list: Optional[List[str]] = None
    assignee: Optional[str] = None
    target_sprint: Optional[str] = None

    # File upload fields
    original_filename: Optional[str] = None
    file_content: Optional[str] = None

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PRDListResponse(BaseModel):
    """Model for PRD list API responses."""
    prds: List[PRDResponse] = Field(..., description="List of PRDs")
    total: int = Field(..., description="Total number of PRDs")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Whether there are more pages")


class PRDMarkdownResponse(BaseModel):
    """Model for PRD markdown export responses."""
    prd_id: str = Field(..., description="PRD ID")
    markdown: str = Field(..., description="Markdown content")
    filename: str = Field(..., description="Suggested filename")
