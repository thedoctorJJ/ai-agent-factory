"""
Refactored PRD router with proper separation of concerns.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import Response

from ..models.prd import (
    PRDCreate, PRDUpdate, PRDResponse, PRDType, PRDStatus,
    PRDListResponse, PRDMarkdownResponse
)
from ..services.prd_service import prd_service

router = APIRouter()


@router.post("/prds", response_model=PRDResponse)
async def create_prd(prd_data: PRDCreate):
    """Create a new PRD."""
    return await prd_service.create_prd(prd_data)


@router.get("/prds", response_model=PRDListResponse)
async def get_prds(
    skip: int = Query(0, ge=0, description="Number of PRDs to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of PRDs to return"),
    prd_type: Optional[PRDType] = Query(None, description="Filter by PRD type"),
    status: Optional[PRDStatus] = Query(None, description="Filter by PRD status")
):
    """Get a list of PRDs with optional filtering and pagination."""
    return await prd_service.get_prds(skip=skip, limit=limit, prd_type=prd_type, status=status)


# Devin AI workflow endpoints (must come before /prds/{prd_id} to avoid routing conflicts)
@router.get("/prds/ready-for-devin")
async def get_prds_ready_for_devin():
    """Get all PRDs that are ready for Devin AI processing."""
    from ..models.prd import PRDStatus
    
    prds_response = await prd_service.get_prds(status=PRDStatus.READY_FOR_DEVIN, limit=1000)
    
    return {
        "message": "PRDs ready for Devin AI",
        "count": prds_response.total,
        "prds": [prd.dict() for prd in prds_response.prds]
    }


@router.get("/prds/{prd_id}", response_model=PRDResponse)
async def get_prd(prd_id: str):
    """Get a specific PRD by ID."""
    return await prd_service.get_prd(prd_id)


@router.put("/prds/{prd_id}", response_model=PRDResponse)
async def update_prd(prd_id: str, prd_data: PRDUpdate):
    """Update an existing PRD."""
    return await prd_service.update_prd(prd_id, prd_data)


@router.delete("/prds/{prd_id}")
async def delete_prd(prd_id: str):
    """Delete a PRD."""
    return await prd_service.delete_prd(prd_id)


@router.post("/prds/upload", response_model=PRDResponse)
async def upload_prd_file(file: UploadFile = File(...)):
    """Upload a PRD file (.md or .txt)."""
    return await prd_service.upload_prd_file(file)


@router.get("/prds/{prd_id}/markdown", response_model=PRDMarkdownResponse)
async def get_prd_markdown(prd_id: str):
    """Get PRD as markdown for sharing with Devin AI."""
    return await prd_service.get_prd_markdown(prd_id)


@router.get("/prds/{prd_id}/markdown/download")
async def download_prd_markdown(prd_id: str):
    """Download PRD as markdown file."""
    markdown_response = await prd_service.get_prd_markdown(prd_id)
    
    return Response(
        content=markdown_response.markdown,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename={markdown_response.filename}"}
    )


# Roadmap-specific endpoints
@router.get("/roadmap/categories")
async def get_roadmap_categories():
    """Get all roadmap categories."""
    roadmap_data = prd_service.get_roadmap_data()
    return roadmap_data["categories"]


@router.get("/roadmap/statuses")
async def get_roadmap_statuses():
    """Get all roadmap statuses."""
    roadmap_data = prd_service.get_roadmap_data()
    return roadmap_data["statuses"]


@router.get("/roadmap/priorities")
async def get_roadmap_priorities():
    """Get all roadmap priorities."""
    roadmap_data = prd_service.get_roadmap_data()
    return roadmap_data["priorities"]


@router.get("/roadmap")
async def get_roadmap():
    """Get the complete roadmap with all PRDs organized by category and status."""
    roadmap_data = prd_service.get_roadmap_data()
    prds_response = await prd_service.get_prds(limit=1000)  # Get all PRDs
    
    return {
        "categories": roadmap_data["categories"],
        "statuses": roadmap_data["statuses"],
        "priorities": roadmap_data["priorities"],
        "prds": [prd.dict() for prd in prds_response.prds]
    }


# Devin AI workflow endpoints
@router.post("/prds/{prd_id}/ready-for-devin")
async def mark_prd_ready_for_devin(prd_id: str):
    """Mark a PRD as ready for Devin AI processing."""
    from ..models.prd import PRDUpdate, PRDStatus
    
    # Update PRD status to ready_for_devin
    prd_update = PRDUpdate(status=PRDStatus.READY_FOR_DEVIN)
    updated_prd = await prd_service.update_prd(prd_id, prd_update)
    
    return {
        "message": "PRD marked as ready for Devin AI",
        "prd_id": prd_id,
        "status": "ready_for_devin",
        "prd": updated_prd
    }
