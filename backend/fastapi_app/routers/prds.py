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


@router.post("/prds/submit", response_model=Dict[str, str])
async def submit_prd_to_github(request_body: IncomingPRDRequest):
    """
    Submit a PRD from ChatGPT - commits ONLY to GitHub (cloud source of truth).
    
    This is the preferred endpoint for ChatGPT Actions. It:
    1. Checks for duplicates in GitHub
    2. Commits PRD to GitHub ONLY (no database writes)
    3. GitHub Actions will sync to database automatically
    
    IMPORTANT: This endpoint does NOT write to the database. GitHub is the source of truth.
    All database updates happen via GitHub Actions after the file is committed.
    
    Accepts JSON body with PRD content:
    ```json
    POST /api/v1/prds/submit
    Content-Type: application/json
    {
        "content": "# PRD Title\n\n## Description\n..."
    }
    ```
    
    Returns:
    ```json
    {
        "status": "ok",
        "file_path": "prds/queue/2025-11-27_prd-title.md",
        "title": "PRD Title",
        "github_url": "https://github.com/...",
        "message": "PRD committed to GitHub (cloud source of truth)"
    }
    ```
    """
    from datetime import datetime
    import re
    import hashlib
    import base64
    import requests
    from ..config import config
    import os
    
    content = request_body.content
    
    # Extract title from content
    content_lines = content.split('\n')
    title = "untitled-prd"
    
    for line in content_lines:
        line = line.strip()
        if line.startswith('# '):
            title = line[2:].strip()
            # Strip markdown formatting
            title = re.sub(r'\*\*(.+?)\*\*', r'\1', title)
            title = re.sub(r'__(.+?)__', r'\1', title)
            title = re.sub(r'\*(.+?)\*', r'\1', title)
            title = re.sub(r'_(.+?)_', r'\1', title)
            title = re.sub(r'`(.+?)`', r'\1', title)
            break
    
    # Generate filename from title
    def slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", "-", text)
        return text.strip("-") or "prd"
    
    def normalize_text(text: str) -> str:
        """Normalize text for consistent hashing (matches backend logic)"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        text = re.sub(r'`(.+?)`', r'\1', text)
        return text.strip()
    
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    base = slugify(title)
    file_name = f"{date_str}_{base}.md"
    file_path = f"prds/queue/{file_name}"
    
    # Get GitHub credentials
    github_token = config.github_token or os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise HTTPException(
            status_code=500,
            detail="GitHub token not configured. Cannot commit PRD to GitHub."
        )
    
    repo_owner = os.getenv("GITHUB_ORG_NAME", "thedoctorJJ")
    repo_name = os.getenv("GITHUB_REPO_NAME", "ai-agent-factory")
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Step 1: Check for duplicates in GitHub
    try:
        # Get list of files in prds/queue/
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/prds/queue'
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            files = response.json()
            
            # Calculate hash of new content (title + first 500 chars of description)
            description = ""
            capture_desc = False
            for line in content_lines:
                if line.strip().startswith('## Description'):
                    capture_desc = True
                    continue
                if capture_desc and line.strip().startswith('##'):
                    break
                if capture_desc:
                    description += line + "\n"
            
            norm_title = normalize_text(title)
            norm_description = normalize_text(description)[:500]
            new_content_key = f"{norm_title}::{norm_description}"
            new_hash = hashlib.sha256(new_content_key.encode('utf-8')).hexdigest()
            
            # Check each existing PRD file
            for item in files:
                if isinstance(item, dict) and item.get("name", "").endswith(".md") and item.get("name") != "README.md":
                    # Get file content
                    file_content_url = item.get("download_url")
                    if file_content_url:
                        file_response = requests.get(file_content_url, timeout=10)
                        if file_response.status_code == 200:
                            existing_content = file_response.text
                            
                            # Extract title and description from existing file
                            existing_lines = existing_content.split('\n')
                            existing_title = ""
                            existing_description = ""
                            existing_capture_desc = False
                            
                            for line in existing_lines:
                                if line.strip().startswith('# '):
                                    existing_title = line[2:].strip()
                                if line.strip().startswith('## Description'):
                                    existing_capture_desc = True
                                    continue
                                if existing_capture_desc and line.strip().startswith('##'):
                                    break
                                if existing_capture_desc:
                                    existing_description += line + "\n"
                            
                            # Normalize and hash existing content
                            existing_norm_title = normalize_text(existing_title)
                            existing_norm_desc = normalize_text(existing_description)[:500]
                            existing_content_key = f"{existing_norm_title}::{existing_norm_desc}"
                            existing_hash = hashlib.sha256(existing_content_key.encode('utf-8')).hexdigest()
                            
                            # Check if content matches
                            if new_hash == existing_hash:
                                return {
                                    "status": "duplicate_prevented",
                                    "message": f"PRD with identical content already exists: {item.get('name')}",
                                    "existing_file": item.get("name"),
                                    "github_url": item.get("html_url", "")
                                }
    except Exception as e:
        # If duplicate check fails, log but continue (don't block PRD creation)
        print(f"⚠️  Warning: Duplicate check failed: {e}")
    
    # Step 2: Check if exact filename already exists
    check_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    check_response = requests.get(check_url, headers=headers, timeout=10)
    
    # If filename exists, add timestamp to make unique
    if check_response.status_code == 200:
        timestamp = datetime.utcnow().strftime("%H%M%S")
        file_name = f"{date_str}_{base}-{timestamp}.md"
        file_path = f"prds/queue/{file_name}"
    
    # Step 3: Commit PRD to GitHub
    commit_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    commit_data = {
        "message": f"Add PRD: {title} (from ChatGPT)",
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "branch": "main"
    }
    
    commit_response = requests.put(commit_url, headers=headers, json=commit_data, timeout=10)
    
    if commit_response.status_code not in [200, 201]:
        error_detail = commit_response.json().get("message", "Unknown error")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to commit PRD to GitHub: {error_detail}"
        )
    
    commit_result = commit_response.json()
    
    return {
        "status": "ok",
        "file_path": file_path,
        "title": title,
        "github_url": commit_result.get("content", {}).get("html_url", ""),
        "commit_sha": commit_result.get("commit", {}).get("sha", ""),
        "message": "PRD committed to GitHub (cloud source of truth). GitHub Actions will sync to database automatically."
    }


@router.post("/prds/incoming", response_model=Dict[str, str])
async def submit_incoming_prd(request_body: IncomingPRDRequest):
    """
    Submit a PRD from an external source (AI tool, webhook, etc.).
    
    Directly creates PRD in database with content hash-based duplicate detection.
    
    NOTE: For ChatGPT Actions, use /api/v1/prds/submit instead (commits to GitHub first).
    
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
