"""
Custom exceptions for the Todo API
"""

from fastapi import HTTPException, status


class TaskNotFoundException(HTTPException):
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )


class UnauthorizedUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: User does not have permission to access this resource"
        )


class InvalidTaskDataException(HTTPException):
    def __init__(self, detail: str = "Invalid task data provided"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class DatabaseOperationException(HTTPException):
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )