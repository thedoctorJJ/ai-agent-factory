# Manual Devin Workflow Guide

This guide explains how to use the AI Agent Factory with Devin AI in a manual workflow, which is perfect for users who don't have API access to Devin AI but still want to leverage its capabilities.

## Overview

The Manual Devin Workflow allows you to:
1. Create and manage PRDs in the AI Agent Factory
2. Mark PRDs as ready for Devin AI processing
3. Manually start Devin AI and point it to your Supabase database
4. Let Devin AI read and process your PRDs
5. Monitor the results in your dashboard

## Prerequisites

- AI Agent Factory running locally or deployed
- Supabase database configured and accessible
- Devin AI account (any plan level)
- Access to your Supabase project dashboard

## Step-by-Step Workflow

### 1. Create PRDs

Start by creating PRDs in your AI Agent Factory:

1. **Navigate to the dashboard** at http://localhost:3000
2. **Go to the "Submit PRD" tab**
3. **Create a new PRD** by either:
   - Uploading a markdown file
   - Pasting PRD content directly
   - Using the guided form

### 2. Mark PRDs as Ready for Devin

Once you have PRDs created:

1. **Go to the "PRD Repository" tab**
2. **Find PRDs you want Devin to process**
3. **Click the "Ready for Devin" button** on each PRD
4. **Verify the status changes** to "Ready for Devin" (🤖 icon)

### 3. Prepare Devin AI

Before starting Devin AI:

1. **Note your Supabase credentials**:
   - Project URL: Found in your Supabase dashboard
   - Service Role Key: Found in Settings > API
   - Database connection details

2. **Prepare Devin AI context**:
   - Tell Devin about your AI Agent Factory project
   - Explain that you want it to process PRDs from your Supabase database
   - Provide the database connection information

### 4. Start Devin AI Manually

1. **Open Devin AI** in your browser
2. **Start a new project**
3. **Give Devin the following context**:

```
I have an AI Agent Factory project with PRDs stored in a Supabase database. 
I need you to:

1. Connect to my Supabase database using these credentials:
   - URL: [YOUR_SUPABASE_URL]
   - Service Role Key: [YOUR_SERVICE_ROLE_KEY]

2. Query the 'prds' table for records where status = 'ready_for_devin'

3. For each PRD found:
   - Read the PRD content and requirements
   - Create the corresponding AI agent based on the specifications
   - Update the PRD status to 'completed' when done
   - Create any necessary repositories or deployments

The PRDs contain detailed technical requirements, user stories, and acceptance criteria.
```

### 5. Devin AI Processing

Devin AI will:

1. **Connect to your Supabase database**
2. **Query for PRDs with `ready_for_devin` status**
3. **Read and analyze each PRD**
4. **Create agents based on the specifications**
5. **Update PRD status to `completed`**
6. **Provide progress updates**

### 6. Monitor Progress

While Devin AI is working:

1. **Check your dashboard** at http://localhost:3000
2. **Monitor the "PRD Repository" tab** for status changes
3. **View created agents** in the "Agents" tab
4. **Use the API endpoints** to get real-time updates:
   - `GET /api/v1/prds/ready-for-devin` - See what Devin is processing
   - `GET /api/v1/agents` - View created agents

## API Endpoints for Manual Workflow

### Mark PRD as Ready for Devin
```bash
POST /api/v1/prds/{prd_id}/ready-for-devin
```

**Response:**
```json
{
  "message": "PRD marked as ready for Devin AI",
  "prd_id": "uuid",
  "status": "ready_for_devin",
  "prd": { /* PRD object */ }
}
```

### Get PRDs Ready for Devin
```bash
GET /api/v1/prds/ready-for-devin
```

**Response:**
```json
{
  "message": "PRDs ready for Devin AI",
  "count": 1,
  "prds": [
    {
      "id": "uuid",
      "title": "PRD Title",
      "status": "ready_for_devin",
      /* ... other PRD fields */
    }
  ]
}
```

### Get All PRDs (with status filtering)
```bash
GET /api/v1/prds?status=ready_for_devin
```

## Database Schema

The manual workflow uses a new PRD status in the database:

```sql
-- PRD Status Enum (updated)
CREATE TYPE prd_status AS ENUM (
  'queue',
  'ready_for_devin',  -- New status for manual workflow
  'in_progress',
  'completed',
  'failed',
  'processed'
);
```

## Troubleshooting

### Common Issues

1. **"PRD not found" error**:
   - Ensure the PRD ID is correct
   - Check that the PRD exists in the database

2. **Database connection issues**:
   - Verify Supabase credentials are correct
   - Check that the database schema is updated with the new status

3. **Devin AI can't connect**:
   - Double-check the Supabase URL and service role key
   - Ensure the service role key has the correct permissions

4. **Status not updating**:
   - Check that the database schema includes the `ready_for_devin` status
   - Verify the API endpoints are working correctly

### Database Schema Update

If you need to update your database schema:

1. **Go to your Supabase dashboard**
2. **Navigate to SQL Editor**
3. **Run this command**:
   ```sql
   ALTER TYPE prd_status ADD VALUE 'ready_for_devin';
   ```

## Best Practices

1. **Batch Processing**: Mark multiple PRDs as ready before starting Devin AI
2. **Clear Communication**: Provide Devin AI with clear context about your project
3. **Monitor Progress**: Regularly check the dashboard for status updates
4. **Backup Data**: Ensure your Supabase database is properly backed up
5. **Test First**: Try the workflow with a simple PRD before processing complex ones

## Example Devin AI Prompt

Here's a complete example prompt you can give to Devin AI:

```
I have an AI Agent Factory project that creates AI agents from Product Requirements Documents (PRDs). 

The PRDs are stored in a Supabase PostgreSQL database. I need you to:

1. Connect to my Supabase database:
   - URL: https://ssdcbhxctakgysnayzeq.supabase.co
   - Service Role Key: [YOUR_SERVICE_ROLE_KEY]

2. Query the 'prds' table for records where status = 'ready_for_devin'

3. For each PRD you find:
   - Read the full PRD content (title, description, requirements, technical specs, etc.)
   - Create the corresponding AI agent based on the specifications
   - Use the technical requirements and user stories to guide implementation
   - Update the PRD status to 'completed' when the agent is created
   - Provide a summary of what was created

The PRDs contain detailed information including:
- Problem statement and target users
- User stories and acceptance criteria
- Technical requirements and architecture
- Success metrics and timeline

Please start by connecting to the database and showing me what PRDs are ready for processing.
```

## Support

If you encounter issues with the manual Devin workflow:

1. Check the [troubleshooting section](#troubleshooting) above
2. Review the API documentation at http://localhost:8000/docs
3. Check the backend logs for error messages
4. Verify your Supabase database connection and schema

The manual Devin workflow provides a flexible way to leverage Devin AI's capabilities even without direct API access, making the AI Agent Factory accessible to users on any Devin AI plan.
