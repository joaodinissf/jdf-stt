#!/bin/bash
# Speech-to-Text launcher (Portuguese, save to file)
# Run this file to record and transcribe audio to a file in Portuguese

echo "========================================"
echo "Speech-to-Text (STT) - Portuguese"
echo "========================================"
echo
echo "Model: medium"
echo "Language: Portuguese (pt)"
echo "Output: transcripts/ directory"
echo

uv run python -m src --lang pt --no-clipboard
