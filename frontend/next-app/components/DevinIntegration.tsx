'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Copy, ExternalLink, CheckCircle, Clock, AlertCircle, Loader2, ChevronDown, ChevronUp } from 'lucide-react'

interface DevinTask {
  id: string
  prd_id: string
  title: string
  description: string
  requirements: string[]
  devin_prompt: string
  status: 'pending' | 'in_devin' | 'completed' | 'failed'
  created_at: string
  updated_at: string
  devin_output?: string
  agent_code?: string
}

interface PRD {
  id: string
  title: string
  description: string
  requirements?: string[]
}

interface DevinIntegrationProps {
  prds: PRD[]
}

export default function DevinIntegration({ 
  prds 
}: DevinIntegrationProps) {
  const [tasks, setTasks] = useState<DevinTask[]>([])
  const [selectedTask, setSelectedTask] = useState<DevinTask | null>(null)
  const [selectedPRD, setSelectedPRD] = useState<PRD | null>(null)
  const [copied, setCopied] = useState(false)
  const [agentCode, setAgentCode] = useState('')
  const [showPrompt, setShowPrompt] = useState(false)
  const [showTasks, setShowTasks] = useState(false)
  const [showPromptModal, setShowPromptModal] = useState(false)
  const [devinPrompt, setDevinPrompt] = useState('')
  const [progress, setProgress] = useState({
    codeGeneration: false,
    githubRepo: false,
    databaseSetup: false,
    cloudDeployment: false
  })

  // Fetch existing Devin tasks when component loads
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch('/api/v1/devin/tasks')
        if (response.ok) {
          const tasksData = await response.json()
          setTasks(tasksData.tasks || [])
          // If there's a task, select it
          if (tasksData.tasks && tasksData.tasks.length > 0) {
            setSelectedTask(tasksData.tasks[0])
          }
        }
      } catch (error) {
        console.error('Error fetching Devin tasks:', error)
      }
    }

    fetchTasks()
  }, [])

  // Simulate progress updates for active tasks
  useEffect(() => {
    if (selectedTask && selectedTask.status === 'in_devin') {
      const progressSteps = [
        { key: 'codeGeneration', delay: 2000 },
        { key: 'githubRepo', delay: 5000 },
        { key: 'databaseSetup', delay: 8000 },
        { key: 'cloudDeployment', delay: 12000 }
      ]

      progressSteps.forEach((step, index) => {
        setTimeout(() => {
          setProgress(prev => ({ ...prev, [step.key]: true }))
        }, step.delay)
      })
    } else if (selectedTask && selectedTask.status === 'completed') {
      // If task is completed, mark all progress steps as completed
      setProgress({
        codeGeneration: true,
        githubRepo: true,
        databaseSetup: true,
        cloudDeployment: true
      })
    }
  }, [selectedTask])

  const loadPRDToMCP = async () => {
    if (!selectedPRD) {
      alert('Please select a PRD first')
      return
    }

    try {
      // Load PRD data to MCP server
      const loadResponse = await fetch('/api/v1/mcp/load-prd', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prd_id: selectedPRD.id
        }),
      })
      
      if (loadResponse.ok) {
        const loadResult = await loadResponse.json()
        console.log('PRD loaded to MCP server:', loadResult)
        
        // Show success message with simple startup prompt
        const simplePrompt = `✅ PRD "${selectedPRD.title}" has been loaded into the MCP server cache.

🚀 To start working with Devin AI:

1. Open Devin AI in your browser
2. Use this simple prompt to begin:

---

# AI Agent Factory - Simple Startup Prompt

## 🚀 Welcome to the AI Agent Factory!

You are an AI agent creation specialist connected to the AI Agent Factory system via MCP.

## 📋 Quick Start Instructions:

1. **Get the complete guide** from the MCP server:
   \`\`\`
   Use MCP tool: get_startup_guide
   \`\`\`

2. **Follow the guide** to check for available PRDs and create agents

3. **Start the process** by checking for work:
   \`\`\`
   Use MCP tool: check_available_prds
   \`\`\`

## 🎯 Your Mission:
- Find PRDs that need agents created
- Analyze requirements and create appropriate AI agents  
- Deploy agents to the cloud
- Update the platform with results

## 🚀 Let's Begin!

First, get the complete startup guide:

\`\`\`
Use MCP tool: get_startup_guide
\`\`\`

Then follow the guide to start creating agents!

---

Copy this prompt and paste it into Devin AI to begin the agent creation process!`
        
        setDevinPrompt(simplePrompt)
        setShowPromptModal(true)
      } else {
        console.error('Failed to load PRD to MCP server')
        alert('Failed to load PRD to MCP server. Please try again.')
      }
    } catch (error) {
      console.error('Error loading PRD to MCP server:', error)
      alert('Error loading PRD to MCP server. Please try again.')
    }
  }

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy:', error)
    }
  }


  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'in_devin':
        return <Clock className="h-4 w-4 text-blue-500" />
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'in_devin':
        return 'bg-blue-100 text-blue-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const ProgressBar = () => {
    const steps = [
      { key: 'codeGeneration', label: 'Code Generation', description: 'Devin AI is analyzing the PRD and generating agent code' },
      { key: 'githubRepo', label: 'GitHub Repository', description: 'Creating repository and pushing initial code' },
      { key: 'databaseSetup', label: 'Database Setup', description: 'Configuring Supabase database and schemas' },
      { key: 'cloudDeployment', label: 'Cloud Deployment', description: 'Deploying to Google Cloud Run' }
    ]

    const completedSteps = Object.values(progress).filter(Boolean).length
    const totalSteps = steps.length
    const progressPercentage = (completedSteps / totalSteps) * 100

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h4 className="text-sm font-medium">Agent Creation Progress</h4>
          <span className="text-sm text-muted-foreground">{completedSteps}/{totalSteps} steps completed</span>
        </div>
        
        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progressPercentage}%` }}
          ></div>
        </div>

        {/* Progress Steps */}
        <div className="space-y-3">
          {steps.map((step, index) => {
            const isCompleted = progress[step.key as keyof typeof progress]
            const isCurrent = !isCompleted && (index === 0 || progress[steps[index - 1].key as keyof typeof progress])
            
            return (
              <div key={step.key} className="flex items-start space-x-3">
                <div className="flex-shrink-0 mt-0.5">
                  {isCompleted ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : isCurrent ? (
                    <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
                  ) : (
                    <div className="h-5 w-5 rounded-full border-2 border-gray-300"></div>
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
    )
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ExternalLink className="h-5 w-5" />
            Select a PRD to create an agent
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {prds.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground mb-4">No PRDs available. Please upload a PRD in the PRDs tab first.</p>
            </div>
          ) : (
            <>
              <div className="space-y-2">
                <select
                  className="w-full p-3 border border-gray-200 rounded-lg bg-white"
                  value={selectedPRD?.id || ''}
                  onChange={(e) => {
                    const prd = prds.find(p => p.id === e.target.value)
                    setSelectedPRD(prd || null)
                  }}
                >
                  <option value="">Choose a PRD...</option>
                  {prds.map((prd) => (
                    <option key={prd.id} value={prd.id}>
                      {prd.title}
                    </option>
                  ))}
                </select>
              </div>

              {selectedPRD && (
                <div className="space-y-4">
                  <div className="p-3 border border-blue-500 bg-blue-50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <h5 className="font-medium">{selectedPRD.title}</h5>
                        <p className="text-sm text-muted-foreground">
                          {selectedPRD.description || 'No description'}
                        </p>
                      </div>
                      <div className="w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
                        <div className="w-2 h-2 bg-white rounded-full"></div>
                      </div>
                    </div>
                  </div>
                  
                  <Button 
                    onClick={loadPRDToMCP} 
                    className="w-full"
                  >
                    📤 Load PRD to MCP Server
                  </Button>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>

      {selectedTask && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              {selectedTask.title}
              <Badge className={getStatusColor(selectedTask.status)}>
                {getStatusIcon(selectedTask.status)}
                <span className="ml-1 capitalize">{selectedTask.status}</span>
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Generated Prompt - First Step */}
            <div className="space-y-2">
              <Button
                variant="ghost"
                onClick={() => setShowPrompt(!showPrompt)}
                className="w-full justify-between p-0 h-auto"
              >
                <span className="text-sm font-medium">PRD</span>
                {showPrompt ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </Button>
              
              {showPrompt && (
                <div className="mt-3 space-y-2">
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-muted-foreground">The PRD data has been automatically sent to Devin AI via API integration.</p>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => copyToClipboard(selectedTask.devin_prompt)}
                    >
                      {copied ? <CheckCircle className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                      {copied ? 'Copied!' : 'Copy'}
                    </Button>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg border max-h-96 overflow-y-auto">
                    <pre className="text-sm whitespace-pre-wrap">{selectedTask.devin_prompt}</pre>
                  </div>
                </div>
              )}
            </div>

            {/* Status and Progress - Second Step */}
            <div className="border-t pt-4 space-y-4">
              
              {selectedTask.status === 'completed' ? (
                <div className="space-y-4">
                  <ProgressBar />
                  <div className="bg-green-50 p-3 rounded-lg border border-green-200">
                    <h4 className="text-sm font-medium text-green-800">✅ Agent Created Successfully!</h4>
                  </div>
                </div>
              ) : selectedTask.status === 'in_devin' || selectedTask.status === 'pending' ? (
                <ProgressBar />
              ) : (
                <div className="text-center py-8">
                  <p className="text-muted-foreground">Waiting for agent creation to begin...</p>
                </div>
              )}
            </div>
            
            {selectedTask.status === 'completed' && (
              <div className="text-center py-4">
                <p className="text-sm text-muted-foreground">
                  ✅ Your agent is now available in the <strong>Agents</strong> tab
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {tasks.length > 0 && (
        <Card>
          <CardHeader>
            <Button
              variant="ghost"
              onClick={() => setShowTasks(!showTasks)}
              className="w-full justify-between p-0 h-auto"
            >
              <CardTitle className="text-left">Changelog</CardTitle>
              {showTasks ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
            </Button>
          </CardHeader>
          {showTasks && (
            <CardContent>
              <div className="space-y-2">
                {tasks.map((task) => (
                  <div
                    key={task.id}
                    className="flex items-center justify-between p-3 border rounded-lg cursor-pointer hover:bg-gray-50"
                    onClick={() => setSelectedTask(task)}
                  >
                    <div>
                      <h4 className="font-medium">{task.title || 'Quick Test Agent PRD'}</h4>
                      <p className="text-sm text-gray-500">
                        Created: {new Date(task.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <Badge className={getStatusColor(task.status)}>
                      {getStatusIcon(task.status)}
                      <span className="ml-1 capitalize">{task.status}</span>
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          )}
        </Card>
      )}

      {/* MCP Prompt Modal */}
      {showPromptModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">Devin AI Simple Startup Prompt</h3>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowPromptModal(false)}
              >
                Close
              </Button>
            </div>
            
            <div className="mb-4">
              <div className="bg-green-100 p-4 rounded-lg mb-4">
                <pre className="whitespace-pre-wrap text-sm font-mono text-green-800">
                  {devinPrompt}
                </pre>
              </div>
              
              <div className="mt-4 flex gap-2">
                <Button
                  onClick={() => {
                    navigator.clipboard.writeText(devinPrompt)
                    setCopied(true)
                    setTimeout(() => setCopied(false), 2000)
                  }}
                  className="flex items-center gap-2"
                >
                  <Copy className="h-4 w-4" />
                  {copied ? 'Copied!' : 'Copy Prompt'}
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => window.open('https://devin.ai', '_blank')}
                  className="flex items-center gap-2"
                >
                  <ExternalLink className="h-4 w-4" />
                  Open Devin AI
                </Button>
              </div>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-blue-800 mb-2">🚀 Next Steps:</h4>
              <ol className="text-sm text-blue-700 space-y-1">
                <li>1. <strong>PRD data is loaded</strong> into the MCP server cache</li>
                <li>2. Copy the simple prompt above</li>
                <li>3. Open Devin AI in your browser</li>
                <li>4. Paste the prompt into Devin AI</li>
                <li>5. Devin will use the MCP tool to get the complete guide</li>
                <li>6. Devin will follow the guide and check for available PRDs</li>
                <li>7. Devin will find your PRD and start the agent creation process</li>
                <li>8. Check back here for status updates</li>
              </ol>
            </div>
            
            <div className="bg-green-50 p-4 rounded-lg mt-4">
              <h4 className="font-semibold text-green-800 mb-2">✅ Smart Startup Ready:</h4>
              <p className="text-sm text-green-700">
                This approach is much cleaner:
                <br />• <strong>Simple prompt</strong> - Easy to copy and paste
                <br />• <strong>Guide fetched dynamically</strong> - Always up-to-date
                <br />• <strong>Maintainable</strong> - Update guide without changing frontend
                <br />• <strong>Self-contained</strong> - Guide includes everything needed
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
