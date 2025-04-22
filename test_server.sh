#!/bin/bash
# Test script for running the server and client on Linux/macOS

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server in the background
echo "Starting server..."
python3 src/mcp_handler.py > server.log 2>&1 &
SERVER_PID=$!
sleep 1

# Check if server is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "Error: Server failed to start. Check server.log."
    exit 1
fi

echo "Server running with PID $SERVER_PID"
echo "Running test client..."

# Run the test client
python3 examples/test_client.py

# Clean up
kill $SERVER_PID
echo "Server stopped."