#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify application icon display
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

def test_icon():
    """Test if the application icon is displayed correctly"""
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("ClipForge")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("ClipForge")
    
    # Check if icon file exists
    icon_path = Path(__file__).parent / "assets" / "clipforge.ico"
    print(f"Checking icon file: {icon_path}")
    print(f"Icon file exists: {icon_path.exists()}")
    
    if icon_path.exists():
        # Get file size
        file_size = icon_path.stat().st_size
        print(f"Icon file size: {file_size} bytes")
        
        # Set application icon
        app.setWindowIcon(QIcon(str(icon_path)))
        print(f"✅ Application icon set from: {icon_path}")
        
        # Create test window
        window = QMainWindow()
        window.setWindowTitle("ClipForge - Icon Test")
        window.setMinimumSize(400, 300)
        
        # Set window icon
        window.setWindowIcon(QIcon(str(icon_path)))
        print(f"✅ Window icon set from: {icon_path}")
        
        # Create central widget
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Add test label
        label = QLabel("🔍 Icon Test Window")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)
        
        # Add info label
        info_label = QLabel(f"Icon path: {icon_path}\nFile size: {file_size} bytes")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 12px; color: gray;")
        layout.addWidget(info_label)
        
        # Show window
        window.show()
        
        print("✅ Test window created and shown")
        print("📋 Check the taskbar to see if the icon appears")
        print("📋 Also check the window title bar icon")
        
        return app.exec_()
    else:
        print(f"❌ Icon file not found at: {icon_path}")
        return 1

if __name__ == "__main__":
    test_icon() 