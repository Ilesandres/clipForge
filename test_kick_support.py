#!/usr/bin/env python3
"""
Test script to verify Kick URL support with improved anti-bot measures
"""

import sys
from pathlib import Path
from processor.url_processor import URLProcessor
from processor.url_clip_processor_v8 import URLClipProcessorV8

def test_kick_support():
    """Test Kick URL support"""
    
    # Test URL (the one that was failing)
    test_url = "https://kick.com/jameseopessego/videos/295ca282-7b8e-4348-b47b-f48ef12d1bf8"
    
    print("🎮 Testing Kick URL Support")
    print("=" * 50)
    
    # Test URL processor first
    print("\n1️⃣ Testing URL processor...")
    processor = URLProcessor()
    
    # Check if URL is supported
    support_info = processor.is_supported_url(test_url)
    print(f"✅ Platform: {support_info['platform_name']}")
    print(f"✅ Supported: {support_info['supported']}")
    
    if not support_info['supported']:
        print("❌ URL not supported")
        return False
    
    # Test video info extraction
    print("\n2️⃣ Testing video info extraction...")
    video_info = processor.get_video_info(test_url)
    
    if video_info:
        print(f"✅ Title: {video_info['title']}")
        print(f"✅ Duration: {processor.format_duration(video_info['duration'])}")
        print(f"✅ Uploader: {video_info['uploader']}")
        print(f"✅ Platform: {video_info['platform']}")
        print(f"✅ View count: {video_info['view_count']}")
    else:
        print("❌ Failed to get video info")
        return False
    
    # Test V8 processor
    print("\n3️⃣ Testing V8 processor...")
    v8_processor = URLClipProcessorV8()
    
    # Test preview
    preview = v8_processor.get_video_preview(test_url)
    
    if preview['valid']:
        print(f"✅ Preview successful: {preview['title']}")
        print(f"✅ Duration: {preview['duration_formatted']}")
        print(f"✅ Platform: {preview['platform']}")
    else:
        print(f"❌ Preview failed: {preview['error']}")
        return False
    
    # Test stream URL extraction
    print("\n4️⃣ Testing stream URL extraction...")
    stream_url = v8_processor._get_stream_url(test_url)
    
    if stream_url:
        print(f"✅ Stream URL obtained: {stream_url[:100]}...")
        
        # Test a short clip extraction
        print("\n5️⃣ Testing short clip extraction...")
        output_dir = Path("test_kick_output")
        output_dir.mkdir(exist_ok=True)
        
        # Try to extract just 10 seconds
        result = v8_processor.process_url_video(test_url, output_dir, 10)
        
        if result['success']:
            print(f"✅ Successfully created {result['successful_clips']} clips")
            for file_path in result['output_files']:
                print(f"✅ Clip: {file_path}")
        else:
            print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            return False
    else:
        print("❌ Failed to get stream URL")
        return False
    
    print("\n🎉 Kick support test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_kick_support()
    sys.exit(0 if success else 1) 