"""
Error handling utilities and custom exceptions.
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class AgentFactoryException(Exception):
    """Base exception for Agent Factory."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class PRDNotFoundError(AgentFactoryException):
    """Exception raised when PRD is not found."""
    pass


class AgentNotFoundError(AgentFactoryException):
    """Exception raised when agent is not found."""
    pass


class DevinTaskNotFoundError(AgentFactoryException):
    """Exception raised when Devin task is not found."""
    pass


class InvalidPRDTypeError(AgentFactoryException):
    """Exception raised when PRD type is invalid."""
    pass


class InvalidFileTypeError(AgentFactoryException):
    """Exception raised when file type is invalid."""
    pass


class ServiceUnavailableError(AgentFactoryException):
    """Exception raised when external service is unavailable."""
    pass


def handle_service_exception(exc: AgentFactoryException) -> HTTPException:
    """Convert service exceptions to HTTP exceptions."""
    if isinstance(exc, PRDNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message
        )
    elif isinstance(exc, AgentNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message
        )
    elif isinstance(exc, DevinTaskNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message
        )
    elif isinstance(exc, InvalidPRDTypeError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message
        )
    elif isinstance(exc, InvalidFileTypeError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message
        )
    elif isinstance(exc, ServiceUnavailableError):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=exc.message
        )
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


def create_error_response(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a standardized error response."""
    return HTTPException(
        status_code=status_code,
        detail={
            "message": message,
            "details": details or {}
        }
    )
