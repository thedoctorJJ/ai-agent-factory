'use client'

import { useState, useEffect } from 'react'

interface Agent {
  id: string
  name: string
  description: string
  status: string
}

interface PRD {
  id: string
  title: string
  description: string
  status: string
}

export default function SimpleDashboard() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [prds, setPrds] = useState<PRD[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('🔄 Fetching data...')
        
        const [agentsRes, prdsRes] = await Promise.all([
          fetch('/api/v1/agents'),
          fetch('/api/v1/prds')
        ])
        
        console.log('📡 Responses:', {
          agents: agentsRes.status,
          prds: prdsRes.status
        })
        
        if (agentsRes.ok) {
          const agentsData = await agentsRes.json()
          setAgents(agentsData.agents || [])
          console.log('✅ Agents loaded:', agentsData.agents?.length || 0)
        }
        
        if (prdsRes.ok) {
          const prdsData = await prdsRes.json()
          setPrds(prdsData.prds || [])
          console.log('✅ PRDs loaded:', prdsData.prds?.length || 0)
        }
        
      } catch (err) {
        console.error('❌ Error:', err)
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Simple Dashboard</h1>
        <div className="flex items-center space-x-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
          <span>Loading data...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Simple Dashboard</h1>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <strong>Error:</strong> {error}
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Simple Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Agents ({agents.length})</h2>
          {agents.length > 0 ? (
            <ul className="space-y-2">
              {agents.map((agent) => (
                <li key={agent.id} className="border p-2 rounded">
                  <div className="font-medium">{agent.name}</div>
                  <div className="text-sm text-gray-600">{agent.description}</div>
                  <div className="text-xs text-blue-600">Status: {agent.status}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">No agents found</p>
          )}
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">PRDs ({prds.length})</h2>
          {prds.length > 0 ? (
            <ul className="space-y-2">
              {prds.map((prd) => (
                <li key={prd.id} className="border p-2 rounded">
                  <div className="font-medium">{prd.title}</div>
                  <div className="text-sm text-gray-600">{prd.description}</div>
                  <div className="text-xs text-blue-600">Status: {prd.status}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">No PRDs found</p>
          )}
        </div>
      </div>
    </div>
  )
}
