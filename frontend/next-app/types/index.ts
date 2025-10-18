/**
 * Type definitions for the AI Agent Factory application.
 */

// Enums
export enum PRDType {
  PLATFORM = 'platform',
  AGENT = 'agent'
}

export enum PRDStatus {
  UPLOADED = 'uploaded',
  STANDARDIZING = 'standardizing',
  REVIEW = 'review',
  QUEUE = 'queue',
  READY_FOR_DEVIN = 'ready_for_devin',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  PROCESSED = 'processed'
}

export enum PRDPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum PRDEffort {
  SMALL = 'small',
  MEDIUM = 'medium',
  LARGE = 'large',
  EPIC = 'epic'
}

export enum AgentStatus {
  PENDING = 'pending',
  DEPLOYED = 'deployed',
  RUNNING = 'running',
  STOPPED = 'stopped',
  FAILED = 'failed',
  MAINTENANCE = 'maintenance'
}

export enum AgentHealthStatus {
  HEALTHY = 'healthy',
  UNHEALTHY = 'unhealthy',
  UNKNOWN = 'unknown',
  DEGRADED = 'degraded'
}

export enum DevinTaskStatus {
  PENDING = 'pending',
  IN_DEVIN = 'in_devin',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

// Core Interfaces
export interface PRD {
  id: string
  title: string
  description: string
  requirements: string[]
  prd_type: PRDType
  status: PRDStatus
  github_repo_url?: string
  created_at: string
  updated_at?: string
  
  // Enhanced PRD sections
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
  
  // Roadmap-specific fields
  category?: string
  priority?: PRDPriority
  effort_estimate?: PRDEffort
  business_value?: number
  technical_complexity?: number
  dependencies_list?: string[]
  assignee?: string
  target_sprint?: string
  
  // File upload fields
  original_filename?: string
  file_content?: string
}

export interface Agent {
  id: string
  name: string
  description: string
  purpose: string
  version: string
  tools: string[]
  status: AgentStatus
  repository_url?: string
  deployment_url?: string
  health_check_url?: string
  prd_id?: string
  devin_task_id?: string
  capabilities: string[]
  configuration: Record<string, any>
  last_health_check?: string
  health_status: AgentHealthStatus
  created_at: string
  updated_at: string
}

export interface DevinTask {
  id: string
  prd_id: string
  title: string
  description: string
  requirements: string[]
  devin_prompt: string
  status: DevinTaskStatus
  created_at: string
  updated_at: string
  devin_output?: string
  agent_code?: string
}

// API Response Types
export interface PRDListResponse {
  prds: PRD[]
  total: number
  page: number
  size: number
  has_next: boolean
}

export interface AgentListResponse {
  agents: Agent[]
  total: number
  page: number
  size: number
  has_next: boolean
}

export interface DevinTaskListResponse {
  tasks: DevinTask[]
  total: number
  page: number
  size: number
  has_next: boolean
}

export interface PRDMarkdownResponse {
  prd_id: string
  markdown: string
  filename: string
}

export interface AgentHealthResponse {
  agent_id: string
  agent_name: string
  health_check_url: string
  last_checked?: string
  status: AgentHealthStatus
  details: Record<string, any>
  response_time_ms: number
}

export interface AgentMetricsResponse {
  agent_id: string
  agent_name: string
  status: AgentStatus
  health_status: AgentHealthStatus
  last_health_check?: string
  deployment_url?: string
  repository_url?: string
  version: string
  capabilities: string[]
  uptime_seconds?: number
  request_count?: number
  error_count?: number
  avg_response_time_ms?: number
}

// Form Types
export interface PRDCreateForm {
  title: string
  description: string
  requirements: string[]
  prd_type: PRDType
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
  category?: string
  priority?: PRDPriority
  effort_estimate?: PRDEffort
  business_value?: number
  technical_complexity?: number
  dependencies_list?: string[]
  assignee?: string
  target_sprint?: string
}

export interface AgentRegistrationForm {
  name: string
  description: string
  purpose: string
  version: string
  repository_url: string
  deployment_url: string
  health_check_url: string
  prd_id?: string
  devin_task_id?: string
  capabilities: string[]
  configuration: Record<string, any>
}

export interface DevinTaskCreateForm {
  prd_id: string
  title: string
  description: string
  requirements: string[]
}

// UI State Types
export interface DashboardState {
  agents: Agent[]
  prds: PRD[]
  loading: boolean
  error?: string
}

export interface PRDFilters {
  prd_type?: PRDType
  status?: PRDStatus
  category?: string
  priority?: PRDPriority
}

export interface AgentFilters {
  status?: AgentStatus
  health_status?: AgentHealthStatus
  prd_id?: string
}

export interface DevinTaskFilters {
  status?: DevinTaskStatus
  prd_id?: string
}

// Component Props Types
export interface PRDCardProps {
  prd: PRD
  onView?: (prd: PRD) => void
  onEdit?: (prd: PRD) => void
  onDelete?: (prd: PRD) => void
}

export interface AgentCardProps {
  agent: Agent
  onView?: (agent: Agent) => void
  onEdit?: (agent: Agent) => void
  onDelete?: (agent: Agent) => void
  onHealthCheck?: (agent: Agent) => void
}

export interface DevinTaskCardProps {
  task: DevinTask
  onView?: (task: DevinTask) => void
  onExecute?: (task: DevinTask) => void
  onComplete?: (task: DevinTask) => void
}

// API Error Types
export interface APIError {
  message: string
  details?: Record<string, any>
  status_code?: number
}

export interface APIResponse<T> {
  data?: T
  error?: APIError
  success: boolean
}

// Utility Types
export type SortDirection = 'asc' | 'desc'

export interface SortConfig {
  field: string
  direction: SortDirection
}

export interface PaginationConfig {
  page: number
  size: number
  total: number
}

export interface FilterConfig {
  field: string
  operator: 'eq' | 'ne' | 'gt' | 'lt' | 'gte' | 'lte' | 'contains' | 'in'
  value: any
}
