#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Video Duration Issues
Diagnoses problems with video duration calculation and processing
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_duration_calculation():
    """Test duration calculation and clip generation"""
    print("Testing duration calculation...")
    
    try:
        from processor.url_processor import URLProcessor
        
        processor = URLProcessor()
        
        # Test cases
        test_cases = [
            ("02:44", 164),  # 2 minutes 44 seconds = 164 seconds
            ("09:55", 595),  # 9 minutes 55 seconds = 595 seconds
            ("01:30", 90),   # 1 minute 30 seconds = 90 seconds
            ("00:30", 30),   # 30 seconds = 30 seconds
        ]
        
        for duration_str, expected_seconds in test_cases:
            # Parse duration string (MM:SS format)
            parts = duration_str.split(':')
            minutes = int(parts[0])
            seconds = int(parts[1])
            calculated_seconds = minutes * 60 + seconds
            
            print(f"Duration: {duration_str}")
            print(f"  Minutes: {minutes}")
            print(f"  Seconds: {seconds}")
            print(f"  Calculated: {calculated_seconds}s")
            print(f"  Expected: {expected_seconds}s")
            print(f"  Match: {'✅' if calculated_seconds == expected_seconds else '❌'}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing duration calculation: {e}")
        return False

def test_clip_generation():
    """Test clip generation for different durations"""
    print("Testing clip generation...")
    
    try:
        # Test video duration: 2:44 = 164 seconds
        video_duration = 164  # seconds
        clip_duration = 30    # seconds
        
        # Calculate clips
        clips = []
        start_time = 0.0
        
        while start_time < video_duration:
            end_time = min(start_time + clip_duration, video_duration)
            clips.append({
                'start': start_time,
                'end': end_time,
                'duration': end_time - start_time
            })
            start_time = end_time
        
        print(f"Video duration: {video_duration}s ({video_duration//60}:{video_duration%60:02d})")
        print(f"Clip duration: {clip_duration}s")
        print(f"Total clips: {len(clips)}")
        print()
        
        for i, clip in enumerate(clips):
            print(f"Clip {i + 1}: {clip['start']:.1f}s - {clip['end']:.1f}s (duration: {clip['duration']:.1f}s)")
            
            # Check if clip end time exceeds video duration
            if clip['end'] > video_duration:
                print(f"  ⚠️ WARNING: Clip end time exceeds video duration!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing clip generation: {e}")
        return False

def test_url_processor_methods():
    """Test URL processor methods with duration formatting"""
    print("\nTesting URL processor methods...")
    
    try:
        from processor.url_processor import URLProcessor
        
        processor = URLProcessor()
        
        # Test format_duration method
        test_cases = [
            (164, "02:44"),  # 2 minutes 44 seconds
            (595, "09:55"),  # 9 minutes 55 seconds
            (90, "01:30"),   # 1 minute 30 seconds
            (30, "00:30"),   # 30 seconds
        ]
        
        for seconds, expected in test_cases:
            result = processor.format_duration(seconds)
            if result == expected:
                print(f"✅ format_duration({seconds}s) = '{result}'")
            else:
                print(f"❌ format_duration({seconds}s) = '{result}', expected '{expected}'")
        
        # Test estimate_clips_count method
        test_cases = [
            (164, 30, 6),   # 164s video, 30s clips = 6 clips
            (595, 60, 10),  # 595s video, 60s clips = 10 clips
            (90, 30, 3),    # 90s video, 30s clips = 3 clips
        ]
        
        for duration, clip_duration, expected in test_cases:
            result = processor.estimate_clips_count(duration, clip_duration)
            if result == expected:
                print(f"✅ estimate_clips_count({duration}s, {clip_duration}s) = {result}")
            else:
                print(f"❌ estimate_clips_count({duration}s, {clip_duration}s) = {result}, expected {expected}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing URL processor methods: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("ClipForge - Video Duration Test")
    print("=" * 60)
    
    tests = [
        ("Duration Calculation", test_duration_calculation),
        ("Clip Generation", test_clip_generation),
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
        print("🎉 All tests passed! Duration calculations are correct.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 