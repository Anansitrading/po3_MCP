#!/usr/bin/env python3
"""
Example script demonstrating how to use the Poe o3 MCP server.

This script shows how to connect to the MCP server and call its tools.
"""

import asyncio
import os
import sys
from pathlib import Path
import subprocess
from typing import Dict, Any, List

# Try to import mcp client, with helpful error if not installed
try:
    from mcp.client import MCPClient
except ImportError:
    print("Error: mcp package not found. Please install it with:")
    print("pip install fastmcp")
    sys.exit(1)

async def main():
    """Run the example."""
    print("Starting Poe o3 MCP client example")
    
    # Path to the server script
    server_script = Path(__file__).parent / "poe_o3_mcp_server.py"
    
    # Make sure the server script is executable
    if not os.access(server_script, os.X_OK):
        os.chmod(server_script, 0o755)
    
    # Create an MCP client that launches the server
    print(f"Connecting to MCP server at: {server_script}")
    client = MCPClient(server_command=["python", str(server_script)])
    
    # Test the ping tool
    print("Testing ping tool...")
    ping_result = await client.call_tool("ping", {})
    print(f"Ping result: {ping_result}")
    
    # If we have a Poe API key, test the o3_query tool
    if os.getenv("POE_API_KEY"):
        print("\nTesting o3_query tool...")
        query = "What are the three laws of robotics?"
        print(f"Query: {query}")
        
        try:
            o3_result = await client.call_tool("o3_query", {"message": query})
            print(f"o3 response: {o3_result}")
        except Exception as e:
            print(f"Error calling o3_query: {e}")
    else:
        print("\nSkipping o3_query test because POE_API_KEY is not set")
        print("Set your Poe API key in the .env file to test this functionality")
    
    # Close the client (which will also terminate the server)
    await client.close()
    print("\nExample completed")

if __name__ == "__main__":
    asyncio.run(main())