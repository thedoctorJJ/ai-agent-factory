'use client'

import { useState, useEffect, useMemo } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Plus, Bot, FileText, Activity, Github, Download, Eye, BarChart3, Upload, ChevronDown, CheckCircle } from 'lucide-react'
import DevinIntegration from '@/components/DevinIntegration'
import RoadmapDashboard from '@/components/RoadmapDashboard'
import PRDCreationForm from '@/components/PRDCreationForm'
import MarkdownPRDImporter from '@/components/MarkdownPRDImporter'
import PRDChatbot from '@/components/PRDChatbot'

interface Agent {
  id: string
  name: string
  description: string
  purpose: string
  status: string
  created_at: string
}

interface PRD {
  id: string
  title: string
  description: string
  prd_type?: 'platform' | 'agent'
  status: string
  created_at: string
  completion_percentage?: number
  missing_sections?: string[]
}

export default function Dashboard() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [prds, setPrds] = useState<PRD[]>([])
  const [loading, setLoading] = useState(true)
  const [prdTypeFilter, setPrdTypeFilter] = useState<'all' | 'platform' | 'agent'>('all')
  const [showPRDForm, setShowPRDForm] = useState(false)
  const [showMarkdownImporter, setShowMarkdownImporter] = useState(false)
  const [showPRDChatbot, setShowPRDChatbot] = useState(false)
  const [activeChatPRDId, setActiveChatPRDId] = useState<string | null>(null)

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
      }
      
      if (prdsRes.ok) {
        const prdsData = await prdsRes.json()
        setPrds(prdsData)
      }
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePRDSuccess = (prdId?: string) => {
    fetchData() // Refresh the data to show the new PRD
    if (prdId) {
      setActiveChatPRDId(prdId)
      setShowPRDChatbot(true)
    }
  }

  const handleMarkdownImportSuccess = (prdId: string) => {
    fetchData()
    setActiveChatPRDId(prdId)
    setShowPRDChatbot(true)
  }


  const startPRDChat = (prdId: string) => {
    setActiveChatPRDId(prdId)
    setShowPRDChatbot(true)
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

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
      case 'created':
        return 'bg-green-100 text-green-800'
      case 'pending':
      case 'submitted':
        return 'bg-yellow-100 text-yellow-800'
      case 'error':
      case 'failed':
        return 'bg-red-100 text-red-800'
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
          A repeatable, voice-first, AI-driven platform for creating modular agents
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Agents</CardTitle>
            <Bot className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{agents.length}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {activeAgentsCount}
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">PRDs Submitted</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{prds.length}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">GitHub Repos</CardTitle>
            <Github className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {completedPrdsCount}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="create" className="space-y-4">
        <TabsList>
          <TabsTrigger value="create">Create New</TabsTrigger>
          <TabsTrigger value="prds">PRDs</TabsTrigger>
          <TabsTrigger value="agents">Agents</TabsTrigger>
          <TabsTrigger value="roadmap">Roadmap</TabsTrigger>
          <TabsTrigger value="devin">Devin AI</TabsTrigger>
        </TabsList>

        <TabsContent value="agents" className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-semibold">AI Agents</h2>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Create Agent
            </Button>
          </div>
          
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
                <Card key={agent.id}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="flex items-center gap-2">
                          {agent.name}
                          <Badge className={getStatusColor(agent.status)}>
                            {agent.status}
                          </Badge>
                        </CardTitle>
                        <CardDescription>{agent.description}</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-2">
                      <strong>Purpose:</strong> {agent.purpose}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Created: {new Date(agent.created_at).toLocaleDateString()}
                    </p>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>

        <TabsContent value="prds" className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-semibold">Product Requirements Documents</h2>
            <div className="flex items-center gap-3">
              <select
                className="border rounded px-2 py-1 text-sm"
                value={prdTypeFilter}
                onChange={(e) => setPrdTypeFilter(e.target.value as any)}
              >
                <option value="all">All Types</option>
                <option value="agent">Agent PRDs</option>
                <option value="platform">Platform PRDs</option>
              </select>
              <div className="relative">
                <Button onClick={() => setShowPRDForm(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Submit PRD
                </Button>
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={() => setShowMarkdownImporter(true)}
                  className="ml-2"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Import Markdown
                </Button>
              </div>
            </div>
          </div>
          
          <div className="grid gap-4">
            {prds.filter(p => prdTypeFilter === 'all' ? true : (p.prd_type || 'agent') === prdTypeFilter).length === 0 ? (
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-8">
                  <FileText className="h-12 w-12 text-muted-foreground mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No PRDs yet</h3>
                  <p className="text-muted-foreground text-center mb-4">
                    Submit your first PRD to start creating AI agents
                  </p>
                  <Button onClick={() => setShowPRDForm(true)}>Submit First PRD</Button>
                </CardContent>
              </Card>
            ) : (
              prds
                .filter(p => prdTypeFilter === 'all' ? true : (p.prd_type || 'agent') === prdTypeFilter)
                .map((prd) => (
                <Card key={prd.id}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <CardTitle className="flex items-center gap-2">
                          {prd.title}
                          {prd.prd_type && (
                            <Badge variant="outline">{prd.prd_type}</Badge>
                          )}
                          <Badge className={getStatusColor(prd.status)}>
                            {prd.status}
                          </Badge>
                        </CardTitle>
                        <CardDescription>{prd.description}</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {prd.completion_percentage !== undefined && (
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-medium">Completion:</span>
                          <div className="flex-1 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${prd.completion_percentage}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-muted-foreground">
                            {prd.completion_percentage}%
                          </span>
                        </div>
                      )}
                      <div className="flex justify-between items-center">
                        <p className="text-xs text-muted-foreground">
                          Submitted: {new Date(prd.created_at).toLocaleDateString()}
                        </p>
                        <div className="flex gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => viewPRDMarkdown(prd.id)}
                            className="flex items-center gap-1"
                          >
                            <Eye className="h-3 w-3" />
                            View PRD
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => downloadPRDMarkdown(prd.id, prd.title)}
                            className="flex items-center gap-1"
                          >
                            <Download className="h-3 w-3" />
                            Download
                          </Button>
                          <Button
                            size="sm"
                            onClick={() => startPRDChat(prd.id)}
                            className="flex items-center gap-1"
                          >
                            <Bot className="h-3 w-3" />
                            Chat to Complete
                          </Button>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>

        <TabsContent value="roadmap" className="space-y-4">
          <RoadmapDashboard />
        </TabsContent>

        <TabsContent value="devin" className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-semibold">Devin AI Integration</h2>
            <Badge variant="outline">Copy-Paste Workflow</Badge>
          </div>
          <DevinIntegration />
        </TabsContent>

        <TabsContent value="create" className="space-y-6">
          <div className="text-center space-y-4">
            <h2 className="text-3xl font-bold">Create Your AI Agent</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Upload your completed PRD and let our AI Factory create and deploy your custom AI agent 
              with all the specifications and requirements you've defined.
            </p>
          </div>

          {/* Primary Workflow - ChatGPT Voice Integration */}
          <div className="max-w-4xl mx-auto">
            <Card className="border-2 border-green-200 hover:border-green-300 transition-all duration-200 shadow-lg">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-20 h-20 bg-gradient-to-br from-green-100 to-green-200 rounded-full flex items-center justify-center mb-4">
                  <Bot className="h-10 w-10 text-green-600" />
                </div>
                <CardTitle className="text-2xl text-green-800">Agent Creation from PRD</CardTitle>
                <CardDescription className="text-base text-green-700">
                  Upload your completed PRD and create your AI agent automatically
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* How it works section */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-800 mb-3 flex items-center gap-2">
                    <span className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm">1</span>
                    Upload Your PRD
                  </h4>
                  <p className="text-blue-700 text-sm mb-3">
                    Upload your completed PRD that has been refined and formatted by your GPT.
                  </p>
                  <Button 
                    onClick={() => setShowMarkdownImporter(true)}
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
                    Agent Generation
                  </h4>
                  <p className="text-green-700 text-sm mb-3">
                    Our AI Factory automatically generates your custom agent based on the PRD specifications.
                  </p>
                </div>

                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                  <h4 className="font-semibold text-purple-800 mb-3 flex items-center gap-2">
                    <span className="w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm">3</span>
                    Deploy & Monitor
                  </h4>
                  <p className="text-purple-700 text-sm">
                    Your agent is deployed and ready to use. Monitor its performance and make adjustments as needed.
                  </p>
                </div>

                {/* Benefits */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Automated Generation</p>
                      <p className="text-xs text-muted-foreground">No manual coding required</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">PRD-Driven</p>
                      <p className="text-xs text-muted-foreground">Built from your specifications</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Ready to Deploy</p>
                      <p className="text-xs text-muted-foreground">Immediately usable agents</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Performance Monitoring</p>
                      <p className="text-xs text-muted-foreground">Track and optimize</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Alternative Options */}
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-4">
              <h3 className="text-lg font-semibold text-muted-foreground">Alternative Methods</h3>
              <p className="text-sm text-muted-foreground">Other ways to create agents</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card className="hover:shadow-md transition-shadow">
                <CardContent className="p-6 text-center">
                  <div className="mx-auto w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-3">
                    <FileText className="h-6 w-6 text-gray-600" />
                  </div>
                  <h4 className="font-medium mb-2">Manual PRD Creation</h4>
                  <p className="text-sm text-muted-foreground mb-4">
                    Create a PRD using our form if you don't have one ready
                  </p>
                  <Button 
                    onClick={() => setShowPRDForm(true)}
                    variant="outline"
                    size="sm"
                    className="w-full"
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Create PRD
                  </Button>
                </CardContent>
              </Card>
              
              <Card className="hover:shadow-md transition-shadow">
                <CardContent className="p-6 text-center">
                  <div className="mx-auto w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-3">
                    <Github className="h-6 w-6 text-purple-600" />
                  </div>
                  <h4 className="font-medium mb-2">API Integration</h4>
                  <p className="text-sm text-muted-foreground mb-4">
                    Submit PRDs programmatically via REST API
                  </p>
                  <Button variant="outline" size="sm" disabled className="w-full">
                    <Activity className="h-4 w-4 mr-2" />
                    Coming Soon
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>
      </Tabs>

      {/* PRD Creation Form Modal */}
      {showPRDForm && (
        <PRDCreationForm
          onClose={() => setShowPRDForm(false)}
          onSuccess={handlePRDSuccess}
        />
      )}

      {/* Markdown PRD Importer Modal */}
      {showMarkdownImporter && (
        <MarkdownPRDImporter
          onClose={() => setShowMarkdownImporter(false)}
          onSuccess={handleMarkdownImportSuccess}
        />
      )}

      {/* PRD Chatbot Modal */}
      {showPRDChatbot && activeChatPRDId && (
        <PRDChatbot
          prdId={activeChatPRDId}
          onClose={() => setShowPRDChatbot(false)}
          onComplete={() => {
            setShowPRDChatbot(false)
            setActiveChatPRDId(null)
            fetchData()
          }}
        />
      )}

    </div>
  )
}
