#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test URL Functionality for ClipForge
Tests the new URL processing features
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        from processor.url_processor import URLProcessor
        print("✅ URLProcessor imported successfully")
    except ImportError as e:
        print(f"❌ Error importing URLProcessor: {e}")
        return False
    
    try:
        from processor.url_clip_processor import URLClipProcessor
        print("✅ URLClipProcessor imported successfully")
    except ImportError as e:
        print(f"❌ Error importing URLClipProcessor: {e}")
        return False
    
    try:
        from gui.url_window import URLWindow
        print("✅ URLWindow imported successfully")
    except ImportError as e:
        print(f"❌ Error importing URLWindow: {e}")
        return False
    
    return True

def test_url_processor():
    """Test URL processor functionality"""
    print("\nTesting URL processor...")
    
    try:
        from processor.url_processor import URLProcessor
        
        processor = URLProcessor()
        
        # Test supported platforms
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.twitch.tv/videos/123456789",
            "https://kick.com/video/123456",
            "https://www.unsupported.com/video/123"
        ]
        
        for url in test_urls:
            result = processor.is_supported_url(url)
            print(f"URL: {url}")
            print(f"  Supported: {result['supported']}")
            print(f"  Platform: {result['platform_name']}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing URL processor: {e}")
        return False

def test_url_validation():
    """Test URL validation"""
    print("\nTesting URL validation...")
    
    try:
        from processor.url_processor import URLProcessor
        
        processor = URLProcessor()
        
        # Test with a known YouTube video (Rick Roll)
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        print(f"Testing validation for: {test_url}")
        validation = processor.validate_url(test_url)
        
        if validation['valid']:
            print("✅ URL validation successful")
            print(f"  Platform: {validation['platform']}")
            print(f"  Title: {validation['video_info']['title']}")
            print(f"  Duration: {validation['video_info']['duration']}s")
        else:
            print(f"❌ URL validation failed: {validation['error']}")
        
        return validation['valid']
        
    except Exception as e:
        print(f"❌ Error testing URL validation: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are installed"""
    print("\nTesting dependencies...")
    
    try:
        import yt_dlp
        print(f"✅ yt-dlp version: {yt_dlp.version.__version__}")
    except ImportError:
        print("❌ yt-dlp not installed")
        return False
    
    try:
        import requests
        print(f"✅ requests version: {requests.__version__}")
    except ImportError:
        print("❌ requests not installed")
        return False
    
    return True

def test_config_manager():
    """Test config manager integration"""
    print("\nTesting config manager...")
    
    try:
        from config.config_manager import ConfigManager
        
        config = ConfigManager()
        
        # Test URL-related config
        output_path = config.get_output_path()
        print(f"✅ Output path: {output_path}")
        
        durations = config.get_available_durations()
        print(f"✅ Available durations: {durations}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing config manager: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("ClipForge - URL Functionality Test")
    print("=" * 60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Imports", test_imports),
        ("Config Manager", test_config_manager),
        ("URL Processor", test_url_processor),
        ("URL Validation", test_url_validation),
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
        print("🎉 All tests passed! URL functionality is ready.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 