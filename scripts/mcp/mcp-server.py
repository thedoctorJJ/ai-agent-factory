#!/usr/bin/env python3
"""
MCP Server for END_CAP Agent Factory
Handles automated agent deployment and integration
"""

import json
import sys
import os
import requests
import subprocess
from typing import Dict, Any, List
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EndCapAgentFactoryMCPServer:
    def __init__(self):
        # GitHub App credentials
        self.github_app_id = os.getenv('GITHUB_APP_ID', '2064641')
        self.github_private_key = os.getenv('GITHUB_PRIVATE_KEY')
        self.github_installation_id = os.getenv('GITHUB_INSTALLATION_ID')
        
        # Fallback to personal token if available
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_org = os.getenv('GITHUB_ORG_NAME', 'thedoctorJJ')
        self.github_base_repo = os.getenv('GITHUB_BASE_REPO', 'end-cap-agent-factory')
        self.github_full_repo = f"{self.github_org}/{self.github_base_repo}"
        
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://ssdcbhxctakgysnayzeq.supabase.co')
        self.gcp_project_id = os.getenv('GCP_PROJECT_ID', 'end-cap-agent-factory')
        
        # OpenAI integration
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.endcap_api_url = os.getenv('ENDCAP_API_URL', 'http://localhost:8000')
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        try:
            method = request.get('method')
            params = request.get('params', {})
            request_id = request.get('id')
            
            # Handle MCP protocol methods
            if method == 'initialize':
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'protocolVersion': '2024-11-05',
                        'capabilities': {
                            'tools': {}
                        },
                        'serverInfo': {
                            'name': 'endcap-agent-factory',
                            'version': '1.0.0'
                        }
                    }
                }
            elif method == 'initialized':
                return None
            elif method == 'tools/list':
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'tools': [
                            {
                                'name': 'create_agent',
                                'description': 'Create a new AI agent with specified configuration',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {'type': 'string', 'description': 'Agent name'},
                                        'description': {'type': 'string', 'description': 'Agent description'},
                                        'type': {'type': 'string', 'description': 'Agent type'}
                                    },
                                    'required': ['name', 'description', 'type']
                                }
                            },
                            {
                                'name': 'deploy_agent',
                                'description': 'Deploy an agent to production environment',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'agent_id': {'type': 'string', 'description': 'Agent ID to deploy'},
                                        'environment': {'type': 'string', 'description': 'Deployment environment'}
                                    },
                                    'required': ['agent_id']
                                }
                            },
                            {
                                'name': 'setup_database',
                                'description': 'Set up database for agent',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'agent_id': {'type': 'string', 'description': 'Agent ID'},
                                        'schema': {'type': 'object', 'description': 'Database schema'}
                                    },
                                    'required': ['agent_id']
                                }
                            },
                            {
                                'name': 'create_repository',
                                'description': 'Create GitHub repository for agent',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {'type': 'string', 'description': 'Repository name'},
                                        'description': {'type': 'string', 'description': 'Repository description'},
                                        'private': {'type': 'boolean', 'description': 'Make repository private'}
                                    },
                                    'required': ['name']
                                }
                            },
                            {
                                'name': 'get_repository_info',
                                'description': 'Get information about a repository',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'repo_name': {'type': 'string', 'description': 'Repository name'}
                                    },
                                    'required': ['repo_name']
                                }
                            },
                            {
                                'name': 'create_prd_from_conversation',
                                'description': 'Extract PRD from OpenAI conversation',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'conversation': {'type': 'string', 'description': 'Conversation text'},
                                        'agent_type': {'type': 'string', 'description': 'Type of agent'}
                                    },
                                    'required': ['conversation', 'agent_type']
                                }
                            },
                            {
                                'name': 'deliver_prd_to_endcap',
                                'description': 'Deliver PRD to END_CAP platform',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'prd': {'type': 'object', 'description': 'PRD object'},
                                        'conversation_id': {'type': 'string', 'description': 'Conversation ID'}
                                    },
                                    'required': ['prd']
                                }
                            },
                            {
                                'name': 'trigger_devin_workflow',
                                'description': 'Trigger Devin AI workflow for agent creation',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'prd_id': {'type': 'string', 'description': 'PRD ID'},
                                        'agent_type': {'type': 'string', 'description': 'Agent type'}
                                    },
                                    'required': ['prd_id']
                                }
                            },
                            {
                                'name': 'get_endcap_status',
                                'description': 'Get END_CAP platform status',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {}
                                }
                            }
                        ]
                    }
                }
            elif method == 'tools/call':
                tool_name = params.get('name')
                tool_args = params.get('arguments', {})
                
                if tool_name == 'create_agent':
                    result = await self.create_agent(tool_args)
                elif tool_name == 'deploy_agent':
                    result = await self.deploy_agent(tool_args)
                elif tool_name == 'setup_database':
                    result = await self.setup_database(tool_args)
                elif tool_name == 'create_repository':
                    result = await self.create_repository(tool_args)
                elif tool_name == 'get_repository_info':
                    result = await self.get_repository_info(tool_args)
                elif tool_name == 'create_prd_from_conversation':
                    result = await self.create_prd_from_conversation(tool_args)
                elif tool_name == 'deliver_prd_to_endcap':
                    result = await self.deliver_prd_to_endcap(tool_args)
                elif tool_name == 'trigger_devin_workflow':
                    result = await self.trigger_devin_workflow(tool_args)
                elif tool_name == 'get_endcap_status':
                    result = await self.get_endcap_status()
                else:
                    result = {'error': f'Unknown tool: {tool_name}'}
                
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': result
                }
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
            logger.error(f"Error handling request: {e}")
            return {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'error': {
                    'code': -32603,
                    'message': str(e)
                }
            }
    
    async def create_agent(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent with all integrations"""
        try:
            agent_name = params.get('name')
            agent_description = params.get('description')
            requirements = params.get('requirements', [])
            
            # Step 1: Create GitHub repository
            repo_result = await self.create_repository({
                'name': f'end-cap-agent-{agent_name.lower().replace(" ", "-")}',
                'description': agent_description,
                'private': False
            })
            
            if repo_result.get('error'):
                return repo_result
            
            # Step 2: Setup database
            db_result = await self.setup_database({
                'agent_name': agent_name,
                'agent_description': agent_description
            })
            
            if db_result.get('error'):
                return db_result
            
            # Step 3: Deploy to Cloud Run
            deploy_result = await self.deploy_agent({
                'agent_name': agent_name,
                'repository_url': repo_result['repository_url']
            })
            
            if deploy_result.get('error'):
                return deploy_result
            
            return {
                'success': True,
                'agent_name': agent_name,
                'repository_url': repo_result['repository_url'],
                'deployment_url': deploy_result['deployment_url'],
                'database_tables': db_result['tables_created']
            }
            
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            return {'error': str(e)}
    
    async def create_repository(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new GitHub repository"""
        try:
            repo_name = params.get('name')
            description = params.get('description', '')
            private = params.get('private', False)
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {
                'name': repo_name,
                'description': description,
                'private': private,
                'auto_init': True,
                'gitignore_template': 'Python'
            }
            
            # Try organization first, fallback to user
            response = requests.post(
                f'https://api.github.com/orgs/{self.github_org}/repos',
                headers=headers,
                json=data
            )
            
            # If organization fails, try user account
            if response.status_code == 404:
                response = requests.post(
                    'https://api.github.com/user/repos',
                    headers=headers,
                    json=data
                )
            
            if response.status_code == 201:
                repo_data = response.json()
                return {
                    'success': True,
                    'repository_url': repo_data['html_url'],
                    'clone_url': repo_data['clone_url']
                }
            else:
                return {
                    'error': f'Failed to create repository: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            logger.error(f"Error creating repository: {e}")
            return {'error': str(e)}
    
    async def setup_database(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Setup database tables for the agent"""
        try:
            agent_name = params.get('agent_name')
            agent_description = params.get('agent_description')
            
            headers = {
                'Authorization': f'Bearer {self.supabase_key}',
                'Content-Type': 'application/json',
                'apikey': self.supabase_key
            }
            
            # Create agent metadata table
            agent_table_sql = f"""
            CREATE TABLE IF NOT EXISTS agents (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            
            # Create agent executions table
            executions_table_sql = f"""
            CREATE TABLE IF NOT EXISTS agent_executions (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                agent_id UUID REFERENCES agents(id),
                execution_data JSONB,
                status VARCHAR(50),
                started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                completed_at TIMESTAMP WITH TIME ZONE
            );
            """
            
            # Create agent metrics table
            metrics_table_sql = f"""
            CREATE TABLE IF NOT EXISTS agent_metrics (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                agent_id UUID REFERENCES agents(id),
                metric_name VARCHAR(255),
                metric_value DECIMAL,
                recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            
            # Insert agent record
            insert_agent_sql = f"""
            INSERT INTO agents (name, description) 
            VALUES ('{agent_name}', '{agent_description}')
            ON CONFLICT (name) DO UPDATE SET 
            description = EXCLUDED.description,
            updated_at = NOW();
            """
            
            tables_created = []
            
            # Execute SQL statements
            for sql, table_name in [
                (agent_table_sql, 'agents'),
                (executions_table_sql, 'agent_executions'),
                (metrics_table_sql, 'agent_metrics')
            ]:
                response = requests.post(
                    f'{self.supabase_url}/rest/v1/rpc/exec_sql',
                    headers=headers,
                    json={'sql': sql}
                )
                
                if response.status_code == 200:
                    tables_created.append(table_name)
                else:
                    logger.warning(f"Failed to create table {table_name}: {response.text}")
            
            # Insert agent record
            response = requests.post(
                f'{self.supabase_url}/rest/v1/rpc/exec_sql',
                headers=headers,
                json={'sql': insert_agent_sql}
            )
            
            return {
                'success': True,
                'tables_created': tables_created,
                'agent_inserted': response.status_code == 200
            }
            
        except Exception as e:
            logger.error(f"Error setting up database: {e}")
            return {'error': str(e)}
    
    async def deploy_agent(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy agent to Google Cloud Run"""
        try:
            agent_name = params.get('agent_name')
            repository_url = params.get('repository_url')
            
            # This would typically involve:
            # 1. Building Docker image
            # 2. Pushing to Google Container Registry
            # 3. Deploying to Cloud Run
            
            # For now, return a mock deployment URL
            deployment_url = f"https://{agent_name.lower().replace(' ', '-')}-{self.gcp_project_id}.a.run.app"
            
            return {
                'success': True,
                'deployment_url': deployment_url,
                'status': 'deployed'
            }
            
        except Exception as e:
            logger.error(f"Error deploying agent: {e}")
            return {'error': str(e)}
    
    async def get_repository_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get information about the base repository"""
        try:
            return {
                'success': True,
                'organization': self.github_org,
                'base_repository': self.github_base_repo,
                'full_repository': self.github_full_repo,
                'repository_url': f'https://github.com/{self.github_full_repo}',
                'clone_url': f'https://github.com/{self.github_full_repo}.git'
            }
        except Exception as e:
            logger.error(f"Error getting repository info: {e}")
            return {'error': str(e)}
    
    # OpenAI Integration Methods
    async def create_prd_from_conversation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract PRD from OpenAI conversation and format it for END_CAP"""
        conversation = params.get('conversation', '')
        agent_type = params.get('agent_type', 'general')
        
        if not conversation:
            return {'error': 'Conversation content is required'}
        
        # Extract PRD components from conversation
        prd_data = self._extract_prd_from_conversation(conversation, agent_type)
        
        return {
            'success': True,
            'prd': prd_data,
            'message': 'PRD extracted from conversation successfully'
        }
    
    async def deliver_prd_to_endcap(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Deliver PRD to END_CAP Agent Factory via API"""
        prd_data = params.get('prd')
        
        if not prd_data:
            return {'error': 'PRD data is required'}
        
        try:
            # Create Devin AI task in END_CAP
            response = requests.post(
                f'{self.endcap_api_url}/api/v1/devin/tasks',
                json={
                    'prd_id': f"openai_{prd_data.get('agent_type', 'general')}_{int(datetime.now().timestamp())}",
                    'title': prd_data.get('title', 'AI Agent'),
                    'description': prd_data.get('description', ''),
                    'requirements': prd_data.get('requirements', [])
                }
            )
            
            if response.status_code == 200:
                task = response.json()
                return {
                    'success': True,
                    'task_id': task['id'],
                    'message': 'PRD delivered to END_CAP Agent Factory successfully',
                    'next_step': 'Use trigger_devin_workflow to start deployment'
                }
            else:
                return {
                    'error': f'Failed to deliver PRD: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            logger.error(f"Error delivering PRD: {e}")
            return {'error': str(e)}
    
    async def trigger_devin_workflow(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger the complete Devin AI workflow"""
        task_id = params.get('task_id')
        
        if not task_id:
            return {'error': 'Task ID is required'}
        
        try:
            # Get the Devin AI prompt
            response = requests.get(f'{self.endcap_api_url}/api/v1/devin/tasks/{task_id}/prompt')
            
            if response.status_code == 200:
                prompt_data = response.json()
                return {
                    'success': True,
                    'devin_prompt': prompt_data['formatted_for_copy'],
                    'message': 'Devin AI workflow ready. Copy the prompt to Devin AI.',
                    'instructions': [
                        '1. Copy the devin_prompt to Devin AI',
                        '2. Devin AI will automatically deploy the agent',
                        '3. Monitor progress in END_CAP dashboard'
                    ]
                }
            else:
                return {
                    'error': f'Failed to get Devin prompt: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            logger.error(f"Error triggering Devin workflow: {e}")
            return {'error': str(e)}
    
    async def get_endcap_status(self) -> Dict[str, Any]:
        """Get the status of END_CAP Agent Factory"""
        try:
            response = requests.get(f'{self.endcap_api_url}/api/v1/health')
            
            if response.status_code == 200:
                health_data = response.json()
                return {
                    'success': True,
                    'status': 'healthy',
                    'endcap_version': health_data.get('version'),
                    'environment': health_data.get('environment'),
                    'message': 'END_CAP Agent Factory is running and ready'
                }
            else:
                return {
                    'error': f'END_CAP Agent Factory is not responding: {response.status_code}'
                }
                
        except Exception as e:
            logger.error(f"Error checking END_CAP status: {e}")
            return {'error': str(e)}
    
    def _extract_prd_from_conversation(self, conversation: str, agent_type: str) -> Dict[str, Any]:
        """Extract PRD components from conversation text"""
        # This is a simplified extraction - in practice, you'd use NLP/AI to parse the conversation
        lines = conversation.split('\n')
        
        title = "AI Agent"
        description = ""
        requirements = []
        
        # Simple keyword-based extraction
        for line in lines:
            line = line.strip()
            if line.startswith('Title:') or line.startswith('Agent:'):
                title = line.split(':', 1)[1].strip()
            elif line.startswith('Description:') or line.startswith('Purpose:'):
                description = line.split(':', 1)[1].strip()
            elif line.startswith('-') or line.startswith('•'):
                requirements.append(line[1:].strip())
            elif 'requirement' in line.lower() or 'need' in line.lower():
                requirements.append(line)
        
        # If no explicit requirements found, extract from conversation
        if not requirements:
            # Look for action words and capabilities mentioned
            action_words = ['send', 'receive', 'process', 'analyze', 'generate', 'create', 'manage', 'track', 'monitor']
            for line in lines:
                for word in action_words:
                    if word in line.lower():
                        requirements.append(line.strip())
                        break
        
        return {
            'title': title,
            'description': description or f"An AI agent for {agent_type} tasks",
            'requirements': requirements[:10],  # Limit to 10 requirements
            'agent_type': agent_type,
            'source': 'openai_conversation'
        }

async def main():
    """Main MCP server loop"""
    server = EndCapAgentFactoryMCPServer()
    
    while True:
        try:
            # Read request from stdin
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            # Write response to stdout (skip for notifications that return None)
            if response is not None:
                print(json.dumps(response))
                sys.stdout.flush()
            
        except json.JSONDecodeError:
            error_response = {'error': 'Invalid JSON request'}
            print(json.dumps(error_response))
            sys.stdout.flush()
        except Exception as e:
            error_response = {'error': str(e)}
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == '__main__':
    asyncio.run(main())
