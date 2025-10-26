-- Create Agents Table - Safe Version for Supabase
-- This version uses DO blocks to safely create types and table

-- Create agent_status enum if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_type WHERE typname = 'agent_status'
  ) THEN
    CREATE TYPE agent_status AS ENUM ('draft', 'active', 'inactive', 'deprecated', 'error');
  END IF;
END$$;

-- Create agent_health_status enum if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_type WHERE typname = 'agent_health_status'
  ) THEN
    CREATE TYPE agent_health_status AS ENUM ('healthy', 'degraded', 'unhealthy', 'unknown');
  END IF;
END$$;

-- Create agent_type enum if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_type WHERE typname = 'agent_type'
  ) THEN
    CREATE TYPE agent_type AS ENUM ('web_app', 'api_service', 'data_processor', 'automation_script', 'ai_model', 'integration', 'other');
  END IF;
END$$;

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
    
    -- Constraints for data validation
    CONSTRAINT agents_name_not_empty CHECK (length(trim(name)) > 0),
    CONSTRAINT agents_purpose_not_empty CHECK (length(trim(purpose)) > 0)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_health_status ON agents(health_status);
CREATE INDEX IF NOT EXISTS idx_agents_prd_id ON agents(prd_id);
CREATE INDEX IF NOT EXISTS idx_agents_created_at ON agents(created_at);
CREATE INDEX IF NOT EXISTS idx_agents_name ON agents(name);

-- Verify the table was created successfully
SELECT 
    'agents' as table_name,
    COUNT(*) as column_count
FROM information_schema.columns 
WHERE table_name = 'agents';

-- Show the table structure
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'agents'
ORDER BY ordinal_position;
