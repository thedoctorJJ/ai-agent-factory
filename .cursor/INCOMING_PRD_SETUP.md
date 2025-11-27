# Incoming PRD Setup - Complete ✅

## 🎉 What Was Set Up

I've created a complete system for automatically processing PRDs from any AI tool (ChatGPT, Gemini, Claude) or manual creation.

## 📁 Folder Structure

**Created**: `prds/incoming/` folder
- This is where you (or AI tools) save PRD files
- Files are automatically detected and processed
- Processed files are moved to `prds/uploaded/`

## 🔧 Components Created

### 1. **File Watcher Script** ✅
**Location**: `scripts/prd-management/watch-incoming-prds.py`

**What it does**:
- Monitors `prds/incoming/` for new `.md` files
- Automatically uploads PRDs to the backend
- Moves processed files to `prds/uploaded/`
- Shows real-time status

**How to use**:
```bash
# Start the file watcher
python3 scripts/prd-management/watch-incoming-prds.py
```

### 2. **Manual Processing Script** ✅
**Location**: `scripts/prd-management/process-incoming-prds.sh`

**What it does**:
- Processes all files in `prds/incoming/` folder
- Useful if watcher isn't running
- Uploads and moves files automatically

**How to use**:
```bash
./scripts/prd-management/process-incoming-prds.sh
```

### 3. **Webhook API Endpoint** ✅
**Location**: `backend/fastapi_app/routers/prds.py`

**Endpoint**: `POST /api/v1/prds/incoming`

**Supports**:
- JSON body (for AI tools with API access)
- File upload (multipart/form-data)
- Form data (for simple webhooks)

**Example**:
```bash
curl -X POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming \
  -H "Content-Type: application/json" \
  -d '{"content": "# PRD Title\n\n## Description\n..."}'
```

### 4. **Documentation** ✅
- `prds/incoming/README.md` - User guide
- `prds/incoming/INSTRUCTIONS_FOR_AI_TOOLS.md` - Instructions for AI tools
- `docs/guides/INCOMING_PRD_WORKFLOW.md` - Complete workflow guide

## 🚀 How to Use

### Option 1: File Folder (Recommended)

1. **Start the file watcher** (in a terminal):
   ```bash
   python3 scripts/prd-management/watch-incoming-prds.py
   ```

2. **Tell ChatGPT (or any AI tool)**:
   ```
   When creating a PRD, save it to:
   /Users/jason/Repositories/ai-agent-factory/prds/incoming/
   
   File naming: YYYY-MM-DD_prd-title.md
   ```

3. **Create PRD**: Ask ChatGPT to create a PRD and save it to that folder

4. **Automatic Processing**: The watcher will automatically:
   - Detect the new file
   - Upload it to the system
   - Move it to `prds/uploaded/`
   - Show status in the terminal

### Option 2: API Webhook

If your AI tool supports API calls, use the webhook endpoint:

```
POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
Content-Type: application/json

{
  "content": "# Your PRD markdown content here..."
}
```

## 📋 Example ChatGPT Prompt

```
Create a PRD for a user authentication system and save it to:
/Users/jason/Repositories/ai-agent-factory/prds/incoming/2025-11-16_user-authentication-system.md

The PRD should include:
- Title
- Description
- Requirements
- Technical requirements
- Success metrics
```

## ✅ Testing

To test the setup:

1. **Start the watcher**:
   ```bash
   python3 scripts/prd-management/watch-incoming-prds.py
   ```

2. **Create a test PRD file**:
   ```bash
   echo "# Test PRD\n\n## Description\nThis is a test PRD" > prds/incoming/2025-11-16_test-prd.md
   ```

3. **Watch it process**: The watcher should detect and process it automatically

## 📚 Documentation

- **Quick Start**: `prds/incoming/README.md`
- **AI Tool Instructions**: `prds/incoming/INSTRUCTIONS_FOR_AI_TOOLS.md`
- **Complete Guide**: `docs/guides/INCOMING_PRD_WORKFLOW.md`

## 🎯 Next Steps

1. **Start the file watcher** (if you want automatic processing)
2. **Share the folder path with ChatGPT**: `/Users/jason/Repositories/ai-agent-factory/prds/incoming/`
3. **Create PRDs** and they'll be automatically processed!

## ⚠️ Important Notes

- The file watcher must be running for automatic processing
- If watcher isn't running, use `process-incoming-prds.sh` to process manually
- Files are moved to `prds/uploaded/` after successful processing
- Duplicate PRDs (by title) are automatically detected and skipped

---

**Status**: ✅ **SETUP COMPLETE** - Ready to use!



