# Changelog

All notable changes to the AI Agent Factory project will be documented in this file.

## [Unreleased] - 2025-10-26

### 🔧 **Configuration & Deployment Fixes**
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
