"""
Database utilities for Supabase integration.
"""
import os
import asyncio
import time
from typing import Optional, Dict, Any, List
from supabase import create_client, Client
from ..config import config
# Removed local_database import - using only Supabase now


class DatabaseManager:
    """Database manager for Supabase operations with connection pooling and retry logic."""
    
    def __init__(self):
        """Initialize the database manager."""
        self._client: Optional[Client] = None
        self._connected = False
        self._max_retries = 3
        self._retry_delay = 1  # seconds
        self._connection_timeout = 30  # seconds
    
    @property
    def client(self) -> Client:
        """Get the Supabase client."""
        if self._client is None:
            self._connect()
        return self._client
    
    def _connect(self) -> None:
        """Connect to Supabase with retry logic."""
        for attempt in range(self._max_retries):
            try:
                supabase_url = config.supabase_url
                supabase_key = config.supabase_key
                
                if not supabase_url or not supabase_key:
                    raise ValueError("Supabase URL and key are required")
                
                self._client = create_client(supabase_url, supabase_key)
                self._connected = True
                print(f"✅ Connected to Supabase database (attempt {attempt + 1})")
                return
            except Exception as e:
                print(f"❌ Failed to connect to Supabase (attempt {attempt + 1}): {e}")
                if attempt < self._max_retries - 1:
                    print(f"⏳ Retrying in {self._retry_delay} seconds...")
                    time.sleep(self._retry_delay)
                    self._retry_delay *= 2  # Exponential backoff
                else:
                    self._connected = False
                    raise
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        try:
            # Test if we can create a client and make a simple query
            if self._client is None:
                self._connect()
            
            # Try a simple query to test connection
            result = self.client.table('prds').select('id').limit(1).execute()
            return True
        except Exception as e:
            print(f"❌ Supabase connection check failed: {e}")
            return False
    
    async def _retry_operation(self, operation, *args, **kwargs):
        """Retry a database operation with exponential backoff."""
        for attempt in range(self._max_retries):
            try:
                return await operation(*args, **kwargs)
            except Exception as e:
                print(f"❌ Database operation failed (attempt {attempt + 1}): {e}")
                if attempt < self._max_retries - 1:
                    delay = self._retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"⏳ Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    raise
    
    async def test_connection(self) -> bool:
        """Test database connection."""
        try:
            # Try to query a simple table
            result = self.client.table('agents').select('id').limit(1).execute()
            return True
        except Exception as e:
            print(f"❌ Supabase connection test failed: {e}")
            return False
    
    async def initialize_schema(self) -> None:
        """Initialize database schema if it doesn't exist."""
        try:
            # Read and execute the schema file
            import os
            schema_path = os.path.join(os.path.dirname(__file__), '../../../../infra/database/schema.sql')
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                # Note: Supabase client doesn't support raw SQL execution
                # This would need to be done via Supabase dashboard or CLI
                print("Schema file found. Please run the schema.sql file in your Supabase dashboard.")
            else:
                print("Schema file not found. Creating basic tables...")
                await self._create_basic_tables()
        except Exception as e:
            print(f"Schema initialization error: {e}")
            raise
    
    async def _create_basic_tables(self) -> None:
        """Create basic tables if they don't exist."""
        # This is a fallback - in production, use proper migrations
        print("Basic table creation would go here - using Supabase dashboard for now")
    
    # PRD Operations
    async def create_prd(self, prd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a PRD in the database."""
        try:
            async def _create():
                result = self.client.table('prds').insert(prd_data).execute()
                return result.data[0] if result.data else None
            
            return await self._retry_operation(_create)
        except Exception as e:
            print(f"❌ Supabase PRD creation failed: {e}")
            raise e
    
    async def get_prds(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get PRDs from the database."""
        try:
            async def _get():
                query = self.client.table('prds').select('*')
                if status:
                    query = query.eq('status', status)
                result = query.range(skip, skip + limit - 1).execute()
                return result.data or []
            
            return await self._retry_operation(_get)
        except Exception as e:
            print(f"❌ Supabase PRD retrieval failed: {e}")
            raise e
    
    async def get_prd(self, prd_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific PRD by ID."""
        async def _get():
            result = self.client.table('prds').select('*').eq('id', prd_id).execute()
            return result.data[0] if result.data else None
        
        try:
            return await self._retry_operation(_get)
        except Exception as e:
            print(f"Error getting PRD: {e}")
            return None
    
    async def update_prd(self, prd_id: str, prd_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a PRD in the database."""
        try:
            async def _update():
                result = self.client.table('prds').update(prd_data).eq('id', prd_id).execute()
                return result.data[0] if result.data else None
            
            return await self._retry_operation(_update)
        except Exception as e:
            print(f"❌ Supabase PRD update failed: {e}")
            raise e
    
    async def delete_prd(self, prd_id: str) -> bool:
        """Delete a PRD from the database."""
        async def _delete():
            result = self.client.table('prds').delete().eq('id', prd_id).execute()
            return True
        
        try:
            return await self._retry_operation(_delete)
        except Exception as e:
            print(f"Error deleting PRD: {e}")
            return False

    async def clear_all_prds(self) -> bool:
        """Clear all PRDs from the database."""
        async def _clear():
            result = self.client.table('prds').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            return True
        
        try:
            return await self._retry_operation(_clear)
        except Exception as e:
            print(f"Error clearing all PRDs: {e}")
            return False
    
    # Agent Operations
    async def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an agent in the database."""
        async def _create():
            result = self.client.table('agents').insert(agent_data).execute()
            return result.data[0] if result.data else None
        
        return await self._retry_operation(_create)
    
    async def get_agents(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get agents from the database."""
        async def _get():
            result = self.client.table('agents').select('*').range(skip, skip + limit - 1).execute()
            return result.data or []
        
        try:
            return await self._retry_operation(_get)
        except Exception as e:
            print(f"Error getting agents: {e}")
            return []
    
    async def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific agent by ID."""
        async def _get():
            result = self.client.table('agents').select('*').eq('id', agent_id).execute()
            return result.data[0] if result.data else None
        
        try:
            return await self._retry_operation(_get)
        except Exception as e:
            print(f"Error getting agent: {e}")
            return None
    
    async def update_agent(self, agent_id: str, agent_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an agent in the database."""
        async def _update():
            result = self.client.table('agents').update(agent_data).eq('id', agent_id).execute()
            return result.data[0] if result.data else None
        
        try:
            return await self._retry_operation(_update)
        except Exception as e:
            print(f"Error updating agent: {e}")
            return None
    
    async def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent from the database."""
        async def _delete():
            result = self.client.table('agents').delete().eq('id', agent_id).execute()
            return True
        
        try:
            return await self._retry_operation(_delete)
        except Exception as e:
            print(f"Error deleting agent: {e}")
            return False

    async def clear_all_agents(self) -> bool:
        """Clear all agents from the database."""
        async def _clear():
            result = self.client.table('agents').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            return True
        
        try:
            return await self._retry_operation(_clear)
        except Exception as e:
            print(f"Error clearing all agents: {e}")
            return False
    
    # Devin Task Operations
    async def create_devin_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Devin task in the database."""
        async def _create():
            result = self.client.table('devin_tasks').insert(task_data).execute()
            return result.data[0] if result.data else None
        
        return await self._retry_operation(_create)
    
    async def get_devin_tasks(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get Devin tasks from the database."""
        async def _get():
            result = self.client.table('devin_tasks').select('*').range(skip, skip + limit - 1).execute()
            return result.data or []
        
        try:
            return await self._retry_operation(_get)
        except Exception as e:
            print(f"Error getting Devin tasks: {e}")
            return []
    
    async def get_devin_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific Devin task by ID."""
        async def _get():
            result = self.client.table('devin_tasks').select('*').eq('id', task_id).execute()
            return result.data[0] if result.data else None
        
        try:
            return await self._retry_operation(_get)
        except Exception as e:
            print(f"Error getting Devin task: {e}")
            return None
    
    async def update_devin_task(self, task_id: str, task_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a Devin task in the database."""
        async def _update():
            result = self.client.table('devin_tasks').update(task_data).eq('id', task_id).execute()
            return result.data[0] if result.data else None
        
        try:
            return await self._retry_operation(_update)
        except Exception as e:
            print(f"Error updating Devin task: {e}")
            return None


# Global database manager instance
db_manager = DatabaseManager()
