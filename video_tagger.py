#!/usr/bin/env python3
"""
Video Metadata Tagger
A Python program to add, read, and modify metadata tags for video files.
Similar to ID3 tags for MP3 files, but for video formats.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
from datetime import datetime

try:
    import ffmpeg
except ImportError:
    print("Error: ffmpeg-python not installed. Please run: pip install ffmpeg-python")
    sys.exit(1)

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # Fallback if colorama is not available
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        BLUE = ""
        CYAN = ""
    class Style:
        BRIGHT = ""
        RESET_ALL = ""


class VideoTagger:
    """A class to handle video metadata tagging operations."""
    
    def __init__(self, video_path: str):
        self.video_path = Path(video_path)
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
    
    def get_video_info(self) -> Dict[str, Any]:
        """Get basic video information using ffprobe."""
        try:
            probe = ffmpeg.probe(str(self.video_path))
            return probe
        except ffmpeg.Error as e:
            print(f"{Fore.RED}Error reading video info: {e}")
            return {}
    
    def read_metadata(self) -> Dict[str, Any]:
        """Read existing metadata from the video file."""
        try:
            probe = ffmpeg.probe(str(self.video_path))
            metadata = {}
            
            # Extract metadata from format info
            if 'format' in probe and 'tags' in probe['format']:
                metadata.update(probe['format']['tags'])
            
            # Extract metadata from video stream
            for stream in probe.get('streams', []):
                if stream.get('codec_type') == 'video' and 'tags' in stream:
                    metadata.update(stream['tags'])
            
            return metadata
        except ffmpeg.Error as e:
            print(f"{Fore.RED}Error reading metadata: {e}")
            return {}
    
    def write_metadata(self, metadata: Dict[str, str], output_path: Optional[str] = None) -> bool:
        """Write metadata to the video file."""
        if output_path is None:
            output_path = str(self.video_path)
        
        try:
            # Build ffmpeg command with metadata
            input_stream = ffmpeg.input(str(self.video_path))
            
            # Add metadata to the output
            output_stream = input_stream
            
            # Add format metadata
            for key, value in metadata.items():
                output_stream = ffmpeg.output(
                    output_stream,
                    output_path,
                    metadata=f"{key}={value}",
                    codec='copy'  # Copy streams without re-encoding
                )
            
            # Run the ffmpeg command
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            
            print(f"{Fore.GREEN}✓ Metadata written successfully to: {output_path}")
            return True
            
        except ffmpeg.Error as e:
            print(f"{Fore.RED}Error writing metadata: {e}")
            return False
    
    def add_single_tag(self, key: str, value: str, output_path: Optional[str] = None) -> bool:
        """Add a single metadata tag."""
        current_metadata = self.read_metadata()
        current_metadata[key] = value
        return self.write_metadata(current_metadata, output_path)
    
    def remove_tag(self, key: str, output_path: Optional[str] = None) -> bool:
        """Remove a specific metadata tag."""
        current_metadata = self.read_metadata()
        if key in current_metadata:
            del current_metadata[key]
            return self.write_metadata(current_metadata, output_path)
        else:
            print(f"{Fore.YELLOW}Tag '{key}' not found in metadata")
            return False
    
    def clear_all_metadata(self, output_path: Optional[str] = None) -> bool:
        """Clear all metadata from the video file."""
        try:
            input_stream = ffmpeg.input(str(self.video_path))
            output_stream = ffmpeg.output(
                input_stream,
                output_path or str(self.video_path),
                map_metadata='-1',  # Remove all metadata
                codec='copy'
            )
            
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            print(f"{Fore.GREEN}✓ All metadata cleared from: {output_path or str(self.video_path)}")
            return True
            
        except ffmpeg.Error as e:
            print(f"{Fore.RED}Error clearing metadata: {e}")
            return False
    
    def display_metadata(self):
        """Display all metadata in a formatted way."""
        metadata = self.read_metadata()
        
        if not metadata:
            print(f"{Fore.YELLOW}No metadata found in: {self.video_path}")
            return
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Metadata for: {self.video_path}")
        print(f"{Fore.CYAN}{'='*50}")
        
        for key, value in metadata.items():
            print(f"{Fore.GREEN}{key:20}: {Fore.WHITE}{value}")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Video Metadata Tagger - Add, read, and modify video metadata tags",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python video_tagger.py video.mp4 --read
  python video_tagger.py video.mp4 --add title "My Video Title"
  python video_tagger.py video.mp4 --add artist "John Doe" --add year "2024"
  python video_tagger.py video.mp4 --remove title
  python video_tagger.py video.mp4 --clear
  python video_tagger.py video.mp4 --batch metadata.json
        """
    )
    
    parser.add_argument('video_file', help='Path to the video file')
    parser.add_argument('--read', action='store_true', help='Read and display metadata')
    parser.add_argument('--add', nargs=2, metavar=('KEY', 'VALUE'), action='append', 
                       help='Add a metadata tag (can be used multiple times)')
    parser.add_argument('--remove', metavar='KEY', help='Remove a specific metadata tag')
    parser.add_argument('--clear', action='store_true', help='Clear all metadata')
    parser.add_argument('--batch', metavar='JSON_FILE', help='Load metadata from JSON file')
    parser.add_argument('--output', '-o', metavar='OUTPUT_FILE', help='Output file path')
    parser.add_argument('--info', action='store_true', help='Show video information')
    
    args = parser.parse_args()
    
    try:
        tagger = VideoTagger(args.video_file)
        
        # Show video information
        if args.info:
            info = tagger.get_video_info()
            if info:
                print(f"\n{Fore.CYAN}{Style.BRIGHT}Video Information:")
                print(f"{Fore.CYAN}{'='*30}")
                if 'format' in info:
                    format_info = info['format']
                    print(f"{Fore.GREEN}Duration: {Fore.WHITE}{format_info.get('duration', 'N/A')}s")
                    print(f"{Fore.GREEN}Size: {Fore.WHITE}{format_info.get('size', 'N/A')} bytes")
                    print(f"{Fore.GREEN}Format: {Fore.WHITE}{format_info.get('format_name', 'N/A')}")
                print()
        
        # Read metadata
        if args.read:
            tagger.display_metadata()
        
        # Add metadata tags
        if args.add:
            for key, value in args.add:
                print(f"{Fore.BLUE}Adding tag: {key} = {value}")
                success = tagger.add_single_tag(key, value, args.output)
                if not success:
                    print(f"{Fore.RED}Failed to add tag: {key}")
        
        # Remove metadata tag
        if args.remove:
            print(f"{Fore.BLUE}Removing tag: {args.remove}")
            tagger.remove_tag(args.remove, args.output)
        
        # Clear all metadata
        if args.clear:
            print(f"{Fore.BLUE}Clearing all metadata...")
            tagger.clear_all_metadata(args.output)
        
        # Batch load from JSON
        if args.batch:
            try:
                with open(args.batch, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                print(f"{Fore.BLUE}Loading metadata from: {args.batch}")
                success = tagger.write_metadata(metadata, args.output)
                if success:
                    print(f"{Fore.GREEN}✓ Batch metadata applied successfully")
                else:
                    print(f"{Fore.RED}Failed to apply batch metadata")
                    
            except FileNotFoundError:
                print(f"{Fore.RED}JSON file not found: {args.batch}")
            except json.JSONDecodeError:
                print(f"{Fore.RED}Invalid JSON format in: {args.batch}")
        
        # If no specific action was requested, show metadata
        if not any([args.read, args.add, args.remove, args.clear, args.batch, args.info]):
            tagger.display_metadata()
    
    except FileNotFoundError as e:
        print(f"{Fore.RED}Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 