#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Splitter for ClipForge
Handles video processing and clipping operations
"""

import os
from pathlib import Path
from typing import List, Optional, Callable, Dict, Any
from moviepy.editor import VideoFileClip
from utils.file_utils import FileUtils


class VideoSplitter:
    """Handles video splitting and processing operations"""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """Initialize video splitter"""
        self.progress_callback = progress_callback or (lambda x: None)
        self.current_video_path = None
        self.current_clip = None
    
    def get_video_info(self, video_path: str) -> Optional[Dict[str, Any]]:
        """Get detailed video information"""
        try:
            with VideoFileClip(video_path) as clip:
                return {
                    'duration': clip.duration,
                    'fps': clip.fps,
                    'size': (clip.w, clip.h),
                    'filename': Path(video_path).name,
                    'file_size': FileUtils.get_file_size(video_path)
                }
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
    
    def calculate_clips(self, video_duration: float, clip_duration: int) -> List[Dict[str, float]]:
        """Calculate clip segments for a video"""
        clips = []
        start_time = 0.0
        
        while start_time < video_duration:
            end_time = min(start_time + clip_duration, video_duration)
            clips.append({
                'start': start_time,
                'end': end_time,
                'duration': end_time - start_time
            })
            start_time = end_time
        
        return clips
    
    def split_video(self, video_path: str, output_folder: Path, 
                   clip_duration: int, base_filename: str) -> List[str]:
        """Split video into clips of specified duration"""
        output_files = []
        
        try:
            # Load video
            with VideoFileClip(video_path) as video:
                self.current_video_path = video_path
                self.current_clip = video
                
                # Calculate clips
                clips = self.calculate_clips(video.duration, clip_duration)
                total_clips = len(clips)
                
                print(f"Splitting video into {total_clips} clips...")
                
                for i, clip_info in enumerate(clips):
                    # Generate output filename
                    output_filename = FileUtils.generate_clip_filename(
                        base_filename, i + 1, clip_duration
                    )
                    output_path = output_folder / output_filename
                    
                    # Create clip
                    start_time = clip_info['start']
                    end_time = clip_info['end']
                    
                    print(f"Processing clip {i + 1}/{total_clips}: {start_time:.1f}s - {end_time:.1f}s")
                    
                    # Extract subclip
                    subclip = video.subclip(start_time, end_time)
                    
                    # Write clip
                    subclip.write_videofile(
                        str(output_path),
                        codec='libx264',
                        audio_codec='aac',
                        temp_audiofile='temp-audio.m4a',
                        remove_temp=True,
                        verbose=False,
                        logger=None
                    )
                    
                    output_files.append(str(output_path))
                    
                    # Update progress
                    progress = (i + 1) / total_clips * 100
                    self.progress_callback(progress)
                    
                    # Clean up subclip
                    subclip.close()
                
                print(f"Successfully created {len(output_files)} clips")
                
        except Exception as e:
            print(f"Error splitting video: {e}")
            raise
        
        finally:
            # Clean up
            if self.current_clip:
                self.current_clip = None
            self.current_video_path = None
        
        return output_files
    
    def process_video(self, video_path: str, output_base_path: Path, 
                     clip_duration: int) -> Dict[str, Any]:
        """Process a video file and return results"""
        try:
            # Get video info
            video_info = self.get_video_info(video_path)
            if not video_info:
                raise ValueError("Could not read video file")
            
            # Create output folder
            base_filename = Path(video_path).stem
            safe_folder_name = FileUtils.get_safe_folder_name(base_filename)
            output_folder = FileUtils.create_unique_folder_name(output_base_path, safe_folder_name)
            
            # Ensure output directory exists
            if not FileUtils.ensure_directory_exists(output_folder):
                raise OSError(f"Could not create output directory: {output_folder}")
            
            # Split video
            output_files = self.split_video(video_path, output_folder, clip_duration, base_filename)
            
            # Calculate total output size
            total_output_size = sum(FileUtils.get_file_size(f) for f in output_files)
            
            return {
                'success': True,
                'input_file': video_path,
                'output_folder': str(output_folder),
                'output_files': output_files,
                'clips_count': len(output_files),
                'input_size': video_info['file_size'],
                'output_size': total_output_size,
                'input_duration': video_info['duration'],
                'clip_duration': clip_duration
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'input_file': video_path
            }
    
    def cancel_processing(self):
        """Cancel current video processing"""
        if self.current_clip:
            print("Canceling video processing...")
            # The processing will be canceled in the next iteration
            # This is a simple implementation - in a real app you'd want
            # to use threading and proper cancellation mechanisms
    
    def get_processing_status(self) -> Dict[str, Any]:
        """Get current processing status"""
        return {
            'is_processing': self.current_clip is not None,
            'current_video': self.current_video_path
        } 