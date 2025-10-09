'use client'

import React, { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { X, Send, Bot, User, Lightbulb, CheckCircle, ArrowRight } from 'lucide-react'

interface ChatMessage {
  id: string
  type: 'user' | 'assistant' | 'system'
  content: string
  suggestions?: string[]
  timestamp: Date
}

interface PRDChatbotProps {
  prdId: string
  onClose: () => void
  onComplete: () => void
}

export default function PRDChatbot({ prdId, onClose, onComplete }: PRDChatbotProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentSection, setCurrentSection] = useState<string | null>(null)
  const [completionPercentage, setCompletionPercentage] = useState(0)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    initializeChat()
  }, [prdId])

  const initializeChat = async () => {
    try {
      // Get PRD details and current completion status
      const [prdRes, completionRes] = await Promise.all([
        fetch(`/api/v1/prds/${prdId}`),
        fetch(`/api/v1/prds/${prdId}/completion`)
      ])

      if (prdRes.ok && completionRes.ok) {
        const prd = await prdRes.json()
        const completion = await completionRes.json()
        
        setCompletionPercentage(completion.completion_percentage || 0)
        
        // Start with a welcoming message and context
        let welcomeContent = `Hi! I'm here to help you complete your PRD: **${prd.title}**\n\n`
        
        // For well-structured PRDs, provide analysis
        if (completion.completion_percentage > 60) {
          welcomeContent += `I can see you have a well-structured PRD at ${completion.completion_percentage}% completion. Let me analyze what you have so far and suggest improvements.\n\n`
          welcomeContent += `**✅ Strong Sections:**\n`
          
          if (prd.problem_statement && prd.problem_statement.length > 50) {
            welcomeContent += `- Problem Statement - Clear and specific\n`
          }
          if (prd.success_metrics && prd.success_metrics.length > 0) {
            welcomeContent += `- Success Metrics - Measurable and actionable\n`
          }
          if (prd.user_stories && prd.user_stories.length > 0) {
            welcomeContent += `- User Stories - Well-defined personas and use cases\n`
          }
          if (prd.requirements && prd.requirements.length > 0) {
            welcomeContent += `- Requirements - Detailed and specific\n`
          }
          if (prd.technical_requirements && prd.technical_requirements.length > 0) {
            welcomeContent += `- Technical Requirements - Detailed and specific\n`
          }
          
          welcomeContent += `\n**🔍 Areas We Could Enhance:**\n`
          
          if (!prd.target_users || prd.target_users.length === 0) {
            welcomeContent += `- Target Users - Could be more explicit about primary users\n`
          }
          if (!prd.acceptance_criteria || prd.acceptance_criteria.length === 0) {
            welcomeContent += `- Acceptance Criteria - Could add specific testable criteria for each feature\n`
          }
          if (!prd.timeline || prd.timeline.trim() === "") {
            welcomeContent += `- Timeline - No specific dates or milestones mentioned\n`
          }
          
          welcomeContent += `\n**What would you like to focus on first?**`
        } else if (completion.completion_percentage === 0) {
          welcomeContent += `I can see this is a fresh PRD. Let's start from the beginning and build this out together through conversation.\n\nWhat problem are you trying to solve with this agent?`
        } else if (completion.completion_percentage < 50) {
          welcomeContent += `I can see you're at ${completion.completion_percentage}% completion. We have a good start! Let's continue building this out.\n\nWhat would you like to work on next?`
        } else {
          welcomeContent += `Great progress! You're at ${completion.completion_percentage}% completion. We're almost there!\n\nWhat's the next section you'd like to focus on?`
        }

        const welcomeMessage: ChatMessage = {
          id: 'welcome',
          type: 'assistant',
          content: welcomeContent,
          suggestions: completion.missing_sections && completion.missing_sections.length > 0 ? [
            `Work on ${completion.missing_sections[0].replace('_', ' ').replace(' (optional)', '')}`,
            "Tell me about the problem this solves",
            "Who are the target users?",
            "What are the main requirements?",
            "How will we measure success?"
          ] : [
            "Review the problem statement",
            "Add more user stories", 
            "Refine the requirements",
            "Update the timeline"
          ],
          timestamp: new Date()
        }

        setMessages([welcomeMessage])
      }
    } catch (error) {
      console.error('Error initializing chat:', error)
      const errorMessage: ChatMessage = {
        id: 'error',
        type: 'system',
        content: 'Sorry, I had trouble loading your PRD. Please try again.',
        timestamp: new Date()
      }
      setMessages([errorMessage])
    }
  }

  const sendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: content.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      // Analyze the user's input and determine what section they're working on
      const response = await fetch(`/api/v1/prds/${prdId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          context: {
            current_section: currentSection,
            completion_percentage: completionPercentage,
            recent_messages: messages.slice(-3).map(m => ({ type: m.type, content: m.content }))
          }
        }),
      })

      if (response.ok) {
        const data = await response.json()
        
        const assistantMessage: ChatMessage = {
          id: `assistant-${Date.now()}`,
          type: 'assistant',
          content: data.response,
          suggestions: data.suggestions || [],
          timestamp: new Date()
        }

        setMessages(prev => [...prev, assistantMessage])
        
        if (data.updated_section) {
          setCurrentSection(data.updated_section)
        }
        
        if (data.completion_percentage) {
          setCompletionPercentage(data.completion_percentage)
        }

        // Check if PRD is complete
        if (data.completion_percentage >= 100) {
          setTimeout(() => {
            const completeMessage: ChatMessage = {
              id: 'complete',
              type: 'system',
              content: '🎉 Congratulations! Your PRD is now complete and ready for agent creation.',
              suggestions: ['View the completed PRD', 'Start creating the agent', 'Export as markdown'],
              timestamp: new Date()
            }
            setMessages(prev => [...prev, completeMessage])
          }, 1000)
        }
      } else {
        // Fallback to a simple response if the API isn't available
        const fallbackMessage: ChatMessage = {
          id: `assistant-${Date.now()}`,
          type: 'assistant',
          content: `Thanks for that input! I understand you're working on: "${content}"\n\nLet me help you think through this. Can you tell me more about the specific details or context around this?`,
          suggestions: [
            "Can you provide more details?",
            "What's the main goal here?",
            "Who would benefit from this?",
            "What are the key requirements?"
          ],
          timestamp: new Date()
        }
        setMessages(prev => [...prev, fallbackMessage])
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'system',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion)
  }

  const formatMessage = (content: string) => {
    // Simple markdown-like formatting
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>')
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-4xl h-[80vh] flex flex-col">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4 border-b">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-5 w-5" />
              PRD Completion Assistant
            </CardTitle>
            <CardDescription>
              Let's complete your PRD together through conversation
            </CardDescription>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">Progress:</span>
              <div className="w-24 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${completionPercentage}%` }}
                ></div>
              </div>
              <span className="text-sm font-medium">{completionPercentage}%</span>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 flex flex-col p-0">
          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.type !== 'user' && (
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    message.type === 'assistant' ? 'bg-blue-100' : 'bg-gray-100'
                  }`}>
                    {message.type === 'assistant' ? (
                      <Bot className="h-4 w-4 text-blue-600" />
                    ) : (
                      <CheckCircle className="h-4 w-4 text-gray-600" />
                    )}
                  </div>
                )}
                
                <div className={`max-w-[80%] ${
                  message.type === 'user' ? 'order-first' : ''
                }`}>
                  <div
                    className={`p-3 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-blue-600 text-white'
                        : message.type === 'assistant'
                        ? 'bg-gray-100 text-gray-900'
                        : 'bg-yellow-50 text-yellow-800 border border-yellow-200'
                    }`}
                  >
                    <div
                      dangerouslySetInnerHTML={{
                        __html: formatMessage(message.content)
                      }}
                    />
                  </div>
                  
                  {message.suggestions && message.suggestions.length > 0 && (
                    <div className="mt-2 space-y-1">
                      {message.suggestions.map((suggestion, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={() => handleSuggestionClick(suggestion)}
                          className="text-xs h-auto py-1 px-2 mr-2 mb-1"
                        >
                          <Lightbulb className="h-3 w-3 mr-1" />
                          {suggestion}
                        </Button>
                      ))}
                    </div>
                  )}
                  
                  <div className="text-xs text-muted-foreground mt-1">
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
                
                {message.type === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
                    <User className="h-4 w-4 text-white" />
                  </div>
                )}
              </div>
            ))}
            
            {isLoading && (
              <div className="flex gap-3 justify-start">
                <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                  <Bot className="h-4 w-4 text-blue-600" />
                </div>
                <div className="bg-gray-100 p-3 rounded-lg">
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                    <span className="text-sm text-gray-600">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
          
          {/* Input Area */}
          <div className="border-t p-4 bg-white">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage(inputValue)}
                placeholder="Type your response or ask a question..."
                className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
                autoFocus
              />
              <Button
                onClick={() => sendMessage(inputValue)}
                disabled={!inputValue.trim() || isLoading}
                size="sm"
                className="px-4"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
            
            {completionPercentage >= 100 && (
              <div className="mt-3 flex justify-end">
                <Button onClick={onComplete} className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4" />
                  Complete & Close
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
