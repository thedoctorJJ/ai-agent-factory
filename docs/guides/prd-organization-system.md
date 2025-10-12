# PRD Organization System

This guide explains the comprehensive PRD organization system implemented in the AI Agent Factory, which provides both file-based and database-based management of Product Requirements Documents.

## 🎯 Overview

The PRD Organization System provides:
- **File-based organization** for easy browsing and management
- **Database synchronization** for structured data and API access
- **Status-based workflow** that mirrors the agent creation process
- **Management tools** for efficient PRD operations

## 📁 Folder Structure

```
prds/
├── queue/              # PRDs waiting to be processed
├── in-progress/        # PRDs currently being processed
├── completed/          # Successfully processed PRDs
├── failed/             # PRDs that failed processing
├── archive/            # Historical PRDs for reference
├── templates/          # PRD templates for new documents
└── README.md          # Organization system documentation
```

## 🔄 Workflow

The PRD workflow follows this progression:

```
queue/ → in-progress/ → completed/ (or failed/)
                ↓
            archive/
```

### Status Transitions

1. **New PRD**: Created in `queue/` folder
2. **Processing**: Moved to `in-progress/` when Devin AI starts processing
3. **Completion**: Moved to `completed/` when agent creation succeeds
4. **Failure**: Moved to `failed/` when processing fails
5. **Archival**: Moved to `archive/` for long-term storage

## 📋 Folder Descriptions

### `queue/`
- **Purpose**: PRDs waiting to be processed
- **Status**: `queue`
- **Contents**: Validated PRDs ready for agent creation
- **Next Action**: Will be picked up by Devin AI

### `in-progress/`
- **Purpose**: PRDs currently being processed
- **Status**: `in_progress`
- **Contents**: PRDs being worked on by Devin AI
- **Next Action**: Will complete or fail processing

### `completed/`
- **Purpose**: Successfully processed PRDs
- **Status**: `completed`
- **Contents**: PRDs with created and deployed agents
- **Next Action**: Monitor agent performance

### `failed/`
- **Purpose**: PRDs that failed processing
- **Status**: `failed`
- **Contents**: PRDs that encountered errors
- **Next Action**: Review errors and retry

### `archive/`
- **Purpose**: Historical PRDs for reference
- **Status**: Various (archived)
- **Contents**: Long-term storage of completed/cancelled PRDs
- **Next Action**: Reference and analysis

### `templates/`
- **Purpose**: PRD templates for new documents
- **Status**: N/A (templates)
- **Contents**: Template files for different PRD types
- **Next Action**: Copy and customize for new PRDs

## 🛠️ Management Tools

### List PRDs
```bash
# Show summary of all PRDs
./scripts/prd-management/list-prds.sh -s

# List PRDs in specific folder
./scripts/prd-management/list-prds.sh queue

# Show detailed information
./scripts/prd-management/list-prds.sh completed -l

# Show count only
./scripts/prd-management/list-prds.sh -c
```

### Move PRDs
```bash
# Move PRD between folders
./scripts/prd-management/move-prd.sh database-integration-supabase queue in-progress

# Move with full filename
./scripts/prd-management/move-prd.sh 2024-01-15_database-integration-supabase.md completed archive
```

## 📝 File Naming Convention

Use descriptive filenames with timestamps:
```
YYYY-MM-DD_prd-title-description.md
```

Examples:
- `2024-01-15_database-integration-supabase.md`
- `2024-01-16_user-authentication-system.md`
- `2024-01-17_api-rate-limiting.md`

## 🗄️ Database Synchronization

The file system organization mirrors the database statuses:

| File Folder | Database Status | Description |
|-------------|----------------|-------------|
| `queue/` | `queue` | Waiting to be processed |
| `in-progress/` | `in_progress` | Currently being processed |
| `completed/` | `completed` | Successfully processed |
| `failed/` | `failed` | Processing failed |
| `archive/` | Various | Historical storage |

## 📋 PRD Templates

### Available Templates

1. **`prd-template-basic.md`**
   - Essential sections only
   - Quick PRD creation
   - Standard requirements

2. **`prd-template-comprehensive.md`**
   - All sections included
   - Detailed requirements
   - Complete documentation

3. **`prd-template-platform.md`**
   - Platform/infrastructure focused
   - Technical requirements
   - System-level features

4. **`prd-template-agent.md`**
   - AI agent specific
   - Agent capabilities
   - AI/ML requirements

### Using Templates

1. **Copy Template**: Copy appropriate template
2. **Customize**: Fill in your specific requirements
3. **Validate**: Check structure and content
4. **Submit**: Place in `queue/` folder

## 🔧 Best Practices

### PRD Creation
- Use appropriate template for your PRD type
- Follow naming convention with timestamps
- Include all required sections
- Validate before submitting

### File Management
- Keep PRDs in correct status folders
- Use management scripts for operations
- Archive old PRDs regularly
- Maintain clean folder structure

### Database Sync
- Update database when moving files
- Monitor status consistency
- Use dashboard for status updates
- Verify synchronization regularly

## 📊 Monitoring and Analytics

### File System Metrics
- PRD count by status
- Processing time analysis
- Success/failure rates
- Archive utilization

### Database Metrics
- Query performance
- Data consistency
- Status transitions
- Error tracking

## 🚀 Integration with AI Agent Factory

### Automatic Operations
- **File Monitoring**: System watches for new PRDs in `queue/`
- **Status Updates**: Automatic file moves during processing
- **Database Sync**: Real-time status synchronization
- **Error Handling**: Failed PRDs moved to `failed/` folder

### Manual Operations
- **PRD Creation**: Use templates and place in `queue/`
- **Status Management**: Use scripts to move PRDs
- **Archive Management**: Move old PRDs to `archive/`
- **Error Resolution**: Fix failed PRDs and retry

## 🔍 Troubleshooting

### Common Issues

1. **File Not Found**
   - Check correct folder location
   - Verify filename spelling
   - Use list script to find files

2. **Status Mismatch**
   - Check database status
   - Verify file location
   - Use sync tools to align

3. **Permission Errors**
   - Check file permissions
   - Verify script execution rights
   - Use proper user account

### Resolution Steps

1. **Identify Issue**: Use diagnostic tools
2. **Check Status**: Verify file and database status
3. **Fix Problem**: Resolve underlying issue
4. **Sync Systems**: Align file and database
5. **Test**: Verify resolution

## 📈 Future Enhancements

### Planned Features
- **Automated Sync**: Real-time file/database synchronization
- **Bulk Operations**: Mass PRD management capabilities
- **Advanced Analytics**: Detailed reporting and insights
- **Integration APIs**: Programmatic access to PRD system

### Extensibility
- **Custom Templates**: User-defined PRD templates
- **Workflow Customization**: Configurable status workflows
- **Plugin System**: Extensible management tools
- **API Integration**: External system integration

## 📚 Related Documentation

- [Database Setup Guide](../setup/database-setup-guide.md)
- [AI Agent Factory Architecture](../architecture/01-infrastructure-blueprint.md)
- [Devin AI Integration Guide](04-devin-ai-integration.md)
- [File Organization Documentation](../architecture/25-file-organization.md)
