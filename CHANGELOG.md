# Changelog

All notable changes to the AI Agent Factory project will be documented in this file.

## [Unreleased] - 2024-12-19

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
