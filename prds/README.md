# PRD Organization System

This directory contains Product Requirements Documents (PRDs) organized by their processing status, mirroring the database workflow.

## 📁 Folder Structure

### `queue/`
PRDs that are waiting to be processed by the AI Agent Factory.
- **Status**: `queue`
- **Action**: Ready for agent creation workflow
- **Next Step**: Will be picked up by Devin AI for processing

### `in-progress/`
PRDs that are currently being processed by Devin AI.
- **Status**: `in_progress` 
- **Action**: Being worked on by Devin AI
- **Next Step**: Will move to `completed/` or `failed/` when done

### `completed/`
PRDs that have been successfully processed and agents have been created.
- **Status**: `completed`
- **Action**: Agent creation workflow finished successfully
- **Next Step**: Agents are deployed and operational

### `failed/`
PRDs that failed during the agent creation process.
- **Status**: `failed`
- **Action**: Processing failed, needs review
- **Next Step**: Review error logs and retry or fix issues

### `archive/`
Historical PRDs that are no longer active.
- **Status**: Various (completed, cancelled, etc.)
- **Action**: Long-term storage for reference
- **Next Step**: Used for historical analysis and reference

### `templates/`
Template PRDs for creating new requirements documents.
- **Status**: N/A (templates)
- **Action**: Reference documents for PRD creation
- **Next Step**: Copy and customize for new PRDs

## 🔄 Workflow

```
queue/ → in-progress/ → completed/ (or failed/)
                ↓
            archive/
```

## 📋 Usage Guidelines

1. **New PRDs**: Place in `queue/` folder
2. **Processing**: System automatically moves to `in-progress/`
3. **Completion**: System moves to `completed/` or `failed/`
4. **Archival**: Move old PRDs to `archive/` for long-term storage

## 🗄️ Database Sync

This file organization mirrors the database statuses:
- File system provides easy browsing and management
- Database provides structured data and API access
- Both systems stay synchronized through the application

## 📝 File Naming Convention

Use descriptive filenames with timestamps:
```
YYYY-MM-DD_prd-title-description.md
```

Example:
```
2024-01-15_database-integration-supabase.md
2024-01-16_user-authentication-system.md
```

## 🔧 Management Scripts

Use the provided scripts in `scripts/prd-management/` for:
- Moving PRDs between folders
- Syncing with database
- Bulk operations
- Status updates
