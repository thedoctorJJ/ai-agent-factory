'use client'

import React, { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowLeft, Download, Eye, Bot, Building, FileText, Calendar, User, Target, CheckCircle, Wrench, Shield, Link, Rocket, BarChart3, Clock, AlertTriangle, Lightbulb } from 'lucide-react'

interface PRD {
  id: string
  title: string
  description: string
  requirements: string[]
  prd_type: string
  status: string
  created_at: string
  updated_at: string
  problem_statement?: string
  target_users?: string[]
  user_stories?: string[]
  acceptance_criteria?: string[]
  technical_requirements?: string[]
  performance_requirements?: Record<string, string>
  security_requirements?: string[]
  integration_requirements?: string[]
  deployment_requirements?: string[]
  success_metrics?: string[]
  timeline?: string
  dependencies?: string[]
  risks?: string[]
  assumptions?: string[]
  original_filename?: string
  file_content?: string
}

export default function PRDDetailPage() {
  const router = useRouter()
  const params = useParams()
  const [prd, setPrd] = useState<PRD | null>(null)
  const [loading, setLoading] = useState(true)
  const [showMarkdown, setShowMarkdown] = useState(false)

  useEffect(() => {
    if (params.id) {
      fetchPRD(params.id as string)
    }
  }, [params.id])

  const fetchPRD = async (id: string) => {
    try {
      const response = await fetch(`/api/v1/prds/${id}`)
      if (response.ok) {
        const data = await response.json()
        setPrd(data)
      } else {
        console.error('Failed to fetch PRD')
      }
    } catch (error) {
      console.error('Error fetching PRD:', error)
    } finally {
      setLoading(false)
    }
  }

  const downloadMarkdown = async () => {
    if (!prd) return
    
    try {
      const response = await fetch(`/api/v1/prds/${prd.id}/markdown/download`)
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${prd.title.replace(/\s+/g, '-').toLowerCase()}.md`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }
    } catch (error) {
      console.error('Download error:', error)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready_for_agent_creation': return 'bg-green-100 text-green-800'
      case 'backlog': return 'bg-gray-100 text-gray-800'
      case 'in_progress': return 'bg-blue-100 text-blue-800'
      case 'completed': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p>Loading PRD...</p>
        </div>
      </div>
    )
  }

  if (!prd) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">PRD Not Found</h1>
          <Button onClick={() => router.push('/')}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-6 max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="ghost"
            onClick={() => router.back()}
            className="mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
          
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-3xl font-bold tracking-tight">{prd.title}</h1>
                <Badge className={getStatusColor(prd.status)}>
                  {prd.status.replace(/_/g, ' ')}
                </Badge>
                <Badge variant="outline" className="flex items-center gap-1">
                  {prd.prd_type === 'agent' ? <Bot className="h-3 w-3" /> : <Building className="h-3 w-3" />}
                  {prd.prd_type} PRD
                </Badge>
              </div>
              <p className="text-muted-foreground text-lg">{prd.description}</p>
            </div>
            
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => setShowMarkdown(!showMarkdown)}>
                <Eye className="h-4 w-4 mr-2" />
                {showMarkdown ? 'Hide' : 'Show'} Markdown
              </Button>
              <Button onClick={downloadMarkdown}>
                <Download className="h-4 w-4 mr-2" />
                Download
              </Button>
            </div>
          </div>
        </div>

        {showMarkdown && prd.file_content && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Original Markdown Content</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="whitespace-pre-wrap text-sm bg-gray-50 p-4 rounded-lg overflow-auto max-h-96">
                {prd.file_content}
              </pre>
            </CardContent>
          </Card>
        )}

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Left Column */}
          <div className="space-y-6">
            {/* Problem Statement */}
            {prd.problem_statement && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5" />
                    Problem Statement
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm">{prd.problem_statement}</p>
                </CardContent>
              </Card>
            )}

            {/* Target Users */}
            {prd.target_users && prd.target_users.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <User className="h-5 w-5" />
                    Target Users
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-1">
                    {prd.target_users.map((user, index) => (
                      <li key={index} className="text-sm flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
                        {user}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Requirements */}
            {prd.requirements && prd.requirements.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="h-5 w-5" />
                    Requirements
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.requirements.map((req, index) => (
                      <li key={index} className="text-sm flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                        {req}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* User Stories */}
            {prd.user_stories && prd.user_stories.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="h-5 w-5" />
                    User Stories
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.user_stories.map((story, index) => (
                      <li key={index} className="text-sm p-3 bg-blue-50 rounded-lg">
                        {story}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Acceptance Criteria */}
            {prd.acceptance_criteria && prd.acceptance_criteria.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="h-5 w-5" />
                    Acceptance Criteria
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.acceptance_criteria.map((criteria, index) => (
                      <li key={index} className="text-sm flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2 flex-shrink-0"></div>
                        {criteria}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Technical Requirements */}
            {prd.technical_requirements && prd.technical_requirements.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Wrench className="h-5 w-5" />
                    Technical Requirements
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.technical_requirements.map((req, index) => (
                      <li key={index} className="text-sm flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-orange-500 rounded-full mt-2 flex-shrink-0"></div>
                        {req}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Security Requirements */}
            {prd.security_requirements && prd.security_requirements.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Shield className="h-5 w-5" />
                    Security Requirements
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.security_requirements.map((req, index) => (
                      <li key={index} className="text-sm flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                        {req}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Integration Requirements */}
            {prd.integration_requirements && prd.integration_requirements.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Link className="h-5 w-5" />
                    Integration Requirements
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.integration_requirements.map((req, index) => (
                      <li key={index} className="text-sm flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full mt-2 flex-shrink-0"></div>
                        {req}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Deployment Requirements */}
            {prd.deployment_requirements && prd.deployment_requirements.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Rocket className="h-5 w-5" />
                    Deployment Requirements
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.deployment_requirements.map((req, index) => (
                      <li key={index} className="text-sm flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-teal-500 rounded-full mt-2 flex-shrink-0"></div>
                        {req}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Success Metrics */}
            {prd.success_metrics && prd.success_metrics.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Success Metrics
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.success_metrics.map((metric, index) => (
                      <li key={index} className="text-sm flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full mt-2 flex-shrink-0"></div>
                        {metric}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Timeline */}
            {prd.timeline && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Clock className="h-5 w-5" />
                    Timeline
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm whitespace-pre-wrap">{prd.timeline}</p>
                </CardContent>
              </Card>
            )}

            {/* Risks */}
            {prd.risks && prd.risks.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5" />
                    Risks
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.risks.map((risk, index) => (
                      <li key={index} className="text-sm flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-yellow-500 rounded-full mt-2 flex-shrink-0"></div>
                        {risk}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Assumptions */}
            {prd.assumptions && prd.assumptions.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Lightbulb className="h-5 w-5" />
                    Assumptions
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prd.assumptions.map((assumption, index) => (
                      <li key={index} className="text-sm flex items-start gap-2">
                        <div className="w-1.5 h-1.5 bg-pink-500 rounded-full mt-2 flex-shrink-0"></div>
                        {assumption}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Metadata */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>PRD Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <div>
                <h4 className="font-medium text-sm text-muted-foreground">Created</h4>
                <p className="text-sm">{new Date(prd.created_at).toLocaleDateString()}</p>
              </div>
              <div>
                <h4 className="font-medium text-sm text-muted-foreground">Last Updated</h4>
                <p className="text-sm">{new Date(prd.updated_at).toLocaleDateString()}</p>
              </div>
              {prd.original_filename && (
                <div>
                  <h4 className="font-medium text-sm text-muted-foreground">Original File</h4>
                  <p className="text-sm">{prd.original_filename}</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
