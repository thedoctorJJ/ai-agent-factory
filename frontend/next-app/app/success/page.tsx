'use client'

import React, { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { CheckCircle, Clock, Loader2, ExternalLink, Github, Activity } from 'lucide-react'

interface Agent {
  id: string
  name: string
  description: string
  status: string
  repository_url?: string
  deployment_url?: string
  health_check_url?: string
  created_at: string
}

export default function SuccessPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [agent, setAgent] = useState<Agent | null>(null)
  const [progress, setProgress] = useState({
    codeGeneration: false,
    githubRepo: false,
    databaseSetup: false,
    cloudDeployment: false
  })
  const [isComplete, setIsComplete] = useState(false)

  const prdId = searchParams.get('prd')
  const taskId = searchParams.get('agent')

  useEffect(() => {
    if (taskId) {
      // Simulate progress updates
      const progressSteps = [
        { key: 'codeGeneration', delay: 2000 },
        { key: 'githubRepo', delay: 5000 },
        { key: 'databaseSetup', delay: 8000 },
        { key: 'cloudDeployment', delay: 12000 }
      ]

      progressSteps.forEach((step) => {
        setTimeout(() => {
          setProgress(prev => ({ ...prev, [step.key]: true }))
        }, step.delay)
      })

      // Check for completed agent after 15 seconds
      setTimeout(async () => {
        try {
          const response = await fetch('/api/v1/agents')
          if (response.ok) {
            const agents = await response.json()
            const latestAgent = agents[agents.length - 1] // Get the most recent agent
            if (latestAgent) {
              setAgent(latestAgent)
              setIsComplete(true)
            }
          }
        } catch (error) {
          console.error('Error fetching agent:', error)
        }
      }, 15000)
    }
  }, [taskId])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'in_progress':
        return <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'in_progress':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🚀 Agent Creation in Progress
          </h1>
          <p className="text-xl text-gray-600">
            Your PRD is being transformed into a fully deployed AI agent
          </p>
        </div>

        {/* Progress Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Loader2 className="h-5 w-5 animate-spin text-blue-500" />
              Creating Your Agent
            </CardTitle>
            <CardDescription>
              Devin AI is automatically building and deploying your agent. This usually takes 2-3 minutes.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {/* Progress Bar */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-medium">Agent Creation Progress</h4>
                  <span className="text-sm text-muted-foreground">
                    {Object.values(progress).filter(Boolean).length}/4 steps completed
                  </span>
                </div>
                
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-blue-600 h-3 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${(Object.values(progress).filter(Boolean).length / 4) * 100}%` }}
                  ></div>
                </div>
              </div>

              {/* Progress Steps */}
              <div className="space-y-4">
                {[
                  { key: 'codeGeneration', label: 'Code Generation', description: 'Devin AI is analyzing your PRD and generating agent code' },
                  { key: 'githubRepo', label: 'GitHub Repository', description: 'Creating repository and pushing initial code' },
                  { key: 'databaseSetup', label: 'Database Setup', description: 'Configuring Supabase database and schemas' },
                  { key: 'cloudDeployment', label: 'Cloud Deployment', description: 'Deploying to Google Cloud Run' }
                ].map((step, index) => {
                  const isCompleted = progress[step.key as keyof typeof progress]
                  const isCurrent = !isCompleted && (index === 0 || progress[Object.keys(progress)[index - 1] as keyof typeof progress])
                  
                  return (
                    <div key={step.key} className="flex items-start space-x-4">
                      <div className="flex-shrink-0 mt-1">
                        {isCompleted ? (
                          <CheckCircle className="h-6 w-6 text-green-500" />
                        ) : isCurrent ? (
                          <Loader2 className="h-6 w-6 text-blue-500 animate-spin" />
                        ) : (
                          <div className="h-6 w-6 rounded-full border-2 border-gray-300"></div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className={`text-sm font-medium ${isCompleted ? 'text-green-700' : isCurrent ? 'text-blue-700' : 'text-gray-500'}`}>
                          {step.label}
                        </p>
                        <p className={`text-xs ${isCompleted ? 'text-green-600' : isCurrent ? 'text-blue-600' : 'text-gray-400'}`}>
                          {step.description}
                        </p>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Agent Result */}
        {isComplete && agent && (
          <Card className="border-green-200 bg-green-50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-800">
                <CheckCircle className="h-5 w-5" />
                Agent Successfully Created!
              </CardTitle>
              <CardDescription className="text-green-700">
                Your AI agent has been deployed and is ready to use.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-green-800">{agent.name}</h3>
                    <p className="text-sm text-green-600">{agent.description}</p>
                  </div>
                  <Badge className={getStatusColor(agent.status)}>
                    {getStatusIcon(agent.status)}
                    <span className="ml-1 capitalize">{agent.status}</span>
                  </Badge>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {agent.repository_url && (
                    <div className="flex items-center gap-2 p-3 bg-white rounded-lg border border-green-200">
                      <Github className="h-4 w-4 text-green-600" />
                      <div>
                        <p className="text-xs text-green-600">Repository</p>
                        <a 
                          href={agent.repository_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-sm font-medium text-green-800 hover:underline"
                        >
                          View on GitHub
                        </a>
                      </div>
                    </div>
                  )}

                  {agent.deployment_url && (
                    <div className="flex items-center gap-2 p-3 bg-white rounded-lg border border-green-200">
                      <ExternalLink className="h-4 w-4 text-green-600" />
                      <div>
                        <p className="text-xs text-green-600">Deployment</p>
                        <a 
                          href={agent.deployment_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-sm font-medium text-green-800 hover:underline"
                        >
                          Live Agent
                        </a>
                      </div>
                    </div>
                  )}

                  {agent.health_check_url && (
                    <div className="flex items-center gap-2 p-3 bg-white rounded-lg border border-green-200">
                      <Activity className="h-4 w-4 text-green-600" />
                      <div>
                        <p className="text-xs text-green-600">Health Check</p>
                        <a 
                          href={agent.health_check_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-sm font-medium text-green-800 hover:underline"
                        >
                          Monitor Status
                        </a>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              <div className="flex gap-3 pt-4">
                <Button 
                  onClick={() => router.push('/')}
                  className="flex-1"
                >
                  Back to Dashboard
                </Button>
                <Button 
                  variant="outline"
                  onClick={() => router.push('/agents')}
                  className="flex-1"
                >
                  View All Agents
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Loading State */}
        {!isComplete && (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Loader2 className="h-12 w-12 text-blue-500 animate-spin mb-4" />
              <h3 className="text-lg font-semibold mb-2">Creating Your Agent...</h3>
              <p className="text-muted-foreground text-center">
                Please wait while Devin AI builds and deploys your agent. 
                You can close this page and check back later.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
