// Test page to check outbound connectivity from Cloud Run
async function testConnectivity() {
  const tests = []
  
  // Test 1: External service (httpbin.org)
  try {
    const response = await fetch('https://httpbin.org/get', {
      cache: 'no-store'
    })
    tests.push({
      name: 'External Service (httpbin.org)',
      status: response.ok ? 'SUCCESS' : 'FAILED',
      statusCode: response.status
    })
  } catch (error) {
    tests.push({
      name: 'External Service (httpbin.org)',
      status: 'ERROR',
      error: error instanceof Error ? error.message : 'Unknown error'
    })
  }
  
  // Test 2: Backend service (full URL)
  try {
    const response = await fetch('https://ai-agent-factory-backend-fdqqqinvyq-uc.a.run.app/api/v1/health', {
      cache: 'no-store'
    })
    tests.push({
      name: 'Backend Service (full URL)',
      status: response.ok ? 'SUCCESS' : 'FAILED',
      statusCode: response.status
    })
  } catch (error) {
    tests.push({
      name: 'Backend Service (full URL)',
      status: 'ERROR',
      error: error instanceof Error ? error.message : 'Unknown error'
    })
  }
  
  // Test 3: Backend service (relative URL)
  try {
    const response = await fetch('/api/v1/health', {
      cache: 'no-store'
    })
    tests.push({
      name: 'Backend Service (relative URL)',
      status: response.ok ? 'SUCCESS' : 'FAILED',
      statusCode: response.status
    })
  } catch (error) {
    tests.push({
      name: 'Backend Service (relative URL)',
      status: 'ERROR',
      error: error instanceof Error ? error.message : 'Unknown error'
    })
  }
  
  return tests
}

export default async function ConnectivityTestPage() {
  const tests = await testConnectivity()
  
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Connectivity Test Page</h1>
      <div className="space-y-4">
        {tests.map((test, index) => (
          <div key={index} className="border p-4 rounded">
            <h3 className="font-semibold">{test.name}</h3>
            <p className={`font-mono ${test.status === 'SUCCESS' ? 'text-green-600' : 'text-red-600'}`}>
              Status: {test.status}
            </p>
            {test.statusCode && (
              <p className="text-sm text-gray-600">Status Code: {test.statusCode}</p>
            )}
            {test.error && (
              <p className="text-sm text-red-600">Error: {test.error}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
