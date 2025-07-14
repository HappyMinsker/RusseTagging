#!/usr/bin/env python3
"""
Video Metadata Tagger GUI
A simple GUI version of the video tagger for easier use.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from pathlib import Path
from video_tagger import VideoTagger


class VideoTaggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Metadata Tagger")
        self.root.geometry("800x600")
        
        self.video_path = None
        self.tagger = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # File selection
        ttk.Label(main_frame, text="Video File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_var = tk.StringVar()
        file_entry = ttk.Entry(main_frame, textvariable=self.file_var, width=50)
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, pady=5)
        
        # Video info frame
        info_frame = ttk.LabelFrame(main_frame, text="Video Information", padding="5")
        info_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        info_frame.columnconfigure(0, weight=1)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=6, width=80)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Metadata frame
        metadata_frame = ttk.LabelFrame(main_frame, text="Metadata Tags", padding="5")
        metadata_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        metadata_frame.columnconfigure(1, weight=1)
        
        # Common tags
        common_tags = [
            ("Title:", "title"),
            ("Artist:", "artist"),
            ("Album:", "album"),
            ("Year:", "year"),
            ("Genre:", "genre"),
            ("Language:", "language"),
            ("Description:", "description"),
            ("Keywords:", "keywords"),
            ("Creator:", "creator"),
            ("Copyright:", "copyright"),
            ("Comment:", "comment"),
            ("Rating:", "rating"),
            ("Category:", "category")
        ]
        
        self.tag_vars = {}
        for i, (label, tag) in enumerate(common_tags):
            ttk.Label(metadata_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=(0, 5), pady=2)
            var = tk.StringVar()
            self.tag_vars[tag] = var
            entry = ttk.Entry(metadata_frame, textvariable=var, width=50)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Read Metadata", command=self.read_metadata).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Write Metadata", command=self.write_metadata).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_metadata).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load JSON", command=self.load_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save JSON", command=self.save_json).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_var.set(file_path)
            self.video_path = file_path
            self.load_video_info()
    
    def load_video_info(self):
        if not self.video_path:
            return
        
        try:
            self.tagger = VideoTagger(self.video_path)
            info = self.tagger.get_video_info()
            
            self.info_text.delete(1.0, tk.END)
            if info and 'format' in info:
                format_info = info['format']
                info_text = f"File: {os.path.basename(self.video_path)}\n"
                info_text += f"Duration: {format_info.get('duration', 'N/A')} seconds\n"
                info_text += f"Size: {format_info.get('size', 'N/A')} bytes\n"
                info_text += f"Format: {format_info.get('format_name', 'N/A')}\n"
                
                # Stream info
                if 'streams' in info:
                    video_streams = [s for s in info['streams'] if s.get('codec_type') == 'video']
                    if video_streams:
                        stream = video_streams[0]
                        info_text += f"Video Codec: {stream.get('codec_name', 'N/A')}\n"
                        info_text += f"Resolution: {stream.get('width', 'N/A')}x{stream.get('height', 'N/A')}\n"
                
                self.info_text.insert(1.0, info_text)
            
            self.status_var.set(f"Loaded: {os.path.basename(self.video_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load video info: {str(e)}")
            self.status_var.set("Error loading video")
    
    def read_metadata(self):
        if not self.tagger:
            messagebox.showwarning("Warning", "Please select a video file first")
            return
        
        try:
            metadata = self.tagger.read_metadata()
            
            # Clear existing values
            for var in self.tag_vars.values():
                var.set("")
            
            # Fill in found metadata
            for tag, var in self.tag_vars.items():
                if tag in metadata:
                    var.set(metadata[tag])
            
            self.status_var.set("Metadata read successfully")
            messagebox.showinfo("Success", f"Read {len(metadata)} metadata tags")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read metadata: {str(e)}")
            self.status_var.set("Error reading metadata")
    
    def write_metadata(self):
        if not self.tagger:
            messagebox.showwarning("Warning", "Please select a video file first")
            return
        
        try:
            # Collect non-empty metadata
            metadata = {}
            for tag, var in self.tag_vars.items():
                value = var.get().strip()
                if value:
                    metadata[tag] = value
            
            if not metadata:
                messagebox.showwarning("Warning", "No metadata to write")
                return
            
            # Ask for output file
            output_path = filedialog.asksaveasfilename(
                title="Save Tagged Video As",
                defaultextension=".mp4",
                filetypes=[
                    ("MP4 files", "*.mp4"),
                    ("All files", "*.*")
                ],
                initialvalue=os.path.splitext(self.video_path)[0] + "_tagged.mp4"
            )
            
            if output_path:
                success = self.tagger.write_metadata(metadata, output_path)
                if success:
                    self.status_var.set(f"Metadata written to: {os.path.basename(output_path)}")
                    messagebox.showinfo("Success", f"Metadata written successfully to:\n{output_path}")
                else:
                    messagebox.showerror("Error", "Failed to write metadata")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write metadata: {str(e)}")
            self.status_var.set("Error writing metadata")
    
    def clear_metadata(self):
        for var in self.tag_vars.values():
            var.set("")
        self.status_var.set("Metadata cleared")
    
    def load_json(self):
        file_path = filedialog.askopenfilename(
            title="Load Metadata from JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Clear existing values
                for var in self.tag_vars.values():
                    var.set("")
                
                # Fill in loaded metadata
                for tag, var in self.tag_vars.items():
                    if tag in metadata:
                        var.set(str(metadata[tag]))
                
                self.status_var.set(f"Loaded metadata from: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Loaded {len(metadata)} metadata tags from JSON")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON: {str(e)}")
    
    def save_json(self):
        # Collect non-empty metadata
        metadata = {}
        for tag, var in self.tag_vars.items():
            value = var.get().strip()
            if value:
                metadata[tag] = value
        
        if not metadata:
            messagebox.showwarning("Warning", "No metadata to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Metadata to JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=4, ensure_ascii=False)
                
                self.status_var.set(f"Saved metadata to: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Metadata saved to:\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save JSON: {str(e)}")


def main():
    root = tk.Tk()
    app = VideoTaggerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main() 