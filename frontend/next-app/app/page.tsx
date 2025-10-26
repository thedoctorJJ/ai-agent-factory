'use client'

import { useState, useEffect } from 'react'

interface Agent {
  id: string
  name: string
  description: string
  status: string
  deployment_url?: string
  health_check_url?: string
}

interface PRD {
  id: string
  title: string
  description: string
  status: string
  prd_type?: 'platform' | 'agent'
}

export default function Dashboard() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [prds, setPrds] = useState<PRD[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [mounted, setMounted] = useState(false)

  // Ensure component is mounted on client side
  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!mounted) return

    const fetchData = async () => {
      try {
        console.log('🔄 Starting data fetch...')
        
        const [agentsRes, prdsRes] = await Promise.all([
          fetch('/api/v1/agents'),
          fetch('/api/v1/prds')
        ])
        
        console.log('📡 API responses:', {
          agents: agentsRes.status,
          prds: prdsRes.status
        })
        
        if (agentsRes.ok) {
          const agentsData = await agentsRes.json()
          setAgents(agentsData.agents || [])
          console.log('✅ Agents loaded:', agentsData.agents?.length || 0)
        } else {
          console.error('❌ Failed to fetch agents:', agentsRes.status)
        }
        
        if (prdsRes.ok) {
          const prdsData = await prdsRes.json()
          setPrds(prdsData.prds || [])
          console.log('✅ PRDs loaded:', prdsData.prds?.length || 0)
        } else {
          console.error('❌ Failed to fetch PRDs:', prdsRes.status)
        }
        
      } catch (err) {
        console.error('❌ Error fetching data:', err)
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [mounted])

  // Don't render anything until mounted
  if (!mounted) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Initializing...</p>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading AI Agent Factory...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <strong>Error:</strong> {error}
          </div>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">AI Agent Factory</h1>
          <p className="mt-2 text-gray-600">A repeatable, AI-driven platform for creating modular agents from completed PRDs</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Agents Section */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Agents ({agents.length})</h2>
            </div>
            <div className="p-6">
              {agents.length > 0 ? (
                <div className="space-y-4">
                  {agents.map((agent) => (
                    <div key={agent.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="text-sm font-medium text-gray-900">{agent.name}</h3>
                          <p className="mt-1 text-sm text-gray-500">{agent.description}</p>
                          <div className="mt-2 flex items-center space-x-2">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              agent.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                            }`}>
                              {agent.status}
                            </span>
                          </div>
                        </div>
                        {agent.deployment_url && (
                          <a
                            href={agent.deployment_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 text-sm"
                          >
                            View
                          </a>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">No agents found</p>
              )}
            </div>
          </div>

          {/* PRDs Section */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">PRDs ({prds.length})</h2>
            </div>
            <div className="p-6">
              {prds.length > 0 ? (
                <div className="space-y-4">
                  {prds.map((prd) => (
                    <div key={prd.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="text-sm font-medium text-gray-900">{prd.title}</h3>
                          <p className="mt-1 text-sm text-gray-500">{prd.description}</p>
                          <div className="mt-2 flex items-center space-x-2">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              prd.status === 'completed' ? 'bg-green-100 text-green-800' :
                              prd.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                              prd.status === 'failed' ? 'bg-red-100 text-red-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {prd.status}
                            </span>
                            {prd.prd_type && (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                {prd.prd_type}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">No PRDs found</p>
              )}
            </div>
          </div>
        </div>

        {/* Status Summary */}
        <div className="mt-8 bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">System Status</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{agents.length}</div>
                <div className="text-sm text-gray-500">Total Agents</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{agents.filter(a => a.status === 'active').length}</div>
                <div className="text-sm text-gray-500">Active Agents</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">{prds.length}</div>
                <div className="text-sm text-gray-500">Total PRDs</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}