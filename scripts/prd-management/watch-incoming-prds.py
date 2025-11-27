#!/usr/bin/env python3
"""
File watcher for incoming PRDs folder.
Automatically processes new PRD files when they are added to prds/incoming/
"""

import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("⚠️  watchdog library not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog"])
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

import requests


class PRDFileHandler(FileSystemEventHandler):
    """Handler for PRD file events."""
    
    def __init__(self, incoming_dir: Path, uploaded_dir: Path, backend_url: str):
        self.incoming_dir = incoming_dir
        self.uploaded_dir = uploaded_dir
        self.backend_url = backend_url
        self.processed_files = set()
        
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Only process .md files
        if not file_path.suffix == '.md':
            return
        
        # Skip README files
        if file_path.name.lower() == 'readme.md':
            return
        
        # Avoid processing the same file multiple times
        if str(file_path) in self.processed_files:
            return
        
        # Wait a moment for file to be fully written
        time.sleep(0.5)
        
        print(f"\n📄 New PRD file detected: {file_path.name}")
        self.process_prd_file(file_path)
    
    def process_prd_file(self, file_path: Path):
        """Process a PRD file by uploading it to the backend."""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Upload to backend
            print(f"📤 Uploading PRD to backend...")
            response = requests.post(
                f"{self.backend_url}/api/v1/prds/upload",
                files={"file": (file_path.name, content, "text/markdown")},
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                prd_data = response.json()
                prd_id = prd_data.get('id', 'unknown')
                title = prd_data.get('title', file_path.name)
                
                print(f"✅ PRD uploaded successfully!")
                print(f"   Title: {title}")
                print(f"   ID: {prd_id[:8]}...")
                
                # Move file to uploaded directory
                uploaded_path = self.uploaded_dir / file_path.name
                shutil.move(str(file_path), str(uploaded_path))
                print(f"📁 Moved to: {uploaded_path}")
                
                # Mark as processed
                self.processed_files.add(str(file_path))
                
            elif response.status_code == 400:
                error_detail = response.json().get('detail', 'Unknown error')
                print(f"⚠️  Upload failed: {error_detail}")
                print(f"   File kept in incoming folder for manual review")
                
            else:
                print(f"❌ Upload failed: HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                print(f"   File kept in incoming folder for manual review")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            print(f"   File kept in incoming folder for manual review")
        except Exception as e:
            print(f"❌ Error processing file: {e}")
            print(f"   File kept in incoming folder for manual review")


def watch_incoming_prds(backend_url: Optional[str] = None):
    """Start watching the incoming PRDs folder."""
    # Get paths
    project_root = Path(__file__).parent.parent.parent
    incoming_dir = project_root / "prds" / "incoming"
    uploaded_dir = project_root / "prds" / "uploaded"
    
    # Ensure directories exist
    incoming_dir.mkdir(parents=True, exist_ok=True)
    uploaded_dir.mkdir(parents=True, exist_ok=True)
    
    # Get backend URL
    if not backend_url:
        backend_url = os.getenv(
            "BACKEND_URL",
            "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
        )
    
    print("=" * 60)
    print("🔍 PRD File Watcher - Incoming PRDs")
    print("=" * 60)
    print(f"📁 Watching: {incoming_dir}")
    print(f"📁 Uploaded to: {uploaded_dir}")
    print(f"🌐 Backend URL: {backend_url}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\n💡 Add .md files to the incoming folder to process them automatically")
    print("   Press Ctrl+C to stop\n")
    
    # Create event handler
    event_handler = PRDFileHandler(incoming_dir, uploaded_dir, backend_url)
    
    # Create observer
    observer = Observer()
    observer.schedule(event_handler, str(incoming_dir), recursive=False)
    observer.start()
    
    try:
        # Process any existing files first
        existing_files = list(incoming_dir.glob("*.md"))
        existing_files = [f for f in existing_files if f.name.lower() != 'readme.md']
        
        if existing_files:
            print(f"📋 Found {len(existing_files)} existing file(s), processing...")
            for file_path in existing_files:
                event_handler.process_prd_file(file_path)
            print()
        
        # Keep watching
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping file watcher...")
        observer.stop()
    
    observer.join()
    print("✅ File watcher stopped")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Watch incoming PRDs folder for new files")
    parser.add_argument(
        "--backend-url",
        help="Backend API URL (default: from env or production URL)",
        default=None
    )
    
    args = parser.parse_args()
    watch_incoming_prds(args.backend_url)



