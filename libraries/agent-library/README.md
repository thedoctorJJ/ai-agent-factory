# Agent Library

This directory contains reusable AI agent templates, configurations, and reference implementations for the AI Agent Factory platform.

## 📁 Structure

```
agent-library/
├── templates/           # Pre-built agent templates
│   ├── fastapi-agent/   # FastAPI-based agent template
│   ├── flask-agent/     # Flask-based agent template
│   └── cli-agent/       # Command-line agent template
├── configs/            # Agent configuration files
│   ├── docker/         # Docker configurations
│   ├── cloud-run/      # Google Cloud Run configs
│   └── monitoring/     # Monitoring and logging configs
├── examples/           # Example agent implementations
│   ├── data-processor/ # Data processing agent example
│   ├── api-gateway/    # API gateway agent example
│   └── notification/   # Notification agent example
└── docs/              # Agent development documentation
    ├── best-practices.md
    ├── deployment-guide.md
    └── testing-guide.md
```

## 🎯 Purpose

The Agent Library provides:

- **Standardized Templates**: Consistent agent structure and patterns
- **Best Practices**: Proven patterns for agent development
- **Quick Start**: Ready-to-use templates for common agent types
- **Reference Implementations**: Working examples of different agent patterns
- **Configuration Management**: Standardized deployment and monitoring configs

## 🚀 Quick Start

### 1. Choose a Template

```bash
# Copy a template to start your agent
cp -r templates/fastapi-agent/ my-new-agent/
cd my-new-agent/
```

### 2. Customize Your Agent

```bash
# Update agent configuration
vim config/agent.yaml

# Modify agent logic
vim src/main.py

# Update requirements
vim requirements.txt
```

### 3. Test Your Agent

```bash
# Run tests
python -m pytest tests/

# Start development server
python src/main.py
```

## 📋 Available Templates

### FastAPI Agent Template
- **Purpose**: RESTful API agents with automatic documentation
- **Features**: OpenAPI docs, request validation, async support
- **Use Cases**: Data processing, API gateways, web services

### Flask Agent Template
- **Purpose**: Lightweight web agents with flexible routing
- **Features**: Simple routing, template support, extensions
- **Use Cases**: Simple web services, prototypes, microservices

### CLI Agent Template
- **Purpose**: Command-line interface agents
- **Features**: Argument parsing, logging, configuration
- **Use Cases**: Data processing, automation, batch operations

## 🔧 Configuration

### Agent Configuration (`config/agent.yaml`)

```yaml
agent:
  name: "my-agent"
  version: "1.0.0"
  description: "Agent description"
  
deployment:
  platform: "google-cloud-run"
  region: "us-central1"
  memory: "1Gi"
  cpu: "1"
  
monitoring:
  health_check: "/health"
  metrics: "/metrics"
  logging: "structured"
```

### Environment Variables

```bash
# Required
AGENT_NAME=my-agent
AGENT_VERSION=1.0.0

# Optional
LOG_LEVEL=INFO
DEBUG=false
```

## 📊 Monitoring & Health Checks

All agent templates include:

- **Health Check Endpoint**: `/health` for service health monitoring
- **Metrics Endpoint**: `/metrics` for Prometheus metrics
- **Structured Logging**: JSON-formatted logs for better analysis
- **Error Handling**: Standardized error responses and logging

## 🧪 Testing

### Test Structure

```bash
tests/
├── unit/              # Unit tests for individual components
├── integration/       # Integration tests for API endpoints
├── fixtures/          # Test data and fixtures
└── conftest.py        # Pytest configuration
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_agent.py
```

## 🚀 Deployment

### Google Cloud Run

```bash
# Build and deploy
gcloud run deploy my-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Docker

```bash
# Build image
docker build -t my-agent .

# Run container
docker run -p 8000:8000 my-agent
```

## 📚 Best Practices

### Agent Development

1. **Follow Templates**: Use provided templates as starting points
2. **Health Checks**: Always implement `/health` endpoint
3. **Error Handling**: Use standardized error responses
4. **Logging**: Use structured logging for better monitoring
5. **Testing**: Write comprehensive tests for all functionality

### Configuration

1. **Environment Variables**: Use environment variables for configuration
2. **Secrets Management**: Use secure secret management for sensitive data
3. **Validation**: Validate all configuration on startup
4. **Defaults**: Provide sensible defaults for all configuration options

### Deployment

1. **Containerization**: Always use Docker for consistent deployments
2. **Resource Limits**: Set appropriate CPU and memory limits
3. **Scaling**: Configure auto-scaling based on demand
4. **Monitoring**: Set up comprehensive monitoring and alerting

## 🔗 Integration

### With AI Agent Factory

Agents created from these templates automatically integrate with:

- **Platform Registration**: Automatic registration with the AI Agent Factory
- **Health Monitoring**: Real-time health status tracking
- **Performance Metrics**: Response time and throughput monitoring
- **Dashboard Integration**: Appear in the agent management dashboard

### API Standards

All agents follow these API standards:

- **RESTful Design**: Follow REST principles for API design
- **OpenAPI Documentation**: Automatic API documentation generation
- **Error Responses**: Standardized error response format
- **Authentication**: JWT-based authentication support

## 📖 Documentation

- **[Best Practices Guide](docs/best-practices.md)** - Development best practices
- **[Deployment Guide](docs/deployment-guide.md)** - Deployment procedures
- **[Testing Guide](docs/testing-guide.md)** - Testing strategies and tools

## 🤝 Contributing

To contribute to the Agent Library:

1. **Fork the repository**
2. **Create a feature branch**
3. **Add your agent template or example**
4. **Update documentation**
5. **Submit a pull request**

## 📄 License

This Agent Library is part of the AI Agent Factory project and follows the same licensing terms.
