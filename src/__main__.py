"""Main entry point for stt (speech-to-text tool)"""

import sys
from datetime import datetime
from pathlib import Path

from .audio import check_audio_available, record_audio
from .cli import parse_args
from .clipboard import copy_to_clipboard
from .transcribe import check_whisper_available, transcribe_audio


def check_dependencies():
    """Check if all required dependencies are available"""
    errors = []

    if not check_whisper_available():
        errors.append("OpenAI Whisper not available")

    if not check_audio_available():
        errors.append("No audio input devices found")

    # Clipboard is optional (only needed for default behavior)
    # Don't fail if clipboard isn't available

    if errors:
        print("Error: Missing dependencies:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        print("\nRun the installation script to fix these issues.", file=sys.stderr)
        return False

    return True


def main(argv=None):
    """Main function"""
    # Parse arguments
    args = parse_args(argv)

    # Check dependencies
    if not check_dependencies():
        return 1

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create recordings directory if it doesn't exist
    recordings_dir = Path("./recordings")
    recordings_dir.mkdir(parents=True, exist_ok=True)

    audio_file = recordings_dir / f"recording_{timestamp}.wav"

    # Record audio
    print("Starting audio recording...", file=sys.stderr)
    if not record_audio(str(audio_file), args.sample_rate):
        print("Error: Audio recording failed", file=sys.stderr)
        return 1

    # Transcribe audio
    print("Transcribing audio...", file=sys.stderr)
    try:
        transcription = transcribe_audio(
            str(audio_file), model=args.model, language=args.lang
        )
    except Exception as e:
        print(f"Error: Transcription failed: {e}", file=sys.stderr)
        return 1

    if not transcription:
        print("Error: Transcription is empty", file=sys.stderr)
        return 1

    # Handle output based on --no-clipboard flag
    if args.no_clipboard:
        # Print to stdout
        print(transcription)

        # Save to timestamped file
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"transcript_{timestamp}.txt"
        output_file.write_text(transcription, encoding="utf-8")

        print(f"✓ Saved to: {output_file}", file=sys.stderr)
    else:
        # Copy to clipboard (default behavior)
        if copy_to_clipboard(transcription):
            print("✓ Transcription copied to clipboard", file=sys.stderr)
            print("\nTranscription:", file=sys.stderr)
            print(transcription)
        else:
            print("Error: Failed to copy to clipboard", file=sys.stderr)
            print("Transcription:", file=sys.stderr)
            print(transcription, file=sys.stderr)
            return 1

    # Optional: cleanup recording file
    # Uncomment the line below to auto-delete recordings
    # audio_file.unlink(missing_ok=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
