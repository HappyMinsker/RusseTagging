#!/usr/bin/env python3
"""
YouTube Playlist Downloader
Downloads videos from a YouTube playlist using yt-dlp
"""

import os
import sys
import argparse
from pathlib import Path
import yt_dlp

def download_playlist(playlist_url, output_dir="input", quality="best", audio_only=False):
    """
    Download videos from a YouTube playlist
    
    Args:
        playlist_url (str): URL of the YouTube playlist
        output_dir (str): Directory to save downloaded videos
        quality (str): Video quality preference
        audio_only (bool): If True, download only audio
    """
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(playlist_index)s-%(title)s.%(ext)s'),
        'ignoreerrors': True,  # Continue downloading even if some videos fail
        'no_warnings': False,
        'extract_flat': False,
    }
    
    # Set quality preferences
    if audio_only:
        ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = f'best[height<={quality}]' if quality.isdigit() else quality
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Starting download of playlist: {playlist_url}")
            print(f"Output directory: {output_dir}")
            print(f"Quality: {'Audio only' if audio_only else quality}")
            print("-" * 50)
            
            # Download the playlist
            ydl.download([playlist_url])
            
            print("-" * 50)
            print("Download completed!")
            
    except Exception as e:
        print(f"Error downloading playlist: {e}")
        return False
    
    return True

def list_playlist_videos(playlist_url):
    """
    List all videos in a playlist without downloading them
    
    Args:
        playlist_url (str): URL of the YouTube playlist
    """
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Fetching playlist information: {playlist_url}")
            print("-" * 50)
            
            # Extract playlist info
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' in playlist_info:
                print(f"Playlist: {playlist_info.get('title', 'Unknown')}")
                print(f"Total videos: {len(playlist_info['entries'])}")
                print("-" * 50)
                
                for i, entry in enumerate(playlist_info['entries'], 1):
                    if entry:
                        title = entry.get('title', 'Unknown title')
                        duration = entry.get('duration', 'Unknown duration')
                        print(f"{i:2d}. {title}")
                        if duration != 'Unknown duration':
                            minutes = duration // 60
                            seconds = duration % 60
                            print(f"    Duration: {minutes}:{seconds:02d}")
                        print()
            else:
                print("No videos found in playlist or playlist is private.")
                
    except Exception as e:
        print(f"Error fetching playlist: {e}")

def main():
    parser = argparse.ArgumentParser(description='Download videos from a YouTube playlist')
    parser.add_argument('url', help='YouTube playlist URL')
    parser.add_argument('-o', '--output', default='input', 
                       help='Output directory (default: input)')
    parser.add_argument('-q', '--quality', default='best',
                       help='Video quality (default: best, or specify height like 720)')
    parser.add_argument('-a', '--audio-only', action='store_true',
                       help='Download audio only (MP3)')
    parser.add_argument('-l', '--list', action='store_true',
                       help='List videos in playlist without downloading')
    
    args = parser.parse_args()
    
    if args.list:
        list_playlist_videos(args.url)
    else:
        success = download_playlist(
            args.url, 
            args.output, 
            args.quality, 
            args.audio_only
        )
        
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main() 