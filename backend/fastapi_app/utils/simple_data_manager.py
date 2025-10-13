"""
Simplified data manager with Supabase + In-Memory storage.
No more complex fallback chains - just clean, predictable storage.
"""
import os
from typing import Dict, Any, List, Optional
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
        """Initialize Supabase client."""
        try:
            supabase_url = config.supabase_url
            supabase_key = config.supabase_key
            
            if not supabase_url or not supabase_key:
                raise ValueError("Supabase URL and key are required for production mode")
            
            self.supabase = create_client(supabase_url, supabase_key)
            print(f"✅ Connected to Supabase (mode: {self.mode})")
        except Exception as e:
            print(f"❌ Failed to connect to Supabase: {e}")
            raise e
    
    # Agent Operations
    async def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an agent."""
        if self.mode == "development":
            agent_id = agent_data.get("id", f"agent_{len(self.memory_storage['agents']) + 1}")
            self.memory_storage["agents"][agent_id] = agent_data
            return agent_data
        else:
            result = self.supabase.table('agents').insert(agent_data).execute()
            return result.data[0] if result.data else None
    
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
    
    async def update_agent(self, agent_id: str, agent_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an agent."""
        if self.mode == "development":
            if agent_id in self.memory_storage["agents"]:
                self.memory_storage["agents"][agent_id].update(agent_data)
                return self.memory_storage["agents"][agent_id]
            return None
        else:
            result = self.supabase.table('agents').update(agent_data).eq('id', agent_id).execute()
            return result.data[0] if result.data else None
    
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
            result = self.supabase.table('prds').delete().eq('id', prd_id).execute()
            return True
    
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


# Global instance - defaults to development mode
data_manager = SimpleDataManager(mode=os.getenv("DATA_MODE", "development"))
