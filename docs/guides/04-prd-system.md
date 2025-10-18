# PRD System Guide

## 📋 **Document Summary**

This document explains the PRD (Product Requirements Document) system designed to receive completed, formatted PRDs and process them for agent creation, covering available templates (basic, comprehensive, agent-specific, platform-specific), the complete PRD processing workflow from upload through validation, storage, and processing, the status system with lifecycle management, PRD organization structure, automated parsing features that extract 22+ fields from templates, completion tracking and quality analysis, the PRD management interface with dashboard features, API endpoints for PRD operations, testing procedures with sample PRDs, and best practices for PRD creation, processing, and management.

---

## 🎯 **PRD System Overview**

The AI Agent Factory PRD (Product Requirements Document) system is designed to receive completed, formatted PRDs and process them for agent creation. The system does NOT handle voice input or PRD creation - it focuses on processing completed PRDs.

## 📋 **PRD Templates**

### **Available Templates**
- **`prd-template-agent.md`** - AI Agent PRD template with full technical infrastructure integration
- **`prd-template-platform.md`** - Platform PRD template for infrastructure and platform features

Both templates are pre-configured to leverage the AI Agent Factory's technical infrastructure including FastAPI, Supabase, Google Cloud Run, MCP protocol, and GitHub integration.

## 🏗️ **Repository Strategy**

The AI Agent Factory uses a hybrid repository strategy based on PRD type:

### **Platform PRDs**
- **Purpose**: Infrastructure, platform features, and system components
- **Repository**: Main repository (`ai-agent-factory`)
- **Location**: `/agents/{agent-name}/` folder
- **Benefits**: 
  - Centralized management of platform components
  - Easy access to shared infrastructure
  - Simplified deployment and maintenance

### **Agent PRDs**
- **Purpose**: Individual AI agents and specialized applications
- **Repository**: Separate GitHub repositories
- **Naming**: `ai-agents-{agent-name}`
- **Benefits**:
  - Full isolation and independence
  - Individual versioning and release cycles
  - Dedicated CI/CD pipelines
  - Scalable agent ecosystem

### **Automatic Detection**
The system automatically determines the appropriate repository strategy based on:
- PRD content analysis
- Keyword detection (platform vs agent indicators)
- Explicit PRD type specification
- Template selection

### **PRD Sections**
#### **Core Sections**
- **Title** - Project name and description
- **Description** - High-level project overview
- **Problem Statement** - What problem does this solve?
- **Target Users** - Who will use this?
- **User Stories** - Specific user scenarios
- **Requirements** - Functional and non-functional requirements
- **Acceptance Criteria** - How do we know it's done?
- **Technical Requirements** - Technical specifications
- **Success Metrics** - How do we measure success?
- **Timeline** - Project timeline and milestones

#### **Optional Sections**
- **Performance Requirements** - Performance specifications
- **Security Requirements** - Security considerations
- **Integration Requirements** - Third-party integrations
- **Deployment Requirements** - Deployment specifications
- **Dependencies** - External dependencies
- **Risks** - Potential risks and mitigation
- **Assumptions** - Project assumptions

## 🔄 **PRD Processing Workflow**

### **1. PRD Upload**
- **Upload** - Users upload PRDs in any format to the `uploaded/` folder
- **Classification** - System determines if it's an agent or platform PRD
- **Repository Strategy** - System automatically determines repository approach:
  - **Platform PRDs**: Agents added to main repository (`/agents/` folder)
  - **Agent PRDs**: Separate GitHub repositories created (`ai-agents-{name}`)
- **Initial Processing** - PRD is prepared for standardization

### **2. PRD Standardization**
- **Template Selection** - System chooses appropriate template (agent or platform)
- **Content Mapping** - User content is mapped to template structure
- **Infrastructure Addition** - Technical requirements are added from templates
- **Validation** - Standardized PRD is validated for completeness

### **3. User Review**
- **Review Process** - Users review standardized PRDs and approve or request changes
- **Approval Actions**:
  - **Approve** - Move PRD to queue for processing
  - **Request Changes** - Send feedback and move back to standardizing
  - **Reject** - Remove PRD from workflow

### **4. PRD Processing**
- **Queue Management** - Approved PRDs move to processing queue
- **Devin Integration** - Devin AI processes PRDs into AI agents
- **Deployment** - Agents are deployed to Google Cloud Run
- **Registration** - Agents are registered with the platform

## 📊 **PRD Status System**

### **Status Types**
- **`uploaded`** - PRD uploaded and awaiting standardization
- **`standardizing`** - PRD being converted to AI Agent Factory format
- **`review`** - PRD awaiting user review and approval
- **`queue`** - PRD approved and waiting for processing
- **`in_progress`** - PRD being processed by Devin AI
- **`completed`** - PRD successfully processed and agent deployed
- **`failed`** - PRD processing failed

### **Status Transitions**
```
uploaded → standardizing → review → queue → in_progress → completed
    ↓           ↓            ↓        ↓         ↓
archive/   standardizing/  archive/  failed ←──┘
           (if changes)
```

## 🗂️ **PRD Organization**

### **Directory Structure**
```
prds/
├── uploaded/                # PRDs uploaded by users (any format)
├── standardizing/           # PRDs being converted to AI Agent Factory format
├── review/                  # PRDs awaiting user review and approval
├── queue/                   # PRDs approved and waiting for processing
├── in-progress/             # PRDs currently being processed
├── completed/               # Successfully completed PRDs
├── failed/                  # PRDs that failed processing
├── archive/                 # Archived PRDs
└── templates/               # PRD templates
```

### **File Naming Convention**
- **Format**: `YYYY-MM-DD_prd-title.md`
- **Example**: `2024-01-15_database-integration-supabase.md`

## 🔧 **PRD Processing Features**

### **Automated Parsing**
- **Field Extraction** - Automatically extracts all 22+ fields from PRD templates
- **Data Validation** - Validates extracted data for completeness and accuracy
- **Template Recognition** - Recognizes different PRD template types
- **Content Analysis** - Analyzes PRD content for quality and completeness

### **Completion Tracking**
- **Completeness Score** - Calculates percentage of completed sections
- **Missing Sections** - Identifies missing or incomplete sections
- **Quality Metrics** - Provides quality assessment of PRD content
- **Improvement Suggestions** - Suggests specific improvements

### **Markdown Export**
- **Professional Formatting** - Exports PRDs in professional markdown format
- **Template Compliance** - Ensures exported PRDs follow template standards
- **Devin-Ready Format** - Optimizes PRDs for Devin AI processing
- **Download Support** - One-click download of formatted PRDs

## 📱 **PRD Management Interface**

### **Dashboard Features**
- **PRD Repository** - Organized view of all PRDs
- **Status Filtering** - Filter PRDs by status
- **Search Functionality** - Search PRDs by title, description, or content
- **Bulk Operations** - Perform operations on multiple PRDs

### **PRD Cards**
- **Status Indicators** - Visual status indicators with color coding
- **Completion Progress** - Progress bars showing completion percentage
- **Quick Actions** - Quick access to view, edit, or process PRDs
- **Metadata Display** - Show creation date, last modified, and other metadata

### **PRD Creation Form**
- **Template Selection** - Choose from available PRD templates
- **Guided Completion** - Step-by-step PRD completion assistance
- **Real-time Validation** - Immediate feedback on form completion
- **Auto-save** - Automatic saving of form progress

## 🔗 **API Endpoints**

### **PRD Management**
- `POST /api/v1/prds` - Create new PRD
- `GET /api/v1/prds` - List all PRDs with filtering
- `GET /api/v1/prds/{prd_id}` - Get specific PRD
- `PUT /api/v1/prds/{prd_id}` - Update PRD
- `DELETE /api/v1/prds/{prd_id}` - Delete PRD
- `DELETE /api/v1/prds` - Delete all PRDs

### **File Upload**
- `POST /api/v1/prds/upload` - Upload PRD markdown file

### **PRD Processing**
- `POST /api/v1/prds/{prd_id}/ready-for-devin` - Mark PRD as ready for Devin AI
- `GET /api/v1/prds/ready-for-devin` - Get PRDs ready for Devin AI processing
- `GET /api/v1/prds/{prd_id}/markdown` - Export PRD as markdown
- `GET /api/v1/prds/{prd_id}/markdown/download` - Download PRD as .md file

### **Roadmap & Analytics**
- `GET /api/v1/roadmap/categories` - Get available categories
- `GET /api/v1/roadmap/statuses` - Get available statuses
- `GET /api/v1/roadmap/priorities` - Get available priorities
- `GET /api/v1/roadmap` - Get roadmap data with filtering

## 🧪 **Testing the PRD System**

### **Sample PRDs**
Run the sample PRD creation script to populate the system:
```bash
python scripts/create-sample-prds.py
```

This creates 9 comprehensive PRDs covering:
- Infrastructure improvements
- Feature enhancements
- Platform optimizations
- Agent development projects

### **PRD Validation Testing**
```bash
# Test PRD parsing and validation
./scripts/testing/test-comprehensive-prd-parsing.py
```

### **Manual Testing Workflow**
1. **Upload PRD** - Upload a completed PRD using the dashboard
2. **Validate Structure** - Check that all fields are extracted correctly
3. **Review Analysis** - Review the PRD quality analysis
4. **Mark Ready** - Mark PRD as ready for Devin AI processing
5. **Export Markdown** - Test markdown export functionality

## 🎯 **Best Practices**

### **PRD Creation**
- **Use Templates** - Always start with the appropriate template
- **Complete Sections** - Fill out all relevant sections thoroughly
- **Be Specific** - Provide specific, actionable requirements
- **Include Examples** - Add examples and use cases where helpful

### **PRD Processing**
- **Validate Early** - Validate PRD structure before processing
- **Review Analysis** - Review quality analysis and address issues
- **Test Export** - Test markdown export before marking ready
- **Monitor Status** - Keep track of PRD processing status

### **PRD Management**
- **Organize by Status** - Use the directory structure to organize PRDs
- **Regular Cleanup** - Archive completed PRDs regularly
- **Backup Important PRDs** - Keep backups of critical PRDs
- **Document Changes** - Document any changes to PRD templates

## 🚀 **Advanced Features**

### **PRD Analytics**
- **Completion Trends** - Track PRD completion trends over time
- **Quality Metrics** - Monitor PRD quality metrics
- **Processing Statistics** - View PRD processing statistics
- **Performance Analysis** - Analyze PRD processing performance

### **Integration Features**
- **Devin AI Integration** - Seamless integration with Devin AI processing
- **GitHub Integration** - Link PRDs to GitHub repositories
- **Notification System** - Get notified of PRD status changes
- **Collaboration Tools** - Share and collaborate on PRDs

## 📚 **Documentation**

### **PRD Templates**
- **Template Guide** - Comprehensive guide to using PRD templates
- **Field Reference** - Complete reference of all PRD fields
- **Examples** - Example PRDs for different use cases
- **Best Practices** - Best practices for PRD creation

### **API Documentation**
- **Endpoint Reference** - Complete API endpoint reference
- **Request/Response Examples** - Example requests and responses
- **Error Handling** - Error codes and handling
- **Authentication** - API authentication and authorization

The PRD system provides a comprehensive solution for managing Product Requirements Documents from creation to agent deployment, with robust validation, processing, and integration capabilities.
