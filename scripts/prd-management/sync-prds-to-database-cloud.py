#!/usr/bin/env python3
"""
Sync PRDs from repository to database via API (for GitHub Actions)
This script uploads all PRD files from prds/queue/ to the backend database.
"""

import os
import sys
import requests
from pathlib import Path
import time

def get_backend_url():
    """Get backend URL from environment or use default"""
    return os.getenv(
        "BACKEND_URL",
        "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
    )

def sync_prd_file(file_path: Path, backend_url: str) -> dict:
    """Upload a single PRD file to the database"""
    try:
        # Read file content
        content = file_path.read_text(encoding='utf-8')
        
        # Upload via API
        response = requests.post(
            f"{backend_url}/api/v1/prds/upload",
            files={"file": (file_path.name, content, "text/markdown")},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            return {
                "success": True,
                "title": result.get("title"),
                "id": result.get("id"),
                "status": result.get("status")
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text[:200]}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    """Main sync function"""
    print("🔄 Syncing PRDs to Database (Cloud)")
    print("=" * 50)
    
    backend_url = get_backend_url()
    print(f"📡 Backend URL: {backend_url}")
    
    # Find PRD files
    project_root = Path(__file__).parent.parent.parent
    queue_folder = project_root / "prds" / "queue"
    
    if not queue_folder.exists():
        print(f"❌ Error: PRD queue folder not found: {queue_folder}")
        sys.exit(1)
    
    prd_files = sorted(queue_folder.glob("*.md"))
    # Exclude README
    prd_files = [f for f in prd_files if f.name.lower() != "readme.md"]
    
    print(f"\n📋 Found {len(prd_files)} PRD files")
    
    if not prd_files:
        print("⚠️  No PRD files to sync")
        sys.exit(0)
    
    # Sync each file
    uploaded = 0
    failed = 0
    skipped = 0
    
    for prd_file in prd_files:
        print(f"\n📤 Syncing: {prd_file.name}")
        
        result = sync_prd_file(prd_file, backend_url)
        
        if result["success"]:
            print(f"   ✅ Uploaded: {result.get('title', 'Unknown title')}")
            print(f"   📝 ID: {result.get('id', 'N/A')}")
            uploaded += 1
        else:
            error = result.get("error", "Unknown error")
            # Check if it's a duplicate (already exists)
            if "already exists" in error.lower() or "duplicate" in error.lower():
                print(f"   ⏭️  Already synced")
                skipped += 1
            else:
                print(f"   ❌ Failed: {error}")
                failed += 1
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Sync Summary:")
    print(f"   ✅ Uploaded: {uploaded}")
    print(f"   ⏭️  Already synced: {skipped}")
    if failed > 0:
        print(f"   ❌ Failed: {failed}")
    
    # Get final database count
    try:
        response = requests.get(f"{backend_url}/api/v1/prds", timeout=10)
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            print(f"\n📊 Database PRDs: {total}")
        else:
            print(f"\n⚠️  Could not verify database count: HTTP {response.status_code}")
    except Exception as e:
        print(f"\n⚠️  Could not verify database count: {e}")
    
    print("\n✅ Sync complete!")
    
    # Exit with error if any failed (excluding skipped)
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()

