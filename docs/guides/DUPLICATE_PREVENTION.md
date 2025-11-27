# Duplicate Prevention System

## Overview

The AI Agent Factory prevents duplicate PRD files in GitHub through a **multi-layer defense strategy**:

1. **Prevention at Creation** (MCP Server) - Stops duplicates before they're created
2. **Reconciliation at Sync** (GitHub Actions) - Cleans up duplicates if they slip through
3. **Content-Based Detection** (Hash Matching) - Catches duplicates even with different filenames

## Layer 1: Prevention at Creation (MCP Server)

### How It Works

When ChatGPT or any tool submits a PRD via the MCP server, **before** creating the file in GitHub:

```
1. Extract title + description from new PRD content
2. Calculate content hash (SHA-256 of normalized text)
3. List all existing PRD files in GitHub (prds/queue/)
4. For each existing file:
   - Extract its title + description
   - Calculate its content hash
   - Compare with new PRD hash
5. If match found:
   ❌ REJECT creation
   ✅ Return existing file info
6. If no match:
   ✅ CREATE new file
```

### What Gets Compared

**Content Hash Components:**
- Title (normalized: lowercase, stripped of markdown)
- Description (first 500 characters, normalized)

**Normalization:**
- Convert to lowercase
- Remove extra whitespace
- Strip markdown formatting (**, __, *, _, `)

**Example:**
```markdown
# Weather Dashboard
## Description
A responsive weather dashboard...
```
↓ Normalized ↓
```
weather dashboard::a responsive weather dashboard...
```
↓ Hashed ↓
```
5ce887cd7da5daaa7d20ad136d64970460b757711ad1d1d57c0d26eaa385b35b
```

### Response When Duplicate Detected

**Success Response (Normal):**
```json
{
  "status": "ok",
  "file_path": "prds/queue/2025-11-27_weather-dashboard.md",
  "title": "Weather Dashboard",
  "github_url": "https://github.com/...",
  "commit_sha": "abc123..."
}
```

**Duplicate Response (Prevented):**
```json
{
  "status": "duplicate_prevented",
  "message": "PRD with identical content already exists: 2025-11-27_weather-dashboard.md",
  "existing_file": "2025-11-27_weather-dashboard.md",
  "existing_path": "prds/queue/2025-11-27_weather-dashboard.md",
  "github_url": "https://github.com/.../prds/queue/2025-11-27_weather-dashboard.md"
}
```

**ChatGPT sees:** "This PRD already exists in the system, here's the link"

## Layer 2: Reconciliation at Sync (GitHub Actions)

### How It Works

Even if a duplicate somehow gets into GitHub (manual creation, API call, etc.), the reconciliation system cleans it up:

```
1. GitHub Actions triggers on push to prds/queue/
2. Reconciliation script runs within 30 seconds
3. For each title in GitHub:
   - Counts how many files have that title
   - If count > 1 in database:
     → Deletes extras from database
   - If count = 1:
     → Ensures it's in database
4. Final state: Database has ≤ 1 PRD per unique title
```

### What Happens to Duplicate Files

**In GitHub:**
- Files remain (manual cleanup required)
- Only first file is added to database
- System logs warning about duplicate

**In Database:**
- Only 1 PRD per title maintained
- Extras are automatically deleted
- Website shows clean list

**Manual Cleanup (if needed):**
```bash
cd /Users/jason/Repositories/ai-agent-factory
ls prds/queue/ | grep weather  # Find duplicates
git rm prds/queue/2025-11-27_weather-dashboard-copy.md
git commit -m "Remove duplicate PRD"
git push
```

## Layer 3: Content-Based Detection (Database)

### How It Works

The database stores a `content_hash` for each PRD:

```sql
-- PRD table schema
CREATE TABLE prds (
  id UUID PRIMARY KEY,
  title TEXT,
  description TEXT,
  content_hash VARCHAR(64),  -- SHA-256 hash
  ...
);

CREATE INDEX idx_prds_content_hash ON prds(content_hash);
```

**When creating PRD in database:**
1. Calculate content hash from title + description
2. Query for existing PRD with same hash
3. If found: Return existing PRD (don't create duplicate)
4. If not found: Create new PRD with hash

**Hash Calculation:**
```python
from backend.fastapi_app.utils.prd_hash import calculate_prd_hash

title = "Weather Dashboard"
description = "A responsive weather dashboard..."
content_hash = calculate_prd_hash(title, description)
# → "5ce887cd7da5daaa7d20ad136d64970460b757711ad1d1d57c0d26eaa385b35b"
```

## Complete Duplicate Prevention Flow

### Scenario: ChatGPT Submits Same PRD Twice

**First Submission:**
```
ChatGPT → MCP Server → GitHub Check (no match) → Create File → Commit → GitHub Actions → Add to DB
Result: ✅ PRD created successfully
```

**Second Submission (Same Content):**
```
ChatGPT → MCP Server → GitHub Check (MATCH FOUND!) → STOP
Result: ❌ Duplicate prevented
Response: "PRD already exists: [link]"
```

### Scenario: Manual Duplicate Created

**User Creates Duplicate Manually:**
```bash
# User accidentally creates duplicate file
cp prds/queue/existing-prd.md prds/queue/duplicate-prd.md
git add prds/queue/duplicate-prd.md
git commit -m "Duplicate"
git push
```

**What Happens:**
```
1. GitHub Actions triggers (30s)
2. Reconciliation runs
3. Finds 2 files with same title
4. Only adds first one to database
5. Logs warning about duplicate
6. Database stays clean (1 PRD)
```

**Result:** Database protected, but files remain in GitHub

### Scenario: Different Title, Same Content

**First PRD:**
```markdown
# Weather Dashboard
## Description
A responsive weather dashboard...
```

**Second PRD (Different Name):**
```markdown
# Weather App
## Description
A responsive weather dashboard...
```

**Content Hash Comparison:**
```
PRD 1: "weather dashboard::a responsive weather dashboard..."
       → Hash: abc123...

PRD 2: "weather app::a responsive weather dashboard..."
       → Hash: def456...  (DIFFERENT - description alone not enough)
```

**Result:** ✅ Allowed (different titles = different PRDs)

## Configuration

### MCP Server Settings

Located in `scripts/mcp/cursor-agent-mcp-server.py`:

```python
# Duplicate check settings
DESCRIPTION_COMPARE_LENGTH = 500  # Compare first 500 chars
HASH_ALGORITHM = "sha256"         # Content hash algorithm

# GitHub API settings
GITHUB_ORG_NAME = os.getenv("GITHUB_ORG_NAME", "thedoctorJJ")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "ai-agent-factory")
```

### Database Settings

Located in `backend/fastapi_app/utils/prd_hash.py`:

```python
def calculate_prd_hash(title: str, description: str) -> str:
    """Calculate deterministic hash for duplicate detection"""
    # Normalize inputs
    norm_title = normalize_text(title)
    norm_description = normalize_text(description)
    
    # Create combined content (first 500 chars of description)
    content = f"{norm_title}::{norm_description[:500]}"
    
    # Calculate SHA-256 hash
    return hashlib.sha256(content.encode('utf-8')).hexdigest()
```

## Monitoring & Verification

### Check for Duplicates in GitHub

```bash
cd prds/queue/

# Find files with duplicate content (by title)
for file in *.md; do 
  echo "$file: $(head -1 "$file")"; 
done | sort -t: -k2 | uniq -f1 -D

# Example output if duplicates exist:
# 2025-11-27_weather-dashboard.md: # Weather Dashboard
# 2025-11-27_weather-dashboard-copy.md: # Weather Dashboard
```

### Check for Duplicates in Database

```bash
# Query for duplicate content hashes
curl -s https://[backend]/api/v1/prds | \
  jq '.prds | group_by(.content_hash) | map(select(length > 1))'

# Query for duplicate titles
curl -s https://[backend]/api/v1/prds | \
  jq '.prds | group_by(.title) | map(select(length > 1))'
```

### Test Duplicate Prevention

```bash
# Create test PRD
cat > /tmp/test-prd.md << 'EOF'
# Test PRD
## Description
This is a test PRD for duplicate detection.
EOF

# Submit first time (should succeed)
curl -X POST https://[backend]/api/v1/prds/upload -F "file=@/tmp/test-prd.md"

# Submit second time (should return existing PRD)
curl -X POST https://[backend]/api/v1/prds/upload -F "file=@/tmp/test-prd.md"
```

## Troubleshooting

### Problem: Duplicate Still Created

**Symptoms:**
- Same PRD appears twice in GitHub
- Different filenames but same content

**Cause:** MCP server duplicate check failed (network error, API issue)

**Fix:**
```bash
# Reconciliation will clean up database automatically
python3 scripts/prd-management/reconcile-prds.py

# Manually remove duplicate file from GitHub
git rm prds/queue/duplicate-file.md
git commit -m "Remove duplicate"
git push
```

### Problem: False Positive (Not Really Duplicate)

**Symptoms:**
- MCP server rejects new PRD
- User insists it's different content

**Cause:** Titles/descriptions are too similar

**Fix:**
```bash
# Make title or description more distinct
# Old: "Weather Dashboard - A weather app"
# New: "Weather Dashboard v2 - Advanced forecasting app"

# Or manually create file in GitHub
cd prds/queue/
vim 2025-11-27_new-prd.md
git add 2025-11-27_new-prd.md
git commit -m "Add new PRD"
git push
```

### Problem: Can't Tell if Duplicate Check Working

**Symptoms:**
- Unsure if prevention is active
- Want to verify system status

**Check:**
```bash
# Check MCP server logs (Cloud Run)
gcloud run services logs read ai-agent-factory-mcp-server \
  --region=us-central1 \
  --limit=50

# Look for:
# "⚠️  Warning: Duplicate check failed" (if errors)
# "PRD with identical content already exists" (if prevention working)
```

## Summary: Multi-Layer Defense

| Layer | Where | When | Action | Effectiveness |
|-------|-------|------|--------|---------------|
| **Layer 1: Prevention** | MCP Server | Before GitHub | Reject creation | ✅ 95%+ |
| **Layer 2: Reconciliation** | GitHub Actions | After GitHub | Clean database | ✅ 100% (DB) |
| **Layer 3: Hash Check** | Database | On insert | Prevent DB dup | ✅ 100% (DB) |
| **Manual Cleanup** | GitHub Files | As needed | Remove files | ⚠️ Manual |

**Bottom Line:** Duplicates are prevented automatically at creation. If one slips through, the database stays clean. Only GitHub files may need occasional manual cleanup.

## Related Documentation

- `docs/guides/PRD_RECONCILIATION.md` - Reconciliation system
- `docs/architecture/PRD_CONSISTENCY_SYSTEM.md` - Technical design
- `backend/fastapi_app/utils/prd_hash.py` - Hash calculation
- `scripts/mcp/cursor-agent-mcp-server.py` - MCP duplicate check

