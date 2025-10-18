// This is a server-side rendered page that fetches data on the server
async function getData() {
  try {
    const response = await fetch('http://localhost:8000/api/v1/agents', {
      cache: 'no-store'
    })
    
    if (response.ok) {
      return await response.json()
    } else {
      return { error: `HTTP ${response.status}` }
    }
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Unknown error' }
  }
}

export default async function SSRTestPage() {
  const data = await getData()
  
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">SSR Test Page</h1>
      <pre className="bg-gray-100 p-4 rounded overflow-auto">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  )
}
