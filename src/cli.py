"""Command-line argument parsing for stt"""

import argparse


def create_parser():
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog="stt",
        description="Speech-to-text tool using OpenAI Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  stt                                  # Record and copy to clipboard
  stt --lang pt                        # Portuguese transcription
  stt --no-clipboard                   # Save to file instead
  stt --model medium --lang en         # Use medium model
  stt --output-dir ~/Documents/stt     # Custom output directory

For more information, visit: https://github.com/yourusername/stt
        """,
    )

    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Save to file and print to stdout instead of copying to clipboard",
    )

    parser.add_argument(
        "--lang",
        type=str,
        default="en",
        help="Language code for transcription (default: en). Examples: en, pt, es, fr, de, ja, zh",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: medium)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="./transcripts",
        help="Custom output directory for transcripts (default: ./transcripts)",
    )

    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="Audio sample rate in Hz (default: 16000)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    return parser


def parse_args(argv=None):
    """Parse command-line arguments"""
    parser = create_parser()
    args = parser.parse_args(argv)
    return args
