-- Update PRD Schema to Match Template Structure
-- Add missing fields to the prds table

-- Add new columns for comprehensive PRD parsing
ALTER TABLE prds ADD COLUMN IF NOT EXISTS functional_requirements TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS non_functional_requirements TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS platform_requirements TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS infrastructure_requirements TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS operational_requirements TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS agent_capabilities TEXT[];

-- Add timeline-specific fields
ALTER TABLE prds ADD COLUMN IF NOT EXISTS start_date DATE;
ALTER TABLE prds ADD COLUMN IF NOT EXISTS target_completion_date DATE;
ALTER TABLE prds ADD COLUMN IF NOT EXISTS key_milestones TEXT[];

-- Update existing columns to ensure they exist
ALTER TABLE prds ADD COLUMN IF NOT EXISTS problem_statement TEXT;
ALTER TABLE prds ADD COLUMN IF NOT EXISTS target_users TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS user_stories TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS acceptance_criteria TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS technical_requirements TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS performance_requirements JSONB;
ALTER TABLE prds ADD COLUMN IF NOT EXISTS security_requirements TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS integration_requirements TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS deployment_requirements TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS success_metrics TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS timeline TEXT;
ALTER TABLE prds ADD COLUMN IF NOT EXISTS dependencies TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS risks TEXT[];
ALTER TABLE prds ADD COLUMN IF NOT EXISTS assumptions TEXT[];

-- Add file upload fields if they don't exist
ALTER TABLE prds ADD COLUMN IF NOT EXISTS original_filename VARCHAR(255);
ALTER TABLE prds ADD COLUMN IF NOT EXISTS file_content TEXT;

-- Create indexes for new fields
CREATE INDEX IF NOT EXISTS idx_prds_start_date ON prds(start_date);
CREATE INDEX IF NOT EXISTS idx_prds_target_completion_date ON prds(target_completion_date);
CREATE INDEX IF NOT EXISTS idx_prds_original_filename ON prds(original_filename);

-- Update the prd_summary view to include new fields
DROP VIEW IF EXISTS prd_summary;
CREATE VIEW prd_summary AS
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
    start_date,
    target_completion_date,
    array_length(requirements, 1) as requirements_count,
    array_length(functional_requirements, 1) as functional_requirements_count,
    array_length(non_functional_requirements, 1) as non_functional_requirements_count,
    array_length(acceptance_criteria, 1) as acceptance_criteria_count,
    array_length(key_milestones, 1) as milestones_count
FROM prds;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO postgres;
