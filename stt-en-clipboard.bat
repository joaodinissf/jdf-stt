@echo off
REM Speech-to-Text launcher
REM Double-click this file to record and transcribe audio

REM Set console to UTF-8 for proper Unicode support
chcp 65001 >nul
set PYTHONUTF8=1

cd /d "%~dp0"

echo ========================================
echo Speech-to-Text (STT)
echo ========================================
echo.
echo Model: medium
echo.

uv run python -m src

echo.
echo ========================================
pause
