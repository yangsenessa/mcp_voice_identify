#!/bin/bash

# Set test file path
TEST_FILE="test.wav"

# Check if file exists
if [ ! -f "$TEST_FILE" ]; then
    echo "Error: Test file $TEST_FILE not found"
    exit 1
fi

# Test with Python directly
echo "Testing voice identification:"
echo '{"jsonrpc": "2.0", "method": "identify_voice", "params": {"file_path": "'$TEST_FILE'"}, "id": 1}' | python stdio_server.py

# Test with executable (if exists)
if [ -f "dist/voice_stdio" ]; then
    echo -e "\nTesting with executable:"
    echo '{"jsonrpc": "2.0", "method": "identify_voice", "params": {"file_path": "'$TEST_FILE'"}, "id": 1}' | ./dist/voice_stdio
else
    echo -e "\nExecutable not found. Please build it first using: python build.py"
fi 