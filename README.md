# MCP Integration example with Telegram

A Python-based Model Context Protocol (MCP) client and server that enables LLMs to send notifications via Telegram and receive user responses.

## Features
- Send text alerts to a Telegram chat with customizable urgency levels
- Check for user replies with configurable timeouts
- Flexible template for integration with MCP-compatible LLM applications

## MCP vs Function Calls or Agent tools

### MCP Protocol (Model Context Protocol):
- Separates the LLM’s reasoning (the “context”) from the execution of external actions. For example, the LLM decides what action to take and the MCP server handles how to execute that action.
- This decoupling means you can update or swap out external tools without changing the core LLM model or its prompts.
- It also allows for safer and more controlled execution of actions.

### LLM Function Call or Agent:
- Direct function calls or agent-based methods often mix decision-making and execution logic, which can make the system less modular.
- Changes in how an action is performed may require reengineering the agent or modifying the LLM’s prompts, making maintenance harder.

## Prerequisites
- Python 3.11+
- A Telegram bot token (from [@BotFather](https://t.me/botfather))
- Your Telegram chat ID

## Installation
1. Clone the repository:
   ```bash
   git git@github.com:arananet/mcp-telegram-poc.git
   cd mcp-telegram-poc
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create the virtual environment:
   ```bash
   python3 -m venv .venv
   ```
4. Copy `.env.example` to `.env` and fill in your Telegram credentials:
   ```bash
   cp .env.example .env
   nano .env
   ```

## Configuration
Edit `.env` with:
- TELEGRAM_BOT_TOKEN=your_bot_token_here
- TELEGRAM_CHAT_ID=your_chat_id_here
- OPENAI_API_KEY=your_openai_apikey

### Getting a Telegram Bot Token
1. Chat with [@BotFather](https://t.me/botfather) on Telegram.
2. Send `/newbot` and provide a name (e.g. mcp_example) and then provide an user name (e.g. mcp_example_bot) after this telegram botfather will reply with the token.
3. Copy the token provided.

### Finding Your Chat ID
1. Send a message to your bot (go to the created bot and send some example, e.g. hi).
2. Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`.
3. Find the `chat` object's `id` field. You will see something like this (e.g. "chat":{"id":107184517,"first_name":"Edu","last_name":"Arana"...) the Chat ID is 107184517.

## Usage
### Running Standalone
```bash
python3 src/mcp_handler.py
```

### Programmatic Usage
For testing sending and receiving an alert:
```bash
python3 examples/test_client.py
```

### Agent integration
For testing the integration of the MCP using an agent with autogen 0.4 framework
```bash
python3 examples/test_autogen_agent.py
```

### Testing Locally
Use the test script (Linux/macOS):
```bash
chmod +x test_server.sh
./test_server.sh
```

## Available Tools
### `send_alert`
- **Parameters**:
  - `message` (str, required): Message to send (Markdown supported).
  - `project` (str, required): Project name.
  - `urgency` (str, optional): "low", "medium", "high" (default: "medium").
- **Description**: Sends a Telegram alert and waits for a reply.

### `check_reply`
- **Parameters**:
  - `message_id` (int, required): Message ID to check.
  - `timeout_seconds` (int, optional): Wait time (default: 60).
- **Description**: Polls for replies to a specific message.

## Development
- **Install dependencies**: `pip install -r requirements.txt`
- **Run server**: `python3 src/mcp_handler.py`
- **Test client**: `python3 examples/test_client.py`
- **Test Agent**: `python3 examples/test_autogen_agent.py`

## Examples
The `examples` folder contains:
- `test_server.py`: Runs the server standalone.
- `test_client.py`: Demonstrates client interaction.
- `test_autogen_agent.py`: Demostrates the MCP integration between an AutoGen Agent

- In the images folder you can find some screenshots of the testings.

## Developer
- Eduardo Arana
  
## Availability
- Certified by MCPHub https://mcphub.com/mcp-servers/arananet/mcp-telegram-poc
