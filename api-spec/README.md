# API Specification

This directory contains the OpenAPI specification that serves as the contract between the backend and frontend.

## 📋 Files

- **`openapi.json`** - OpenAPI 3.1 specification in JSON format
- **`openapi.yaml`** - OpenAPI 3.1 specification in YAML format
- **`types.ts`** - Generated TypeScript types from the OpenAPI spec

## 🔄 Generating the Specification

### From FastAPI (Backend)

The OpenAPI spec is automatically generated from the FastAPI application:

```bash
# Generate OpenAPI spec from FastAPI
python3 scripts/api/generate-openapi-spec.py
```

This will:
1. Extract the OpenAPI schema from the FastAPI app
2. Enhance it with metadata (servers, contact info, etc.)
3. Save both JSON and YAML versions to `api-spec/`

### Manual Updates

If you need to manually update the spec, edit `openapi.yaml` and then convert to JSON:

```bash
# Convert YAML to JSON (requires yq or python)
python3 -c "import yaml, json; print(json.dumps(yaml.safe_load(open('api-spec/openapi.yaml')), indent=2))" > api-spec/openapi.json
```

## 📝 Using the Specification

### Generate TypeScript Types

Generate TypeScript types from the OpenAPI spec:

```bash
# Install openapi-typescript if not already installed
npm install -D openapi-typescript

# Generate types
npx openapi-typescript api-spec/openapi.json -o frontend/next-app/types/api.ts
```

### Validate API Responses

Use the spec to validate API responses:

```bash
# Install swagger-cli if not already installed
npm install -g swagger-cli

# Validate the spec
swagger-cli validate api-spec/openapi.json
```

### API Documentation

View the interactive API documentation:

- **Swagger UI**: `https://ai-agent-factory-backend-952475323593.us-central1.run.app/docs`
- **ReDoc**: `https://ai-agent-factory-backend-952475323593.us-central1.run.app/redoc`

## 🔗 Integration with Frontend

### Type Safety

The generated TypeScript types ensure type safety between backend and frontend:

```typescript
import { Agent, AgentListResponse } from '@/types/api'

// Type-safe API calls
const response: AgentListResponse = await fetch('/api/v1/agents').then(r => r.json())
```

### API Client Generation

You can generate a type-safe API client from the OpenAPI spec:

```bash
# Using openapi-generator
npx @openapitools/openapi-generator-cli generate \
  -i api-spec/openapi.json \
  -g typescript-fetch \
  -o frontend/next-app/lib/api-client
```

## 🔄 Workflow

1. **Backend Changes**: Update FastAPI models/routes
2. **Generate Spec**: Run `python3 scripts/api/generate-openapi-spec.py`
3. **Generate Types**: Run `npm run generate:types` (in frontend)
4. **Validate**: Run `npm run validate:api` (in frontend)
5. **Commit**: Commit both spec and generated types

## 📚 Resources

- [OpenAPI Specification](https://swagger.io/specification/)
- [FastAPI OpenAPI](https://fastapi.tiangolo.com/advanced/openapi-customization/)
- [openapi-typescript](https://github.com/drwpow/openapi-typescript)

