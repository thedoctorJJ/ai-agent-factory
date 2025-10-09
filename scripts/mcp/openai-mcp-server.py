#!/usr/bin/env python3
"""
OpenAI MCP Server for END_CAP Agent Factory
Receives PRDs from ChatGPT/OpenAI conversations and automatically delivers them to the platform
"""

import json
import sys
import os
import requests
import logging
from typing import Dict, Any, List
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIEndCapMCPServer:
    def __init__(self):
        self.endcap_api_url = os.getenv('ENDCAP_API_URL', 'http://localhost:8000')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests from OpenAI"""
        try:
            method = request.get('method')
            params = request.get('params', {})

            if method == 'create_prd_from_conversation':
                return await self.create_prd_from_conversation(params)
            elif method == 'deliver_prd_to_endcap':
                return await self.deliver_prd_to_endcap(params)
            elif method == 'trigger_devin_workflow':
                return await self.trigger_devin_workflow(params)
            elif method == 'get_endcap_status':
                return await self.get_endcap_status()
            else:
                return {
                    'error': f'Unknown method: {method}',
                    'available_methods': [
                        'create_prd_from_conversation',
                        'deliver_prd_to_endcap', 
                        'trigger_devin_workflow',
                        'get_endcap_status'
                    ]
                }
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {'error': str(e)}
    
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
    server = OpenAIEndCapMCPServer()
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line)
            response = await server.handle_request(request)
            
            sys.stdout.write(json.dumps(response) + '\n')
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            logger.error("Received invalid JSON from stdin.")
            sys.stdout.write(json.dumps({'error': 'Invalid JSON input'}) + '\n')
            sys.stdout.flush()
        except Exception as e:
            logger.error(f"Unhandled error in MCP server loop: {e}")
            sys.stdout.write(json.dumps({'error': f'Unhandled server error: {e}'}) + '\n')
            sys.stdout.flush()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
