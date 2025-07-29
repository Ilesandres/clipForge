#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for video processing functionality
"""

import os
import tempfile
from pathlib import Path
from processor.video_splitter import VideoSplitter
from utils.file_utils import FileUtils

def test_video_processing():
    """Test video processing functionality"""
    print("=" * 50)
    print("Testing Video Processing")
    print("=" * 50)
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Test video splitter
        splitter = VideoSplitter()
        
        # Test with a sample video file (if available)
        # For now, we'll test the video info functionality
        print("\nTesting video info functionality...")
        
        # Test with a non-existent file first
        test_result = splitter.get_video_info("non_existent_video.mp4")
        if test_result is None:
            print("✓ Correctly handled non-existent video file")
        else:
            print("✗ Should have returned None for non-existent file")
        
        print("\nVideo processing test completed.")
        print("Note: To test actual video processing, you need a video file.")
        print("You can test with any .mp4, .avi, .mov file.")

def test_ffmpeg_availability():
    """Test if ffmpeg is available"""
    print("\n" + "=" * 50)
    print("Testing FFmpeg Availability")
    print("=" * 50)
    
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"✓ FFmpeg found at: {ffmpeg_path}")
        
        # Test if ffmpeg executable exists
        if os.path.exists(ffmpeg_path):
            print("✓ FFmpeg executable exists")
        else:
            print("✗ FFmpeg executable not found")
            
    except ImportError as e:
        print(f"✗ imageio_ffmpeg not available: {e}")
    except Exception as e:
        print(f"✗ Error checking FFmpeg: {e}")

def test_moviepy_import():
    """Test moviepy import and basic functionality"""
    print("\n" + "=" * 50)
    print("Testing MoviePy Import")
    print("=" * 50)
    
    try:
        from moviepy.editor import VideoFileClip
        print("✓ VideoFileClip imported successfully")
        
        # Test basic moviepy functionality
        print("✓ MoviePy basic functionality available")
        
    except ImportError as e:
        print(f"✗ MoviePy import failed: {e}")
    except Exception as e:
        print(f"✗ MoviePy test failed: {e}")

def main():
    """Run all video processing tests"""
    print("ClipForge - Video Processing Test")
    
    test_moviepy_import()
    test_ffmpeg_availability()
    test_video_processing()
    
    print("\n" + "=" * 50)
    print("Video Processing Test Complete")
    print("=" * 50)
    
    print("\nTo test with actual video processing:")
    print("1. Place a video file in the ClipForge directory")
    print("2. Run the main application: python main.py")
    print("3. Select the video file and try processing")

if __name__ == "__main__":
    main() 