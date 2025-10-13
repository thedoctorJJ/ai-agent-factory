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
        """Create a new PRD."""
        prd_id = str(uuid.uuid4())
        now = datetime.utcnow()

        prd_dict = {
            "id": prd_id,
            "title": prd_data.title,
            "description": prd_data.description,
            "requirements": prd_data.requirements,
            "prd_type": prd_data.prd_type.value,
            "status": PRDStatus.QUEUE.value,
            "github_repo_url": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
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

    async def delete_prd(self, prd_id: str) -> Dict[str, str]:
        """Delete a PRD."""
        # Try to delete from database first
        try:
            if data_manager.is_connected():
                success = await data_manager.delete_prd(prd_id)
                if success:
                    return {"message": "PRD deleted successfully"}
        except Exception as e:
            print(f"Database delete failed, trying in-memory storage: {e}")
        
        # Fallback to in-memory storage
        if not hasattr(self, '_prds_db'):
            self._prds_db: Dict[str, Dict[str, Any]] = {}
        if prd_id not in self._prds_db:
            raise HTTPException(status_code=404, detail="PRD not found")

        del self._prds_db[prd_id]
        return {"message": "PRD deleted successfully"}

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
