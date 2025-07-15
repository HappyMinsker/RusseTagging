# YouTube Playlist Downloader

A Python script to download videos from YouTube playlists using `yt-dlp`.

## ⚠️ Important Notice

Before using this script, please ensure you:
- Have permission to download the content
- Are complying with YouTube's Terms of Service
- Are respecting copyright laws
- Are downloading content you own or that's in the public domain

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r youtube_requirements.txt
   ```

2. **Install FFmpeg (required for audio extraction):**
   - **Windows:** Download from https://ffmpeg.org/download.html or install via chocolatey: `choco install ffmpeg`
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

## Usage

### Basic Usage

Download all videos from a playlist:
```bash
python youtube_playlist_downloader.py "https://www.youtube.com/watch?v=qvYQ7QK6MP0&list=PL9OVcuPQUHuP1hiuz1sPteq0wSBK4WBFr"
```

### Advanced Options

**List videos without downloading:**
```bash
python youtube_playlist_downloader.py -l "https://www.youtube.com/playlist?list=PL9OVcuPQUHuP1hiuz1sPteq0wSBK4WBFr"
```

**Download to a specific directory:**
```bash
python youtube_playlist_downloader.py -o "my_videos" "https://www.youtube.com/playlist?list=PL9OVcuPQUHuP1hiuz1sPteq0wSBK4WBFr"
```

**Download audio only (MP3):**
```bash
python youtube_playlist_downloader.py -a "https://www.youtube.com/playlist?list=PL9OVcuPQUHuP1hiuz1sPteq0wSBK4WBFr"
```

**Specify video quality:**
```bash
python youtube_playlist_downloader.py -q 720 "https://www.youtube.com/playlist?list=PL9OVcuPQUHuP1hiuz1sPteq0wSBK4WBFr"
```

### Command Line Options

- `url`: YouTube playlist URL (required)
- `-o, --output`: Output directory (default: input)
- `-q, --quality`: Video quality (default: best, or specify height like 720)
- `-a, --audio-only`: Download audio only (MP3 format)
- `-l, --list`: List videos in playlist without downloading

## Features

- ✅ Downloads entire playlists
- ✅ Supports video quality selection
- ✅ Audio-only download option (MP3)
- ✅ Automatic directory creation
- ✅ Error handling and continuation
- ✅ Playlist information listing
- ✅ Numbered filenames with playlist order

## File Naming

Videos are saved with the format: `{playlist_index}-{title}.{extension}`

Example: `01-Introduction to Python.mp4`

## Troubleshooting

**Common Issues:**

1. **"FFmpeg not found" error:**
   - Install FFmpeg and ensure it's in your system PATH

2. **"No module named 'yt_dlp'" error:**
   - Run: `pip install -r youtube_requirements.txt`

3. **Download fails for some videos:**
   - The script continues downloading other videos even if some fail
   - Check your internet connection and try again

4. **Private or restricted playlist:**
   - Ensure the playlist is public or you have access to it

## Example Output

```
Starting download of playlist: https://www.youtube.com/playlist?list=PL9OVcuPQUHuP1hiuz1sPteq0wSBK4WBFr
Output directory: input
Quality: best
--------------------------------------------------
[download] Downloading video 1 of 10
[download] 01-Introduction to Python.mp4 has already been downloaded
[download] Downloading video 2 of 10
[download] 02-Basic Syntax.mp4 has already been downloaded
...
--------------------------------------------------
Download completed!
```

## Legal Disclaimer

This tool is provided for educational purposes only. Users are responsible for ensuring they comply with all applicable laws and terms of service when downloading content. 