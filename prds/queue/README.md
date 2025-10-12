# Queue PRDs

PRDs in this folder are waiting to be processed by the AI Agent Factory.

## Status: `queue`

These PRDs are:
- ✅ **Validated**: Passed initial validation checks
- ⏳ **Waiting**: Ready for agent creation workflow
- 🎯 **Next**: Will be picked up by Devin AI for processing

## What Happens Next

1. **Devin AI Processing**: PRD will be moved to `in-progress/`
2. **Agent Creation**: Devin AI will create agents based on the PRD
3. **Status Update**: Database status will change to `in_progress`
4. **Completion**: Will move to `completed/` or `failed/` when done

## File Requirements

PRDs in this folder should:
- Be in Markdown format (`.md`)
- Follow the PRD template structure
- Have all required sections completed
- Be ready for processing

## Current Queue

Check the AI Agent Factory dashboard to see:
- Number of PRDs in queue
- Estimated processing time
- Current system load
