#!/usr/bin/env python3
"""
Configuration validation script for AI Agent Factory Agent Factory.
This script validates all API keys, connections, and configurations.
"""

import os
import sys
import json
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConfigValidator:
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
        
    def validate_required_env_vars(self):
        """Validate all required environment variables are present."""
        print("\n🔍 Validating Environment Variables...")
        
        required_vars = [
            'DATABASE_URL',
            'SUPABASE_URL',
            'SUPABASE_KEY',
            'SUPABASE_SERVICE_ROLE_KEY',
            'GOOGLE_CLOUD_PROJECT_ID',
            'GITHUB_APP_ID',
            'OPENAI_API_KEY',
            'DEVIN_AI_API_KEY'
        ]
        
        for var in required_vars:
            if not os.getenv(var):
                self.log_error(f"Missing required environment variable: {var}")
            else:
                self.log_success(f"Environment variable {var} is set")
                
    def validate_supabase_connection(self):
        """Test Supabase connection and API keys."""
        print("\n🗄️  Validating Supabase Connection...")
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            self.log_error("Supabase URL or key not configured")
            return
            
        try:
            # Test connection to Supabase
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
            
    def validate_devin_ai_api(self):
        """Test Devin AI API key."""
        print("\n🤖 Validating Devin AI API...")
        
        api_key = os.getenv('DEVIN_AI_API_KEY')
        base_url = os.getenv('DEVIN_AI_BASE_URL', 'https://api.devin.ai')
        
        if not api_key:
            self.log_error("Devin AI API key not configured")
            return
            
        if api_key == 'your-devin-ai-api-key':
            self.log_warning("Devin AI API key is still set to placeholder value")
            return
            
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            # Try to make a simple API call (this may need adjustment based on actual Devin AI API)
            response = requests.get(f'{base_url}/health', headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.log_success("Devin AI API key is valid")
            else:
                self.log_warning(f"Devin AI API validation returned status {response.status_code} - API may not be available yet")
                
        except requests.exceptions.RequestException as e:
            self.log_warning(f"Devin AI API error: {str(e)} - API may not be available yet")
            
    def validate_github_config(self):
        """Validate GitHub App configuration."""
        print("\n🐙 Validating GitHub Configuration...")
        
        github_app_id = os.getenv('GITHUB_APP_ID')
        github_private_key = os.getenv('GITHUB_PRIVATE_KEY')
        
        if not github_app_id:
            self.log_error("GitHub App ID not configured")
        else:
            self.log_success("GitHub App ID is configured")
            
        if not github_private_key:
            self.log_error("GitHub private key not configured")
        else:
            # Basic validation of private key format
            if github_private_key.startswith('-----BEGIN'):
                self.log_success("GitHub private key format looks correct")
            else:
                self.log_warning("GitHub private key format may be incorrect")
                
    def validate_google_cloud_config(self):
        """Validate Google Cloud configuration."""
        print("\n☁️  Validating Google Cloud Configuration...")
        
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        service_account_key = os.getenv('GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY')
        
        if not project_id:
            self.log_error("Google Cloud Project ID not configured")
        else:
            self.log_success("Google Cloud Project ID is configured")
            
        if not service_account_key:
            self.log_warning("Google Cloud service account key not configured")
        else:
            if os.path.exists(service_account_key):
                self.log_success("Google Cloud service account key file exists")
            else:
                self.log_error("Google Cloud service account key file not found")
                
    def validate_database_url(self):
        """Validate database URL format."""
        print("\n🗃️  Validating Database URL...")
        
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            self.log_error("Database URL not configured")
            return
            
        try:
            parsed = urlparse(database_url)
            if parsed.scheme == 'postgresql' and parsed.hostname and parsed.port:
                self.log_success("Database URL format is valid")
            else:
                self.log_error("Database URL format is invalid")
        except Exception as e:
            self.log_error(f"Database URL validation error: {str(e)}")
            
    def validate_frontend_config(self):
        """Validate frontend configuration."""
        print("\n🎨 Validating Frontend Configuration...")
        
        api_url = os.getenv('NEXT_PUBLIC_API_URL')
        supabase_url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
        supabase_key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')
        
        if api_url:
            self.log_success("Frontend API URL is configured")
        else:
            self.log_warning("Frontend API URL not configured")
            
        if supabase_url and supabase_key:
            self.log_success("Frontend Supabase configuration is complete")
        else:
            self.log_warning("Frontend Supabase configuration is incomplete")
            
    def run_all_validations(self):
        """Run all validation checks."""
        print("🚀 Starting Configuration Validation for AI Agent Factory Agent Factory")
        print("=" * 70)
        
        self.validate_required_env_vars()
        self.validate_supabase_connection()
        self.validate_openai_api()
        self.validate_devin_ai_api()
        self.validate_github_config()
        self.validate_google_cloud_config()
        self.validate_database_url()
        self.validate_frontend_config()
        
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
    validator = ConfigValidator()
    validator.run_all_validations()

if __name__ == "__main__":
    main()
