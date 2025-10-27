# PRD Status Standardization

## 📊 **Standardized PRD States**

This document defines the standardized PRD (Product Requirements Document) states used across the AI Agent Factory system.

## 🔄 **Complete State Flow**

### **1. `uploaded`**
- **Description**: PRD has been uploaded by a user
- **Action**: Awaiting standardization to AI Agent Factory format
- **Next Step**: Move to `standardizing` when standardization begins
- **Database Default**: ✅ **NEW DEFAULT** - All new PRDs start here

### **2. `standardizing`**
- **Description**: PRD is being converted to match AI Agent Factory standards
- **Action**: System is applying templates and adding technical requirements
- **Next Step**: Move to `review` when standardization is complete
- **Fallback**: Can return to `standardizing` if changes are needed

### **3. `review`**
- **Description**: PRD has been standardized and awaits user review
- **Action**: User must review and approve the standardized PRD
- **Next Step**: Move to `queue` when approved
- **Fallback**: Can return to `standardizing` if changes are requested

### **4. `queue`**
- **Description**: PRD is approved and ready for processing
- **Action**: Waiting to be picked up for agent creation
- **Next Step**: Move to `ready_for_devin` when ready for Devin AI
- **Previous Default**: This was the old default state

### **5. `ready_for_devin`**
- **Description**: PRD is ready to be processed by Devin AI
- **Action**: Available for Devin AI to pick up and process
- **Next Step**: Move to `in_progress` when Devin AI starts processing

### **6. `in_progress`**
- **Description**: PRD is currently being processed by Devin AI
- **Action**: Devin AI is creating the agent based on the PRD
- **Next Step**: Move to `completed` or `failed` when processing finishes

### **7. `completed`**
- **Description**: PRD has been successfully processed and agent created
- **Action**: Agent creation workflow finished successfully
- **Next Step**: Move to `processed` for final archival

### **8. `failed`**
- **Description**: PRD processing failed during agent creation
- **Action**: Processing failed, needs review and potential retry
- **Next Step**: Review error logs and retry or fix issues

### **9. `processed`**
- **Description**: PRD has completed the full workflow
- **Action**: Final state - PRD workflow is complete
- **Next Step**: Used for historical analysis and reference

## 🔧 **Implementation Details**

### **Database Schema**
```sql
CREATE TYPE prd_status AS ENUM (
    'uploaded', 
    'standardizing', 
    'review', 
    'queue', 
    'ready_for_devin', 
    'in_progress', 
    'completed', 
    'failed', 
    'processed'
);
```

### **Backend Python Models**
```python
class PRDStatus(str, Enum):
    UPLOADED = "uploaded"
    STANDARDIZING = "standardizing"
    REVIEW = "review"
    QUEUE = "queue"
    READY_FOR_DEVIN = "ready_for_devin"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PROCESSED = "processed"
```

### **Frontend TypeScript Types**
```typescript
export enum PRDStatus {
  UPLOADED = 'uploaded',
  STANDARDIZING = 'standardizing',
  REVIEW = 'review',
  QUEUE = 'queue',
  READY_FOR_DEVIN = 'ready_for_devin',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  PROCESSED = 'processed'
}
```

## 📁 **File System Organization**

The PRDs are organized in folders that correspond to their states:

```
prds/
├── uploaded/                # PRDs uploaded by users (any format)
├── standardizing/           # PRDs being converted to AI Agent Factory format
├── review/                  # PRDs awaiting user review and approval
├── queue/                   # PRDs approved and waiting for processing
├── in-progress/            # PRDs currently being processed
├── completed/               # Successfully processed PRDs
├── failed/                  # Failed PRDs
├── archive/                 # Historical PRDs
└── templates/               # Template PRDs for standardization
```

## 🔄 **State Transitions**

### **Normal Flow**
```
uploaded → standardizing → review → queue → ready_for_devin → in_progress → completed → processed
```

### **Error Handling**
```
uploaded → standardizing → review → queue → ready_for_devin → in_progress → failed
    ↓           ↓            ↓        ↓           ↓             ↓
archive/   standardizing/  archive/  failed ←─────────────────┘
           (if changes)
```

### **Retry Flow**
```
failed → queue → ready_for_devin → in_progress → completed → processed
```

## ⚠️ **Breaking Changes**

### **Database Schema Changes**
- **Old Default**: `queue` (PRDs started in queue)
- **New Default**: `uploaded` (PRDs start when uploaded)
- **Migration Required**: Existing PRDs in `queue` status remain valid

### **Service Changes**
- **PRD Creation**: New PRDs now start with `uploaded` status
- **Workflow**: Added `ready_for_devin` state for better Devin AI integration
- **Completion**: Added `processed` state for final archival

## 🧪 **Testing**

### **State Validation**
- All states are defined in database schema
- All states are implemented in backend models
- All states are defined in frontend types
- All states have corresponding file system folders

### **Workflow Testing**
- Test PRD creation starts with `uploaded` status
- Test state transitions follow the defined flow
- Test error handling moves PRDs to `failed` state
- Test completion flow moves PRDs to `processed` state

## 📝 **Migration Notes**

### **For Existing PRDs**
- PRDs currently in `queue` status remain valid
- No data migration required - all existing states are still supported
- New PRDs will use the updated workflow

### **For Developers**
- Update any hardcoded status references
- Use the new `uploaded` default for new PRDs
- Implement proper state transition logic
- Update UI to handle all 9 states

## 🎯 **Benefits of Standardization**

1. **Consistency**: All parts of the system use the same state definitions
2. **Clarity**: Clear workflow from upload to completion
3. **Traceability**: Better tracking of PRD progress
4. **Error Handling**: Proper failure states and retry mechanisms
5. **Integration**: Better Devin AI integration with `ready_for_devin` state
6. **Archival**: Proper completion with `processed` state

## 🔮 **Future Enhancements**

- **State History**: Track state transition history
- **Automated Transitions**: Automatic state transitions based on conditions
- **State Notifications**: Notify users of state changes
- **State Analytics**: Analyze PRD processing patterns
- **State Permissions**: Role-based state transition permissions
