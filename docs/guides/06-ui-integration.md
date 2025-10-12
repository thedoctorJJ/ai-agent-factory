# UI Integration and Transition Layer

## Overview
Next.js + shadcn/ui frontend module bridging conversation → PRD → backend → orchestration → execution.

## Components
| Component | Purpose |
|-----------|---------|
| PRD Submission Page | Allows voice or text submission |
| Agent Dashboard | Shows active agents, status, logs, orchestration |
| Version History | Tracks agent versions and PRD references |
| Logs Viewer | Streams FastAPI and Supabase logs |
| Alerts & Notifications | Error/completion updates |

## Data Flow
```
[User Interaction] --> Next.js UI
↓
[API Calls] --> FastAPI Backend
↓
[Supabase Storage / Vector DB]
↓
[Devin AI Orchestration]
↓
[Next.js UI Updates Dashboard]
```

## Principles
- Modular frontend reusable across projects
- Supabase Auth for login
- Async communication with backend and MCP
- Supports voice-first and manual PRD entry
