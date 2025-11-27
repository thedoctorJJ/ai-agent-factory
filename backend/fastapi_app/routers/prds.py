"""
Refactored PRD router with proper separation of concerns.
"""
from typing import List, Optional, Union, Dict
from fastapi import APIRouter, HTTPException, UploadFile, File, Query, Form, Body
from fastapi.responses import Response
from pydantic import BaseModel

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


@router.delete("/prds")
async def clear_all_prds():
    """Clear all PRDs from the system."""
    return await prd_service.clear_all_prds()


@router.post("/prds/upload", response_model=PRDResponse)
async def upload_prd_file(file: UploadFile = File(...)):
    """Upload a PRD file (.md or .txt)."""
    return await prd_service.upload_prd_file(file)


class IncomingPRDRequest(BaseModel):
    """Request model for incoming PRD submission."""
    content: str


class SavePRDRequest(BaseModel):
    """Minimal request model for ChatGPT Actions - simple PRD saving."""
    title: str
    content_markdown: str


@router.post("/prds/incoming", response_model=Dict[str, str])
async def submit_incoming_prd(request_body: IncomingPRDRequest):
    """
    Submit a PRD from an external source (AI tool, webhook, etc.).
    
    Directly creates PRD in database with content hash-based duplicate detection.
    
    Accepts JSON body with PRD content:
    ```json
    POST /api/v1/prds/incoming
    Content-Type: application/json
    {
        "content": "# PRD Title\n\n## Description\n..."
    }
    ```
    
    Returns:
    ```json
    {
        "status": "ok",
        "prd_id": "uuid",
        "title": "PRD Title",
        "message": "PRD created in database (with duplicate detection)"
    }
    ```
    """
    from io import BytesIO
    
    # Create a fake uploaded file object
    content_bytes = request_body.content.encode('utf-8')
    file_obj = BytesIO(content_bytes)
    
    class IncomingFile:
        def __init__(self, file_obj, filename):
            self.file = file_obj
            self.filename = filename
            self.headers = {}
        
        async def read(self):
            return self.file.read()
    
    # Use upload_prd_file which calls create_prd with hash-based duplicate detection
    upload_file = IncomingFile(file_obj, "incoming-prd.md")
    prd_response = await prd_service.upload_prd_file(upload_file)
    
    return {
        "status": "ok",
        "prd_id": prd_response.id,
        "title": prd_response.title,
        "message": "PRD created in database with content hash-based duplicate detection"
    }


@router.post("/prds/save", response_model=Dict[str, str])
async def save_prd(req: SavePRDRequest):
    """
    Minimal endpoint for ChatGPT Actions - saves PRD with simple title and markdown.
    This is the simplest possible endpoint for voice mode.
    
    Request:
    ```json
    {
      "title": "Some PRD Title",
      "content_markdown": "# PRD Title\n\nFull markdown content here..."
    }
    ```
    
    Response:
    ```json
    {
      "status": "ok",
      "file_name": "generated-filename.md",
      "prd_id": "uuid-here"
    }
    ```
    """
    from datetime import datetime
    import re
    from pathlib import Path
    
    # Generate filename from title
    def slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", "-", text)
        return text.strip("-") or "prd"
    
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    base = slugify(req.title)
    file_name = f"{base}-{ts}.md"
    
    # Save to incoming folder (for file-based workflow)
    project_root = Path(__file__).parent.parent.parent.parent
    incoming_folder = project_root / "prds" / "incoming"
    incoming_folder.mkdir(parents=True, exist_ok=True)
    
    file_path = incoming_folder / file_name
    file_path.write_text(req.content_markdown, encoding="utf-8")
    
    # Also submit to API for database storage
    try:
        from io import BytesIO
        
        content_bytes = req.content_markdown.encode('utf-8')
        file_obj = BytesIO(content_bytes)
        
        class IncomingFile:
            def __init__(self, file_obj, filename):
                self.file = file_obj
                self.filename = filename
                self.headers = {}
            
            async def read(self):
                return self.file.read()
        
        upload_file = IncomingFile(file_obj, file_name)
        prd_response = await prd_service.upload_prd_file(upload_file)
        
        return {
            "status": "ok",
            "file_name": file_name,
            "prd_id": prd_response.id,
            "title": prd_response.title
        }
    except Exception as e:
        # If API submission fails, still return success for file save
        return {
            "status": "ok",
            "file_name": file_name,
            "warning": f"File saved but API submission failed: {str(e)}"
        }


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
