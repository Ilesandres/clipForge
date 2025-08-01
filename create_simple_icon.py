#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create simple icon with multiple sizes for Windows taskbar
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import QRect, QSize, Qt

def create_simple_icon():
    """Create a simple icon with multiple sizes"""
    
    print("🎨 Creating simple icon with multiple sizes...")
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create icon
    icon = QIcon()
    
    # Windows taskbar sizes
    sizes = [16, 32, 48, 64, 128, 256]
    
    for size in sizes:
        print(f"📐 Creating {size}x{size}...")
        
        # Create pixmap
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(0, 120, 215))  # Windows blue
        
        # Create painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw text
        painter.setPen(QColor(255, 255, 255))
        font_size = max(6, size // 4)
        font = QFont("Arial", font_size, QFont.Bold)
        painter.setFont(font)
        
        # Draw "CF" text
        painter.drawText(QRect(0, 0, size, size), Qt.AlignCenter, "CF")
        painter.end()
        
        # Add to icon
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        
        print(f"✅ {size}x{size} created")
    
    # Save icon - use the largest pixmap
    icon_path = Path(__file__).parent / "assets" / "clipforge_multi.ico"
    
    # Get the largest pixmap and save it
    largest_pixmap = icon.pixmap(QSize(256, 256))
    success = largest_pixmap.save(str(icon_path), "ICO")
    
    if success:
        print(f"✅ Icon saved to: {icon_path}")
        
        # Test the saved icon
        test_icon = QIcon(str(icon_path))
        available_sizes = test_icon.availableSizes()
        print(f"✅ Available sizes: {available_sizes}")
        
        return icon_path
    else:
        print("❌ Failed to save icon")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("SIMPLE ICON CREATOR")
    print("=" * 50)
    
    icon_path = create_simple_icon()
    
    if icon_path and icon_path.exists():
        print(f"\n✅ Success! Icon created at: {icon_path}")
        print(f"📁 File size: {icon_path.stat().st_size} bytes")
    else:
        print("\n❌ Failed to create icon") 