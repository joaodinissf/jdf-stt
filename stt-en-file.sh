#!/bin/bash
# Speech-to-Text launcher (save to file)
# Run this file to record and transcribe audio to a file

echo "========================================"
echo "Speech-to-Text (STT) - Save to File"
echo "========================================"
echo
echo "Model: medium"
echo "Output: transcripts/ directory"
echo

uv run python -m src --no-clipboard
