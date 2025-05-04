#!/bin/bash

# Set test file path
TEST_FILE="test.wav"

# Check if file exists
if [ ! -f "$TEST_FILE" ]; then
    echo "Error: Test file $TEST_FILE not found"
    exit 1
fi

# Convert file to base64
BASE64_DATA=$(base64 -w 0 "$TEST_FILE")

# Test with Python directly
#echo "Testing voice identification with base64 data:"
#echo '{"jsonrpc": "2.0", "method": "identify_voice_base64", "params": {"base64_data": "'$BASE64_DATA'"}, "id": 1}' | python stdio_server.py

# Test with executable (if exists)
if [ -f "dist/voice_stdio" ]; then
    echo -e "\nTesting with executable:"
    echo '{"jsonrpc": "2.0", "method": "identify_voice_base64", "params": {"base64_data": "'$BASE64_DATA'"}, "id": 1}' | ./dist/voice_stdio
else
    echo -e "\nExecutable not found. Please build it first using: python build.py"
fi 
