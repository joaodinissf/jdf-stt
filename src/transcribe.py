"""Whisper transcription using whisper.cpp binary"""

import sys
import subprocess
import platform
from pathlib import Path


def get_whisper_cpp_path() -> Path:
    """Get the path to whisper.cpp binary"""
    # Check in the expected installation directory
    script_dir = Path(__file__).parent.parent
    whisper_dir = script_dir / "whisper"

    # Try different possible binary names based on platform
    possible_binaries = [
        # New simplified structure
        whisper_dir / "bin" / "whisper-cli.exe",
        whisper_dir / "bin" / "main.exe",
        whisper_dir / "bin" / "whisper-cli",
        whisper_dir / "bin" / "main",
        # Legacy whisper.cpp directory structure (for backwards compatibility)
        script_dir / "whisper.cpp" / "build" / "bin" / "whisper-cli.exe",
        script_dir / "whisper.cpp" / "build" / "bin" / "main.exe",
        script_dir / "whisper.cpp" / "build" / "bin" / "whisper-cli",
        script_dir / "whisper.cpp" / "build" / "bin" / "main",
        # System paths
        Path.home() / ".local" / "bin" / "whisper-cpp",
    ]

    for binary in possible_binaries:
        if binary.exists() and binary.is_file():
            return binary

    # Try to find in PATH (platform-specific command)
    try:
        if platform.system() == "Windows":
            # Windows uses 'where' command
            result = subprocess.run(
                ["where", "whisper-cli.exe"],
                capture_output=True,
                text=True,
                check=False
            )
        else:
            # Unix uses 'which' command - try whisper-cli first (Homebrew), then whisper-cpp
            result = subprocess.run(
                ["which", "whisper-cli"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                result = subprocess.run(
                    ["which", "whisper-cpp"],
                    capture_output=True,
                    text=True,
                    check=False
                )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip().split('\n')[0])
    except Exception:
        pass

    raise FileNotFoundError(
        "whisper.cpp binary not found. Please install whisper-cpp (brew install whisper-cpp) or build it with ./install.sh"
    )


def get_model_path(model: str) -> Path:
    """Get the path to the whisper.cpp model file"""
    script_dir = Path(__file__).parent.parent

    # Try new simplified structure first, then legacy
    possible_model_dirs = [
        script_dir / "whisper" / "models",
        script_dir / "whisper.cpp" / "models",
    ]

    # whisper.cpp model filename format: ggml-{model}.bin
    for models_dir in possible_model_dirs:
        model_file = models_dir / f"ggml-{model}.bin"
        if model_file.exists():
            return model_file

    raise FileNotFoundError(
        f"Model file not found: ggml-{model}.bin\n"
        f"Please download from: https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-{model}.bin\n"
        f"Save to: {script_dir / 'whisper' / 'models' / f'ggml-{model}.bin'}"
    )


def transcribe_audio(audio_path: str, model: str = "medium", language: str = "en") -> str:
    """
    Transcribe audio file using whisper.cpp binary.

    Args:
        audio_path: Path to audio file (WAV format)
        model: Whisper model size (tiny, base, small, medium, large)
        language: Language code (e.g., 'en', 'pt', 'es')

    Returns:
        Transcribed text as string

    Raises:
        FileNotFoundError: If audio file, binary, or model doesn't exist
        Exception: If transcription fails
    """
    # Check if audio file exists
    if not Path(audio_path).exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Get whisper.cpp binary and model paths
    try:
        whisper_binary = get_whisper_cpp_path()
        model_path = get_model_path(model)
    except FileNotFoundError as e:
        raise FileNotFoundError(str(e))

    print(f"Using whisper.cpp: {whisper_binary}", file=sys.stderr)
    print(f"Using model: {model_path}", file=sys.stderr)
    print(f"Transcribing with language: {language}", file=sys.stderr)

    # Prepare whisper.cpp command
    # -m: model file
    # -f: input audio file
    # -l: language
    # -nt: no timestamps in output
    # -np: no progress output
    cmd = [
        str(whisper_binary),
        "-m", str(model_path),
        "-f", str(audio_path),
        "-l", language,
        "-nt",  # No timestamps
        "-np",  # No progress
    ]

    try:
        # Run whisper.cpp
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',  # Explicitly use UTF-8 to handle Portuguese/Unicode characters
            check=True,
            timeout=300  # 5 minute timeout
        )

        # whisper.cpp outputs transcription to stdout
        transcription = result.stdout.strip()

        # Remove any [BLANK_AUDIO] markers or metadata
        transcription = transcription.replace("[BLANK_AUDIO]", "").strip()

        if not transcription:
            raise Exception("Transcription is empty. Audio may not contain speech.")

        return transcription

    except subprocess.TimeoutExpired:
        raise Exception("Transcription timed out (>5 minutes)")
    except subprocess.CalledProcessError as e:
        raise Exception(f"whisper.cpp failed: {e.stderr}")
    except Exception as e:
        raise Exception(f"Transcription failed: {e}")


def check_whisper_available() -> bool:
    """Check if whisper.cpp is installed and available"""
    try:
        whisper_binary = get_whisper_cpp_path()

        # Try to run whisper.cpp with --help to verify it works
        result = subprocess.run(
            [str(whisper_binary), "--help"],
            capture_output=True,
            timeout=5,
            check=False
        )

        if result.returncode == 0:
            return True
        else:
            print(f"Error: whisper.cpp binary found but failed to run", file=sys.stderr)
            return False

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Run ./install.sh to install whisper.cpp", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error checking whisper.cpp: {e}", file=sys.stderr)
        return False
