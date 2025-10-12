"""
Validation utilities for data validation and sanitization.
"""
import re
from typing import List, Optional
from urllib.parse import urlparse


def validate_prd_title(title: str) -> str:
    """Validate and sanitize PRD title."""
    if not title or not title.strip():
        raise ValueError("PRD title cannot be empty")

    title = title.strip()
    if len(title) > 200:
        raise ValueError("PRD title cannot exceed 200 characters")

    # Remove potentially harmful characters
    title = re.sub(r'[<>:"/\\|?*]', '', title)

    return title


def validate_prd_description(description: str) -> str:
    """Validate and sanitize PRD description."""
    if not description or not description.strip():
        raise ValueError("PRD description cannot be empty")

    description = description.strip()
    if len(description) > 10000:
        raise ValueError("PRD description cannot exceed 10,000 characters")

    return description


def validate_requirements(requirements: List[str]) -> List[str]:
    """Validate and sanitize requirements list."""
    if not requirements:
        return []

    validated_requirements = []
    for req in requirements:
        if req and req.strip():
            req = req.strip()
            if len(req) > 500:
                raise ValueError(
                    "Individual requirement cannot exceed 500 characters")
            validated_requirements.append(req)

    if len(validated_requirements) > 50:
        raise ValueError("Cannot have more than 50 requirements")

    return validated_requirements


def validate_agent_name(name: str) -> str:
    """Validate and sanitize agent name."""
    if not name or not name.strip():
        raise ValueError("Agent name cannot be empty")

    name = name.strip()
    if len(name) > 100:
        raise ValueError("Agent name cannot exceed 100 characters")

    # Agent names should be alphanumeric with hyphens and underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        raise ValueError(
            "Agent name can only contain letters, numbers, hyphens, and underscores")

    return name


def validate_url(url: str, field_name: str = "URL") -> str:
    """Validate URL format."""
    if not url or not url.strip():
        raise ValueError(f"{field_name} cannot be empty")

    url = url.strip()

    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid {field_name} format")

        if parsed.scheme not in ['http', 'https']:
            raise ValueError(f"{field_name} must use HTTP or HTTPS protocol")

        return url
    except Exception:
        raise ValueError(f"Invalid {field_name} format")


def validate_version(version: str) -> str:
    """Validate version string format."""
    if not version or not version.strip():
        raise ValueError("Version cannot be empty")

    version = version.strip()

    # Basic semantic versioning validation
    if not re.match(
        r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$',
            version):
        raise ValueError(
            "Version must follow semantic versioning format (e.g., 1.0.0)")

    return version


def validate_capabilities(capabilities: List[str]) -> List[str]:
    """Validate and sanitize capabilities list."""
    if not capabilities:
        return []

    validated_capabilities = []
    for cap in capabilities:
        if cap and cap.strip():
            cap = cap.strip()
            if len(cap) > 200:
                raise ValueError(
                    "Individual capability cannot exceed 200 characters")
            validated_capabilities.append(cap)

    if len(validated_capabilities) > 20:
        raise ValueError("Cannot have more than 20 capabilities")

    return validated_capabilities


def validate_priority_score(
        score: Optional[int],
        field_name: str = "Priority score") -> Optional[int]:
    """Validate priority score (1-10 scale)."""
    if score is None:
        return None

    if not isinstance(score, int):
        raise ValueError(f"{field_name} must be an integer")

    if score < 1 or score > 10:
        raise ValueError(f"{field_name} must be between 1 and 10")

    return score


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    if not filename:
        return "untitled"

    # Remove path components
    filename = filename.split('/')[-1].split('\\')[-1]

    # Remove potentially harmful characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit(
            '.', 1) if '.' in filename else (
            filename, '')
        filename = name[:250] + ('.' + ext if ext else '')

    return filename


def validate_file_content(content: str, max_size: int = 1024 * 1024) -> str:
    """Validate file content."""
    if not content:
        raise ValueError("File content cannot be empty")

    if len(content.encode('utf-8')) > max_size:
        raise ValueError(f"File content cannot exceed {max_size // 1024}KB")

    return content


def validate_pagination_params(skip: int, limit: int) -> tuple[int, int]:
    """Validate pagination parameters."""
    if skip < 0:
        raise ValueError("Skip parameter cannot be negative")

    if limit < 1:
        raise ValueError("Limit parameter must be at least 1")

    if limit > 1000:
        raise ValueError("Limit parameter cannot exceed 1000")

    return skip, limit
