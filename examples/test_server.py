#!/usr/bin/env python3
"""Test script to run the MCP server standalone."""

import asyncio
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mcp_handler import main

if __name__ == "__main__":
    asyncio.run(main())