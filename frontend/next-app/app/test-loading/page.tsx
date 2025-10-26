'use client'

import { useState, useEffect } from 'react'

export default function TestLoadingPage() {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    console.log('🔄 Test page useEffect running...')
    
    const fetchData = async () => {
      try {
        console.log('🌐 Fetching from /api/v1/health...')
        const response = await fetch('/api/v1/health')
        console.log('📡 Response status:', response.status)
        
        if (response.ok) {
          const result = await response.json()
          console.log('✅ Data received:', result)
          setData(result)
        } else {
          console.error('❌ Response not ok:', response.status)
          setError(`HTTP ${response.status}`)
        }
      } catch (err) {
        console.error('❌ Fetch error:', err)
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        console.log('🏁 Setting loading to false')
        setLoading(false)
      }
    }

    // Add a small delay to see the loading state
    setTimeout(fetchData, 1000)
  }, [])

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Test Loading Page</h1>
        <div className="flex items-center space-x-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
          <span>Loading...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Test Loading Page</h1>
      {error ? (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <strong>Error:</strong> {error}
        </div>
      ) : (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          <strong>Success!</strong> Data loaded successfully.
          <pre className="mt-2 text-sm bg-white p-2 rounded overflow-auto">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}
