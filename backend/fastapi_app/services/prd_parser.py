"""
Comprehensive PRD Parser Service
Extracts all fields from PRD templates and maps them to database schema
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date
import json


class PRDParser:
    """Comprehensive PRD parser that extracts all template fields"""
    
    def __init__(self):
        self.section_patterns = {
            'title': r'^#\s*\*?\*?Title\*?\*?\s*$',
            'description': r'^##\s*\*?\*?Description\*?\*?\s*$',
            'problem_statement': r'^##\s*\*?\*?Problem Statement\*?\*?\s*$',
            'target_users': r'^##\s*\*?\*?Target Users\*?\*?\s*$',
            'user_stories': r'^##\s*\*?\*?User Stories\*?\*?\s*$',
            'requirements': r'^##\s*\*?\*?Requirements\*?\*?\s*$',
            'functional_requirements': r'^###\s*\*?\*?Functional Requirements\*?\*?\s*$',
            'non_functional_requirements': r'^###\s*\*?\*?Non-Functional Requirements\*?\*?\s*$',
            'platform_requirements': r'^###\s*\*?\*?Platform Requirements\*?\*?\s*$',
            'infrastructure_requirements': r'^###\s*\*?\*?Infrastructure Requirements\*?\*?\s*$',
            'operational_requirements': r'^###\s*\*?\*?Operational Requirements\*?\*?\s*$',
            'acceptance_criteria': r'^##\s*\*?\*?Acceptance Criteria\*?\*?\s*$',
            'technical_requirements': r'^##\s*\*?\*?Technical Requirements\*?\*?\s*$',
            'performance_requirements': r'^##\s*\*?\*?Performance Requirements\*?\*?\s*$',
            'security_requirements': r'^##\s*\*?\*?Security Requirements\*?\*?\s*$',
            'integration_requirements': r'^##\s*\*?\*?Integration Requirements\*?\*?\s*$',
            'deployment_requirements': r'^##\s*\*?\*?Deployment Requirements\*?\*?\s*$',
            'success_metrics': r'^##\s*\*?\*?Success Metrics\*?\*?\s*$',
            'timeline': r'^##\s*\*?\*?Timeline\*?\*?\s*$',
            'dependencies': r'^##\s*\*?\*?Dependencies\*?\*?\s*$',
            'risks': r'^##\s*\*?\*?Risks\*?\*?\s*$',
            'assumptions': r'^##\s*\*?\*?Assumptions\*?\*?\s*$',
            'agent_capabilities': r'^##\s*\*?\*?Agent Capabilities\*?\*?\s*$',
        }
    
    def parse_prd_content(self, content: str, filename: str = None) -> Dict[str, Any]:
        """
        Parse PRD content and extract all fields according to template structure
        """
        lines = content.split('\n')
        
        # Initialize result with defaults
        result = {
            'title': 'Untitled PRD',
            'description': '',
            'prd_type': 'agent',  # Default to agent
            'problem_statement': '',
            'target_users': [],
            'user_stories': [],
            'requirements': [],
            'functional_requirements': [],
            'non_functional_requirements': [],
            'platform_requirements': [],
            'infrastructure_requirements': [],
            'operational_requirements': [],
            'agent_capabilities': [],
            'acceptance_criteria': [],
            'technical_requirements': [],
            'performance_requirements': {},
            'security_requirements': [],
            'integration_requirements': [],
            'deployment_requirements': [],
            'success_metrics': [],
            'timeline': '',
            'start_date': None,
            'target_completion_date': None,
            'key_milestones': [],
            'dependencies': [],
            'risks': [],
            'assumptions': [],
            'original_filename': filename,
            'file_content': content
        }
        
        # Extract title first
        result['title'] = self._extract_title(lines)
        
        # Determine PRD type based on content
        result['prd_type'] = self._determine_prd_type(content, filename)
        
        # First, try to extract inline fields (e.g., **Description:** value)
        self._extract_inline_fields(content, result)
        
        # Parse all sections
        sections = self._identify_sections(lines)
        
        for section_name, section_content in sections.items():
            if section_name in result:
                if section_name in ['target_users', 'user_stories', 'requirements', 
                                  'functional_requirements', 'non_functional_requirements',
                                  'platform_requirements', 'infrastructure_requirements',
                                  'operational_requirements', 'agent_capabilities',
                                  'acceptance_criteria', 'technical_requirements',
                                  'security_requirements', 'integration_requirements',
                                  'deployment_requirements', 'success_metrics',
                                  'key_milestones', 'dependencies', 'risks', 'assumptions']:
                    parsed_value = self._parse_list_section(section_content)
                    # Only override if we don't already have a value from inline extraction
                    if not result[section_name] or (isinstance(result[section_name], list) and len(result[section_name]) == 0):
                        result[section_name] = parsed_value
                elif section_name == 'performance_requirements':
                    parsed_value = self._parse_performance_requirements(section_content)
                    if not result[section_name]:
                        result[section_name] = parsed_value
                elif section_name == 'timeline':
                    timeline_data = self._parse_timeline(section_content)
                    if not result['timeline']:
                        result['timeline'] = timeline_data['timeline']
                    if not result['start_date']:
                        result['start_date'] = timeline_data['start_date']
                    if not result['target_completion_date']:
                        result['target_completion_date'] = timeline_data['target_completion_date']
                    if not result['key_milestones']:
                        result['key_milestones'] = timeline_data['key_milestones']
                else:
                    parsed_value = self._parse_text_section(section_content)
                    # Only override if we don't already have a value from inline extraction
                    if not result[section_name] or (isinstance(result[section_name], str) and not result[section_name].strip()):
                        result[section_name] = parsed_value
        
        return result
    
    def _extract_title(self, lines: List[str]) -> str:
        """Extract title from PRD content with improved logic"""
        if not lines:
            return "Untitled PRD"

        # Helper function to strip markdown formatting
        def strip_markdown(text: str) -> str:
            """Remove markdown formatting from text"""
            # Remove bold (**text** or __text__)
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            text = re.sub(r'__(.+?)__', r'\1', text)
            # Remove italic (*text* or _text_)
            text = re.sub(r'\*(.+?)\*', r'\1', text)
            text = re.sub(r'_(.+?)_', r'\1', text)
            # Remove inline code (`text`)
            text = re.sub(r'`(.+?)`', r'\1', text)
            return text.strip()

        # First, look for explicit title sections
        for i, line in enumerate(lines):
            line = line.strip()
            if line.lower() in ['## title', '## **title**', '### title', '### **title**']:
                # Found a title section, get the next non-empty line
                for j in range(i + 1, min(i + 3, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not next_line.startswith('#'):
                        return strip_markdown(next_line)

        # Look for the first meaningful heading (H1 or H2)
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                # H1 heading - this is likely the main title
                title = strip_markdown(line[2:].strip())
                if title and len(title) > 3:  # Must be meaningful
                    return title
            elif line.startswith('## ') and not any(keyword in line.lower() for keyword in ['description', 'overview', 'summary', 'introduction', 'title']):
                # H2 heading that's not a section header
                title = strip_markdown(line[3:].strip())
                if title and len(title) > 3:
                    return title

        # Look for title patterns in the first few lines
        for i, line in enumerate(lines[:5]):  # Check first 5 lines
            line = line.strip()
            if not line:
                continue

            # Skip common PRD headers
            if any(header in line.lower() for header in [
                'product requirements document',
                'prd',
                'document information',
                'table of contents',
                'overview',
                'summary'
            ]):
                continue

            # Look for title-like patterns
            if (len(line) > 5 and len(line) < 100 and
                not line.startswith('#') and
                not line.startswith('-') and
                not line.startswith('*') and
                not line.startswith('1.') and
                not line.startswith('2.') and
                not line.startswith('3.') and
                not line.startswith('4.') and
                not line.startswith('5.') and
                not line.startswith('##') and
                not line.startswith('###')):
                return line

        # Fallback: use first non-empty line
        for line in lines:
            line = line.strip()
            if line and len(line) > 3:
                return line[:100]  # Limit length

        return "Untitled PRD"
    
    def _extract_inline_fields(self, content: str, result: Dict[str, Any]) -> None:
        """Extract fields from inline format like **Field:** value"""
        lines = content.split('\n')
        
        # Map of inline field patterns to result keys
        field_patterns = {
            r'\*\*Description:\*\*': 'description',
            r'\*\*Problem Statement:\*\*': 'problem_statement',
            r'\*\*Description\*\*:': 'description',
            r'\*\*Problem Statement\*\*:': 'problem_statement',
        }
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            # Check for inline field patterns
            for pattern, field_key in field_patterns.items():
                if re.search(pattern, line_stripped, re.IGNORECASE):
                    # Extract value after the colon
                    match = re.search(r':\s*(.+)', line_stripped)
                    if match:
                        value = match.group(1).strip()
                        # Remove any remaining markdown formatting (including leading/trailing **)
                        value = re.sub(r'^\*\*\s*', '', value)  # Remove leading **
                        value = re.sub(r'\s*\*\*$', '', value)  # Remove trailing **
                        value = re.sub(r'\*\*(.+?)\*\*', r'\1', value)  # Remove inline **
                        value = re.sub(r'\*(.+?)\*', r'\1', value)  # Remove inline *
                        if value and (not result[field_key] or (isinstance(result[field_key], str) and not result[field_key].strip())):
                            result[field_key] = value
                    break
            
            # Also check for Requirements inline format
            if re.search(r'\*\*Requirements?:\*\*', line_stripped, re.IGNORECASE):
                # Look for list items on following lines
                requirements = []
                for next_line in lines[lines.index(line) + 1:]:
                    next_line_stripped = next_line.strip()
                    if not next_line_stripped:
                        continue
                    if next_line_stripped.startswith('-') or next_line_stripped.startswith('*'):
                        # Extract requirement text
                        req_text = re.sub(r'^[\*\-\+]\s*', '', next_line_stripped)
                        req_text = re.sub(r'\*\*(.+?)\*\*', r'\1', req_text)
                        req_text = re.sub(r'\*(.+?)\*', r'\1', req_text)
                        if req_text.strip():
                            requirements.append(req_text.strip())
                    elif next_line_stripped.startswith('#'):
                        # Hit another section, stop
                        break
                if requirements and (not result['requirements'] or len(result['requirements']) == 0):
                    result['requirements'] = requirements
    
    def _determine_prd_type(self, content: str, filename: str = None) -> str:
        """Determine PRD type based on content and filename"""
        content_lower = content.lower()
        
        # Check filename for type indicators
        if filename:
            filename_lower = filename.lower()
            if 'platform' in filename_lower:
                return 'platform'
            elif 'agent' in filename_lower:
                return 'agent'
        
        # Check content for type indicators
        platform_indicators = [
            'platform', 'infrastructure', 'system', 'deployment', 
            'scalability', 'monitoring', 'operational'
        ]
        
        agent_indicators = [
            'ai agent', 'agent', 'artificial intelligence', 'machine learning',
            'automation', 'chatbot', 'assistant', 'intelligent'
        ]
        
        platform_score = sum(1 for indicator in platform_indicators if indicator in content_lower)
        agent_score = sum(1 for indicator in agent_indicators if indicator in content_lower)
        
        if platform_score > agent_score:
            return 'platform'
        else:
            return 'agent'  # Default to agent
    
    def _identify_sections(self, lines: List[str]) -> Dict[str, List[str]]:
        """Identify and extract all sections from PRD content"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Check if this line is a section header
            section_found = None
            for section_name, pattern in self.section_patterns.items():
                if re.match(pattern, line_stripped, re.IGNORECASE):
                    section_found = section_name
                    break
            
            if section_found:
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = current_content
                
                # Start new section
                current_section = section_found
                current_content = []
            elif current_section and line_stripped:
                # Add content to current section
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = current_content
        
        return sections
    
    def _parse_list_section(self, content: List[str]) -> List[str]:
        """Parse a section that contains a list of items"""
        items = []
        
        for line in content:
            line = line.strip()
            if not line or line.startswith('---'):
                continue
            
            # Remove markdown list markers
            line = re.sub(r'^[\*\-\+]\s*', '', line)
            line = re.sub(r'^\d+\.\s*', '', line)
            line = re.sub(r'^\s*\[\s*\]\s*', '', line)  # Remove checkbox markers
            
            # Remove bold/italic markers
            line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
            line = re.sub(r'\*(.*?)\*', r'\1', line)
            
            if line and len(line) > 2:
                items.append(line)
        
        return items
    
    def _parse_text_section(self, content: List[str]) -> str:
        """Parse a section that contains plain text"""
        text_lines = []
        
        for line in content:
            line = line.strip()
            if line and not line.startswith('---'):
                # Remove markdown formatting
                line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
                line = re.sub(r'\*(.*?)\*', r'\1', line)
                text_lines.append(line)
        
        return '\n'.join(text_lines)
    
    def _parse_performance_requirements(self, content: List[str]) -> Dict[str, Any]:
        """Parse performance requirements into structured format"""
        performance = {}
        
        for line in content:
            line = line.strip()
            if not line or line.startswith('---'):
                continue
            
            # Look for key-value pairs
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace('*', '').replace(' ', '_')
                value = value.strip()
                performance[key] = value
        
        return performance
    
    def _parse_timeline(self, content: List[str]) -> Dict[str, Any]:
        """Parse timeline section and extract dates and milestones"""
        timeline_data = {
            'timeline': '',
            'start_date': None,
            'target_completion_date': None,
            'key_milestones': []
        }
        
        timeline_text = []
        
        for line in content:
            line = line.strip()
            if not line or line.startswith('---'):
                continue
            
            # Look for date patterns
            if 'start date' in line.lower():
                date_match = re.search(r'(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})', line)
                if date_match:
                    try:
                        timeline_data['start_date'] = datetime.strptime(date_match.group(1), '%Y-%m-%d').date()
                    except ValueError:
                        try:
                            timeline_data['start_date'] = datetime.strptime(date_match.group(1), '%m/%d/%Y').date()
                        except ValueError:
                            pass
            
            elif 'target completion' in line.lower() or 'completion date' in line.lower():
                date_match = re.search(r'(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})', line)
                if date_match:
                    try:
                        timeline_data['target_completion_date'] = datetime.strptime(date_match.group(1), '%Y-%m-%d').date()
                    except ValueError:
                        try:
                            timeline_data['target_completion_date'] = datetime.strptime(date_match.group(1), '%m/%d/%Y').date()
                        except ValueError:
                            pass
            
            elif 'milestone' in line.lower():
                # Extract milestone
                milestone = re.sub(r'^[\*\-\+]\s*', '', line)
                milestone = re.sub(r'^\d+\.\s*', '', milestone)
                if milestone and len(milestone) > 2:
                    timeline_data['key_milestones'].append(milestone)
            
            else:
                timeline_text.append(line)
        
        timeline_data['timeline'] = '\n'.join(timeline_text)
        return timeline_data
    
    def validate_prd_structure(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that the parsed PRD has the required structure"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'completeness_score': 0
        }
        
        required_fields = ['title', 'description', 'problem_statement']
        optional_fields = [
            'target_users', 'user_stories', 'requirements', 'acceptance_criteria',
            'technical_requirements', 'success_metrics', 'timeline'
        ]
        
        # Check required fields (but don't fail validation - just warn)
        for field in required_fields:
            if not parsed_data.get(field) or (isinstance(parsed_data[field], str) and not parsed_data[field].strip()):
                validation_result['warnings'].append(f"Missing or empty field: {field}")
                # Don't mark as invalid - allow PRDs with missing fields to be created
                # validation_result['is_valid'] = False
        
        # Check optional fields and calculate completeness
        present_fields = 0
        total_fields = len(required_fields) + len(optional_fields)
        
        for field in required_fields + optional_fields:
            if parsed_data.get(field):
                if isinstance(parsed_data[field], str) and parsed_data[field].strip():
                    present_fields += 1
                elif isinstance(parsed_data[field], list) and len(parsed_data[field]) > 0:
                    present_fields += 1
                elif isinstance(parsed_data[field], dict) and parsed_data[field]:
                    present_fields += 1
        
        validation_result['completeness_score'] = (present_fields / total_fields) * 100
        
        # Add warnings for low completeness
        if validation_result['completeness_score'] < 50:
            validation_result['warnings'].append("PRD has low completeness score - consider adding more details")
        
        return validation_result
