"""Clipboard operations for cross-platform systems"""

import sys

import pyperclip


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to system clipboard using pyperclip.

    Pyperclip works on:
    - Linux (xclip, xsel, or wl-copy)
    - macOS (pbcopy)
    - Windows (clip.exe)
    - WSL (clip.exe)

    Args:
        text: Text to copy to clipboard

    Returns:
        True if successful, False otherwise
    """
    if not text:
        print("Error: No text provided to copy to clipboard", file=sys.stderr)
        return False

    try:
        pyperclip.copy(text)
        print("✓ Copied to clipboard", file=sys.stderr)
        return True
    except Exception as e:
        print(f"Error: Could not copy to clipboard: {e}", file=sys.stderr)
        return False


def check_clipboard_available() -> bool:
    """Check if clipboard functionality is available"""
    try:
        pyperclip.copy("")
        return True
    except Exception:
        return False
