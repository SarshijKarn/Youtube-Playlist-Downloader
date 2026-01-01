# YouTube Playlist Downloader

A simple Python application to download YouTube playlists and videos with both CLI and GUI interfaces.

## Features

- Download entire YouTube playlists or single videos
- Multiple quality options (Best, 1080p, 720p, 480p)
- Audio-only download (MP3 format)
- Both command-line and graphical user interfaces
- Progress tracking
- Automatic folder organization by playlist name

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg (required for audio extraction and video merging)

### Install FFmpeg

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract and add to your system PATH

**Or use Chocolatey:**
```powershell
choco install ffmpeg
```

**Or use winget:**
```powershell
winget install ffmpeg
```

### Install Python Dependencies

```bash
cd youtube-playlist-downloader
pip install -r requirements.txt
```

## Usage

### GUI Version (Recommended)

Run the graphical interface:

```bash
python downloader_gui.py
```

1. Paste your YouTube playlist or video URL
2. Choose download location
3. Select video quality or audio-only
4. Click "Download"

### Command-Line Version

Run the CLI version:

```bash
python downloader.py
```

Follow the prompts to:
1. Enter the playlist/video URL
2. Specify download folder (default: "downloads")
3. Choose format/quality

## Examples

### Download a playlist in best quality
```bash
python downloader.py
# Enter URL: https://www.youtube.com/playlist?list=PLxxxxx
# Press Enter for default folder
# Select option 1 for best quality
```

### Download audio only
```bash
python downloader.py
# Enter URL: https://www.youtube.com/playlist?list=PLxxxxx
# Enter folder or press Enter
# Select option 5 for audio only
```

## Output Structure

Files are organized as:
```
downloads/
├── Playlist Name 1/
│   ├── Video 1.mp4
│   ├── Video 2.mp4
│   └── Video 3.mp4
└── Playlist Name 2/
    ├── Video 1.mp3
    └── Video 2.mp3
```

## Troubleshooting

### "ERROR: unable to download video data: HTTP Error 403"
- Try updating yt-dlp: `pip install --upgrade yt-dlp`

### "ffmpeg/avconv not found"
- Install FFmpeg (see Installation section)
- Ensure FFmpeg is in your system PATH

### Video download fails
- Check your internet connection
- Verify the URL is correct and the video/playlist is public
- Some videos may be geo-restricted or age-restricted

## Legal Notice

This tool is for personal use only. Respect YouTube's Terms of Service and copyright laws. Only download content you have permission to download.

---
<div align="center">

### Created with ❤️ by Sarshij Karn

[![Website](https://img.shields.io/badge/Website-sarshijkarn.com.np-8a2be2?style=for-the-badge&logo=google-chrome&logoColor=white)](https://sarshijkarn.com.np)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sarshij-karn-1a7766236/)

</div>

