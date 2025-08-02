#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL Video Processor for ClipForge
Handles video processing from URLs (YouTube, Twitch, Kick)
"""

import re
import yt_dlp
from typing import Dict, Optional, List, Any
from pathlib import Path
from urllib.parse import urlparse
import requests


class URLProcessor:
    """Handles video processing from URLs"""
    
    # Supported platforms
    SUPPORTED_PLATFORMS = {
        'youtube': {
            'domains': ['youtube.com', 'youtu.be', 'www.youtube.com'],
            'name': 'YouTube',
            'supported': True
        },
        'twitch': {
            'domains': ['twitch.tv', 'www.twitch.tv'],
            'name': 'Twitch',
            'supported': True
        },
        'kick': {
            'domains': ['kick.com', 'www.kick.com'],
            'name': 'Kick',
            'supported': False  # Disabled due to aggressive anti-bot measures
        }
    }
    
    def __init__(self):
        """Initialize URL processor"""
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'format': 'best',  # Use best available format
            'socket_timeout': 30,  # 30 second timeout
            'retries': 3,  # Retry failed downloads
        }
        
        # Platform-specific options
        self.platform_opts = {
            'kick': {
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Cache-Control': 'max-age=0',
                },
                'extractor_args': {
                    'kick': {
                        'skip': ['dash', 'live'],  # Skip live streams and DASH
                    }
                },
                'socket_timeout': 60,  # Longer timeout for Kick
                'retries': 5,  # More retries
            }
        }
    
    def is_supported_url(self, url: str) -> Dict[str, Any]:
        """Check if URL is from a supported platform"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            for platform, info in self.SUPPORTED_PLATFORMS.items():
                if any(supported_domain in domain for supported_domain in info['domains']):
                    return {
                        'supported': info['supported'],
                        'platform': platform,
                        'platform_name': info['name'],
                        'url': url
                    }
            
            return {
                'supported': False,
                'platform': 'unknown',
                'platform_name': 'Unknown Platform',
                'url': url
            }
            
        except Exception as e:
            return {
                'supported': False,
                'platform': 'error',
                'platform_name': 'Error parsing URL',
                'url': url,
                'error': str(e)
            }
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get video information from URL"""
        try:
            # Detect platform
            platform_info = self.is_supported_url(url)
            platform = platform_info.get('platform', 'unknown')
            
            # For Kick, try direct extraction first
            if platform == 'kick':
                print("🎯 Using direct Kick extraction method...")
                try:
                    from .kick_stream_extractor import KickStreamExtractor
                    extractor = KickStreamExtractor()
                    kick_info = extractor.extract_video_info(url)
                    
                    if kick_info:
                        print("✅ Successfully extracted Kick video info directly")
                        return {
                            'title': kick_info.get('title', 'Unknown Title'),
                            'duration': kick_info.get('duration', 0),
                            'uploader': kick_info.get('uploader', 'Unknown'),
                            'platform': 'kick',
                            'url': url,
                            'thumbnail': kick_info.get('thumbnail'),
                            'view_count': kick_info.get('view_count', 0),
                            'upload_date': None,
                            'description': '',
                            'formats': [{'url': kick_info.get('stream_url')}] if kick_info.get('stream_url') else []
                        }
                    else:
                        print("⚠️ Direct Kick extraction failed, trying yt-dlp...")
                except Exception as e:
                    print(f"⚠️ Direct Kick extraction error: {e}, trying yt-dlp...")
            
            # Use platform-specific options
            info_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'format': 'best',  # Use best available format
            }
            
            # Add platform-specific options
            if platform in self.platform_opts:
                info_opts.update(self.platform_opts[platform])
            
            print(f"Getting video info for {platform} with custom options...")
            
            try:
                with yt_dlp.YoutubeDL(info_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    if not info:
                        return None
                    
                    return {
                        'title': info.get('title', 'Unknown Title'),
                        'duration': info.get('duration', 0),
                        'uploader': info.get('uploader', 'Unknown'),
                        'platform': info.get('extractor', 'unknown'),
                        'url': url,
                        'thumbnail': info.get('thumbnail'),
                        'view_count': info.get('view_count', 0),
                        'upload_date': info.get('upload_date'),
                        'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                        'formats': self._get_available_formats(info)
                    }
                    
            except Exception as e:
                error_msg = str(e)
                if '403' in error_msg and platform == 'kick':
                    print("⚠️ Kick returned 403 - this video may be restricted or require authentication")
                    print("💡 Try using a different Kick video URL or check if the video is publicly accessible")
                    return None
                else:
                    raise e
                
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
    
    def _get_available_formats(self, info: Dict) -> List[Dict]:
        """Get available video formats"""
        formats = []
        
        if 'formats' in info:
            for fmt in info['formats']:
                if fmt.get('height') and fmt.get('ext'):
                    formats.append({
                        'format_id': fmt.get('format_id', ''),
                        'height': fmt.get('height', 0),
                        'ext': fmt.get('ext', ''),
                        'filesize': fmt.get('filesize', 0),
                        'url': fmt.get('url', '')
                    })
        
        # Sort by height (quality)
        formats.sort(key=lambda x: x['height'], reverse=True)
        return formats[:5]  # Return top 5 formats
    
    def download_video_segment(self, url: str, start_time: float, duration: float, 
                              output_path: Path, format_id: str = 'best') -> Optional[str]:
        """Download a segment of the video"""
        try:
            # Use a simpler approach - download the full video and then extract segment
            temp_download_path = output_path.parent / f"temp_full_{output_path.stem}.mp4"
            
            # Use different options for Twitch videos
            if 'twitch.tv' in url:
                download_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'format': 'best',  # Use best available format for Twitch
                    'outtmpl': str(temp_download_path),
                    'socket_timeout': 30,
                    'retries': 3,
                }
            else:
                download_opts = {
                    **self.ydl_opts,
                    'format': format_id,
                    'outtmpl': str(temp_download_path),
                }
            
            # Check if we already downloaded this video
            if temp_download_path.exists():
                print(f"Using existing downloaded video: {temp_download_path}")
            else:
                print(f"Downloading full video for segment extraction...")
                with yt_dlp.YoutubeDL(download_opts) as ydl:
                    ydl.download([url])
            
            # Check if full video was downloaded
            if temp_download_path.exists():
                print(f"Full video available, extracting segment {start_time}s - {start_time + duration}s")
                # Now extract the segment using moviepy
                from moviepy.editor import VideoFileClip
                
                try:
                    clip = VideoFileClip(str(temp_download_path))
                    
                    # Check if start_time is within video duration
                    if start_time >= clip.duration:
                        print(f"Start time {start_time}s is beyond video duration {clip.duration}s")
                        clip.close()
                        return None
                    
                    # Adjust end time if it exceeds video duration
                    end_time = min(start_time + duration, clip.duration)
                    actual_duration = end_time - start_time
                    
                    print(f"Extracting segment: {start_time}s - {end_time}s (actual duration: {actual_duration}s)")
                    
                    segment = clip.subclip(start_time, end_time)
                    segment.write_videofile(
                        str(output_path),
                        codec='libx264',
                        audio_codec='aac',
                        ffmpeg_params=['-preset', 'fast', '-crf', '23'],
                        verbose=False,
                        logger=None
                    )
                    segment.close()
                    clip.close()
                    
                    print(f"Segment extracted successfully: {output_path}")
                    
                    return str(output_path)
                    
                except Exception as e:
                    print(f"Error extracting segment with moviepy: {e}")
                    import traceback
                    traceback.print_exc()
                    return None
            else:
                print(f"Failed to download full video to {temp_download_path}")
                return None
            
        except Exception as e:
            print(f"Error downloading segment: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_stream_url(self, url: str, format_id: str = 'best') -> Optional[str]:
        """Get direct stream URL for the video"""
        try:
            stream_opts = {
                **self.ydl_opts,
                'format': format_id,
            }
            
            with yt_dlp.YoutubeDL(stream_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info and 'url' in info:
                    return info['url']
                
                # Try to get URL from formats
                if 'formats' in info:
                    for fmt in info['formats']:
                        if fmt.get('url'):
                            return fmt['url']
            
            return None
            
        except Exception as e:
            print(f"Error getting stream URL: {e}")
            return None
    
    def validate_url(self, url: str) -> Dict[str, Any]:
        """Validate URL and get basic info"""
        # Check if it's a supported platform
        platform_info = self.is_supported_url(url)
        
        if not platform_info['supported']:
            if platform_info['platform'] == 'kick':
                return {
                    'valid': False,
                    'error': f"Kick no es soportado debido a sus medidas anti-bot extremadamente estrictas. Por favor usa YouTube o Twitch como alternativas.",
                    'platform': platform_info['platform_name']
                }
            else:
                return {
                    'valid': False,
                    'error': f"Plataforma no soportada: {platform_info['platform_name']}. Por el momento solo soportamos YouTube y Twitch. Esperamos agregar más plataformas en próximas actualizaciones.",
                    'platform': platform_info['platform_name']
                }
        
        # Try to get video info
        video_info = self.get_video_info(url)
        
        if not video_info:
            return {
                'valid': False,
                'error': f"No se pudo obtener información del video. Verifica que la URL sea correcta y el video esté disponible.",
                'platform': platform_info['platform_name']
            }
        
        return {
            'valid': True,
            'video_info': video_info,
            'platform': platform_info['platform_name']
        }
    
    def estimate_clips_count(self, duration: float, clip_duration: int) -> int:
        """Estimate number of clips that will be created"""
        if duration <= 0 or clip_duration <= 0:
            return 0
        return int(duration / clip_duration) + (1 if duration % clip_duration > 0 else 0)
    
    def format_duration(self, seconds: float) -> str:
        """Format duration in seconds to human readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def get_platform_icon(self, platform: str) -> str:
        """Get platform icon/emoji"""
        icons = {
            'youtube': '📺',
            'twitch': '🎮',
            'kick': '🥊',
            'unknown': '❓'
        }
        return icons.get(platform.lower(), '🌐') 