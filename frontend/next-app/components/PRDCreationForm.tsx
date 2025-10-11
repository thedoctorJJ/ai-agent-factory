'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { X, Plus, FileText, Bot, Building } from 'lucide-react'

interface PRDCreationFormProps {
  onClose: () => void
  onSuccess: (prdId?: string) => void
}

export default function PRDCreationForm({ onClose, onSuccess }: PRDCreationFormProps) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    problem_statement: '',
    target_users: '',
    user_stories: '',
    requirements: '',
    acceptance_criteria: '',
    technical_requirements: '',
    success_metrics: '',
    timeline: '',
    prd_type: 'agent' as 'agent' | 'platform'
  })
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      // Parse arrays from comma-separated strings
      const targetUsers = formData.target_users.split(',').map(u => u.trim()).filter(u => u)
      const userStories = formData.user_stories.split('\n').filter(s => s.trim())
      const requirements = formData.requirements.split('\n').filter(r => r.trim())
      const acceptanceCriteria = formData.acceptance_criteria.split('\n').filter(c => c.trim())
      const successMetrics = formData.success_metrics.split('\n').filter(m => m.trim())

      const prdData = {
        title: formData.title,
        description: formData.description,
        problem_statement: formData.problem_statement,
        target_users: targetUsers,
        user_stories: userStories,
        requirements: requirements,
        acceptance_criteria: acceptanceCriteria,
        technical_requirements: formData.technical_requirements,
        success_metrics: successMetrics,
        timeline: formData.timeline,
        prd_type: formData.prd_type
      }

      const response = await fetch('/api/v1/prds', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(prdData),
      })

      if (response.ok) {
        const newPRD = await response.json()
        console.log('PRD created successfully:', newPRD)
        onSuccess(newPRD.id)
        onClose()
      } else {
        const error = await response.text()
        console.error('Error creating PRD:', error)
        alert('Error creating PRD. Please check the console for details.')
      }
    } catch (error) {
      console.error('Error creating PRD:', error)
      alert('Error creating PRD. Please check the console for details.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <div>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Enter Completed PRD
            </CardTitle>
            <CardDescription>
              Enter your completed, formatted Product Requirements Document for agent creation
            </CardDescription>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>
        
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* PRD Type Selection */}
            <div className="flex gap-4">
              <Button
                type="button"
                variant={formData.prd_type === 'agent' ? 'default' : 'outline'}
                onClick={() => setFormData(prev => ({ ...prev, prd_type: 'agent' }))}
                className="flex items-center gap-2"
              >
                <Bot className="h-4 w-4" />
                Agent PRD
              </Button>
              <Button
                type="button"
                variant={formData.prd_type === 'platform' ? 'default' : 'outline'}
                onClick={() => setFormData(prev => ({ ...prev, prd_type: 'platform' }))}
                className="flex items-center gap-2"
              >
                <Building className="h-4 w-4" />
                Platform PRD
              </Button>
            </div>

            {/* Title */}
            <div>
              <label className="block text-sm font-medium mb-2">Title *</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                className="w-full p-2 border rounded-md"
                placeholder="Enter PRD title"
                required
              />
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium mb-2">Description *</label>
              <textarea
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                className="w-full p-2 border rounded-md h-20"
                placeholder="Brief description of the project"
                required
              />
            </div>

            {/* Problem Statement */}
            <div>
              <label className="block text-sm font-medium mb-2">Problem Statement *</label>
              <textarea
                value={formData.problem_statement}
                onChange={(e) => handleInputChange('problem_statement', e.target.value)}
                className="w-full p-2 border rounded-md h-24"
                placeholder="What problem does this solve?"
                required
              />
            </div>

            {/* Target Users */}
            <div>
              <label className="block text-sm font-medium mb-2">Target Users *</label>
              <input
                type="text"
                value={formData.target_users}
                onChange={(e) => handleInputChange('target_users', e.target.value)}
                className="w-full p-2 border rounded-md"
                placeholder="Comma-separated list of target users"
                required
              />
            </div>

            {/* User Stories */}
            <div>
              <label className="block text-sm font-medium mb-2">User Stories *</label>
              <textarea
                value={formData.user_stories}
                onChange={(e) => handleInputChange('user_stories', e.target.value)}
                className="w-full p-2 border rounded-md h-24"
                placeholder="One user story per line (As a user, I want...)"
                required
              />
            </div>

            {/* Requirements */}
            <div>
              <label className="block text-sm font-medium mb-2">Requirements *</label>
              <textarea
                value={formData.requirements}
                onChange={(e) => handleInputChange('requirements', e.target.value)}
                className="w-full p-2 border rounded-md h-24"
                placeholder="One requirement per line"
                required
              />
            </div>

            {/* Acceptance Criteria */}
            <div>
              <label className="block text-sm font-medium mb-2">Acceptance Criteria *</label>
              <textarea
                value={formData.acceptance_criteria}
                onChange={(e) => handleInputChange('acceptance_criteria', e.target.value)}
                className="w-full p-2 border rounded-md h-24"
                placeholder="One criterion per line"
                required
              />
            </div>

            {/* Technical Requirements */}
            <div>
              <label className="block text-sm font-medium mb-2">Technical Requirements *</label>
              <textarea
                value={formData.technical_requirements}
                onChange={(e) => handleInputChange('technical_requirements', e.target.value)}
                className="w-full p-2 border rounded-md h-24"
                placeholder="Technical specifications and constraints"
                required
              />
            </div>

            {/* Success Metrics */}
            <div>
              <label className="block text-sm font-medium mb-2">Success Metrics *</label>
              <textarea
                value={formData.success_metrics}
                onChange={(e) => handleInputChange('success_metrics', e.target.value)}
                className="w-full p-2 border rounded-md h-24"
                placeholder="How will you measure success?"
                required
              />
            </div>

            {/* Timeline */}
            <div>
              <label className="block text-sm font-medium mb-2">Timeline *</label>
              <input
                type="text"
                value={formData.timeline}
                onChange={(e) => handleInputChange('timeline', e.target.value)}
                className="w-full p-2 border rounded-md"
                placeholder="e.g., 2-3 weeks, Q1 2024, etc."
                required
              />
            </div>

            {/* Submit Button */}
            <div className="flex justify-end gap-3 pt-4">
              <Button type="button" variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Submitting...' : 'Submit PRD'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
