"""
A2A (Agent-to-Agent) Protocol Models based on JSON-RPC 2.0 specification.

This module defines Pydantic models for the A2A protocol, enabling standardized
communication between AI agents using JSON-RPC 2.0 as the transport protocol.

Specification: https://a2a.dev/
JSON-RPC 2.0: https://www.jsonrpc.org/specification
"""

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Enumerations
# ============================================================================


class MessageRole(str, Enum):
    """Role of the message sender in the conversation."""

    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"


class MessagePartKind(str, Enum):
    """Type of content in a message part."""

    TEXT = "text"
    DATA = "data"
    FILE = "file"


class TaskState(str, Enum):
    """Current state of a task execution."""

    WORKING = "working"
    COMPLETED = "completed"
    INPUT_REQUIRED = "input-required"
    FAILED = "failed"


class DeploymentType(str, Enum):
    """Deployment mode for the agent."""

    BLOCKING = "blocking"
    WEBHOOK = "webhook"


class OutputMode(str, Enum):
    """Supported output modes for agent responses."""

    TEXT = "text"
    DATA = "data"
    FILE = "file"
    STREAMING = "streaming"


# ============================================================================
# Message Components
# ============================================================================


class MessagePart(BaseModel):
    """
    A part of a message that can contain text, structured data, or file reference.
    
    Supports three kinds:
    - text: Plain text content (use 'text' field)
    - data: Structured JSON data (use 'data' field)
    - file: File reference with metadata
    """

    kind: MessagePartKind = Field(
        ..., description="Type of content: text, data, or file"
    )
    text: Optional[str] = Field(
        None, description="Text content (for kind='text')"
    )
    data: Optional[dict[str, Any]] = Field(
        None, description="Structured data (for kind='data')"
    )
    mimeType: Optional[str] = Field(
        None, description="MIME type of the content (e.g., 'application/json', 'text/plain')"
    )
    fileName: Optional[str] = Field(
        None, description="Original filename (for file kind)"
    )
    fileSize: Optional[int] = Field(
        None, description="File size in bytes (for file kind)"
    )
    url: Optional[str] = Field(
        None, description="URL to access the file or resource"
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: Optional[str], info) -> Optional[str]:
        """Validate text field matches kind."""
        kind = info.data.get("kind")
        if kind == MessagePartKind.TEXT and v is None:
            raise ValueError("Text kind requires 'text' field to be set")
        return v
    
    @field_validator("data")
    @classmethod
    def validate_data(cls, v: Optional[dict], info) -> Optional[dict]:
        """Validate data field matches kind."""
        kind = info.data.get("kind")
        if kind == MessagePartKind.DATA and v is None:
            raise ValueError("Data kind requires 'data' field to be set")
        return v

    class Config:
        use_enum_values = True


class A2AMessage(BaseModel):
    """
    A message in the A2A protocol conversation.
    
    Represents a single message from a user, agent, or system with support
    for multiple parts (text, data, files) and metadata tracking.
    """

    role: MessageRole = Field(
        ..., description="Who sent this message: user, agent, or system"
    )
    parts: list[MessagePart] = Field(
        default_factory=list, description="List of message parts (text, data, files)"
    )
    messageId: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique identifier for this message"
    )
    contextId: Optional[str] = Field(
        None, description="Associated context ID for conversation tracking"
    )
    taskId: Optional[str] = Field(
        None, description="Associated task ID for tracking"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="When this message was created"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the message"
    )

    class Config:
        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat()}


# ============================================================================
# Configuration Models
# ============================================================================


class PushNotificationConfig(BaseModel):
    """Configuration for push notifications in webhook mode."""

    webhookUrl: str = Field(
        ..., description="URL to receive webhook notifications"
    )
    headers: dict[str, str] = Field(
        default_factory=dict, description="Custom headers for webhook requests"
    )
    retryAttempts: int = Field(
        default=3, ge=0, le=10, description="Number of retry attempts for failed webhooks"
    )
    retryDelaySeconds: int = Field(
        default=5, ge=1, le=300, description="Delay between retry attempts in seconds"
    )


class MessageConfiguration(BaseModel):
    """
    Configuration for how the agent should handle and respond to messages.
    
    Defines deployment type (blocking/webhook), accepted output modes,
    and webhook settings for asynchronous responses.
    """

    deploymentType: DeploymentType = Field(
        default=DeploymentType.BLOCKING,
        description="blocking: synchronous response, webhook: asynchronous with callback"
    )
    acceptedOutputModes: list[OutputMode] = Field(
        default_factory=lambda: [OutputMode.TEXT, OutputMode.DATA],
        description="Output modes the agent can use (text, data, file, streaming)"
    )
    pushNotificationConfig: Optional[PushNotificationConfig] = Field(
        None, description="Webhook configuration (required if deploymentType is webhook)"
    )
    maxTokens: Optional[int] = Field(
        None, ge=1, le=100000, description="Maximum tokens for LLM response"
    )
    temperature: Optional[float] = Field(
        None, ge=0.0, le=2.0, description="Temperature for LLM sampling"
    )
    timeout: Optional[int] = Field(
        None, ge=1, le=300, description="Timeout in seconds for agent processing"
    )

    @field_validator("pushNotificationConfig")
    @classmethod
    def validate_webhook_config(cls, v: Optional[PushNotificationConfig], info) -> Optional[PushNotificationConfig]:
        """Ensure webhook config is provided when deployment type is webhook."""
        deployment_type = info.data.get("deploymentType")
        if deployment_type == DeploymentType.WEBHOOK and v is None:
            raise ValueError("pushNotificationConfig is required when deploymentType is webhook")
        return v

    class Config:
        use_enum_values = True


class MessageParams(BaseModel):
    """
    Parameters for sending a message to an agent.
    
    Wraps the messages and configuration for the message/send method.
    Compatible with execute method parameters.
    """

    contextId: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the conversation context"
    )
    taskId: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for this task execution"
    )
    messages: list[A2AMessage] = Field(
        default_factory=list, description="List of messages to send to the agent"
    )
    config: MessageConfiguration = Field(
        default_factory=MessageConfiguration,
        alias="configuration",
        description="Configuration for how the agent should process this message"
    )


class ExecuteParams(BaseModel):
    """
    Parameters for executing a task with an agent.
    
    Contains conversation history and context for the execute method.
    """

    contextId: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the conversation context"
    )
    taskId: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for this task execution"
    )
    messages: list[A2AMessage] = Field(
        default_factory=list, description="List of messages in the conversation history"
    )
    configuration: MessageConfiguration = Field(
        default_factory=MessageConfiguration,
        description="Configuration for task execution"
    )


# ============================================================================
# JSON-RPC Request Models
# ============================================================================


class JSONRPCRequest(BaseModel):
    """
    JSON-RPC 2.0 request for A2A protocol.
    
    Supports two methods:
    - message/send: Send a single message to an agent
    - execute: Execute a task with conversation history
    """

    jsonrpc: Literal["2.0"] = Field(
        default="2.0", description="JSON-RPC version (always 2.0)"
    )
    id: str | int = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for this request"
    )
    method: Literal["message/send", "execute"] = Field(
        ..., description="Method to invoke: message/send or execute"
    )
    params: MessageParams | ExecuteParams = Field(
        ..., description="Parameters for the method (MessageParams or ExecuteParams, both are compatible)"
    )


# ============================================================================
# Task and Response Models
# ============================================================================


class TaskStatus(BaseModel):
    """
    Current status of a task execution.
    
    Tracks the state, timestamp, and optional message about the task progress.
    """

    state: TaskState = Field(
        ..., description="Current state: working, completed, input-required, or failed"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="When this status was recorded"
    )
    message: Optional[str] = Field(
        None, description="Human-readable message about the status"
    )
    progress: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Progress percentage (0.0 to 1.0)"
    )
    error: Optional[str] = Field(
        None, description="Error message if state is failed"
    )

    class Config:
        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class Artifact(BaseModel):
    """
    An artifact produced by the agent (result, file, data).
    
    Artifacts are the outputs of agent processing, such as recommendations,
    generated content, or file references.
    """

    artifactId: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for this artifact"
    )
    name: str = Field(
        ..., description="Human-readable name for the artifact"
    )
    parts: list[MessagePart] = Field(
        default_factory=list, description="Content parts of the artifact"
    )
    mimeType: Optional[str] = Field(
        None, description="MIME type of the artifact"
    )
    description: Optional[str] = Field(
        None, description="Description of what this artifact contains"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the artifact"
    )


class TaskResult(BaseModel):
    """
    Result of a task execution in the A2A protocol.
    
    Contains the task status, artifacts produced, conversation history,
    and metadata about the execution.
    """

    taskId: str = Field(
        ..., description="Unique task identifier from the original request"
    )
    contextId: str = Field(
        ..., description="Context ID from the original request"
    )
    status: TaskStatus = Field(
        ..., description="Current status of the task"
    )
    artifacts: list[Artifact] = Field(
        default_factory=list, description="Artifacts produced by the agent"
    )
    history: list[A2AMessage] = Field(
        default_factory=list, description="Full conversation history including agent responses"
    )
    kind: Literal["task"] = Field(
        default="task", description="Type of result (always 'task' for A2A)"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the task execution"
    )
    createdAt: datetime = Field(
        default_factory=datetime.utcnow, description="When this result was created"
    )
    completedAt: Optional[datetime] = Field(
        None, description="When the task was completed (if applicable)"
    )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


# ============================================================================
# JSON-RPC Response Models
# ============================================================================


class JSONRPCError(BaseModel):
    """
    JSON-RPC 2.0 error object.
    
    Standard error format for JSON-RPC responses.
    """

    code: int = Field(
        ..., description="Error code (standard JSON-RPC error codes)"
    )
    message: str = Field(
        ..., description="Human-readable error message"
    )
    data: Optional[dict[str, Any]] = Field(
        None, description="Additional error data"
    )


class JSONRPCResponse(BaseModel):
    """
    JSON-RPC 2.0 response for A2A protocol.
    
    Contains either a result (TaskResult) on success or an error object on failure.
    """

    jsonrpc: Literal["2.0"] = Field(
        default="2.0", description="JSON-RPC version (always 2.0)"
    )
    id: str | int = Field(
        ..., description="ID matching the original request"
    )
    result: Optional[TaskResult] = Field(
        None, description="Task result on success"
    )
    error: Optional[JSONRPCError] = Field(
        None, description="Error object on failure"
    )

    @field_validator("error")
    @classmethod
    def validate_result_or_error(cls, v: Optional[JSONRPCError], info) -> Optional[JSONRPCError]:
        """Ensure either result or error is present, but not both."""
        result = info.data.get("result")
        if result is not None and v is not None:
            raise ValueError("Response cannot have both result and error")
        if result is None and v is None:
            raise ValueError("Response must have either result or error")
        return v


# ============================================================================
# Standard JSON-RPC Error Codes
# ============================================================================


class JSONRPCErrorCode:
    """Standard JSON-RPC 2.0 error codes."""

    PARSE_ERROR = -32700  # Invalid JSON
    INVALID_REQUEST = -32600  # Invalid request object
    METHOD_NOT_FOUND = -32601  # Method does not exist
    INVALID_PARAMS = -32602  # Invalid method parameters
    INTERNAL_ERROR = -32603  # Internal JSON-RPC error
    
    # A2A-specific error codes (custom range: -32000 to -32099)
    AGENT_ERROR = -32000  # Generic agent error
    TASK_FAILED = -32001  # Task execution failed
    TIMEOUT = -32002  # Request timeout
    RATE_LIMIT = -32003  # Rate limit exceeded
    CONFIGURATION_ERROR = -32004  # Invalid configuration
    AUTHENTICATION_ERROR = -32005  # Authentication failed
