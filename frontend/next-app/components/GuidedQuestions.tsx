'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { X, CheckCircle, ArrowRight, ArrowLeft, FileText } from 'lucide-react'

interface Question {
  section: string
  is_optional: boolean
  question: string
  sub_questions: string[]
  example: string
}

interface GuidedQuestionsProps {
  prdId: string
  onClose: () => void
  onComplete: () => void
}

export default function GuidedQuestions({ prdId, onClose, onComplete }: GuidedQuestionsProps) {
  const [questions, setQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [completionPercentage, setCompletionPercentage] = useState(0)

  useEffect(() => {
    fetchQuestions()
  }, [prdId])

  const fetchQuestions = async () => {
    try {
      const response = await fetch(`/api/v1/prds/${prdId}/guided-questions`)
      if (response.ok) {
        const data = await response.json()
        setQuestions(data.questions || [])
        setCompletionPercentage(data.completion_percentage || 0)
      }
    } catch (error) {
      console.error('Error fetching questions:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleAnswer = async (section: string, answer: string) => {
    setAnswers(prev => ({ ...prev, [section]: answer }))
    
    try {
      const response = await fetch(`/api/v1/prds/${prdId}/answer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          section,
          content: answer,
        }),
      })

      if (response.ok) {
        // Move to next question
        if (currentQuestionIndex < questions.length - 1) {
          setCurrentQuestionIndex(prev => prev + 1)
        } else {
          // All questions answered
          onComplete()
        }
      } else {
        console.error('Error submitting answer')
      }
    } catch (error) {
      console.error('Error submitting answer:', error)
    }
  }

  const handleSkip = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1)
    } else {
      onComplete()
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1)
    }
  }

  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <Card className="w-full max-w-2xl">
          <CardContent className="p-6 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p>Loading guided questions...</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (questions.length === 0) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <Card className="w-full max-w-2xl">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-500" />
              PRD Complete!
            </CardTitle>
            <CardDescription>
              Your PRD is already complete with {completionPercentage}% completion.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={onClose} className="w-full">
              Close
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const currentQuestion = questions[currentQuestionIndex]
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <div>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Complete Your PRD
            </CardTitle>
            <CardDescription>
              Question {currentQuestionIndex + 1} of {questions.length} • {completionPercentage}% complete
            </CardDescription>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>

          {/* Current Question */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <Badge variant={currentQuestion.is_optional ? 'secondary' : 'default'}>
                {currentQuestion.is_optional ? 'Optional' : 'Required'}
              </Badge>
              <span className="text-sm font-medium capitalize">
                {currentQuestion.section.replace('_', ' ')}
              </span>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-3">
                {currentQuestion.question}
              </h3>
              
              {currentQuestion.sub_questions.length > 0 && (
                <div className="mb-4">
                  <p className="text-sm font-medium mb-2">Consider these points:</p>
                  <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                    {currentQuestion.sub_questions.map((subQ, i) => (
                      <li key={i}>{subQ}</li>
                    ))}
                  </ul>
                </div>
              )}

              {currentQuestion.example && (
                <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
                  <p className="text-sm font-medium text-blue-800 mb-1">Example:</p>
                  <p className="text-sm text-blue-700">{currentQuestion.example}</p>
                </div>
              )}
            </div>

            {/* Answer Input */}
            <div>
              <textarea
                value={answers[currentQuestion.section] || ''}
                onChange={(e) => setAnswers(prev => ({ ...prev, [currentQuestion.section]: e.target.value }))}
                className="w-full p-3 border rounded-md h-32"
                placeholder="Enter your answer here..."
              />
            </div>
          </div>

          {/* Navigation */}
          <div className="flex justify-between items-center pt-4 border-t">
            <Button 
              variant="outline" 
              onClick={handlePrevious}
              disabled={currentQuestionIndex === 0}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Previous
            </Button>

            <div className="flex gap-2">
              {currentQuestion.is_optional && (
                <Button variant="ghost" onClick={handleSkip}>
                  Skip
                </Button>
              )}
              
              <Button 
                onClick={() => handleAnswer(currentQuestion.section, answers[currentQuestion.section] || '')}
                disabled={!answers[currentQuestion.section]?.trim()}
              >
                {currentQuestionIndex === questions.length - 1 ? 'Complete PRD' : 'Next'}
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
