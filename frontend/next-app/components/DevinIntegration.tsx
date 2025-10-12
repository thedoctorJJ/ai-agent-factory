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

  const createDevinTask = async () => {
    if (!selectedPRD) {
      alert('Please select a PRD first')
      return
    }

    try {
      const response = await fetch('/api/v1/devin/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prd_id: selectedPRD.id,
          title: selectedPRD.title,
          description: selectedPRD.description || 'No description provided',
          requirements: selectedPRD.requirements || [],
        }),
      })

      if (response.ok) {
        const newTask = await response.json()
        setTasks([...(Array.isArray(tasks) ? tasks : []), newTask])
        setSelectedTask(newTask)
        
        // Reset progress for new task
        setProgress({
          codeGeneration: false,
          githubRepo: false,
          databaseSetup: false,
          cloudDeployment: false
        })

        // Automatically execute the task with Devin AI
        try {
          const executeResponse = await fetch(`/api/v1/devin/tasks/${newTask.id}/execute`, {
            method: 'POST',
          })
          
          if (executeResponse.ok) {
            const executeResult = await executeResponse.json()
            console.log('Devin AI execution initiated:', executeResult)
            // Update the task status
            setSelectedTask({...newTask, status: 'in_devin'})
          }
        } catch (error) {
          console.error('Error executing Devin task:', error)
        }
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
              <p className="text-muted-foreground mb-4">No PRDs available. Upload a PRD first.</p>
              <Button onClick={() => window.location.href = '/upload'}>
                Upload PRD
              </Button>
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
                    onClick={createDevinTask} 
                    className="w-full"
                  >
                    🚀 Create Agent with Devin AI
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
    </div>
  )
}
