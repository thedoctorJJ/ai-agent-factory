'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ChevronDown, ChevronUp, Download, Trash2, Eye } from 'lucide-react'

interface PRD {
  id: string
  title: string
  description: string
  prd_type?: 'platform' | 'agent'
  status: string
  created_at: string
  requirements?: string[]
}

interface PRDStatusSectionProps {
  status: string
  prds: PRD[]
  isExpanded: boolean
  onToggle: () => void
  onDelete: (prdId: string) => void
  onDownload: (prdId: string, title: string) => void
  onApprove?: (prdId: string) => void
  onRequestChanges?: (prdId: string, feedback: string) => void
  onReject?: (prdId: string) => void
  generateAgentDescription: (prd: PRD) => string
}

export default function PRDStatusSection({
  status,
  prds,
  isExpanded,
  onToggle,
  onDelete,
  onDownload,
  onApprove,
  onRequestChanges,
  onReject,
  generateAgentDescription
}: PRDStatusSectionProps) {
  const getStatusConfig = (status: string) => {
    const statusConfig = {
      uploaded: { 
        label: 'Uploaded', 
        variant: 'secondary' as const, 
        icon: '📤',
        colorClass: 'bg-purple-50 hover:bg-purple-100 border-purple-200 text-purple-800',
        badgeClass: 'bg-purple-100 text-purple-800',
        description: 'Uploaded and awaiting standardization'
      },
      standardizing: { 
        label: 'Standardizing', 
        variant: 'secondary' as const, 
        icon: '🔧',
        colorClass: 'bg-orange-50 hover:bg-orange-100 border-orange-200 text-orange-800',
        badgeClass: 'bg-orange-100 text-orange-800',
        description: 'Being converted to AI Agent Factory format'
      },
      review: { 
        label: 'Review', 
        variant: 'secondary' as const, 
        icon: '👀',
        colorClass: 'bg-indigo-50 hover:bg-indigo-100 border-indigo-200 text-indigo-800',
        badgeClass: 'bg-indigo-100 text-indigo-800',
        description: 'Awaiting user review and approval'
      },
      queue: { 
        label: 'Queue', 
        variant: 'secondary' as const, 
        icon: '⏳',
        colorClass: 'bg-yellow-50 hover:bg-yellow-100 border-yellow-200 text-yellow-800',
        badgeClass: 'bg-yellow-100 text-yellow-800',
        description: 'Approved and waiting to be processed into an AI agent'
      },
      in_progress: { 
        label: 'In Progress', 
        variant: 'default' as const, 
        icon: '🔄',
        colorClass: 'bg-blue-50 hover:bg-blue-100 border-blue-200 text-blue-800',
        badgeClass: 'bg-blue-100 text-blue-800',
        description: 'Currently being processed by Devin AI'
      },
      completed: { 
        label: 'Completed', 
        variant: 'default' as const, 
        icon: '✅',
        colorClass: 'bg-green-50 hover:bg-green-100 border-green-200 text-green-800',
        badgeClass: 'bg-green-100 text-green-800',
        description: 'Successfully processed and agent deployed'
      },
      failed: { 
        label: 'Failed', 
        variant: 'destructive' as const, 
        icon: '❌',
        colorClass: 'bg-red-50 hover:bg-red-100 border-red-200 text-red-800',
        badgeClass: 'bg-red-100 text-red-800',
        description: 'Processing failed - needs review'
      },
      processed: { 
        label: 'Processed', 
        variant: 'outline' as const, 
        icon: '📋',
        colorClass: 'bg-gray-50 hover:bg-gray-100 border-gray-200 text-gray-800',
        badgeClass: 'bg-gray-100 text-gray-800',
        description: 'Processed into deployed AI agent'
      }
    }
    
    return statusConfig[status as keyof typeof statusConfig] || { 
      label: status, 
      variant: 'secondary' as const, 
      icon: '❓',
      colorClass: 'bg-gray-50 hover:bg-gray-100 border-gray-200 text-gray-800',
      badgeClass: 'bg-gray-100 text-gray-800',
      description: 'Unknown status'
    }
  }

  const config = getStatusConfig(status)

  return (
    <div className="space-y-4">
      <Button
        variant="ghost"
        onClick={onToggle}
        className={`w-full justify-between p-4 h-auto ${config.colorClass} border rounded-lg transition-colors`}
      >
        <div className="flex items-center gap-2">
          <span className="text-lg">{config.icon}</span>
          <h3 className="text-lg font-semibold">{config.label}</h3>
          <Badge variant="secondary" className="bg-white/50">
            {prds.length}
          </Badge>
        </div>
        {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
      </Button>
      
      {isExpanded && (
        <div className="grid gap-4">
          {prds.length > 0 ? (
            prds.map((prd) => (
              <Card key={prd.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="space-y-1 flex-1">
                      <CardTitle className="text-lg">{prd.title}</CardTitle>
                      <div className="space-y-2">
                        {status === 'queue' && (
                          <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                            <p className="text-sm font-medium text-blue-800 mb-1">🤖 Agent Description:</p>
                            <p className="text-sm text-blue-700">{generateAgentDescription(prd)}</p>
                          </div>
                        )}
                        <div className={`p-2 rounded-lg border ${config.badgeClass.replace('bg-', 'bg-').replace('text-', 'text-')}`}>
                          <p className="text-xs">{config.icon} {config.description}</p>
                        </div>
                        {prd.description && prd.description !== generateAgentDescription(prd) && (
                          <CardDescription className="text-xs text-muted-foreground">
                            Full PRD: {prd.description}
                          </CardDescription>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 ml-4">
                      <Badge className={config.badgeClass}>
                        {config.icon} {config.label}
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        {prd.prd_type || 'agent'}
                      </Badge>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => window.location.href = `/prds/${prd.id}`}
                      >
                        <Eye className="h-4 w-4 mr-2" />
                        View
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onDownload(prd.id, prd.title)}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        <Download className="h-4 w-4" />
                      </Button>
                      {status === 'review' && (
                        <>
                          <Button
                            variant="default"
                            size="sm"
                            onClick={() => onApprove?.(prd.id)}
                            className="bg-green-600 hover:bg-green-700 text-white"
                          >
                            ✅ Approve
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              const feedback = prompt('Please provide feedback for changes needed:')
                              if (feedback) {
                                onRequestChanges?.(prd.id, feedback)
                              }
                            }}
                            className="border-orange-300 text-orange-600 hover:bg-orange-50"
                          >
                            🔄 Request Changes
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => onReject?.(prd.id)}
                            className="border-red-300 text-red-600 hover:bg-red-50"
                          >
                            ❌ Reject
                          </Button>
                        </>
                      )}
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onDelete(prd.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            ))
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              <p>No PRDs in {config.label.toLowerCase()}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
