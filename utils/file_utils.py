#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Utilities for ClipForge
Handles file operations, folder creation, and naming conventions
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple


class FileUtils:
    """Utility class for file and folder operations"""
    
    # Supported video formats
    SUPPORTED_FORMATS = {
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', 
        '.webm', '.m4v', '.3gp', '.ogv', '.ts', '.mts'
    }
    
    @staticmethod
    def is_video_file(file_path: str) -> bool:
        """Check if file is a supported video format"""
        return Path(file_path).suffix.lower() in FileUtils.SUPPORTED_FORMATS
    
    @staticmethod
    def get_safe_folder_name(filename: str) -> str:
        """Convert filename to safe folder name"""
        # Remove file extension
        name = Path(filename).stem
        
        # Replace invalid characters with underscores
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', name)
        
        # Remove leading/trailing spaces and dots
        safe_name = safe_name.strip(' .')
        
        # Limit length
        if len(safe_name) > 100:
            safe_name = safe_name[:100]
        
        return safe_name if safe_name else "unnamed_video"
    
    @staticmethod
    def create_unique_folder_name(base_path: Path, folder_name: str) -> Path:
        """Create a unique folder name by adding timestamp if needed"""
        target_path = base_path / folder_name
        
        if not target_path.exists():
            return target_path
        
        # Add timestamp to make it unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_name = f"{folder_name}_{timestamp}"
        unique_path = base_path / unique_name
        
        return unique_path
    
    @staticmethod
    def ensure_directory_exists(directory_path: Path) -> bool:
        """Ensure directory exists, create if it doesn't"""
        try:
            directory_path.mkdir(parents=True, exist_ok=True)
            return True
        except OSError as e:
            print(f"Error creating directory {directory_path}: {e}")
            return False
    
    @staticmethod
    def get_video_info(video_path: str) -> Optional[dict]:
        """Get basic video information"""
        try:
            from moviepy.editor import VideoFileClip
            
            with VideoFileClip(video_path) as clip:
                return {
                    'duration': clip.duration,
                    'fps': clip.fps,
                    'size': (clip.w, clip.h),
                    'filename': Path(video_path).name
                }
        except Exception as e:
            print(f"Error getting video info for {video_path}: {e}")
            return None
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in seconds to human readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in bytes to human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return Path(file_path).stat().st_size
        except OSError:
            return 0
    
    @staticmethod
    def clean_filename(filename: str) -> str:
        """Clean filename for safe file operations"""
        # Remove or replace invalid characters
        cleaned = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing spaces and dots
        cleaned = cleaned.strip(' .')
        return cleaned
    
    @staticmethod
    def generate_clip_filename(base_name: str, clip_number: int, duration: int) -> str:
        """Generate filename for a clip"""
        safe_base = FileUtils.clean_filename(base_name)
        return f"{safe_base}_clip_{clip_number:03d}_{duration}s.mp4"
    
    @staticmethod
    def get_available_space(directory_path: Path) -> int:
        """Get available disk space in bytes"""
        try:
            return os.statvfs(directory_path).f_frsize * os.statvfs(directory_path).f_bavail
        except OSError:
            return 0
    
    @staticmethod
    def estimate_output_size(input_size: int, input_duration: float, clip_duration: int) -> int:
        """Estimate output file size for a clip"""
        # Rough estimation: assume similar bitrate
        clips_count = int(input_duration / clip_duration)
        if clips_count == 0:
            clips_count = 1
        
        # Add some overhead for encoding
        estimated_size = (input_size / clips_count) * 1.1
        return int(estimated_size) 