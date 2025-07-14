#!/usr/bin/env python3
"""
Batch Video Metadata Tagger
Processes videos from input directory and organizes them into processed/output directories.
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from simple_video_tagger import SimpleVideoTagger


class BatchVideoTagger:
    """A class to handle batch video metadata tagging with directory organization."""
    
    def __init__(self, input_dir: str = "input", processed_dir: str = "processed", output_dir: str = "output"):
        self.input_dir = Path(input_dir)
        self.processed_dir = Path(processed_dir)
        self.output_dir = Path(output_dir)
        
        # Create directories if they don't exist
        self.input_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def get_video_files(self) -> List[Path]:
        """Get all video files from the input directory."""
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
        video_files = []
        
        for file_path in self.input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                video_files.append(file_path)
        
        return sorted(video_files)
    
    def process_single_video(self, video_path: Path, metadata_file: str = "sample_metadata.json") -> bool:
        """Process a single video file."""
        try:
            print(f"\n{'='*60}")
            print(f"Processing: {video_path.name}")
            print(f"{'='*60}")
            
            # Create tagger instance
            tagger = SimpleVideoTagger(str(video_path))
            
            # Load metadata from JSON file
            metadata_path = Path(metadata_file)
            if not metadata_path.exists():
                print(f"Error: Metadata file '{metadata_file}' not found")
                return False
            
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Apply auto-title loading
            metadata = tagger.load_metadata_with_auto_title(metadata)
            
            # Create output filename
            output_filename = f"{video_path.stem}_tagged{video_path.suffix}"
            output_path = self.output_dir / output_filename
            
            # Write metadata
            print(f"Adding metadata to: {output_filename}")
            success = tagger.write_metadata(metadata, str(output_path))
            
            if success:
                # Move original to processed directory
                processed_path = self.processed_dir / video_path.name
                shutil.move(str(video_path), str(processed_path))
                
                print(f"✓ Successfully processed: {video_path.name}")
                print(f"  Original moved to: {processed_path}")
                print(f"  Tagged video saved to: {output_path}")
                
                # Display the metadata that was added
                print(f"\nMetadata added:")
                for key, value in metadata.items():
                    print(f"  {key:15}: {value}")
                
                return True
            else:
                print(f"✗ Failed to process: {video_path.name}")
                return False
                
        except Exception as e:
            print(f"✗ Error processing {video_path.name}: {e}")
            return False
    
    def process_all_videos(self, metadata_file: str = "sample_metadata.json") -> Dict[str, bool]:
        """Process all videos in the input directory."""
        video_files = self.get_video_files()
        
        if not video_files:
            print(f"No video files found in {self.input_dir}")
            return {}
        
        print(f"Found {len(video_files)} video(s) to process:")
        for video_file in video_files:
            print(f"  - {video_file.name}")
        
        results = {}
        successful = 0
        failed = 0
        
        for video_file in video_files:
            success = self.process_single_video(video_file, metadata_file)
            results[video_file.name] = success
            
            if success:
                successful += 1
            else:
                failed += 1
        
        # Summary
        print(f"\n{'='*60}")
        print(f"PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"Total videos: {len(video_files)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success rate: {(successful/len(video_files)*100):.1f}%")
        
        if failed > 0:
            print(f"\nFailed videos:")
            for video_name, success in results.items():
                if not success:
                    print(f"  - {video_name}")
        
        return results
    
    def show_directory_status(self):
        """Show the current status of all directories."""
        print(f"\n{'='*60}")
        print(f"DIRECTORY STATUS")
        print(f"{'='*60}")
        
        # Input directory
        input_videos = self.get_video_files()
        print(f"📁 Input directory ({self.input_dir}): {len(input_videos)} video(s)")
        for video in input_videos:
            print(f"   - {video.name}")
        
        # Processed directory
        processed_files = list(self.processed_dir.glob("*.mp4")) + list(self.processed_dir.glob("*.avi")) + list(self.processed_dir.glob("*.mov"))
        print(f"\n📁 Processed directory ({self.processed_dir}): {len(processed_files)} file(s)")
        for file in processed_files[:5]:  # Show first 5
            print(f"   - {file.name}")
        if len(processed_files) > 5:
            print(f"   ... and {len(processed_files) - 5} more")
        
        # Output directory
        output_files = list(self.output_dir.glob("*_tagged.*"))
        print(f"\n📁 Output directory ({self.output_dir}): {len(output_files)} tagged file(s)")
        for file in output_files[:5]:  # Show first 5
            print(f"   - {file.name}")
        if len(output_files) > 5:
            print(f"   ... and {len(output_files) - 5} more")


def main():
    parser = argparse.ArgumentParser(
        description="Batch Video Metadata Tagger - Process videos from input directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_video_tagger.py --process-all
  python batch_video_tagger.py --status
  python batch_video_tagger.py --metadata custom_metadata.json
  python batch_video_tagger.py --input videos --output tagged --processed done
        """
    )
    
    parser.add_argument('--process-all', action='store_true', 
                       help='Process all videos in input directory')
    parser.add_argument('--status', action='store_true', 
                       help='Show directory status')
    parser.add_argument('--metadata', metavar='JSON_FILE', default='sample_metadata.json',
                       help='Metadata JSON file (default: sample_metadata.json)')
    parser.add_argument('--input', metavar='INPUT_DIR', default='input',
                       help='Input directory (default: input)')
    parser.add_argument('--output', metavar='OUTPUT_DIR', default='output',
                       help='Output directory (default: output)')
    parser.add_argument('--processed', metavar='PROCESSED_DIR', default='processed',
                       help='Processed directory (default: processed)')
    
    args = parser.parse_args()
    
    try:
        tagger = BatchVideoTagger(args.input, args.processed, args.output)
        
        if args.status:
            tagger.show_directory_status()
        elif args.process_all:
            tagger.process_all_videos(args.metadata)
        else:
            # Default: show status
            tagger.show_directory_status()
            print(f"\nUse --process-all to start processing videos")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 