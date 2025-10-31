"""
Models package for MoodMatch A2A Agent.

Exports all Pydantic models for A2A protocol communication.
"""

from .a2a import (
    # Enumerations
    MessageRole,
    MessagePartKind,
    TaskState,
    DeploymentType,
    OutputMode,
    
    # Message Components
    MessagePart,
    A2AMessage,
    
    # Configuration
    PushNotificationConfig,
    MessageConfiguration,
    MessageParams,
    ExecuteParams,
    
    # JSON-RPC Request
    JSONRPCRequest,
    
    # Task and Response
    TaskStatus,
    Artifact,
    TaskResult,
    
    # JSON-RPC Response
    JSONRPCError,
    JSONRPCResponse,
    JSONRPCErrorCode,
)

__all__ = [
    # Enumerations
    "MessageRole",
    "MessagePartKind",
    "TaskState",
    "DeploymentType",
    "OutputMode",
    
    # Message Components
    "MessagePart",
    "A2AMessage",
    
    # Configuration
    "PushNotificationConfig",
    "MessageConfiguration",
    "MessageParams",
    "ExecuteParams",
    
    # JSON-RPC Request
    "JSONRPCRequest",
    
    # Task and Response
    "TaskStatus",
    "Artifact",
    "TaskResult",
    
    # JSON-RPC Response
    "JSONRPCError",
    "JSONRPCResponse",
    "JSONRPCErrorCode",
]
