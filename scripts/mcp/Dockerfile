FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
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
COPY . .

# Expose port
EXPOSE 8001

# Set environment variables
ENV PORT=8001
ENV HOST=0.0.0.0

# Run the MCP HTTP server
CMD ["python", "mcp-http-server.py"]
