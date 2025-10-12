/**
 * Reusable PRD Card component.
 */
import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Eye, Download, Trash2, Edit } from 'lucide-react'
import { PRD, PRDType, PRDStatus } from '@/types'

interface PRDCardProps {
  prd: PRD
  onView?: (prd: PRD) => void
  onEdit?: (prd: PRD) => void
  onDelete?: (prd: PRD) => void
  onDownload?: (prd: PRD) => void
  showActions?: boolean
  className?: string
}

export function PRDCard({
  prd,
  onView,
  onEdit,
  onDelete,
  onDownload,
  showActions = true,
  className = ''
}: PRDCardProps) {
  const getStatusColor = (status: PRDStatus) => {
    switch (status) {
      case PRDStatus.QUEUE:
        return 'bg-yellow-100 text-yellow-800'
      case PRDStatus.PROCESSED:
        return 'bg-green-100 text-green-800'
      case PRDStatus.IN_PROGRESS:
        return 'bg-blue-100 text-blue-800'
      case PRDStatus.COMPLETED:
        return 'bg-purple-100 text-purple-800'
      case PRDStatus.FAILED:
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeColor = (type: PRDType) => {
    switch (type) {
      case PRDType.PLATFORM:
        return 'bg-blue-100 text-blue-800'
      case PRDType.AGENT:
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusIcon = (status: PRDStatus) => {
    switch (status) {
      case PRDStatus.QUEUE:
        return '⏳'
      case PRDStatus.PROCESSED:
        return '✅'
      case PRDStatus.IN_PROGRESS:
        return '🔄'
      case PRDStatus.COMPLETED:
        return '🎉'
      case PRDStatus.FAILED:
        return '❌'
      default:
        return '📄'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const generateAgentDescription = (prd: PRD): string => {
    const requirements = prd.requirements || []
    if (requirements.length === 0) {
      return 'AI agent with general capabilities'
    }
    
    const firstReq = requirements[0].toLowerCase()
    if (firstReq.includes('analyze') || firstReq.includes('analysis')) {
      return 'Data analysis and insights agent'
    } else if (firstReq.includes('chat') || firstReq.includes('conversation')) {
      return 'Conversational AI assistant'
    } else if (firstReq.includes('automate') || firstReq.includes('workflow')) {
      return 'Workflow automation agent'
    } else if (firstReq.includes('monitor') || firstReq.includes('track')) {
      return 'Monitoring and tracking agent'
    } else if (firstReq.includes('generate') || firstReq.includes('create')) {
      return 'Content generation agent'
    } else {
      return 'Specialized AI agent for custom tasks'
    }
  }

  return (
    <Card className={`hover:shadow-md transition-shadow ${className}`}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <CardTitle className="text-lg font-semibold text-gray-900 truncate">
              {prd.title}
            </CardTitle>
            <CardDescription className="mt-1 text-sm text-gray-600 line-clamp-2">
              {prd.description}
            </CardDescription>
          </div>
          <div className="flex flex-col gap-2 ml-4">
            <Badge className={getStatusColor(prd.status)}>
              {getStatusIcon(prd.status)} {prd.status.replace('_', ' ')}
            </Badge>
            <Badge variant="outline" className={getTypeColor(prd.prd_type)}>
              {prd.prd_type}
            </Badge>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-0">
        {/* Agent Description */}
        {prd.status === PRDStatus.PROCESSED && (
          <div className="mb-4 p-3 bg-green-50 rounded-lg border border-green-200">
            <p className="text-sm text-green-800">
              <strong>Agent:</strong> {generateAgentDescription(prd)}
            </p>
          </div>
        )}

        {/* Requirements Preview */}
        {prd.requirements && prd.requirements.length > 0 && (
          <div className="mb-4">
            <p className="text-sm font-medium text-gray-700 mb-2">
              Requirements ({prd.requirements.length}):
            </p>
            <div className="space-y-1">
              {prd.requirements.slice(0, 3).map((req, index) => (
                <p key={index} className="text-sm text-gray-600 line-clamp-1">
                  {index + 1}. {req}
                </p>
              ))}
              {prd.requirements.length > 3 && (
                <p className="text-sm text-gray-500 italic">
                  +{prd.requirements.length - 3} more requirements
                </p>
              )}
            </div>
          </div>
        )}

        {/* Metadata */}
        <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
          <span>Created: {formatDate(prd.created_at)}</span>
          {prd.updated_at !== prd.created_at && (
            <span>Updated: {formatDate(prd.updated_at)}</span>
          )}
        </div>

        {/* Actions */}
        {showActions && (
          <div className="flex gap-2">
            {onView && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onView(prd)}
                className="flex-1"
              >
                <Eye className="h-4 w-4 mr-2" />
                View
              </Button>
            )}
            {onDownload && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onDownload(prd)}
              >
                <Download className="h-4 w-4" />
              </Button>
            )}
            {onEdit && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onEdit(prd)}
              >
                <Edit className="h-4 w-4" />
              </Button>
            )}
            {onDelete && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onDelete(prd)}
                className="text-red-600 hover:text-red-700 hover:bg-red-50"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
