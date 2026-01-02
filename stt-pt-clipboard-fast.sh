#!/bin/bash
# Speech-to-Text launcher (Portuguese, fast mode)
# Run this file to record and transcribe audio in Portuguese
# Exits immediately after transcription (no pause)

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
