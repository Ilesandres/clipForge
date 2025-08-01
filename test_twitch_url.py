#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Twitch URL Processing
Tests the compatibility with Twitch video URLs
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_twitch_url():
    """Test Twitch URL processing"""
    print("Testing Twitch URL processing...")
    
    try:
        from processor.url_processor import URLProcessor
        
        processor = URLProcessor()
        
        # Test URL from the user
        test_url = "https://www.twitch.tv/videos/2525717665"
        
        print(f"Testing URL: {test_url}")
        print("-" * 50)
        
        # Test 1: Check if URL is supported
        print("1. Checking if URL is supported...")
        support_result = processor.is_supported_url(test_url)
        print(f"   Supported: {support_result['supported']}")
        print(f"   Platform: {support_result['platform']}")
        print()
        
        # Test 2: Get video info
        print("2. Getting video information...")
        video_info = processor.get_video_info(test_url)
        
        if video_info:
            print(f"   ✅ Success!")
            print(f"   Title: {video_info['title']}")
            print(f"   Duration: {processor.format_duration(video_info['duration'])}")
            print(f"   Uploader: {video_info['uploader']}")
            print(f"   View Count: {video_info['view_count']:,}")
            print(f"   Platform: {video_info['platform']}")
            print(f"   Available Formats: {len(video_info['formats'])}")
            
            # Show available formats
            if video_info['formats']:
                print("   Formats:")
                for fmt in video_info['formats'][:3]:  # Show first 3 formats
                    print(f"     - {fmt['format_id']}: {fmt['height']}p ({fmt['ext']})")
        else:
            print("   ❌ Failed to get video info")
        print()
        
        # Test 3: Validate URL
        print("3. Validating URL...")
        validation = processor.validate_url(test_url)
        print(f"   Valid: {validation['valid']}")
        if not validation['valid']:
            print(f"   Error: {validation['error']}")
        else:
            print(f"   Platform: {validation['platform']}")
            print(f"   Video Info: {validation['video_info']['title']}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Twitch URL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_twitch_formats():
    """Test available formats for Twitch"""
    print("\nTesting Twitch formats...")
    
    try:
        import yt_dlp
        
        test_url = "https://www.twitch.tv/videos/2525717665"
        
        # Test different format options
        format_options = [
            'best',
            'best[height<=720]',
            'best[height<=480]',
            'worst',
            'bestvideo+bestaudio'
        ]
        
        for fmt in format_options:
            print(f"Testing format: {fmt}")
            try:
                opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'format': fmt,
                }
                
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(test_url, download=False)
                    if info:
                        print(f"  ✅ Success with format '{fmt}'")
                        if 'formats' in info:
                            print(f"  Available formats: {len(info['formats'])}")
                    else:
                        print(f"  ❌ Failed with format '{fmt}'")
                        
            except Exception as e:
                print(f"  ❌ Error with format '{fmt}': {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Twitch formats: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("ClipForge - Twitch URL Test")
    print("=" * 60)
    
    tests = [
        ("Twitch URL Processing", test_twitch_url),
        ("Twitch Formats", test_twitch_formats),
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
        print("🎉 All tests passed! Twitch URLs are working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 