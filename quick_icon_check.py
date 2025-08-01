#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick icon check
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

def check_icon():
    app = QApplication(sys.argv)
    
    # Check both icon files
    icon_files = [
        "assets/clipforge-16x16.ico",
        "assets/clipforge.ico"
    ]
    
    for icon_file in icon_files:
        icon_path = Path(icon_file)
        print(f"\n🔍 Checking: {icon_path}")
        print(f"📁 Exists: {icon_path.exists()}")
        
        if icon_path.exists():
            file_size = icon_path.stat().st_size
            print(f"📁 Size: {file_size} bytes")
            
            try:
                icon = QIcon(str(icon_path))
                if not icon.isNull():
                    sizes = icon.availableSizes()
                    print(f"✅ Valid icon with sizes: {sizes}")
                else:
                    print("❌ Invalid icon")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ File not found")

if __name__ == "__main__":
    check_icon() 