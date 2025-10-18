# PRD Organization System

This directory contains Product Requirements Documents (PRDs) organized by their processing status, mirroring the database workflow.

## 📁 Folder Structure

### `uploaded/`
PRDs that have been uploaded by users but need standardization.
- **Status**: `uploaded`
- **Action**: Awaiting standardization to AI Agent Factory format
- **Next Step**: Will be converted using appropriate template (agent or platform)

### `standardizing/`
PRDs that are currently being converted to match AI Agent Factory standards.
- **Status**: `standardizing`
- **Action**: Being standardized using templates
- **Next Step**: Will move to `review/` when standardization is complete

### `review/`
PRDs that have been standardized and are awaiting user review and approval.
- **Status**: `review`
- **Action**: Awaiting user review and sign-off
- **Next Step**: Will move to `queue/` when approved, or back to `standardizing/` if changes needed

### `queue/`
PRDs that are standardized, reviewed, and approved - ready for processing.
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
Template PRDs for creating new requirements documents and standardizing uploaded PRDs.
- **Status**: N/A (templates)
- **Action**: Reference documents for PRD creation and standardization
- **Next Step**: Used by system to convert uploaded PRDs to AI Agent Factory format

## 🔄 Standardization Process

### **What Gets Standardized**
- **Structure**: Ensures all PRDs follow the same comprehensive format
- **Technical Requirements**: Adds AI Agent Factory infrastructure details (FastAPI, Supabase, Google Cloud Run, etc.)
- **Integration Details**: Includes MCP protocol, GitHub, and platform integration requirements
- **Security & Deployment**: Adds standardized security and deployment specifications
- **Monitoring**: Includes built-in health checks and performance metrics

### **Template Selection**
- **Agent PRDs**: Uses `prd-template-agent.md` for individual AI agent creation
- **Platform PRDs**: Uses `prd-template-platform.md` for platform features and infrastructure

### **Standardization Benefits**
- **Consistency**: All PRDs follow the same structure and include required technical details
- **Completeness**: Ensures no critical information is missing
- **Integration Ready**: PRDs are pre-configured for AI Agent Factory infrastructure
- **Processing Efficiency**: Devin AI can process standardized PRDs more effectively

## 🔄 Workflow

```
uploaded/ → standardizing/ → review/ → queue/ → in-progress/ → completed/ (or failed/)
                ↓              ↓                              ↓
            archive/      standardizing/ (if changes)    archive/
```

### **Complete Process**
1. **Upload**: User uploads PRD (any format) to `uploaded/`
2. **Classification**: System determines if it's an agent or platform PRD
3. **Standardization**: PRD is converted using appropriate template to match AI Agent Factory standards
4. **Review**: User reviews standardized PRD and approves or requests changes
5. **Queue**: Approved PRD moves to `queue/` for processing
6. **Processing**: Devin AI creates agent/feature from standardized PRD
7. **Completion**: PRD moves to `completed/` or `failed/`

## 📋 Usage Guidelines

1. **Upload PRDs**: Users upload PRDs (any format) to `uploaded/` folder
2. **Standardization**: System automatically converts PRDs to AI Agent Factory format
3. **Review**: Users review standardized PRDs and approve or request changes
4. **Queue**: Approved PRDs move to `queue/` folder
5. **Processing**: System automatically moves to `in-progress/`
6. **Completion**: System moves to `completed/` or `failed/`
7. **Archival**: Move old PRDs to `archive/` for long-term storage

## 👥 User Review Process

### **What Users Review**
- **Content Accuracy**: Ensure original intent is preserved
- **Technical Additions**: Review added infrastructure and integration details
- **Structure Changes**: Verify the standardized format meets their needs
- **Completeness**: Confirm all required sections are properly filled

### **Review Actions**
- **Approve**: Move PRD to `queue/` for processing
- **Request Changes**: Move PRD back to `standardizing/` with feedback
- **Reject**: Move PRD to `archive/` if not suitable

### **Review Benefits**
- **Quality Control**: Ensures PRDs meet user expectations
- **Transparency**: Users see exactly what will be processed
- **Collaboration**: Allows for iterative improvement
- **Confidence**: Users can proceed knowing the PRD is correct

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
