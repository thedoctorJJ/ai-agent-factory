FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY scripts/mcp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for MCP server
RUN pip install --no-cache-dir \
    fastapi>=0.118.0 \
    uvicorn>=0.37.0 \
    pydantic>=2.12.0 \
    python-multipart>=0.0.20 \
    httpx>=0.24.0 \
    requests>=2.32.0 \
    python-dotenv>=1.1.1

# Copy MCP server files
COPY scripts/mcp/mcp-http-server.py .
COPY scripts/mcp/cursor-agent-mcp-server.py .
COPY scripts/mcp/devin-mcp-server.py .
COPY scripts/mcp/simple_services.py .
COPY scripts/mcp/google-cloud-run-deploy.py .

# Copy backend config (needed by cursor-agent-mcp-server)
# Note: Build context should be from project root
COPY backend/fastapi_app/config.py ./backend/fastapi_app/
RUN mkdir -p backend/fastapi_app && touch backend/fastapi_app/__init__.py

# Expose port (Cloud Run will set PORT env var)
EXPOSE 8001

# Set environment variables
ENV HOST=0.0.0.0

# Run the MCP HTTP server
CMD ["python", "mcp-http-server.py"]
