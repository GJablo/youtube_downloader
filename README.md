# Decipher YouTube Video Downloader

A Python script that includes a GUI to download and merge YouTube videos from both video and audio codecs at a specified resolution.

## Features

- Download YouTube videos with both video and audio
- Select the desired resolution from available options


## Requirements

- Python 3.x
- `yt-dlp`
- `ffmpeg` (make sure it is installed and available in your system's PATH)
- `tkinter` (install it via your package manager if not included with Python)

## Installation

1. Clone the repository or download the script.
2. Ensure you have Python 3.x installed on your system
3. Install the required `yt-dlp` library using pip:

```bash
pip install yt-dlp
```
4. Ensure `ffmpeg` is installed. You can download it from the official [FFmpeg website here](https://github.com/BtbN/FFmpeg-Builds/releases) choose either a zip for windows or linux
5. Install tkinter
```bash
pip install tk
```

## Usage
1. run on the terminal
```bash
python Youtube_downloader.py
```
2. The GUI window will open. Enter the Youtube video URL in its respective field
3. Click the 'Get Formats' button
4. Available formats will be displayed on the text area
5. Enter the desired video format code e.g 606 and audio format code e.g 139 in the respective fields
6. click the "Download and Merge" button to get your video
7. Provide a name for the final output file when prompted, the prompt will appear on the terminal, ensuring it ends with `.mp4` and uses underscores instead of spaces (e.g., final_video.mp4).
8. The video will be stored on the location where you have the python file, i.e current working directory
