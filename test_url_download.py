#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test URL Download Functionality
Tests the video segment download feature
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_url_download():
    """Test URL download functionality"""
    print("Testing URL download functionality...")
    
    try:
        from processor.url_processor import URLProcessor
        
        processor = URLProcessor()
        
        # Test URL (Rick Roll - short video)
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test downloading a small segment (first 10 seconds)
            output_path = temp_path / "test_segment.mp4"
            
            print(f"Downloading segment from: {test_url}")
            print(f"Output path: {output_path}")
            
            result = processor.download_video_segment(
                test_url, 
                start_time=0.0, 
                duration=10.0, 
                output_path=output_path
            )
            
            if result and Path(result).exists():
                file_size = Path(result).stat().st_size
                print(f"✅ Segment downloaded successfully!")
                print(f"   File: {result}")
                print(f"   Size: {file_size} bytes")
                return True
            else:
                print(f"❌ Failed to download segment")
                return False
                
    except Exception as e:
        print(f"❌ Error testing URL download: {e}")
        return False

def test_url_processor_methods():
    """Test URL processor methods"""
    print("\nTesting URL processor methods...")
    
    try:
        from processor.url_processor import URLProcessor
        
        processor = URLProcessor()
        
        # Test format duration
        test_cases = [
            (30, "00:30"),
            (65, "01:05"),
            (3661, "01:01:01"),
            (0, "00:00")
        ]
        
        for seconds, expected in test_cases:
            result = processor.format_duration(seconds)
            if result == expected:
                print(f"✅ format_duration({seconds}) = '{result}'")
            else:
                print(f"❌ format_duration({seconds}) = '{result}', expected '{expected}'")
                return False
        
        # Test estimate clips count
        test_cases = [
            (100, 30, 4),  # 100s video, 30s clips = 4 clips
            (90, 30, 3),   # 90s video, 30s clips = 3 clips
            (30, 30, 1),   # 30s video, 30s clips = 1 clip
        ]
        
        for duration, clip_duration, expected in test_cases:
            result = processor.estimate_clips_count(duration, clip_duration)
            if result == expected:
                print(f"✅ estimate_clips_count({duration}, {clip_duration}) = {result}")
            else:
                print(f"❌ estimate_clips_count({duration}, {clip_duration}) = {result}, expected {expected}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing URL processor methods: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("ClipForge - URL Download Test")
    print("=" * 60)
    
    tests = [
        ("URL Download", test_url_download),
        ("URL Processor Methods", test_url_processor_methods),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! URL download functionality is working.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 