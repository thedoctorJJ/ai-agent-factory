# API Contract Specification

This document describes the API contract between the backend and frontend, defined using OpenAPI 3.1 specification.

## 📋 Overview

The API contract is defined in the `api-spec/` directory and serves as the single source of truth for:
- API endpoints and their request/response schemas
- Data models and types
- Validation rules
- TypeScript type generation

## 🔄 Workflow

### 1. Backend Changes

When you modify the FastAPI backend (routes, models, etc.):

```bash
# Generate updated OpenAPI spec
python3 scripts/api/generate-openapi-spec.py
```

This will:
- Fetch the latest OpenAPI spec from the production API (or generate from local app)
- Enhance it with metadata (servers, contact info, etc.)
- Save both JSON and YAML versions to `api-spec/`

### 2. Frontend Type Generation

After updating the spec, generate TypeScript types:

```bash
# Generate TypeScript types from OpenAPI spec
./scripts/api/generate-typescript-types.sh
```

Or from the frontend directory:

```bash
cd frontend/next-app
npm run generate:types
```

### 3. Validation

Validate the API contract:

```bash
# Validate OpenAPI spec
./scripts/api/validate-api-contract.sh
```

## 📁 File Structure

```
api-spec/
├── README.md              # API spec documentation
├── openapi.json          # OpenAPI 3.1 spec (JSON)
└── openapi.yaml          # OpenAPI 3.1 spec (YAML)

frontend/next-app/types/
└── api.ts                # Generated TypeScript types

scripts/api/
├── generate-openapi-spec.py      # Generate spec from FastAPI
├── generate-typescript-types.sh  # Generate TS types
└── validate-api-contract.sh      # Validate contract
```

## 🔧 Usage

### Generate OpenAPI Spec

```bash
python3 scripts/api/generate-openapi-spec.py
```

**Options:**
- Fetches from production API by default
- Falls back to local FastAPI app if dependencies available
- Outputs both JSON and YAML formats

### Generate TypeScript Types

```bash
./scripts/api/generate-typescript-types.sh
```

**Requirements:**
- Node.js and npm installed
- `openapi-typescript` package (installed automatically via npx)

**Output:**
- Generates `frontend/next-app/types/api.ts` with all API types

### Validate Contract

```bash
./scripts/api/validate-api-contract.sh [API_URL]
```

**Options:**
- Validates OpenAPI spec syntax
- Tests key endpoints
- Optional: specify API URL (defaults to production)

## 📝 TypeScript Integration

### Using Generated Types

```typescript
import { Agent, AgentListResponse } from '@/types/api'

// Type-safe API calls
async function fetchAgents(): Promise<AgentListResponse> {
  const response = await fetch('/api/v1/agents')
  const data: AgentListResponse = await response.json()
  return data
}
```

### Type Safety Benefits

- **Compile-time validation**: TypeScript catches type mismatches
- **IntelliSense**: Auto-completion for API responses
- **Refactoring safety**: Changes to API are caught during type generation

## 🔍 API Endpoints

The OpenAPI spec includes all endpoints:

### Health
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health check
- `GET /api/v1/config` - Configuration status

### Agents
- `POST /api/v1/agents` - Create agent
- `GET /api/v1/agents` - List agents
- `GET /api/v1/agents/{agent_id}` - Get agent
- `PUT /api/v1/agents/{agent_id}` - Update agent
- `PUT /api/v1/agents/{agent_id}/status` - Update status
- `DELETE /api/v1/agents/{agent_id}` - Delete agent
- `GET /api/v1/agents/{agent_id}/health` - Check health
- `GET /api/v1/agents/{agent_id}/metrics` - Get metrics

### PRDs
- `POST /api/v1/prds` - Create PRD
- `GET /api/v1/prds` - List PRDs
- `GET /api/v1/prds/{prd_id}` - Get PRD
- `PUT /api/v1/prds/{prd_id}` - Update PRD
- `DELETE /api/v1/prds/{prd_id}` - Delete PRD
- `POST /api/v1/prds/upload` - Upload PRD file
- `GET /api/v1/prds/{prd_id}/markdown` - Get markdown

### Devin Integration
- `POST /api/v1/devin/tasks` - Create task
- `GET /api/v1/devin/tasks` - List tasks
- `GET /api/v1/devin/tasks/{task_id}` - Get task
- `POST /api/v1/devin/tasks/{task_id}/execute` - Execute task
- `POST /api/v1/devin/tasks/{task_id}/complete` - Complete task

### MCP Integration
- `POST /api/v1/mcp/load-prd` - Load PRD via MCP
- `GET /api/v1/mcp/status` - MCP status

## 🎯 Best Practices

1. **Always regenerate types after backend changes**
   ```bash
   python3 scripts/api/generate-openapi-spec.py
   ./scripts/api/generate-typescript-types.sh
   ```

2. **Validate before committing**
   ```bash
   ./scripts/api/validate-api-contract.sh
   ```

3. **Use generated types in frontend**
   - Import from `@/types/api`
   - Don't manually define types that exist in the spec

4. **Keep spec in sync**
   - Commit both `api-spec/` and generated `types/api.ts`
   - Update spec when adding new endpoints

5. **Document breaking changes**
   - Update version in OpenAPI spec
   - Document migration path in CHANGELOG

## 🔗 Resources

- [OpenAPI Specification](https://swagger.io/specification/)
- [FastAPI OpenAPI](https://fastapi.tiangolo.com/advanced/openapi-customization/)
- [openapi-typescript](https://github.com/drwpow/openapi-typescript)
- [Swagger Editor](https://editor.swagger.io/) - Edit/view OpenAPI specs

## 📊 Spec Statistics

Current spec includes:
- **28 API endpoints**
- **28 data schemas**
- **Version**: 1.0.0

View the full spec:
- JSON: `api-spec/openapi.json`
- YAML: `api-spec/openapi.yaml`
- Interactive: `https://ai-agent-factory-backend-952475323593.us-central1.run.app/docs`

