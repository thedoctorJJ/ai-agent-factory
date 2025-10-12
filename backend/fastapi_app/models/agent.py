"""
Agent data models.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    """Agent status enumeration."""
    PENDING = "pending"
    DEPLOYED = "deployed"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"
    MAINTENANCE = "maintenance"


class AgentHealthStatus(str, Enum):
    """Agent health status enumeration."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    DEGRADED = "degraded"


class AgentRegistration(BaseModel):
    """Model for agent registration."""
    name: str = Field(..., min_length=1, max_length=100,
                      description="Agent name")
    description: str = Field(..., min_length=1,
                             description="Agent description")
    purpose: str = Field(..., min_length=1, description="Agent purpose")
    version: str = Field(..., description="Agent version")
    repository_url: str = Field(..., description="Repository URL")
    deployment_url: str = Field(..., description="Deployment URL")
    health_check_url: str = Field(..., description="Health check URL")
    prd_id: Optional[str] = Field(None, description="Associated PRD ID")
    devin_task_id: Optional[str] = Field(None, description="Devin task ID")
    capabilities: List[str] = Field(
        default_factory=list,
        description="Agent capabilities")
    configuration: Dict[str, Any] = Field(
        default_factory=dict, description="Agent configuration")

    @validator('capabilities')
    def validate_capabilities(cls, v):
        """Validate capabilities list."""
        if v is None:
            return []
        return [cap.strip() for cap in v if cap.strip()]

    @validator('name')
    def validate_name(cls, v):
        """Validate agent name."""
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        """Validate agent description."""
        return v.strip()

    @validator('purpose')
    def validate_purpose(cls, v):
        """Validate agent purpose."""
        return v.strip()


class AgentResponse(BaseModel):
    """Model for agent API responses."""
    id: str = Field(..., description="Agent ID")
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    purpose: str = Field(..., description="Agent purpose")
    version: str = Field(..., description="Agent version")
    tools: List[str] = Field(default_factory=list, description="Agent tools")
    prompts: List[str] = Field(
        default_factory=list,
        description="Agent prompts")
    status: AgentStatus = Field(..., description="Agent status")
    repository_url: Optional[str] = Field(None, description="Repository URL")
    deployment_url: Optional[str] = Field(None, description="Deployment URL")
    health_check_url: Optional[str] = Field(
        None, description="Health check URL")
    prd_id: Optional[str] = Field(None, description="Associated PRD ID")
    devin_task_id: Optional[str] = Field(None, description="Devin task ID")
    capabilities: List[str] = Field(
        default_factory=list,
        description="Agent capabilities")
    configuration: Dict[str, Any] = Field(
        default_factory=dict, description="Agent configuration")
    last_health_check: Optional[datetime] = Field(
        None, description="Last health check timestamp")
    health_status: AgentHealthStatus = Field(
        default=AgentHealthStatus.UNKNOWN,
        description="Health status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentListResponse(BaseModel):
    """Model for agent list API responses."""
    agents: List[AgentResponse] = Field(..., description="List of agents")
    total: int = Field(..., description="Total number of agents")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Whether there are more pages")


class AgentHealthResponse(BaseModel):
    """Model for agent health check responses."""
    agent_id: str = Field(..., description="Agent ID")
    agent_name: str = Field(..., description="Agent name")
    health_check_url: str = Field(..., description="Health check URL")
    last_checked: Optional[datetime] = Field(
        None, description="Last check timestamp")
    status: AgentHealthStatus = Field(..., description="Health status")
    details: Dict[str, Any] = Field(
        default_factory=dict, description="Health check details")
    response_time_ms: int = Field(
        default=0, description="Response time in milliseconds")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentMetricsResponse(BaseModel):
    """Model for agent metrics responses."""
    agent_id: str = Field(..., description="Agent ID")
    agent_name: str = Field(..., description="Agent name")
    status: AgentStatus = Field(..., description="Agent status")
    health_status: AgentHealthStatus = Field(..., description="Health status")
    last_health_check: Optional[datetime] = Field(
        None, description="Last health check")
    deployment_url: Optional[str] = Field(None, description="Deployment URL")
    repository_url: Optional[str] = Field(None, description="Repository URL")
    version: str = Field(..., description="Agent version")
    capabilities: List[str] = Field(
        default_factory=list,
        description="Agent capabilities")
    uptime_seconds: Optional[int] = Field(
        None, description="Uptime in seconds")
    request_count: Optional[int] = Field(
        None, description="Total request count")
    error_count: Optional[int] = Field(None, description="Total error count")
    avg_response_time_ms: Optional[float] = Field(
        None, description="Average response time")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
