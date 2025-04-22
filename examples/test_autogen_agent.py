#!/usr/bin/env python3
"""
autogen_mcp_integration.py

An example integration using an autogen 0.4 agent to call the MCP server for pushing Telegram notifications.
This script:
  - Defines a tool function (mcp_send_alert) that uses an in‑memory connection to call the MCP 'send_alert' tool.
  - Creates an AssistantAgent that has access to this tool.
  - Sends a prompt to the agent to trigger a notification.
"""

import asyncio
import sys
import os
import traceback

import httpx

# Monkey-patch AsyncClient to disable SSL verification globally.
_original_init = httpx.AsyncClient.__init__

def _patched_init(self, *args, **kwargs):
    kwargs.setdefault("verify", False)
    return _original_init(self, *args, **kwargs)

httpx.AsyncClient.__init__ = _patched_init

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import the in‑memory MCP server instance from mcp_handler.py
from src.mcp_handler import mcp
from mcp.shared.memory import create_connected_server_and_client_session as create_session

# Define a tool function that calls the MCP server's "send_alert" tool using the in‑memory connection.
async def mcp_send_alert(message: str, project: str, urgency: str = "high") -> str:
    try:
        async with create_session(mcp._mcp_server) as client:
            result = await client.call_tool(
                "send_alert",
                {"message": message, "project": project, "urgency": urgency},
            )
            # Here, result is a Pydantic model (CallToolResult) with a field "content" which is a list.
            if result.content and isinstance(result.content, list):
                # Access the text attribute of the first element.
                return result.content[0].text if hasattr(result.content[0], "text") else "No text returned"
            return "No content returned from MCP tool."
    except Exception as e:
        tb = traceback.format_exc()
        print("Exception in mcp_send_alert:\n", tb)
        return f"Error calling MCP tool: {e}"

# Create an AssistantAgent that uses your MCP tool.
# (Replace "gpt-4o" with your desired model and provide API credentials as needed.)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY must be set in .env")

model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini-2024-07-18",
            api_key=OPENAI_KEY
        )

agent = AssistantAgent(
    name="notification_agent",
    model_client=model_client,
    tools=[mcp_send_alert],  # Register the MCP tool as a function tool.
    system_message=(
        "You are a notification agent. When a critical alert is needed, use the provided tool to push "
        "a notification via Telegram."
    ),
)

async def main():
    # Create a user message that instructs the agent to send an alert.
    messages = [
        TextMessage(
            content="Critical alert: the production server is down. Please send an alert now!",
            source="user"
        )
    ]
    cancellation_token = CancellationToken()
    # The agent processes the message; if it determines a tool call is needed, it will call mcp_send_alert.
    response = await agent.on_messages(messages, cancellation_token=cancellation_token)
    print("Final agent response:")
    print(response.chat_message.content)
    print("\nAgent inner messages (tool call chain):")
    for msg in response.inner_messages:
        print(msg)

if __name__ == "__main__":
    asyncio.run(main())
