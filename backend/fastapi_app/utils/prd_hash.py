"""
PRD Content Hash Utility
Generates deterministic hashes for duplicate detection
"""
import hashlib
import re


def normalize_text(text: str) -> str:
    """Normalize text for consistent hashing"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'__(.+?)__', r'\1', text)      # Bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)      # Italic
    text = re.sub(r'_(.+?)_', r'\1', text)        # Italic
    text = re.sub(r'`(.+?)`', r'\1', text)        # Code
    
    # Strip leading/trailing whitespace
    return text.strip()


def calculate_prd_hash(title: str, description: str) -> str:
    """
    Calculate deterministic hash for PRD duplicate detection.
    
    Args:
        title: PRD title
        description: PRD description
        
    Returns:
        64-character hex string (SHA-256 hash)
        
    Example:
        >>> calculate_prd_hash("Weather Dashboard", "A weather app")
        'a1b2c3d4e5f6...'
    """
    # Normalize inputs
    norm_title = normalize_text(title)
    norm_description = normalize_text(description)
    
    # Create combined content string
    content = f"{norm_title}::{norm_description[:500]}"  # Use first 500 chars of description
    
    # Calculate SHA-256 hash
    hash_obj = hashlib.sha256(content.encode('utf-8'))
    return hash_obj.hexdigest()


def generate_prd_filename(title: str, content_hash: str, date_str: str = None) -> str:
    """
    Generate standardized PRD filename with content hash.
    
    Args:
        title: PRD title
        content_hash: Content hash (from calculate_prd_hash)
        date_str: Date string (YYYY-MM-DD), defaults to today
        
    Returns:
        Filename in format: YYYY-MM-DD_slug_HASH.md
        
    Example:
        >>> generate_prd_filename("Weather Dashboard", "abc123...", "2025-11-27")
        '2025-11-27_weather-dashboard_abc123.md'
    """
    from datetime import datetime
    
    if not date_str:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Slugify title
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-') or 'prd'
    
    # Use first 8 chars of hash for brevity
    short_hash = content_hash[:8]
    
    return f"{date_str}_{slug}_{short_hash}.md"


# Example usage and testing
if __name__ == "__main__":
    # Test hash calculation
    title1 = "Weather Dashboard"
    desc1 = "A responsive weather dashboard"
    
    title2 = "**Weather Dashboard**"  # With markdown
    desc2 = "A  responsive   weather  dashboard"  # Extra spaces
    
    hash1 = calculate_prd_hash(title1, desc1)
    hash2 = calculate_prd_hash(title2, desc2)
    
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Same hash: {hash1 == hash2}")  # Should be True (normalized)
    
    # Test filename generation
    filename = generate_prd_filename(title1, hash1)
    print(f"Filename: {filename}")

