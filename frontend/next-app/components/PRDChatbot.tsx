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
        let welcomeContent = `Hi! I'm here to help you create your AI agent from your PRD: **${prd.title}**\n\n`
        
        // For well-structured PRDs, provide agent creation analysis
        if (completion.completion_percentage > 60) {
          welcomeContent += `I can see you have a well-structured PRD at ${completion.completion_percentage}% completion. Let me analyze what you have and guide you through agent creation.\n\n`
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
          
          welcomeContent += `\n**🔍 Areas to Review for Agent Creation:**\n`
          
          if (!prd.target_users || prd.target_users.length === 0) {
            welcomeContent += `- Target Users - Could be more explicit about primary users\n`
          }
          if (!prd.acceptance_criteria || prd.acceptance_criteria.length === 0) {
            welcomeContent += `- Acceptance Criteria - Could add specific testable criteria for each feature\n`
          }
          if (!prd.timeline || prd.timeline.trim() === "") {
            welcomeContent += `- Timeline - No specific dates or milestones mentioned\n`
          }
          
          welcomeContent += `\n**Ready to create your agent? What would you like to focus on first?**`
        } else if (completion.completion_percentage === 0) {
          welcomeContent += `I can see this is a fresh PRD. Let's start from the beginning and build this out together for agent creation.\n\nWhat problem are you trying to solve with this agent?`
        } else if (completion.completion_percentage < 50) {
          welcomeContent += `I can see you're at ${completion.completion_percentage}% completion. We have a good start! Let's continue building this out for agent creation.\n\nWhat would you like to work on next?`
        } else {
          welcomeContent += `Great progress! You're at ${completion.completion_percentage}% completion. We're almost ready for agent creation!\n\nWhat's the next section you'd like to focus on?`
        }

        const welcomeMessage: ChatMessage = {
          id: 'welcome',
          type: 'assistant',
          content: welcomeContent,
          suggestions: completion.missing_sections && completion.missing_sections.length > 0 ? [
            `Work on ${completion.missing_sections[0].replace('_', ' ').replace(' (optional)', '')}`,
            "Tell me about the problem this agent solves",
            "Who are the target users for this agent?",
            "What are the main agent requirements?",
            "How will we measure agent success?",
            "Start agent generation process"
          ] : [
            "Review the agent problem statement",
            "Add more user stories for the agent", 
            "Refine the agent requirements",
            "Update the agent timeline",
            "Start agent generation process"
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

        // Check if PRD is ready for agent creation
        if (data.completion_percentage >= 80) {
          setTimeout(() => {
            const completeMessage: ChatMessage = {
              id: 'complete',
              type: 'system',
              content: '🎉 Congratulations! Your PRD is ready for agent creation. Let\'s generate your AI agent!',
              suggestions: ['Start agent generation', 'Review agent specifications', 'Configure deployment settings'],
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
      <Card className="w-full max-w-5xl h-[85vh] flex flex-col shadow-2xl">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4 border-b bg-gradient-to-r from-blue-50 to-green-50">
          <div>
            <CardTitle className="flex items-center gap-2 text-xl">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <Bot className="h-5 w-5 text-blue-600" />
              </div>
              PRD Completion Assistant
            </CardTitle>
            <CardDescription className="text-base">
              Let's complete your PRD together through conversation
            </CardDescription>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3 bg-white rounded-lg px-3 py-2 shadow-sm">
              <span className="text-sm font-medium text-gray-700">Progress:</span>
              <div className="w-32 bg-gray-200 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${completionPercentage}%` }}
                ></div>
              </div>
              <span className="text-sm font-bold text-blue-600 min-w-[3rem]">{completionPercentage}%</span>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose} className="hover:bg-white/50">
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
                    className={`p-4 rounded-2xl shadow-sm ${
                      message.type === 'user'
                        ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white ml-auto'
                        : message.type === 'assistant'
                        ? 'bg-white border border-gray-200 text-gray-900'
                        : 'bg-gradient-to-r from-yellow-50 to-orange-50 text-yellow-800 border border-yellow-200'
                    }`}
                  >
                    <div
                      className="prose prose-sm max-w-none"
                      dangerouslySetInnerHTML={{
                        __html: formatMessage(message.content)
                      }}
                    />
                  </div>
                  
                  {message.suggestions && message.suggestions.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {message.suggestions.map((suggestion, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={() => handleSuggestionClick(suggestion)}
                          className="text-xs h-auto py-2 px-3 bg-white hover:bg-blue-50 border-blue-200 text-blue-700 hover:text-blue-800 transition-colors"
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
          <div className="border-t p-4 bg-gradient-to-r from-gray-50 to-blue-50">
            <div className="flex gap-3">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage(inputValue)}
                  placeholder="Type your response or ask a question..."
                  className="w-full p-4 pr-12 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white shadow-sm"
                  disabled={isLoading}
                  autoFocus
                />
                {inputValue.length > 0 && (
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  </div>
                )}
              </div>
              <Button
                onClick={() => sendMessage(inputValue)}
                disabled={!inputValue.trim() || isLoading}
                size="lg"
                className="px-6 bg-blue-600 hover:bg-blue-700 text-white shadow-lg"
              >
                {isLoading ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                ) : (
                  <Send className="h-4 w-4" />
                )}
              </Button>
            </div>
            
            {completionPercentage >= 80 && (
              <div className="mt-3 flex justify-end">
                <Button onClick={onComplete} className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4" />
                  Create Agent
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
