#!/bin/bash
# Speech-to-Text launcher (fast mode)
# Run this file to record and transcribe audio
# Exits immediately after transcription (no pause)

# Change to script directory
cd "$(dirname "$0")" || exit

echo "========================================"
echo "Speech-to-Text (STT)"
echo "========================================"
echo
echo "Model: medium"
echo

uv run python -m src
