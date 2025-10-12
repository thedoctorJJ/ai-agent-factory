-- AI Agent Factory Database Schema - Updated to Match PRD Templates
-- Supabase PostgreSQL Schema for persistent data storage

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types
CREATE TYPE prd_type AS ENUM ('platform', 'agent');
CREATE TYPE prd_status AS ENUM ('queue', 'ready_for_devin', 'in_progress', 'completed', 'failed', 'processed');
CREATE TYPE prd_priority AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE prd_effort AS ENUM ('small', 'medium', 'large', 'epic');
CREATE TYPE agent_status AS ENUM ('draft', 'active', 'inactive', 'deprecated', 'error');
CREATE TYPE agent_health_status AS ENUM ('healthy', 'degraded', 'unhealthy', 'unknown');
CREATE TYPE agent_type AS ENUM ('web_app', 'api_service', 'data_processor', 'automation_script', 'ai_model', 'integration', 'other');
CREATE TYPE devin_task_status AS ENUM ('pending', 'in_devin', 'completed', 'failed', 'cancelled');

-- PRDs Table - Updated to match PRD template structure
CREATE TABLE IF NOT EXISTS prds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    prd_type prd_type NOT NULL DEFAULT 'agent',
    status prd_status NOT NULL DEFAULT 'queue',
    github_repo_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Core PRD Template Fields
    problem_statement TEXT,
    target_users TEXT[],
    user_stories TEXT[],
    
    -- Requirements (from templates)
    requirements TEXT[], -- General requirements
    functional_requirements TEXT[], -- Functional requirements (from templates)
    non_functional_requirements TEXT[], -- Non-functional requirements (from templates)
    platform_requirements TEXT[], -- Platform-specific requirements
    infrastructure_requirements TEXT[], -- Infrastructure requirements
    operational_requirements TEXT[], -- Operational requirements
    agent_capabilities TEXT[], -- Agent-specific capabilities
    
    -- Acceptance and Technical
    acceptance_criteria TEXT[],
    technical_requirements TEXT[],
    
    -- Performance and Security
    performance_requirements JSONB,
    security_requirements TEXT[],
    integration_requirements TEXT[],
    deployment_requirements TEXT[],
    
    -- Success and Timeline
    success_metrics TEXT[],
    timeline TEXT, -- General timeline text
    start_date DATE,
    target_completion_date DATE,
    key_milestones TEXT[],
    
    -- Dependencies and Risk Management
    dependencies TEXT[],
    risks TEXT[],
    assumptions TEXT[],
    
    -- Roadmap-specific fields
    category VARCHAR(100),
    priority prd_priority,
    effort_estimate prd_effort,
    business_value INTEGER CHECK (business_value >= 1 AND business_value <= 10),
    technical_complexity INTEGER CHECK (technical_complexity >= 1 AND technical_complexity <= 10),
    dependencies_list TEXT[],
    assignee VARCHAR(255),
    target_sprint VARCHAR(100),
    
    -- File upload fields
    original_filename VARCHAR(255),
    file_content TEXT,
    
    -- Indexes for performance
    CONSTRAINT prds_title_not_empty CHECK (length(trim(title)) > 0),
    CONSTRAINT prds_description_not_empty CHECK (length(trim(description)) > 0)
);

-- Agents Table
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

-- Devin Tasks Table
CREATE TABLE IF NOT EXISTS devin_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    prd_id UUID REFERENCES prds(id) ON DELETE CASCADE,
    status devin_task_status NOT NULL DEFAULT 'pending',
    devin_output TEXT,
    agent_code TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes for performance
    CONSTRAINT devin_tasks_title_not_empty CHECK (length(trim(title)) > 0)
);

-- Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    user_id VARCHAR(255),
    details JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes for performance
    INDEX idx_audit_logs_entity (entity_type, entity_id),
    INDEX idx_audit_logs_timestamp (timestamp)
);

-- System Metrics Table
CREATE TABLE IF NOT EXISTS system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    metric_unit VARCHAR(50),
    tags JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes for performance
    INDEX idx_system_metrics_name (metric_name),
    INDEX idx_system_metrics_timestamp (timestamp)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_prds_status ON prds(status);
CREATE INDEX IF NOT EXISTS idx_prds_type ON prds(prd_type);
CREATE INDEX IF NOT EXISTS idx_prds_created_at ON prds(created_at);
CREATE INDEX IF NOT EXISTS idx_prds_priority ON prds(priority);
CREATE INDEX IF NOT EXISTS idx_prds_category ON prds(category);

CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(agent_type);
CREATE INDEX IF NOT EXISTS idx_agents_prd_id ON agents(prd_id);
CREATE INDEX IF NOT EXISTS idx_agents_created_at ON agents(created_at);

CREATE INDEX IF NOT EXISTS idx_devin_tasks_status ON devin_tasks(status);
CREATE INDEX IF NOT EXISTS idx_devin_tasks_prd_id ON devin_tasks(prd_id);
CREATE INDEX IF NOT EXISTS idx_devin_tasks_created_at ON devin_tasks(created_at);

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_prds_updated_at BEFORE UPDATE ON prds
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_devin_tasks_updated_at BEFORE UPDATE ON devin_tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create views for common queries
CREATE OR REPLACE VIEW prd_summary AS
SELECT 
    id,
    title,
    description,
    prd_type,
    status,
    priority,
    category,
    created_at,
    updated_at,
    array_length(requirements, 1) as requirements_count,
    array_length(acceptance_criteria, 1) as acceptance_criteria_count
FROM prds;

CREATE OR REPLACE VIEW agent_summary AS
SELECT 
    a.id,
    a.name,
    a.description,
    a.agent_type,
    a.status,
    a.health_status,
    a.created_at,
    a.updated_at,
    p.title as prd_title,
    p.prd_type as prd_type
FROM agents a
LEFT JOIN prds p ON a.prd_id = p.id;

-- Create functions for common operations
CREATE OR REPLACE FUNCTION get_prd_status_values()
RETURNS TABLE(status_value prd_status) AS $$
BEGIN
    RETURN QUERY SELECT unnest(enum_range(NULL::prd_status));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_agent_status_values()
RETURNS TABLE(status_value agent_status) AS $$
BEGIN
    RETURN QUERY SELECT unnest(enum_range(NULL::agent_status));
END;
$$ LANGUAGE plpgsql;

-- Row Level Security (RLS) policies
ALTER TABLE prds ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE devin_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_metrics ENABLE ROW LEVEL SECURITY;

-- Create policies (adjust based on your authentication system)
CREATE POLICY "Enable read access for all users" ON prds FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON prds FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update access for all users" ON prds FOR UPDATE USING (true);
CREATE POLICY "Enable delete access for all users" ON prds FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON agents FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON agents FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update access for all users" ON agents FOR UPDATE USING (true);
CREATE POLICY "Enable delete access for all users" ON agents FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON devin_tasks FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON devin_tasks FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update access for all users" ON devin_tasks FOR UPDATE USING (true);
CREATE POLICY "Enable delete access for all users" ON devin_tasks FOR DELETE USING (true);

-- Sample data for testing (optional)
INSERT INTO prds (title, description, prd_type, status, problem_statement, target_users, requirements, acceptance_criteria, technical_requirements, success_metrics, timeline, dependencies, risks, assumptions) VALUES
('Sample AI Agent PRD', 'A sample PRD for testing the system', 'agent', 'queue', 'Need for automated customer support', ARRAY['Customer Service Team', 'End Users'], ARRAY['Handle customer inquiries', 'Provide 24/7 support'], ARRAY['Response time under 2 seconds', '95% accuracy rate'], ARRAY['FastAPI backend', 'PostgreSQL database'], ARRAY['Reduced support tickets', 'Improved customer satisfaction'], '4 weeks development', ARRAY['Customer service training data'], ARRAY['Data privacy concerns'], ARRAY['Customers will adopt the system']);

-- Grant permissions (adjust based on your setup)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO postgres;
