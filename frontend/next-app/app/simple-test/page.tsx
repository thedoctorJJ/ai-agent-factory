'use client'

import { useState, useEffect } from 'react'

export default function SimpleTestPage() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    console.log('Simple test: useEffect running')
    
    const fetchData = async () => {
      try {
        console.log('Simple test: Starting fetch')
        const response = await fetch('/api/v1/agents')
        console.log('Simple test: Response received', response.status)
        
        if (response.ok) {
          const result = await response.json()
          console.log('Simple test: Data received', result)
          setData(result)
        } else {
          console.error('Simple test: Error response', response.status)
        }
      } catch (error) {
        console.error('Simple test: Fetch error', error)
      } finally {
        console.log('Simple test: Setting loading to false')
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  console.log('Simple test: Rendering, loading:', loading, 'data:', data)

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <div>
      <h1>Simple Test</h1>
      <p>Loading: {loading ? 'true' : 'false'}</p>
      <p>Data: {data ? JSON.stringify(data) : 'null'}</p>
    </div>
  )
}
