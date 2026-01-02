@echo off
REM Speech-to-Text launcher (save to file)
REM Double-click this file to record and transcribe audio to a file

REM Set console to UTF-8 for proper Unicode support
chcp 65001 >nul
set PYTHONUTF8=1

cd /d "%~dp0"

echo ========================================
echo Speech-to-Text (STT) - Save to File
echo ========================================
echo.
echo Model: medium
echo Output: transcripts/ directory
echo.

uv run python -m src --no-clipboard

echo.
echo ========================================
pause
