# Agent Documentation

This document describes the STT (Speech-to-Text) project for AI agents and developers.

## Project Overview

**STT** is a cross-platform command-line tool for recording audio and transcribing it using Whisper.cpp. It supports multiple languages and can copy transcriptions to clipboard or save to file.

### Key Features

- Cross-platform (Windows, macOS, Linux)
- Multiple language support (English, Portuguese, extensible)
- Two output modes: clipboard or file
- Uses Whisper.cpp for local, offline transcription
- Easy launcher scripts for common workflows

## Project Structure

```
stt/
├── src/                          # Python source code
│   ├── __main__.py              # Entry point
│   ├── cli.py                   # Command-line argument parsing
│   ├── audio.py                 # Audio recording functionality
│   ├── transcribe.py            # Whisper.cpp integration
│   └── clipboard.py             # Cross-platform clipboard operations
├── whisper/
│   ├── models/                  # Pre-downloaded Whisper models
│   │   └── ggml-medium.bin      # Medium model (default, ~1.5GB)
│   └── download-ggml-model.sh   # Model download script
├── recordings/                   # Temporary audio files (gitignored)
├── transcripts/                  # Output transcription files (gitignored)
├── pyproject.toml               # Python project configuration
├── uv.lock                       # Locked dependency versions (gitignored)
├── README.md                     # User documentation
├── AGENTS.md                     # This file
├── .gitignore                    # Git exclusions
├── stt-{en,pt}-{clipboard,file}.{sh,bat}        # Standard launcher scripts
└── stt-{en,pt}-clipboard-{fast,timeout}.{sh,bat}  # Clipboard variants (fast/timeout modes)
```

## Technology Stack

### Dependencies

- **Python 3.10+** - Core language
- **numpy 2.4.0** - Numerical computing
- **scipy 1.16.3** - Scientific computing
- **sounddevice 0.5.3** - Audio input/capture
- **pyperclip 1.11.0** - Clipboard access fallback
- **cffi 2.0.0** - C Foreign Function Interface

### Build & Package Management

- **uv** - Fast Python package manager (Homebrew installation)
- **CMake 4.2.1** - Build system for whisper.cpp
- **whisper-cpp 1.8.2** - Homebrew package providing `whisper-cli` binary

### Platforms

- **macOS** (Apple Silicon via Homebrew)
- **Windows** (via .bat launcher scripts)
- **Linux** (via .sh launcher scripts)

## Core Modules

### `src/__main__.py`

Entry point that orchestrates the workflow:

1. Imports and validates all dependencies
2. Calls the CLI parser
3. Handles errors and user feedback

### `src/cli.py`

Command-line interface:

- Argument parsing for `--lang`, `--model`, `--no-clipboard` flags
- Workflow coordination
- Default: English language, medium model, clipboard output

### `src/audio.py`

Audio recording:

- Lists available audio input devices
- Records audio at 16kHz sample rate
- Saves to temporary WAV file
- Handles device selection and timeouts

### `src/transcribe.py`

Whisper.cpp integration:

- Detects `whisper-cli` (Homebrew) or `whisper-cpp` binaries
- Constructs command with model path and audio file
- Handles platform-specific command execution
- Returns transcribed text

### `src/clipboard.py`

Cross-platform clipboard operations:

- Uses pyperclip for automatic platform detection
- Supports macOS, Linux, and Windows
- Provides unified clipboard interface across all platforms

## Workflow

### User Flow

1. User runs launcher script (e.g., `./stt-en-clipboard.sh`)
2. System prompts user to press Enter when ready to record
3. Audio recorded until Enter is pressed again
4. Transcription runs via whisper.cpp
5. Result copied to clipboard or saved to file

### Launcher Script Variants

**Standard scripts** (8 total):

- `stt-en-clipboard.{sh,bat}` - English, clipboard output with manual close
- `stt-en-file.{sh,bat}` - English, file output with manual close
- `stt-pt-clipboard.{sh,bat}` - Portuguese, clipboard output with manual close
- `stt-pt-file.{sh,bat}` - Portuguese, file output with manual close

**Clipboard variants** (4 additional for clipboard modes):

- `stt-en-clipboard-fast.{sh,bat}` - Exit immediately after transcription (no pause)
- `stt-en-clipboard-timeout.{sh,bat}` - Auto-close after 2 seconds
- `stt-pt-clipboard-fast.{sh,bat}` - Portuguese, exit immediately
- `stt-pt-clipboard-timeout.{sh,bat}` - Portuguese, auto-close after 2 seconds

**Choice guide:**

- Use **standard** scripts when you want to review results before closing
- Use **fast** scripts for quick transcription into clipboard (useful for hotkeys/automation)
- Use **timeout** scripts for unattended workflows (show result briefly then close)

### Internal Execution

```
launcher script → uv run python -m src [options]
  ↓
__main__.py
  ├→ cli.py (parse args)
  ├→ audio.py (record WAV)
  ├→ transcribe.py (process with whisper-cli)
  └→ clipboard.py (output result)
```

## Key Design Decisions

1. **Binary Detection**: The code detects `whisper-cli` (Homebrew) first, then `whisper-cpp`. This accommodates both Homebrew and source-built installations.

2. **Platform-Agnostic Source Code**: Core Python code has minimal platform checks. Platform differences handled via:
   - System command availability detection (clipboard, binary paths)
   - Launcher scripts (.sh for Unix, .bat for Windows)

3. **No Windows-Specific Documentation**: Documentation is OS-agnostic in README.md. Windows is supported through .bat launcher scripts that match Unix counterparts.

4. **CPU-Only by Default**: Whisper.cpp runs on CPU. GPU acceleration (CUDA/Metal) is optional; users must rebuild whisper-cpp themselves if desired.

5. **Model Management**: Large model files excluded from git via .gitignore. Users download models on first setup using the provided script.

## Development Notes

### Adding a New Language

1. Add language option to `src/cli.py` argument parser
2. Create new launcher script: `stt-{lang}-{mode}.sh` and `.bat`
3. Update README.md with usage examples

### Modifying Audio Input

Edit `src/audio.py`:

- Change `channels=1` for stereo
- Adjust `duration=None` for timeout
- Modify sample rate from `samplerate=16000`

### Binary Detection Issues

If transcription fails, debug in `src/transcribe.py`:

- `get_whisper_cpp_path()` finds the binary
- Check which `whisper-cli` or `which whisper-cpp` commands work on your system
- Verify model file exists at expected path

### Git Exclusions

The `.gitignore` excludes:

- Python cache and virtual environments
- Audio recordings and transcripts
- Large binary model files (*.bin)
- Locked dependency file (uv.lock)
- macOS system files (.DS_Store)

## Common Issues & Solutions

### "No module named 'sounddevice'"

Run `uv sync` to install dependencies.

### "whisper-cli not found"

Install via Homebrew: `brew install whisper-cpp`

### "No audio devices detected"

Check system audio settings; ensure microphone is set as default recording device.

### Recording not working on Linux

May need ALSA configuration; see sounddevice documentation.

## Future Enhancements

- Real-time transcription display
- Language auto-detection
- Multiple output formats (JSON, VTT)
- GUI alternative to CLI
- Streaming transcription for long recordings
