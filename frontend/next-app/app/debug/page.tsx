'use client'

import { useState, useEffect } from 'react'

export default function DebugPage() {
  const [agents, setAgents] = useState([])
  const [prds, setPrds] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('🔄 Debug: Starting data fetch...')
        
        const [agentsRes, prdsRes] = await Promise.all([
          fetch('/api/v1/agents'),
          fetch('/api/v1/prds')
        ])
        
        console.log('📡 Debug: API responses:', {
          agentsStatus: agentsRes.status,
          prdsStatus: prdsRes.status
        })
        
        if (agentsRes.ok) {
          const agentsData = await agentsRes.json()
          console.log('🤖 Debug: Agents data:', agentsData)
          setAgents(agentsData.agents || [])
        } else {
          console.error('❌ Debug: Failed to fetch agents:', agentsRes.status)
          setError(`Failed to fetch agents: ${agentsRes.status}`)
        }
        
        if (prdsRes.ok) {
          const prdsData = await prdsRes.json()
          console.log('📄 Debug: PRDs data:', prdsData)
          setPrds(prdsData.prds || [])
        } else {
          console.error('❌ Debug: Failed to fetch PRDs:', prdsRes.status)
          setError(`Failed to fetch PRDs: ${prdsRes.status}`)
        }
      } catch (error) {
        console.error('❌ Debug: Error fetching data:', error)
        setError(`Error: ${error.message}`)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Debug Page - Loading...</h1>
        <p>Fetching data...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Debug Page - Error</h1>
        <p className="text-red-600">{error}</p>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Debug Page</h1>
      
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Agents ({agents.length})</h2>
        <pre className="bg-gray-100 p-4 rounded overflow-auto max-h-96">
          {JSON.stringify(agents, null, 2)}
        </pre>
      </div>
      
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">PRDs ({prds.length})</h2>
        <pre className="bg-gray-100 p-4 rounded overflow-auto max-h-96">
          {JSON.stringify(prds, null, 2)}
        </pre>
      </div>
      
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Agents by PRD</h2>
        <pre className="bg-gray-100 p-4 rounded overflow-auto max-h-96">
          {JSON.stringify(
            agents.reduce((acc, agent) => {
              const prdId = agent.prd_id || 'standalone'
              if (!acc[prdId]) acc[prdId] = []
              acc[prdId].push(agent.name)
              return acc
            }, {}),
            null,
            2
          )}
        </pre>
      </div>
    </div>
  )
}
