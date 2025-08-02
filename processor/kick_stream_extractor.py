#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kick Stream Extractor for ClipForge
Extracts video stream URLs directly from Kick pages using HTTP requests
"""

import re
import json
import requests
from typing import Dict, Optional, Any
from urllib.parse import urlparse


class KickStreamExtractor:
    """Extracts video stream URLs from Kick pages"""
    
    def __init__(self):
        """Initialize Kick stream extractor"""
        self.session = requests.Session()
        
        # Multiple User-Agents to rotate
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
        # Base headers
        self.base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        
        # Set initial headers
        self._update_headers()
    
    def _update_headers(self):
        """Update headers with a random User-Agent"""
        import random
        user_agent = random.choice(self.user_agents)
        headers = self.base_headers.copy()
        headers['User-Agent'] = user_agent
        self.session.headers.update(headers)
    
    def extract_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract video information from Kick URL"""
        import time
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔍 Extracting video info from: {url} (attempt {attempt + 1}/{max_retries})")
                
                # Update headers for each attempt
                self._update_headers()
                
                # Add a small delay to avoid rate limiting
                if attempt > 0:
                    time.sleep(2)
                
                # Make request to the video page
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                html_content = response.text
                
                # Look for video data in the HTML
                video_data = self._extract_video_data(html_content)
                
                if not video_data:
                    print("❌ No video data found in page")
                    continue
                
                # Extract stream URL
                stream_url = self._extract_stream_url(video_data)
                
                if not stream_url:
                    print("❌ No stream URL found")
                    continue
                
                # Extract metadata
                metadata = self._extract_metadata(video_data)
                
                return {
                    'title': metadata.get('title', 'Unknown Title'),
                    'duration': metadata.get('duration', 0),
                    'uploader': metadata.get('uploader', 'Unknown'),
                    'view_count': metadata.get('view_count', 0),
                    'stream_url': stream_url,
                    'thumbnail': metadata.get('thumbnail'),
                    'platform': 'kick'
                }
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Request error (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    return None
                continue
            except Exception as e:
                print(f"❌ Extraction error (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    return None
                continue
        
        return None
    
    def _extract_video_data(self, html_content: str) -> Optional[Dict]:
        """Extract video data from HTML content"""
        try:
            # Look for different patterns where video data might be stored
            
            # Pattern 1: Look for window.__INITIAL_STATE__
            pattern1 = r'window\.__INITIAL_STATE__\s*=\s*({.*?});'
            match1 = re.search(pattern1, html_content, re.DOTALL)
            
            if match1:
                try:
                    data = json.loads(match1.group(1))
                    print("✅ Found video data in __INITIAL_STATE__")
                    return data
                except json.JSONDecodeError:
                    pass
            
            # Pattern 2: Look for video data in script tags
            pattern2 = r'<script[^>]*>\s*({[^<]*"video"[^<]*})\s*</script>'
            match2 = re.search(pattern2, html_content, re.DOTALL)
            
            if match2:
                try:
                    data = json.loads(match2.group(1))
                    print("✅ Found video data in script tag")
                    return data
                except json.JSONDecodeError:
                    pass
            
            # Pattern 3: Look for any JSON data containing video information
            pattern3 = r'{[^}]*"video"[^}]*}'
            matches3 = re.findall(pattern3, html_content)
            
            for match in matches3:
                try:
                    data = json.loads(match)
                    if 'video' in data:
                        print("✅ Found video data in JSON pattern")
                        return data
                except json.JSONDecodeError:
                    continue
            
            print("⚠️ No video data patterns found")
            return None
            
        except Exception as e:
            print(f"❌ Error extracting video data: {e}")
            return None
    
    def _extract_stream_url(self, video_data: Dict) -> Optional[str]:
        """Extract stream URL from video data"""
        try:
            # Navigate through the data structure to find the stream URL
            # This depends on Kick's data structure
            
            # Try different possible paths
            possible_paths = [
                ['video', 'playbackUrl'],
                ['video', 'streamUrl'],
                ['video', 'url'],
                ['playbackUrl'],
                ['streamUrl'],
                ['url'],
                ['video', 'data', 'playbackUrl'],
                ['video', 'data', 'streamUrl'],
            ]
            
            for path in possible_paths:
                value = self._get_nested_value(video_data, path)
                if value and isinstance(value, str) and ('http' in value or 'm3u8' in value):
                    print(f"✅ Found stream URL: {value[:100]}...")
                    return value
            
            # If no direct URL found, look for HLS manifest
            hls_patterns = [
                ['video', 'hlsUrl'],
                ['hlsUrl'],
                ['video', 'manifestUrl'],
                ['manifestUrl'],
            ]
            
            for path in hls_patterns:
                value = self._get_nested_value(video_data, path)
                if value and isinstance(value, str) and 'm3u8' in value:
                    print(f"✅ Found HLS manifest: {value[:100]}...")
                    return value
            
            print("❌ No stream URL found in video data")
            return None
            
        except Exception as e:
            print(f"❌ Error extracting stream URL: {e}")
            return None
    
    def _extract_metadata(self, video_data: Dict) -> Dict[str, Any]:
        """Extract metadata from video data"""
        try:
            metadata = {}
            
            # Extract title
            title_paths = [
                ['video', 'title'],
                ['title'],
                ['video', 'name'],
                ['name'],
            ]
            
            for path in title_paths:
                value = self._get_nested_value(video_data, path)
                if value:
                    metadata['title'] = str(value)
                    break
            
            # Extract duration
            duration_paths = [
                ['video', 'duration'],
                ['duration'],
                ['video', 'length'],
                ['length'],
            ]
            
            for path in duration_paths:
                value = self._get_nested_value(video_data, path)
                if value and isinstance(value, (int, float)):
                    metadata['duration'] = float(value)
                    break
            
            # Extract uploader
            uploader_paths = [
                ['video', 'uploader'],
                ['uploader'],
                ['video', 'channel'],
                ['channel'],
                ['video', 'user', 'username'],
                ['user', 'username'],
            ]
            
            for path in uploader_paths:
                value = self._get_nested_value(video_data, path)
                if value:
                    metadata['uploader'] = str(value)
                    break
            
            # Extract view count
            views_paths = [
                ['video', 'viewCount'],
                ['viewCount'],
                ['video', 'views'],
                ['views'],
            ]
            
            for path in views_paths:
                value = self._get_nested_value(video_data, path)
                if value and isinstance(value, (int, float)):
                    metadata['view_count'] = int(value)
                    break
            
            # Extract thumbnail
            thumbnail_paths = [
                ['video', 'thumbnail'],
                ['thumbnail'],
                ['video', 'preview'],
                ['preview'],
            ]
            
            for path in thumbnail_paths:
                value = self._get_nested_value(video_data, path)
                if value and isinstance(value, str) and 'http' in value:
                    metadata['thumbnail'] = str(value)
                    break
            
            return metadata
            
        except Exception as e:
            print(f"❌ Error extracting metadata: {e}")
            return {}
    
    def _get_nested_value(self, data: Dict, path: list) -> Any:
        """Get nested value from dictionary using path"""
        try:
            current = data
            for key in path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return None
            return current
        except Exception:
            return None
    
    def get_stream_url(self, url: str) -> Optional[str]:
        """Get stream URL from Kick video URL"""
        try:
            video_info = self.extract_video_info(url)
            if video_info and 'stream_url' in video_info:
                return video_info['stream_url']
            return None
        except Exception as e:
            print(f"❌ Error getting stream URL: {e}")
            return None 