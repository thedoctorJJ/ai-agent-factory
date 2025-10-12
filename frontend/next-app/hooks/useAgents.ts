/**
 * Custom hook for Agent operations.
 */
import { useState, useEffect, useCallback } from 'react'
import { Agent, AgentListResponse, AgentStatus } from '@/types'
import { apiClient } from '@/lib/api'

interface UseAgentsOptions {
  skip?: number
  limit?: number
  status?: AgentStatus
  prdId?: string
  autoFetch?: boolean
}

interface UseAgentsReturn {
  agents: Agent[]
  loading: boolean
  error: string | null
  total: number
  hasNext: boolean
  refetch: () => Promise<void>
  createAgent: (agentData: Partial<Agent>) => Promise<Agent | null>
  updateAgentStatus: (id: string, status: AgentStatus) => Promise<Agent | null>
  deleteAgent: (id: string) => Promise<boolean>
  checkAgentHealth: (id: string) => Promise<boolean>
}

export function useAgents(options: UseAgentsOptions = {}): UseAgentsReturn {
  const {
    skip = 0,
    limit = 100,
    status,
    prdId,
    autoFetch = true
  } = options

  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  const [hasNext, setHasNext] = useState(false)

  const fetchAgents = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await apiClient.getAgents(skip, limit, status, prdId)
      
      if (response.success && response.data) {
        setAgents(response.data.agents)
        setTotal(response.data.total)
        setHasNext(response.data.has_next)
      } else {
        setError(response.error?.message || 'Failed to fetch agents')
        setAgents([])
        setTotal(0)
        setHasNext(false)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setAgents([])
      setTotal(0)
      setHasNext(false)
    } finally {
      setLoading(false)
    }
  }, [skip, limit, status, prdId])

  const createAgent = useCallback(async (agentData: Partial<Agent>): Promise<Agent | null> => {
    try {
      const response = await apiClient.createAgent(agentData)
      
      if (response.success && response.data) {
        setAgents(prev => [response.data!, ...prev])
        setTotal(prev => prev + 1)
        return response.data
      } else {
        setError(response.error?.message || 'Failed to create agent')
        return null
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create agent')
      return null
    }
  }, [])

  const updateAgentStatus = useCallback(async (id: string, status: AgentStatus): Promise<Agent | null> => {
    try {
      const response = await apiClient.updateAgentStatus(id, status)
      
      if (response.success && response.data) {
        setAgents(prev => prev.map(agent => agent.id === id ? response.data! : agent))
        return response.data
      } else {
        setError(response.error?.message || 'Failed to update agent status')
        return null
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update agent status')
      return null
    }
  }, [])

  const deleteAgent = useCallback(async (id: string): Promise<boolean> => {
    try {
      const response = await apiClient.deleteAgent(id)
      
      if (response.success) {
        setAgents(prev => prev.filter(agent => agent.id !== id))
        setTotal(prev => prev - 1)
        return true
      } else {
        setError(response.error?.message || 'Failed to delete agent')
        return false
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete agent')
      return false
    }
  }, [])

  const checkAgentHealth = useCallback(async (id: string): Promise<boolean> => {
    try {
      const response = await apiClient.checkAgentHealth(id)
      
      if (response.success && response.data) {
        // Update the agent's health status in the local state
        setAgents(prev => prev.map(agent => 
          agent.id === id 
            ? { 
                ...agent, 
                health_status: response.data!.status,
                last_health_check: response.data!.last_checked || new Date().toISOString()
              }
            : agent
        ))
        return true
      } else {
        setError(response.error?.message || 'Failed to check agent health')
        return false
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to check agent health')
      return false
    }
  }, [])

  useEffect(() => {
    if (autoFetch) {
      fetchAgents()
    }
  }, [fetchAgents, autoFetch])

  return {
    agents,
    loading,
    error,
    total,
    hasNext,
    refetch: fetchAgents,
    createAgent,
    updateAgentStatus,
    deleteAgent,
    checkAgentHealth
  }
}
