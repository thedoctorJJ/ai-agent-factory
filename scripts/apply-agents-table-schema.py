#!/usr/bin/env python3
"""
Apply Agents Table Schema to Production Supabase
This script creates the agents table in the production Supabase database
"""

import os
import sys
import asyncio
import requests
from pathlib import Path

# Add the backend to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi_app.config import config

def apply_agents_table_schema():
    """Apply the agents table schema to production Supabase"""
    
    print("🗄️  Applying Agents Table Schema to Production Supabase")
    print("=" * 60)
    
    # Get Supabase credentials
    supabase_url = config.supabase_url
    supabase_key = config.supabase_key
    
    if not supabase_url or not supabase_key:
        print("❌ Error: Supabase credentials not found")
        return False
    
    print(f"🔧 Supabase URL: {supabase_url}")
    print(f"🔧 Supabase Key: {supabase_key[:50]}...")
    print()
    
    # Read the schema file
    schema_file = Path(__file__).parent.parent / "infra" / "database" / "schema.sql"
    if not schema_file.exists():
        print(f"❌ Error: Schema file not found: {schema_file}")
        return False
    
    print(f"📄 Reading schema file: {schema_file}")
    with open(schema_file, 'r') as f:
        schema_sql = f.read()
    
    # Extract just the agents table creation part
    agents_table_sql = """
-- Create custom types if they don't exist
CREATE TYPE IF NOT EXISTS agent_status AS ENUM ('draft', 'active', 'inactive', 'deprecated', 'error');
CREATE TYPE IF NOT EXISTS agent_health_status AS ENUM ('healthy', 'degraded', 'unhealthy', 'unknown');
CREATE TYPE IF NOT EXISTS agent_type AS ENUM ('web_app', 'api_service', 'data_processor', 'automation_script', 'ai_model', 'integration', 'other');

-- Create agents table
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    purpose TEXT NOT NULL,
    agent_type agent_type NOT NULL DEFAULT 'other',
    version VARCHAR(50) NOT NULL DEFAULT '1.0.0',
    status agent_status NOT NULL DEFAULT 'draft',
    health_status agent_health_status NOT NULL DEFAULT 'unknown',
    repository_url VARCHAR(500),
    deployment_url VARCHAR(500),
    health_check_url VARCHAR(500),
    prd_id UUID REFERENCES prds(id) ON DELETE SET NULL,
    devin_task_id UUID,
    capabilities TEXT[] DEFAULT '{}',
    configuration JSONB DEFAULT '{}',
    metrics JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_health_check TIMESTAMP WITH TIME ZONE,
    
    -- Indexes for performance
    CONSTRAINT agents_name_not_empty CHECK (length(trim(name)) > 0),
    CONSTRAINT agents_purpose_not_empty CHECK (length(trim(purpose)) > 0)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_health_status ON agents(health_status);
CREATE INDEX IF NOT EXISTS idx_agents_prd_id ON agents(prd_id);
CREATE INDEX IF NOT EXISTS idx_agents_created_at ON agents(created_at);
"""
    
    print("📝 Agents table schema prepared")
    print()
    
    # Test connection first
    print("🔌 Testing Supabase connection...")
    try:
        # Test with a simple query to PRDs table (which we know exists)
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json'
        }
        
        test_url = f"{supabase_url}/rest/v1/prds?select=id&limit=1"
        response = requests.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Supabase connection successful")
        else:
            print(f"❌ Supabase connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Supabase connection error: {e}")
        return False
    
    print()
    print("⚠️  IMPORTANT: This script cannot directly execute SQL on Supabase")
    print("📋 Please follow these steps to create the agents table:")
    print()
    print("1. Go to your Supabase dashboard:")
    print("   https://supabase.com/dashboard/project")
    print()
    print("2. Navigate to SQL Editor")
    print()
    print("3. Copy and paste the following SQL:")
    print("   " + "="*60)
    print(agents_table_sql)
    print("   " + "="*60)
    print()
    print("4. Execute the SQL")
    print()
    print("5. Verify the table was created by running:")
    print("   SELECT * FROM agents LIMIT 1;")
    print()
    print("6. Test the agents endpoint:")
    print("   curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents")
    print()
    
    return True

def main():
    """Main function"""
    print("🚀 Starting Agents Table Schema Application")
    print("=" * 50)
    
    success = apply_agents_table_schema()
    
    if success:
        print("\n✅ Schema application instructions provided!")
        print("Please follow the steps above to create the agents table.")
    else:
        print("\n❌ Schema application failed!")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    main()
