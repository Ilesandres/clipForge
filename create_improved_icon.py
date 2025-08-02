#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create improved icon with multiple sizes for Windows taskbar
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QLinearGradient
from PyQt5.QtCore import QRect, QSize, Qt

def create_improved_icon():
    """Create an improved icon with multiple sizes"""
    
    print("🎨 Creating improved icon with multiple sizes...")
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create icon with multiple sizes
    icon = QIcon()
    
    # Sizes needed for Windows taskbar
    sizes = [16, 32, 48, 64, 128, 256]
    
    for size in sizes:
        print(f"📐 Creating {size}x{size} icon...")
        
        # Create pixmap
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        # Create painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient background
        gradient = QLinearGradient(0, 0, size, size)
        gradient.setColorAt(0, QColor(0, 120, 215))  # Windows blue
        gradient.setColorAt(1, QColor(0, 84, 153))   # Darker blue
        
        # Draw rounded rectangle background
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, size, size, size * 0.2, size * 0.2)
        
        # Draw text "CF" (ClipForge)
        painter.setPen(QColor(255, 255, 255))
        
        # Scale font size based on icon size
        font_size = max(8, size // 4)
        font = QFont("Arial", font_size, QFont.Bold)
        painter.setFont(font)
        
        # Draw text
        painter.drawText(QRect(0, 0, size, size), Qt.AlignCenter, "CF")
        
        # Add a small accent
        if size >= 32:
            # Draw a small circle in corner
            accent_size = size // 8
            painter.setBrush(QColor(255, 255, 255, 100))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(size - accent_size - 2, 2, accent_size, accent_size)
        
        painter.end()
        
        # Add to icon
        icon.addPixmap(pixmap)
        
        print(f"✅ {size}x{size} icon created")
    
    # Save the icon
    icon_path = Path(__file__).parent / "assets" / "clipforge_improved.ico"
    icon.save(str(icon_path), "ICO")
    
    print(f"✅ Improved icon saved to: {icon_path}")
    
    # Test the icon
    print("\n🔍 Testing improved icon...")
    test_icon = QIcon(str(icon_path))
    available_sizes = test_icon.availableSizes()
    print(f"✅ Available sizes: {available_sizes}")
    
    return icon_path

def test_icon_in_window():
    """Test the improved icon in a window"""
    print("\n🪟 Testing icon in window...")
    
    from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
    
    # Create window
    window = QMainWindow()
    window.setWindowTitle("ClipForge - Improved Icon Test")
    window.setMinimumSize(400, 300)
    
    # Set icon
    icon_path = Path(__file__).parent / "assets" / "clipforge_improved.ico"
    if icon_path.exists():
        window.setWindowIcon(QIcon(str(icon_path)))
        print(f"✅ Window icon set from: {icon_path}")
    
    # Create central widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # Create layout
    layout = QVBoxLayout(central_widget)
    
    # Add label
    label = QLabel("✅ Improved Icon Test")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 18px; font-weight: bold;")
    layout.addWidget(label)
    
    # Show window
    window.show()
    
    print("✅ Test window created")
    print("📋 Check the taskbar and title bar for the improved icon")
    
    return window

if __name__ == "__main__":
    print("=" * 60)
    print("IMPROVED ICON CREATOR")
    print("=" * 60)
    
    # Create improved icon
    icon_path = create_improved_icon()
    
    if icon_path and icon_path.exists():
        print(f"\n✅ Improved icon created successfully!")
        print(f"📁 Path: {icon_path}")
        print(f"📁 Size: {icon_path.stat().st_size} bytes")
        
        # Test in window
        window = test_icon_in_window()
        
        # Keep window open
        app = QApplication.instance()
        app.exec_()
    else:
        print("❌ Failed to create improved icon") 