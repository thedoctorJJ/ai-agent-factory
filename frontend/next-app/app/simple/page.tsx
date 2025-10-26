'use client'

import { useState, useEffect } from 'react'

interface Agent {
  id: string
  name: string
  description: string
  purpose: string
  version: string
  status: string
  deployment_url?: string
  health_check_url?: string
  created_at: string
}

interface PRD {
  id: string
  title: string
  description: string
  status: string
  created_at: string
}

export default function SimplePage() {
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
          agentsStatus: agentsRes.status,
          prdsStatus: prdsRes.status
        })
        
        if (agentsRes.ok && prdsRes.ok) {
          const agentsData = await agentsRes.json()
          const prdsData = await prdsRes.json()
          
          setAgents(agentsData.agents || [])
          setPrds(prdsData.prds || [])
          
          console.log('✅ Data loaded successfully')
        } else {
          throw new Error(`API Error: Agents ${agentsRes.status}, PRDs ${prdsRes.status}`)
        }
      } catch (err) {
        console.error('❌ Error:', err)
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    // Add a small delay to ensure proper hydration
    const timer = setTimeout(fetchData, 100)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">AI Agent Factory</h1>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-4">Error</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Agent Factory</h1>
          <p className="text-gray-600">A repeatable, AI-driven platform for creating modular agents from completed PRDs</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Total PRDs</h3>
            <p className="text-3xl font-bold text-blue-600">{prds.length}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Agents Created</h3>
            <p className="text-3xl font-bold text-green-600">{agents.length}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Active Agents</h3>
            <p className="text-3xl font-bold text-purple-600">
              {agents.filter(a => a.status === 'active').length}
            </p>
          </div>
        </div>

        {/* Agents Section */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">AI Agents ({agents.length})</h2>
          </div>
          <div className="p-6">
            {agents.length === 0 ? (
              <div className="text-center py-8">
                <div className="text-gray-400 mb-4">
                  <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No agents yet</h3>
                <p className="text-gray-500">Create your first AI agent by submitting a PRD</p>
              </div>
            ) : (
              <div className="space-y-4">
                {agents.map((agent) => (
                  <div key={agent.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">{agent.name}</h3>
                        <p className="text-gray-600 mb-2">{agent.description}</p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <span>Version: {agent.version}</span>
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            agent.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                          }`}>
                            {agent.status}
                          </span>
                          <span>Created: {new Date(agent.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        {agent.deployment_url && (
                          <a
                            href={agent.deployment_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                          >
                            View
                          </a>
                        )}
                        {agent.health_check_url && (
                          <a
                            href={agent.health_check_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
                          >
                            Health
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* PRDs Section */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">PRDs ({prds.length})</h2>
          </div>
          <div className="p-6">
            {prds.length === 0 ? (
              <div className="text-center py-8">
                <div className="text-gray-400 mb-4">
                  <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No PRDs yet</h3>
                <p className="text-gray-500">Upload your first PRD to get started</p>
              </div>
            ) : (
              <div className="space-y-4">
                {prds.map((prd) => (
                  <div key={prd.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{prd.title}</h3>
                    <p className="text-gray-600 mb-2">{prd.description}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        prd.status === 'completed' ? 'bg-green-100 text-green-800' : 
                        prd.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' : 
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {prd.status}
                      </span>
                      <span>Created: {new Date(prd.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <div className="mt-8 text-center">
          <a 
            href="/" 
            className="bg-gray-600 text-white px-6 py-2 rounded hover:bg-gray-700 mr-4"
          >
            Back to Full Dashboard
          </a>
          <a 
            href="/api/v1/agents" 
            target="_blank"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            View API Directly
          </a>
        </div>
      </div>
    </div>
  )
}
