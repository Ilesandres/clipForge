#!/usr/bin/env python3
"""
Test script to verify YouTube audio extraction
"""

import sys
from pathlib import Path
from processor.url_clip_processor_v8 import URLClipProcessorV8

def test_youtube_audio():
    """Test YouTube audio extraction"""
    
    # Test URL (a short YouTube video)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - short video
    
    print("🎵 Testing YouTube Audio Extraction")
    print("=" * 50)
    
    # Create processor
    processor = URLClipProcessorV8()
    
    # Test video preview first
    print("\n1️⃣ Testing video preview...")
    preview = processor.get_video_preview(test_url)
    
    if not preview['valid']:
        print(f"❌ Video preview failed: {preview['error']}")
        return False
    
    print(f"✅ Video: {preview['title']}")
    print(f"✅ Duration: {preview['duration_formatted']}")
    print(f"✅ Platform: {preview['platform']}")
    
    # Test stream URL extraction
    print("\n2️⃣ Testing stream URL extraction...")
    stream_url = processor._get_stream_url(test_url)
    
    if not stream_url:
        print("❌ Failed to get stream URL")
        return False
    
    print(f"✅ Stream URL obtained: {stream_url[:100]}...")
    
    # Test segment extraction (just 10 seconds)
    print("\n3️⃣ Testing segment extraction with audio...")
    
    # Create output directory
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    # Process a short clip
    result = processor.process_url_video(test_url, output_dir, 10)
    
    if result['success']:
        print(f"✅ Successfully created {result['successful_clips']} clips")
        for file_path in result['output_files']:
            print(f"✅ Clip: {file_path}")
            
            # Check if file has audio (basic check)
            import subprocess
            try:
                # Use ffprobe to check audio streams
                cmd = [
                    'ffprobe', '-v', 'quiet', '-show_streams', 
                    '-select_streams', 'a', str(file_path)
                ]
                result_check = subprocess.run(cmd, capture_output=True, text=True)
                
                if result_check.returncode == 0 and result_check.stdout.strip():
                    print(f"✅ Audio stream detected in: {Path(file_path).name}")
                else:
                    print(f"⚠️ No audio stream detected in: {Path(file_path).name}")
                    
            except FileNotFoundError:
                print(f"⚠️ ffprobe not available, cannot verify audio")
            except Exception as e:
                print(f"⚠️ Error checking audio: {e}")
    else:
        print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
        return False
    
    print("\n🎉 YouTube audio test completed!")
    return True

if __name__ == "__main__":
    success = test_youtube_audio()
    sys.exit(0 if success else 1) 