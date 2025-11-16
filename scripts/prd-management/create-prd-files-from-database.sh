#!/bin/bash
# Create PRD files from database entries that don't have files
# This ensures files become the source of truth

set -e

echo "📝 Creating PRD Files from Database"
echo "===================================="
echo ""

BACKEND_URL="https://ai-agent-factory-backend-952475323593.us-central1.run.app"
PRD_DIR="prds/queue"
CREATED=0
EXISTS=0

# Get all PRDs from database
echo "🔍 Fetching PRDs from database..."
PRDS_JSON=$(curl -s "$BACKEND_URL/api/v1/prds")

# Extract PRD data
echo "$PRDS_JSON" | python3 << 'PYTHON_SCRIPT'
import sys
import json
import os
from datetime import datetime

data = json.load(sys.stdin)
prds = data.get('prds', [])

prd_dir = "prds/queue"
os.makedirs(prd_dir, exist_ok=True)

created = 0
exists = 0

for prd in prds:
    title = prd['title'].strip('*').strip()
    # Create safe filename
    safe_title = title.lower().replace(' ', '-').replace('/', '-').replace(':', '')
    safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')
    
    # Use created_at date or today's date
    if prd.get('created_at'):
        date_str = prd['created_at'][:10]  # YYYY-MM-DD
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    filename = f"{date_str}_{safe_title}.md"
    filepath = os.path.join(prd_dir, filename)
    
    # Check if file already exists
    if os.path.exists(filepath):
        print(f"⏭️  Skipping: {filename} (already exists)")
        exists += 1
        continue
    
    # Create PRD file content
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
    
    content += "\n---\n\n## **User Stories**\n\n"
    
    # Add user stories
    if prd.get('user_stories'):
        for story in prd['user_stories']:
            content += f"* {story}\n"
    
    content += "\n---\n\n## **Requirements**\n\n"
    
    # Add requirements
    if prd.get('requirements'):
        for i, req in enumerate(prd['requirements'], 1):
            content += f"{i}. {req}\n"
    
    content += "\n---\n\n## **Acceptance Criteria**\n\n"
    
    # Add acceptance criteria
    if prd.get('acceptance_criteria'):
        for criterion in prd['acceptance_criteria']:
            content += f"* {criterion}\n"
    
    content += "\n---\n\n## **Technical Requirements**\n\n"
    
    # Add technical requirements
    if prd.get('technical_requirements'):
        for req in prd['technical_requirements']:
            content += f"* {req}\n"
    
    content += "\n---\n\n## **Success Metrics**\n\n"
    
    # Add success metrics
    if prd.get('success_metrics'):
        for metric in prd['success_metrics']:
            content += f"* {metric}\n"
    
    if prd.get('timeline'):
        content += f"\n---\n\n## **Timeline**\n\n{prd['timeline']}\n"
    
    if prd.get('dependencies_list'):
        content += "\n---\n\n## **Dependencies**\n\n"
        for dep in prd['dependencies_list']:
            content += f"* {dep}\n"
    
    # Write file
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ Created: {filename}")
    created += 1

print(f"\n====================================")
print(f"Summary:")
print(f"  Created: {created}")
print(f"  Already exists: {exists}")
PYTHON_SCRIPT

echo ""
echo "✅ PRD files created from database entries"
echo "   Files are now the source of truth"

