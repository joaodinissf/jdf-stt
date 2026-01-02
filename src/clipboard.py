"""Clipboard operations for cross-platform systems"""

import sys
import subprocess
from pathlib import Path


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to system clipboard.

    Works on:
    - Linux (using xclip or xsel)
    - macOS (using pbcopy)
    - Windows (using clip.exe)
    - WSL (using clip.exe)

    Args:
        text: Text to copy to clipboard

    Returns:
        True if successful, False otherwise
    """
    if not text:
        print("Error: No text provided to copy to clipboard", file=sys.stderr)
        return False

    # Try different clipboard methods
    methods = [
        _copy_linux,
        _copy_macos,
        _copy_windows,
        _copy_wsl,
        _copy_pyperclip,
    ]

    for method in methods:
        if method(text):
            return True

    print("Error: Could not copy to clipboard (no method available)", file=sys.stderr)
    return False


def _copy_wsl(text: str) -> bool:
    """Copy using WSL's clip.exe"""
    try:
        # Check if clip.exe exists (WSL environment)
        clip_paths = [
            "clip.exe",  # In PATH
            "/mnt/c/Windows/System32/clip.exe",  # Direct path
        ]

        for clip_path in clip_paths:
            try:
                process = subprocess.run(
                    [clip_path],
                    input=text.encode("utf-8"),
                    capture_output=True,
                    timeout=5,
                )
                if process.returncode == 0:
                    print("✓ Copied to clipboard (WSL)", file=sys.stderr)
                    return True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue

        return False

    except Exception:
        return False


def _copy_linux(text: str) -> bool:
    """Copy using xclip or xsel on Linux"""
    try:
        # Try xclip first
        try:
            process = subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode("utf-8"),
                capture_output=True,
                timeout=5,
            )
            if process.returncode == 0:
                print("✓ Copied to clipboard (xclip)", file=sys.stderr)
                return True
        except FileNotFoundError:
            pass

        # Try xsel
        try:
            process = subprocess.run(
                ["xsel", "--clipboard", "--input"],
                input=text.encode("utf-8"),
                capture_output=True,
                timeout=5,
            )
            if process.returncode == 0:
                print("✓ Copied to clipboard (xsel)", file=sys.stderr)
                return True
        except FileNotFoundError:
            pass

        return False

    except Exception:
        return False


def _copy_macos(text: str) -> bool:
    """Copy using pbcopy on macOS"""
    try:
        process = subprocess.run(
            ["pbcopy"],
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=5,
        )
        if process.returncode == 0:
            print("✓ Copied to clipboard (pbcopy)", file=sys.stderr)
            return True
        return False

    except (FileNotFoundError, Exception):
        return False


def _copy_windows(text: str) -> bool:
    """Copy using clip.exe on Windows"""
    try:
        # Windows clip.exe needs UTF-16LE with BOM for proper Unicode handling
        # Add BOM (Byte Order Mark) to ensure proper encoding
        encoded_text = b'\xff\xfe' + text.encode("utf-16le")

        process = subprocess.run(
            ["clip"],
            input=encoded_text,
            capture_output=True,
            timeout=5,
        )
        if process.returncode == 0:
            print("✓ Copied to clipboard (clip)", file=sys.stderr)
            return True
        return False

    except (FileNotFoundError, Exception):
        return False


def _copy_wsl(text: str) -> bool:
    """Copy using WSL's clip.exe"""
    try:
        # Check if clip.exe exists (WSL environment)
        clip_paths = [
            "clip.exe",  # In PATH
            "/mnt/c/Windows/System32/clip.exe",  # Direct path
        ]

        for clip_path in clip_paths:
            try:
                process = subprocess.run(
                    [clip_path],
                    input=text.encode("utf-8"),
                    capture_output=True,
                    timeout=5,
                )
                if process.returncode == 0:
                    print("✓ Copied to clipboard (WSL)", file=sys.stderr)
                    return True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue

        return False

    except Exception:
        return False


def _copy_pyperclip(text: str) -> bool:
    """Fallback to pyperclip library"""
    try:
        import pyperclip

        pyperclip.copy(text)
        print("✓ Copied to clipboard (pyperclip)", file=sys.stderr)
        return True

    except Exception:
        return False


def check_clipboard_available() -> bool:
    """Check if clipboard functionality is available"""
    # Try to copy an empty string to test
    test_methods = [
        lambda: subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=b"",
            capture_output=True,
            timeout=1,
        ).returncode
        == 0,
        lambda: subprocess.run(
            ["pbcopy"], input=b"", capture_output=True, timeout=1
        ).returncode
        == 0,
        lambda: subprocess.run(
            ["clip.exe"], input=b"", capture_output=True, timeout=1
        ).returncode
        == 0,
    ]

    for test in test_methods:
        try:
            if test():
                return True
        except Exception:
            continue

    # Try pyperclip as last resort
    try:
        import pyperclip

        return True
    except ImportError:
        pass

    return False
