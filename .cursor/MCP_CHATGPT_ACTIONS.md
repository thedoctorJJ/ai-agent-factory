# MCP Tools for ChatGPT Actions Management

## 🎯 Overview

While you **cannot directly control ChatGPT Actions** from MCP (they're configured in ChatGPT's UI), the MCP server now includes tools to help you **manage and configure** ChatGPT Actions.

## 🔧 Available MCP Tools

### 1. `get_chatgpt_action_config`
Get the ChatGPT Action OpenAPI configuration.

**Usage**:
```
Get the ChatGPT Action configuration schema
```

**Returns**: The OpenAPI schema that should be used when setting up ChatGPT Actions.

### 2. `generate_chatgpt_action_schema`
Generate or validate the OpenAPI schema for ChatGPT Actions.

**Usage**:
```
Generate the ChatGPT Action schema
```

**Options**:
- `validate_only`: If true, only validates without generating

### 3. `get_chatgpt_action_setup_instructions`
Get step-by-step instructions for setting up ChatGPT Actions.

**Usage**:
```
Get instructions for setting up ChatGPT Actions
```

**Options**:
- `format`: "markdown", "text", or "json"

### 4. `test_chatgpt_action_endpoint`
Test the ChatGPT Action API endpoint to ensure it's working.

**Usage**:
```
Test the ChatGPT Action endpoint
```

**Options**:
- `test_content`: Optional test PRD content

## 📋 What You Can Do

### ✅ Can Do (via MCP)
- Get the OpenAPI schema for ChatGPT Actions
- Generate/validate the schema file
- Get setup instructions
- Test the API endpoint
- Manage the configuration files

### ❌ Cannot Do (ChatGPT UI Only)
- Directly create/delete ChatGPT Actions
- Modify existing Actions in ChatGPT
- Control when Actions are triggered
- Access ChatGPT's Action settings

## 🚀 Example Usage in Cursor

### Get Configuration
```
Get the ChatGPT Action configuration so I can set it up
```

### Test Endpoint
```
Test the ChatGPT Action endpoint to make sure it works
```

### Get Setup Instructions
```
Give me instructions for setting up ChatGPT Actions
```

## 💡 How It Works

1. **MCP Tools** help you manage the **configuration files** and **test the endpoint**
2. **You configure ChatGPT Actions** manually in ChatGPT's UI
3. **ChatGPT calls your API** when it detects a PRD
4. **MCP tools** can help verify everything is set up correctly

## 🔗 Related Files

- `api-spec/chatgpt-action-openapi.json` - The OpenAPI schema
- `.cursor/CHATGPT_ACTION_SETUP.md` - Manual setup guide
- `.cursor/VOICE_PRD_SOLUTION.md` - Complete solution overview

---

**Note**: ChatGPT Actions must be configured in ChatGPT's UI. MCP tools help you prepare and test the configuration, but cannot directly control ChatGPT's interface.



