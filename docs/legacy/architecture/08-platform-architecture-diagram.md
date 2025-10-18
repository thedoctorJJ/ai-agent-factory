# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[01 - Architecture Overview](../../01-architecture-overview.md)** — Current architecture documentation
> 
> **This file is preserved for historical reference only.**

---

# Platform Architecture Diagram

## Components
1. **User Layer**: Voice or UI input
2. **PRD Storage & Trigger**: Supabase + Edge Functions
3. **MCP Service / GitHub**: Creates new repos from templates
4. **Devin AI Orchestration**: Builds and deploys agents
5. **Backend**: FastAPI API endpoints
6. **Frontend**: Next.js + shadcn dashboard
7. **AI Core**: GPT-5, Whisper, agents
8. **Hosting & Infra**: Google Cloud Run, Storage, Pub/Sub, Secret Manager

## Data Flow
```
[User Voice/UI Input]
↓
[Whisper + GPT-5 PRD Generation]
↓
[Supabase DB]
↓
[Edge Function Trigger] → [GitHub MCP Service]
↓
[New Repo Created] → [PRD.md + Scaffolds]
↓
[Devin AI]
↓
[FastAPI Backend] <---> [Supabase DB + Vector Store]
↓
[Next.js Frontend]
↓
[Monitoring & Logging]
```

## Legend
- Solid arrows: direct flow
- Dashed arrows: event/trigger flow
- Boxes: components/services
- Parallel arrows: async tasks
