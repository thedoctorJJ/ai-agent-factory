# REST API Reference

Complete REST API documentation for the AI Agent Factory platform.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication

Currently, the API does not require authentication for development. In production, JWT-based authentication will be implemented.

## API Endpoints

### Health & Status

#### Get Platform Health
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

#### Get Detailed Health Status
```http
GET /api/v1/health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "supabase": "connected",
    "openai": "connected",
    "github": "connected"
  }
}
```

#### Get Configuration Status
```http
GET /api/v1/config
```

**Response:**
```json
{
  "environment_source": "config/env/.env.local",
  "environment": "development",
  "debug": true,
  "variables": {
    "DATABASE_URL": "configured",
    "SUPABASE_URL": "configured",
    "OPENAI_API_KEY": "configured"
  },
  "overall_status": "valid"
}
```

### PRD Management

#### Create PRD
```http
POST /api/v1/prds
Content-Type: application/json

{
  "title": "My PRD Title",
  "description": "PRD description",
  "requirements": ["Requirement 1", "Requirement 2"],
  "prd_type": "agent",
  "problem_statement": "What problem this solves",
  "target_users": ["User 1", "User 2"],
  "user_stories": ["As a user, I want..."],
  "acceptance_criteria": ["Criteria 1", "Criteria 2"],
  "technical_requirements": ["Tech requirement 1"],
  "success_metrics": ["Metric 1", "Metric 2"]
}
```

**Response:**
```json
{
  "id": "prd_123",
  "title": "My PRD Title",
  "description": "PRD description",
  "status": "queue",
  "prd_type": "agent",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### List PRDs
```http
GET /api/v1/prds?skip=0&limit=100&prd_type=agent&status=queue
```

**Query Parameters:**
- `skip` (int): Number of PRDs to skip (default: 0)
- `limit` (int): Number of PRDs to return (default: 100, max: 1000)
- `prd_type` (string): Filter by PRD type (`platform` or `agent`)
- `status` (string): Filter by PRD status

**Response:**
```json
{
  "prds": [
    {
      "id": "prd_123",
      "title": "My PRD Title",
      "status": "queue",
      "prd_type": "agent",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 100,
  "has_next": false
}
```

#### Get PRD by ID
```http
GET /api/v1/prds/{prd_id}
```

**Response:**
```json
{
  "id": "prd_123",
  "title": "My PRD Title",
  "description": "PRD description",
  "status": "queue",
  "prd_type": "agent",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Update PRD
```http
PUT /api/v1/prds/{prd_id}
Content-Type: application/json

{
  "title": "Updated PRD Title",
  "description": "Updated description"
}
```

#### Delete PRD
```http
DELETE /api/v1/prds/{prd_id}
```

#### Upload PRD File
```http
POST /api/v1/prds/upload
Content-Type: multipart/form-data

file: [markdown file]
```

#### Get PRDs Ready for Devin
```http
GET /api/v1/prds/ready-for-devin
```

**Response:**
```json
{
  "message": "PRDs ready for Devin AI",
  "count": 2,
  "prds": [
    {
      "id": "prd_123",
      "title": "My PRD Title",
      "status": "ready_for_devin"
    }
  ]
}
```

#### Mark PRD as Ready for Devin
```http
POST /api/v1/prds/{prd_id}/ready-for-devin
```

#### Get PRD as Markdown
```http
GET /api/v1/prds/{prd_id}/markdown
```

**Response:**
```json
{
  "prd_id": "prd_123",
  "markdown": "# My PRD Title\n\nDescription...",
  "filename": "my-prd-title.md"
}
```

#### Download PRD as Markdown
```http
GET /api/v1/prds/{prd_id}/markdown/download
```

Returns the markdown file for download.

#### Delete All PRDs
```http
DELETE /api/v1/prds
```

### Agent Management

#### Create Agent
```http
POST /api/v1/agents
Content-Type: application/json

{
  "name": "My Agent",
  "description": "Agent description",
  "purpose": "Agent purpose",
  "version": "1.0.0",
  "repository_url": "https://github.com/user/repo",
  "deployment_url": "https://my-agent.example.com",
  "health_check_url": "https://my-agent.example.com/health",
  "prd_id": "prd_123",
  "capabilities": ["capability1", "capability2"],
  "configuration": {}
}
```

#### List Agents
```http
GET /api/v1/agents?skip=0&limit=100&status=running&prd_id=prd_123
```

**Query Parameters:**
- `skip` (int): Number of agents to skip
- `limit` (int): Number of agents to return
- `status` (string): Filter by agent status
- `prd_id` (string): Filter by PRD ID

#### Get Agent by ID
```http
GET /api/v1/agents/{agent_id}
```

#### Update Agent Status
```http
PUT /api/v1/agents/{agent_id}/status
Content-Type: application/json

{
  "status": "running"
}
```

#### Delete Agent
```http
DELETE /api/v1/agents/{agent_id}
```

#### Delete All Agents
```http
DELETE /api/v1/agents
```

#### Get Agent Health
```http
GET /api/v1/agents/{agent_id}/health
```

**Response:**
```json
{
  "agent_id": "agent_123",
  "agent_name": "My Agent",
  "health_check_url": "https://my-agent.example.com/health",
  "status": "healthy",
  "details": {},
  "response_time_ms": 45
}
```

#### Get Agent Metrics
```http
GET /api/v1/agents/{agent_id}/metrics
```

**Response:**
```json
{
  "agent_id": "agent_123",
  "agent_name": "My Agent",
  "status": "running",
  "health_status": "healthy",
  "version": "1.0.0",
  "capabilities": ["capability1"],
  "uptime_seconds": 3600,
  "request_count": 100,
  "error_count": 0,
  "avg_response_time_ms": 45
}
```

#### Get Agents by PRD
```http
GET /api/v1/agents/by-prd/{prd_id}
```

### Devin AI Integration

#### Create Devin Task
```http
POST /api/v1/devin/tasks
Content-Type: application/json

{
  "prd_id": "prd_123",
  "title": "Task Title",
  "description": "Task description",
  "requirements": ["Requirement 1", "Requirement 2"]
}
```

#### List Devin Tasks
```http
GET /api/v1/devin/tasks?skip=0&limit=100&status=pending&prd_id=prd_123
```

#### Get Devin Task by ID
```http
GET /api/v1/devin/tasks/{task_id}
```

#### Execute Devin Task
```http
POST /api/v1/devin/tasks/{task_id}/execute
```

#### Complete Devin Task
```http
POST /api/v1/devin/tasks/{task_id}/complete
```

### MCP Integration

#### Load PRD for MCP
```http
POST /api/v1/mcp/load-prd
Content-Type: application/json

{
  "prd_id": "prd_123"
}
```

#### Get MCP Status
```http
GET /api/v1/mcp/status
```

### Roadmap & Analytics

#### Get Roadmap Categories
```http
GET /api/v1/roadmap/categories
```

#### Get Roadmap Statuses
```http
GET /api/v1/roadmap/statuses
```

#### Get Roadmap Priorities
```http
GET /api/v1/roadmap/priorities
```

#### Get Roadmap Data
```http
GET /api/v1/roadmap?prd_type=agent&status=queue&category=feature
```

### System Management

#### Clear All Data
```http
DELETE /api/v1/clear-all
```

**Response:**
```json
{
  "message": "All data cleared successfully",
  "agents": {"deleted": 5},
  "prds": {"deleted": 10}
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": {
    "message": "Error description",
    "error_code": "ERROR_CODE",
    "details": {}
  }
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting

Currently no rate limiting is implemented. In production, rate limiting will be added based on user authentication.

## API Versioning

The API uses URL-based versioning (`/api/v1/`). Future versions will use `/api/v2/`, etc.

## Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
