# Speech-to-Text Converter

A Python application that converts speech to text using Sarvam AI's API. This tool supports multiple Indian languages and provides real-time speech recognition capabilities.

## Features

- Live speech recording
- Multiple language support (Hindi, English, Tamil, Telugu, Kannada, Malayalam)
- Audio file transcription
- Simple command-line interface

## Requirements

- Python 3.x
- Internet connection
- Microphone (for live recording)

## Installation

1. Install required packages:
```bash
pip install requests sounddevice numpy
```

2. Grant microphone permissions in System Settings (for macOS users)

## Quick Start

1. Run the program:
```bash
python speech_to_text.py
```

2. Choose from available options:
   - Record and transcribe
   - Transcribe existing audio file
   - List audio devices
   - Exit

## Supported Languages

- Hindi (hi-IN)
- English (en-IN)
- Tamil (ta-IN)
- Telugu (te-IN)
- Kannada (kn-IN)
- Malayalam (ml-IN)

## Note

Make sure you have proper microphone permissions and a working internet connection for the API calls.
