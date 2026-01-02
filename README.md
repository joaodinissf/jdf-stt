# jdf-stt: Speech-to-Text (STT) Tool

A cross-platform speech-to-text transcription tool using Whisper.cpp.

## Prerequisites

- **Python 3.10+**
- **Git**
- **CMake**
- **C++ Compiler**

### GPU Acceleration (Optional)

For faster transcription with GPU acceleration, build whisper.cpp with CUDA/Metal support. By default, whisper.cpp uses CPU-only processing.

## Installation

### 1. Clone or navigate to the project directory

```bash
cd stt
```

### 2. Install UV Package Manager

UV is a fast Python package manager. See installation instructions at: <https://docs.astral.sh/uv/getting-started/installation/>

### 3. Install Python Dependencies

```bash
uv sync
```

### 4. Set up Whisper.cpp

Download the Whisper model:

```bash
cd whisper/models
bash ../download-ggml-model.sh medium
cd ../..
```

## Usage

### Using convenience scripts

The easiest way to run STT is using the provided launcher scripts:

**English, copy to clipboard:**

```bash
./stt-en-clipboard.sh   # Linux/macOS
stt-en-clipboard.bat    # Windows
```

**English, save to file:**

```bash
./stt-en-file.sh        # Linux/macOS
stt-en-file.bat         # Windows
```

**Portuguese, copy to clipboard:**

```bash
./stt-pt-clipboard.sh   # Linux/macOS
stt-pt-clipboard.bat    # Windows
```

**Portuguese, save to file:**

```bash
./stt-pt-file.sh        # Linux/macOS
stt-pt-file.bat         # Windows
```

### Using the command line directly

```bash
# Record and copy to clipboard
uv run python -m src

# With language selection
uv run python -m src --lang pt

# Save to file instead of clipboard
uv run python -m src --no-clipboard

# Use different model
uv run python -m src --model base
```

## Command-Line Options

```
--no-clipboard          # Save to file instead of clipboard
--lang LANG             # Language code (en, pt, es, fr, de, ja, zh, etc.)
--model MODEL           # Whisper model (tiny, base, small, medium, large)
--output-dir DIR        # Custom output directory for transcripts
--help                  # Show usage information
```

## Troubleshooting

### sounddevice ImportError

Run the installation again:

```bash
uv sync
```

### No audio devices detected

Make sure your microphone is:

1. Plugged in and enabled
2. Set as default recording device in system audio settings
3. Not being used by another application

## Rebuilding whisper.cpp

If you need to rebuild whisper.cpp:

```bash
cd whisper
cmake -B build
cmake --build build -j
```

## Next Steps

After installation, try recording some audio:

```bash
uv run python -m src --lang en --model medium
```

Press Enter when you're done speaking. The transcription will be copied to your clipboard!
