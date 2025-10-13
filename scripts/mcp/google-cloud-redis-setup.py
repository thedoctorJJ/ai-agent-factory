#!/usr/bin/env python3
"""
Google Cloud Redis setup for AI Agent Factory
Creates a Redis instance on Google Cloud Memorystore
"""

import os
import json
import subprocess
from typing import Dict, Any, Optional

class GoogleCloudRedisSetup:
    def __init__(self, project_id: str, service_account_key_path: str):
        self.project_id = project_id
        self.service_account_key_path = service_account_key_path
        self.region = "us-central1"
        
    def authenticate(self) -> bool:
        """Authenticate with Google Cloud using service account"""
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.service_account_key_path
            
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
    
    def create_redis_instance(self, instance_name: str = "ai-agent-factory-redis") -> Dict[str, Any]:
        """Create a Redis instance on Google Cloud Memorystore"""
        try:
            print(f"🔧 Creating Redis instance: {instance_name}")
            
            # Create Redis instance
            result = subprocess.run([
                'gcloud', 'redis', 'instances', 'create', instance_name,
                '--size', '1',
                '--region', self.region,
                '--redis-version', 'redis_6_x',
                '--project', self.project_id
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Failed to create Redis instance: {result.stderr}"
                }
            
            # Get instance details
            details_result = subprocess.run([
                'gcloud', 'redis', 'instances', 'describe', instance_name,
                '--region', self.region,
                '--project', self.project_id,
                '--format', 'json'
            ], capture_output=True, text=True)
            
            if details_result.returncode == 0:
                instance_data = json.loads(details_result.stdout)
                host = instance_data.get('host', '')
                port = instance_data.get('port', 6379)
                
                return {
                    "success": True,
                    "instance_name": instance_name,
                    "host": host,
                    "port": port,
                    "region": self.region,
                    "redis_url": f"redis://{host}:{port}",
                    "message": f"Redis instance '{instance_name}' created successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to get instance details: {details_result.stderr}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating Redis instance: {str(e)}"
            }
    
    def get_redis_connection_info(self, instance_name: str) -> Dict[str, Any]:
        """Get connection information for an existing Redis instance"""
        try:
            result = subprocess.run([
                'gcloud', 'redis', 'instances', 'describe', instance_name,
                '--region', self.region,
                '--project', self.project_id,
                '--format', 'json'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                instance_data = json.loads(result.stdout)
                host = instance_data.get('host', '')
                port = instance_data.get('port', 6379)
                
                return {
                    "success": True,
                    "instance_name": instance_name,
                    "host": host,
                    "port": port,
                    "region": self.region,
                    "redis_url": f"redis://{host}:{port}",
                    "message": f"Redis connection info retrieved for '{instance_name}'"
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to get Redis instance info: {result.stderr}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error getting Redis info: {str(e)}"
            }

def main():
    """Main function for testing"""
    project_id = "agent-factory-474201"
    service_account_key = "config/google-cloud-service-account.json"
    
    # Initialize setup
    redis_setup = GoogleCloudRedisSetup(project_id, service_account_key)
    
    # Authenticate
    if not redis_setup.authenticate():
        print("❌ Authentication failed")
        return
    
    # Try to get existing Redis instance info first
    print("🔍 Checking for existing Redis instance...")
    result = redis_setup.get_redis_connection_info("ai-agent-factory-redis")
    
    if result["success"]:
        print(f"✅ Found existing Redis instance!")
        print(f"   Host: {result['host']}")
        print(f"   Port: {result['port']}")
        print(f"   URL: {result['redis_url']}")
    else:
        print("📝 No existing Redis instance found. Creating new one...")
        result = redis_setup.create_redis_instance()
        
        if result["success"]:
            print(f"✅ Redis instance created successfully!")
            print(f"   Host: {result['host']}")
            print(f"   Port: {result['port']}")
            print(f"   URL: {result['redis_url']}")
        else:
            print(f"❌ Failed to create Redis instance: {result['error']}")

if __name__ == "__main__":
    main()
