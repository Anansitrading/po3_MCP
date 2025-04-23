#!/usr/bin/env python3
"""
Poe o3 MCP Server

A minimal MCP server implementation that integrates with the Poe API
to access the o3 model. This implementation only handles text input and output,
focusing on compatibility with Claude models on Windsurf.
"""

import logging
import os
import sys
import re
from pathlib import Path

# Configure logging first
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.DEBUG
)

# Ensure stdout is line-buffered
sys.stdout.reconfigure(line_buffering=True)

# Load environment variables from .env file
from dotenv import load_dotenv
# Get the directory of the current script
script_dir = Path(__file__).resolve().parent
env_path = script_dir / '.env'
print(f"Poe MCP Server Script: Looking for .env file at: {env_path}", flush=True)
load_dotenv(dotenv_path=env_path)

import asyncio
import json
from typing import Optional, Dict, Any, List, Tuple
# Updated imports based on actual fastmcp 2.2.1 module structure
from fastmcp import FastMCP
# Correct import path for TextContent
from mcp.types import TextContent
# Import the local PoeClient instead of fastapi_poe
from poe_client import PoeClient

print("Poe MCP Server Script: Starting imports", flush=True)
api_key = os.getenv("POE_API_KEY")
print(f"Poe MCP Server Script: Loaded environment variables, POE_API_KEY exists: {bool(api_key)}", flush=True)
if not api_key:
    print("WARNING: POE_API_KEY not found in environment variables. Please check your .env file.", flush=True)
    print(f"Current environment variables: {list(os.environ.keys())}", flush=True)

# Custom JSON encoder for MCP protocol
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)

def parse_model_flag(message: str) -> Tuple[str, str]:
    """
    Parse the message to extract model flag and clean the message.
    
    Args:
        message: The input message that may contain a model flag
        
    Returns:
        A tuple containing (cleaned_message, model_name)
        If no model flag is found, model_name will be "o3" (default)
    """
    # Default model
    model_name = "o3"
    
    # Pattern to match --ModelName at word boundaries
    # (?<!\S) ensures we only match flags at the start of a string or after whitespace
    # [a-zA-Z0-9.-]+ matches letters, numbers, dots, and hyphens in the flag name
    # (?=\s|$) ensures the flag ends at whitespace or the end of the string
    pattern = r'(?<!\S)--([\w.-]+)(?=\s|$)'
    
    # Search for the pattern
    match = re.search(pattern, message)
    if match:
        # Extract the model name (already without the -- prefix due to capture group)
        model_name = match.group(1)
        # Remove the flag from the message and normalize whitespace
        message = re.sub(r'(?<!\S)--[\w.-]+\s*', ' ', message).strip()
        # Replace multiple spaces with a single space
        message = re.sub(r'\s+', ' ', message)
        print(f"Poe MCP Server Script: Detected model flag, using model: {model_name}", flush=True)
    
    return message, model_name

# Create the MCP server with stdio transport (now handled automatically)
server = FastMCP(
    name="Poe o3 Server",  # Changed from 'title' to 'name'
)
print("Poe MCP Server Script: FastMCP server object created", flush=True)

@server.tool(name="o3_query", description="Query the OpenAI o3 model via Poe")
async def o3_query(message: str) -> List[TextContent]:
    """
    Send a text query to the o3 model on Poe and return the response.
    
    Args:
        message: The message to send to the o3 model
    """
    print(f"Poe MCP Server Script: o3_query tool called with message: {message[:50]}...", flush=True)
    
    api_key = os.getenv("POE_API_KEY")
    if not api_key:
        error_msg = "POE_API_KEY environment variable not set in .env file"
        print(f"ERROR: {error_msg}", flush=True)
        return [TextContent(type="text", text=error_msg)]
    
    try:
        # Parse the message to extract model flag
        cleaned_message, model_name = parse_model_flag(message)
        
        # Use the local PoeClient instead of fp.Client
        client = PoeClient(api_key=api_key)
        print("Poe MCP Server Script: Created Poe client", flush=True)
        
        print(f"Poe MCP Server Script: Sending request to Poe model: {model_name}", flush=True)
        # Use the async method from PoeClient
        full_response_str = await client.send_message(
            content=cleaned_message,
            bot_name=model_name
        )
        
        # Ensure the result is definitely a string before creating TextContent
        if not isinstance(full_response_str, str):
            raise TypeError(f"PoeClient.send_message returned unexpected type: {type(full_response_str)}")
            
    except Exception as e:
        error_msg = f"Error querying Poe model: {str(e)}"
        print(f"Poe MCP Server Script: {error_msg}", flush=True)
        return [TextContent(type="text", text=error_msg)]
    
    print(f"Poe MCP Server Script: Full response received, length: {len(full_response_str)}", flush=True)
    return [TextContent(type="text", text=full_response_str)]

@server.tool(name="ping", description="Simple ping tool for testing")
def ping() -> List[TextContent]:
    """A simple synchronous tool that returns 'pong'."""
    print("Poe MCP Server Script: ping tool executed", flush=True)
    # Return as a list of TextContent objects
    return [TextContent(type="text", text="pong")]

if __name__ == "__main__":
    print("Poe MCP Server Script: Entering main execution block", flush=True)
    # Run the server (transport is now handled automatically)
    server.run()
    print("Poe MCP Server Script: server.run() finished?", flush=True) # Should not be reached if run blocks