# Review PRDs

This folder contains PRDs that have been standardized and are awaiting user review and approval.

## Purpose

After PRDs are converted to AI Agent Factory format, users must review and approve them before they can be processed. This ensures:

- Original intent is preserved
- Technical additions are appropriate
- User agrees with the standardized format
- Quality control before processing

## What Users Review

### **Content Accuracy**
- Verify original requirements are preserved
- Check that user intent is maintained
- Ensure no important details were lost

### **Technical Additions**
- Review added infrastructure details (FastAPI, Supabase, Google Cloud Run, etc.)
- Check integration requirements (MCP protocol, GitHub, etc.)
- Verify security and deployment specifications

### **Structure Changes**
- Confirm the standardized format meets their needs
- Check that all sections are properly filled
- Ensure completeness of the PRD

## Review Actions

### **Approve** ✅
- Move PRD to `queue/` folder for processing
- PRD will be picked up by Devin AI for agent creation

### **Request Changes** 🔄
- Move PRD back to `standardizing/` folder
- Provide feedback on what needs to be changed
- System will re-standardize with user feedback

### **Reject** ❌
- Move PRD to `archive/` folder
- PRD will not be processed
- Use for PRDs that are not suitable for the platform

## Review Benefits

- **Quality Control**: Ensures PRDs meet user expectations
- **Transparency**: Users see exactly what will be processed
- **Collaboration**: Allows for iterative improvement
- **Confidence**: Users can proceed knowing the PRD is correct

## Status

- **Status**: `review`
- **Action**: Awaiting user review and sign-off
- **Next Step**: Will move to `queue/` when approved, or back to `standardizing/` if changes needed
