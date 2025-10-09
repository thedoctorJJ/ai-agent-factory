from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
import sys
import platform
from pathlib import Path
from ..config import config

router = APIRouter()

@router.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Check if environment file exists
        project_root = Path(__file__).parent.parent.parent.parent
        env_local_path = project_root / "config" / "env" / ".env.local"
        env_path = project_root / ".env"
        
        env_status = "configured" if (env_local_path.exists() or env_path.exists()) else "missing"
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": config.environment,
            "python_version": sys.version,
            "platform": platform.platform(),
            "environment_config": env_status,
            "services": {
                "database": "not_configured",  # TODO: Add actual DB health check
                "openai": "not_configured",    # TODO: Add actual OpenAI health check
                "github": "not_configured",    # TODO: Add actual GitHub health check
                "supabase": "not_configured"   # TODO: Add actual Supabase health check
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with service connectivity"""
    try:
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "python_version": sys.version,
            "platform": platform.platform(),
            "services": {}
        }
        
        # Check environment variables
        required_env_vars = [
            "DATABASE_URL", "SUPABASE_URL", "SUPABASE_KEY", 
            "OPENAI_API_KEY", "GITHUB_TOKEN"
        ]
        
        env_status = {}
        for var in required_env_vars:
            env_status[var] = "configured" if os.getenv(var) else "missing"
        
        health_data["environment_variables"] = env_status
        
        # TODO: Add actual service connectivity checks
        health_data["services"] = {
            "database": "not_implemented",
            "openai": "not_implemented", 
            "github": "not_implemented",
            "supabase": "not_implemented"
        }
        
        return health_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detailed health check failed: {str(e)}")

@router.get("/config")
async def get_configuration():
    """Get application configuration status"""
    try:
        return config.validate_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration check failed: {str(e)}")
