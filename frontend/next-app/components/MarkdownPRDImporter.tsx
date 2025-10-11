'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { X, Upload, FileText, Bot, Building, CheckCircle, AlertCircle, MessageSquare } from 'lucide-react'
import PRDChatbot from './PRDChatbot'

interface ParsedPRD {
  title?: string
  description?: string
  problem_statement?: string
  target_users?: string[]
  user_stories?: string[]
  requirements?: string[]
  acceptance_criteria?: string[]
  technical_requirements?: string
  success_metrics?: string[]
  timeline?: string
  prd_type?: 'agent' | 'platform'
  performance_requirements?: string
  security_requirements?: string[]
  integration_requirements?: string[]
  deployment_requirements?: string[]
  dependencies?: string[]
  risks?: string[]
  assumptions?: string[]
}

interface MarkdownPRDImporterProps {
  onClose: () => void
  onSuccess: (prdId: string) => void
}

export default function MarkdownPRDImporter({ onClose, onSuccess }: MarkdownPRDImporterProps) {
  const [markdownContent, setMarkdownContent] = useState('')
  const [parsedPRD, setParsedPRD] = useState<ParsedPRD | null>(null)
  const [isParsing, setIsParsing] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [parseError, setParseError] = useState('')
  const [showConversationalReview, setShowConversationalReview] = useState(false)
  const [prdId, setPrdId] = useState<string | null>(null)

  const parseMarkdownPRD = (markdown: string): ParsedPRD => {
    const lines = markdown.split('\n')
    const prd: ParsedPRD = {}
    
    let currentSection = ''
    let currentContent: string[] = []
    
    // Helper function to save section content
    const saveSection = (section: string, content: string) => {
      if (!content.trim()) return
      
      switch (section.toLowerCase()) {
        case 'title':
        case 'project title':
        case 'prd title':
          prd.title = content.trim()
          break
        case 'description':
        case 'project overview':
        case 'overview':
          prd.description = content.trim()
          break
        case 'problem statement':
        case 'problem':
        case 'problem definition':
          prd.problem_statement = content.trim()
          break
        case 'target users':
        case 'users':
        case 'audience':
        case 'user base':
          prd.target_users = content.split('\n')
            .map(u => u.replace(/^[-*•]\s*/, '').trim())
            .filter(u => u && !u.startsWith('#'))
          break
        case 'user stories':
        case 'stories':
        case 'user story':
          prd.user_stories = content.split('\n')
            .filter(s => s.trim() && !s.startsWith('#'))
            .map(s => s.replace(/^[-*•]\s*/, '').trim())
            .filter(s => s)
          break
        case 'requirements':
        case 'functional requirements':
        case 'feature requirements':
        case 'specifications':
          prd.requirements = content.split('\n')
            .filter(r => r.trim() && !r.startsWith('#'))
            .map(r => r.replace(/^[-*•]\s*/, '').trim())
            .filter(r => r)
          break
        case 'acceptance criteria':
        case 'criteria':
        case 'acceptance':
          prd.acceptance_criteria = content.split('\n')
            .filter(c => c.trim() && !c.startsWith('#'))
            .map(c => c.replace(/^[-*•]\s*/, '').trim())
            .filter(c => c)
          break
        case 'technical requirements':
        case 'technical specs':
        case 'technical specifications':
        case 'technical details':
          prd.technical_requirements = content.trim()
          break
        case 'success metrics':
        case 'metrics':
        case 'kpis':
        case 'key performance indicators':
          prd.success_metrics = content.split('\n')
            .filter(m => m.trim() && !m.startsWith('#'))
            .map(m => m.replace(/^[-*•]\s*/, '').trim())
            .filter(m => m)
          break
        case 'timeline':
        case 'schedule':
        case 'deadline':
        case 'delivery':
          prd.timeline = content.trim()
          break
        case 'performance requirements':
        case 'performance':
          prd.performance_requirements = content.trim()
          break
        case 'security requirements':
        case 'security':
          prd.security_requirements = content.split('\n')
            .filter(s => s.trim() && !s.startsWith('#'))
            .map(s => s.replace(/^[-*•]\s*/, '').trim())
            .filter(s => s)
          break
        case 'integration requirements':
        case 'integration':
          prd.integration_requirements = content.split('\n')
            .filter(i => i.trim() && !i.startsWith('#'))
            .map(i => i.replace(/^[-*•]\s*/, '').trim())
            .filter(i => i)
          break
        case 'deployment requirements':
        case 'deployment':
          prd.deployment_requirements = content.split('\n')
            .filter(d => d.trim() && !d.startsWith('#'))
            .map(d => d.replace(/^[-*•]\s*/, '').trim())
            .filter(d => d)
          break
        case 'dependencies':
        case 'deps':
          prd.dependencies = content.split('\n')
            .filter(d => d.trim() && !d.startsWith('#'))
            .map(d => d.replace(/^[-*•]\s*/, '').trim())
            .filter(d => d)
          break
        case 'risks':
        case 'risk':
          prd.risks = content.split('\n')
            .filter(r => r.trim() && !r.startsWith('#'))
            .map(r => r.replace(/^[-*•]\s*/, '').trim())
            .filter(r => r)
          break
        case 'assumptions':
        case 'assumption':
          prd.assumptions = content.split('\n')
            .filter(a => a.trim() && !a.startsWith('#'))
            .map(a => a.replace(/^[-*•]\s*/, '').trim())
            .filter(a => a)
          break
      }
    }
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim()
      
      // Skip empty lines
      if (!line) continue
      
      // Check for headers (##, ###, ####)
      if (line.startsWith('#')) {
        // Save previous section
        if (currentSection && currentContent.length > 0) {
          const content = currentContent.join('\n').trim()
          saveSection(currentSection, content)
        }
        
        // Start new section
        currentSection = line.replace(/^#+\s*/, '').toLowerCase()
        currentContent = []
      } else {
        // Add content to current section
        currentContent.push(line)
      }
    }
    
    // Save last section
    if (currentSection && currentContent.length > 0) {
      const content = currentContent.join('\n').trim()
      saveSection(currentSection, content)
    }
    
    // Try to extract title from the first line if not found
    if (!prd.title) {
      const firstLine = lines.find(line => line.trim() && !line.startsWith('#'))
      if (firstLine) {
        prd.title = firstLine.replace(/^#+\s*/, '').trim()
      }
    }
    
    // Try to extract description from early content if not found
    if (!prd.description) {
      const descriptionLines = []
      let foundHeader = false
      for (const line of lines) {
        if (line.startsWith('#')) {
          if (foundHeader) break
          foundHeader = true
          continue
        }
        if (line.trim() && !line.startsWith('#')) {
          descriptionLines.push(line.trim())
        }
        if (descriptionLines.length >= 3) break
      }
      if (descriptionLines.length > 0) {
        prd.description = descriptionLines.join(' ')
      }
    }
    
    // Ensure all required sections are present (backend strict validation)
    const requiredSections = {
      'title': 'Untitled PRD',
      'description': 'Description to be completed',
      'problem_statement': 'Problem statement to be completed',
      'target_users': ['Target users to be defined'],
      'user_stories': ['User stories to be completed'],
      'requirements': ['Requirements to be completed'],
      'acceptance_criteria': ['Acceptance criteria to be completed'],
      'technical_requirements': ['Technical requirements to be completed'],
      'success_metrics': ['Success metrics to be completed'],
      'timeline': 'Timeline to be completed'
    }
    
    // Fill in missing required sections with placeholders
    for (const [section, defaultValue] of Object.entries(requiredSections)) {
      const value = prd[section as keyof ParsedPRD]
      if (!value || (Array.isArray(value) && value.length === 0) || (typeof value === 'string' && !value.trim())) {
        (prd as any)[section] = defaultValue
      }
    }
    
    // Determine PRD type based on content
    if (!prd.prd_type) {
      const content = markdown.toLowerCase()
      if (content.includes('platform') || content.includes('infrastructure') || content.includes('architecture') || content.includes('system')) {
        prd.prd_type = 'platform'
      } else {
        prd.prd_type = 'agent'
      }
    }
    
    return prd
  }

  const handleParse = async () => {
    if (!markdownContent.trim()) {
      setParseError('Please paste your markdown PRD content')
      return
    }

    setIsParsing(true)
    setParseError('')

    try {
      const parsed = parseMarkdownPRD(markdownContent)
      setParsedPRD(parsed)
    } catch (error) {
      setParseError('Error parsing markdown. Please check the format.')
      console.error('Parse error:', error)
    } finally {
      setIsParsing(false)
    }
  }

  const handleSubmit = async () => {
    if (!parsedPRD) return

    setIsSubmitting(true)
    setParseError('')

    // Debug: Log what we're sending
    console.log('Submitting PRD data:', parsedPRD)

    try {
      const response = await fetch('/api/v1/prds', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(parsedPRD),
      })

      if (response.ok) {
        const newPRD = await response.json()
        console.log('PRD created successfully:', newPRD)
        setPrdId(newPRD.id)
        setShowConversationalReview(true)
      } else {
        const error = await response.text()
        console.error('Error creating PRD:', error)
        
        // Try to parse the error for better user feedback
        try {
          const errorData = JSON.parse(error)
          if (errorData.detail && Array.isArray(errorData.detail)) {
            const missingFields = errorData.detail
              .filter((err: any) => err.type === 'missing')
              .map((err: any) => err.loc[1])
            setParseError(`Missing required fields: ${missingFields.join(', ')}. Please ensure your markdown includes these sections.`)
          } else {
            setParseError('Error creating PRD. Please check the console for details.')
          }
        } catch {
          setParseError('Error creating PRD. Please check the console for details.')
        }
      }
    } catch (error) {
      console.error('Error creating PRD:', error)
      setParseError('Network error. Please check your connection and try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const getMissingSections = (prd: ParsedPRD): string[] => {
    const required = [
      'title', 'description', 'problem_statement', 'target_users', 
      'user_stories', 'requirements', 'acceptance_criteria', 
      'technical_requirements', 'success_metrics', 'timeline'
    ]
    
    return required.filter(section => {
      const value = prd[section as keyof ParsedPRD]
      return !value || (Array.isArray(value) && value.length === 0) || (typeof value === 'string' && !value.trim())
    })
  }

  const getCompletionPercentage = (prd: ParsedPRD): number => {
    const required = [
      'title', 'description', 'problem_statement', 'target_users', 
      'user_stories', 'requirements', 'acceptance_criteria', 
      'technical_requirements', 'success_metrics', 'timeline'
    ]
    
    const filled = required.filter(section => {
      const value = prd[section as keyof ParsedPRD]
      return value && (Array.isArray(value) ? value.length > 0 : value.toString().trim())
    }).length
    
    return Math.round((filled / required.length) * 100)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-6xl max-h-[90vh] overflow-y-auto">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Upload Completed PRD
            </CardTitle>
            <CardDescription>
              Upload your completed PRD to create your AI agent automatically
            </CardDescription>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {!parsedPRD ? (
            // Step 1: Paste markdown
            <div className="space-y-6">
              {/* Instructions */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  Upload your completed PRD
                </h4>
                <ol className="text-sm text-blue-700 space-y-1">
                  <li>1. Your PRD should be completed and formatted by your GPT</li>
                  <li>2. Copy the markdown content of your PRD</li>
                  <li>3. Paste it in the text area below</li>
                </ol>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Paste your completed PRD markdown:</label>
                <textarea
                  value={markdownContent}
                  onChange={(e) => setMarkdownContent(e.target.value)}
                  className="w-full p-4 border rounded-lg h-96 font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  placeholder="Paste your completed PRD markdown here...

Example:
# Project Management AI Agent

## Problem Statement
Small to medium teams struggle with task visibility and deadline management...

## Target Users
- Project managers in small to medium teams (5-20 people)
- Team leads who need better visibility

## Requirements
- Real-time task tracking and status updates
- Deadline reminders and notifications..."
                />
                <div className="flex justify-between items-center mt-2">
                  <span className="text-xs text-muted-foreground">
                    {markdownContent.length} characters
                  </span>
                  {markdownContent.length > 100 && (
                    <span className="text-xs text-green-600">✓ Ready to parse</span>
                  )}
                </div>
              </div>
              
              {parseError && (
                <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-md">
                  <AlertCircle className="h-4 w-4 text-red-500" />
                  <span className="text-red-700 text-sm">{parseError}</span>
                </div>
              )}
              
              <div className="flex justify-between">
                <Button variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button 
                  onClick={handleParse} 
                  disabled={isParsing || !markdownContent.trim()}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  {isParsing ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Parsing...
                    </>
                  ) : (
                    <>
                      <FileText className="h-4 w-4 mr-2" />
                      Parse & Import
                    </>
                  )}
                </Button>
              </div>
            </div>
          ) : (
            // Step 2: Review parsed content
            <div className="space-y-6">
              {/* Header with progress */}
              <div className="bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <Badge variant={parsedPRD.prd_type === 'agent' ? 'default' : 'secondary'} className="text-sm">
                      {parsedPRD.prd_type === 'agent' ? (
                        <>
                          <Bot className="h-3 w-3 mr-1" />
                          Agent PRD
                        </>
                      ) : (
                        <>
                          <Building className="h-3 w-3 mr-1" />
                          Platform PRD
                        </>
                      )}
                    </Badge>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium">Completion:</span>
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${getCompletionPercentage(parsedPRD)}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-bold text-blue-600">
                        {getCompletionPercentage(parsedPRD)}%
                      </span>
                    </div>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => setParsedPRD(null)}>
                    Parse Again
                  </Button>
                </div>
                <p className="text-sm text-muted-foreground">
                  ✅ Successfully parsed your PRD! Review the extracted content below.
                </p>
              </div>

              {/* Parsed Content Preview */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg flex items-center gap-2">
                    <FileText className="h-5 w-5" />
                    Extracted Content
                  </h3>
                  
                  {parsedPRD.title && (
                    <div className="bg-white border rounded-lg p-3">
                      <label className={`text-sm font-medium flex items-center gap-2 ${parsedPRD.title.includes('to be') ? 'text-orange-600' : 'text-green-600'}`}>
                        {parsedPRD.title.includes('to be') ? '⚠️' : '✅'} Title
                      </label>
                      <p className="text-sm text-muted-foreground mt-1">{parsedPRD.title}</p>
                    </div>
                  )}
                  
                  {parsedPRD.description && (
                    <div className="bg-white border rounded-lg p-3">
                      <label className={`text-sm font-medium flex items-center gap-2 ${parsedPRD.description.includes('to be') ? 'text-orange-600' : 'text-green-600'}`}>
                        {parsedPRD.description.includes('to be') ? '⚠️' : '✅'} Description
                      </label>
                      <p className="text-sm text-muted-foreground mt-1">{parsedPRD.description}</p>
                    </div>
                  )}
                  
                  {parsedPRD.problem_statement && (
                    <div className="bg-white border rounded-lg p-3">
                      <label className={`text-sm font-medium flex items-center gap-2 ${parsedPRD.problem_statement.includes('to be') ? 'text-orange-600' : 'text-green-600'}`}>
                        {parsedPRD.problem_statement.includes('to be') ? '⚠️' : '✅'} Problem Statement
                      </label>
                      <p className="text-sm text-muted-foreground mt-1">{parsedPRD.problem_statement}</p>
                    </div>
                  )}
                  
                  {parsedPRD.target_users && parsedPRD.target_users.length > 0 && (
                    <div className="bg-white border rounded-lg p-3">
                      <label className={`text-sm font-medium flex items-center gap-2 ${parsedPRD.target_users[0].includes('to be') ? 'text-orange-600' : 'text-green-600'}`}>
                        {parsedPRD.target_users[0].includes('to be') ? '⚠️' : '✅'} Target Users
                      </label>
                      <ul className="text-sm text-muted-foreground list-disc list-inside mt-1">
                        {parsedPRD.target_users.map((user, i) => (
                          <li key={i}>{user}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
                
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg flex items-center gap-2">
                    <CheckCircle className="h-5 w-5" />
                    Next Steps
                  </h3>
                  
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-center gap-2 text-green-600 mb-2">
                      <CheckCircle className="h-4 w-4" />
                      <span className="font-medium">Ready for Review</span>
                    </div>
                    <p className="text-sm text-green-700">
                      Your PRD has been successfully parsed and is ready for agent creation.
                    </p>
                  </div>
                  
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex items-center gap-2 text-blue-600 mb-2">
                      <MessageSquare className="h-4 w-4" />
                      <span className="font-medium">Conversational Review</span>
                    </div>
                    <p className="text-sm text-blue-700">
                      Our AI will generate your agent based on the PRD specifications.
                    </p>
                  </div>
                  
                  {getMissingSections(parsedPRD).length > 0 && (
                    <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                      <div className="flex items-center gap-2 text-orange-600 mb-2">
                        <AlertCircle className="h-4 w-4" />
                        <span className="font-medium">Sections to Complete</span>
                      </div>
                      <p className="text-sm text-orange-700 mb-2">
                        These sections may need attention before agent creation:
                      </p>
                      <ul className="text-xs text-orange-600 list-disc list-inside">
                        {getMissingSections(parsedPRD).slice(0, 3).map((section, i) => (
                          <li key={i}>{section.replace('_', ' ')}</li>
                        ))}
                        {getMissingSections(parsedPRD).length > 3 && (
                          <li>...and {getMissingSections(parsedPRD).length - 3} more</li>
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              </div>

              {parseError && (
                <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-md">
                  <AlertCircle className="h-4 w-4 text-red-500" />
                  <span className="text-red-700 text-sm">{parseError}</span>
                </div>
              )}

              <div className="flex justify-between items-center pt-4 border-t">
                <Button variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button 
                  onClick={handleSubmit} 
                  disabled={isSubmitting}
                  className="bg-green-600 hover:bg-green-700 text-white"
                  size="lg"
                >
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Creating Agent...
                    </>
                  ) : (
                    <>
                      <Bot className="h-4 w-4 mr-2" />
                      Create Agent
                    </>
                  )}
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Conversational Review Interface */}
      {showConversationalReview && prdId && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl h-[80vh] flex flex-col">
            <div className="flex items-center justify-between p-6 border-b">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <MessageSquare className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold">Create Your AI Agent</h2>
                  <p className="text-gray-600">Let's create your AI agent based on your PRD specifications</p>
                </div>
              </div>
              <Button variant="outline" onClick={() => {
                setShowConversationalReview(false)
                onSuccess(prdId)
                onClose()
              }}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="flex-1 overflow-hidden">
              <PRDChatbot 
                prdId={prdId}
                onClose={() => {
                  setShowConversationalReview(false)
                  onSuccess(prdId)
                  onClose()
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
