#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for ClipForge
Verifies that all components work correctly
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from config.config_manager import ConfigManager
        print("✓ ConfigManager imported successfully")
    except ImportError as e:
        print(f"✗ ConfigManager import failed: {e}")
        return False
    
    try:
        from utils.file_utils import FileUtils
        print("✓ FileUtils imported successfully")
    except ImportError as e:
        print(f"✗ FileUtils import failed: {e}")
        return False
    
    try:
        from processor.video_splitter import VideoSplitter
        print("✓ VideoSplitter imported successfully")
    except ImportError as e:
        print(f"✗ VideoSplitter import failed: {e}")
        return False
    
    return True

def test_config_manager():
    """Test configuration manager functionality"""
    print("\nTesting ConfigManager...")
    
    try:
        from config.config_manager import ConfigManager
        
        # Create config manager
        config = ConfigManager()
        print("✓ ConfigManager created successfully")
        
        # Test default values
        output_path = config.get_output_path()
        print(f"✓ Default output path: {output_path}")
        
        # Test setting values
        config.set("test_key", "test_value")
        value = config.get("test_key")
        if value == "test_value":
            print("✓ Config set/get works correctly")
        else:
            print("✗ Config set/get failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ ConfigManager test failed: {e}")
        return False

def test_file_utils():
    """Test file utilities functionality"""
    print("\nTesting FileUtils...")
    
    try:
        from utils.file_utils import FileUtils
        
        # Test video file detection
        test_files = [
            "video.mp4",
            "movie.avi",
            "clip.mov",
            "document.txt",
            "image.jpg"
        ]
        
        for file in test_files:
            is_video = FileUtils.is_video_file(file)
            expected = file.split('.')[-1].lower() in ['mp4', 'avi', 'mov']
            if is_video == expected:
                print(f"✓ Video detection for {file}: {is_video}")
            else:
                print(f"✗ Video detection failed for {file}")
                return False
        
        # Test safe folder name
        safe_name = FileUtils.get_safe_folder_name("Test Video (2024).mp4")
        print(f"✓ Safe folder name: {safe_name}")
        
        # Test duration formatting
        duration_str = FileUtils.format_duration(3661)  # 1:01:01
        if duration_str == "01:01:01":
            print("✓ Duration formatting works")
        else:
            print(f"✗ Duration formatting failed: {duration_str}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ FileUtils test failed: {e}")
        return False

def test_gui_import():
    """Test GUI import (without creating window)"""
    print("\nTesting GUI imports...")
    
    try:
        # Test PyQt5 import
        from PyQt5.QtWidgets import QApplication
        print("✓ PyQt5 imported successfully")
        
        # Test GUI module import
        from gui.main_window import MainWindow
        print("✓ MainWindow imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ GUI import failed: {e}")
        print("Note: PyQt5 needs to be installed for GUI functionality")
        return False
    except Exception as e:
        print(f"✗ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("ClipForge - Component Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config_manager,
        test_file_utils,
        test_gui_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! ClipForge is ready to use.")
        print("\nTo run the application:")
        print("  python main.py")
        print("  or double-click run.bat")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTo install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("  or double-click install.bat")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 