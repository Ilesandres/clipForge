#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for icon build functionality
"""

import os
import subprocess
from pathlib import Path

def test_icon_exists():
    """Test if the icon file exists and is valid"""
    print("Testing Icon File")
    print("=" * 40)
    
    icon_path = Path("assets/clipforge.ico")
    
    if icon_path.exists():
        size_kb = icon_path.stat().st_size / 1024
        print(f"✓ Icon found: {icon_path}")
        print(f"✓ Size: {size_kb:.1f} KB")
        
        # Check if it's a valid ICO file
        if size_kb > 1:  # ICO files should be at least 1KB
            print("✓ Icon appears to be valid")
            return True
        else:
            print("✗ Icon file seems too small")
            return False
    else:
        print(f"✗ Icon not found: {icon_path}")
        return False

def test_pyinstaller_icon_support():
    """Test if PyInstaller supports icon parameter"""
    print("\nTesting PyInstaller Icon Support")
    print("=" * 40)
    
    try:
        import PyInstaller
        print(f"✓ PyInstaller version: {PyInstaller.__version__}")
        
        # Test the help command to see if --icon is supported
        result = subprocess.run(
            ["pyinstaller", "--help"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if "--icon" in result.stdout:
            print("✓ PyInstaller supports --icon parameter")
            return True
        else:
            print("✗ PyInstaller doesn't seem to support --icon")
            return False
            
    except ImportError:
        print("✗ PyInstaller not installed")
        return False
    except Exception as e:
        print(f"✗ Error testing PyInstaller: {e}")
        return False

def test_build_command():
    """Test the build command syntax"""
    print("\nTesting Build Command")
    print("=" * 40)
    
    # The command we want to test
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed", 
        "--name", "ClipForge",
        "--icon=assets/clipforge.ico",
        "--clean",
        "--noconfirm",
        "--add-data", "config;config",
        "--add-data", "gui;gui", 
        "--add-data", "processor;processor",
        "--add-data", "utils;utils",
        "main.py"
    ]
    
    print("Command to test:")
    print(" ".join(cmd))
    print()
    
    # Check if all required files exist
    required_files = [
        "main.py",
        "assets/clipforge.ico",
        "config/",
        "gui/",
        "processor/",
        "utils/"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (missing)")
            all_exist = False
    
    return all_exist

def main():
    """Run all icon build tests"""
    print("ClipForge - Icon Build Test")
    print("=" * 50)
    
    # Run tests
    icon_ok = test_icon_exists()
    pyinstaller_ok = test_pyinstaller_icon_support()
    build_ok = test_build_command()
    
    print("\n" + "=" * 50)
    print("Icon Build Test Results")
    print("=" * 50)
    
    if icon_ok and pyinstaller_ok and build_ok:
        print("✅ All tests passed!")
        print("You can build with icon using:")
        print("pyinstaller --onefile --windowed --name ClipForge --icon=assets/clipforge.ico --clean --noconfirm --add-data \"config;config\" --add-data \"gui;gui\" --add-data \"processor;processor\" --add-data \"utils;utils\" main.py")
        print("\nOr simply run: build_with_icon.bat")
    else:
        print("❌ Some tests failed:")
        if not icon_ok:
            print("- Icon file issue")
        if not pyinstaller_ok:
            print("- PyInstaller issue")
        if not build_ok:
            print("- Build command issue")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 