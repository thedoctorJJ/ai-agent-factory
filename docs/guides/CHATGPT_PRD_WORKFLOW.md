# ChatGPT PRD Submission Workflow

**Date**: November 27, 2025  
**Status**: ✅ **IMPLEMENTED** - GitHub-based cloud source of truth  

---

## 🎯 Overview

ChatGPT can now submit PRDs directly to the AI Agent Factory via MCP connector. PRDs are committed to GitHub (cloud source of truth) and then synced locally and to the database.

---

## 📋 Workflow

### **PRD Submission Flow:**

```
ChatGPT 
  ↓
MCP Server (Cloud Run)
  ↓
GitHub Commit (prds/queue/) ✅ CLOUD SOURCE OF TRUTH
  ↓
Local: git pull
  ↓
Automatic Sync Script
  ↓
Database
```

---

## 🔄 Step-by-Step Process

### **Step 1: Submit PRD from ChatGPT**

In ChatGPT, use the `submit_prd_from_conversation` action:

```
Please create a PRD for [feature description]
```

ChatGPT will:
1. Format the conversation as a PRD
2. Call the MCP server
3. MCP server commits to GitHub
4. Returns success confirmation

**Response:**
```json
{
  "status": "ok",
  "file_path": "prds/queue/2025-11-27_feature-name.md",
  "title": "Feature Name",
  "github_url": "https://github.com/thedoctorJJ/ai-agent-factory/blob/main/prds/queue/...",
  "commit_sha": "abc123...",
  "message": "PRD committed to GitHub. Run 'git pull' and sync to database."
}
```

### **Step 2: Pull from GitHub (Local)**

```bash
cd /Users/jason/Repositories/ai-agent-factory
git pull origin main
```

This brings the new PRD file into your local `prds/queue/` folder.

### **Step 3: Sync to Database**

```bash
./scripts/prd-management/sync-prds-to-database.sh
```

This syncs all PRD files from `prds/queue/` to the database.

### **Step 4: Verify**

```bash
# Check database
curl -s https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds | jq '.total'

# Check local files
ls -1 prds/queue/*.md | wc -l
```

---

## ✅ Benefits

### **Cloud Source of Truth**
- ✅ PRDs stored in GitHub (persistent)
- ✅ Survives database wipes
- ✅ Version controlled
- ✅ Accessible from any machine

### **Consistent Workflow**
- ✅ All PRDs go through same path (files → database)
- ✅ Single source of truth maintained
- ✅ No database-only PRDs

### **Automatic Syncing**
- ✅ GitHub Actions can auto-sync on push
- ✅ Git hooks can trigger local sync
- ✅ Manual sync always available

---

## 🔧 Configuration

### **Environment Variables**

The MCP server requires:

```bash
GITHUB_TOKEN=ghp_your_token_here
GITHUB_ORG_NAME=thedoctorJJ
GITHUB_REPO_NAME=ai-agent-factory
```

### **GitHub Permissions**

The GitHub token needs:
- `repo` scope (full control of private repositories)
- `contents` write permission

---

## 🚨 Important Notes

### **Source of Truth**
- **GitHub** is the cloud source of truth
- **Local files** (`prds/queue/`) are synced from GitHub
- **Database** is synced from local files

### **Sync Order**
```
GitHub → Local Files → Database
```

### **Never Skip Steps**
- Always `git pull` after ChatGPT submission
- Always run sync script after `git pull`
- Database is always last in the chain

---

## 🛠️ Troubleshooting

### **Problem: PRD not showing in database**

**Solution:**
```bash
# 1. Pull from GitHub
git pull origin main

# 2. Check file exists
ls -la prds/queue/2025-11-27_*.md

# 3. Sync to database
./scripts/prd-management/sync-prds-to-database.sh

# 4. Verify
curl -s https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds | jq '.total'
```

### **Problem: GitHub commit failed**

**Check:**
1. GitHub token is valid: `echo $GITHUB_TOKEN`
2. Token has `repo` permissions
3. Repository exists and is accessible
4. MCP server logs for detailed error

### **Problem: File conflicts**

If a file with the same name exists, the MCP server automatically adds a timestamp:
```
2025-11-27_feature-name.md
2025-11-27_feature-name-143052.md  ← Timestamp added
```

---

## 📊 Monitoring

### **Check GitHub Commits**

```bash
# View recent PRD commits
git log --oneline --follow prds/queue/
```

### **Check MCP Server Logs**

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ai-agent-factory-mcp-server" --limit 20 --project agent-factory-474201
```

---

## 🔗 Related Documentation

- `docs/guides/PRD_SYNC_STRATEGY.md` - Overall PRD sync strategy
- `docs/troubleshooting/file-based-prd-system.md` - File-based system details
- `scripts/mcp/cursor-agent-mcp-server.py` - MCP server implementation

---

**Last Updated**: November 27, 2025

