'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { X, Upload, FileText, Bot, Building, CheckCircle, AlertCircle } from 'lucide-react'

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
        onSuccess(newPRD.id)
        onClose()
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
              Import PRD from Markdown
            </CardTitle>
            <CardDescription>
              Paste your markdown PRD and we'll parse it automatically, then guide you through any missing sections
            </CardDescription>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {!parsedPRD ? (
            // Step 1: Paste markdown
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Paste your markdown PRD:</label>
                <textarea
                  value={markdownContent}
                  onChange={(e) => setMarkdownContent(e.target.value)}
                  className="w-full p-3 border rounded-md h-96 font-mono text-sm"
                  placeholder="Paste your markdown PRD here..."
                />
              </div>
              
              {parseError && (
                <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-md">
                  <AlertCircle className="h-4 w-4 text-red-500" />
                  <span className="text-red-700 text-sm">{parseError}</span>
                </div>
              )}
              
              <div className="flex justify-end">
                <Button onClick={handleParse} disabled={isParsing || !markdownContent.trim()}>
                  {isParsing ? 'Parsing...' : 'Parse & Import'}
                </Button>
              </div>
            </div>
          ) : (
            // Step 2: Review parsed content
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Badge variant={parsedPRD.prd_type === 'agent' ? 'default' : 'secondary'}>
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
                  <span className="text-sm text-muted-foreground">
                    Completion: {getCompletionPercentage(parsedPRD)}%
                  </span>
                </div>
                <Button variant="outline" onClick={() => setParsedPRD(null)}>
                  Parse Again
                </Button>
              </div>

              {/* Parsed Content Preview */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-4">
                  <h3 className="font-semibold">Parsed Content:</h3>
                  
                  {parsedPRD.title && (
                    <div>
                      <label className={`text-sm font-medium ${parsedPRD.title.includes('to be') ? 'text-orange-600' : 'text-green-600'}`}>
                        {parsedPRD.title.includes('to be') ? '⚠️' : '✓'} Title
                      </label>
                      <p className="text-sm text-muted-foreground">{parsedPRD.title}</p>
                    </div>
                  )}
                  
                  {parsedPRD.description && (
                    <div>
                      <label className={`text-sm font-medium ${parsedPRD.description.includes('to be') ? 'text-orange-600' : 'text-green-600'}`}>
                        {parsedPRD.description.includes('to be') ? '⚠️' : '✓'} Description
                      </label>
                      <p className="text-sm text-muted-foreground">{parsedPRD.description}</p>
                    </div>
                  )}
                  
                  {parsedPRD.problem_statement && (
                    <div>
                      <label className={`text-sm font-medium ${parsedPRD.problem_statement.includes('to be') ? 'text-orange-600' : 'text-green-600'}`}>
                        {parsedPRD.problem_statement.includes('to be') ? '⚠️' : '✓'} Problem Statement
                      </label>
                      <p className="text-sm text-muted-foreground">{parsedPRD.problem_statement}</p>
                    </div>
                  )}
                  
                  {parsedPRD.target_users && parsedPRD.target_users.length > 0 && (
                    <div>
                      <label className={`text-sm font-medium ${parsedPRD.target_users[0].includes('to be') ? 'text-orange-600' : 'text-green-600'}`}>
                        {parsedPRD.target_users[0].includes('to be') ? '⚠️' : '✓'} Target Users
                      </label>
                      <ul className="text-sm text-muted-foreground list-disc list-inside">
                        {parsedPRD.target_users.map((user, i) => (
                          <li key={i}>{user}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
                
                <div className="space-y-4">
                  <h3 className="font-semibold">Status:</h3>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-green-600">
                      <CheckCircle className="h-4 w-4" />
                      <span className="text-sm">All required sections present</span>
                    </div>
                    <div className="flex items-center gap-2 text-orange-600">
                      <AlertCircle className="h-4 w-4" />
                      <span className="text-sm">Some sections need completion</span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Sections marked with ⚠️ contain placeholder content and will be completed through guided questions.
                    </p>
                  </div>
                </div>
              </div>

              {parseError && (
                <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-md">
                  <AlertCircle className="h-4 w-4 text-red-500" />
                  <span className="text-red-700 text-sm">{parseError}</span>
                </div>
              )}

              <div className="flex justify-end gap-3">
                <Button variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button onClick={handleSubmit} disabled={isSubmitting}>
                  {isSubmitting ? 'Creating PRD...' : 'Create PRD & Start Guided Questions'}
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
