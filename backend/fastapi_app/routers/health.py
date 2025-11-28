from fastapi import APIRouter
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
        # Determine environment configuration status
        env_status = "missing"

        # Check if we're in production (environment variables)
        if config.environment == "production":
            # In production, check if we have the required environment variables
            has_env_vars = all([
                config.supabase_url, config.supabase_key,
                config.openai_api_key, config.github_token,
                config.google_cloud_project_id
            ])
            env_status = "configured" if has_env_vars else "missing"
        else:
            # In development, check for environment files
            try:
                project_root = Path(__file__).parent.parent.parent.parent
                env_local_path = project_root / "config" / "env" / ".env.local"
                env_path = project_root / ".env"

                # Check if environment files exist
                if env_local_path.exists() or env_path.exists():
                    env_status = "configured"
                else:
                    # Fallback: check if we have environment variables even in dev
                    has_env_vars = all([
                        config.supabase_url, config.supabase_key,
                        config.openai_api_key, config.github_token,
                        config.google_cloud_project_id
                    ])
                    env_status = "configured" if has_env_vars else "missing"
            except Exception:
                # If file checking fails, fall back to environment variable check
                has_env_vars = all([
                    config.supabase_url, config.supabase_key,
                    config.openai_api_key, config.github_token,
                    config.google_cloud_project_id
                ])
                env_status = "configured" if has_env_vars else "missing"

        # Check service configurations
        supabase_configured = (config.supabase_url and config.supabase_key)
        google_cloud_configured = config.google_cloud_project_id

        services = {
            "supabase": "configured" if supabase_configured else "not_configured",
            "openai": "configured" if config.openai_api_key else "not_configured",
            "github": "configured" if config.github_token else "not_configured",
            "google_cloud": "configured" if google_cloud_configured else "not_configured"
        }

        # Determine overall health status
        all_services_configured = all(
            status == "configured" for status in services.values())
        is_healthy = (env_status == "configured" and all_services_configured)
        overall_status = "healthy" if is_healthy else "degraded"

        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": config.environment,
            "python_version": sys.version,
            "platform": platform.platform(),
            "environment_config": env_status,
            "services": services
        }
    except Exception as e:
        # Return a degraded status instead of throwing an error
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": "unknown",
            "python_version": sys.version,
            "platform": platform.platform(),
            "environment_config": "error",
            "services": {
                "supabase": "error",
                "openai": "error",
                "github": "error",
                "google_cloud": "error"
            },
            "error": str(e)
        }


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with service connectivity
    
    Note: This endpoint checks configuration via the config object, which is what
    the application actually uses. In production, environment variables may be
    set via Google Cloud Run environment variables or Cloud Secrets Manager,
    but the config object will load them correctly regardless of the source.
    """
    try:
        # Check environment variables via config object (what the app actually uses)
        # This ensures consistency with how the application loads configuration
        env_status = {
            "SUPABASE_URL": "configured" if config.supabase_url else "missing",
            "SUPABASE_KEY": "configured" if config.supabase_key else "missing",
            "OPENAI_API_KEY": "configured" if config.openai_api_key else "missing",
            "GITHUB_TOKEN": "configured" if config.github_token else "missing",
            "GOOGLE_CLOUD_PROJECT_ID": "configured" if config.google_cloud_project_id else "missing"
        }

        # Service connectivity checks
        supabase_configured = (config.supabase_url and config.supabase_key)
        google_cloud_configured = config.google_cloud_project_id

        services = {
            "supabase": "configured" if supabase_configured else "not_configured",
            "openai": "configured" if config.openai_api_key else "not_configured",
            "github": "configured" if config.github_token else "not_configured",
            "google_cloud": "configured" if google_cloud_configured else "not_configured"
        }

        # Determine overall status
        # Use service configuration status as the source of truth since that's what matters
        all_services_configured = all(
            status == "configured" for status in services.values())
        # Note: In production, environment variables may be set via Cloud Run
        # but not directly accessible via os.getenv(). The config object handles
        # loading from various sources (env vars, secrets, files), so we trust
        # the service configuration status as the authoritative check.
        is_healthy = all_services_configured
        overall_status = "healthy" if is_healthy else "degraded"

        health_data = {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": config.environment,
            "python_version": sys.version,
            "platform": platform.platform(),
            "environment_variables": env_status,
            "services": services
        }

        return health_data
    except Exception as e:
        # Return error information instead of throwing HTTPException
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": "unknown",
            "python_version": sys.version,
            "platform": platform.platform(),
            "environment_variables": {"error": "failed_to_check"},
            "services": {"error": "failed_to_check"},
            "error": str(e)
        }


@router.get("/debug/data-manager")
async def debug_data_manager():
    """Debug endpoint to check data manager status."""
    from ..utils.simple_data_manager import data_manager
    from ..config import config
    import os
    
    return {
        "data_manager": {
            "mode": data_manager.mode,
            "is_connected": data_manager.is_connected(),
            "has_supabase_client": data_manager.supabase is not None,
            "memory_storage_count": {
                "prds": len(data_manager.memory_storage.get("prds", {})),
                "agents": len(data_manager.memory_storage.get("agents", {}))
            }
        },
        "environment": {
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "not set"),
            "DATA_MODE": os.getenv("DATA_MODE", "not set"),
        },
        "supabase_config": {
            "url_set": bool(config.supabase_url),
            "url_preview": config.supabase_url[:30] + "..." if config.supabase_url else None,
            "anon_key_set": bool(config.supabase_key),
            "service_role_key_set": bool(config.supabase_service_role_key),
            "key_type": "service_role" if config.supabase_service_role_key else "anon" if config.supabase_key else "none"
        }
    }


@router.get("/config")
async def get_configuration():
    """Get application configuration status"""
    try:
        return config.validate_config()
    except Exception as e:
        # Return error information instead of throwing HTTPException
        return {
            "environment_source": "error",
            "environment": "unknown",
            "debug": False,
            "variables": {"error": "failed_to_check"},
            "overall_status": "error",
            "missing_variables": ["error"],
            "error": str(e)
        }
