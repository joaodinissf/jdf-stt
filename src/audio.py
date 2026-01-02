"""Audio recording using sounddevice"""

import sys
from pathlib import Path
from typing import Any

import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd


def list_audio_devices() -> list[Any]:
    """List all available audio devices"""
    return sd.query_devices()  # type: ignore[return-value]


def get_default_input_device() -> dict[str, Any]:
    """Get the default input device"""
    return sd.query_devices(kind="input")  # type: ignore[return-value]


def record_audio(output_path: str, sample_rate: int = 16000) -> bool:
    """
    Record audio from microphone until user presses Enter.

    Args:
        output_path: Path to save the recorded audio (WAV format)
        sample_rate: Sample rate in Hz (default: 16000)

    Returns:
        True if recording successful, False otherwise
    """
    try:
        print(f"Recording audio at {sample_rate}Hz...", file=sys.stderr)
        print("Press ENTER to stop recording.", file=sys.stderr)

        # List available devices for debugging
        default_device = get_default_input_device()
        print(f"Using microphone: {default_device['name']}", file=sys.stderr)

        # Start recording in a separate thread
        recording = []

        def callback(indata, frames, time, status):
            """Called for each audio block from the stream"""
            if status:
                print(f"Recording status: {status}", file=sys.stderr)
            recording.append(indata.copy())

        # Open input stream
        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype=np.float32,
            callback=callback,
        ):
            # Wait for user to press Enter
            input()

        print("Recording stopped.", file=sys.stderr)

        # Check if we recorded anything
        if not recording:
            print("Error: No audio data recorded", file=sys.stderr)
            return False

        # Concatenate all chunks
        audio_data = np.concatenate(recording, axis=0)

        # Convert float32 to int16 for WAV format
        audio_data = (audio_data * 32767).astype(np.int16)

        # Ensure output directory exists
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save as WAV file
        wavfile.write(output_path, sample_rate, audio_data)

        print(f"Recording saved: {output_path}", file=sys.stderr)
        return True

    except Exception as e:
        print(f"Error recording audio: {e}", file=sys.stderr)
        return False


def check_audio_available() -> bool:
    """Check if audio input devices are available"""
    try:
        devices = sd.query_devices()  # type: ignore[assignment]
        input_devices = [
            d
            for d in devices
            if isinstance(d, dict) and d.get("max_input_channels", 0) > 0
        ]

        if not input_devices:
            print("Error: No audio input devices found", file=sys.stderr)
            return False

        return True

    except Exception as e:
        print(f"Error checking audio devices: {e}", file=sys.stderr)
        return False
