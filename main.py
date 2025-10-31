"""
FastAPI server implementing the A2A protocol for MoodMatch agent.

Production-ready server with JSON-RPC 2.0 support, proper error handling,
and lifespan management.
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from agents.moodmatch_agent import MoodMatchAgent
from models.a2a import (
    A2AMessage,
    ExecuteParams,
    JSONRPCError,
    JSONRPCErrorCode,
    JSONRPCRequest,
    JSONRPCResponse,
    MessageParams,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global agent instance
agent: MoodMatchAgent | None = None


# ============================================================================
# Lifespan Management
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI app.
    
    Handles startup and shutdown events for the MoodMatch agent.
    """
    global agent
    
    # Startup
    logger.info("Starting MoodMatch A2A Agent server...")
    
    try:
        # Get API credentials from environment
        gemini_key = os.getenv("GEMINI_API_KEY")
        tmdb_key = os.getenv("TMDB_API_KEY")
        spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
        spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
        
        # Validate required credentials
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        if not tmdb_key:
            raise ValueError("TMDB_API_KEY not found in environment")
        if not spotify_id or not spotify_secret:
            raise ValueError("Spotify credentials not found in environment")
        
        # Initialize MoodMatch agent
        agent = MoodMatchAgent(
            gemini_api_key=gemini_key,
            tmdb_api_key=tmdb_key,
            spotify_client_id=spotify_id,
            spotify_client_secret=spotify_secret,
            google_books_api_key=books_key
        )
        
        logger.info("✅ MoodMatch agent initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down MoodMatch A2A Agent server...")
    
    if agent:
        try:
            await agent.close()
            logger.info("✅ Agent cleanup completed")
        except Exception as e:
            logger.error(f"⚠️  Error during agent cleanup: {e}")


# ============================================================================
# FastAPI Application
# ============================================================================


app = FastAPI(
    title="MoodMatch A2A Agent",
    description="Mood-based recommendation agent that suggests movies, music, and books using AI analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Endpoints
# ============================================================================


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the status of the service and agent availability.
    """
    return {
        "status": "healthy",
        "agent": "MoodMatch A2A Agent",
        "version": "1.0.0",
        "agent_ready": agent is not None
    }


@app.post("/a2a/moodmatch")
async def a2a_endpoint(request: Request):
    """
    A2A protocol endpoint implementing JSON-RPC 2.0.
    
    Handles both 'message/send' and 'execute' methods for mood-based
    recommendations.
    
    Args:
        request: FastAPI request object
        
    Returns:
        JSONResponse with JSON-RPC 2.0 response
    """
    global agent
    
    # Check if agent is initialized
    if not agent:
        logger.error("Agent not initialized")
        return _create_error_response(
            id=None,
            code=JSONRPCErrorCode.INTERNAL_ERROR,
            message="Agent not initialized"
        )
    
    try:
        # Parse request body
        try:
            body = await request.json()
        except Exception as e:
            logger.error(f"Invalid JSON in request: {e}")
            return _create_error_response(
                id=None,
                code=JSONRPCErrorCode.PARSE_ERROR,
                message="Invalid JSON"
            )
        
        # Validate JSON-RPC 2.0 format
        if not isinstance(body, dict):
            return _create_error_response(
                id=None,
                code=JSONRPCErrorCode.INVALID_REQUEST,
                message="Request must be a JSON object"
            )
        
        if body.get("jsonrpc") != "2.0":
            return _create_error_response(
                id=body.get("id"),
                code=JSONRPCErrorCode.INVALID_REQUEST,
                message="Invalid JSON-RPC version, must be '2.0'"
            )
        
        if "id" not in body:
            return _create_error_response(
                id=None,
                code=JSONRPCErrorCode.INVALID_REQUEST,
                message="Missing required field 'id'"
            )
        
        # Parse into JSONRPCRequest model
        try:
            rpc_request = JSONRPCRequest(**body)
        except Exception as e:
            logger.error(f"Failed to parse JSON-RPC request: {e}")
            return _create_error_response(
                id=body.get("id"),
                code=JSONRPCErrorCode.INVALID_REQUEST,
                message=f"Invalid request format: {str(e)}"
            )
        
        logger.info(f"Received {rpc_request.method} request (id: {rpc_request.id})")
        
        # Handle method
        if rpc_request.method == "message/send":
            result = await _handle_message_send(rpc_request)
            
        elif rpc_request.method == "execute":
            result = await _handle_execute(rpc_request)
            
        else:
            logger.warning(f"Unknown method: {rpc_request.method}")
            return _create_error_response(
                id=rpc_request.id,
                code=JSONRPCErrorCode.METHOD_NOT_FOUND,
                message=f"Method '{rpc_request.method}' not found"
            )
        
        # Create successful response
        response = JSONRPCResponse(
            jsonrpc="2.0",
            id=rpc_request.id,
            result=result.model_dump()
        )
        
        logger.info(f"Request {rpc_request.id} completed successfully")
        
        return JSONResponse(
            content=response.model_dump(exclude_none=True, mode='json'),
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in a2a_endpoint: {e}", exc_info=True)
        return _create_error_response(
            id=body.get("id") if "body" in locals() else None,
            code=JSONRPCErrorCode.INTERNAL_ERROR,
            message=f"Internal server error: {str(e)}"
        )


# ============================================================================
# Handler Functions
# ============================================================================


async def _handle_message_send(rpc_request: JSONRPCRequest):
    """
    Handle 'message/send' method.
    
    Args:
        rpc_request: The JSON-RPC request
        
    Returns:
        TaskResult from agent processing
        
    Raises:
        ValueError: If params are invalid
    """
    global agent
    
    # Validate params
    if not rpc_request.params:
        raise ValueError("Missing required 'params' field")
    
    # Params is already a MessageParams object from the validator
    params = rpc_request.params
    
    # Validate messages
    if not params.messages or len(params.messages) == 0:
        raise ValueError("At least one message is required")
    
    # Process messages with agent
    try:
        result = await agent.process_messages(
            messages=params.messages,
            context_id=params.contextId,
            task_id=params.taskId,
            config=params.config
        )
        return result
        
    except Exception as e:
        logger.error(f"Error processing messages: {e}", exc_info=True)
        raise


async def _handle_execute(rpc_request: JSONRPCRequest):
    """
    Handle 'execute' method.
    
    Args:
        rpc_request: The JSON-RPC request
        
    Returns:
        TaskResult from agent processing
        
    Raises:
        ValueError: If params are invalid
    """
    global agent
    
    # Validate params
    if not rpc_request.params:
        raise ValueError("Missing required 'params' field")
    
    # Params is already an ExecuteParams object from the validator
    params = rpc_request.params
    
    # Validate messages
    if not params.messages or len(params.messages) == 0:
        raise ValueError("At least one message is required")
    
    # Process messages with agent
    try:
        # Use .config for MessageParams or .configuration for ExecuteParams
        # MessageParams has 'config' field with alias 'configuration'
        config = params.config if isinstance(params, MessageParams) else params.configuration
        
        result = await agent.process_messages(
            messages=params.messages,
            context_id=params.contextId,
            task_id=params.taskId,
            config=config
        )
        return result
        
    except Exception as e:
        logger.error(f"Error executing: {e}", exc_info=True)
        raise


# ============================================================================
# Helper Functions
# ============================================================================


def _create_error_response(
    id: str | int | None,
    code: JSONRPCErrorCode,
    message: str,
    data: Any = None
) -> JSONResponse:
    """
    Create JSON-RPC error response.
    
    Args:
        id: Request ID (can be None for parse errors)
        code: JSON-RPC error code
        message: Error message
        data: Optional additional error data
        
    Returns:
        JSONResponse with error
    """
    error = JSONRPCError(
        code=code,
        message=message,
        data=data
    )
    
    response = JSONRPCResponse(
        jsonrpc="2.0",
        id=id,
        error=error
    )
    
    # Map error codes to HTTP status codes
    status_map = {
        JSONRPCErrorCode.PARSE_ERROR: 400,
        JSONRPCErrorCode.INVALID_REQUEST: 400,
        JSONRPCErrorCode.METHOD_NOT_FOUND: 404,
        JSONRPCErrorCode.INVALID_PARAMS: 400,
        JSONRPCErrorCode.INTERNAL_ERROR: 500,
    }
    
    status_code = status_map.get(code, 500)
    
    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=status_code
    )


# ============================================================================
# Main Entry Point
# ============================================================================


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 5001))
    
    logger.info(f"Starting server on port {port}...")
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
