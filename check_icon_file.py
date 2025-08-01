#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check icon file integrity and format
"""

import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

def check_icon_file():
    """Check the icon file for issues"""
    
    icon_path = Path(__file__).parent / "assets" / "clipforge.ico"
    
    print("🔍 Checking icon file integrity...")
    print(f"📁 Path: {icon_path}")
    
    # Check if file exists
    if not icon_path.exists():
        print("❌ Icon file does not exist")
        return False
    
    # Get file info
    file_size = icon_path.stat().st_size
    print(f"📁 File size: {file_size} bytes")
    
    if file_size == 0:
        print("❌ Icon file is empty")
        return False
    
    # Check file extension
    if icon_path.suffix.lower() != '.ico':
        print("⚠️ Warning: File extension is not .ico")
    
    # Try to load with QIcon
    try:
        icon = QIcon(str(icon_path))
        
        if icon.isNull():
            print("❌ QIcon reports icon as null/invalid")
            return False
        
        # Get available sizes
        sizes = icon.availableSizes()
        print(f"✅ Available sizes: {sizes}")
        
        if not sizes:
            print("⚠️ Warning: No icon sizes available")
        else:
            print(f"✅ Icon has {len(sizes)} different sizes")
            
            # Check for common Windows taskbar sizes
            taskbar_sizes = [QSize(16, 16), QSize(32, 32), QSize(48, 48)]
            found_sizes = []
            
            for size in taskbar_sizes:
                if size in sizes:
                    found_sizes.append(f"{size.width()}x{size.height()}")
            
            if found_sizes:
                print(f"✅ Found taskbar-compatible sizes: {found_sizes}")
            else:
                print("⚠️ Warning: No taskbar-compatible sizes found")
        
        # Try to create a pixmap
        try:
            # Try different sizes
            for size in [QSize(16, 16), QSize(32, 32), QSize(48, 48)]:
                pixmap = icon.pixmap(size)
                if not pixmap.isNull():
                    print(f"✅ Successfully created {size.width()}x{size.height()} pixmap")
                else:
                    print(f"⚠️ Failed to create {size.width()}x{size.height()} pixmap")
        except Exception as e:
            print(f"⚠️ Error creating pixmap: {e}")
        
        print("✅ Icon file appears to be valid")
        return True
        
    except Exception as e:
        print(f"❌ Error loading icon: {e}")
        return False

def create_test_icon():
    """Create a simple test icon if the current one has issues"""
    print("\n🔧 Creating a simple test icon...")
    
    try:
        from PyQt5.QtGui import QPainter, QColor, QFont
        from PyQt5.QtCore import QRect
        
        # Create a simple 32x32 icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(0, 120, 215))  # Windows blue
        
        # Draw text
        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        painter.drawText(QRect(0, 0, 32, 32), Qt.AlignCenter, "CF")
        painter.end()
        
        # Save as ICO
        test_icon_path = Path(__file__).parent / "assets" / "test_icon.ico"
        pixmap.save(str(test_icon_path), "ICO")
        
        print(f"✅ Test icon created: {test_icon_path}")
        return test_icon_path
        
    except Exception as e:
        print(f"❌ Error creating test icon: {e}")
        return None

if __name__ == "__main__":
    # Create QApplication first
    app = QApplication(sys.argv)
    
    print("=" * 60)
    print("ICON FILE CHECKER")
    print("=" * 60)
    
    # Check current icon
    is_valid = check_icon_file()
    
    if not is_valid:
        print("\n" + "=" * 60)
        print("CREATING TEST ICON")
        print("=" * 60)
        test_icon = create_test_icon()
        
        if test_icon:
            print(f"\n✅ Test icon created successfully")
            print(f"📁 You can try using: {test_icon}")
    
    print("\n" + "=" * 60)
    print("CHECK COMPLETED")
    print("=" * 60) 