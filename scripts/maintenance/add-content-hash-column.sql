-- Add content_hash column to prds table for duplicate detection
-- This provides deterministic duplicate detection based on content

-- Add column (allow NULL initially for backfill)
ALTER TABLE prds ADD COLUMN IF NOT EXISTS content_hash VARCHAR(64);

-- Create index for fast lookup
CREATE INDEX IF NOT EXISTS idx_prds_content_hash ON prds(content_hash);

-- Note: We'll add UNIQUE constraint after backfilling existing PRDs
-- ALTER TABLE prds ADD CONSTRAINT unique_content_hash UNIQUE (content_hash);

