#!/usr/bin/env python3
"""
Create sample PRD FILES (not database entries)
PRD files are the source of truth - they can be synced to database later
"""

import json
import os
from datetime import datetime

# Import the sample PRDs from the original script
import sys
sys.path.append(os.path.dirname(__file__))
from create_sample_prds import SAMPLE_PRDS

PRD_DIR = "prds/queue"

def create_prd_file(prd_data, date_str=None):
    """Create a PRD markdown file from PRD data"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    title = prd_data['title']
    safe_title = title.lower().replace(' ', '-').replace('/', '-').replace(':', '')
    safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')
    filename = f"{date_str}_{safe_title}.md"
    filepath = os.path.join(PRD_DIR, filename)
    
    # Check if file already exists
    if os.path.exists(filepath):
        print(f"⏭️  Skipping: {filename} (already exists)")
        return False
    
    # Generate markdown content
    content = f"""## **Title**

**{title}**

---

## **Description**

{prd_data.get('description', '')}

---

## **Problem Statement**

{prd_data.get('problem_statement', '')}

---

## **Target Users**

"""
    
    # Add target users
    if prd_data.get('target_users'):
        for user in prd_data['target_users']:
            content += f"* {user}\n"
    
    content += "\n---\n\n## **User Stories**\n\n"
    
    # Add user stories
    if prd_data.get('user_stories'):
        for story in prd_data['user_stories']:
            content += f"* {story}\n"
    
    content += "\n---\n\n## **Requirements**\n\n"
    
    # Add requirements
    if prd_data.get('requirements'):
        for i, req in enumerate(prd_data['requirements'], 1):
            content += f"{i}. {req}\n"
    
    content += "\n---\n\n## **Acceptance Criteria**\n\n"
    
    # Add acceptance criteria
    if prd_data.get('acceptance_criteria'):
        for criterion in prd_data['acceptance_criteria']:
            content += f"* {criterion}\n"
    
    if prd_data.get('technical_requirements'):
        content += "\n---\n\n## **Technical Requirements**\n\n"
        for req in prd_data['technical_requirements']:
            content += f"* {req}\n"
    
    if prd_data.get('success_metrics'):
        content += "\n---\n\n## **Success Metrics**\n\n"
        for metric in prd_data['success_metrics']:
            content += f"* {metric}\n"
    
    if prd_data.get('timeline'):
        content += f"\n---\n\n## **Timeline**\n\n{prd_data['timeline']}\n"
    
    if prd_data.get('dependencies_list'):
        content += "\n---\n\n## **Dependencies**\n\n"
        for dep in prd_data['dependencies_list']:
            content += f"* {dep}\n"
    
    # Write file
    os.makedirs(PRD_DIR, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created PRD file: {filename}")
    return True

def main():
    """Create sample PRD files"""
    print("📝 Creating Sample PRD Files")
    print("=============================")
    print("")
    print("🎯 PRD files are the source of truth")
    print("   Run ./scripts/prd-management/sync-prds-to-database.sh to upload them")
    print("")
    
    created = 0
    skipped = 0
    
    for prd_data in SAMPLE_PRDS:
        if create_prd_file(prd_data):
            created += 1
        else:
            skipped += 1
    
    print("")
    print("=============================")
    print(f"Summary:")
    print(f"  ✅ Created: {created}")
    print(f"  ⏭️  Skipped: {skipped}")
    print("")
    print("💡 Next step: Run ./scripts/prd-management/sync-prds-to-database.sh to upload to database")

if __name__ == "__main__":
    main()

