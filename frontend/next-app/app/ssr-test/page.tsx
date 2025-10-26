// This is a server-side rendered page that fetches data on the server
async function getData() {
  const results = []
  
  // Test 1: External service
  try {
    const response = await fetch('https://httpbin.org/get', {
      cache: 'no-store'
    })
    results.push({
      test: 'External Service (httpbin.org)',
      status: response.ok ? 'SUCCESS' : 'FAILED',
      statusCode: response.status
    })
  } catch (error) {
    results.push({
      test: 'External Service (httpbin.org)',
      status: 'ERROR',
      error: error instanceof Error ? error.message : 'Unknown error'
    })
  }
  
  // Test 2: Backend service (full URL)
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://ai-agent-factory-backend-fdqqqinvyq-uc.a.run.app'
    const response = await fetch(`${apiUrl}/api/v1/agents`, {
      cache: 'no-store'
    })
    results.push({
      test: 'Backend Service (full URL)',
      status: response.ok ? 'SUCCESS' : 'FAILED',
      statusCode: response.status,
      data: response.ok ? await response.json() : null
    })
  } catch (error) {
    results.push({
      test: 'Backend Service (full URL)',
      status: 'ERROR',
      error: error instanceof Error ? error.message : 'Unknown error'
    })
  }
  
  // Test 3: Backend service (relative URL)
  try {
    const response = await fetch('/api/v1/agents', {
      cache: 'no-store'
    })
    results.push({
      test: 'Backend Service (relative URL)',
      status: response.ok ? 'SUCCESS' : 'FAILED',
      statusCode: response.status,
      data: response.ok ? await response.json() : null
    })
  } catch (error) {
    results.push({
      test: 'Backend Service (relative URL)',
      status: 'ERROR',
      error: error instanceof Error ? error.message : 'Unknown error'
    })
  }
  
  return results
}

export default async function SSRTestPage() {
  const data = await getData()
  
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">SSR Connectivity Test</h1>
      <div className="space-y-4">
        {data.map((result, index) => (
          <div key={index} className="border p-4 rounded">
            <h3 className="font-semibold">{result.test}</h3>
            <p className={`font-mono ${result.status === 'SUCCESS' ? 'text-green-600' : 'text-red-600'}`}>
              Status: {result.status}
            </p>
            {result.statusCode && (
              <p className="text-sm text-gray-600">Status Code: {result.statusCode}</p>
            )}
            {result.error && (
              <p className="text-sm text-red-600">Error: {result.error}</p>
            )}
            {result.data && (
              <details className="mt-2">
                <summary className="cursor-pointer text-sm text-blue-600">View Data</summary>
                <pre className="bg-gray-100 p-2 rounded mt-2 text-xs overflow-auto">
                  {JSON.stringify(result.data, null, 2)}
                </pre>
              </details>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
