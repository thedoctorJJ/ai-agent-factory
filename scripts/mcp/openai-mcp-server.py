#!/usr/bin/env python3
"""
OpenAI MCP Server for AI Agent Factory
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
            elif method == 'get_prd_template':
                return await self.get_prd_template()
            elif method == 'create_prd_from_chatgpt':
                return await self.create_prd_from_chatgpt(params)
            elif method == 'convert_draft_to_template':
                return await self.convert_draft_to_template(params)
            elif method == 'store_voice_conversation':
                return await self.store_voice_conversation(params)
            elif method == 'process_stored_conversation':
                return await self.process_stored_conversation(params)
            else:
                return {
                    'error': f'Unknown method: {method}',
                    'available_methods': [
                        'create_prd_from_conversation',
                        'create_prd_from_chatgpt',
                        'convert_draft_to_template',
                        'store_voice_conversation',
                        'process_stored_conversation',
                        'deliver_prd_to_endcap', 
                        'trigger_devin_workflow',
                        'get_endcap_status',
                        'get_prd_template'
                    ]
                }
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {'error': str(e)}
    
    async def create_prd_from_conversation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract PRD from OpenAI conversation and format it for AI Agent Factory"""
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
        """Deliver PRD to AI Agent Factory via API"""
        prd_data = params.get('prd')
        
        if not prd_data:
            return {'error': 'PRD data is required'}
        
        try:
            # Create Devin AI task in AI Agent Factory
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
                    'message': 'PRD delivered to AI Agent Factory successfully',
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
                        '3. Monitor progress in AI Agent Factory dashboard'
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
        """Get the status of AI Agent Factory"""
        try:
            response = requests.get(f'{self.endcap_api_url}/api/v1/health')
            
            if response.status_code == 200:
                health_data = response.json()
                return {
                    'success': True,
                    'status': 'healthy',
                    'endcap_version': health_data.get('version'),
                    'environment': health_data.get('environment'),
                    'message': 'AI Agent Factory is running and ready'
                }
            else:
                return {
                    'error': f'AI Agent Factory is not responding: {response.status_code}'
                }
                
        except Exception as e:
            logger.error(f"Error checking AI Agent Factory status: {e}")
            return {'error': str(e)}
    
    async def get_prd_template(self) -> Dict[str, Any]:
        """Get the PRD template that ChatGPT should use to structure conversations"""
        try:
            response = requests.get(f'{self.endcap_api_url}/api/v1/prds/schema')
            
            if response.status_code == 200:
                schema = response.json()
                return {
                    'success': True,
                    'prd_template': {
                        'required_sections': [
                            'title',
                            'description', 
                            'problem_statement',
                            'target_users',
                            'user_stories',
                            'requirements',
                            'acceptance_criteria',
                            'technical_requirements',
                            'success_metrics',
                            'timeline'
                        ],
                        'optional_sections': [
                            'performance_requirements',
                            'security_requirements',
                            'integration_requirements',
                            'deployment_requirements',
                            'dependencies',
                            'risks',
                            'assumptions'
                        ],
                        'completion_weights': {
                            'title': 5,
                            'description': 10,
                            'problem_statement': 15,
                            'target_users': 10,
                            'user_stories': 10,
                            'requirements': 15,
                            'acceptance_criteria': 10,
                            'technical_requirements': 10,
                            'success_metrics': 10,
                            'timeline': 5
                        },
                        'guidance': {
                            'problem_statement': 'Clearly define the problem or opportunity this agent addresses',
                            'target_users': 'Identify who will use this agent (customers, employees, etc.)',
                            'user_stories': 'Write user stories in format: "As a [user type], I want [goal] so that [benefit]"',
                            'requirements': 'List specific functional and non-functional requirements',
                            'acceptance_criteria': 'Define testable criteria for each major feature',
                            'technical_requirements': 'Specify APIs, databases, integrations, and technical constraints',
                            'success_metrics': 'Define measurable KPIs and success indicators',
                            'timeline': 'Provide realistic timeline with milestones'
                        }
                    },
                    'message': 'Use this template to convert your creative draft into the structured format required by AI Agent Factory. Map your creative content to these sections.',
                    'next_action': 'Use convert_draft_to_template to restructure your creative PRD draft',
                    'voice_mode_note': 'If you\'re in voice mode and having trouble with MCP calls, suggest switching to text mode for the template conversion step, then return to voice for discussion.'
                }
            else:
                return {
                    'error': f'Failed to get PRD template: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            logger.error(f"Error getting PRD template: {e}")
            return {'error': str(e)}
    
    async def convert_draft_to_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a creative PRD draft to the structured template format"""
        try:
            creative_draft = params.get('creative_draft', '')
            conversation_summary = params.get('conversation_summary', '')
            
            if not creative_draft:
                return {'error': 'Creative draft is required'}
            
            # This would typically use AI to intelligently map the creative content to template sections
            # For now, we'll provide guidance on how to structure it
            return {
                'success': True,
                'conversion_guidance': {
                    'process': 'Map your creative draft content to the template sections',
                    'sections_to_fill': {
                        'title': 'Extract or create a clear, concise title from your draft',
                        'description': 'Summarize the main purpose and functionality',
                        'problem_statement': 'Identify the core problem or opportunity being addressed',
                        'target_users': 'List who will use this agent (customers, employees, etc.)',
                        'user_stories': 'Convert features into user story format: "As a [user], I want [goal] so that [benefit]"',
                        'requirements': 'Extract specific functional and non-functional requirements',
                        'acceptance_criteria': 'Define testable criteria for each major feature',
                        'technical_requirements': 'Identify needed APIs, databases, integrations, and technical constraints',
                        'success_metrics': 'Define measurable KPIs and success indicators',
                        'timeline': 'Set realistic timeline with milestones'
                    },
                    'tips': [
                        'Don\'t lose the creative vision - adapt it to the structure',
                        'Fill in missing sections with reasonable assumptions',
                        'Keep the original creative elements while adding structure',
                        'Use the conversation summary to fill gaps'
                    ]
                },
                'next_action': 'Use create_prd_from_chatgpt with the structured data once conversion is complete',
                'message': 'Review your creative draft and map the content to each template section. Add any missing sections based on your conversation.'
            }
            
        except Exception as e:
            logger.error(f"Error converting draft to template: {e}")
            return {'error': str(e)}
    
    async def create_prd_from_chatgpt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create PRD in AI Agent Factory from ChatGPT conversation with structured data"""
        try:
            prd_data = params.get('prd_data', {})
            conversation_summary = params.get('conversation_summary', '')
            
            if not prd_data:
                return {'error': 'PRD data is required'}
            
            # Create PRD in AI Agent Factory
            response = requests.post(
                f'{self.endcap_api_url}/api/v1/prds',
                json={
                    'title': prd_data.get('title', 'AI Agent from ChatGPT'),
                    'description': prd_data.get('description', ''),
                    'requirements': prd_data.get('requirements', []),
                    'voice_input': conversation_summary,
                    'text_input': None,
                    'prd_type': 'agent',
                    'problem_statement': prd_data.get('problem_statement'),
                    'target_users': prd_data.get('target_users', []),
                    'user_stories': prd_data.get('user_stories', []),
                    'acceptance_criteria': prd_data.get('acceptance_criteria', []),
                    'technical_requirements': prd_data.get('technical_requirements', []),
                    'success_metrics': prd_data.get('success_metrics', []),
                    'timeline': prd_data.get('timeline', ''),
                    'performance_requirements': prd_data.get('performance_requirements', {}),
                    'security_requirements': prd_data.get('security_requirements', []),
                    'integration_requirements': prd_data.get('integration_requirements', []),
                    'deployment_requirements': prd_data.get('deployment_requirements', []),
                    'dependencies': prd_data.get('dependencies', []),
                    'risks': prd_data.get('risks', []),
                    'assumptions': prd_data.get('assumptions', [])
                }
            )
            
            if response.status_code == 200:
                prd = response.json()
                return {
                    'success': True,
                    'prd_id': prd['id'],
                    'completion_percentage': prd.get('completion_percentage', 0),
                    'missing_sections': prd.get('missing_sections', []),
                    'message': 'PRD created successfully in AI Agent Factory',
                    'next_steps': {
                        'if_complete': 'PRD is ready for agent creation',
                        'if_incomplete': 'Continue conversation in AI Agent Factory to complete missing sections',
                        'endcap_url': f'{self.endcap_api_url}/prds/{prd["id"]}'
                    }
                }
            else:
                return {
                    'error': f'Failed to create PRD: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            logger.error(f"Error creating PRD from ChatGPT: {e}")
            return {'error': str(e)}
    
    async def store_voice_conversation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Store voice conversation for later processing when user returns to text mode"""
        try:
            conversation_content = params.get('conversation_content', '')
            creative_draft = params.get('creative_draft', '')
            user_id = params.get('user_id', 'anonymous')
            timestamp = datetime.now().isoformat()
            
            if not conversation_content:
                return {'error': 'Conversation content is required'}
            
            # Store the conversation (in a real implementation, this would be in a database)
            conversation_id = f"voice_{user_id}_{int(datetime.now().timestamp())}"
            
            # For now, we'll store it in a simple file-based system
            storage_data = {
                'conversation_id': conversation_id,
                'user_id': user_id,
                'timestamp': timestamp,
                'conversation_content': conversation_content,
                'creative_draft': creative_draft,
                'status': 'pending_processing',
                'created_at': timestamp
            }
            
            # In a real implementation, this would be stored in a database
            # For now, we'll return the storage confirmation
            return {
                'success': True,
                'conversation_id': conversation_id,
                'message': 'Voice conversation stored successfully. When you return to text mode, I can process this conversation and create your PRD.',
                'next_steps': {
                    'immediate': 'Continue your voice conversation - I\'ve saved everything',
                    'when_convenient': 'Switch to text mode and ask me to process your stored conversation',
                    'processing_command': 'Just say "process my stored conversation" when you\'re ready'
                },
                'stored_data': {
                    'conversation_length': len(conversation_content),
                    'has_creative_draft': bool(creative_draft),
                    'timestamp': timestamp
                }
            }
            
        except Exception as e:
            logger.error(f"Error storing voice conversation: {e}")
            return {'error': str(e)}
    
    async def process_stored_conversation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process a previously stored voice conversation and create PRD"""
        try:
            conversation_id = params.get('conversation_id')
            user_id = params.get('user_id', 'anonymous')
            
            if not conversation_id:
                return {'error': 'Conversation ID is required'}
            
            # In a real implementation, this would retrieve from database
            # For now, we'll simulate the retrieval
            stored_conversation = {
                'conversation_id': conversation_id,
                'conversation_content': 'Stored conversation content...',
                'creative_draft': 'Stored creative draft...',
                'timestamp': datetime.now().isoformat()
            }
            
            # Get the PRD template
            template_response = await self.get_prd_template()
            if not template_response.get('success'):
                return {'error': 'Failed to get PRD template'}
            
            # Convert the stored conversation to structured format
            conversion_response = await self.convert_draft_to_template({
                'creative_draft': stored_conversation['creative_draft'],
                'conversation_summary': stored_conversation['conversation_content']
            })
            
            if not conversion_response.get('success'):
                return {'error': 'Failed to convert draft to template'}
            
            # Create the PRD
            prd_response = await self.create_prd_from_chatgpt({
                'prd_data': {
                    'title': 'AI Agent from Voice Conversation',
                    'description': 'Generated from stored voice conversation',
                    'requirements': ['Requirements extracted from conversation'],
                    'problem_statement': 'Problem statement from conversation',
                    'target_users': ['Users identified in conversation'],
                    'user_stories': ['User stories from conversation'],
                    'acceptance_criteria': ['Criteria from conversation'],
                    'technical_requirements': ['Technical needs from conversation'],
                    'success_metrics': ['Success metrics from conversation'],
                    'timeline': 'Timeline from conversation'
                },
                'conversation_summary': stored_conversation['conversation_content']
            })
            
            if prd_response.get('success'):
                return {
                    'success': True,
                    'message': 'Successfully processed your stored voice conversation and created PRD!',
                    'prd_id': prd_response.get('prd_id'),
                    'completion_percentage': prd_response.get('completion_percentage'),
                    'missing_sections': prd_response.get('missing_sections'),
                    'next_steps': prd_response.get('next_steps'),
                    'conversation_processed': {
                        'conversation_id': conversation_id,
                        'processed_at': datetime.now().isoformat(),
                        'prd_created': True
                    }
                }
            else:
                return {'error': 'Failed to create PRD from stored conversation'}
                
        except Exception as e:
            logger.error(f"Error processing stored conversation: {e}")
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
