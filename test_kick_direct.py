#!/usr/bin/env python3
"""
Test script for direct Kick stream extraction
"""

import sys
from pathlib import Path
from processor.kick_stream_extractor import KickStreamExtractor
from processor.url_processor import URLProcessor

def test_kick_direct_extraction():
    """Test direct Kick extraction method"""
    
    # Test URL (the one that was failing)
    test_url = "https://kick.com/jameseopessego/videos/295ca282-7b8e-4348-b47b-f48ef12d1bf8"
    
    print("🎮 Testing Direct Kick Extraction")
    print("=" * 50)
    
    # Test direct extractor
    print("\n1️⃣ Testing direct Kick extractor...")
    extractor = KickStreamExtractor()
    
    # Test video info extraction
    print("\n2️⃣ Extracting video info directly...")
    video_info = extractor.extract_video_info(test_url)
    
    if video_info:
        print(f"✅ Title: {video_info.get('title', 'Unknown')}")
        print(f"✅ Duration: {video_info.get('duration', 0)} seconds")
        print(f"✅ Uploader: {video_info.get('uploader', 'Unknown')}")
        print(f"✅ View count: {video_info.get('view_count', 0)}")
        print(f"✅ Stream URL: {video_info.get('stream_url', 'None')[:100]}..." if video_info.get('stream_url') else "❌ No stream URL")
        print(f"✅ Thumbnail: {video_info.get('thumbnail', 'None')}")
    else:
        print("❌ Failed to extract video info directly")
        return False
    
    # Test stream URL extraction
    print("\n3️⃣ Testing stream URL extraction...")
    stream_url = extractor.get_stream_url(test_url)
    
    if stream_url:
        print(f"✅ Stream URL obtained: {stream_url[:100]}...")
    else:
        print("❌ Failed to get stream URL")
        return False
    
    # Test URL processor integration
    print("\n4️⃣ Testing URL processor integration...")
    processor = URLProcessor()
    
    # Test video info through URL processor
    processor_info = processor.get_video_info(test_url)
    
    if processor_info:
        print(f"✅ URL processor title: {processor_info.get('title', 'Unknown')}")
        print(f"✅ URL processor duration: {processor_info.get('duration', 0)}")
        print(f"✅ URL processor uploader: {processor_info.get('uploader', 'Unknown')}")
        print(f"✅ URL processor platform: {processor_info.get('platform', 'Unknown')}")
        
        # Check if we have formats
        formats = processor_info.get('formats', [])
        if formats:
            print(f"✅ Found {len(formats)} format(s)")
            for i, fmt in enumerate(formats):
                print(f"   Format {i+1}: {fmt.get('url', 'No URL')[:50]}...")
        else:
            print("⚠️ No formats found")
    else:
        print("❌ URL processor failed")
        return False
    
    print("\n🎉 Direct Kick extraction test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_kick_direct_extraction()
    sys.exit(0 if success else 1) 