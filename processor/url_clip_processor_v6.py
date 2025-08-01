#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL Clip Processor V6 for ClipForge
Uses real streaming to extract clips without downloading full video
"""

import os
import tempfile
import time
import gc
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from .url_processor import URLProcessor
from utils.file_utils import FileUtils


class URLClipProcessorV6:
    """URL clip processor that uses real streaming without downloading full video"""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """Initialize URL clip processor V6"""
        self.url_processor = URLProcessor()
        self.progress_callback = progress_callback or (lambda x: None)
        self.temp_dir = None
    
    def process_url_video(self, url: str, output_base_path: Path, 
                         clip_duration: int) -> Dict[str, Any]:
        """Process a video from URL using real streaming"""
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
            self.temp_dir = tempfile.mkdtemp(prefix="clipforge_v6_")
            temp_path = Path(self.temp_dir)
            
            print(f"Processing {platform} video: {video_info['title']}")
            print(f"Duration: {self.url_processor.format_duration(video_info['duration'])}")
            print(f"Using V6 processor - real streaming without downloading full video")
            
            # Calculate clips
            clips = self._calculate_clips(video_info['duration'], clip_duration)
            total_clips = len(clips)
            
            print(f"Creating {total_clips} clips of {clip_duration}s each")
            
            # Create output folder
            safe_title = FileUtils.get_safe_folder_name(video_info['title'])
            output_folder = FileUtils.create_unique_folder_name(output_base_path, safe_title)
            FileUtils.ensure_directory_exists(output_folder)
            
            output_files = []
            successful_clips = 0
            
            # Extract segments using real streaming
            print("Step 1: Extracting segments using real streaming...")
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
                    
                    # Extract segment using real streaming
                    segment_path = self._extract_segment_streaming(
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
                        print(f"❌ Clip {i + 1} failed: extraction error")
                    
                    # Force garbage collection to free memory
                    gc.collect()
                    
                    # Small delay to prevent overwhelming the system
                    time.sleep(0.5)  # Longer delay for streaming
                    
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
    
    def _extract_segment_streaming(self, url: str, start_time: float, duration: float, 
                                 temp_dir: Path, clip_index: int) -> Optional[str]:
        """Extract a segment using real streaming without downloading full video"""
        try:
            # Create temporary file path for segment
            temp_segment_path = temp_dir / f"segment_{clip_index:03d}.mp4"
            
            print(f"Extracting segment {clip_index + 1}: {start_time:.1f}s - {start_time + duration:.1f}s")
            
            # Calculate end time
            end_time = start_time + duration
            
            print(f"Streaming segment: {start_time}s - {end_time}s (duration: {duration}s)")
            
            # V6: Use yt-dlp with range parameters for real streaming
            import yt_dlp
            
            # Configure yt-dlp for streaming with range
            download_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
                'outtmpl': str(temp_segment_path),
                'socket_timeout': 30,
                'retries': 3,
                # Real streaming options
                'external_downloader': 'ffmpeg',
                'external_downloader_args': {
                    'ffmpeg_i': [
                        '-ss', str(start_time),  # Start time
                        '-t', str(duration),     # Duration
                        '-avoid_negative_ts', 'make_zero',
                        '-c', 'copy'  # Copy streams without re-encoding
                    ]
                }
            }
            
            # Use different options for Twitch videos
            if 'twitch.tv' in url:
                download_opts.update({
                    'format': 'best',
                    'external_downloader_args': {
                        'ffmpeg_i': [
                            '-ss', str(start_time),
                            '-t', str(duration),
                            '-avoid_negative_ts', 'make_zero',
                            '-c', 'copy'
                        ]
                    }
                })
            
            # Download segment using streaming
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                ydl.download([url])
            
            if temp_segment_path.exists():
                file_size = temp_segment_path.stat().st_size
                print(f"✅ Segment streamed successfully: {file_size} bytes")
                return str(temp_segment_path)
            else:
                print("❌ Segment streaming failed")
                return None
                
        except Exception as e:
            print(f"Error streaming segment: {e}")
            import traceback
            traceback.print_exc()
            return None
    
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
        
        # V6 streaming: 10 seconds per clip (faster than downloading)
        estimated_seconds = clips_count * 10
        
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