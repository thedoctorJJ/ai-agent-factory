"""
Devin AI integration data models.
"""
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class DevinTaskStatus(str, Enum):
    """Devin task status enumeration."""
    PENDING = "pending"
    IN_DEVIN = "in_devin"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DevinTaskCreate(BaseModel):
    """Model for creating a Devin task."""
    prd_id: str = Field(..., description="Associated PRD ID")
    title: str = Field(..., min_length=1, max_length=200,
                       description="Task title")
    description: str = Field(..., min_length=1, description="Task description")
    requirements: List[str] = Field(
        default_factory=list,
        description="Task requirements")

    @validator('requirements')
    def validate_requirements(cls, v):
        """Validate requirements list."""
        if v is None:
            return []
        return [req.strip() for req in v if req.strip()]

    @validator('title')
    def validate_title(cls, v):
        """Validate task title."""
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        """Validate task description."""
        return v.strip()


class DevinTaskResponse(BaseModel):
    """Model for Devin task API responses."""
    id: str = Field(..., description="Task ID")
    prd_id: str = Field(..., description="Associated PRD ID")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    requirements: List[str] = Field(..., description="Task requirements")
    devin_prompt: str = Field(..., description="Generated Devin prompt")
    status: DevinTaskStatus = Field(..., description="Task status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    devin_output: Optional[str] = Field(None, description="Devin AI output")
    agent_code: Optional[str] = Field(None, description="Generated agent code")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DevinTaskListResponse(BaseModel):
    """Model for Devin task list API responses."""
    tasks: List[DevinTaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Whether there are more pages")


class DevinTaskComplete(BaseModel):
    """Model for completing a Devin task."""
    agent_code: Optional[str] = Field(None, description="Generated agent code")
    deployment_method: str = Field(
        default="mcp_automatic",
        description="Deployment method")
    devin_output: Optional[str] = Field(None, description="Devin AI output")
    error_message: Optional[str] = Field(
        None, description="Error message if failed")

    @validator('deployment_method')
    def validate_deployment_method(cls, v):
        """Validate deployment method."""
        allowed_methods = ["mcp_automatic", "manual", "api"]
        if v not in allowed_methods:
            raise ValueError(
                f"Deployment method must be one of: {allowed_methods}")
        return v


class DevinTaskExecuteResponse(BaseModel):
    """Model for Devin task execution responses."""
    message: str = Field(..., description="Execution message")
    task_id: str = Field(..., description="Task ID")
    status: DevinTaskStatus = Field(..., description="Task status")
    note: Optional[str] = Field(None, description="Additional notes")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
