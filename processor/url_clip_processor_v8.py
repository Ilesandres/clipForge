#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL Clip Processor V8 for ClipForge
Real streaming without downloading full video - uses yt-dlp + moviepy streaming
"""

import os
import tempfile
import time
import gc
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from .url_processor import URLProcessor
from utils.file_utils import FileUtils


class URLClipProcessorV8:
    """URL clip processor that does real streaming without downloading full video"""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """Initialize URL clip processor V8"""
        self.url_processor = URLProcessor()
        self.progress_callback = progress_callback or (lambda x: None)
        self.temp_dir = None
        self._stop_flag = False
    
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
            self.temp_dir = tempfile.mkdtemp(prefix="clipforge_v8_")
            temp_path = Path(self.temp_dir)
            
            print(f"Processing {platform} video: {video_info['title']}")
            print(f"Duration: {self.url_processor.format_duration(video_info['duration'])}")
            print(f"Using V8 processor - REAL streaming without full download")
            
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
            
            # Get stream URL once for all clips
            print("Step 1: Getting video stream URL...")
            stream_url = self._get_stream_url(url)
            if not stream_url:
                return {
                    'success': False,
                    'error': 'Could not get video stream URL',
                    'url': url
                }
            
            print(f"✅ Stream URL obtained: {stream_url[:50]}...")
            
            # Extract segments using real streaming
            print("Step 2: Extracting segments using real streaming...")
            for i, clip_info in enumerate(clips):
                # Check if processing was stopped
                if self._stop_flag:
                    print("🛑 Processing stopped by user")
                    break
                    
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
                        stream_url, clip_info['start'], clip_info['duration'], temp_path, i
                    )
                    
                    if segment_path:
                        # Move to final location
                        if Path(segment_path).exists():
                            Path(segment_path).rename(output_path)
                            output_files.append(str(output_path))
                            successful_clips += 1
                            print(f"✅ Clip {i + 1} created: {output_filename}")
                        else:
                            print(f"❌ Segment file not found: {segment_path}")
                    else:
                        print(f"❌ Failed to extract clip {i + 1}")
                        
                except Exception as e:
                    print(f"❌ Error processing clip {i + 1}: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Cleanup
            self._cleanup_temp_dir()
            
            # Return results
            return {
                'success': successful_clips > 0,
                'total_clips': total_clips,
                'successful_clips': successful_clips,
                'output_files': output_files,
                'output_folder': str(output_folder),
                'video_info': video_info,
                'platform': platform,
                'url': url
            }
            
        except Exception as e:
            print(f"Error processing URL video: {e}")
            import traceback
            traceback.print_exc()
            self._cleanup_temp_dir()
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def _get_stream_url(self, url: str) -> Optional[str]:
        """Get direct stream URL using yt-dlp with audio included"""
        try:
            import yt_dlp
            
            print("Getting video stream information...")
            
            # Detect platform and use specific options
            platform_info = self.url_processor.is_supported_url(url)
            platform = platform_info.get('platform', 'unknown')
            
            info_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            # Add platform-specific options if available
            if hasattr(self.url_processor, 'platform_opts') and platform in self.url_processor.platform_opts:
                info_opts.update(self.url_processor.platform_opts[platform])
                print(f"Using {platform}-specific options for stream extraction...")
            
            with yt_dlp.YoutubeDL(info_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Get the best video format with direct URL
                formats = info.get('formats', [])
                if not formats:
                    print("❌ No video formats found")
                    return None
                
                # Find the best format with audio included (prefer formats with audio)
                best_format = None
                for fmt in formats:
                    if fmt.get('url') and not fmt.get('fragments'):
                        # Check if format has audio (acodec not None and not 'none')
                        has_audio = fmt.get('acodec') and fmt.get('acodec') != 'none'
                        
                        # Prefer formats with audio and higher resolution
                        if has_audio:
                            if not best_format or (fmt.get('height', 0) or 0) > (best_format.get('height', 0) or 0):
                                best_format = fmt
                
                # If no format with audio found, fallback to any format
                if not best_format:
                    print("⚠️ No format with audio found, trying any format...")
                    for fmt in formats:
                        if fmt.get('url') and not fmt.get('fragments'):
                            if not best_format or (fmt.get('height', 0) or 0) > (best_format.get('height', 0) or 0):
                                best_format = fmt
                
                if not best_format:
                    print("❌ No suitable video format found")
                    return None
                
                stream_url = best_format.get('url')
                format_info = best_format.get('format_note', 'Unknown')
                file_size = best_format.get('filesize', 0)
                has_audio = best_format.get('acodec') and best_format.get('acodec') != 'none'
                
                print(f"✅ Selected format: {format_info}")
                print(f"✅ Has audio: {has_audio}")
                print(f"✅ Video size: {file_size} bytes")
                print(f"✅ Stream URL: {stream_url[:50]}...")
                
                return stream_url
                
        except Exception as e:
            print(f"Error getting stream URL: {e}")
            return None
    
    def _extract_segment_streaming(self, stream_url: str, start_time: float, duration: float, 
                                  temp_dir: Path, clip_index: int) -> Optional[str]:
        """Extract a segment using real streaming without downloading full video"""
        try:
            # Create temporary file path for segment
            temp_segment_path = temp_dir / f"segment_{clip_index:03d}.mp4"
            
            print(f"Extracting segment {clip_index + 1}: {start_time:.1f}s - {start_time + duration:.1f}s")
            print(f"Streaming segment: {start_time}s - {start_time + duration}s (duration: {duration}s)")
            
            # Calculate end time
            end_time = start_time + duration
            
            # Use moviepy to extract segment directly from stream URL
            print("Extracting segment with moviepy streaming...")
            from moviepy.editor import VideoFileClip
            
            video = None
            segment = None
            
            try:
                # Open the video stream directly - this is the key difference!
                # MoviePy will stream the video without downloading it completely
                video = VideoFileClip(stream_url, audio=True, target_resolution=None)
                
                # Extract the segment
                segment = video.subclip(start_time, end_time)
                
                # Write the segment with optimized settings
                segment.write_videofile(
                    str(temp_segment_path),
                    codec='libx264',
                    audio_codec='aac',
                    ffmpeg_params=['-preset', 'ultrafast', '-crf', '28'],
                    verbose=False,
                    logger=None,
                    threads=2,
                    fps=video.fps
                )
                
                # Verify the segment
                if temp_segment_path.exists():
                    segment_size = temp_segment_path.stat().st_size
                    print(f"✅ Segment extracted: {segment_size} bytes")
                    
                    # Verify duration
                    try:
                        clip = VideoFileClip(str(temp_segment_path))
                        actual_duration = clip.duration
                        clip.close()
                        
                        print(f"✅ Segment duration: {actual_duration:.1f}s")
                        
                        if actual_duration > 0 and abs(actual_duration - duration) <= 5:
                            return str(temp_segment_path)
                        else:
                            print(f"⚠️ Duration mismatch: {actual_duration:.1f}s (expected: {duration:.1f}s)")
                            
                    except Exception as e:
                        print(f"⚠️ Could not verify duration: {e}")
                        if segment_size > 1000:
                            return str(temp_segment_path)
                else:
                    print("❌ Segment file not created")
                    
            except Exception as e:
                print(f"⚠️ MoviePy streaming error: {e}")
                # Try alternative encoding settings
                try:
                    if segment:
                        segment.write_videofile(
                            str(temp_segment_path),
                            codec='libx264',
                            audio=False,  # Try without audio
                            ffmpeg_params=['-preset', 'ultrafast'],
                            verbose=False,
                            logger=None
                        )
                        
                        if temp_segment_path.exists():
                            segment_size = temp_segment_path.stat().st_size
                            print(f"✅ Segment extracted (no audio): {segment_size} bytes")
                            return str(temp_segment_path)
                            
                except Exception as e2:
                    print(f"⚠️ Alternative encoding failed: {e2}")
                    
            finally:
                # Clean up resources properly
                if segment:
                    try:
                        segment.close()
                    except:
                        pass
                if video:
                    try:
                        video.close()
                    except:
                        pass
                
                # Force garbage collection
                gc.collect()
            
            print("❌ Segment extraction failed")
            return None
                
        except Exception as e:
            print(f"Error extracting segment: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _calculate_clips(self, video_duration: float, clip_duration: int) -> List[Dict[str, float]]:
        """Calculate clip segments for a video"""
        clips = []
        current_time = 0.0
        
        while current_time < video_duration:
            end_time = min(current_time + clip_duration, video_duration)
            duration = end_time - current_time
            
            clips.append({
                'start': current_time,
                'end': end_time,
                'duration': duration
            })
            
            current_time = end_time
        
        return clips
    
    def _cleanup_temp_dir(self):
        """Clean up temporary directory"""
        try:
            if self.temp_dir and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir)
                print(f"✅ Temporary directory cleaned: {self.temp_dir}")
        except Exception as e:
            print(f"⚠️ Error cleaning temp directory: {e}")
    
    def get_video_preview(self, url: str) -> Dict[str, Any]:
        """Get video preview information"""
        try:
            validation = self.url_processor.validate_url(url)
            if not validation['valid']:
                return {
                    'valid': False,
                    'error': validation['error']
                }
            
            video_info = validation['video_info']
            platform = validation['platform']
            
            # Get platform icon
            platform_icon = "🌐"
            if platform.lower() == "youtube":
                platform_icon = "📺"
            elif platform.lower() == "twitch":
                platform_icon = "🎮"
            
            return {
                'valid': True,
                'success': True,
                'title': video_info['title'],
                'duration': video_info['duration'],
                'duration_formatted': self.url_processor.format_duration(video_info['duration']),
                'platform': platform,
                'platform_icon': platform_icon,
                'uploader': video_info.get('uploader', 'Desconocido'),
                'view_count': video_info.get('view_count', 0),
                'url': url
            }
            
        except Exception as e:
            return {
                'valid': False,
                'success': False,
                'error': str(e)
            }
    
    def estimate_processing_time(self, duration: float, clip_duration: int) -> str:
        """Estimate processing time for clips"""
        clips = self._calculate_clips(duration, clip_duration)
        total_clips = len(clips)
        
        # Estimate 10-15 seconds per clip for streaming
        estimated_seconds = total_clips * 12
        
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
        print("🛑 Processing cancelled by user")
        self._stop_flag = True
        self._cleanup_temp_dir() 