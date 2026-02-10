import logging
import time
from fastapi import Request
from typing import Dict, Any
import json
from datetime import datetime
import uuid
from enum import Enum

# Configure logger for audit logs
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

# Create a file handler for audit logs
if not audit_logger.handlers:
    handler = logging.FileHandler("audit.log")
    formatter = logging.Formatter(
        '%(asctime)s - AUDIT - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    audit_logger.addHandler(handler)


class AuditEventType(str, Enum):
    """Enumeration of possible audit event types"""
    USER_LOGIN = "USER_LOGIN"
    USER_LOGOUT = "USER_LOGOUT"
    TASK_CREATE = "TASK_CREATE"
    TASK_READ = "TASK_READ"
    TASK_UPDATE = "TASK_UPDATE"
    TASK_DELETE = "TASK_DELETE"
    TASK_TOGGLE_COMPLETION = "TASK_TOGGLE_COMPLETION"
    TASK_SEARCH = "TASK_SEARCH"
    CONVERSATION_CREATE = "CONVERSATION_CREATE"
    CONVERSATION_READ = "CONVERSATION_READ"
    CONVERSATION_UPDATE = "CONVERSATION_UPDATE"
    CONVERSATION_DELETE = "CONVERSATION_DELETE"
    API_ACCESS = "API_ACCESS"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"


def log_audit_event(
    event_type: AuditEventType,
    user_id: str,
    resource_id: str = None,
    resource_type: str = "unknown",
    action: str = "unknown",
    ip_address: str = None,
    user_agent: str = None,
    success: bool = True,
    details: Dict[str, Any] = None
):
    """
    Log an audit event with standardized format.
    """
    audit_entry = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type.value if isinstance(event_type, AuditEventType) else event_type,
        "user_id": user_id,
        "resource_id": resource_id,
        "resource_type": resource_type,
        "action": action,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "success": success,
        "details": details or {}
    }
    
    audit_logger.info(json.dumps(audit_entry))


def audit_middleware_handler(request: Request, call_next):
    """
    Middleware function to log API access events.
    """
    start_time = time.time()
    
    # Get client IP
    forwarded_for = request.headers.get("x-forwarded-for")
    ip_address = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host
    
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    processing_time = time.time() - start_time
    
    # Extract user ID if available in request state
    user_id = getattr(request.state, 'user_id', 'anonymous')
    
    # Log the API access
    log_audit_event(
        event_type=AuditEventType.API_ACCESS,
        user_id=user_id,
        resource_type="api_endpoint",
        action=request.method,
        ip_address=ip_address,
        user_agent=user_agent,
        success=response.status_code < 400,
        details={
            "path": request.url.path,
            "status_code": response.status_code,
            "processing_time_ms": round(processing_time * 1000, 2),
            "response_size": response.headers.get("content-length", 0)
        }
    )
    
    return response


class AuditLogger:
    """
    A class to provide audit logging functionality for different operations.
    """
    
    @staticmethod
    def log_user_login(user_id: str, ip_address: str, user_agent: str = None, success: bool = True):
        """Log user login event"""
        log_audit_event(
            event_type=AuditEventType.USER_LOGIN,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success
        )
    
    @staticmethod
    def log_user_logout(user_id: str, ip_address: str, user_agent: str = None):
        """Log user logout event"""
        log_audit_event(
            event_type=AuditEventType.USER_LOGOUT,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    @staticmethod
    def log_task_operation(
        operation: str,  # "create", "read", "update", "delete", "toggle_completion"
        user_id: str,
        task_id: str = None,
        ip_address: str = None,
        user_agent: str = None,
        success: bool = True,
        details: Dict[str, Any] = None
    ):
        """Log task-related operations"""
        event_type_map = {
            "create": AuditEventType.TASK_CREATE,
            "read": AuditEventType.TASK_READ,
            "update": AuditEventType.TASK_UPDATE,
            "delete": AuditEventType.TASK_DELETE,
            "toggle_completion": AuditEventType.TASK_TOGGLE_COMPLETION,
            "search": AuditEventType.TASK_SEARCH
        }
        
        event_type = event_type_map.get(operation, AuditEventType.TASK_UPDATE)
        
        log_audit_event(
            event_type=event_type,
            user_id=user_id,
            resource_id=task_id,
            resource_type="task",
            action=operation,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            details=details
        )
    
    @staticmethod
    def log_conversation_operation(
        operation: str,  # "create", "read", "update", "delete"
        user_id: str,
        conversation_id: str = None,
        ip_address: str = None,
        user_agent: str = None,
        success: bool = True,
        details: Dict[str, Any] = None
    ):
        """Log conversation-related operations"""
        event_type_map = {
            "create": AuditEventType.CONVERSATION_CREATE,
            "read": AuditEventType.CONVERSATION_READ,
            "update": AuditEventType.CONVERSATION_UPDATE,
            "delete": AuditEventType.CONVERSATION_DELETE
        }
        
        event_type = event_type_map.get(operation, AuditEventType.CONVERSATION_UPDATE)
        
        log_audit_event(
            event_type=event_type,
            user_id=user_id,
            resource_id=conversation_id,
            resource_type="conversation",
            action=operation,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            details=details
        )
    
    @staticmethod
    def log_permission_denied(user_id: str, resource_type: str, resource_id: str, action: str, ip_address: str = None):
        """Log permission denied events"""
        log_audit_event(
            event_type=AuditEventType.PERMISSION_DENIED,
            user_id=user_id,
            resource_id=resource_id,
            resource_type=resource_type,
            action=action,
            ip_address=ip_address,
            success=False
        )
    
    @staticmethod
    def log_rate_limit_exceeded(user_id: str, ip_address: str, endpoint: str = None):
        """Log rate limit exceeded events"""
        log_audit_event(
            event_type=AuditEventType.RATE_LIMIT_EXCEEDED,
            user_id=user_id,
            resource_type="api_endpoint",
            action="access",
            ip_address=ip_address,
            success=False,
            details={"endpoint": endpoint}
        )


# Create a global instance of the audit logger
audit_logger_instance = AuditLogger()