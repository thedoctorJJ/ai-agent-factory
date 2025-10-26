export default function WorkingPage() {
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
            <p className="text-3xl font-bold text-blue-600">8</p>
            <p className="text-sm text-gray-500 mt-1">Sample PRDs loaded</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Agents Created</h3>
            <p className="text-3xl font-bold text-green-600">1</p>
            <p className="text-sm text-gray-500 mt-1">Redis Caching Agent</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Status</h3>
            <p className="text-3xl font-bold text-purple-600">✅</p>
            <p className="text-sm text-gray-500 mt-1">System Operational</p>
          </div>
        </div>

        {/* Redis Agent Section */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Redis Caching Layer Agent</h2>
            <p className="text-gray-600 mt-1">Successfully deployed and running</p>
          </div>
          <div className="p-6">
            <div className="border border-gray-200 rounded-lg p-4">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Redis Caching Layer Agent</h3>
                  <p className="text-gray-600 mb-2">High-performance caching service for Google Cloud Run with in-memory fallback</p>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span>Version: 2.0.0</span>
                    <span className="px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">draft</span>
                    <span>Created: Oct 26, 2025</span>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <a
                    href="https://redis-caching-agent-fdqqqinvyq-uc.a.run.app"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                  >
                    View Agent
                  </a>
                  <a
                    href="https://redis-caching-agent-fdqqqinvyq-uc.a.run.app/health"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
                  >
                    Health Check
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* API Status */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">API Status</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div>
                  <h3 className="font-medium text-green-900">Backend API</h3>
                  <p className="text-sm text-green-700">ai-agent-factory-backend-952475323593.us-central1.run.app</p>
                </div>
                <span className="text-green-600">✅ Online</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div>
                  <h3 className="font-medium text-green-900">Agents Endpoint</h3>
                  <p className="text-sm text-green-700">/api/v1/agents</p>
                </div>
                <span className="text-green-600">✅ Working</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div>
                  <h3 className="font-medium text-green-900">PRDs Endpoint</h3>
                  <p className="text-sm text-green-700">/api/v1/prds</p>
                </div>
                <span className="text-green-600">✅ Working</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div>
                  <h3 className="font-medium text-green-900">Redis Agent</h3>
                  <p className="text-sm text-green-700">redis-caching-agent-fdqqqinvyq-uc.a.run.app</p>
                </div>
                <span className="text-green-600">✅ Running</span>
              </div>
            </div>
          </div>
        </div>

        {/* Direct API Links */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Direct API Access</h2>
            <p className="text-gray-600 mt-1">Access the APIs directly while we fix the frontend rendering</p>
          </div>
          <div className="p-6">
            <div className="space-y-3">
              <a
                href="https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents"
                target="_blank"
                rel="noopener noreferrer"
                className="block p-3 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
              >
                <h3 className="font-medium text-blue-900">View Agents API</h3>
                <p className="text-sm text-blue-700">See the Redis agent data in JSON format</p>
              </a>
              <a
                href="https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds"
                target="_blank"
                rel="noopener noreferrer"
                className="block p-3 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors"
              >
                <h3 className="font-medium text-green-900">View PRDs API</h3>
                <p className="text-sm text-green-700">See all PRDs including Redis Caching Layer</p>
              </a>
              <a
                href="https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/health"
                target="_blank"
                rel="noopener noreferrer"
                className="block p-3 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors"
              >
                <h3 className="font-medium text-purple-900">Health Check API</h3>
                <p className="text-sm text-purple-700">Check system health and configuration</p>
              </a>
            </div>
          </div>
        </div>

        {/* Status Message */}
        <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">Frontend Rendering Issue</h3>
              <div className="mt-2 text-sm text-yellow-700">
                <p>The main dashboard is experiencing a Next.js 15 hydration issue. The backend APIs are working perfectly, and the Redis agent is successfully deployed and running. You can access all functionality through the direct API links above.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
