-- AI Agent Factory Database Schema
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
CREATE TYPE devin_task_status AS ENUM ('pending', 'in_devin', 'completed', 'failed', 'cancelled');

-- PRDs Table
CREATE TABLE IF NOT EXISTS prds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT[] DEFAULT '{}',
    prd_type prd_type NOT NULL DEFAULT 'agent',
    status prd_status NOT NULL DEFAULT 'queue',
    github_repo_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Enhanced PRD sections
    problem_statement TEXT,
    target_users TEXT[],
    user_stories TEXT[],
    acceptance_criteria TEXT[],
    technical_requirements TEXT[],
    performance_requirements JSONB,
    security_requirements TEXT[],
    integration_requirements TEXT[],
    deployment_requirements TEXT[],
    success_metrics TEXT[],
    timeline TEXT,
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
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}',
    
    -- Indexes for performance
    CONSTRAINT devin_tasks_title_not_empty CHECK (length(trim(title)) > 0)
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    old_values JSONB,
    new_values JSONB,
    user_id VARCHAR(255),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- System Metrics Table
CREATE TABLE IF NOT EXISTS system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    metric_unit VARCHAR(50),
    tags JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_prds_status ON prds(status);
CREATE INDEX IF NOT EXISTS idx_prds_type ON prds(prd_type);
CREATE INDEX IF NOT EXISTS idx_prds_priority ON prds(priority);
CREATE INDEX IF NOT EXISTS idx_prds_created_at ON prds(created_at);
CREATE INDEX IF NOT EXISTS idx_prds_updated_at ON prds(updated_at);
CREATE INDEX IF NOT EXISTS idx_prds_requirements ON prds USING GIN(requirements);
CREATE INDEX IF NOT EXISTS idx_prds_target_users ON prds USING GIN(target_users);
CREATE INDEX IF NOT EXISTS idx_prds_user_stories ON prds USING GIN(user_stories);
CREATE INDEX IF NOT EXISTS idx_prds_acceptance_criteria ON prds USING GIN(acceptance_criteria);
CREATE INDEX IF NOT EXISTS idx_prds_technical_requirements ON prds USING GIN(technical_requirements);

CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_health_status ON agents(health_status);
CREATE INDEX IF NOT EXISTS idx_agents_prd_id ON agents(prd_id);
CREATE INDEX IF NOT EXISTS idx_agents_created_at ON agents(created_at);
CREATE INDEX IF NOT EXISTS idx_agents_updated_at ON agents(updated_at);
CREATE INDEX IF NOT EXISTS idx_agents_capabilities ON agents USING GIN(capabilities);

CREATE INDEX IF NOT EXISTS idx_devin_tasks_status ON devin_tasks(status);
CREATE INDEX IF NOT EXISTS idx_devin_tasks_prd_id ON devin_tasks(prd_id);
CREATE INDEX IF NOT EXISTS idx_devin_tasks_created_at ON devin_tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_devin_tasks_updated_at ON devin_tasks(updated_at);

CREATE INDEX IF NOT EXISTS idx_audit_logs_table_record ON audit_logs(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);

CREATE INDEX IF NOT EXISTS idx_system_metrics_name_timestamp ON system_metrics(metric_name, timestamp);
CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_prds_updated_at BEFORE UPDATE ON prds
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_devin_tasks_updated_at BEFORE UPDATE ON devin_tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create audit trigger function
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (table_name, record_id, action, new_values, timestamp)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW), NOW());
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (table_name, record_id, action, old_values, new_values, timestamp)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW), NOW());
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_logs (table_name, record_id, action, old_values, timestamp)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD), NOW());
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Create audit triggers
CREATE TRIGGER audit_prds_trigger
    AFTER INSERT OR UPDATE OR DELETE ON prds
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_agents_trigger
    AFTER INSERT OR UPDATE OR DELETE ON agents
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_devin_tasks_trigger
    AFTER INSERT OR UPDATE OR DELETE ON devin_tasks
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Row Level Security (RLS) policies
ALTER TABLE prds ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE devin_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_metrics ENABLE ROW LEVEL SECURITY;

-- Create policies for service role access (for API operations)
CREATE POLICY "Service role can do everything on prds" ON prds
    FOR ALL USING (true);

CREATE POLICY "Service role can do everything on agents" ON agents
    FOR ALL USING (true);

CREATE POLICY "Service role can do everything on devin_tasks" ON devin_tasks
    FOR ALL USING (true);

CREATE POLICY "Service role can do everything on audit_logs" ON audit_logs
    FOR ALL USING (true);

CREATE POLICY "Service role can do everything on system_metrics" ON system_metrics
    FOR ALL USING (true);

-- Create views for common queries
CREATE OR REPLACE VIEW prd_summary AS
SELECT 
    p.id,
    p.title,
    p.prd_type,
    p.status,
    p.priority,
    p.created_at,
    p.updated_at,
    COUNT(a.id) as agent_count,
    COUNT(dt.id) as task_count
FROM prds p
LEFT JOIN agents a ON a.prd_id = p.id
LEFT JOIN devin_tasks dt ON dt.prd_id = p.id
GROUP BY p.id, p.title, p.prd_type, p.status, p.priority, p.created_at, p.updated_at;

CREATE OR REPLACE VIEW agent_summary AS
SELECT 
    a.id,
    a.name,
    a.status,
    a.health_status,
    a.created_at,
    a.updated_at,
    a.last_health_check,
    p.title as prd_title,
    p.status as prd_status
FROM agents a
LEFT JOIN prds p ON p.id = a.prd_id;

-- Insert sample data for testing
INSERT INTO prds (id, title, description, requirements, prd_type, status, priority, problem_statement, target_users, user_stories, acceptance_criteria, technical_requirements, success_metrics) VALUES
(
    '550e8400-e29b-41d4-a716-446655440001',
    'Database Integration with Supabase',
    'This agent integrates the AI Agent Factory with a persistent Supabase PostgreSQL backend, replacing volatile in-memory storage.',
    ARRAY[
        'Establish a secure and authenticated connection with Supabase PostgreSQL',
        'Design and implement normalized data models for AI Agents and PRDs',
        'Implement CRUD operations through a well-defined data access layer',
        'Add database migration, schema validation, and rollback capabilities',
        'Configure connection pooling, retry logic, and transaction management'
    ],
    'platform',
    'queue',
    'high',
    'The AI Agent Factory currently uses in-memory storage, causing all data to be lost after system restarts and limiting scalability.',
    ARRAY['AI Agents', 'AI Agent Developers', 'Product Managers'],
    ARRAY[
        'As an AI Agent, I need to persist my configuration, learning history, and state across sessions',
        'As an AI Agent Developer, I want to create, update, and manage agent and PRD data in a reliable Supabase backend',
        'As a Product Manager, I need access to consistent and historical agent data to monitor performance'
    ],
    ARRAY[
        'All AI Agent and PRD entities are stored and retrieved persistently through Supabase',
        'System restarts or crashes do not result in any data loss',
        'All CRUD operations pass integration and end-to-end tests with 100% reliability',
        'Database migrations execute successfully in both development and production environments'
    ],
    ARRAY[
        'Backend: Python 3.11 using FastAPI, deployed as a containerized microservice on Google Cloud Run',
        'Database: Supabase (PostgreSQL) serves as the persistent data layer',
        'ORM / Schema Management: Alembic for database migrations and Supabase CLI for schema synchronization',
        'Authentication & Security: JWT-based authentication and Supabase service role keys'
    ],
    ARRAY[
        '100% data persistence across restarts and deployments',
        'Average database query response time: <200ms under standard load',
        'API response time (read/write operations): <300ms p95',
        '0 failed migrations in production or staging environments'
    ]
) ON CONFLICT (id) DO NOTHING;

-- Create functions for common operations
CREATE OR REPLACE FUNCTION get_agent_health_summary()
RETURNS TABLE (
    total_agents BIGINT,
    healthy_agents BIGINT,
    degraded_agents BIGINT,
    unhealthy_agents BIGINT,
    unknown_agents BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) as total_agents,
        COUNT(*) FILTER (WHERE health_status = 'healthy') as healthy_agents,
        COUNT(*) FILTER (WHERE health_status = 'degraded') as degraded_agents,
        COUNT(*) FILTER (WHERE health_status = 'unhealthy') as unhealthy_agents,
        COUNT(*) FILTER (WHERE health_status = 'unknown') as unknown_agents
    FROM agents;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_prd_status_summary()
RETURNS TABLE (
    total_prds BIGINT,
    queue_prds BIGINT,
    in_progress_prds BIGINT,
    completed_prds BIGINT,
    failed_prds BIGINT,
    processed_prds BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) as total_prds,
        COUNT(*) FILTER (WHERE status = 'queue') as queue_prds,
        COUNT(*) FILTER (WHERE status = 'in_progress') as in_progress_prds,
        COUNT(*) FILTER (WHERE status = 'completed') as completed_prds,
        COUNT(*) FILTER (WHERE status = 'failed') as failed_prds,
        COUNT(*) FILTER (WHERE status = 'processed') as processed_prds
    FROM prds;
END;
$$ LANGUAGE plpgsql;