#!/usr/bin/env python3
"""
Test script to verify Kick URLs are properly handled as unsupported
"""

import sys
from processor.url_processor import URLProcessor
from processor.url_clip_processor_v8 import URLClipProcessorV8

def test_kick_disabled():
    """Test that Kick URLs are properly handled as unsupported"""
    
    # Test URL
    test_url = "https://kick.com/jameseopessego/videos/295ca282-7b8e-4348-b47b-f48ef12d1bf8"
    
    print("🚫 Testing Kick URL Handling (Disabled)")
    print("=" * 50)
    
    # Test URL processor
    print("\n1️⃣ Testing URL processor...")
    processor = URLProcessor()
    
    # Check if URL is supported
    support_info = processor.is_supported_url(test_url)
    print(f"✅ Platform: {support_info['platform_name']}")
    print(f"✅ Supported: {support_info['supported']}")
    
    if support_info['supported']:
        print("❌ Kick should not be supported")
        return False
    
    # Test validation
    print("\n2️⃣ Testing URL validation...")
    validation = processor.validate_url(test_url)
    
    if validation['valid']:
        print("❌ Kick URL should not be valid")
        return False
    
    print(f"✅ Validation error: {validation['error']}")
    
    # Test V8 processor
    print("\n3️⃣ Testing V8 processor...")
    v8_processor = URLClipProcessorV8()
    
    # Test preview
    preview = v8_processor.get_video_preview(test_url)
    
    if preview['valid']:
        print("❌ Kick preview should not be valid")
        return False
    
    print(f"✅ Preview error: {preview['error']}")
    
    # Test with a valid YouTube URL for comparison
    print("\n4️⃣ Testing with valid YouTube URL for comparison...")
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    youtube_support = processor.is_supported_url(youtube_url)
    print(f"✅ YouTube supported: {youtube_support['supported']}")
    
    youtube_validation = processor.validate_url(youtube_url)
    print(f"✅ YouTube valid: {youtube_validation['valid']}")
    
    print("\n🎉 Kick disabled test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_kick_disabled()
    sys.exit(0 if success else 1) 