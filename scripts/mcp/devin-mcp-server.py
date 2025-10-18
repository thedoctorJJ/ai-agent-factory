#!/usr/bin/env python3
"""
Devin AI MCP Server for AI Agent Factory
Provides PRD access and agent creation tools for Devin AI integration
"""

import json
import sys
import os
import requests
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DevinMCPServer:
    def __init__(self):
        """Initialize the Devin MCP Server"""
        self.endcap_api_url = os.getenv('ENDCAP_API_URL', 'http://localhost:8000')
        
        # Multi-token GitHub configuration
        self.github_token_tellenai = os.getenv('GITHUB_TOKEN_TELLENAI')
        self.github_token_thedoctorjj = os.getenv('GITHUB_TOKEN_THEDOCTORJJ')
        self.default_github_org = os.getenv('DEFAULT_GITHUB_ORG', 'thedoctorJJ')
        
        # Legacy support for single token
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_org = os.getenv('GITHUB_ORG_NAME', self.default_github_org)
        
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        # In-memory storage for PRD data loaded from our application
        self._prd_cache = {}
        self._agent_library_cache = {}
        
        logger.info(f"Devin MCP Server initialized with API URL: {self.endcap_api_url}")
        logger.info(f"GitHub token (tellenai) configured: {bool(self.github_token_tellenai)}")
        logger.info(f"GitHub token (thedoctorJJ) configured: {bool(self.github_token_thedoctorjj)}")
        logger.info(f"Default GitHub org: {self.default_github_org}")

    def _get_github_config(self, target_org: Optional[str] = None) -> tuple[str, str]:
        """Get the appropriate GitHub token and organization for the target org"""
        org = target_org or self.default_github_org
        
        if org.lower() == 'tellenai' and self.github_token_tellenai:
            return self.github_token_tellenai, 'tellenai'
        elif org.lower() == 'thedoctorjj' and self.github_token_thedoctorjj:
            return self.github_token_thedoctorjj, 'thedoctorJJ'
        elif self.github_token:
            # Fallback to legacy single token
            return self.github_token, self.github_org
        else:
            # No token available
            return None, org

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests from Devin AI"""
        try:
            method = request.get('method')
            params = request.get('params', {})
            request_id = request.get('id')
            
            logger.info(f"Handling MCP request: {method}")
            
            # Handle MCP protocol methods
            if method == 'initialize':
                return self._handle_initialize(request_id)
            elif method == 'initialized':
                return None
            elif method == 'tools/list':
                return self._handle_tools_list(request_id)
            elif method == 'tools/call':
                return await self._handle_tool_call(request_id, params)
            else:
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'error': {
                        'code': -32601,
                        'message': f'Method not found: {method}'
                    }
                }
                
        except Exception as e:
            logger.error(f"Error handling MCP request: {e}")
            return {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'error': {
                    'code': -32603,
                    'message': f'Internal error: {str(e)}'
                }
            }

    def _handle_initialize(self, request_id: str) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'protocolVersion': '2024-11-05',
                'capabilities': {
                    'tools': {}
                },
                'serverInfo': {
                    'name': 'ai-agent-factory-devin',
                    'version': '1.0.0',
                    'description': 'AI Agent Factory integration for Devin AI'
                }
            }
        }

    def _handle_tools_list(self, request_id: str) -> Dict[str, Any]:
        """Return list of available tools for Devin AI"""
        tools = [
            {
                'name': 'get_prd_details',
                'description': 'Get detailed information about a specific PRD by ID',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'prd_id': {
                            'type': 'string',
                            'description': 'The ID of the PRD to retrieve'
                        }
                    },
                    'required': ['prd_id']
                }
            },
            {
                'name': 'list_available_prds',
                'description': 'List all PRDs available for agent creation',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'status': {
                            'type': 'string',
                            'description': 'Filter PRDs by status (optional)',
                            'enum': ['draft', 'ready_for_devin', 'in_progress', 'completed']
                        }
                    }
                }
            },
            {
                'name': 'create_agent_from_prd',
                'description': 'Create a new AI agent based on a PRD specification',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'prd_id': {
                            'type': 'string',
                            'description': 'The ID of the PRD to use for agent creation'
                        },
                        'agent_name': {
                            'type': 'string',
                            'description': 'Name for the new agent'
                        },
                        'agent_description': {
                            'type': 'string',
                            'description': 'Description of the agent'
                        },
                        'repository_name': {
                            'type': 'string',
                            'description': 'Name for the GitHub repository (optional)'
                        }
                    },
                    'required': ['prd_id', 'agent_name', 'agent_description']
                }
            },
            {
                'name': 'get_agent_library_info',
                'description': 'Get information about available agent libraries and tools',
                'inputSchema': {
                    'type': 'object',
                    'properties': {}
                }
            },
            {
                'name': 'update_agent_status',
                'description': 'Update the status of an agent (e.g., mark as deployed)',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'agent_id': {
                            'type': 'string',
                            'description': 'The ID of the agent to update'
                        },
                        'status': {
                            'type': 'string',
                            'description': 'New status for the agent',
                            'enum': ['draft', 'active', 'inactive', 'deprecated', 'error']
                        },
                        'repository_url': {
                            'type': 'string',
                            'description': 'GitHub repository URL (optional)'
                        },
                        'deployment_url': {
                            'type': 'string',
                            'description': 'Deployment URL (optional)'
                        }
                    },
                    'required': ['agent_id', 'status']
                }
            },
            {
                'name': 'load_prd_data',
                'description': 'Load PRD data from the AI Agent Factory application into MCP cache',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'prd_id': {
                            'type': 'string',
                            'description': 'The ID of the PRD to load'
                        }
                    },
                    'required': ['prd_id']
                }
            },
            {
                'name': 'check_available_prds',
                'description': 'Check what PRDs are available in the MCP cache for processing',
                'inputSchema': {
                    'type': 'object',
                    'properties': {}
                }
            },
            {
                'name': 'get_startup_guide',
                'description': 'Get the complete startup guide for working with the AI Agent Factory',
                'inputSchema': {
                    'type': 'object',
                    'properties': {}
                }
            },
            {
                'name': 'create_github_repository',
                'description': 'Create a new GitHub repository for an AI agent (only for Agent PRDs)',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'repository_name': {
                            'type': 'string',
                            'description': 'Name for the new repository'
                        },
                        'description': {
                            'type': 'string',
                            'description': 'Description of the repository (optional)'
                        },
                        'private': {
                            'type': 'boolean',
                            'description': 'Whether the repository should be private (default: false)'
                        },
                        'auto_init': {
                            'type': 'boolean',
                            'description': 'Whether to initialize the repository with a README (default: true)'
                        },
                        'organization': {
                            'type': 'string',
                            'description': 'Target organization (tellenai or thedoctorJJ, default: thedoctorJJ)'
                        },
                        'prd_type': {
                            'type': 'string',
                            'description': 'PRD type (platform or agent) - determines repository strategy'
                        }
                    },
                    'required': ['repository_name', 'prd_type']
                }
            },
            {
                'name': 'determine_repository_strategy',
                'description': 'Determine the repository strategy based on PRD type',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'prd_id': {
                            'type': 'string',
                            'description': 'PRD ID to check (optional)'
                        },
                        'prd_type': {
                            'type': 'string',
                            'description': 'PRD type (platform or agent)'
                        }
                    },
                    'required': ['prd_type']
                }
            },
            {
                'name': 'deploy_to_google_cloud_run',
                'description': 'Deploy an AI agent to Google Cloud Run',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'agent_name': {
                            'type': 'string',
                            'description': 'Name for the agent (used for service naming)'
                        },
                        'agent_code': {
                            'type': 'string',
                            'description': 'Python code for the agent (FastAPI app)'
                        },
                        'requirements': {
                            'type': 'array',
                            'items': {'type': 'string'},
                            'description': 'Additional Python package requirements (optional)'
                        },
                        'environment_variables': {
                            'type': 'object',
                            'description': 'Environment variables for the deployment (optional)'
                        }
                    },
                    'required': ['agent_name', 'agent_code']
                }
            }
        ]
        
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'tools': tools
            }
        }

    async def _handle_tool_call(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution requests from Devin AI"""
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        
        logger.info(f"Executing tool: {tool_name} with args: {arguments}")
        
        try:
            if tool_name == 'get_prd_details':
                result = await self._get_prd_details(arguments)
            elif tool_name == 'list_available_prds':
                result = await self._list_available_prds(arguments)
            elif tool_name == 'create_agent_from_prd':
                result = await self._create_agent_from_prd(arguments)
            elif tool_name == 'get_agent_library_info':
                result = await self._get_agent_library_info(arguments)
            elif tool_name == 'update_agent_status':
                result = await self._update_agent_status(arguments)
            elif tool_name == 'load_prd_data':
                result = await self._load_prd_data(arguments)
            elif tool_name == 'check_available_prds':
                result = await self._check_available_prds(arguments)
            elif tool_name == 'get_startup_guide':
                result = await self._get_startup_guide(arguments)
            elif tool_name == 'create_github_repository':
                result = await self._create_github_repository(arguments)
            elif tool_name == 'determine_repository_strategy':
                result = await self._determine_repository_strategy(arguments)
            elif tool_name == 'deploy_to_google_cloud_run':
                result = await self._deploy_to_google_cloud_run(arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'result': {
                    'content': [
                        {
                            'type': 'text',
                            'text': json.dumps(result, indent=2)
                        }
                    ]
                }
            }
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {
                    'code': -32603,
                    'message': f'Tool execution error: {str(e)}'
                }
            }

    async def _get_prd_details(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed PRD information from cache or API"""
        prd_id = args.get('prd_id')
        if not prd_id:
            raise ValueError("prd_id is required")
        
        # First check cache
        if prd_id in self._prd_cache:
            prd_data = self._prd_cache[prd_id]
            return {
                'success': True,
                'prd': prd_data,
                'message': f"Retrieved PRD from cache: {prd_data.get('title', 'Unknown')}",
                'source': 'cache'
            }
        
        # Fallback to API call
        try:
            response = requests.get(f"{self.endcap_api_url}/api/v1/prds/{prd_id}")
            if response.status_code == 200:
                prd_data = response.json()
                # Cache the result
                self._prd_cache[prd_id] = prd_data
                return {
                    'success': True,
                    'prd': prd_data,
                    'message': f"Retrieved PRD from API: {prd_data.get('title', 'Unknown')}",
                    'source': 'api'
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to retrieve PRD: {response.status_code}",
                    'message': "PRD not found or API error"
                }
        except Exception as e:
            return {
                'success': False,
                'error': f"API call failed: {str(e)}",
                'message': "Unable to connect to AI Agent Factory API"
            }

    async def _list_available_prds(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List all available PRDs"""
        status = args.get('status')
        
        # Call our API to get PRDs
        url = f"{self.endcap_api_url}/api/v1/prds"
        if status:
            url += f"?status={status}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            prds = data.get('prds', [])
            return {
                'success': True,
                'prds': prds,
                'total': len(prds),
                'message': f"Found {len(prds)} PRDs"
            }
        else:
            return {
                'success': False,
                'error': f"Failed to retrieve PRDs: {response.status_code}",
                'message': "API error"
            }

    async def _create_agent_from_prd(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create an agent from a PRD with hybrid repository strategy"""
        prd_id = args.get('prd_id')
        agent_name = args.get('agent_name')
        agent_description = args.get('agent_description')
        repository_name = args.get('repository_name')
        
        if not all([prd_id, agent_name, agent_description]):
            raise ValueError("prd_id, agent_name, and agent_description are required")
        
        # First, get the PRD details
        prd_response = requests.get(f"{self.endcap_api_url}/api/v1/prds/{prd_id}")
        if prd_response.status_code != 200:
            return {
                'success': False,
                'error': "PRD not found",
                'message': f"Could not find PRD with ID: {prd_id}"
            }
        
        prd_data = prd_response.json()
        prd_type = prd_data.get('prd_type', 'agent')  # Default to 'agent' if not specified
        
        # Determine repository strategy based on PRD type
        if prd_type == 'platform':
            # Platform PRDs: Use main repository structure
            repository_url = f"https://github.com/thedoctorJJ/ai-agent-factory/tree/main/agents/{self._clean_agent_name(agent_name)}"
            repository_strategy = "main_repository"
        else:
            # Agent PRDs: Create separate repository
            if not repository_name:
                repository_name = f"ai-agents-{self._clean_agent_name(agent_name)}"
            repository_url = f"https://github.com/thedoctorJJ/{repository_name}"
            repository_strategy = "separate_repository"
        
        # Create a placeholder agent record
        agent_data = {
            'name': agent_name,
            'description': agent_description,
            'purpose': f"Agent created from PRD: {prd_data.get('title', 'Unknown')}",
            'agent_type': 'custom',
            'version': '1.0.0',
            'status': 'draft',
            'prd_id': prd_id,
            'repository_url': repository_url,
            'capabilities': ['task_management', 'notifications', 'reporting'],
            'configuration': {
                'created_by': 'devin_ai',
                'repository_name': repository_name,
                'repository_strategy': repository_strategy,
                'prd_title': prd_data.get('title'),
                'prd_type': prd_type
            }
        }
        
        # Create the agent via our API
        response = requests.post(
            f"{self.endcap_api_url}/api/v1/agents",
            json=agent_data
        )
        
        if response.status_code in [200, 201]:
            agent_result = response.json()
            return {
                'success': True,
                'agent_id': agent_result.get('id'),
                'agent_name': agent_name,
                'repository_strategy': repository_strategy,
                'repository_url': repository_url,
                'message': f"Agent created successfully with {repository_strategy} strategy"
            }
        else:
            return {
                'success': False,
                'error': f"Failed to create agent: {response.status_code}",
                'message': f"API error: {response.text}"
            }
    
    def _clean_agent_name(self, name: str) -> str:
        """Clean agent name for use in repository names and URLs."""
        import re
        # Remove emojis and special characters
        cleaned = re.sub(r'[^\w\s-]', '', name)
        # Replace spaces with hyphens and convert to lowercase
        cleaned = re.sub(r'[-\s]+', '-', cleaned).lower()
        # Remove leading/trailing hyphens
        return cleaned.strip('-')

    async def _determine_repository_strategy(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the repository strategy based on PRD type"""
        try:
            prd_type = args.get('prd_type', 'agent')
            prd_id = args.get('prd_id')
            
            if prd_type == 'platform':
                return {
                    'success': True,
                    'repository_strategy': 'main_repository',
                    'repository_url_template': 'https://github.com/thedoctorJJ/ai-agent-factory/tree/main/agents/{agent_name}',
                    'instructions': 'Add agent code to the main repository in /agents/{agent_name}/ folder',
                    'message': 'Platform PRDs use the main repository structure'
                }
            else:
                return {
                    'success': True,
                    'repository_strategy': 'separate_repository',
                    'repository_url_template': 'https://github.com/thedoctorJJ/ai-agents-{agent_name}',
                    'instructions': 'Create a separate GitHub repository with naming pattern: ai-agents-{agent_name}',
                    'message': 'Agent PRDs get separate repositories'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to determine repository strategy: {str(e)}",
                'message': "Error determining repository strategy"
            }

    async def _get_agent_library_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get information about available agent libraries and tools"""
        return {
            'success': True,
            'libraries': {
                'agent_library': {
                    'path': 'libraries/agent-library/',
                    'description': 'Base agent templates and utilities',
                    'available_templates': ['task_agent', 'notification_agent', 'reporting_agent']
                },
                'tool_library': {
                    'path': 'libraries/tool-library/',
                    'description': 'Reusable tools and utilities',
                    'available_tools': ['database_connector', 'api_client', 'file_handler']
                },
                'prompt_library': {
                    'path': 'libraries/prompt-library/',
                    'description': 'Pre-built prompts and templates',
                    'available_prompts': ['task_analysis', 'code_generation', 'testing']
                }
            },
                'deployment_targets': {
                'github': {
                    'organization': self.github_org,
                    'repository_prefix': 'ai-agent-',
                    'description': 'GitHub repositories for agent code'
                },
                'supabase': {
                    'url': self.supabase_url,
                    'description': 'Database and metadata storage'
                },
                'google_cloud_run': {
                    'project': 'agent-factory-474201',
                    'service': 'Cloud Run',
                    'description': 'Agent deployment platform (replaces Fly.io)',
                    'region': 'us-central1'
                }
            },
            'message': "Agent library information retrieved successfully"
        }

    async def _update_agent_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update agent status after Devin completes implementation"""
        agent_id = args.get('agent_id')
        status = args.get('status')
        repository_url = args.get('repository_url')
        deployment_url = args.get('deployment_url')
        
        if not agent_id or not status:
            raise ValueError("agent_id and status are required")
        
        # Prepare update data
        update_data = {'status': status}
        if repository_url:
            update_data['repository_url'] = repository_url
        if deployment_url:
            update_data['deployment_url'] = deployment_url
        
        # Update the agent via our API
        response = requests.put(
            f"{self.endcap_api_url}/api/v1/agents/{agent_id}",
            json=update_data
        )
        
        if response.status_code == 200:
            agent = response.json()
            return {
                'success': True,
                'agent': agent,
                'message': f"Agent status updated to '{status}' successfully"
            }
        else:
            return {
                'success': False,
                'error': f"Failed to update agent: {response.status_code}",
                'message': "API error during agent update"
            }

    async def _load_prd_data(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Load PRD data from our application into MCP cache"""
        prd_id = args.get('prd_id')
        prd_data = args.get('prd_data')  # Accept PRD data directly
        
        if not prd_id:
            raise ValueError("prd_id is required")
        
        try:
            # If PRD data is provided directly, use it
            if prd_data:
                # Store in cache
                self._prd_cache[prd_id] = prd_data
                
                return {
                    'success': True,
                    'prd': prd_data,
                    'message': f"PRD data loaded into MCP cache: {prd_data.get('title', 'Unknown')}",
                    'cache_size': len(self._prd_cache)
                }
            else:
                # Fallback: Get PRD data from our API (for backward compatibility)
                response = requests.get(f"{self.endcap_api_url}/api/v1/prds/{prd_id}")
                if response.status_code == 200:
                    prd_data = response.json()
                    
                    # Store in cache
                    self._prd_cache[prd_id] = prd_data
                    
                    return {
                        'success': True,
                        'prd': prd_data,
                        'message': f"PRD data loaded into MCP cache: {prd_data.get('title', 'Unknown')}",
                        'cache_size': len(self._prd_cache)
                    }
                else:
                    return {
                        'success': False,
                        'error': f"Failed to load PRD: {response.status_code}",
                        'message': "PRD not found or API error"
                    }
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to load PRD data: {str(e)}",
                'message': "Unable to connect to AI Agent Factory API"
            }

    async def _check_available_prds(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Check what PRDs are available in the MCP cache for processing"""
        try:
            if not self._prd_cache:
                return {
                    'success': True,
                    'available_prds': [],
                    'message': "No PRDs are currently loaded in the MCP cache. Use the AI Agent Factory platform to load PRDs first.",
                    'cache_size': 0
                }
            
            # Return all cached PRDs with basic info
            available_prds = []
            for prd_id, prd_data in self._prd_cache.items():
                available_prds.append({
                    'id': prd_id,
                    'title': prd_data.get('title', 'Unknown Title'),
                    'description': prd_data.get('description', 'No description'),
                    'status': prd_data.get('status', 'unknown'),
                    'created_at': prd_data.get('created_at', 'unknown')
                })
            
            return {
                'success': True,
                'available_prds': available_prds,
                'message': f"Found {len(available_prds)} PRD(s) available for processing",
                'cache_size': len(self._prd_cache)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to check available PRDs: {str(e)}",
                'message': "Error accessing MCP cache"
            }

    async def _get_startup_guide(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get the complete startup guide for working with the AI Agent Factory"""
        try:
            # Read the startup guide from the file
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            guide_path = os.path.join(current_dir, 'devin-cold-start-guide.md')
            
            if os.path.exists(guide_path):
                with open(guide_path, 'r', encoding='utf-8') as f:
                    guide_content = f.read()
                
                return {
                    'success': True,
                    'guide': guide_content,
                    'message': "Complete startup guide retrieved successfully"
                }
            else:
                # Fallback to embedded guide if file not found
                embedded_guide = """# AI Agent Factory - Devin AI Cold Start Guide

## 🚀 Welcome to the AI Agent Factory!

You are now connected to the AI Agent Factory system via MCP (Model Context Protocol). This guide will help you understand your role and how to get started.

## 🎯 Your Mission

You are an AI agent creation specialist. Your job is to:
1. **Find PRDs** (Product Requirements Documents) that need agents created
2. **Analyze the requirements** and create appropriate AI agents
3. **Deploy the agents** to the cloud
4. **Update the platform** with the results

## 🔧 How to Get Started

### Step 1: Check for Available Work
First, check if there are any PRDs waiting for agent creation:

```
Use MCP tool: check_available_prds
```

This will show you all PRDs that have been loaded into the MCP cache and are ready for processing.

### Step 2: Get PRD Details
If PRDs are available, select one and get its full details:

```
Use MCP tool: get_prd_details
Parameters: {"prd_id": "the-prd-id-from-step-1"}
```

### Step 3: Understand the Agent Library
Before creating an agent, understand what tools and libraries are available:

```
Use MCP tool: get_agent_library_info
```

### Step 4: Create the Agent Record
Create a record for the agent in the AI Agent Factory platform:

```
Use MCP tool: create_agent_from_prd
Parameters: {
  "prd_id": "the-prd-id",
  "agent_name": "Your Agent Name",
  "agent_description": "Your agent description",
  "repository_name": "your-repo-name" (optional for agent PRDs)
}
```

**Repository Strategy:**
- **Platform PRDs**: Agents are added to the main repository (`/agents/` folder)
- **Agent PRDs**: Separate GitHub repositories are created (`ai-agents-{name}`)

### Step 5: Implement the Agent
Now implement the agent according to the PRD requirements:
- **Platform PRDs**: Add code to `/agents/{agent-name}/` in main repository
- **Agent PRDs**: Create separate repository and implement functionality
- Set up deployment configuration
- Deploy to the cloud

### Step 6: Update Status
When the agent is complete, update its status:

```
Use MCP tool: update_agent_status
Parameters: {
  "agent_id": "agent_id_from_step_4",
  "status": "active",
  "repository_url": "https://github.com/thedoctorJJ/your-repo",
  "deployment_url": "https://your-agent-uc.a.run.app"
}
```

## 🎯 Available MCP Tools

- `check_available_prds` - See what PRDs are ready for processing
- `get_prd_details` - Get full PRD information
- `list_available_prds` - List all PRDs in the system
- `create_agent_from_prd` - Create agent record in the platform
- `get_agent_library_info` - Access agent libraries and tools
- `update_agent_status` - Update agent status when complete
- `load_prd_data` - Load PRD data into MCP cache
- `get_startup_guide` - Get this startup guide

## 🏗️ Technical Stack

- **Backend**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Google Cloud Run (replaces Fly.io)
- **Repository**: GitHub (thedoctorJJ organization)
- **Monitoring**: Built-in health checks and logging

## 🚀 Let's Begin!

Start by checking for available PRDs:

```
Use MCP tool: check_available_prds
```

If you find PRDs, select one and begin the agent creation process. If no PRDs are available, you can wait for new ones to be loaded or ask the user to load PRDs through the AI Agent Factory platform.

## 📋 Workflow Summary

1. **Check for work** → `check_available_prds`
2. **Get PRD details** → `get_prd_details`
3. **Understand tools** → `get_agent_library_info`
4. **Create agent record** → `create_agent_from_prd` (determines repository strategy)
5. **Implement agent** → 
   - **Platform PRDs**: Add to main repository `/agents/` folder
   - **Agent PRDs**: Create separate repository and implement
6. **Deploy and test** → Deploy to Cloud Run
7. **Update status** → `update_agent_status`

Ready to start? Let's check for available PRDs!"""
                
                return {
                    'success': True,
                    'guide': embedded_guide,
                    'message': "Startup guide retrieved from embedded content"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to get startup guide: {str(e)}",
                'message': "Error retrieving startup guide"
            }

    async def _create_github_repository(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new GitHub repository for an AI agent (only for Agent PRDs)"""
        try:
            repository_name = args.get('repository_name')
            description = args.get('description', 'AI Agent created by AI Agent Factory')
            private = args.get('private', False)
            auto_init = args.get('auto_init', True)
            target_org = args.get('organization', self.default_github_org)
            prd_type = args.get('prd_type', 'agent')
            
            # Check if this is a platform PRD - if so, don't create separate repository
            if prd_type == 'platform':
                return {
                    'success': False,
                    'error': 'Platform PRDs use main repository structure',
                    'message': 'Platform PRDs should be added to the main repository in /agents/ folder, not as separate repositories'
                }
            
            if not repository_name:
                return {
                    'success': False,
                    'error': 'Repository name is required',
                    'message': 'Please provide a repository name'
                }
            
            # Get the appropriate token and organization
            github_token, github_org = self._get_github_config(target_org)
            
            if not github_token:
                return {
                    'success': False,
                    'error': f'GitHub token not configured for organization: {github_org}',
                    'message': f'Please configure GITHUB_TOKEN_{github_org.upper()} environment variable'
                }
            
            # GitHub API endpoint for creating a repository
            # Check if it's a personal account or organization
            if github_org.lower() in ['thedoctorjj']:
                # Personal account - use user endpoint
                url = f"https://api.github.com/user/repos"
            else:
                # Organization - use org endpoint
                url = f"https://api.github.com/orgs/{github_org}/repos"
            
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            }
            
            data = {
                'name': repository_name,
                'description': description,
                'private': private,
                'auto_init': auto_init,
                'has_issues': True,
                'has_projects': True,
                'has_wiki': True
            }
            
            logger.info(f"Creating GitHub repository: {repository_name} in org: {github_org}")
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                repo_data = response.json()
                repository_url = repo_data['html_url']
                clone_url = repo_data['clone_url']
                
                logger.info(f"Successfully created repository: {repository_url}")
                
                return {
                    'success': True,
                    'repository_name': repository_name,
                    'repository_url': repository_url,
                    'clone_url': clone_url,
                    'message': f'Successfully created repository: {repository_name}'
                }
            else:
                error_message = response.json().get('message', 'Unknown error')
                logger.error(f"Failed to create repository: {error_message}")
                
                return {
                    'success': False,
                    'error': f'GitHub API error: {error_message}',
                    'message': f'Failed to create repository: {error_message}'
                }
                
        except Exception as e:
            logger.error(f"Error creating GitHub repository: {e}")
            return {
                'success': False,
                'error': f"Failed to create repository: {str(e)}",
                'message': "Error creating GitHub repository"
            }

    async def _deploy_to_google_cloud_run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy an AI agent to Google Cloud Run"""
        try:
            agent_name = args.get('agent_name')
            agent_code = args.get('agent_code')
            requirements = args.get('requirements', [])
            environment_variables = args.get('environment_variables', {})
            
            if not agent_name or not agent_code:
                return {
                    'success': False,
                    'error': 'agent_name and agent_code are required',
                    'message': 'Please provide both agent name and code'
                }
            
            # Import the Google Cloud Run deployer
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            deployer_path = os.path.join(current_dir, 'google-cloud-run-deploy.py')
            
            if not os.path.exists(deployer_path):
                return {
                    'success': False,
                    'error': 'Google Cloud Run deployer not found',
                    'message': 'The google-cloud-run-deploy.py script is missing'
                }
            
            # Import the deployer class
            import importlib.util
            spec = importlib.util.spec_from_file_location("google_cloud_deployer", deployer_path)
            deployer_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(deployer_module)
            
            # Initialize the deployer
            project_id = "agent-factory-474201"
            service_account_key = os.path.join(os.path.dirname(current_dir), "..", "config", "google-cloud-service-account.json")
            
            deployer = deployer_module.GoogleCloudRunDeployer(project_id, service_account_key)
            
            # Authenticate
            if not deployer.authenticate():
                return {
                    'success': False,
                    'error': 'Google Cloud authentication failed',
                    'message': 'Unable to authenticate with Google Cloud. Check service account credentials.'
                }
            
            # Deploy the agent
            logger.info(f"Deploying agent to Google Cloud Run: {agent_name}")
            result = deployer.build_and_deploy(agent_name, agent_code, requirements)
            
            if result["success"]:
                return {
                    'success': True,
                    'service_name': result['service_name'],
                    'service_url': result['service_url'],
                    'image_name': result['image_name'],
                    'region': result['region'],
                    'message': f"Successfully deployed agent '{agent_name}' to Google Cloud Run"
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Unknown deployment error'),
                    'message': f"Failed to deploy agent to Google Cloud Run: {result.get('error', 'Unknown error')}"
                }
                
        except Exception as e:
            logger.error(f"Error deploying to Google Cloud Run: {e}")
            return {
                'success': False,
                'error': f"Deployment error: {str(e)}",
                'message': "Error deploying to Google Cloud Run"
            }

async def main():
    """Main MCP server loop"""
    server = DevinMCPServer()
    
    # Handle stdin/stdout for MCP protocol
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            if response:
                print(json.dumps(response))
                sys.stdout.flush()
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")

if __name__ == "__main__":
    asyncio.run(main())
