#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for URL Clip Processor V8 - Real Streaming
Tests that the processor extracts clips without downloading the full video
"""

import sys
from pathlib import Path
from processor.url_clip_processor_v8 import URLClipProcessorV8

def test_v8_streaming():
    """Test V8 streaming functionality"""
    
    # Test URLs
    test_urls = [
        "https://www.youtube.com/watch?v=nCyPQzEvTJ4",
        "https://www.twitch.tv/videos/2525717665"
    ]
    
    # Create output directory
    output_dir = Path("test_output_v8")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize processor
    processor = URLClipProcessorV8()
    
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"Testing URL: {url}")
        print(f"{'='*60}")
        
        try:
            # Test video preview
            print("\n1. Testing video preview...")
            preview = processor.get_video_preview(url)
            if preview['success']:
                print(f"✅ Title: {preview['title']}")
                print(f"✅ Duration: {preview['duration_formatted']}")
                print(f"✅ Platform: {preview['platform']}")
                
                # Test processing with 30s clips
                print(f"\n2. Testing clip processing (30s clips)...")
                result = processor.process_url_video(url, output_dir, 30)
                
                if result['success']:
                    print(f"✅ Processing successful!")
                    print(f"✅ Total clips: {result['total_clips']}")
                    print(f"✅ Successful clips: {result['successful_clips']}")
                    print(f"✅ Output folder: {result['output_folder']}")
                    
                    # List output files
                    if result['output_files']:
                        print(f"✅ Output files:")
                        for file_path in result['output_files']:
                            file_size = Path(file_path).stat().st_size
                            print(f"   - {Path(file_path).name} ({file_size} bytes)")
                else:
                    print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ Preview failed: {preview.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("Test completed!")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_v8_streaming() 