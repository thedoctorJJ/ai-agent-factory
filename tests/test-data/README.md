# Test Data Management

This directory contains scripts for creating and managing test data for the AI Agent Factory. All test data is clearly marked and can be easily identified and removed.

## 🎯 Purpose

These scripts demonstrate the **one-to-many PRD-to-Agent relationship** where:
- A single PRD can produce multiple agents at Devin's discretion
- Agents are properly grouped and displayed by their source PRD
- The UI shows agent counts on PRD cards
- Agents can be viewed both individually and grouped by PRD

## 📁 Files

### `create-agents-via-api.py`
Creates test agents via API calls to demonstrate the one-to-many relationship:
- **3 agents** from "Database Integration with Supabase" PRD
- **2 agents** from "JWT Authentication System" PRD  
- **1 agent** from "Comprehensive Testing Suite" PRD
- **1 standalone agent** (no PRD reference)

All test agents have names starting with `TEST_` for easy identification.

### `restart-and-clear.sh` ⭐ **Recommended Cleanup Method**
The most reliable way to clear all data and start fresh:
- Stops the backend service
- Clears all in-memory storage
- Restarts the backend
- Verifies the data is cleared

### `cleanup-via-ui.py`
Removes all test data using the same API endpoints as the UI.

### `clear-database.py`
Directly clears the Supabase database tables (nuclear option).

### `check-supabase-agents.py`
Checks what's actually stored in the Supabase database.

## 🚀 Usage

### Create Test Data
```bash
# From the project root
cd backend
source venv/bin/activate
python ../tests/test-data/create-agents-via-api.py
```

### Clean Up Test Data ⭐ **Recommended**
```bash
# From the project root
./tests/test-data/restart-and-clear.sh
```

**Alternative cleanup methods:**
```bash
# Via API endpoints (same as UI)
python tests/test-data/cleanup-via-ui.py

# Direct database cleanup
python tests/test-data/clear-database.py
```

### Check Data Status
```bash
# Check what's in Supabase
python tests/test-data/check-supabase-agents.py

# Check what the API returns
curl http://localhost:8000/api/v1/agents | jq '.agents | length'
```

## 🔍 What You'll See

After creating test data, the UI will demonstrate:

### PRD Cards
- **Agent count badges** showing how many agents were created from each PRD
- **"View Agents" buttons** to jump to the agents section
- Clear indication of the one-to-many relationship

### Agents Tab
- **Grouped display** by PRD with headers showing the source PRD
- **Agent numbering** when multiple agents exist per PRD (e.g., "Agent 1 of 3")
- **Standalone agents section** for agents without PRD references
- **Enhanced descriptions** that include agent numbering

### Navigation
- **Smooth scrolling** from PRD cards to related agents
- **Cross-references** between PRDs and their created agents
- **Organized layout** that makes the relationship clear

## 🧹 Cleanup - Important!

### Why Agents Sometimes Persist After Deletion

The system uses a fallback to **in-memory storage** when database operations fail (e.g., schema mismatches). This means:

1. **Agents may be stored in memory** instead of the database
2. **Deleting via UI removes them from memory** but they persist until the backend restarts
3. **Page refreshes don't clear in-memory storage** - only a backend restart does

**Solution:** Always use `restart-and-clear.sh` when you need a truly clean slate. This script:
1. Stops the backend (clearing in-memory storage)
2. Restarts the backend fresh
3. Verifies all data is cleared

## ⚠️ Important Notes

- **Test data is clearly marked** with `TEST_` prefixes and `test_data: true` flags
- **Easy to identify** and remove without affecting real data
- **Safe to run** - only affects test data, not production data
- **Reversible** - you can recreate test data anytime
- **Use restart-and-clear.sh for reliable cleanup** - it's the only way to fully clear in-memory storage

## 🎨 UI Features Demonstrated

1. **One-to-Many Relationship Display**
   - PRD cards show agent counts
   - Agents grouped by source PRD
   - Clear visual hierarchy

2. **Enhanced Navigation**
   - Jump from PRD to agents
   - Cross-reference between related items
   - Smooth scrolling and transitions

3. **Improved Organization**
   - Logical grouping of related agents
   - Clear separation of standalone agents
   - Intuitive information architecture

4. **Better User Experience**
   - Agent numbering for multiple agents per PRD
   - Enhanced descriptions with context
   - Visual indicators for relationships
