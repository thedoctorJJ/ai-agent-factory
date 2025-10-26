'use client'

import { useState, useEffect } from 'react'

export default function TestPage() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('🔄 Testing API calls...')
        
        const [agentsRes, prdsRes] = await Promise.all([
          fetch('/api/v1/agents'),
          fetch('/api/v1/prds')
        ])
        
        console.log('📡 Responses:', {
          agentsStatus: agentsRes.status,
          prdsStatus: prdsRes.status
        })
        
        const agentsData = await agentsRes.json()
        const prdsData = await prdsRes.json()
        
        setData({
          agents: agentsData,
          prds: prdsData
        })
        
        console.log('✅ Data loaded:', { agents: agentsData, prds: prdsData })
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
        <h1 className="text-2xl font-bold mb-4">API Test Page</h1>
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p>Loading...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">API Test Page</h1>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <strong>Error:</strong> {error}
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">API Test Page</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-2">Agents ({data?.agents?.agents?.length || 0})</h2>
          <pre className="text-xs bg-gray-100 p-2 rounded overflow-auto max-h-64">
            {JSON.stringify(data?.agents, null, 2)}
          </pre>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-2">PRDs ({data?.prds?.prds?.length || 0})</h2>
          <pre className="text-xs bg-gray-100 p-2 rounded overflow-auto max-h-64">
            {JSON.stringify(data?.prds, null, 2)}
          </pre>
        </div>
      </div>
      
      <div className="mt-6">
        <a 
          href="/" 
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Back to Dashboard
        </a>
      </div>
    </div>
  )
}
