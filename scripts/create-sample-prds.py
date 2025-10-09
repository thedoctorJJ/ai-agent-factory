#!/usr/bin/env python3
"""
Script to create sample PRDs for the improvement suggestions
"""

import requests
import json
from datetime import datetime

# Sample PRDs based on the improvement suggestions
SAMPLE_PRDS = [
    {
        "title": "Database Integration with Supabase",
        "description": "Replace in-memory storage with persistent Supabase database integration for agents and PRDs",
        "requirements": [
            "Connect to Supabase PostgreSQL database",
            "Implement data models for agents and PRDs",
            "Add database migrations and schema management",
            "Implement CRUD operations for all entities",
            "Add database connection pooling and error handling",
            "Set up database backup and recovery procedures"
        ],
        "problem_statement": "Currently using in-memory storage which causes data loss on server restart and doesn't support concurrent users or data relationships.",
        "target_users": ["Backend developers", "Platform administrators", "End users"],
        "user_stories": [
            "As a developer, I want persistent data storage so that my data survives server restarts",
            "As an admin, I want to manage data relationships so that I can maintain data integrity",
            "As a user, I want my PRDs and agents to be saved so that I can access them later"
        ],
        "acceptance_criteria": [
            "All PRDs and agents are stored in Supabase database",
            "Data persists across server restarts",
            "Database operations complete within 200ms",
            "Proper error handling for database failures",
            "Database migrations run automatically on deployment"
        ],
        "technical_requirements": [
            "Supabase client integration",
            "SQLAlchemy ORM for data modeling",
            "Alembic for database migrations",
            "Connection pooling with async support",
            "Database health checks and monitoring"
        ],
        "success_metrics": [
            "100% data persistence across restarts",
            "Database response time < 200ms",
            "Zero data loss incidents",
            "Successful migration of existing in-memory data"
        ],
        "timeline": "2-3 weeks",
        "category": "core_functionality",
        "priority_score": 9,
        "effort_estimate": "large",
        "business_value": 9,
        "technical_complexity": 6,
        "dependencies_list": ["Supabase account setup", "Database schema design"],
        "assignee": "Backend Team",
        "target_sprint": "Sprint 1"
    },
    {
        "title": "JWT Authentication System",
        "description": "Implement secure JWT-based authentication with user management and role-based access control",
        "requirements": [
            "User registration and login endpoints",
            "JWT token generation and validation",
            "Password hashing with bcrypt",
            "Role-based access control (RBAC)",
            "Protected route middleware",
            "User session management",
            "Password reset functionality",
            "API rate limiting"
        ],
        "problem_statement": "No authentication system exists, making the platform insecure and unsuitable for production use with multiple users.",
        "target_users": ["End users", "Platform administrators", "Security team"],
        "user_stories": [
            "As a user, I want to create an account so that I can access the platform securely",
            "As an admin, I want to manage user permissions so that I can control access to features",
            "As a developer, I want secure API endpoints so that I can protect sensitive data"
        ],
        "acceptance_criteria": [
            "Users can register and login securely",
            "JWT tokens expire appropriately",
            "Protected routes require valid authentication",
            "Role-based permissions work correctly",
            "Password reset functionality works",
            "API rate limiting prevents abuse"
        ],
        "technical_requirements": [
            "python-jose for JWT handling",
            "passlib for password hashing",
            "FastAPI security middleware",
            "Redis for session storage",
            "Email service for password reset"
        ],
        "success_metrics": [
            "100% of API endpoints properly protected",
            "Zero unauthorized access incidents",
            "User registration completion rate > 90%",
            "Password reset success rate > 95%"
        ],
        "timeline": "2-3 weeks",
        "category": "production_readiness",
        "priority_score": 8,
        "effort_estimate": "large",
        "business_value": 8,
        "technical_complexity": 7,
        "dependencies_list": ["Database integration", "Email service setup"],
        "assignee": "Backend Team",
        "target_sprint": "Sprint 2"
    },
    {
        "title": "Comprehensive Testing Suite",
        "description": "Implement unit tests, integration tests, and end-to-end tests for all platform components",
        "requirements": [
            "Unit tests for all API endpoints",
            "Integration tests for database operations",
            "End-to-end tests for user workflows",
            "Test coverage reporting",
            "Automated test execution in CI/CD",
            "Mock services for external dependencies",
            "Performance testing for critical paths"
        ],
        "problem_statement": "No automated tests exist, making it difficult to ensure code quality and catch regressions during development.",
        "target_users": ["Development team", "QA team", "DevOps team"],
        "user_stories": [
            "As a developer, I want automated tests so that I can catch bugs early",
            "As a QA engineer, I want comprehensive test coverage so that I can ensure quality",
            "As a DevOps engineer, I want tests in CI/CD so that I can prevent bad deployments"
        ],
        "acceptance_criteria": [
            "Test coverage > 80% for all modules",
            "All tests pass in CI/CD pipeline",
            "Tests run in < 5 minutes",
            "Mock services for external APIs",
            "Performance tests for critical endpoints"
        ],
        "technical_requirements": [
            "pytest for Python testing",
            "Jest for frontend testing",
            "Playwright for E2E testing",
            "Coverage.py for coverage reporting",
            "GitHub Actions for CI/CD"
        ],
        "success_metrics": [
            "Test coverage > 80%",
            "Zero test failures in CI/CD",
            "Test execution time < 5 minutes",
            "100% of critical paths tested"
        ],
        "timeline": "2-3 weeks",
        "category": "production_readiness",
        "priority_score": 7,
        "effort_estimate": "large",
        "business_value": 7,
        "technical_complexity": 6,
        "dependencies_list": ["Database integration", "Authentication system"],
        "assignee": "QA Team",
        "target_sprint": "Sprint 3"
    },
    {
        "title": "Structured Logging and Error Tracking",
        "description": "Implement comprehensive logging system with structured logs and error tracking integration",
        "requirements": [
            "Structured logging with JSON format",
            "Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
            "Request/response logging middleware",
            "Error tracking with Sentry integration",
            "Log aggregation and search capabilities",
            "Performance monitoring and metrics",
            "Alert system for critical errors"
        ],
        "problem_statement": "Current logging is basic console output, making it difficult to debug issues and monitor system health in production.",
        "target_users": ["Development team", "DevOps team", "Support team"],
        "user_stories": [
            "As a developer, I want detailed logs so that I can debug issues quickly",
            "As a DevOps engineer, I want error alerts so that I can respond to issues immediately",
            "As a support agent, I want searchable logs so that I can help users with problems"
        ],
        "acceptance_criteria": [
            "All API requests are logged with timing",
            "Errors are automatically tracked and alerted",
            "Logs are searchable and filterable",
            "Performance metrics are collected",
            "Critical errors trigger immediate alerts"
        ],
        "technical_requirements": [
            "structlog for structured logging",
            "Sentry for error tracking",
            "Prometheus for metrics",
            "ELK stack or similar for log aggregation",
            "AlertManager for notifications"
        ],
        "success_metrics": [
            "Mean time to detection < 5 minutes",
            "Mean time to resolution < 30 minutes",
            "Log search response time < 2 seconds",
            "Zero missed critical errors"
        ],
        "timeline": "1-2 weeks",
        "category": "production_readiness",
        "priority_score": 6,
        "effort_estimate": "medium",
        "business_value": 6,
        "technical_complexity": 5,
        "dependencies_list": ["Authentication system"],
        "assignee": "DevOps Team",
        "target_sprint": "Sprint 3"
    },
    {
        "title": "Redis Caching Layer",
        "description": "Implement Redis caching to improve API response times and reduce database load",
        "requirements": [
            "Redis integration for caching",
            "Cache invalidation strategies",
            "API response caching",
            "Database query result caching",
            "Session storage in Redis",
            "Cache warming strategies",
            "Cache monitoring and metrics"
        ],
        "problem_statement": "API responses are slow due to repeated database queries, and there's no caching layer to improve performance.",
        "target_users": ["End users", "Backend developers", "DevOps team"],
        "user_stories": [
            "As a user, I want fast API responses so that I can use the platform efficiently",
            "As a developer, I want cached data so that I can reduce database load",
            "As a DevOps engineer, I want cache metrics so that I can monitor performance"
        ],
        "acceptance_criteria": [
            "API response times < 100ms for cached data",
            "Cache hit rate > 80%",
            "Automatic cache invalidation on data updates",
            "Cache warming on application startup",
            "Cache monitoring dashboard"
        ],
        "technical_requirements": [
            "Redis client for Python",
            "Cache decorators for API endpoints",
            "Cache invalidation middleware",
            "Redis cluster for high availability",
            "Cache monitoring tools"
        ],
        "success_metrics": [
            "API response time improvement > 50%",
            "Cache hit rate > 80%",
            "Database query reduction > 60%",
            "Cache availability > 99.9%"
        ],
        "timeline": "1-2 weeks",
        "category": "performance_scale",
        "priority_score": 5,
        "effort_estimate": "medium",
        "business_value": 5,
        "technical_complexity": 4,
        "dependencies_list": ["Database integration"],
        "assignee": "Backend Team",
        "target_sprint": "Sprint 4"
    },
    {
        "title": "Performance Monitoring and Metrics",
        "description": "Implement comprehensive performance monitoring with Prometheus metrics and Grafana dashboards",
        "requirements": [
            "Prometheus metrics collection",
            "Custom metrics for business logic",
            "Grafana dashboards for visualization",
            "Performance alerting",
            "Application performance monitoring (APM)",
            "Database performance monitoring",
            "User experience monitoring"
        ],
        "problem_statement": "No performance monitoring exists, making it difficult to identify bottlenecks and optimize system performance.",
        "target_users": ["DevOps team", "Development team", "Product managers"],
        "user_stories": [
            "As a DevOps engineer, I want performance metrics so that I can monitor system health",
            "As a developer, I want APM data so that I can optimize slow code paths",
            "As a product manager, I want user experience metrics so that I can improve the product"
        ],
        "acceptance_criteria": [
            "All critical metrics are monitored",
            "Performance dashboards are available",
            "Alerts trigger for performance degradation",
            "APM traces show request flows",
            "User experience metrics are tracked"
        ],
        "technical_requirements": [
            "Prometheus client for metrics",
            "Grafana for visualization",
            "Jaeger for distributed tracing",
            "AlertManager for notifications",
            "Custom metrics for business KPIs"
        ],
        "success_metrics": [
            "Mean time to detection < 2 minutes",
            "Performance dashboard availability > 99%",
            "Alert accuracy > 95%",
            "User experience score > 4.5/5"
        ],
        "timeline": "1-2 weeks",
        "category": "performance_scale",
        "priority_score": 4,
        "effort_estimate": "medium",
        "business_value": 4,
        "technical_complexity": 5,
        "dependencies_list": ["Logging system", "Caching layer"],
        "assignee": "DevOps Team",
        "target_sprint": "Sprint 4"
    },
    {
        "title": "Enhanced User Interface Components",
        "description": "Improve the frontend with advanced UI components, better UX, and responsive design enhancements",
        "requirements": [
            "Advanced data tables with sorting and filtering",
            "Interactive charts and visualizations",
            "Improved form validation and error handling",
            "Better loading states and skeleton screens",
            "Enhanced mobile responsiveness",
            "Dark mode support",
            "Accessibility improvements (WCAG 2.1)"
        ],
        "problem_statement": "The current UI is functional but lacks advanced features and could provide a better user experience.",
        "target_users": ["End users", "UI/UX designers", "Frontend developers"],
        "user_stories": [
            "As a user, I want better data visualization so that I can understand information quickly",
            "As a mobile user, I want responsive design so that I can use the platform on any device",
            "As a user with disabilities, I want accessible features so that I can use the platform effectively"
        ],
        "acceptance_criteria": [
            "All components are mobile responsive",
            "Data tables support sorting and filtering",
            "Charts are interactive and informative",
            "Forms have proper validation and error states",
            "WCAG 2.1 AA compliance achieved"
        ],
        "technical_requirements": [
            "Advanced shadcn/ui components",
            "Chart.js or D3.js for visualizations",
            "React Hook Form for form management",
            "Framer Motion for animations",
            "Accessibility testing tools"
        ],
        "success_metrics": [
            "User satisfaction score > 4.5/5",
            "Mobile usage increase > 30%",
            "Form completion rate > 95%",
            "Accessibility score > 95%"
        ],
        "timeline": "2-3 weeks",
        "category": "user_experience",
        "priority_score": 3,
        "effort_estimate": "large",
        "business_value": 6,
        "technical_complexity": 4,
        "dependencies_list": ["Authentication system"],
        "assignee": "Frontend Team",
        "target_sprint": "Sprint 5"
    },
    {
        "title": "Advanced Agent Orchestration",
        "description": "Implement advanced agent management features including agent chaining, workflow automation, and intelligent routing",
        "requirements": [
            "Agent chaining and workflow orchestration",
            "Intelligent request routing between agents",
            "Agent performance monitoring and optimization",
            "Dynamic agent scaling based on load",
            "Agent versioning and rollback capabilities",
            "Agent marketplace for sharing and discovery",
            "Advanced agent configuration management"
        ],
        "problem_statement": "Current agent system is basic and doesn't support advanced orchestration, limiting the platform's capabilities.",
        "target_users": ["Power users", "Enterprise customers", "Platform administrators"],
        "user_stories": [
            "As a power user, I want to chain agents so that I can create complex workflows",
            "As an enterprise user, I want intelligent routing so that requests go to the best agent",
            "As an admin, I want agent monitoring so that I can optimize performance"
        ],
        "acceptance_criteria": [
            "Agents can be chained in workflows",
            "Intelligent routing improves response quality",
            "Agent performance is monitored and optimized",
            "Dynamic scaling handles load spikes",
            "Agent marketplace is functional"
        ],
        "technical_requirements": [
            "Workflow orchestration engine",
            "Load balancing and routing algorithms",
            "Agent performance metrics",
            "Auto-scaling infrastructure",
            "Agent registry and discovery"
        ],
        "success_metrics": [
            "Workflow completion rate > 95%",
            "Response quality improvement > 20%",
            "Agent utilization > 80%",
            "Marketplace adoption > 50%"
        ],
        "timeline": "4-6 weeks",
        "category": "platform_features",
        "priority_score": 2,
        "effort_estimate": "epic",
        "business_value": 8,
        "technical_complexity": 9,
        "dependencies_list": ["Database integration", "Authentication system", "Performance monitoring"],
        "assignee": "Platform Team",
        "target_sprint": "Sprint 6-8"
    }
]

def create_sample_prds():
    """Create sample PRDs via API"""
    base_url = "http://localhost:8000"
    
    for prd_data in SAMPLE_PRDS:
        try:
            response = requests.post(f"{base_url}/api/v1/prds", json=prd_data)
            if response.status_code == 200:
                prd = response.json()
                print(f"✅ Created PRD: {prd['title']} (ID: {prd['id']})")
            else:
                print(f"❌ Failed to create PRD: {prd_data['title']} - {response.status_code}: {response.text}")
        except Exception as e:
            print(f"❌ Error creating PRD: {prd_data['title']} - {str(e)}")

if __name__ == "__main__":
    print("Creating sample PRDs for improvement suggestions...")
    create_sample_prds()
    print("Sample PRD creation completed!")
