#!/usr/bin/env python3
"""
Robust Configuration Validation Script
This script loads configuration using the robust loader and validates all services
"""

import os
import sys
import requests
from pathlib import Path

# Add config directory to path
config_dir = Path(__file__).parent.parent / "config"
sys.path.insert(0, str(config_dir))

# Import the robust config loader
import importlib.util
spec = importlib.util.spec_from_file_location("load_config", config_dir / "load-config.py")
load_config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(load_config_module)
load_config = load_config_module.load_config
set_environment_variables = load_config_module.set_environment_variables

class RobustConfigValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
        
    def log_error(self, message):
        self.errors.append(f"❌ {message}")
        print(f"❌ {message}")
        
    def log_warning(self, message):
        self.warnings.append(f"⚠️  {message}")
        print(f"⚠️  {message}")
        
    def log_success(self, message):
        self.success_count += 1
        print(f"✅ {message}")
        
    def validate_google_cloud_config(self):
        """Validate Google Cloud configuration."""
        print("\n☁️  Validating Google Cloud Configuration...")
        
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        service_account_key = os.getenv('GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY')
        redis_host = os.getenv('REDIS_HOST')
        redis_port = os.getenv('REDIS_PORT')
        
        if not project_id:
            self.log_error("Google Cloud Project ID not configured")
        else:
            self.log_success(f"Google Cloud Project ID: {project_id}")
            
        if not service_account_key:
            self.log_warning("Google Cloud service account key not configured")
        else:
            if os.path.exists(service_account_key):
                self.log_success("Google Cloud service account key file exists")
            else:
                self.log_error("Google Cloud service account key file not found")
        
        if redis_host and redis_port:
            self.log_success(f"Redis configured: {redis_host}:{redis_port}")
        else:
            self.log_warning("Redis configuration incomplete")
            
    def validate_supabase_connection(self):
        """Test Supabase connection and API keys."""
        print("\n🗄️  Validating Supabase Connection...")
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            self.log_error("Supabase URL or key not configured")
            return
            
        try:
            headers = {
                'apikey': supabase_key,
                'Authorization': f'Bearer {supabase_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.log_success("Supabase connection successful")
            else:
                self.log_error(f"Supabase connection failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.log_error(f"Supabase connection error: {str(e)}")
            
    def validate_openai_api(self):
        """Test OpenAI API key."""
        print("\n🤖 Validating OpenAI API...")
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            self.log_error("OpenAI API key not configured")
            return
            
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get('https://api.openai.com/v1/models', headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.log_success("OpenAI API key is valid")
            else:
                self.log_error(f"OpenAI API key validation failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.log_error(f"OpenAI API error: {str(e)}")
            
    def validate_github_config(self):
        """Validate GitHub App configuration."""
        print("\n🐙 Validating GitHub Configuration...")
        
        github_token = os.getenv('GITHUB_TOKEN')
        github_org = os.getenv('GITHUB_ORG_NAME')
        
        if not github_token:
            self.log_error("GitHub token not configured")
        else:
            self.log_success("GitHub token is configured")
            
        if not github_org:
            self.log_warning("GitHub organization not configured")
        else:
            self.log_success(f"GitHub organization: {github_org}")
            
    def validate_deployment_config(self):
        """Validate deployment configuration."""
        print("\n🚀 Validating Deployment Configuration...")
        
        platform = os.getenv('DEPLOYMENT_PLATFORM')
        region = os.getenv('DEPLOYMENT_REGION')
        project = os.getenv('DEPLOYMENT_PROJECT')
        
        if platform == 'google-cloud-run':
            self.log_success("Deployment platform: Google Cloud Run (not Fly.io)")
        else:
            self.log_warning(f"Deployment platform: {platform}")
            
        if region:
            self.log_success(f"Deployment region: {region}")
        else:
            self.log_warning("Deployment region not configured")
            
        if project:
            self.log_success(f"Deployment project: {project}")
        else:
            self.log_warning("Deployment project not configured")
            
    def run_all_validations(self):
        """Run all validation checks."""
        print("🚀 Starting Robust Configuration Validation for AI Agent Factory")
        print("=" * 70)
        
        # Load configuration first using secure API manager
        print("📋 Loading configuration...")
        import subprocess
        import sys
        
        # Use the secure API manager to create working .env
        result = subprocess.run([
            sys.executable, 'config/secure-api-manager.py', 'create'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Failed to load secure configuration: {result.stderr}")
            return
        
        # Load the generated .env file
        from dotenv import load_dotenv
        load_dotenv()
        
        # Run validations
        self.validate_google_cloud_config()
        self.validate_supabase_connection()
        self.validate_openai_api()
        self.validate_github_config()
        self.validate_deployment_config()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)
        
        print(f"✅ Successful validations: {self.success_count}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.errors:
            print("\n🔧 REQUIRED ACTIONS:")
            for error in self.errors:
                print(f"  {error}")
                
        if self.warnings:
            print("\n💡 RECOMMENDATIONS:")
            for warning in self.warnings:
                print(f"  {warning}")
                
        if not self.errors:
            print("\n🎉 All critical configurations are valid! Your platform is ready to run.")
        else:
            print(f"\n⚠️  Please fix {len(self.errors)} error(s) before running the platform.")
            sys.exit(1)

def main():
    """Main function."""
    validator = RobustConfigValidator()
    validator.run_all_validations()

if __name__ == "__main__":
    main()
