# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[01 - Architecture Overview](../../01-architecture-overview.md)** — Current architecture documentation
> 
> **This file is preserved for historical reference only.**

---

# AI Agent Factory — Infrastructure Blueprint

## Overview
The AI Agent Factory is a repeatable, modular architecture that allows the creation of AI agents, each with its own module and attached tools.  
Every component is designed to be reusable and scalable, enabling rapid deployment of new agents without rebuilding the core infrastructure.

## Folder Structure
```
/ai-agent-factory
│
├── /docs                    # Comprehensive documentation
├── /backend                 # FastAPI backend application
│   ├── /fastapi_app
│   │   ├── main.py
│   │   ├── /routers
│   │   ├── /models
│   │   ├── /agents
│   │   └── /utils
│   └── requirements.txt
├── /frontend                # Next.js frontend application
│   ├── /next-app
│   │   ├── /components
│   │   ├── /app
│   │   ├── /lib
│   │   └── /styles
│   └── package.json
├── /scripts                 # Organized automation scripts
│   ├── /mcp                # MCP server scripts and configs
│   ├── /config             # Configuration management scripts
│   ├── /setup              # Development setup scripts
│   ├── /deployment         # Deployment automation scripts
│   └── /testing            # Test automation scripts
├── /config                  # Configuration files and templates
│   ├── /env                # Environment configuration files
│   └── env.example         # Environment variables template
├── /setup                   # Setup guides and checklists
├── /tests                   # Test results and reports
├── /reports                 # Project reports and analysis
├── /libraries               # Agent, prompt, and tool libraries
│   ├── /prompt-library
│   ├── /agent-library
│   └── /tool-library
├── /infra
│   ├── docker-compose.yml
│   ├── supabase-config.json
│   ├── google-cloud.yaml
│   └── README.md
└── README.md
```

## Key Components
- **Backend**: FastAPI application managing APIs, agents, and orchestration.
- **Frontend**: Next.js + shadcn/ui dashboard for submitting PRDs and monitoring agents.
- **Libraries**: Reusable prompts, agents, and tools.
- **Infra**: Deployment and hosting configurations for Supabase and Google Cloud.
