/**
 * Reusable Agent Card component.
 */
import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Eye, ExternalLink, Activity, Trash2, Edit, Github } from 'lucide-react'
import { Agent, AgentStatus, AgentHealthStatus } from '@/types'

interface AgentCardProps {
  agent: Agent
  onView?: (agent: Agent) => void
  onEdit?: (agent: Agent) => void
  onDelete?: (agent: Agent) => void
  onHealthCheck?: (agent: Agent) => void
  showActions?: boolean
  className?: string
}

export function AgentCard({
  agent,
  onView,
  onEdit,
  onDelete,
  onHealthCheck,
  showActions = true,
  className = ''
}: AgentCardProps) {
  const getStatusColor = (status: AgentStatus) => {
    switch (status) {
      case AgentStatus.DEPLOYED:
        return 'bg-green-100 text-green-800'
      case AgentStatus.RUNNING:
        return 'bg-blue-100 text-blue-800'
      case AgentStatus.PENDING:
        return 'bg-yellow-100 text-yellow-800'
      case AgentStatus.STOPPED:
        return 'bg-gray-100 text-gray-800'
      case AgentStatus.FAILED:
        return 'bg-red-100 text-red-800'
      case AgentStatus.MAINTENANCE:
        return 'bg-orange-100 text-orange-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getHealthColor = (health: AgentHealthStatus) => {
    switch (health) {
      case AgentHealthStatus.HEALTHY:
        return 'bg-green-100 text-green-800'
      case AgentHealthStatus.UNHEALTHY:
        return 'bg-red-100 text-red-800'
      case AgentHealthStatus.DEGRADED:
        return 'bg-yellow-100 text-yellow-800'
      case AgentHealthStatus.UNKNOWN:
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusIcon = (status: AgentStatus) => {
    switch (status) {
      case AgentStatus.DEPLOYED:
        return '🚀'
      case AgentStatus.RUNNING:
        return '🟢'
      case AgentStatus.PENDING:
        return '⏳'
      case AgentStatus.STOPPED:
        return '⏸️'
      case AgentStatus.FAILED:
        return '❌'
      case AgentStatus.MAINTENANCE:
        return '🔧'
      default:
        return '🤖'
    }
  }

  const getHealthIcon = (health: AgentHealthStatus) => {
    switch (health) {
      case AgentHealthStatus.HEALTHY:
        return '💚'
      case AgentHealthStatus.UNHEALTHY:
        return '❤️'
      case AgentHealthStatus.DEGRADED:
        return '💛'
      case AgentHealthStatus.UNKNOWN:
        return '❓'
      default:
        return '❓'
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

  const formatUptime = (seconds?: number) => {
    if (!seconds) return 'N/A'
    
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`
    }
    return `${minutes}m`
  }

  return (
    <Card className={`hover:shadow-md transition-shadow ${className}`}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <CardTitle className="text-lg font-semibold text-gray-900 truncate">
              {agent.name}
            </CardTitle>
            <CardDescription className="mt-1 text-sm text-gray-600 line-clamp-2">
              {agent.description}
            </CardDescription>
          </div>
          <div className="flex flex-col gap-2 ml-4">
            <Badge className={getStatusColor(agent.status)}>
              {getStatusIcon(agent.status)} {agent.status}
            </Badge>
            <Badge variant="outline" className={getHealthColor(agent.health_status)}>
              {getHealthIcon(agent.health_status)} {agent.health_status}
            </Badge>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-0">
        {/* Purpose */}
        <div className="mb-4">
          <p className="text-sm text-gray-700">
            <strong>Purpose:</strong> {agent.purpose}
          </p>
        </div>

        {/* Capabilities */}
        {agent.capabilities && agent.capabilities.length > 0 && (
          <div className="mb-4">
            <p className="text-sm font-medium text-gray-700 mb-2">
              Capabilities:
            </p>
            <div className="flex flex-wrap gap-1">
              {agent.capabilities.slice(0, 3).map((capability, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {capability}
                </Badge>
              ))}
              {agent.capabilities.length > 3 && (
                <Badge variant="outline" className="text-xs">
                  +{agent.capabilities.length - 3} more
                </Badge>
              )}
            </div>
          </div>
        )}

        {/* Links */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mb-4">
          {agent.repository_url && (
            <a
              href={agent.repository_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 p-2 bg-gray-50 rounded text-xs text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-colors"
            >
              <Github className="h-3 w-3" />
              Repository
            </a>
          )}
          {agent.deployment_url && (
            <a
              href={agent.deployment_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 p-2 bg-gray-50 rounded text-xs text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-colors"
            >
              <ExternalLink className="h-3 w-3" />
              Live Agent
            </a>
          )}
          {agent.health_check_url && (
            <a
              href={agent.health_check_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 p-2 bg-gray-50 rounded text-xs text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-colors"
            >
              <Activity className="h-3 w-3" />
              Health Check
            </a>
          )}
        </div>

        {/* Metadata */}
        <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
          <span>v{agent.version}</span>
          <span>Created: {formatDate(agent.created_at)}</span>
        </div>

        {/* Health Check Info */}
        {agent.last_health_check && (
          <div className="mb-4 p-2 bg-gray-50 rounded text-xs text-gray-600">
            Last health check: {formatDate(agent.last_health_check)}
          </div>
        )}

        {/* Actions */}
        {showActions && (
          <div className="flex gap-2">
            {onView && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onView(agent)}
                className="flex-1"
              >
                <Eye className="h-4 w-4 mr-2" />
                View
              </Button>
            )}
            {onHealthCheck && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onHealthCheck(agent)}
              >
                <Activity className="h-4 w-4" />
              </Button>
            )}
            {onEdit && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onEdit(agent)}
              >
                <Edit className="h-4 w-4" />
              </Button>
            )}
            {onDelete && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onDelete(agent)}
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
