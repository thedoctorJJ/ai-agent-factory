"""
PRD service for business logic operations.
"""
import uuid
import re
from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException, UploadFile

from ..models.prd import (
    PRDCreate, PRDUpdate, PRDResponse, PRDType, PRDStatus,
    PRDListResponse, PRDMarkdownResponse
)
from ..utils.simple_data_manager import data_manager
from ..utils.prd_hash import calculate_prd_hash
from .prd_parser import PRDParser


class PRDService:
    """Service class for PRD operations."""

    def __init__(self):
        """Initialize the PRD service."""
        self._roadmap_db = {
            "categories": ["infrastructure", "features", "improvements", "bugfixes"],
            "statuses": ["backlog", "planned", "in_progress", "review", "completed"],
            "priorities": ["low", "medium", "high", "critical"]
        }
        self.parser = PRDParser()

    async def create_prd(self, prd_data: PRDCreate) -> PRDResponse:
        """Create a new PRD with content hash-based duplicate detection."""
        # Calculate content hash for duplicate detection
        content_hash = calculate_prd_hash(prd_data.title, prd_data.description)
        print(f"🔍 Creating PRD: '{prd_data.title}'")
        print(f"   Content hash: {content_hash[:16]}...")
        
        # Check for duplicate by content hash (deterministic, reliable)
        print(f"   Checking for duplicates in database...")
        existing_prd = await data_manager.get_prd_by_hash(content_hash)
        
        if existing_prd:
            print(f"⚠️  DUPLICATE DETECTED! PRD with same content already exists")
            print(f"   Existing ID: {existing_prd.get('id')}")
            print(f"   Title: '{prd_data.title}'")
            print(f"   Hash: {content_hash[:16]}...")
            print(f"   ✅ Returning existing PRD (no duplicate created)")
            # Return existing PRD instead of creating duplicate
            # CRITICAL: Must return here to prevent duplicate creation
            try:
                if isinstance(existing_prd.get("created_at"), str):
                    existing_prd["created_at"] = datetime.fromisoformat(existing_prd["created_at"].replace('Z', '+00:00'))
                if isinstance(existing_prd.get("updated_at"), str):
                    existing_prd["updated_at"] = datetime.fromisoformat(existing_prd["updated_at"].replace('Z', '+00:00'))
                return PRDResponse(**existing_prd)
            except Exception as e:
                # If datetime parsing fails, still return the existing PRD
                # Use current time as fallback for datetime fields
                print(f"   ⚠️  Warning: Datetime parsing failed, using fallback: {e}")
                if "created_at" not in existing_prd or not isinstance(existing_prd.get("created_at"), datetime):
                    existing_prd["created_at"] = datetime.utcnow()
                if "updated_at" not in existing_prd or not isinstance(existing_prd.get("updated_at"), datetime):
                    existing_prd["updated_at"] = datetime.utcnow()
                return PRDResponse(**existing_prd)
        
        print(f"   ✅ No duplicate found - creating new PRD")
        
        prd_id = str(uuid.uuid4())
        now = datetime.utcnow()

        prd_dict = {
            "id": prd_id,
            "title": prd_data.title,
            "description": prd_data.description,
            "requirements": prd_data.requirements,
            "prd_type": prd_data.prd_type.value,
            "status": PRDStatus.QUEUE.value,  # Use 'queue' instead of 'uploaded' (not in DB enum)
            "github_repo_url": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "content_hash": content_hash,  # Add content hash for duplicate detection
            "problem_statement": prd_data.problem_statement,
            "target_users": prd_data.target_users,
            "user_stories": prd_data.user_stories,
            "acceptance_criteria": prd_data.acceptance_criteria,
            "technical_requirements": prd_data.technical_requirements,
            "performance_requirements": prd_data.performance_requirements,
            "security_requirements": prd_data.security_requirements,
            "integration_requirements": prd_data.integration_requirements,
            "deployment_requirements": prd_data.deployment_requirements,
            "success_metrics": prd_data.success_metrics,
            "timeline": prd_data.timeline,
            "dependencies": prd_data.dependencies,
            "risks": prd_data.risks,
            "assumptions": prd_data.assumptions,
            "category": prd_data.category,
            "priority": prd_data.priority.value if prd_data.priority else None,
            "effort_estimate": prd_data.effort_estimate.value if prd_data.effort_estimate else None,
            "business_value": prd_data.business_value,
            "technical_complexity": prd_data.technical_complexity,
            "dependencies_list": prd_data.dependencies_list,
            "assignee": prd_data.assignee,
            "target_sprint": prd_data.target_sprint,
            "original_filename": prd_data.original_filename,
            "file_content": prd_data.file_content}

        # Try to save to database (will fallback to local database if Supabase fails)
        try:
            saved_prd = await data_manager.create_prd(prd_dict)
            if saved_prd:
                # Convert datetime strings back to datetime objects for response
                saved_prd["created_at"] = datetime.fromisoformat(saved_prd["created_at"].replace('Z', '+00:00'))
                saved_prd["updated_at"] = datetime.fromisoformat(saved_prd["updated_at"].replace('Z', '+00:00'))
                return PRDResponse(**saved_prd)
        except Exception as e:
            print(f"Database save failed, using in-memory storage: {e}")
        
        # Fallback to in-memory storage
        if not hasattr(self, '_prds_db'):
            self._prds_db: Dict[str, Dict[str, Any]] = {}
        self._prds_db[prd_id] = prd_dict
        return PRDResponse(**prd_dict)

    async def get_prd(self, prd_id: str) -> PRDResponse:
        """Get a PRD by ID."""
        # Try to get from database first
        try:
            if data_manager.is_connected():
                prd_data = await data_manager.get_prd(prd_id)
                if prd_data:
                    # Convert datetime strings back to datetime objects
                    prd_data["created_at"] = datetime.fromisoformat(prd_data["created_at"].replace('Z', '+00:00'))
                    prd_data["updated_at"] = datetime.fromisoformat(prd_data["updated_at"].replace('Z', '+00:00'))
                    return PRDResponse(**prd_data)
        except Exception as e:
            print(f"Database get failed, trying in-memory storage: {e}")
        
        # Fallback to in-memory storage
        if not hasattr(self, '_prds_db'):
            self._prds_db: Dict[str, Dict[str, Any]] = {}
        if prd_id not in self._prds_db:
            raise HTTPException(status_code=404, detail="PRD not found")

        return PRDResponse(**self._prds_db[prd_id])

    async def get_prds(
        self,
        skip: int = 0,
        limit: int = 100,
        prd_type: Optional[PRDType] = None,
        status: Optional[PRDStatus] = None
    ) -> PRDListResponse:
        """Get a list of PRDs with optional filtering."""
        # Try to get from database first (will fallback to local database if Supabase fails)
        try:
            # Pass status parameter to database manager for efficient filtering
            status_value = status.value if status else None
            prds_data = await data_manager.get_prds(skip, limit)
            if prds_data:
                # Convert datetime strings back to datetime objects
                for prd in prds_data:
                    prd["created_at"] = datetime.fromisoformat(prd["created_at"].replace('Z', '+00:00'))
                    prd["updated_at"] = datetime.fromisoformat(prd["updated_at"].replace('Z', '+00:00'))
                
                # Apply remaining filters (prd_type filtering still done in memory)
                filtered_prds = prds_data
                if prd_type:
                    filtered_prds = [p for p in filtered_prds if p["prd_type"] == prd_type.value]
                
                return PRDListResponse(
                    prds=[PRDResponse(**prd) for prd in filtered_prds],
                    total=len(filtered_prds),
                    page=skip // limit + 1,
                    size=limit,
                    has_next=len(filtered_prds) == limit
                )
        except Exception as e:
            print(f"Database get_prds failed, using in-memory storage: {e}")
        
        # Fallback to in-memory storage
        if not hasattr(self, '_prds_db'):
            self._prds_db: Dict[str, Dict[str, Any]] = {}
        prds = list(self._prds_db.values())

        # Apply filters
        if prd_type:
            prds = [p for p in prds if p["prd_type"] == prd_type.value]
        if status:
            prds = [p for p in prds if p["status"] == status.value]

        # Sort by created_at descending
        prds.sort(key=lambda x: x["created_at"], reverse=True)

        # Apply pagination
        total = len(prds)
        prds = prds[skip:skip + limit]

        return PRDListResponse(
            prds=[PRDResponse(**prd) for prd in prds],
            total=total,
            page=skip // limit + 1,
            size=limit,
            has_next=skip + limit < total
        )

    async def update_prd(
            self,
            prd_id: str,
            prd_data: PRDUpdate) -> PRDResponse:
        """Update an existing PRD."""
        # Try to update in database first
        try:
            if data_manager.is_connected():
                update_data = prd_data.dict(exclude_unset=True)
                updated_prd = await data_manager.update_prd(prd_id, update_data)
                if updated_prd:
                    return PRDResponse(**updated_prd)
        except Exception as e:
            print(f"Database update failed, trying in-memory storage: {e}")

        # Fallback to in-memory storage
        if prd_id not in self._prds_db:
            raise HTTPException(status_code=404, detail="PRD not found")

        prd_dict = self._prds_db[prd_id]

        # Update fields that are provided
        update_data = prd_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(prd_dict, field):
                prd_dict[field] = value

        prd_dict["updated_at"] = datetime.utcnow()

        return PRDResponse(**prd_dict)

    async def delete_prd(self, prd_id: str, database_only: bool = False) -> Dict[str, str]:
        """Delete a PRD.
        
        Args:
            prd_id: The PRD ID to delete
            database_only: If True, only delete from database (for reconciliation).
                          If False, delete from GitHub (hard delete - overrides source of truth).
        
        When database_only=False (hard delete button):
        1. Delete from GitHub ONLY (hard delete overrides GitHub as source of truth)
        2. Do NOT delete from database
        3. GitHub Actions reconciliation will automatically delete from database within 30 seconds
        4. This is the ONLY way to delete from GitHub (the override)
        
        When database_only=True (reconciliation script):
        1. Delete from database only
        2. Used when PRD exists in database but not in GitHub (orphaned PRD)
        """
        # Log the delete operation for debugging
        print(f"🗑️  DELETE PRD: prd_id={prd_id}, database_only={database_only} (type: {type(database_only).__name__})")
        
        if database_only:
            # Delete from database only (for reconciliation script)
            try:
                if data_manager.is_connected():
                    success = await data_manager.delete_prd(prd_id)
                    if not success:
                        raise HTTPException(status_code=404, detail="PRD not found")
                else:
                    # Fallback to in-memory storage
                    if not hasattr(self, '_prds_db'):
                        self._prds_db: Dict[str, Dict[str, Any]] = {}
                    if prd_id not in self._prds_db:
                        raise HTTPException(status_code=404, detail="PRD not found")
                    del self._prds_db[prd_id]
                
                return {"message": "PRD deleted from database only (orphaned PRD cleanup)"}
            except HTTPException:
                raise
            except Exception as e:
                print(f"Database delete failed: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to delete PRD: {str(e)}")
        else:
            # Hard delete: Delete from GitHub ONLY (overrides GitHub as source of truth)
            # IMPORTANT: Do NOT delete from database - GitHub Actions will sync database automatically
            print(f"🔴 HARD DELETE: Deleting PRD {prd_id} from GitHub ONLY (NOT from database)")
            
            # Step 1: Get PRD details before deletion (need filename for GitHub)
            prd_data = None
            try:
                if data_manager.is_connected():
                    prd_data = await data_manager.get_prd(prd_id)
                    print(f"✅ Fetched PRD data: {prd_data.get('title', 'N/A') if prd_data else 'None'}")
            except Exception as e:
                print(f"❌ Error fetching PRD before delete: {e}")
            
            if not prd_data:
                print(f"❌ PRD not found in database: {prd_id}")
                raise HTTPException(status_code=404, detail="PRD not found")
            
            # Step 2: Delete from GitHub (hard delete - the ONLY override to GitHub source of truth)
            # Do NOT delete from database - GitHub Actions will sync database automatically
            print(f"🔄 Attempting to delete PRD from GitHub...")
            github_deleted = await self._delete_prd_from_github(prd_data)
            
            if not github_deleted:
                print(f"❌ GitHub deletion failed for PRD {prd_id}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to delete PRD from GitHub. Please check GitHub token and permissions."
                )
            
            print(f"✅ Successfully deleted PRD {prd_id} from GitHub. Database will be synced by GitHub Actions.")
            return {
                "message": "PRD deleted from GitHub (hard delete - source of truth override). Database will be synced automatically via GitHub Actions within 30 seconds."
            }
    
    async def _delete_prd_from_github(self, prd_data: Dict[str, Any]) -> bool:
        """Delete PRD file from GitHub repository (helper method).
        
        Uses multiple matching strategies in order of reliability:
        1. Content hash matching (most reliable - same as duplicate detection)
        2. Exact filename match (if original_filename is stored)
        3. Filename pattern matching (based on title slug)
        4. Title/description content comparison
        
        Returns:
            bool: True if deletion succeeded, False otherwise
        """
        try:
            from ..config import config
            from ..utils.prd_hash import calculate_prd_hash, normalize_text
            import os
            import requests
            import re
            import base64
            
            github_token = config.github_token or os.getenv("GITHUB_TOKEN")
            if not github_token:
                print("⚠️  Error: GitHub token not available, cannot delete from GitHub")
                return False
            
            # Get GitHub repo details
            repo_owner = os.getenv("GITHUB_ORG_NAME", "thedoctorJJ")
            repo_name = os.getenv("GITHUB_REPO_NAME", "ai-agent-factory")
            
            # Extract PRD data
            title = prd_data.get("title", "")
            description = prd_data.get("description", "")
            original_filename = prd_data.get("original_filename")
            content_hash = prd_data.get("content_hash")  # If stored in DB
            
            if not title:
                print("⚠️  Error: PRD title not available, cannot match GitHub file")
                return False
            
            # Calculate content hash for matching (if not already stored)
            if not content_hash and description:
                content_hash = calculate_prd_hash(title, description)
            
            # Helper function for slugifying
            def slugify(text: str) -> str:
                text = text.lower()
                text = re.sub(r"[^a-z0-9]+", "-", text)
                return text.strip("-") or "prd"
            
            # Search for the file in GitHub
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Get all files in prds/queue/
            url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/prds/queue'
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"⚠️  Error: Could not list GitHub files: {response.status_code}")
                if response.status_code == 404:
                    print(f"   Directory prds/queue/ may not exist in repository")
                return False
            
            files = response.json()
            if not isinstance(files, list):
                print(f"⚠️  Error: Unexpected response format from GitHub API")
                return False
            
            matched_file = None
            match_strategy = None
            
            # Strategy 1: Exact filename match (if original_filename is stored)
            if original_filename:
                for file_info in files:
                    file_name = file_info.get("name", "")
                    if file_name == original_filename or file_name == f"prds/queue/{original_filename}":
                        matched_file = file_info
                        match_strategy = "exact_filename"
                        print(f"✅ Matched file by exact filename: {file_name}")
                        break
            
            # Strategy 2: Content hash matching (most reliable)
            if not matched_file and content_hash:
                title_slug = slugify(title)
                for file_info in files:
                    file_name = file_info.get("name", "")
                    if file_name.endswith(".md") and file_name != "README.md":
                        # Check if filename contains hash (format: YYYY-MM-DD_slug_HASH.md)
                        # Extract hash from filename if present
                        file_base = file_name.replace(".md", "")
                        if "_" in file_base:
                            parts = file_base.split("_")
                            if len(parts) >= 3:
                                # Format: date_slug_hash
                                file_hash_part = parts[-1]
                                # Compare with first 8 chars of our hash
                                if content_hash[:8].lower() == file_hash_part.lower():
                                    # Verify by reading file content
                                    file_path = file_info.get("path", "")
                                    file_content_url = file_info.get("download_url")
                                    if file_content_url:
                                        try:
                                            file_response = requests.get(file_content_url, timeout=10)
                                            if file_response.status_code == 200:
                                                file_content = file_response.text
                                                # Extract title and description from file
                                                file_lines = file_content.split('\n')
                                                file_title = ""
                                                file_description = ""
                                                capture_desc = False
                                                
                                                for line in file_lines:
                                                    if line.strip().startswith('# '):
                                                        file_title = line[2:].strip()
                                                    if line.strip().startswith('## Description'):
                                                        capture_desc = True
                                                        continue
                                                    if capture_desc and line.strip().startswith('##'):
                                                        break
                                                    if capture_desc:
                                                        file_description += line + "\n"
                                                
                                                # Calculate hash of file content
                                                file_hash = calculate_prd_hash(file_title, file_description)
                                                if file_hash == content_hash:
                                                    matched_file = file_info
                                                    match_strategy = "content_hash"
                                                    print(f"✅ Matched file by content hash: {file_name}")
                                                    break
                                        except Exception as e:
                                            print(f"   ⚠️  Error reading file {file_name}: {e}")
                                            continue
            
            # Strategy 3: Filename pattern matching (based on title slug)
            if not matched_file:
                title_slug = slugify(title)
                # Try different filename patterns
                patterns = [
                    f"*{title_slug}*.md",
                    f"*{title_slug.replace('-', '_')}*.md",
                ]
                
                for file_info in files:
                    file_name = file_info.get("name", "")
                    if file_name.endswith(".md") and file_name != "README.md":
                        file_base = file_name.replace(".md", "").lower()
                        # Remove date prefix if present (YYYY-MM-DD_)
                        if "_" in file_base:
                            file_slug = "_".join(file_base.split("_")[1:])  # Skip date part
                        else:
                            file_slug = file_base
                        
                        # Check if title slug matches file slug
                        if title_slug in file_slug or file_slug in title_slug:
                            # Verify by reading file and comparing title
                            file_content_url = file_info.get("download_url")
                            if file_content_url:
                                try:
                                    file_response = requests.get(file_content_url, timeout=10)
                                    if file_response.status_code == 200:
                                        file_content = file_response.text
                                        file_lines = file_content.split('\n')
                                        for line in file_lines:
                                            if line.strip().startswith('# '):
                                                file_title = line[2:].strip()
                                                # Normalize and compare
                                                if normalize_text(file_title) == normalize_text(title):
                                                    matched_file = file_info
                                                    match_strategy = "filename_pattern"
                                                    print(f"✅ Matched file by filename pattern: {file_name}")
                                                    break
                                except Exception as e:
                                    print(f"   ⚠️  Error reading file {file_name}: {e}")
                                    continue
                        
                        if matched_file:
                            break
            
            # Strategy 4: Content comparison (read all files and compare title/description)
            if not matched_file and description:
                print(f"   🔍 Trying content comparison for '{title}'...")
                for file_info in files:
                    file_name = file_info.get("name", "")
                    if file_name.endswith(".md") and file_name != "README.md":
                        file_content_url = file_info.get("download_url")
                        if file_content_url:
                            try:
                                file_response = requests.get(file_content_url, timeout=10)
                                if file_response.status_code == 200:
                                    file_content = file_response.text
                                    file_lines = file_content.split('\n')
                                    file_title = ""
                                    file_description = ""
                                    capture_desc = False
                                    
                                    for line in file_lines:
                                        if line.strip().startswith('# '):
                                            file_title = line[2:].strip()
                                        if line.strip().startswith('## Description'):
                                            capture_desc = True
                                            continue
                                        if capture_desc and line.strip().startswith('##'):
                                            break
                                        if capture_desc:
                                            file_description += line + "\n"
                                    
                                    # Compare normalized title and description
                                    if (normalize_text(file_title) == normalize_text(title) and
                                        normalize_text(file_description[:500]) == normalize_text(description[:500])):
                                        matched_file = file_info
                                        match_strategy = "content_comparison"
                                        print(f"✅ Matched file by content comparison: {file_name}")
                                        break
                            except Exception as e:
                                print(f"   ⚠️  Error reading file {file_name}: {e}")
                                continue
            
            if not matched_file:
                print(f"⚠️  Error: Could not find PRD file in GitHub for '{title}'")
                print(f"   Tried strategies: exact_filename, content_hash, filename_pattern, content_comparison")
                if original_filename:
                    print(f"   Original filename: {original_filename}")
                if content_hash:
                    print(f"   Content hash: {content_hash[:16]}...")
                return False
            
            # Delete the file from GitHub
            file_path = matched_file["path"]
            file_sha = matched_file["sha"]
            
            delete_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
            delete_data = {
                "message": f"Delete PRD: {title} (via website)",
                "sha": file_sha,
                "branch": "main"
            }
            
            delete_response = requests.delete(delete_url, headers=headers, json=delete_data, timeout=10)
            
            if delete_response.status_code in [200, 204]:
                print(f"✅ Deleted PRD file from GitHub: {file_path} (matched via {match_strategy})")
                return True
            else:
                error_detail = delete_response.json().get("message", "Unknown error") if delete_response.text else "No error message"
                print(f"⚠️  Error: Failed to delete from GitHub: {delete_response.status_code}")
                print(f"   Error: {error_detail}")
                print(f"   File path: {file_path}")
                return False
        
        except Exception as e:
            # Log the error but return False so caller knows deletion failed
            print(f"⚠️  Error: Could not delete from GitHub: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def clear_all_prds(self) -> Dict[str, str]:
        """Clear all PRDs from the system."""
        # Use simplified data manager
        success = await data_manager.clear_all_prds()
        if success:
            return {"message": "All PRDs cleared successfully"}
        else:
            return {"message": "Failed to clear PRDs"}

    async def upload_prd_file(self, file: UploadFile) -> PRDResponse:
        """Upload and parse a PRD file."""
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        if not file.filename.endswith(('.md', '.txt')):
            raise HTTPException(
                status_code=400,
                detail="File must be a .md or .txt file"
            )

        content = await file.read()
        try:
            content_str = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File must be UTF-8 encoded"
            )

        # Parse the file content
        parsed_data = self._parse_prd_content(content_str, file.filename)

        # Detect PRD type
        detected_type = self._detect_prd_type(content_str)

        # Create PRD
        prd_data = PRDCreate(
            title=parsed_data["title"],
            description=parsed_data["description"],
            requirements=parsed_data["requirements"],
            prd_type=PRDType(detected_type),
            problem_statement=parsed_data.get("problem_statement"),
            target_users=parsed_data.get("target_users"),
            user_stories=parsed_data.get("user_stories"),
            acceptance_criteria=parsed_data.get("acceptance_criteria"),
            technical_requirements=parsed_data.get("technical_requirements"),
            performance_requirements=parsed_data.get("performance_requirements"),
            security_requirements=parsed_data.get("security_requirements"),
            integration_requirements=parsed_data.get("integration_requirements"),
            deployment_requirements=parsed_data.get("deployment_requirements"),
            success_metrics=parsed_data.get("success_metrics"),
            timeline=parsed_data.get("timeline"),
            dependencies=parsed_data.get("dependencies"),
            risks=parsed_data.get("risks"),
            assumptions=parsed_data.get("assumptions"),
            original_filename=file.filename,
            file_content=content_str)

        return await self.create_prd(prd_data)

    async def get_prd_markdown(self, prd_id: str) -> PRDMarkdownResponse:
        """Get PRD as markdown."""
        prd = await self.get_prd(prd_id)
        markdown_content = self._generate_prd_markdown(prd)
        filename = f"PRD_{prd.title.replace(' ', '_')}_{prd.id[:8]}.md"

        return PRDMarkdownResponse(
            prd_id=prd_id,
            markdown=markdown_content,
            filename=filename
        )

    def _parse_prd_content(self, content: str, filename: str = None) -> Dict[str, Any]:
        """Parse PRD content using comprehensive parser."""
        try:
            # Use the comprehensive PRD parser
            parsed_data = self.parser.parse_prd_content(content, filename)
            
            # Validate the parsed structure
            validation = self.parser.validate_prd_structure(parsed_data)
            
            # Add validation info to parsed data
            parsed_data['validation'] = validation
            
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
                "validation": {"is_valid": False, "errors": [f"Parsing failed: {str(e)}"], "warnings": [], "completeness_score": 0}
            }


    def _detect_prd_type(self, content: str) -> str:
        """Detect if PRD is for platform or agent based on content."""
        content_lower = content.lower()

        # Platform indicators (high weight)
        platform_keywords = [
            'platform',
            'factory',
            'infrastructure',
            'system',
            'architecture',
            'framework',
            'core',
            'base',
            'foundation',
            'engine',
            'orchestrator',
            'deployment',
            'ci/cd',
            'pipeline',
            'monitoring',
            'logging',
            'authentication',
            'authorization',
            'database',
            'api',
            'backend',
            'frontend',
            'ui',
            'ux',
            'dashboard',
            'admin',
            'management']

        # Agent indicators (high weight)
        agent_keywords = [
            'agent', 'bot', 'assistant', 'automation', 'workflow', 'task',
            'process', 'execution', 'ai', 'ml', 'model', 'prediction',
            'analysis', 'recommendation', 'chat', 'conversation', 'nlp',
            'openai', 'anthropic', 'claude'
        ]

        # Count keyword occurrences
        platform_score = sum(
            1 for keyword in platform_keywords if keyword in content_lower)
        agent_score = sum(
            1 for keyword in agent_keywords if keyword in content_lower)

        # Additional heuristics
        if any(pattern in content_lower for pattern in [
            'prd type', 'platform prd', 'agent prd', 'type:', 'category:'
        ]):
            if 'platform' in content_lower:
                return 'platform'
            elif 'agent' in content_lower:
                return 'agent'

        # Check for specific patterns
        if 'create agent' in content_lower or 'build agent' in content_lower:
            return 'agent'
        if 'improve platform' in content_lower or 'enhance system' in content_lower:
            return 'platform'

        # Default based on scores
        if platform_score > agent_score:
            return 'platform'
        else:
            return 'agent'

    def _generate_prd_markdown(self, prd: PRDResponse) -> str:
        """Generate standardized markdown PRD."""
        try:
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

    def get_roadmap_data(self) -> Dict[str, Any]:
        """Get roadmap data."""
        return self._roadmap_db


# Global service instance
prd_service = PRDService()
