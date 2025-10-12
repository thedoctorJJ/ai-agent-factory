-- Add agent_type column to agents table
-- Run this in your Supabase SQL Editor

-- First, create the agent_type enum if it doesn't exist
DO $$ BEGIN
    CREATE TYPE agent_type AS ENUM ('web_app', 'api_service', 'data_processor', 'automation_script', 'ai_model', 'integration', 'other');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Add the agent_type column to the agents table
ALTER TABLE agents ADD COLUMN IF NOT EXISTS agent_type agent_type DEFAULT 'other';

-- Add a comment to document the column
COMMENT ON COLUMN agents.agent_type IS 'Type of agent (web_app, api_service, data_processor, automation_script, ai_model, integration, other)';

-- Verify the column was added
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'agents' AND column_name = 'agent_type';
