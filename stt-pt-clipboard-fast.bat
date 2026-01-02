@echo off
REM Speech-to-Text launcher (Portuguese, fast mode)
REM Double-click this file to record and transcribe audio in Portuguese
REM Exits immediately after transcription (no pause)

REM Set console to UTF-8 for proper Unicode support
chcp 65001 >nul
set PYTHONUTF8=1

cd /d "%~dp0"

echo ========================================
echo Speech-to-Text (STT) - Portuguese
echo ========================================
echo.
echo Model: medium
echo Language: Portuguese (pt)
echo.

uv run python -m src --lang pt
