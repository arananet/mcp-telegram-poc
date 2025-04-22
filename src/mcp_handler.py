#!/usr/bin/env python3
"""
mcp_handler.py

A FastMCP-based server for sending Telegram notifications.
This version uses the official MCP SDK style.
"""
import asyncio
import os
import sys
from typing import Dict, Any
import httpx

from mcp.server.fastmcp import FastMCP
from telegram import Bot
from telegram.request import HTTPXRequest #only required if you are behind a proxy.
from telegram.error import TelegramError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in .env")

# Initialize HTTPXRequest with SSL verification disabled
request = HTTPXRequest(
    connection_pool_size=1,
    httpx_kwargs={"verify": False}
)

bot = Bot(token=BOT_TOKEN, request=request)

# Create a FastMCP server instance.
mcp = FastMCP(instructions="Telegram MCP Server")

# Register tool: send_alert
@mcp.tool()
async def send_alert(message: str, project: str, urgency: str = "medium") -> Dict[str, Any]:
    """
    Send a Telegram alert with customizable urgency.
    """
    urgency_prefix = {"high": "🚨 URGENT: ", "medium": "⚠️ ", "low": ""}.get(urgency, "⚠️ ")
    formatted_message = f"{urgency_prefix}LLM Alert ({project}):\n\n{message}"
    try:
        sent_message = await bot.send_message(
            chat_id=CHAT_ID,
            text=formatted_message,
            parse_mode="HTML"
        )
        # Set offset to only get updates after the sent message.
        offset = sent_message.message_id + 1
        # For testing, set a short overall timeout.
        overall_timeout = 20  # seconds
        start_time = asyncio.get_event_loop().time()
        while (asyncio.get_event_loop().time() - start_time) < overall_timeout:
            try:
                # Wrap get_updates with a wait_for so that if it hangs, we continue.
                updates = await asyncio.wait_for(
                    bot.get_updates(offset=offset, limit=10, timeout=1),
                    timeout=2,
                )
            except asyncio.TimeoutError:
                updates = []
            for update in updates:
                if update.message and update.message.message_id >= offset:
                    return {"content": [{"type": "text", "text": update.message.text}]}
            await asyncio.sleep(1)
        return {"content": [{"type": "text", "text": "No reply received within timeout."}]}
    except TelegramError as e:
        return {"content": [{"type": "text", "text": f"Failed to send alert: {e}"}], "isError": True}


# Register tool: check_reply
@mcp.tool()
async def check_reply(message_id: int, timeout_seconds: int = 60) -> Dict[str, Any]:
    """
    Check for replies to a specific message ID.
    """
    offset = message_id + 1
    start_time = asyncio.get_event_loop().time()
    try:
        while (asyncio.get_event_loop().time() - start_time) < timeout_seconds:
            updates = await bot.get_updates(offset=offset, limit=10, timeout=1)
            for update in updates:
                if update.message and update.message.message_id >= offset:
                    return {"content": [{"type": "text", "text": update.message.text}]}
            await asyncio.sleep(1)
        return {"content": [{"type": "text", "text": "No reply received within timeout."}]}
    except TelegramError as e:
        return {"content": [{"type": "text", "text": f"Failed to check reply: {e}"}], "isError": True}

def main():
    # For standalone use you can run the server on its default transport.
    sys.stderr.write("Starting Telegram MCP server...\n")
    mcp.run()

if __name__ == "__main__":
    main()
