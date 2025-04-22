#!/usr/bin/env python3
"""
test_client.py

Test script demonstrating client interaction with the Telegram MCP Server.
Uses an in-memory connection via the SDK’s create_connected_server_and_client_session.
"""

import asyncio
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import httpx

# Monkey-patch AsyncClient to disable SSL verification globally.
_original_init = httpx.AsyncClient.__init__

def _patched_init(self, *args, **kwargs):
    kwargs.setdefault("verify", False)
    return _original_init(self, *args, **kwargs)

httpx.AsyncClient.__init__ = _patched_init

from mcp.shared.memory import create_connected_server_and_client_session as create_session

# Import the server instance.
# This allows the client to connect directly to the in‑memory server.
from src.mcp_handler import mcp

async def test_client():
    async with create_session(mcp._mcp_server) as client:
        # List available tools
        tools_result = await client.list_tools()
        tool_names = [tool.name for tool in tools_result.tools]
        print("Available tools:", tool_names)

        # Call the send_alert tool
        result = await client.call_tool(
            "send_alert",
            {"message": "Hello from test_client!", "project": "Test", "urgency": "high"},
        )
        # For demonstration, print the first content's text.
        if result.content:
            print("Send alert result:", result.content[0].text)
        else:
            print("No content received.")

if __name__ == "__main__":
    asyncio.run(test_client())
