#!/bin/bash
# Speech-to-Text launcher (timeout mode)
# Run this file to record and transcribe audio
# Auto-closes after 2 seconds (no manual input needed)

# Change to script directory
cd "$(dirname "$0")" || exit

echo "========================================"
echo "Speech-to-Text (STT)"
echo "========================================"
echo
echo "Model: medium"
echo

uv run python -m src

echo
echo "Closing in 2 seconds..."
sleep 2
