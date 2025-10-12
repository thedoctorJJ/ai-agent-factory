-- Update PRD Status Enum to include 'ready_for_devin'
-- Run this in your Supabase SQL Editor

-- Add the new status value to the existing enum
ALTER TYPE prd_status ADD VALUE 'ready_for_devin';

-- Verify the enum values
SELECT unnest(enum_range(NULL::prd_status)) as prd_status_values;
