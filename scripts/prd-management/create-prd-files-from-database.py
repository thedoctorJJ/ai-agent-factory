#!/usr/bin/env python3
"""
Create PRD files from database entries that don't have files
This ensures files become the source of truth
"""

import requests
import json
import os
from datetime import datetime

BACKEND_URL = "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
PRD_DIR = "prds/queue"

def create_safe_filename(title, date_str=None):
    """Create a safe filename from PRD title"""
    safe_title = title.lower().replace(' ', '-').replace('/', '-').replace(':', '')
    safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')
    if date_str:
        return f"{date_str}_{safe_title}.md"
    else:
        return f"{datetime.now().strftime('%Y-%m-%d')}_{safe_title}.md"

def get_prd_markdown_content(prd):
    """Generate markdown content from PRD data"""
    title = prd['title'].strip('*').strip()
    
    content = f"""## **Title**

**{title}**

---

## **Description**

{prd.get('description', '')}

---

## **Problem Statement**

{prd.get('problem_statement', '')}

---

## **Target Users**

"""
    
    # Add target users
    if prd.get('target_users'):
        for user in prd['target_users']:
            content += f"* {user}\n"
    else:
        content += "* Users\n"
    
    content += "\n---\n\n## **User Stories**\n\n"
    
    # Add user stories
    if prd.get('user_stories'):
        for story in prd['user_stories']:
            content += f"* {story}\n"
    else:
        content += "* As a user, I want...\n"
    
    content += "\n---\n\n## **Requirements**\n\n"
    
    # Add requirements
    if prd.get('requirements'):
        for i, req in enumerate(prd['requirements'], 1):
            content += f"{i}. {req}\n"
    else:
        content += "1. [Requirement]\n"
    
    content += "\n---\n\n## **Acceptance Criteria**\n\n"
    
    # Add acceptance criteria
    if prd.get('acceptance_criteria'):
        for criterion in prd['acceptance_criteria']:
            # Clean up markdown formatting
            criterion = criterion.strip()
            if not criterion.startswith('*'):
                content += f"* {criterion}\n"
            else:
                content += f"{criterion}\n"
    else:
        content += "* [Criterion]\n"
    
    if prd.get('technical_requirements'):
        content += "\n---\n\n## **Technical Requirements**\n\n"
        for req in prd['technical_requirements']:
            content += f"* {req}\n"
    
    if prd.get('success_metrics'):
        content += "\n---\n\n## **Success Metrics**\n\n"
        for metric in prd['success_metrics']:
            content += f"* {metric}\n"
    
    if prd.get('timeline'):
        content += f"\n---\n\n## **Timeline**\n\n{prd['timeline']}\n"
    
    if prd.get('dependencies_list'):
        content += "\n---\n\n## **Dependencies**\n\n"
        for dep in prd['dependencies_list']:
            content += f"* {dep}\n"
    
    return content

def main():
    print("📝 Creating PRD Files from Database")
    print("====================================")
    print("")
    
    # Ensure directory exists
    os.makedirs(PRD_DIR, exist_ok=True)
    
    # Get all PRDs from database
    print("🔍 Fetching PRDs from database...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/prds", timeout=10)
        response.raise_for_status()
        data = response.json()
        prds = data.get('prds', [])
    except Exception as e:
        print(f"❌ Error fetching PRDs: {e}")
        return
    
    print(f"Found {len(prds)} PRDs in database\n")
    
    created = 0
    exists = 0
    skipped = 0
    
    for prd in prds:
        title = prd['title'].strip('*').strip()
        
        # Use created_at date or today's date
        if prd.get('created_at'):
            date_str = prd['created_at'][:10]  # YYYY-MM-DD
        else:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        filename = create_safe_filename(title, date_str)
        filepath = os.path.join(PRD_DIR, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            print(f"⏭️  Skipping: {filename} (already exists)")
            exists += 1
            continue
        
        # Check if a file with similar title exists
        existing_files = [f for f in os.listdir(PRD_DIR) if f.endswith('.md') and title.lower().replace(' ', '-') in f.lower()]
        if existing_files:
            print(f"⏭️  Skipping: {title} (similar file exists: {existing_files[0]})")
            skipped += 1
            continue
        
        # Create PRD file content
        content = get_prd_markdown_content(prd)
        
        # Write file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created: {filename}")
            created += 1
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")
    
    print(f"\n====================================")
    print(f"Summary:")
    print(f"  ✅ Created: {created}")
    print(f"  ⏭️  Already exists: {exists}")
    print(f"  ⏭️  Skipped (similar): {skipped}")
    print(f"\n✅ PRD files are now the source of truth")

if __name__ == "__main__":
    main()

