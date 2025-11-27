# Incoming PRDs - Cloud-Based Submission

**⚠️ IMPORTANT**: This folder is for local development only. For cloud-based PRD submission, use the API endpoint directly.

## 🌐 Cloud-Based Submission (Recommended)

### Use the Webhook API Endpoint

Submit PRDs directly to the cloud via API - no local files needed!

**Endpoint**: 
```
POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
```

See `docs/guides/INCOMING_PRD_WORKFLOW.md` for complete instructions.

## 📋 Local Development (Optional)

If you're running locally and want to test with files:

1. Save PRD as `.md` file in this folder
2. Run the file watcher: `python3 scripts/prd-management/watch-incoming-prds.py`
3. Files will be processed and moved to `prds/uploaded/`

## 📝 File Naming

**Recommended format**: `YYYY-MM-DD_prd-title.md`

Examples:
- `2025-11-16_user-authentication-system.md`
- `2025-11-16_api-rate-limiting.md`
- `2025-11-16_database-backup-service.md`

## ✅ What Happens Automatically

1. **File Detection**: The watcher detects new `.md` files
2. **PRD Parsing**: The system parses the PRD content
3. **Database Upload**: PRD is uploaded to the database
4. **File Organization**: Processed file is moved to `prds/uploaded/`
5. **Status Update**: PRD status is set to `uploaded`

## 🔧 Manual Processing

If automatic processing isn't working, you can manually process files:

```bash
# Process all files in incoming folder
./scripts/prd-management/process-incoming-prds.sh

# Process a specific file
python3 scripts/prd-management/process-incoming-prd.py prds/incoming/my-prd.md
```

## 📚 PRD Format

Your PRD should follow the standard PRD template format. See `prds/templates/` for examples:
- `prd-template-agent.md` - For AI agent PRDs
- `prd-template-platform.md` - For platform feature PRDs

## ⚠️ Important Notes

- Only `.md` files are processed
- Files are moved after successful processing
- Duplicate PRDs (by title) are detected and skipped
- Processing happens automatically via file watcher (if running)

