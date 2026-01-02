#!/bin/bash
# Speech-to-Text launcher
# Run this file to record and transcribe audio

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
echo "Press Enter to close..."
read
