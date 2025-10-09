'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Copy, ExternalLink, CheckCircle, Clock, AlertCircle } from 'lucide-react'

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

interface DevinIntegrationProps {
  prdId?: string
  prdTitle?: string
  prdDescription?: string
  prdRequirements?: string[]
}

export default function DevinIntegration({ 
  prdId, 
  prdTitle, 
  prdDescription, 
  prdRequirements 
}: DevinIntegrationProps) {
  const [tasks, setTasks] = useState<DevinTask[]>([])
  const [selectedTask, setSelectedTask] = useState<DevinTask | null>(null)
  const [copied, setCopied] = useState(false)
  const [agentCode, setAgentCode] = useState('')

  const createDevinTask = async () => {
    if (!prdId || !prdTitle || !prdDescription || !prdRequirements) {
      alert('Please provide PRD information first')
      return
    }

    try {
      const response = await fetch('/api/v1/devin/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prd_id: prdId,
          title: prdTitle,
          description: prdDescription,
          requirements: prdRequirements,
        }),
      })

      if (response.ok) {
        const newTask = await response.json()
        setTasks([...tasks, newTask])
        setSelectedTask(newTask)
      }
    } catch (error) {
      console.error('Error creating Devin task:', error)
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

  const markTaskCompleted = async (taskId: string) => {
    try {
      const response = await fetch(`/api/v1/devin/tasks/${taskId}/complete`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          agent_code: 'Deployed via MCP servers',
          deployment_method: 'mcp_automatic'
        }),
      })

      if (response.ok) {
        const updatedTask = await response.json()
        setTasks(tasks.map(task => task.id === taskId ? updatedTask : task))
        setSelectedTask(updatedTask)
        setAgentCode('')
      }
    } catch (error) {
      console.error('Error completing task:', error)
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

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ExternalLink className="h-5 w-5" />
            Devin AI Integration
          </CardTitle>
          <CardDescription>
            Create optimized prompts for Devin AI and manage the copy-paste workflow. 
            <br />
            <strong>💡 Tip:</strong> You can also export PRDs as markdown files from the PRDs tab to share with Devin AI.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={createDevinTask} className="w-full">
            Create Devin AI Task
          </Button>
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
          <CardContent>
            <Tabs defaultValue="prompt" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="prompt">Devin Prompt</TabsTrigger>
                <TabsTrigger value="result">Agent Code</TabsTrigger>
              </TabsList>
              
              <TabsContent value="prompt" className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-medium">Copy this prompt to Devin AI:</h4>
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
                
                <div className="flex gap-2">
                  <Button
                    onClick={() => window.open('https://devin.ai', '_blank')}
                    variant="outline"
                  >
                    <ExternalLink className="h-4 w-4 mr-2" />
                    Open Devin AI
                  </Button>
                  <Button
                    onClick={() => {
                      setSelectedTask({...selectedTask, status: 'in_devin'})
                    }}
                    variant="outline"
                  >
                    Mark as "In Devin"
                  </Button>
                </div>
              </TabsContent>
              
              <TabsContent value="result" className="space-y-4">
                <div className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                    <h4 className="text-sm font-medium text-blue-800 mb-2">🚀 Streamlined Deployment</h4>
                    <p className="text-sm text-blue-700">
                      Devin AI will automatically deploy the agent using MCP servers. No manual code copying required!
                    </p>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium">Deployment Status:</h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-sm">
                      <div className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                        <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                        GitHub Repository
                      </div>
                      <div className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                        <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                        Supabase Database
                      </div>
                      <div className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                        <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                        Cloud Run Deployment
                      </div>
                    </div>
                  </div>
                </div>
                
                <Button
                  onClick={() => markTaskCompleted(selectedTask.id)}
                  className="w-full"
                >
                  Mark as Deployed
                </Button>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      )}

      {tasks.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Devin AI Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between p-3 border rounded-lg cursor-pointer hover:bg-gray-50"
                  onClick={() => setSelectedTask(task)}
                >
                  <div>
                    <h4 className="font-medium">{task.title}</h4>
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
        </Card>
      )}
    </div>
  )
}
