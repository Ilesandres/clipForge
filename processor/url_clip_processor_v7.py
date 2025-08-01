#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL Clip Processor V7 for ClipForge
Uses yt-dlp and moviepy for real streaming without system tools
"""

import os
import tempfile
import time
import gc
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from .url_processor import URLProcessor
from utils.file_utils import FileUtils


class URLClipProcessorV7:
    """URL clip processor that uses yt-dlp and moviepy for real streaming"""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """Initialize URL clip processor V7"""
        self.url_processor = URLProcessor()
        self.progress_callback = progress_callback or (lambda x: None)
        self.temp_dir = None
    
    def process_url_video(self, url: str, output_base_path: Path, 
                         clip_duration: int) -> Dict[str, Any]:
        """Process a video from URL using yt-dlp and moviepy streaming"""
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
            self.temp_dir = tempfile.mkdtemp(prefix="clipforge_v7_")
            temp_path = Path(self.temp_dir)
            
            print(f"Processing {platform} video: {video_info['title']}")
            print(f"Duration: {self.url_processor.format_duration(video_info['duration'])}")
            print(f"Using V7 processor - yt-dlp and moviepy streaming")
            
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
            
            # Extract segments using yt-dlp and moviepy
            print("Step 1: Extracting segments using yt-dlp and moviepy...")
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
                    
                    # Extract segment using yt-dlp and moviepy
                    segment_path = self._extract_segment_with_libraries(
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
    
    def _extract_segment_with_libraries(self, url: str, start_time: float, duration: float, 
                                      temp_dir: Path, clip_index: int) -> Optional[str]:
        """Extract a segment using yt-dlp and moviepy libraries only"""
        try:
            # Create temporary file path for segment
            temp_segment_path = temp_dir / f"segment_{clip_index:03d}.mp4"
            
            print(f"Extracting segment {clip_index + 1}: {start_time:.1f}s - {start_time + duration:.1f}s")
            
            # Calculate end time
            end_time = start_time + duration
            
            print(f"Streaming segment: {start_time}s - {end_time}s (duration: {duration}s)")
            
            # V7: Use yt-dlp to get proper video stream URL and download segment
            import yt_dlp
            
            # Step 1: Get video info and find the best video format
            print("Getting video stream information...")
            info_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(info_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Get the best video format with direct URL
                formats = info.get('formats', [])
                if not formats:
                    print("❌ No video formats found")
                    return None
                
                # Find the best format with direct URL (not fragmented)
                best_format = None
                for fmt in formats:
                    if fmt.get('url') and not fmt.get('fragments'):
                        # Prefer formats with higher resolution/bitrate
                        if not best_format or fmt.get('height', 0) > best_format.get('height', 0):
                            best_format = fmt
                
                if not best_format:
                    # Fallback to any format with URL
                    for fmt in formats:
                        if fmt.get('url'):
                            best_format = fmt
                            break
                
                if not best_format:
                    print("❌ No suitable video format found")
                    return None
                
                stream_url = best_format.get('url')
                format_info = best_format.get('format_note', 'Unknown')
                file_size = best_format.get('filesize', 0)
                
                print(f"✅ Selected format: {format_info}")
                print(f"✅ Video size: {file_size} bytes")
                print(f"✅ Stream URL: {stream_url[:50]}...")
            
            if not stream_url:
                print("❌ Could not get video stream URL")
                return None
            
            # Step 2: Download the full video once and extract segments
            print("Downloading video for segment extraction...")
            temp_full_video = temp_dir / f"full_video_{clip_index:03d}.mp4"
            
            # Use yt-dlp to download the video
            download_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
                'outtmpl': str(temp_full_video),
                'socket_timeout': 30,
                'retries': 3,
            }
            
            try:
                with yt_dlp.YoutubeDL(download_opts) as ydl:
                    ydl.download([url])
                
                if temp_full_video.exists():
                    full_size = temp_full_video.stat().st_size
                    print(f"✅ Downloaded video: {full_size} bytes")
                    
                    # Step 3: Use moviepy to extract the segment with better memory management
                    print("Extracting segment with moviepy...")
                    from moviepy.editor import VideoFileClip
                    
                    video = None
                    segment = None
                    
                    try:
                        # Open the video file with specific settings for better performance
                        video = VideoFileClip(str(temp_full_video), audio=True, target_resolution=None)
                        
                        # Extract the segment
                        segment = video.subclip(start_time, end_time)
                        
                        # Write the segment with optimized settings
                        segment.write_videofile(
                            str(temp_segment_path),
                            codec='libx264',
                            audio_codec='aac',
                            ffmpeg_params=['-preset', 'ultrafast', '-crf', '28'],  # Faster encoding
                            verbose=False,
                            logger=None,
                            threads=2,  # Limit threads to prevent memory issues
                            fps=video.fps  # Use original FPS
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
                        print(f"⚠️ MoviePy processing error: {e}")
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
                        
                        # Remove the full video file
                        if temp_full_video.exists():
                            temp_full_video.unlink()
                        
                        # Force garbage collection
                        gc.collect()
                        
                else:
                    print("❌ Full video download failed")
                    
            except Exception as e:
                print(f"⚠️ Download/processing error: {e}")
                # Clean up if file exists
                if temp_full_video.exists():
                    temp_full_video.unlink()
            
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
        
        # V7 simplified approach: 15 seconds per clip
        estimated_seconds = clips_count * 15
        
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