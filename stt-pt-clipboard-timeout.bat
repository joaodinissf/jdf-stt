@echo off
REM Speech-to-Text launcher (Portuguese, timeout mode)
REM Double-click this file to record and transcribe audio in Portuguese
REM Auto-closes after 2 seconds (no manual input needed)

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

echo.
echo Closing in 2 seconds...
timeout /t 2 /nobreak
