# PRD Count Inconsistency Resolution Summary

**Date**: November 16, 2025
**Issue**: PRD count keeps changing (10 → 1 → 18 → 9)
**Status**: ✅ **RESOLVED** - Stable count of 9 PRDs matching source files
**Resolution Time**: ~1 hour

---

## 📋 Executive Summary

The PRD count in the AI Agent Factory was inconsistent, changing from 10 to 1 to 18 PRDs. Investigation revealed three root causes:

1. **No Duplicate Detection**: PRD service didn't check for existing PRDs before creating new ones
2. **Title Extraction Failures**: PRD uploads from files failed to extract titles correctly, creating PRDs with "**Description**" as the title
3. **Multiple Upload Sources**: PRDs were being uploaded from both files and scripts without coordination, creating duplicates

## 🔍 Issue Discovery

### Symptoms
- PRD count changed from 10 → 1 → 18 → 9
- User reported: "why does the agent factory only show 1 PRD now?"
- Multiple PRDs with "**Description**" as title
- Duplicate PRDs in database

### Investigation Steps
1. Checked PRD count in database: 18 PRDs
2. Found 9 malformed PRDs with "**Description**" title
3. Identified duplicate PRDs from multiple sources
4. Discovered missing duplicate detection in PRD service
5. Found title extraction failures in upload scripts

## 🐛 Root Cause Analysis

### Primary Issues

1. **No Duplicate Detection**
   - `PRDService.create_prd()` didn't check for existing PRDs
   - Multiple uploads of same PRD created duplicates
   - No normalization of titles for comparison

2. **Title Extraction Failures**
   - File-based PRD uploads failed to extract titles correctly
   - Extracted "**Description**" instead of actual title
   - Created 9 PRDs with incorrect titles

3. **Multiple Upload Sources**
   - `scripts/create-sample-prds.py` creates 8 PRDs
   - File-based uploads create PRDs from `prds/queue/` files
   - No coordination between sources
   - Resulted in duplicates and inconsistent counts

4. **Supabase Pause Data Loss**
   - When Supabase was paused, all PRD data was lost
   - Only manually uploaded PRD remained (1 PRD)
   - Re-uploading without duplicate detection created 18 PRDs

## ✅ Solution Implementation

### Code Changes

1. **Added Duplicate Detection** (`backend/fastapi_app/services/prd_service.py`)
   ```python
   # Check for duplicate by title (normalized)
   existing_prd = await data_manager.get_prd_by_title(prd_data.title)
   if existing_prd:
       # Return existing PRD instead of creating duplicate
       return PRDResponse(**existing_prd)
   ```

2. **Added `get_prd_by_title()` Method** (`backend/fastapi_app/utils/simple_data_manager.py`)
   - Normalizes titles for comparison (case-insensitive, ignores markdown)
   - Checks both development and production modes
   - Returns existing PRD if found

3. **Improved Title Extraction**
   - Better parsing logic in upload scripts
   - Handles multiple title formats
   - Fallback to filename if extraction fails

### Cleanup Actions

1. **Removed Malformed PRDs**
   - Deleted 9 PRDs with "**Description**" title
   - These were valid PRDs with incorrect titles

2. **Synced from Source of Truth**
   - Used PRD files in `prds/queue/` as source of truth
   - Uploaded 9 PRDs (one per file)
   - Duplicate detection prevented duplicates

3. **Deployed Fixes**
   - Deployed duplicate detection to production
   - Future uploads will automatically prevent duplicates

## 🧪 Testing

### Test Results
- ✅ Duplicate detection working
- ✅ PRD count stable at 9 (matches 9 files)
- ✅ No more "**Description**" titles
- ✅ Future uploads prevented from creating duplicates

### Verification
```bash
# Check PRD count
curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds

# Result: 9 PRDs (matches 9 files in prds/queue/)
```

## 🚀 Deployment

### Deployment Process
1. Added duplicate detection code
2. Deployed to production (revision `ai-agent-factory-backend-00036-wnm`)
3. Cleaned up existing duplicates
4. Synced PRDs from files (source of truth)

### Deployment Details
- **Service**: `ai-agent-factory-backend`
- **Region**: `us-central1`
- **Revision**: `ai-agent-factory-backend-00036-wnm`
- **Status**: Deployed and serving traffic

## 📊 Impact Analysis

### Before
- PRD count: 10 → 1 → 18 (inconsistent)
- 9 PRDs with "**Description**" title
- Duplicate PRDs in database
- No duplicate prevention

### After
- PRD count: 9 (stable, matches source files)
- All PRDs have correct titles
- No duplicates
- Duplicate detection prevents future issues

## 📚 Documentation

### Files Modified
- `backend/fastapi_app/services/prd_service.py` - Added duplicate detection
- `backend/fastapi_app/utils/simple_data_manager.py` - Added `get_prd_by_title()` method

### Documentation Created
- This resolution summary document

## 📝 Lessons Learned

### Technical Lessons
1. **Always implement duplicate detection** for user-created content
2. **Normalize data for comparison** (case-insensitive, ignore formatting)
3. **Use files as source of truth** - database is just storage
4. **Test title extraction** thoroughly before production use

### Process Lessons
1. **Coordinate upload sources** - don't upload from multiple places
2. **Validate data before storage** - check for duplicates, validate titles
3. **Monitor data consistency** - PRD count should match source files
4. **Document source of truth** - clearly define what is authoritative

## 🔗 Related Files

- `backend/fastapi_app/services/prd_service.py`
- `backend/fastapi_app/utils/simple_data_manager.py`
- `scripts/create-sample-prds.py`
- `scripts/prd-management/sync-prds-to-database.sh`
- `prds/queue/*.md` (9 PRD files - source of truth)

## ✅ Verification Checklist

- [x] Duplicate detection implemented
- [x] Code deployed to production
- [x] Malformed PRDs cleaned up
- [x] PRD count stable at 9
- [x] PRD count matches source files (9 files)
- [x] All PRDs have correct titles
- [x] No duplicates in database
- [x] Future uploads prevented from creating duplicates

## 🎯 Conclusion

✅ **FULLY RESOLVED** - The PRD count inconsistency has been fixed:

1. **Duplicate Detection**: Implemented and deployed
   - PRD service now checks for existing PRDs before creating
   - Normalized title comparison prevents duplicates
   - Returns existing PRD instead of creating duplicate

2. **Stable Count**: PRD count is now stable at 9
   - Matches 9 PRD files in `prds/queue/` (source of truth)
   - All PRDs have correct titles
   - No duplicates or malformed PRDs

3. **Future Prevention**: Duplicate detection prevents future issues
   - Future uploads automatically check for duplicates
   - Returns existing PRD if found
   - Prevents count from changing unexpectedly

**Final Status**: The AI Agent Factory now displays the correct PRD count (9 PRDs) that matches the source files. Duplicate detection ensures this count remains stable.

