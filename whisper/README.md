# Whisper.cpp Models

This directory stores Whisper models used for speech-to-text transcription.

## Downloading Models

Models are managed by the original whisper.cpp repository. To download a model, use the official download script from:

**https://github.com/ggerganov/whisper.cpp/blob/master/models/download-ggml-model.sh**

### Quick Download

To download the medium model (recommended, ~1.5GB):

```bash
# From the project root:
curl -L https://raw.githubusercontent.com/ggerganov/whisper.cpp/master/models/download-ggml-model.sh | bash -s -- medium
```

Or download and run the script manually:

```bash
cd whisper/models
wget https://raw.githubusercontent.com/ggerganov/whisper.cpp/master/models/download-ggml-model.sh
bash download-ggml-model.sh medium
cd ../..
```

### Available Models

- `tiny` - ~75MB (fastest, least accurate)
- `base` - ~140MB
- `small` - ~466MB
- `medium` - ~1.5GB (default, good balance)
- `large` - ~2.9GB (slowest, most accurate)

### Manual Download

Alternatively, download models directly from Hugging Face:

```bash
cd whisper/models
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin
cd ../..
```

Replace `medium` with the desired model size.

## File Organization

```txt
whisper/
├── README.md          # This file
├── models/            # Downloaded models go here
│   └── ggml-*.bin     # Model files (gitignored)
```

## Notes

- Model files (.bin) are large and gitignored
- Only download the models you need
- The download script can be run multiple times safely (checks for existing files)
