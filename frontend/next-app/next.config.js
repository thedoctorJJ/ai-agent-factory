/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  trailingSlash: false,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  async rewrites() {
    // Get the API URL from environment variable or use production default
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 
                   process.env.NODE_ENV === 'production' 
                     ? 'https://ai-agent-factory-backend-fdqqqinvyq-uc.a.run.app'
                     : 'http://localhost:8000'
    
    console.log('🔧 Next.js rewrites config - API URL:', apiUrl)
    console.log('🔧 NODE_ENV:', process.env.NODE_ENV)
    console.log('🔧 Environment variables available:', Object.keys(process.env).filter(key => key.includes('API')))
    
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ]
  },
  // Add experimental features for better API handling
  experimental: {
    // serverComponentsExternalPackages is deprecated in Next.js 15
  },
  // Use the new serverExternalPackages instead
  serverExternalPackages: [],
  // Ensure proper headers for API proxy
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          {
            key: 'Access-Control-Allow-Origin',
            value: '*',
          },
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET, POST, PUT, DELETE, OPTIONS',
          },
          {
            key: 'Access-Control-Allow-Headers',
            value: 'Content-Type, Authorization',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig
