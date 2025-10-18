# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[04-06 - System Guides](../../04-prd-system.md)** — Current implementation documentation
> 
> **This file is preserved for historical reference only.**

---

# Repository Strategy Quick Reference

## 🎯 **Decision: Separate Repositories**

**Each AI agent gets its own GitHub repository** for maximum scalability, isolation, and maintainability.

## 📁 **Repository Structure**

```
thedoctorJJ/
├── ai-agent-factory/          # Main platform (this repo)
│   ├── backend/                    # Core platform backend
│   ├── frontend/                   # Core platform frontend
│   ├── scripts/                    # Platform automation
│   └── libraries/                  # Shared components
│
├── ai-agents-email-assistant/  # Individual agent repos
├── ai-agents-data-processor/   # Each with their own:
├── ai-agents-content-generator/ # - Code
├── ai-agents-customer-support/  # - Tests
└── ai-agents-analytics/        # - Documentation
                                    # - Deployment configs
```

## 🔄 **Workflow**

1. **PRD Creation** → ChatGPT voice/text conversation
2. **PRD Upload** → AI Agent Factory platform
3. **Agent Generation** → Devin AI creates new repository
4. **Deployment** → Cloud Run + Platform registration
5. **Management** → Centralized dashboard

## 🛠️ **Key Components**

### **Repository Naming**
- Pattern: `ai-agents-{kebab-case-name}`
- Example: `ai-agents-email-assistant`

### **Template Base**
- Uses `thedoctorJJ/ai-agent-factory` as template
- Ensures consistent structure across all agents

### **MCP Integration**
- **GitHub MCP**: Creates repositories automatically
- **Supabase MCP**: Sets up database tables
- **Google Cloud MCP**: Deploys to Cloud Run

### **Platform Integration**
- Agents register with main platform
- Centralized monitoring and management
- Shared libraries for common functionality

## ✅ **Benefits**

- **Scalability**: No limits on number of agents
- **Isolation**: Independent development and deployment
- **Team Collaboration**: Clear ownership boundaries
- **Maintenance**: Update agents independently
- **Security**: Isolated security boundaries
- **CI/CD**: Independent pipelines per agent

## 📚 **Documentation**

- **Full Guide**: [Agent Repository Strategy](./19-agent-repository-strategy.md)
- **Implementation**: Complete code templates and examples
- **Best Practices**: Security, monitoring, and maintenance
- **Troubleshooting**: Common issues and solutions

## 🚀 **Getting Started**

1. Create PRD in AI Agent Factory
2. Deploy with Devin AI (creates repository automatically)
3. Monitor in platform dashboard
4. Develop independently in agent repository

**This strategy is already implemented and ready to use!**
