# Changelog

All notable changes to the AI Agent Factory project will be documented in this file.

## [Unreleased] - 2025-11-16

### 🐛 **Redis Agent Registration Fix - Resolved**
- **✅ Issue**: Redis agent registration failing with 500 Internal Server Error
- **✅ Root Cause**: Multiple issues - duplicate agent handling, Supabase project paused, incorrect PRD ID
- **✅ Fix**: 
  - Added duplicate agent detection - now updates existing agents instead of failing
  - Enhanced error handling with retry logic and exponential backoff
  - Improved DNS/network error detection and reporting
  - Fixed PRD ID in registration script
  - Added `get_agent_by_name()` method for agent lookup
- **✅ Impact**: Redis agent successfully registered, all systems operational
- **Status**: Fully resolved and deployed to production
- **Documentation**: See `docs/resolution-summaries/redis-agent-registration-fix-resolution-2025-11-16.md`

### **Technical Details**
- **Files**: 
  - `backend/fastapi_app/services/agent_service.py` - Added duplicate agent handling
  - `backend/fastapi_app/utils/simple_data_manager.py` - Added retry logic and `get_agent_by_name()`
  - `scripts/register-redis-agent-production.py` - Fixed PRD ID
- **Changes**: 
  - Check for existing agents by name before creating
  - Update existing agents instead of failing on duplicates
  - Retry logic with exponential backoff for network operations
  - Better error messages for DNS/network issues
- **Testing**: Agent registration now works correctly
- **Deployment**: Revision `ai-agent-factory-backend-00035-lmb` deployed successfully

### 🐛 **Agents Endpoint 500 Error - Fixed (Regression)**
- **✅ Issue**: `/api/v1/agents` endpoint returning 500 Internal Server Error (regression from Nov 13 fix)
- **✅ Root Cause**: Insufficient error handling when creating `AgentResponse` objects from database records
- **✅ Fix**: Added comprehensive error handling, field validation, and type checking in `get_agents()` method
- **✅ Impact**: Endpoint now gracefully handles database errors, missing fields, and malformed records
- **Status**: Code fix completed and deployed to production
- **Documentation**: See `docs/resolution-summaries/agents-endpoint-500-error-resolution-nov-16-2025.md`

### **Technical Details**
- **Files**: 
  - `backend/fastapi_app/services/agent_service.py` - Updated `get_agents()` with comprehensive error handling
- **Changes**: 
  - Added try-catch around data fetching from database
  - Added validation for required fields with safe defaults
  - Added type validation for list/dict fields
  - Separated `AgentResponse` creation with individual error handling
  - Added traceback logging for debugging
- **Testing**: Endpoint now returns 200 OK with proper JSON response
- **Deployment**: Revision `ai-agent-factory-backend-00034-7b6` deployed successfully

### 🐛 **Health Check Environment Variable Detection - Fixed**
- **✅ Issue**: Health check endpoints showing environment variables as "missing" in production despite services functioning correctly
- **✅ Root Cause**: Health check using `os.getenv()` directly instead of config object, which may not detect variables set via Cloud Run environment variables or Cloud Secrets Manager
- **✅ Fix**: Updated health check endpoints to use config object for configuration detection, ensuring consistency with how the application loads configuration
- **✅ Impact**: Health checks now accurately reflect actual application configuration status
- **Status**: Code fix completed, pending production deployment
- **Documentation**: See `docs/troubleshooting/health-check-environment-variables.md`

### **Technical Details**
- **Files**: 
  - `backend/fastapi_app/routers/health.py` - Updated `detailed_health_check()` to use config object
  - `backend/fastapi_app/config.py` - Updated `validate_config()` to use config properties
- **Changes**: 
  - Health check now checks `config.supabase_url`, `config.openai_api_key`, etc. instead of `os.getenv()` directly
  - Ensures detection works regardless of configuration source (env vars, Cloud Run vars, secrets)
- **Testing**: Health checks now accurately detect configuration in production environments

## [Unreleased] - 2025-11-13

### 📋 **API Contract Specification System - Added**
- **✅ OpenAPI 3.1 Specification**: Complete API contract with 28 endpoints and 28 schemas
- **✅ TypeScript Type Generation**: Automated type generation from OpenAPI spec
- **✅ Contract Validation**: Scripts to validate API contract and endpoints
- **✅ CI/CD Integration**: GitHub Actions workflow for automated contract validation
- **✅ Documentation**: Comprehensive API contract documentation and guides
- **Status**: API contract system fully operational and integrated

### **Technical Details**
- **Files**: `api-spec/openapi.json`, `api-spec/openapi.yaml` - OpenAPI 3.1 specifications
- **Scripts**: `scripts/api/generate-openapi-spec.py`, `scripts/api/generate-typescript-types.sh`, `scripts/api/validate-api-contract.sh`
- **Documentation**: `docs/api/API_CONTRACT.md` - Complete API contract guide
- **CI/CD**: `.github/workflows/api-contract.yml` - Automated validation workflow
- **Impact**: Type-safe frontend integration with automatic type generation
- **Testing**: Contract validation passes for all endpoints

### 🐛 **Agents Endpoint Internal Server Error - Fixed**
- **✅ Issue**: `/api/v1/agents` endpoint returning 500 Internal Server Error
- **✅ Root Cause**: Missing datetime conversion and enum validation in `get_agents()` method
- **✅ Fix**: Added proper data type conversion for datetime fields and enum validation
- **✅ Error Handling**: Added graceful error handling for malformed agent records
- **Status**: Code fix completed, pending production deployment
- **Documentation**: See `docs/troubleshooting/agents-endpoint-internal-server-error.md`

### **Technical Details**
- **File**: `backend/fastapi_app/services/agent_service.py`
- **Method**: `get_agents()` - Added datetime conversion and enum validation
- **Impact**: Agents endpoint now properly handles Supabase data format
- **Testing**: Endpoint now returns proper JSON response instead of 500 error

## [Unreleased] - 2025-10-27

### 🤖 **Cursor Agent Integration - FULLY OPERATIONAL**
- **✅ MCP Server**: Fully operational and healthy
- **✅ MCP Tools**: All 11 tools working correctly
- **✅ Backend Integration**: Successfully connects to AI Agent Factory backend
- **✅ Data Access**: Can retrieve PRDs, agents, and platform data
- **✅ Configuration**: Ready for Cursor Agent connection
- **Status**: Cursor agent integration is fully functional and ready to use

### **MCP Server Details**
- **URL**: https://ai-agent-factory-mcp-server-952475323593.us-central1.run.app
- **Available Tools**: 11 comprehensive tools for platform management
- **Test Results**: Successfully tested PRD retrieval and startup guide
- **Configuration Files**: Standard and enhanced configs available

### 🔗 **Redis Agent-PRD Linking Fixed**
- **✅ Agent Update Endpoint**: Added comprehensive agent update API endpoint
- **✅ Redis Agent Linked**: Successfully linked Redis agent to its PRD
- **✅ Production Environment**: Fixed missing environment variables using secure configuration
- **✅ Backend Health**: All services now properly configured and operational
- **Status**: Redis agent no longer shows as "Standalone Agent"

### **Technical Details**
- **Agent Update Model**: Added `AgentUpdate` model for partial agent updates
- **API Endpoint**: `PUT /api/v1/agents/{agent_id}` for updating agent properties
- **Environment Variables**: Used secure API manager to set production environment variables
- **Agent-PRD Link**: Redis agent now properly linked to PRD `1191e06d-453b-4903-9edd-f3a4d11f9d99`

## [Unreleased] - 2025-10-26

### 🔧 **PRD Status Standardization**
- **✅ Database Schema**: Updated to include all 9 PRD states
- **✅ Backend Models**: Standardized PRD status enumeration
- **✅ Frontend Types**: Aligned TypeScript types with backend
- **✅ Documentation**: Updated all PRD workflow documentation
- **✅ Default Status**: Changed from `queue` to `uploaded` for new PRDs
- **Status**: All PRD states now consistent across the entire system

### **Standardized PRD States**
- **`uploaded`** - PRD uploaded and awaiting standardization
- **`standardizing`** - PRD being converted to AI Agent Factory format
- **`review`** - PRD awaiting user review and approval
- **`queue`** - PRD approved and waiting for processing
- **`ready_for_devin`** - PRD ready to be picked up by Devin AI
- **`in_progress`** - PRD being processed by Devin AI
- **`completed`** - PRD successfully processed and agent deployed
- **`failed`** - PRD processing failed
- **`processed`** - Final state after completion

### **Configuration & Deployment Fixes**
- **✅ Backend URL Configuration**: Fixed Next.js configuration to use correct backend URL
- **✅ Environment Variables**: Resolved missing production environment variables
- **✅ Network Connectivity**: All services properly connected and operational
- **✅ Documentation**: Updated deployment documentation with current status
- **Backend URL**: Updated to `https://ai-agent-factory-backend-fdqqqinvyq-uc.a.run.app`
- **Status**: Production environment fully operational

### Fixed
- **Backend URL Mismatch**: Resolved incorrect backend URL fallback in Next.js config
- **Environment Variables**: Fixed missing production environment variables
- **Service Connectivity**: All services now properly connected
- **Documentation**: Updated README and deployment docs with current URLs

### Known Issues
- **Frontend SSR Issue**: Next.js server-side rendering shows `BAILOUT_TO_CLIENT_SIDE_RENDERING`
- **Impact**: Minimal - client-side functionality works correctly
- **Workaround**: Application loads and functions properly once JavaScript executes

## [Unreleased] - 2024-12-19

### 🎉 **MAJOR SUCCESS: Redis Caching Layer Agent Integration**
- **✅ Redis Agent Deployed**: Successfully deployed Redis Caching Layer Agent to production
- **✅ Agent Registration**: Agent successfully registered with AI Agent Factory platform
- **✅ Database Integration**: Agents table created and operational in Supabase
- **✅ API Integration**: Backend API fully functional with agent management
- **✅ Health Monitoring**: Agent health check system operational
- **Agent URL**: https://redis-caching-agent-fdqqqinvyq-uc.a.run.app
- **Health Check**: https://redis-caching-agent-fdqqqinvyq-uc.a.run.app/health

### Added
- **Hybrid Repository Strategy**: Implemented intelligent repository management based on PRD type
  - Platform PRDs: Agents stored in main repository (`/agents/` folder)
  - Agent PRDs: Separate GitHub repositories created (`ai-agents-{name}`)
- **New MCP Tool**: `determine_repository_strategy` for Devin AI to understand repository approach
- **Enhanced Agent Creation**: Automatic repository strategy detection during agent creation

### Changed
- **Repository Naming Convention**: Updated from `end-cap-agent-{name}` to `ai-agents-{name}`
- **Devin MCP Server**: Enhanced with hybrid repository strategy logic
- **Devin Service**: Updated agent creation flow to support both repository strategies
- **Documentation**: Updated all references to reflect new naming convention and strategy

### Technical Details
- Modified `scripts/mcp/devin-mcp-server.py`:
  - Updated `_create_agent_from_prd` with repository strategy logic
  - Enhanced `_create_github_repository` to validate PRD type
  - Added `_determine_repository_strategy` MCP tool
  - Updated startup guide with hybrid strategy information

- Modified `backend/fastapi_app/services/devin_service.py`:
  - Updated `_create_agent_from_task` with repository strategy detection
  - Enhanced agent registration with repository strategy metadata

- Updated Documentation:
  - `docs/guides/05-agent-management.md`
  - `docs/guides/02-devin-ai-integration.md`
  - All legacy documentation files
  - Main README.md with repository strategy information

### Benefits
- **Organized Infrastructure**: Platform agents stay in main repository for easy management
- **Isolated Agent Development**: Individual agents get dedicated repositories for full isolation
- **Automatic Detection**: System automatically chooses appropriate repository strategy
- **Consistent Branding**: All agent repositories use professional `ai-agents-` prefix
- **Backward Compatible**: Existing agents continue to work unchanged

---

## Previous Releases

*Note: This changelog was created to document the hybrid repository strategy implementation. Previous changes are not documented here but can be found in git history.*
