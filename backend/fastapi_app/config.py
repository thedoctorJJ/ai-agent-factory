"""
Configuration management for AI Agent Factory
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Application configuration"""

    def __init__(self):
        self._load_environment()

    def _load_environment(self):
        """Load environment variables from appropriate location"""
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent
        env_local_path = project_root / "config" / "env" / ".env.local"
        env_path = project_root / ".env"

        if env_local_path.exists():
            load_dotenv(env_local_path)
            self.env_source = "config/env/.env.local"
        elif env_path.exists():
            load_dotenv(env_path)
            self.env_source = ".env"
        else:
            # Fallback to default .env loading
            load_dotenv()
            self.env_source = "default"

    @property
    def environment(self) -> str:
        """Get current environment"""
        return os.getenv("ENVIRONMENT", "development")

    @property
    def debug(self) -> bool:
        """Check if debug mode is enabled"""
        return os.getenv("DEBUG", "false").lower() == "true"

    @property
    def database_url(self) -> Optional[str]:
        """Get database URL"""
        return os.getenv("DATABASE_URL")

    @property
    def supabase_url(self) -> Optional[str]:
        """Get Supabase URL"""
        return os.getenv("SUPABASE_URL")

    @property
    def supabase_key(self) -> Optional[str]:
        """Get Supabase anon key"""
        return os.getenv("SUPABASE_KEY")

    @property
    def supabase_service_role_key(self) -> Optional[str]:
        """Get Supabase service role key"""
        return os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key"""
        return os.getenv("OPENAI_API_KEY")

    @property
    def github_token(self) -> Optional[str]:
        """Get GitHub token"""
        return os.getenv("GITHUB_TOKEN")

    @property
    def google_cloud_project_id(self) -> Optional[str]:
        """Get Google Cloud project ID"""
        return os.getenv("GOOGLE_CLOUD_PROJECT_ID")

    @property
    def cors_origins(self) -> list:
        """Get CORS allowed origins"""
        origins = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:3001")
        return [origin.strip() for origin in origins.split(",")]

    @property
    def strict_prd(self) -> bool:
        """Whether to enforce strict PRD validation"""
        return os.getenv("STRICT_PRD", "true").lower() == "true"

    def validate_config(self) -> dict:
        """Validate configuration and return status
        
        Note: This method checks configuration via config properties, which ensures
        consistency with how the application actually loads configuration. In production,
        variables may be set via Cloud Run environment variables or Cloud Secrets Manager,
        and this method will detect them correctly.
        """
        # Map of environment variable names to config properties
        var_mapping = {
            "SUPABASE_URL": self.supabase_url,
            "SUPABASE_KEY": self.supabase_key,
            "OPENAI_API_KEY": self.openai_api_key,
            "GITHUB_TOKEN": self.github_token,
            "GOOGLE_CLOUD_PROJECT_ID": self.google_cloud_project_id
        }

        status = {
            "environment_source": self.env_source,
            "environment": self.environment,
            "debug": self.debug,
            "variables": {},
            "overall_status": "valid"
        }

        missing_vars = []
        for var_name, config_value in var_mapping.items():
            status["variables"][var_name] = "configured" if config_value else "missing"
            if not config_value:
                missing_vars.append(var_name)

        if missing_vars:
            status["overall_status"] = "incomplete"
            status["missing_variables"] = missing_vars

        return status


# Global config instance
config = Config()
