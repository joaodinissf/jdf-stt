#!/bin/bash
# Speech-to-Text launcher (Portuguese, timeout mode)
# Run this file to record and transcribe audio in Portuguese
# Auto-closes after 2 seconds (no manual input needed)

# Change to script directory
cd "$(dirname "$0")" || exit

echo "========================================"
echo "Speech-to-Text (STT) - Portuguese"
echo "========================================"
echo
echo "Model: medium"
echo "Language: Portuguese (pt)"
echo

uv run python -m src --lang pt

echo
echo "Closing in 2 seconds..."
sleep 2
