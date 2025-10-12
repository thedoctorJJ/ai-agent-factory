'use client'

import { useState, useEffect, useMemo } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Plus, Bot, FileText, Activity, Github, Download, Eye, BarChart3, Upload, ChevronDown, ChevronUp, CheckCircle, Trash2 } from 'lucide-react'
import DevinIntegration from '@/components/DevinIntegration'
import PRDCreationForm from '@/components/PRDCreationForm'

interface Agent {
  id: string
  name: string
  description: string
  purpose: string
  version: string
  status: string
  repository_url?: string
  deployment_url?: string
  health_check_url?: string
  prd_id?: string
  devin_task_id?: string
  capabilities: string[]
  configuration: Record<string, any>
  last_health_check?: string
  health_status?: string
  created_at: string
  updated_at: string
}

interface PRD {
  id: string
  title: string
  description: string
  prd_type?: 'platform' | 'agent'
  status: string
  created_at: string
  requirements?: string[]
}

export default function Dashboard() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [prds, setPrds] = useState<PRD[]>([])
  const [loading, setLoading] = useState(true)
  const [prdTypeFilter, setPrdTypeFilter] = useState<'all' | 'platform' | 'agent'>('all')
  const [prdStatusFilter, setPrdStatusFilter] = useState<string>('all')
  const [showPRDForm, setShowPRDForm] = useState(false)
  const [showQueueSection, setShowQueueSection] = useState(false)
  const [showProcessedSection, setShowProcessedSection] = useState(false)
  const [showAgentsSection, setShowAgentsSection] = useState(false)

  const activeAgentsCount = useMemo(() => 
    agents.filter(a => a.status === 'active').length,
    [agents]
  )
  
  const completedPrdsCount = useMemo(() => 
    prds.filter(p => p.status === 'completed').length,
    [prds]
  )

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [agentsRes, prdsRes] = await Promise.all([
        fetch('/api/v1/agents'),
        fetch('/api/v1/prds')
      ])
      
      if (agentsRes.ok) {
        const agentsData = await agentsRes.json()
        setAgents(agentsData)
      } else {
        console.error('Failed to fetch agents:', agentsRes.status)
        setAgents([]) // Clear agents if fetch fails
      }
      
      if (prdsRes.ok) {
        const prdsData = await prdsRes.json()
        setPrds(prdsData)
      } else {
        console.error('Failed to fetch PRDs:', prdsRes.status)
        setPrds([]) // Clear PRDs if fetch fails
      }
    } catch (error) {
      console.error('Error fetching data:', error)
      // Clear data on error to prevent stale state
      setAgents([])
      setPrds([])
    } finally {
      setLoading(false)
    }
  }

  const handlePRDSuccess = () => {
    fetchData() // Refresh the data to show the new PRD
  }

  const downloadPRDMarkdown = async (prdId: string, title: string) => {
    try {
      const response = await fetch(`/api/v1/prds/${prdId}/markdown/download`)
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `PRD_${title.replace(/\s+/g, '_')}_${prdId.slice(0, 8)}.md`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }
    } catch (error) {
      console.error('Error downloading PRD markdown:', error)
    }
  }

  const deleteAgent = async (agentId: string) => {
    if (confirm('Are you sure you want to delete this agent? This action cannot be undone.')) {
      try {
        const response = await fetch(`/api/v1/agents/${agentId}`, {
          method: 'DELETE',
        })
        if (response.ok) {
          // Remove the agent from the local state
          setAgents(agents.filter(agent => agent.id !== agentId))
        } else {
          const errorData = await response.json().catch(() => ({}))
          const errorMessage = errorData.detail || `Failed to delete agent (${response.status})`
          alert(`Error: ${errorMessage}`)
          console.error('Failed to delete agent:', errorMessage)
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error'
        alert(`Error deleting agent: ${errorMessage}`)
        console.error('Error deleting agent:', error)
      }
    }
  }

  const viewPRDMarkdown = async (prdId: string) => {
    try {
      const response = await fetch(`/api/v1/prds/${prdId}/markdown`)
      if (response.ok) {
        const data = await response.json()
        // Open in new window/tab for viewing
        const newWindow = window.open('', '_blank')
        if (newWindow) {
          newWindow.document.write(`
            <html>
              <head>
                <title>${data.filename}</title>
                <style>
                  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
                  pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
                  code { background: #f5f5f5; padding: 2px 4px; border-radius: 3px; }
                  h1, h2, h3 { color: #333; }
                  ul, ol { padding-left: 20px; }
                  blockquote { border-left: 4px solid #ddd; margin: 0; padding-left: 20px; color: #666; }
                </style>
              </head>
              <body>
                <pre>${data.markdown}</pre>
              </body>
            </html>
          `)
        }
      }
    } catch (error) {
      console.error('Error viewing PRD markdown:', error)
    }
  }

  const findPRDForAgent = (agent: Agent) => {
    if (agent.prd_id) {
      return prds.find(prd => prd.id === agent.prd_id)
    }
    return null
  }

  const generateAgentDescription = (prd: PRD) => {
    // Create a concise description of what the agent will do
    if (prd.description && prd.description.length > 0) {
      // Use the first sentence or first 100 characters of description
      const firstSentence = prd.description.split('.')[0]
      if (firstSentence.length <= 100) {
        return firstSentence
      } else {
        return prd.description.substring(0, 100) + '...'
      }
    }
    
    // Fallback: generate from requirements
    if (prd.requirements && prd.requirements.length > 0) {
      const firstReq = prd.requirements[0]
      return `Agent that ${firstReq.toLowerCase()}${firstReq.endsWith('.') ? '' : '.'}`
    }
    
    // Final fallback
    return `AI agent created from ${prd.title}`
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      // Agent statuses
      case 'active':
      case 'created':
        return 'bg-green-100 text-green-800'
      case 'pending':
      case 'submitted':
        return 'bg-yellow-100 text-yellow-800'
      case 'error':
      case 'failed':
        return 'bg-red-100 text-red-800'
      
      // PRD statuses (simplified repository system)
      case 'queue':
        return 'bg-yellow-100 text-yellow-800'
      case 'processed':
        return 'bg-green-100 text-green-800'
      
      // Legacy statuses (for backward compatibility)
      case 'backlog':
        return 'bg-gray-100 text-gray-800'
      case 'planned':
        return 'bg-blue-100 text-blue-800'
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800'
      case 'review':
        return 'bg-purple-100 text-purple-800'
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'cancelled':
        return 'bg-red-100 text-red-800'
      case 'ready_for_agent_creation':
        return 'bg-emerald-100 text-emerald-800'
      
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <Activity className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p>Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">AI Agent Factory</h1>
        <p className="text-muted-foreground mt-2">
          A repeatable, AI-driven platform for creating modular agents from completed, formatted PRDs
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total PRDs submitted</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{prds.length}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">PRDs Processed</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {prds.filter(p => p.status === 'processed').length}
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Agents Created</CardTitle>
            <Bot className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {agents.length}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="create" className="space-y-4">
        <TabsList>
          <TabsTrigger value="create">Submit PRD</TabsTrigger>
          <TabsTrigger value="prds">PRDs</TabsTrigger>
          <TabsTrigger value="devin">Create Agent</TabsTrigger>
          <TabsTrigger value="agents">Agents</TabsTrigger>
        </TabsList>

        <TabsContent value="create" className="space-y-6">
          <div className="text-center space-y-4">
            <h2 className="text-3xl font-bold">Submit Your PRD</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Upload your completed PRD and watch it automatically transform into a deployed AI agent. 
              Our streamlined workflow handles everything from parsing to deployment.
            </p>
          </div>

          {/* Streamlined Workflow */}
          <div className="max-w-4xl mx-auto">
            <Card className="border-2 border-green-200 hover:border-green-300 transition-all duration-200 shadow-lg">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-20 h-20 bg-gradient-to-br from-green-100 to-green-200 rounded-full flex items-center justify-center mb-4">
                  <Bot className="h-10 w-10 text-green-600" />
                </div>
                <CardTitle className="text-2xl text-green-800">Automated PRD-to-Agent Pipeline</CardTitle>
                <CardDescription className="text-base text-green-700">
                  One upload, fully automated agent creation and deployment
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Streamlined Process */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-800 mb-3 flex items-center gap-2">
                    <span className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm">1</span>
                    PRDs
                  </h4>
                   <p className="text-blue-700 text-sm mb-3">
                     Upload your completed PRD file or paste the content. Your PRD will be added to the queue to create an AI agent.
                   </p>
                  <Button 
                    onClick={() => window.location.href = '/upload'}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                    size="lg"
                  >
                    <Upload className="h-5 w-5 mr-2" />
                    Upload PRD
                  </Button>
                </div>

                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-3 flex items-center gap-2">
                    <span className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-sm">2</span>
                    Create Agent
                  </h4>
                  <p className="text-green-700 text-sm mb-3">
                    Select a PRD and let Devin AI automatically create your agent, set up the repository, and deploy it to the cloud. 
                    Watch the progress in real-time with our progress bar.
                  </p>
                </div>

                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                  <h4 className="font-semibold text-purple-800 mb-3 flex items-center gap-2">
                    <span className="w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm">3</span>
                    Agents
                  </h4>
                  <p className="text-purple-700 text-sm">
                    Your agent is deployed and ready to use! View it in the Agents tab with full traceability back to the original PRD.
                  </p>
                </div>

                {/* Key Benefits */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Zero-Click Deployment</p>
                      <p className="text-xs text-muted-foreground">Fully automated from PRD to live agent</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Real-time Progress</p>
                      <p className="text-xs text-muted-foreground">Watch agent creation with live updates</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Full Traceability</p>
                      <p className="text-xs text-muted-foreground">PRD-to-Agent connection maintained</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Repository Management</p>
                      <p className="text-xs text-muted-foreground">Organized PRD queue and processed agents</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

        </TabsContent>

        <TabsContent value="agents" className="space-y-6">
          <div className="space-y-2">
            <Button
              variant="ghost"
              onClick={() => setShowAgentsSection(!showAgentsSection)}
              className="w-full justify-between p-4 h-auto bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-lg transition-colors"
            >
              <div className="flex items-center gap-2">
                <h2 className="text-2xl font-semibold text-blue-800">AI Agents</h2>
                <Badge variant="secondary" className="bg-blue-200 text-blue-800">
                  {agents.length}
                </Badge>
              </div>
              {showAgentsSection ? <ChevronUp className="h-4 w-4 text-blue-600" /> : <ChevronDown className="h-4 w-4 text-blue-600" />}
            </Button>
            <p className="text-muted-foreground">
              Deployed AI agents created from processed PRDs. Each agent is automatically generated and deployed from your PRD specifications.
            </p>
          </div>
          
          
          {showAgentsSection && (
            <div className="grid gap-4">
            {agents.length === 0 ? (
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-8">
                  <Bot className="h-12 w-12 text-muted-foreground mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No agents yet</h3>
                  <p className="text-muted-foreground text-center mb-4">
                    Create your first AI agent by submitting a PRD
                  </p>
                  <Button>Create First Agent</Button>
                </CardContent>
              </Card>
            ) : (
              agents.map((agent) => (
                <Card key={agent.id} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <CardTitle className="flex items-center gap-2 mb-2">
                          {agent.name}
                          <Badge className={getStatusColor(agent.status)}>
                            {agent.status}
                          </Badge>
                          <Badge variant="outline" className="text-xs">
                            v{agent.version}
                          </Badge>
                        </CardTitle>
                        <CardDescription className="mb-2">{agent.description}</CardDescription>
                        
                        {/* Show PRD connection */}
                        {findPRDForAgent(agent) && (
                          <div className="mb-2 p-2 bg-green-50 rounded-lg border border-green-200">
                            <p className="text-xs font-medium text-green-800 mb-1">📄 Created from PRD:</p>
                            <p className="text-sm text-green-700">{findPRDForAgent(agent)?.title}</p>
                          </div>
                        )}
                        
                        <div className="flex items-center gap-2">
                          <Badge 
                            variant={agent.health_status === 'healthy' ? 'default' : 
                                    agent.health_status === 'unhealthy' ? 'destructive' : 'secondary'}
                            className="text-xs"
                          >
                            {agent.health_status || 'unknown'}
                          </Badge>
                          {agent.last_health_check && (
                            <span className="text-xs text-muted-foreground">
                              Last check: {new Date(agent.last_health_check).toLocaleTimeString()}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                      
                      <div className="flex gap-2 mb-3">
                      {agent.repository_url && (
                        <Button variant="outline" size="sm" asChild>
                          <a href={agent.repository_url} target="_blank" rel="noopener noreferrer">
                            <Github className="h-4 w-4 mr-2" />
                            Repository
                          </a>
                        </Button>
                      )}
                      {agent.deployment_url && (
                        <Button variant="outline" size="sm" asChild>
                          <a href={agent.deployment_url} target="_blank" rel="noopener noreferrer">
                            <Activity className="h-4 w-4 mr-2" />
                            Deploy
                          </a>
                        </Button>
                      )}
                    </div>
                    
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        <Eye className="h-4 w-4 mr-2" />
                        View Details
                      </Button>
                      {findPRDForAgent(agent) && (
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => window.location.href = `/prds/${agent.prd_id}`}
                        >
                          <FileText className="h-4 w-4 mr-2" />
                          View PRD
                        </Button>
                      )}
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => deleteAgent(agent.id)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="h-4 w-4 mr-2" />
                        Delete
                      </Button>
                      <Button variant="outline" size="sm">
                        <BarChart3 className="h-4 w-4 mr-2" />
                        Metrics
                      </Button>
                    </div>
                    
                    <p className="text-xs text-muted-foreground mt-2">
                      Created: {new Date(agent.created_at).toLocaleDateString()}
                    </p>
                  </CardContent>
                </Card>
              ))
            )}
            </div>
          )}
        </TabsContent>

        <TabsContent value="prds" className="space-y-6">
          <div className="space-y-2">
            <h2 className="text-2xl font-semibold">PRD Repository</h2>
            <p className="text-muted-foreground">
              Manage your Product Requirements Documents. PRDs in "Queue" are waiting to be processed into agents. 
              "Processed" PRDs have been converted into deployed AI agents.
            </p>
          </div>
          
          {/* In Queue Section */}
          <div className="space-y-4">
            <Button
              variant="ghost"
              onClick={() => setShowQueueSection(!showQueueSection)}
              className="w-full justify-between p-4 h-auto bg-yellow-50 hover:bg-yellow-100 border border-yellow-200 rounded-lg transition-colors"
            >
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-semibold text-yellow-800">In Queue</h3>
                <Badge variant="secondary" className="bg-yellow-200 text-yellow-800">
                  {prds.filter(p => p.status === 'queue').length}
                </Badge>
              </div>
              {showQueueSection ? <ChevronUp className="h-4 w-4 text-yellow-600" /> : <ChevronDown className="h-4 w-4 text-yellow-600" />}
            </Button>
            {showQueueSection && (
              <div className="grid gap-4">
              {prds.filter(p => p.status === 'queue').length > 0 ? (
                prds.filter(p => p.status === 'queue').map((prd) => (
                  <Card key={prd.id} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="space-y-1">
                          <CardTitle className="text-lg">{prd.title}</CardTitle>
                          <div className="space-y-2">
                            <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                              <p className="text-sm font-medium text-blue-800 mb-1">🤖 Agent Description:</p>
                              <p className="text-sm text-blue-700">{generateAgentDescription(prd)}</p>
                            </div>
                            <div className="bg-yellow-50 p-2 rounded-lg border border-yellow-200">
                              <p className="text-xs text-yellow-700">⏳ Waiting to be processed into an AI agent</p>
                            </div>
                            {prd.description && prd.description !== generateAgentDescription(prd) && (
                              <CardDescription className="text-xs text-muted-foreground">
                                Full PRD: {prd.description}
                              </CardDescription>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge className="bg-yellow-100 text-yellow-800">⏳ In Queue</Badge>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => window.location.href = `/prds/${prd.id}`}
                          >
                            <Eye className="h-4 w-4 mr-2" />
                            View
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                  </Card>
                ))
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <p>No PRDs in queue</p>
                </div>
              )}
              </div>
            )}
          </div>

          {/* Processed Section */}
          <div className="space-y-4">
            <Button
              variant="ghost"
              onClick={() => setShowProcessedSection(!showProcessedSection)}
              className="w-full justify-between p-4 h-auto bg-green-50 hover:bg-green-100 border border-green-200 rounded-lg transition-colors"
            >
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-semibold text-green-800">Processed</h3>
                <Badge variant="secondary" className="bg-green-200 text-green-800">
                  {prds.filter(p => p.status === 'processed').length}
                </Badge>
              </div>
              {showProcessedSection ? <ChevronUp className="h-4 w-4 text-green-600" /> : <ChevronDown className="h-4 w-4 text-green-600" />}
            </Button>
            {showProcessedSection && (
              <div className="grid gap-4">
              {prds.filter(p => p.status === 'processed').length > 0 ? (
                prds.filter(p => p.status === 'processed').map((prd) => (
                  <Card key={prd.id} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="space-y-1">
                          <CardTitle className="text-lg">{prd.title}</CardTitle>
                          <div className="space-y-2">
                            <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                              <p className="text-sm font-medium text-blue-800 mb-1">🤖 Agent Description:</p>
                              <p className="text-sm text-blue-700">{generateAgentDescription(prd)}</p>
                            </div>
                            <div className="bg-green-50 p-2 rounded-lg border border-green-200">
                              <p className="text-xs text-green-700">✅ Successfully converted into a deployed AI agent</p>
                            </div>
                            {prd.description && prd.description !== generateAgentDescription(prd) && (
                              <CardDescription className="text-xs text-muted-foreground">
                                Full PRD: {prd.description}
                              </CardDescription>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge className="bg-green-100 text-green-800">✅ Processed</Badge>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => window.location.href = `/prds/${prd.id}`}
                          >
                            <Eye className="h-4 w-4 mr-2" />
                            View
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                  </Card>
                ))
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <p>No processed PRDs</p>
                </div>
              )}
              </div>
            )}
          </div>
        </TabsContent>

        <TabsContent value="devin" className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-semibold">Create An Agent</h2>
            <Badge variant="outline">API Integration</Badge>
          </div>
          <DevinIntegration 
            prds={prds}
          />
        </TabsContent>
      </Tabs>

      {/* PRD Creation Form Modal */}
      {showPRDForm && (
        <PRDCreationForm
          onClose={() => setShowPRDForm(false)}
          onSuccess={handlePRDSuccess}
        />
      )}


    </div>
  )
}
