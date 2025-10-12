"""
Refactored Devin AI integration router with proper separation of concerns.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from ..models.devin import (
    DevinTaskCreate, DevinTaskResponse, DevinTaskStatus,
    DevinTaskListResponse, DevinTaskComplete, DevinTaskExecuteResponse
)
from ..services.devin_service import devin_service

router = APIRouter()


@router.post("/devin/tasks", response_model=DevinTaskResponse)
async def create_devin_task(task_data: DevinTaskCreate):
    """Create a new Devin AI task."""
    return await devin_service.create_task(task_data)


@router.get("/devin/tasks", response_model=DevinTaskListResponse)
async def get_devin_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of tasks to return"),
    status: Optional[DevinTaskStatus] = Query(None, description="Filter by task status"),
    prd_id: Optional[str] = Query(None, description="Filter by PRD ID")
):
    """Get a list of Devin tasks with optional filtering and pagination."""
    return await devin_service.get_tasks(skip=skip, limit=limit, status=status, prd_id=prd_id)


@router.get("/devin/tasks/{task_id}", response_model=DevinTaskResponse)
async def get_devin_task(task_id: str):
    """Get a specific Devin task by ID."""
    return await devin_service.get_task(task_id)


@router.post("/devin/tasks/{task_id}/execute", response_model=DevinTaskExecuteResponse)
async def execute_devin_task(task_id: str):
    """Execute a Devin task (submit to Devin AI)."""
    return await devin_service.execute_task(task_id)


@router.post("/devin/tasks/{task_id}/complete", response_model=DevinTaskResponse)
async def complete_devin_task(task_id: str, completion_data: DevinTaskComplete):
    """Mark a Devin task as completed."""
    return await devin_service.complete_task(task_id, completion_data)
