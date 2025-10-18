# API Reference

Complete API documentation for the AI Agent Factory platform.

## 📚 API Documentation

### [REST API](./rest-api.md)
Complete REST API documentation including:
- Authentication endpoints
- PRD management endpoints
- Agent management endpoints
- Health check endpoints

### [MCP Servers](./mcp-servers.md)
Model Context Protocol server documentation:
- Devin AI MCP server
- Cursor Agent MCP server
- HTTP MCP server
- Configuration and setup

### [Webhooks](./webhooks.md)
Webhook integration guide:
- GitHub webhooks
- Supabase webhooks
- Custom webhook endpoints
- Event handling

## 🔗 External APIs

### Supabase
- **Database**: PostgreSQL with real-time features
- **Authentication**: JWT-based auth system
- **Storage**: File storage for PRDs and assets

### Google Cloud
- **Cloud Run**: Container hosting
- **Secret Manager**: Secure credential storage
- **Cloud Build**: CI/CD pipeline

### GitHub
- **Repository Management**: Automated repo creation
- **Webhooks**: Event-driven integration
- **API**: Repository and organization management

### OpenAI
- **GPT Models**: AI processing and analysis
- **Embeddings**: Vector search capabilities
- **API**: Text generation and analysis

## 📖 Usage Examples

### REST API Examples
```bash
# Get all PRDs
curl -X GET "http://localhost:8000/api/v1/prds"

# Create a new PRD
curl -X POST "http://localhost:8000/api/v1/prds" \
  -H "Content-Type: application/json" \
  -d '{"title": "My PRD", "content": "..."}'

# Get platform status
curl -X GET "http://localhost:8000/api/v1/status"
```

### MCP Server Examples
```python
# Connect to MCP server
from mcp import ClientSession, StdioServerParameters

async with ClientSession(StdioServerParameters(
    command="python3",
    args=["scripts/mcp/cursor-agent-mcp-server.py"]
)) as session:
    # List available tools
    tools = await session.list_tools()
    
    # Call a tool
    result = await session.call_tool("get_platform_status", {})
```

## 🔧 Development

### API Testing
```bash
# Start the backend
cd backend
uvicorn fastapi_app.main:app --reload

# Test endpoints
curl http://localhost:8000/docs  # Interactive API docs
curl http://localhost:8000/health  # Health check
```

### MCP Server Testing
```bash
# Test MCP server
python scripts/mcp/cursor-agent-mcp-server.py

# Test with MCP client
python -m mcp.client scripts/mcp/cursor-agent-mcp-server.py
```

## 📊 API Status

- **REST API**: ✅ Fully functional
- **MCP Servers**: ✅ Operational
- **Webhooks**: ✅ Configured
- **External APIs**: ✅ Integrated

## 🆘 Support

- **API Issues**: [GitHub Issues](https://github.com/thedoctorJJ/ai-agent-factory/issues)
- **Documentation**: This API reference
- **Examples**: See individual API documentation files
