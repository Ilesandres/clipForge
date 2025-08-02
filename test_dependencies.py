#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify all project dependencies are installed correctly
"""

import sys
from pathlib import Path

def test_dependencies():
    """Test all project dependencies"""
    print("🔍 Testing ClipForge Dependencies...")
    print("=" * 50)
    
    # List of required dependencies with correct import names
    dependencies = [
        ("PyQt5", "PyQt5", "5.15.11", "GUI framework"),
        ("moviepy", "moviepy", "1.0.3", "Video processing"),
        ("Pillow", "PIL", "11.3.0", "Image processing"),
        ("pathlib2", "pathlib2", "2.3.7.post1", "Path utilities"),
        ("pyinstaller", "PyInstaller", "6.14.2", "Executable creation"),
        ("yt-dlp", "yt_dlp", "2023.12.30", "Video download from URLs"),
        ("requests", "requests", "2.31.0", "HTTP requests"),
        ("numpy", "numpy", "1.21.0", "Numerical computing"),
        ("decorator", "decorator", "4.4.2", "Decorator utilities"),
        ("imageio", "imageio", "2.31.0", "Image I/O"),
        ("imageio-ffmpeg", "imageio_ffmpeg", "0.4.8", "FFmpeg integration"),
        ("proglog", "proglog", "0.1.9", "Progress logging"),
        ("tqdm", "tqdm", "4.64.0", "Progress bars")
    ]
    
    all_passed = True
    
    for package_name, import_name, min_version, description in dependencies:
        try:
            # Try to import the package
            module = __import__(import_name)
            
            # Get version
            if hasattr(module, '__version__'):
                version = module.__version__
            elif hasattr(module, 'version') and hasattr(module.version, '__version__'):
                version = module.version.__version__
            elif import_name == "yt_dlp" and hasattr(module, 'version'):
                version = module.version.__version__
            else:
                version = "unknown"
            
            print(f"✅ {package_name} {version} - {description}")
            
        except ImportError as e:
            print(f"❌ {package_name} - {description}")
            print(f"   Error: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    
    # Test specific functionality
    print("\n🧪 Testing specific functionality...")
    
    # Test PyQt5
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QIcon
        print("✅ PyQt5 GUI components working")
    except Exception as e:
        print(f"❌ PyQt5 GUI test failed: {e}")
        all_passed = False
    
    # Test moviepy
    try:
        from moviepy.editor import VideoFileClip
        print("✅ MoviePy video processing working")
    except Exception as e:
        print(f"❌ MoviePy test failed: {e}")
        all_passed = False
    
    # Test yt-dlp
    try:
        import yt_dlp
        print("✅ yt-dlp video download working")
    except Exception as e:
        print(f"❌ yt-dlp test failed: {e}")
        all_passed = False
    
    # Test requests
    try:
        import requests
        print("✅ requests HTTP library working")
    except Exception as e:
        print(f"❌ requests test failed: {e}")
        all_passed = False
    
    # Test project modules
    print("\n📦 Testing project modules...")
    
    try:
        from config.config_manager import ConfigManager
        print("✅ ConfigManager imported successfully")
    except Exception as e:
        print(f"❌ ConfigManager import failed: {e}")
        all_passed = False
    
    try:
        from utils.file_utils import FileUtils
        print("✅ FileUtils imported successfully")
    except Exception as e:
        print(f"❌ FileUtils import failed: {e}")
        all_passed = False
    
    try:
        from processor.video_splitter import VideoSplitter
        print("✅ VideoSplitter imported successfully")
    except Exception as e:
        print(f"❌ VideoSplitter import failed: {e}")
        all_passed = False
    
    try:
        from processor.url_processor import URLProcessor
        print("✅ URLProcessor imported successfully")
    except Exception as e:
        print(f"❌ URLProcessor import failed: {e}")
        all_passed = False
    
    try:
        from processor.url_clip_processor_v8 import URLClipProcessorV8
        print("✅ URLClipProcessorV8 imported successfully")
    except Exception as e:
        print(f"❌ URLClipProcessorV8 import failed: {e}")
        all_passed = False
    
    try:
        from gui.main_window import MainWindow
        print("✅ MainWindow imported successfully")
    except Exception as e:
        print(f"❌ MainWindow import failed: {e}")
        all_passed = False
    
    try:
        from gui.url_window import URLWindow
        print("✅ URLWindow imported successfully")
    except Exception as e:
        print(f"❌ URLWindow import failed: {e}")
        all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 All dependencies and modules are working correctly!")
        print("✅ ClipForge is ready to use!")
        return True
    else:
        print("❌ Some dependencies or modules failed to load.")
        print("💡 Try running: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = test_dependencies()
    sys.exit(0 if success else 1) 