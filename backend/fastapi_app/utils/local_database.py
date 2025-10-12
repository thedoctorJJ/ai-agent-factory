"""
Local SQLite database manager as a fallback when Supabase is not available.
"""
import sqlite3
import json
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import os

class LocalDatabaseManager:
    """Local SQLite database manager for development and testing."""
    
    def __init__(self, db_path: str = "ai_agent_factory.db"):
        """Initialize the local database manager."""
        self.db_path = db_path
        self._connected = False
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database with required tables."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create PRDs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prds (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    requirements TEXT,
                    prd_type TEXT NOT NULL DEFAULT 'agent',
                    status TEXT NOT NULL DEFAULT 'queue',
                    github_repo_url TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    problem_statement TEXT,
                    target_users TEXT,
                    user_stories TEXT,
                    acceptance_criteria TEXT,
                    technical_requirements TEXT,
                    performance_requirements TEXT,
                    security_requirements TEXT,
                    integration_requirements TEXT,
                    deployment_requirements TEXT,
                    success_metrics TEXT,
                    timeline TEXT,
                    dependencies TEXT,
                    risks TEXT,
                    assumptions TEXT,
                    category TEXT,
                    priority TEXT,
                    effort_estimate TEXT,
                    business_value INTEGER,
                    technical_complexity INTEGER,
                    dependencies_list TEXT,
                    assignee TEXT,
                    target_sprint TEXT,
                    original_filename TEXT,
                    file_content TEXT
                )
            ''')
            
            # Create agents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    purpose TEXT NOT NULL,
                    version TEXT NOT NULL,
                    tools TEXT,
                    prompts TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    repository_url TEXT,
                    deployment_url TEXT,
                    health_check_url TEXT,
                    prd_id TEXT,
                    devin_task_id TEXT,
                    capabilities TEXT,
                    configuration TEXT,
                    last_health_check TEXT,
                    health_status TEXT NOT NULL DEFAULT 'unknown',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Create devin_tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devin_tasks (
                    id TEXT PRIMARY KEY,
                    prd_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    requirements TEXT,
                    devin_prompt TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    devin_output TEXT,
                    agent_code TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            self._connected = True
            print(f"✅ Local SQLite database initialized: {self.db_path}")
            
        except Exception as e:
            print(f"❌ Failed to initialize local database: {e}")
            self._connected = False
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._connected
    
    async def test_connection(self) -> bool:
        """Test database connection."""
        return self._connected
    
    def _serialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize data for SQLite storage."""
        serialized = {}
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                serialized[key] = json.dumps(value)
            else:
                serialized[key] = value
        return serialized
    
    def _deserialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Deserialize data from SQLite storage."""
        deserialized = {}
        for key, value in data.items():
            if key in ['requirements', 'target_users', 'user_stories', 'acceptance_criteria', 
                      'technical_requirements', 'security_requirements', 'integration_requirements',
                      'deployment_requirements', 'success_metrics', 'dependencies', 'risks',
                      'assumptions', 'dependencies_list', 'tools', 'prompts', 'capabilities']:
                try:
                    deserialized[key] = json.loads(value) if value else []
                except (json.JSONDecodeError, TypeError):
                    deserialized[key] = []
            elif key in ['performance_requirements', 'configuration']:
                try:
                    deserialized[key] = json.loads(value) if value else {}
                except (json.JSONDecodeError, TypeError):
                    deserialized[key] = {}
            else:
                deserialized[key] = value
        return deserialized
    
    async def create_prd(self, prd_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new PRD."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            serialized_data = self._serialize_data(prd_data)
            columns = ', '.join(serialized_data.keys())
            placeholders = ', '.join(['?' for _ in serialized_data])
            values = list(serialized_data.values())
            
            cursor.execute(f'''
                INSERT INTO prds ({columns})
                VALUES ({placeholders})
            ''', values)
            
            conn.commit()
            conn.close()
            
            print(f"✅ PRD created in local database: {prd_data.get('id')}")
            return prd_data
            
        except Exception as e:
            print(f"❌ Failed to create PRD in local database: {e}")
            return None
    
    async def get_prds(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all PRDs."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM prds 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            ''', (limit, skip))
            
            rows = cursor.fetchall()
            conn.close()
            
            prds = []
            for row in rows:
                prd_data = dict(row)
                prds.append(self._deserialize_data(prd_data))
            
            print(f"✅ Retrieved {len(prds)} PRDs from local database")
            return prds
            
        except Exception as e:
            print(f"❌ Failed to get PRDs from local database: {e}")
            return []
    
    async def get_prd(self, prd_id: str) -> Optional[Dict[str, Any]]:
        """Get a PRD by ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM prds WHERE id = ?', (prd_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                prd_data = dict(row)
                return self._deserialize_data(prd_data)
            return None
            
        except Exception as e:
            print(f"❌ Failed to get PRD from local database: {e}")
            return None
    
    async def update_prd(self, prd_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a PRD."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.utcnow().isoformat()
            
            serialized_data = self._serialize_data(update_data)
            set_clause = ', '.join([f'{key} = ?' for key in serialized_data.keys()])
            values = list(serialized_data.values()) + [prd_id]
            
            cursor.execute(f'''
                UPDATE prds 
                SET {set_clause}
                WHERE id = ?
            ''', values)
            
            conn.commit()
            conn.close()
            
            print(f"✅ PRD updated in local database: {prd_id}")
            return await self.get_prd(prd_id)
            
        except Exception as e:
            print(f"❌ Failed to update PRD in local database: {e}")
            return None
    
    async def create_agent(self, agent_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new agent."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            serialized_data = self._serialize_data(agent_data)
            columns = ', '.join(serialized_data.keys())
            placeholders = ', '.join(['?' for _ in serialized_data])
            values = list(serialized_data.values())
            
            cursor.execute(f'''
                INSERT INTO agents ({columns})
                VALUES ({placeholders})
            ''', values)
            
            conn.commit()
            conn.close()
            
            print(f"✅ Agent created in local database: {agent_data.get('id')}")
            return agent_data
            
        except Exception as e:
            print(f"❌ Failed to create agent in local database: {e}")
            return None
    
    async def get_agents(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all agents."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM agents 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            ''', (limit, skip))
            
            rows = cursor.fetchall()
            conn.close()
            
            agents = []
            for row in rows:
                agent_data = dict(row)
                agents.append(self._deserialize_data(agent_data))
            
            print(f"✅ Retrieved {len(agents)} agents from local database")
            return agents
            
        except Exception as e:
            print(f"❌ Failed to get agents from local database: {e}")
            return []
    
    async def create_devin_task(self, task_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new Devin task."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            serialized_data = self._serialize_data(task_data)
            columns = ', '.join(serialized_data.keys())
            placeholders = ', '.join(['?' for _ in serialized_data])
            values = list(serialized_data.values())
            
            cursor.execute(f'''
                INSERT INTO devin_tasks ({columns})
                VALUES ({placeholders})
            ''', values)
            
            conn.commit()
            conn.close()
            
            print(f"✅ Devin task created in local database: {task_data.get('id')}")
            return task_data
            
        except Exception as e:
            print(f"❌ Failed to create Devin task in local database: {e}")
            return None
    
    async def get_devin_tasks(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all Devin tasks."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM devin_tasks 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            ''', (limit, skip))
            
            rows = cursor.fetchall()
            conn.close()
            
            tasks = []
            for row in rows:
                task_data = dict(row)
                tasks.append(self._deserialize_data(task_data))
            
            print(f"✅ Retrieved {len(tasks)} Devin tasks from local database")
            return tasks
            
        except Exception as e:
            print(f"❌ Failed to get Devin tasks from local database: {e}")
            return []

# Create a global instance
local_db_manager = LocalDatabaseManager()
