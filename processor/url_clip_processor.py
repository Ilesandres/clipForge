#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL Clip Processor for ClipForge
Processes video clips from URLs using streaming
"""

import os
import tempfile
import time
import gc
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from .url_processor import URLProcessor
from .video_splitter import VideoSplitter
from utils.file_utils import FileUtils


class URLClipProcessor:
    """Processes video clips from URLs"""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """Initialize URL clip processor"""
        self.url_processor = URLProcessor()
        self.video_splitter = VideoSplitter(progress_callback)
        self.progress_callback = progress_callback or (lambda x: None)
        self.temp_dir = None
    
    def process_url_video(self, url: str, output_base_path: Path, 
                         clip_duration: int) -> Dict[str, Any]:
        """Process a video from URL and create clips"""
        try:
            # Validate URL first
            validation = self.url_processor.validate_url(url)
            if not validation['valid']:
                return {
                    'success': False,
                    'error': validation['error'],
                    'url': url
                }
            
            video_info = validation['video_info']
            platform = validation['platform']
            
            # Create temporary directory for processing
            self.temp_dir = tempfile.mkdtemp(prefix="clipforge_")
            temp_path = Path(self.temp_dir)
            
            # Calculate clips
            clips = self._calculate_clips(video_info['duration'], clip_duration)
            total_clips = len(clips)
            
            print(f"Processing {platform} video: {video_info['title']}")
            print(f"Duration: {self.url_processor.format_duration(video_info['duration'])}")
            print(f"Creating {total_clips} clips of {clip_duration}s each")
            
            # Create output folder
            safe_title = FileUtils.get_safe_folder_name(video_info['title'])
            output_folder = FileUtils.create_unique_folder_name(output_base_path, safe_title)
            FileUtils.ensure_directory_exists(output_folder)
            
            output_files = []
            successful_clips = 0
            
            # Process each clip
            for i, clip_info in enumerate(clips):
                try:
                    # Update progress
                    progress = int((i / total_clips) * 100)
                    progress = max(0, min(100, progress))
                    print(f"Progress: {progress}% ({i + 1}/{total_clips})")
                    if self.progress_callback:
                        self.progress_callback(progress)
                    
                    print(f"Processing clip {i + 1}/{total_clips}: {clip_info['start']:.1f}s - {clip_info['end']:.1f}s")
                    
                    # Check if clip end time exceeds video duration
                    if clip_info['end'] > video_info['duration']:
                        print(f"⚠️ Clip {i + 1} end time ({clip_info['end']:.1f}s) exceeds video duration ({video_info['duration']:.1f}s), skipping")
                        continue
                    
                    # Generate output filename
                    output_filename = FileUtils.generate_clip_filename(
                        video_info['title'], i + 1, clip_duration
                    )
                    output_path = output_folder / output_filename
                    
                    # Download segment with timeout
                    segment_path = self._download_segment(
                        url, clip_info['start'], clip_info['duration'], temp_path, i
                    )
                    
                    if segment_path:
                        # Move to final location
                        if Path(segment_path).exists():
                            Path(segment_path).rename(output_path)
                            output_files.append(str(output_path))
                            successful_clips += 1
                            print(f"✅ Clip {i + 1} created: {output_filename}")
                        else:
                            print(f"❌ Clip {i + 1} failed: file not found")
                    else:
                        print(f"❌ Clip {i + 1} failed: download error")
                    
                    # Force garbage collection to free memory
                    import gc
                    gc.collect()
                    
                    # Small delay to prevent overwhelming the system
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"❌ Error processing clip {i + 1}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            # Clean up temporary directory
            self._cleanup_temp_dir()
            
            # Update final progress
            if self.progress_callback:
                self.progress_callback(100)
            
            # Calculate results
            total_output_size = sum(FileUtils.get_file_size(f) for f in output_files)
            
            return {
                'success': successful_clips > 0,
                'url': url,
                'platform': platform,
                'video_title': video_info['title'],
                'output_folder': str(output_folder),
                'output_files': output_files,
                'clips_created': successful_clips,
                'total_clips_attempted': total_clips,
                'input_duration': video_info['duration'],
                'clip_duration': clip_duration,
                'output_size': total_output_size,
                'uploader': video_info.get('uploader', 'Unknown'),
                'view_count': video_info.get('view_count', 0)
            }
            
        except Exception as e:
            self._cleanup_temp_dir()
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def _calculate_clips(self, video_duration: float, clip_duration: int) -> List[Dict[str, float]]:
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
    
    def _download_segment(self, url: str, start_time: float, duration: float, 
                         temp_dir: Path, clip_index: int) -> Optional[str]:
        """Download a video segment"""
        try:
            # Create temporary file path
            temp_file = temp_dir / f"clip_{clip_index:03d}.mp4"
            
            # Download segment using yt-dlp
            segment_path = self.url_processor.download_video_segment(
                url, start_time, duration, temp_file
            )
            
            return segment_path
            
        except Exception as e:
            print(f"Error downloading segment: {e}")
            return None
    
    def _cleanup_temp_dir(self):
        """Clean up temporary directory"""
        if self.temp_dir and Path(self.temp_dir).exists():
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
                print(f"Cleaned up temporary directory: {self.temp_dir}")
            except Exception as e:
                print(f"Error cleaning up temp directory: {e}")
    
    def get_video_preview(self, url: str) -> Dict[str, Any]:
        """Get video preview information"""
        validation = self.url_processor.validate_url(url)
        
        if not validation['valid']:
            return {
                'valid': False,
                'error': validation['error']
            }
        
        video_info = validation['video_info']
        
        return {
            'valid': True,
            'title': video_info['title'],
            'duration': video_info['duration'],
            'duration_formatted': self.url_processor.format_duration(video_info['duration']),
            'uploader': video_info.get('uploader', 'Unknown'),
            'platform': validation['platform'],
            'platform_icon': self.url_processor.get_platform_icon(validation['platform']),
            'thumbnail': video_info.get('thumbnail'),
            'view_count': video_info.get('view_count', 0),
            'description': video_info.get('description', ''),
            'formats': video_info.get('formats', [])
        }
    
    def estimate_processing_time(self, duration: float, clip_duration: int) -> str:
        """Estimate processing time"""
        clips_count = self.url_processor.estimate_clips_count(duration, clip_duration)
        
        # Rough estimation: 30 seconds per clip for download + processing
        estimated_seconds = clips_count * 30
        
        if estimated_seconds < 60:
            return f"~{estimated_seconds} segundos"
        elif estimated_seconds < 3600:
            minutes = estimated_seconds // 60
            return f"~{minutes} minutos"
        else:
            hours = estimated_seconds // 3600
            minutes = (estimated_seconds % 3600) // 60
            return f"~{hours}h {minutes}m"
    
    def cancel_processing(self):
        """Cancel current processing"""
        self._cleanup_temp_dir()
        if self.video_splitter:
            self.video_splitter.cancel_processing() 