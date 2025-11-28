#!/usr/bin/env python3
"""
PRD Reconciliation Script
Ensures database matches GitHub (source of truth) by:
1. Removing PRDs in database that aren't in GitHub
2. Adding PRDs from GitHub that aren't in database
3. Updating PRDs where content differs
"""

import os
import sys
import requests
from pathlib import Path
from typing import Set, Dict, List
import hashlib
import re


def get_backend_url():
    """Get backend URL from environment or use default"""
    return os.getenv(
        "BACKEND_URL",
        "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
    )


def calculate_file_hash(file_path: Path) -> str:
    """Calculate hash of file content"""
    content = file_path.read_text(encoding='utf-8')
    # Normalize line endings
    content = content.replace('\r\n', '\n')
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def normalize_text(text: str) -> str:
    """Normalize text for consistent hashing (matches backend logic)"""
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


def calculate_prd_content_hash(file_path: Path) -> str:
    """Calculate PRD content hash from file (matches backend calculate_prd_hash logic)"""
    content = file_path.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # Extract title (first H1)
    title = ""
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Extract description (first 500 chars after ## Description)
    description = ""
    capture_desc = False
    for line in lines:
        if line.strip().startswith('## Description'):
            capture_desc = True
            continue
        if capture_desc and line.strip().startswith('##'):
            break
        if capture_desc:
            description += line + "\n"
    
    # Normalize and hash (matches backend logic)
    norm_title = normalize_text(title)
    norm_description = normalize_text(description)[:500]  # First 500 chars
    content_key = f"{norm_title}::{norm_description}"
    
    return hashlib.sha256(content_key.encode('utf-8')).hexdigest()


def extract_title_from_file(file_path: Path) -> str:
    """Extract title from markdown file"""
    content = file_path.read_text(encoding='utf-8')
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return file_path.stem


def get_github_prds(project_root: Path) -> Dict[str, Dict]:
    """Get all PRDs from GitHub (local repo)"""
    queue_folder = project_root / "prds" / "queue"
    
    if not queue_folder.exists():
        print(f"❌ Error: PRD queue folder not found: {queue_folder}")
        sys.exit(1)
    
    prd_files = sorted(queue_folder.glob("*.md"))
    # Exclude README
    prd_files = [f for f in prd_files if f.name.lower() != "readme.md"]
    
    github_prds = {}
    for prd_file in prd_files:
        file_hash = calculate_file_hash(prd_file)
        title = extract_title_from_file(prd_file)
        github_prds[prd_file.name] = {
            "filename": prd_file.name,
            "title": title,
            "file_hash": file_hash,
            "path": prd_file
        }
    
    return github_prds


def get_database_prds(backend_url: str) -> Dict[str, Dict]:
    """Get all PRDs from database"""
    try:
        response = requests.get(f"{backend_url}/api/v1/prds", timeout=10)
        if response.status_code != 200:
            print(f"❌ Error fetching PRDs from database: HTTP {response.status_code}")
            sys.exit(1)
        
        data = response.json()
        db_prds = {}
        
        for prd in data.get("prds", []):
            # Try to match by title (imperfect, but best we have without original_filename)
            title = prd.get("title", "")
            # Handle multiple PRDs with same title by using title + id
            key = f"{title}_{prd.get('id')}" if title in db_prds else title
            db_prds[key] = {
                "id": prd.get("id"),
                "title": title,
                "content_hash": prd.get("content_hash"),
                "original_filename": prd.get("original_filename"),
                "file_content": prd.get("file_content")  # Store full content for comparison
            }
        
        return db_prds
    except Exception as e:
        print(f"❌ Error fetching database PRDs: {e}")
        sys.exit(1)


def delete_prd(backend_url: str, prd_id: str, title: str) -> bool:
    """Delete a PRD from database"""
    try:
        response = requests.delete(f"{backend_url}/api/v1/prds/{prd_id}", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Deleted: {title}")
            return True
        else:
            print(f"   ❌ Failed to delete: {title} (HTTP {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Error deleting {title}: {e}")
        return False


def upload_prd(backend_url: str, file_path: Path) -> bool:
    """Upload a PRD file to database"""
    try:
        content = file_path.read_text(encoding='utf-8')
        response = requests.post(
            f"{backend_url}/api/v1/prds/upload",
            files={"file": (file_path.name, content, "text/markdown")},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"   ✅ Added: {result.get('title')} (ID: {result.get('id')})")
            return True
        else:
            print(f"   ❌ Failed to add: {file_path.name} (HTTP {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Error uploading {file_path.name}: {e}")
        return False


def reconcile():
    """Main reconciliation function"""
    print("🔄 PRD Reconciliation: GitHub → Database")
    print("=" * 60)
    print("📌 GitHub is the source of truth")
    print("")
    
    backend_url = get_backend_url()
    project_root = Path(__file__).parent.parent.parent
    
    # Get PRDs from both sources
    print("📂 Reading GitHub PRDs...")
    github_prds = get_github_prds(project_root)
    print(f"   Found {len(github_prds)} PRDs in GitHub")
    
    print("\n📊 Reading Database PRDs...")
    db_prds = get_database_prds(backend_url)
    print(f"   Found {len(db_prds)} PRDs in Database")
    
    # Build title → filename mapping for GitHub
    github_by_title = {v["title"]: k for k, v in github_prds.items()}
    
    # Track changes
    deleted = 0
    added = 0
    unchanged = 0
    
    # Step 1: Remove PRDs in database that aren't in GitHub
    print("\n🗑️  Step 1: Removing PRDs not in GitHub...")
    for db_title, db_prd in db_prds.items():
        if db_title not in github_by_title:
            print(f"   🔍 '{db_title}' exists in database but not in GitHub")
            if delete_prd(backend_url, db_prd["id"], db_title):
                deleted += 1
    
    if deleted == 0:
        print("   ✅ No orphaned PRDs found")
    
    # Step 2: Add PRDs from GitHub that aren't in database
    print("\n➕ Step 2: Adding missing PRDs from GitHub...")
    for github_title, github_filename in github_by_title.items():
        if github_title not in db_prds:
            print(f"   🔍 '{github_title}' exists in GitHub but not in database")
            github_prd = github_prds[github_filename]
            
            # CRITICAL FIX: Check content hash before uploading to prevent duplicates
            github_content_hash = calculate_prd_content_hash(github_prd["path"])
            duplicate_found = False
            
            # Check if any database PRD has the same content hash
            for db_key, db_prd in db_prds.items():
                db_hash = db_prd.get("content_hash")
                if db_hash and db_hash == github_content_hash:
                    print(f"   ⚠️  Duplicate detected by content hash - skipping upload")
                    print(f"      Existing PRD: '{db_prd.get('title', 'N/A')}' (ID: {db_prd.get('id', 'N/A')[:8]}...)")
                    duplicate_found = True
                    unchanged += 1
                    break
            
            if not duplicate_found:
                if upload_prd(backend_url, github_prd["path"]):
                    added += 1
        else:
            unchanged += 1
    
    if added == 0:
        print("   ✅ No missing PRDs found")
    
    # Step 3: Update PRDs where content differs (GitHub wins)
    print("\n🔄 Step 3: Updating PRDs where content differs...")
    updated = 0
    
    # Re-fetch database PRDs to get the latest state after adds/deletes
    db_prds_current = get_database_prds(backend_url)
    db_by_title = {}
    for key, prd in db_prds_current.items():
        title = prd["title"]
        if title not in db_by_title:
            db_by_title[title] = prd
    
    for github_title, github_filename in github_by_title.items():
        if github_title in db_by_title:
            github_prd = github_prds[github_filename]
            db_prd = db_by_title[github_title]
            
            # Read GitHub file content
            github_content = github_prd["path"].read_text(encoding='utf-8')
            github_content_normalized = github_content.replace('\r\n', '\n').strip()
            
            # Get database file content
            db_content = db_prd.get("file_content", "")
            if db_content:
                db_content_normalized = db_content.replace('\r\n', '\n').strip()
            else:
                db_content_normalized = ""
            
            # Compare content
            if github_content_normalized != db_content_normalized:
                print(f"   🔍 '{github_title}' has different content - updating from GitHub")
                # Delete old version
                if delete_prd(backend_url, db_prd["id"], github_title):
                    # Upload new version
                    if upload_prd(backend_url, github_prd["path"]):
                        print(f"   ✅ Updated: {github_title}")
                        updated += 1
                    else:
                        print(f"   ❌ Failed to re-upload: {github_title}")
    
    if updated == 0:
        print("   ✅ No content updates needed")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Reconciliation Summary:")
    print(f"   ➖ Deleted:   {deleted} PRD(s)")
    print(f"   ➕ Added:     {added} PRD(s)")
    print(f"   🔄 Updated:   {updated} PRD(s)")
    print(f"   ✅ Unchanged: {unchanged - updated} PRD(s)")
    
    # Verify final state
    print("\n🔍 Verifying final state...")
    final_db_prds = get_database_prds(backend_url)
    
    if len(final_db_prds) == len(github_prds):
        print(f"   ✅ Database matches GitHub: {len(final_db_prds)} PRDs")
        print("\n✅ Reconciliation complete - GitHub and Database are in sync!")
        return 0
    else:
        print(f"   ⚠️  Mismatch: GitHub has {len(github_prds)}, Database has {len(final_db_prds)}")
        print("\n⚠️  Reconciliation completed with discrepancies")
        return 1


if __name__ == "__main__":
    sys.exit(reconcile())

