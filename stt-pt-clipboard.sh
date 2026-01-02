#!/bin/bash
# Speech-to-Text launcher (Portuguese)
# Run this file to record and transcribe audio in Portuguese

echo "========================================"
echo "Speech-to-Text (STT) - Portuguese"
echo "========================================"
echo
echo "Model: medium"
echo "Language: Portuguese (pt)"
echo

uv run python -m src --lang pt
