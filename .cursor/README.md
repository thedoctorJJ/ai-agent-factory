# Cursor Configuration

This directory contains Cursor-specific configuration and startup scripts.

## 📋 Startup Prompt

**File**: `startup-prompt.md`

This prompt is designed to be used when starting a new Cursor session on the AI Agent Factory project. It guides the AI assistant through:

1. Understanding the application
2. Reading documentation
3. Reviewing previous issue resolutions
4. Checking environment configuration
5. Running health checks
6. Generating a comprehensive summary

### Usage

When starting a new session, copy the contents of `startup-prompt.md` and paste it as your first message to Cursor. The AI assistant will follow the instructions systematically.

### Alternative: Quick Start Command

You can also use this quick command:

```
Read the README, scan the project structure, review resolution summaries in docs/resolution-summaries/, check .env files for API keys (don't show values), and run health checks on all production endpoints. Then provide a comprehensive summary of the application status.
```

---

## 🔧 Customization

Feel free to modify `startup-prompt.md` to include additional checks or steps specific to your workflow.

