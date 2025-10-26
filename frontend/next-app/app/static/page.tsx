export default function StaticPage() {
  return (
    <html>
      <head>
        <title>Static Test Page</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body style={{ fontFamily: 'Arial, sans-serif', padding: '20px', margin: 0 }}>
        <h1>Static Test Page</h1>
        <p>This is a completely static page with no client-side JavaScript.</p>
        <p>If you can see this, the routing is working!</p>
        <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0', borderRadius: '5px' }}>
          <h2>System Status</h2>
          <p>✅ Backend API: Working</p>
          <p>✅ Redis Agent: Running</p>
          <p>✅ Database: Connected</p>
          <p>✅ Frontend: Serving</p>
        </div>
        <div style={{ marginTop: '20px' }}>
          <h3>Direct API Links:</h3>
          <ul>
            <li><a href="/api/v1/agents" target="_blank">View Agents API</a></li>
            <li><a href="/api/v1/prds" target="_blank">View PRDs API</a></li>
            <li><a href="/api/v1/health" target="_blank">Health Check API</a></li>
          </ul>
        </div>
      </body>
    </html>
  )
}
