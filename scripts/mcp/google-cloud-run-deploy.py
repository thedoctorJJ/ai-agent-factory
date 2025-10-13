#!/usr/bin/env python3
"""
Google Cloud Run deployment script for AI Agent Factory
Deploys agents to Google Cloud Run instead of Fly.io
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

class GoogleCloudRunDeployer:
    def __init__(self, project_id: str, service_account_key_path: str):
        self.project_id = project_id
        self.service_account_key_path = service_account_key_path
        self.region = "us-central1"  # Default region
        
    def authenticate(self) -> bool:
        """Authenticate with Google Cloud using service account"""
        try:
            # Set the service account key file
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.service_account_key_path
            
            # Authenticate
            result = subprocess.run([
                'gcloud', 'auth', 'activate-service-account',
                '--key-file', self.service_account_key_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Google Cloud authentication successful")
                return True
            else:
                print(f"❌ Google Cloud authentication failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error authenticating with Google Cloud: {e}")
            return False
    
    def create_dockerfile(self, agent_code: str, requirements: list) -> str:
        """Create a Dockerfile for the agent"""
        dockerfile_content = f"""
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY agent.py .

# Expose port
EXPOSE 8080

# Run the agent
CMD ["python", "agent.py"]
"""
        return dockerfile_content.strip()
    
    def create_requirements_txt(self, requirements: list) -> str:
        """Create requirements.txt for the agent"""
        base_requirements = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "pydantic==2.5.0",
            "redis==5.0.1",
            "httpx==0.25.2"
        ]
        
        # Add custom requirements
        all_requirements = base_requirements + requirements
        
        return "\n".join(all_requirements)
    
    def build_and_deploy(self, agent_name: str, agent_code: str, requirements: list = None) -> Dict[str, Any]:
        """Build and deploy agent to Google Cloud Run"""
        if requirements is None:
            requirements = []
            
        try:
            # Create temporary directory for build
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Create Dockerfile
                dockerfile_content = self.create_dockerfile(agent_code, requirements)
                dockerfile_path = temp_path / "Dockerfile"
                dockerfile_path.write_text(dockerfile_content)
                
                # Create requirements.txt
                requirements_content = self.create_requirements_txt(requirements)
                requirements_path = temp_path / "requirements.txt"
                requirements_path.write_text(requirements_content)
                
                # Create agent.py
                agent_path = temp_path / "agent.py"
                agent_path.write_text(agent_code)
                
                # Build image
                image_name = f"gcr.io/{self.project_id}/{agent_name}"
                print(f"🔨 Building image: {image_name}")
                
                build_result = subprocess.run([
                    'gcloud', 'builds', 'submit',
                    '--tag', image_name,
                    '--project', self.project_id,
                    str(temp_path)
                ], capture_output=True, text=True)
                
                if build_result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"Build failed: {build_result.stderr}"
                    }
                
                # Deploy to Cloud Run
                service_name = f"{agent_name}-service"
                print(f"🚀 Deploying to Cloud Run: {service_name}")
                
                deploy_result = subprocess.run([
                    'gcloud', 'run', 'deploy', service_name,
                    '--image', image_name,
                    '--platform', 'managed',
                    '--region', self.region,
                    '--allow-unauthenticated',
                    '--project', self.project_id,
                    '--port', '8080',
                    '--memory', '1Gi',
                    '--cpu', '1',
                    '--max-instances', '10'
                ], capture_output=True, text=True)
                
                if deploy_result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"Deploy failed: {deploy_result.stderr}"
                    }
                
                # Get service URL
                url_result = subprocess.run([
                    'gcloud', 'run', 'services', 'describe', service_name,
                    '--platform', 'managed',
                    '--region', self.region,
                    '--project', self.project_id,
                    '--format', 'value(status.url)'
                ], capture_output=True, text=True)
                
                if url_result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"Failed to get service URL: {url_result.stderr}"
                    }
                
                service_url = url_result.stdout.strip()
                
                return {
                    "success": True,
                    "service_name": service_name,
                    "service_url": service_url,
                    "image_name": image_name,
                    "region": self.region
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Deployment error: {str(e)}"
            }
    
    def get_service_info(self, service_name: str) -> Dict[str, Any]:
        """Get information about a deployed service"""
        try:
            result = subprocess.run([
                'gcloud', 'run', 'services', 'describe', service_name,
                '--platform', 'managed',
                '--region', self.region,
                '--project', self.project_id,
                '--format', 'json'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": result.stderr}
                
        except Exception as e:
            return {"error": str(e)}

def main():
    """Main function for testing"""
    # Configuration
    project_id = "agent-factory-474201"
    service_account_key = "../../config/google-cloud-service-account.json"
    
    # Initialize deployer
    deployer = GoogleCloudRunDeployer(project_id, service_account_key)
    
    # Authenticate
    if not deployer.authenticate():
        print("❌ Authentication failed")
        return
    
    # Test deployment
    test_agent_code = """
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Google Cloud Run!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
"""
    
    result = deployer.build_and_deploy("test-agent", test_agent_code)
    
    if result["success"]:
        print(f"✅ Deployment successful!")
        print(f"   Service URL: {result['service_url']}")
        print(f"   Service Name: {result['service_name']}")
    else:
        print(f"❌ Deployment failed: {result['error']}")

if __name__ == "__main__":
    main()
