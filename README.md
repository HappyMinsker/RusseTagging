# Video Metadata Tagger

A Python program to add, read, and modify metadata tags for video files, similar to ID3 tags for MP3 files.

## Features

- ✅ Read existing metadata from video files
- ✅ Add individual metadata tags
- ✅ Add multiple tags at once
- ✅ Remove specific tags
- ✅ Clear all metadata
- ✅ Batch import metadata from JSON files
- ✅ Display video information (duration, size, format)
- ✅ Support for various video formats (MP4, AVI, MOV, etc.)
- ✅ Colored output for better readability

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg:**
   - **Windows:** Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) or use Chocolatey: `choco install ffmpeg`
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

## Usage

### Batch Processing (Recommended)

**Process all videos in input directory:**
```bash
python batch_video_tagger.py --process-all
```

**Check directory status:**
```bash
python batch_video_tagger.py --status
```

### Individual Video Commands

**Read metadata from a video file:**
```bash
python simple_video_tagger.py "video.mp4" --read
```

**Add a single metadata tag:**
```bash
python simple_video_tagger.py "video.mp4" --add title "My Video Title"
```

**Add multiple metadata tags:**
```bash
python simple_video_tagger.py "video.mp4" --add title "My Video Title" --add artist "John Doe" --add year "2024"
```

**Remove a specific tag:**
```bash
python simple_video_tagger.py "video.mp4" --remove title
```

**Clear all metadata:**
```bash
python simple_video_tagger.py "video.mp4" --clear
```

**Show video information:**
```bash
python simple_video_tagger.py "video.mp4" --info
```

### Batch Operations

**Load metadata from JSON file:**
```bash
python simple_video_tagger.py "video.mp4" --batch sample_metadata.json
```

**Save to a new file (preserve original):**
```bash
python simple_video_tagger.py "video.mp4" --batch sample_metadata.json --output "video_tagged.mp4"
```

### Common Metadata Tags

Here are some commonly used metadata tags:

- `title` - Video title
- `artist` - Creator or author
- `album` - Series or collection name
- `year` - Release year
- `genre` - Video genre/category
- `description` - Video description
- `keywords` - Search keywords
- `language` - Video language
- `creator` - Content creator
- `copyright` - Copyright information
- `comment` - Additional comments
- `rating` - Content rating
- `category` - Content category

## Examples

### Example 1: Tag your Russian learning video

```bash
python video_tagger.py "100 Common Russian phrases for natural conversation #3.mp4" \
  --add title "100 Common Russian Phrases for Natural Conversation #3" \
  --add artist "Russian Language Learning" \
  --add genre "Educational" \
  --add language "Russian" \
  --add year "2024" \
  --add description "Learn 100 common Russian phrases for natural conversation. Part 3 of the series."
```

### Example 2: Use batch JSON file

```bash
python video_tagger.py "100 Common Russian phrases for natural conversation #3.mp4" --batch sample_metadata.json
```

### Example 3: Check current metadata

```bash
python video_tagger.py "100 Common Russian phrases for natural conversation #3.mp4" --read
```

## JSON Metadata Format

Create a JSON file with your metadata tags:

```json
{
    "title": "Your Video Title",
    "artist": "Creator Name",
    "album": "Series Name",
    "year": "2024",
    "genre": "Educational",
    "description": "Video description here",
    "keywords": "tag1, tag2, tag3",
    "language": "English"
}
```

## Command Line Options

```
positional arguments:
  video_file            Path to the video file

optional arguments:
  -h, --help            show this help message and exit
  --read                Read and display metadata
  --add KEY VALUE       Add a metadata tag (can be used multiple times)
  --remove KEY          Remove a specific metadata tag
  --clear               Clear all metadata
  --batch JSON_FILE     Load metadata from JSON file
  --output OUTPUT_FILE, -o OUTPUT_FILE
                        Output file path
  --info                Show video information
```

## Notes

- The program uses FFmpeg under the hood, so it supports most video formats
- Metadata is written using stream copying to avoid re-encoding the video
- If no output file is specified, the original file will be modified
- Use `--output` to create a new file and preserve the original
- Some video players may not display all metadata tags
- Metadata support varies by video format and container

## Troubleshooting

**"FFmpeg not found" error:**
- Make sure FFmpeg is installed and in your system PATH
- On Windows, you may need to restart your terminal after installing FFmpeg

**"Permission denied" error:**
- Make sure you have write permissions for the video file
- Try running as administrator (Windows) or with sudo (Linux/macOS)

**Metadata not showing in media player:**
- Different media players support different metadata formats
- Try using a different media player or check the player's metadata display settings

## License

This project is open source and available under the MIT License. 