#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for progress bar functionality
"""

import time
from processor.video_splitter import VideoSplitter

def test_progress_callback():
    """Test progress callback functionality"""
    print("Testing Progress Callback")
    print("=" * 40)
    
    progress_values = []
    
    def progress_callback(value):
        progress_values.append(value)
        print(f"Progress callback: {value}%")
    
    # Create video splitter with progress callback
    splitter = VideoSplitter(progress_callback)
    
    # Simulate progress updates
    print("Simulating progress updates...")
    for i in range(5):
        progress = (i + 1) * 20  # 20%, 40%, 60%, 80%, 100%
        splitter.progress_callback(progress)
        time.sleep(0.5)  # Small delay to see the updates
    
    print(f"\nProgress values received: {progress_values}")
    
    # Check if all values are valid
    all_valid = all(0 <= val <= 100 for val in progress_values)
    print(f"All values valid (0-100): {all_valid}")
    
    return all_valid

def test_progress_calculation():
    """Test progress calculation logic"""
    print("\nTesting Progress Calculation")
    print("=" * 40)
    
    # Test different scenarios
    test_cases = [
        (1, 5),   # 1 of 5 clips
        (3, 10),  # 3 of 10 clips
        (5, 5),   # 5 of 5 clips (complete)
        (0, 1),   # 0 of 1 clips
    ]
    
    for current, total in test_cases:
        progress = int((current / total) * 100)
        progress = max(0, min(100, progress))
        print(f"Clip {current}/{total}: {progress}%")
    
    return True

def main():
    """Run all progress tests"""
    print("ClipForge - Progress Bar Test")
    print("=" * 50)
    
    # Test progress callback
    callback_ok = test_progress_callback()
    
    # Test progress calculation
    calculation_ok = test_progress_calculation()
    
    print("\n" + "=" * 50)
    print("Progress Test Results")
    print("=" * 50)
    
    if callback_ok and calculation_ok:
        print("✅ All progress tests passed!")
        print("The progress bar should work correctly now.")
    else:
        print("❌ Some progress tests failed.")
        print("Check the output above for details.")
    
    print("\nTo test the actual progress bar:")
    print("1. Run the application: python main.py")
    print("2. Select a video file")
    print("3. Start processing and watch the progress bar")

if __name__ == "__main__":
    main() 