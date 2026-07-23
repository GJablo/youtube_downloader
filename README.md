# Decipher YouTube Video Downloader

A Python script that includes a GUI to download and merge YouTube videos from both video and audio codecs at a specified resolution.

## Features

- Download YouTube videos with both video and audio

## Requirements

- Python 3.x
- `yt-dlp`
- `ffmpeg` (make sure it is installed and available in your system's PATH)
- `tkinter` (use your OS package manager if it is not included with Python)

## Installation

1. Clone the repository or download the script.
2. From the repository root, create and activate a Python virtual environment:

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

3. Install Python dependencies from the requirements file:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Install `ffmpeg` and `tkinter` using your operating system package manager if needed.

- Debian/Ubuntu/Kali:

```bash
sudo apt update
sudo apt install ffmpeg python3-tk
```

- Fedora:

```bash
sudo dnf install ffmpeg python3-tkinter
```

- macOS (Homebrew):

```bash
brew install ffmpeg
```

- Windows:
  1. Install `ffmpeg` and add it to your PATH. You can download it from the official [FFmpeg website here](https://github.com/BtbN/FFmpeg-Builds/releases)
  2. Install Python using the official installer and make sure the "tkinter" option is enabled.

## Usage

1. Activate the virtual environment and run the script:

```bash
source .venv/bin/activate
python Youtube_downloader.py
```

2. Enter the YouTube video URL.
3. Click "Download".
4. Choose a filename for the final `.mp4` output.

## Notes

- `yt-dlp` is installed from `requirements.txt`.
- `ffmpeg` and `tkinter` are system-level dependencies and must be installed separately.
- If you are using the virtual environment, always activate it before running the script.
