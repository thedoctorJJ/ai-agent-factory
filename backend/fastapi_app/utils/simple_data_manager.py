"""
Simplified data manager with Supabase + In-Memory storage.
No more complex fallback chains - just clean, predictable storage.
"""
import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from supabase import create_client, Client
from ..config import config


class SimpleDataManager:
    """Simplified data manager with mode-based storage."""
    
    def __init__(self, mode: str = "development"):
        """
        Initialize the data manager.
        
        Args:
            mode: "development" (in-memory only) or "production" (Supabase only)
        """
        self.mode = mode
        self.supabase: Optional[Client] = None
        self.memory_storage = {
            "agents": {},
            "prds": {}
        }
        
        if mode == "production":
            self._init_supabase()
    
    def _init_supabase(self):
        """Initialize Supabase client with retry logic."""
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                supabase_url = config.supabase_url
                supabase_key = config.supabase_key
                
                if not supabase_url or not supabase_key:
                    raise ValueError("Supabase URL and key are required for production mode")
                
                # Test DNS resolution by checking if URL is valid
                if not supabase_url.startswith('https://'):
                    raise ValueError(f"Invalid Supabase URL format: {supabase_url}")
                
                self.supabase = create_client(supabase_url, supabase_key)
                
                # Test connection with a simple query
                try:
                    self.supabase.table('prds').select('id').limit(1).execute()
                    print(f"✅ Connected to Supabase (mode: {self.mode}, attempt {attempt + 1})")
                    return
                except Exception as test_error:
                    # If test query fails, it might be a connection issue
                    error_str = str(test_error).lower()
                    if "name or service not known" in error_str or "nxdomain" in error_str:
                        raise ConnectionError(f"DNS resolution failed for Supabase URL: {supabase_url}. The domain may not exist or be unreachable.")
                    raise
                    
            except ConnectionError as e:
                # DNS/Network errors - don't retry
                print(f"❌ Connection error to Supabase: {e}")
                raise e
            except Exception as e:
                print(f"❌ Failed to connect to Supabase (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print(f"⏳ Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f"❌ Failed to connect to Supabase after {max_retries} attempts")
                    raise e
    
    def _prepare_data_for_db(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for database storage by converting datetime objects to ISO strings."""
        db_data = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                db_data[key] = value.isoformat()
            else:
                db_data[key] = value
        return db_data
    
    # Agent Operations
    async def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an agent."""
        if self.mode == "development":
            agent_id = agent_data.get("id", f"agent_{len(self.memory_storage['agents']) + 1}")
            self.memory_storage["agents"][agent_id] = agent_data
            return agent_data
        else:
            # Ensure datetime objects are converted to ISO strings for database storage
            db_data = self._prepare_data_for_db(agent_data)
            max_retries = 3
            retry_delay = 1
            
            for attempt in range(max_retries):
                try:
                    result = self.supabase.table('agents').insert(db_data).execute()
                    return result.data[0] if result.data else None
                except Exception as e:
                    error_str = str(e).lower()
                    # Check for DNS/network errors
                    if "name or service not known" in error_str or "nxdomain" in error_str or "connection" in error_str:
                        if attempt < max_retries - 1:
                            print(f"⚠️  Network error creating agent (attempt {attempt + 1}/{max_retries}): {e}")
                            print(f"   Retrying in {retry_delay} seconds...")
                            time.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                        else:
                            print(f"❌ Network error creating agent after {max_retries} attempts: {e}")
                            raise ConnectionError(f"Failed to connect to Supabase: {e}")
                    else:
                        # Log the error for debugging
                        print(f"❌ Error creating agent in database: {e}")
                        print(f"   Agent data: {db_data}")
                        # Re-raise to let the service handle it
                        raise
    
    async def get_agents(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get agents."""
        if self.mode == "development":
            agents = list(self.memory_storage["agents"].values())
            return agents[skip:skip + limit]
        else:
            result = self.supabase.table('agents').select('*').range(skip, skip + limit - 1).execute()
            return result.data or []
    
    async def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific agent."""
        if self.mode == "development":
            return self.memory_storage["agents"].get(agent_id)
        else:
            result = self.supabase.table('agents').select('*').eq('id', agent_id).execute()
            return result.data[0] if result.data else None
    
    async def get_agent_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get an agent by name."""
        if self.mode == "development":
            return next((a for a in self.memory_storage["agents"].values() if a.get("name") == name), None)
        else:
            result = self.supabase.table('agents').select('*').eq('name', name).execute()
            return result.data[0] if result.data else None
    
    async def update_agent(self, agent_id: str, agent_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an agent."""
        if self.mode == "development":
            if agent_id in self.memory_storage["agents"]:
                self.memory_storage["agents"][agent_id].update(agent_data)
                return self.memory_storage["agents"][agent_id]
            return None
        else:
            # Ensure datetime objects are converted to ISO strings for database storage
            db_data = self._prepare_data_for_db(agent_data)
            
            # Note: We skip PRD verification here because:
            # 1. The foreign key constraint will validate it
            # 2. RLS might prevent the verification check even though PRD exists
            # 3. If PRD doesn't exist, the foreign key constraint will fail with a clear error
            # The RLS fix should allow the foreign key check to work properly
            
            try:
                result = self.supabase.table('agents').update(db_data).eq('id', agent_id).execute()
                if result.data and len(result.data) > 0:
                    print(f"✅ Updated agent {agent_id}: {result.data[0].get('name', 'N/A')}")
                    return result.data[0]
                else:
                    # No rows updated - agent might not exist
                    print(f"⚠️  No agent found with ID {agent_id} to update")
                    return None
            except Exception as e:
                error_str = str(e).lower()
                if 'foreign key' in error_str or '23503' in str(e):
                    # Foreign key constraint violation - provide more helpful error
                    print(f"❌ Foreign key constraint violation: {e}")
                    if 'prd_id' in db_data:
                        print(f"   Attempted to set prd_id to: {db_data.get('prd_id')}")
                        print(f"   This might be an RLS (Row Level Security) issue.")
                        print(f"   The PRD exists but RLS might be blocking the foreign key check.")
                print(f"❌ Error updating agent {agent_id}: {e}")
                raise
    
    async def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent."""
        if self.mode == "development":
            if agent_id in self.memory_storage["agents"]:
                del self.memory_storage["agents"][agent_id]
                return True
            return False
        else:
            result = self.supabase.table('agents').delete().eq('id', agent_id).execute()
            return True
    
    async def clear_all_agents(self) -> bool:
        """Clear all agents."""
        if self.mode == "development":
            self.memory_storage["agents"].clear()
            return True
        else:
            result = self.supabase.table('agents').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            return True
    
    # PRD Operations
    async def create_prd(self, prd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a PRD."""
        if self.mode == "development":
            prd_id = prd_data.get("id", f"prd_{len(self.memory_storage['prds']) + 1}")
            self.memory_storage["prds"][prd_id] = prd_data
            return prd_data
        else:
            result = self.supabase.table('prds').insert(prd_data).execute()
            return result.data[0] if result.data else None
    
    async def get_prds(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get PRDs."""
        if self.mode == "development":
            prds = list(self.memory_storage["prds"].values())
            return prds[skip:skip + limit]
        else:
            result = self.supabase.table('prds').select('*').range(skip, skip + limit - 1).execute()
            return result.data or []
    
    async def get_prd(self, prd_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific PRD."""
        if self.mode == "development":
            return self.memory_storage["prds"].get(prd_id)
        else:
            result = self.supabase.table('prds').select('*').eq('id', prd_id).execute()
            return result.data[0] if result.data else None
    
    async def get_prd_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Get a PRD by title (case-insensitive, ignoring markdown formatting)."""
        if self.mode == "development":
            # Normalize title for comparison
            normalized_title = title.strip().lower().replace('*', '').replace('#', '').strip()
            for prd in self.memory_storage["prds"].values():
                prd_title = prd.get("title", "").strip().lower().replace('*', '').replace('#', '').strip()
                if prd_title == normalized_title:
                    return prd
            return None
        else:
            # Get all PRDs and filter by normalized title (Supabase doesn't have case-insensitive search easily)
            result = self.supabase.table('prds').select('*').execute()
            if result.data:
                normalized_title = title.strip().lower().replace('*', '').replace('#', '').strip()
                for prd in result.data:
                    prd_title = prd.get("title", "").strip().lower().replace('*', '').replace('#', '').strip()
                    if prd_title == normalized_title:
                        return prd
            return None
    
    async def update_prd(self, prd_id: str, prd_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a PRD."""
        if self.mode == "development":
            if prd_id in self.memory_storage["prds"]:
                self.memory_storage["prds"][prd_id].update(prd_data)
                return self.memory_storage["prds"][prd_id]
            return None
        else:
            result = self.supabase.table('prds').update(prd_data).eq('id', prd_id).execute()
            return result.data[0] if result.data else None
    
    async def delete_prd(self, prd_id: str) -> bool:
        """Delete a PRD."""
        if self.mode == "development":
            if prd_id in self.memory_storage["prds"]:
                del self.memory_storage["prds"][prd_id]
                return True
            return False
        else:
            try:
                # Supabase delete returns the deleted record(s) in result.data
                # If result.data is not empty, the delete succeeded
                result = self.supabase.table('prds').delete().eq('id', prd_id).execute()
                
                # Check if deletion was successful
                # Supabase returns deleted records in result.data
                if result.data and len(result.data) > 0:
                    print(f"✅ Deleted PRD {prd_id}: {result.data[0].get('title', 'N/A')}")
                    return True
                else:
                    # No records deleted - PRD might not exist
                    print(f"⚠️  No PRD found with ID {prd_id} to delete")
                    return False
            except Exception as e:
                print(f"❌ Error deleting PRD {prd_id}: {e}")
                raise
    
    async def clear_all_prds(self) -> bool:
        """Clear all PRDs."""
        if self.mode == "development":
            self.memory_storage["prds"].clear()
            return True
        else:
            result = self.supabase.table('prds').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            return True
    
    def is_connected(self) -> bool:
        """Check if the data manager is connected."""
        if self.mode == "development":
            return True  # In-memory is always "connected"
        else:
            try:
                # Test Supabase connection
                self.supabase.table('agents').select('id').limit(1).execute()
                return True
            except:
                return False


# Global instance - auto-detect mode based on Supabase availability
def _get_data_mode():
    """Auto-detect the appropriate data mode."""
    # Check if DATA_MODE is explicitly set
    explicit_mode = os.getenv("DATA_MODE")
    if explicit_mode:
        return explicit_mode
    
    # Check if Supabase is configured
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        return "production"  # Use Supabase when available
    else:
        return "development"  # Fallback to in-memory

# Initialize data manager with auto-detected mode
data_manager = SimpleDataManager(mode=_get_data_mode())
