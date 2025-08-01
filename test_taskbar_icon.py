#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify taskbar icon display in Windows
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

def test_taskbar_icon():
    """Test if the application icon appears in Windows taskbar"""
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("ClipForge")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("ClipForge")
    
    # Check if icon file exists
    icon_path = Path(__file__).parent / "assets" / "clipforge.ico"
    print(f"🔍 Testing taskbar icon display...")
    print(f"📁 Icon path: {icon_path}")
    print(f"📁 Icon exists: {icon_path.exists()}")
    
    if icon_path.exists():
        # Get file info
        file_size = icon_path.stat().st_size
        print(f"📁 Icon file size: {file_size} bytes")
        
        try:
            # Create QIcon object
            icon = QIcon(str(icon_path))
            
            # Check if icon is valid
            if not icon.isNull():
                print(f"✅ Icon loaded successfully")
                
                # Get available sizes
                sizes = icon.availableSizes()
                print(f"✅ Available icon sizes: {sizes}")
                
                # Set application icon
                app.setWindowIcon(icon)
                print(f"✅ Application icon set")
                
                # Create test window
                window = QMainWindow()
                window.setWindowTitle("ClipForge - Taskbar Icon Test")
                window.setMinimumSize(500, 400)
                
                # Set window icon
                window.setWindowIcon(icon)
                print(f"✅ Window icon set")
                
                # Create central widget
                central_widget = QWidget()
                window.setCentralWidget(central_widget)
                
                # Create layout
                layout = QVBoxLayout(central_widget)
                
                # Add title
                title_label = QLabel("🔍 Taskbar Icon Test")
                title_label.setAlignment(Qt.AlignCenter)
                title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px;")
                layout.addWidget(title_label)
                
                # Add icon info
                info_text = f"""
                📋 Icon Information:
                • Path: {icon_path}
                • Size: {file_size} bytes
                • Available sizes: {sizes}
                • Icon valid: ✅ Yes
                
                📋 What to check:
                • Look at the Windows taskbar
                • Check the window title bar
                • Minimize the window to see taskbar icon
                """
                
                info_label = QLabel(info_text)
                info_label.setAlignment(Qt.AlignLeft)
                info_label.setStyleSheet("font-size: 12px; font-family: monospace; margin: 20px;")
                layout.addWidget(info_label)
                
                # Add test button
                test_btn = QPushButton("🔄 Test Icon Display")
                test_btn.setStyleSheet("font-size: 14px; padding: 10px; margin: 20px;")
                test_btn.clicked.connect(lambda: print("✅ Button clicked - check taskbar icon"))
                layout.addWidget(test_btn)
                
                # Add instructions
                instructions = QLabel("""
                📋 Instructions:
                1. Check if the icon appears in the Windows taskbar
                2. Minimize this window and look for the icon
                3. Check the window title bar for the icon
                4. If no icon appears, there might be an issue with the .ico file
                """)
                instructions.setAlignment(Qt.AlignLeft)
                instructions.setStyleSheet("font-size: 11px; color: #666; margin: 20px;")
                layout.addWidget(instructions)
                
                # Show window
                window.show()
                
                print("✅ Test window created and shown")
                print("📋 Check the Windows taskbar for the ClipForge icon")
                print("📋 Also check the window title bar")
                
                return app.exec_()
            else:
                print(f"❌ Icon file is invalid or corrupted")
                return 1
                
        except Exception as e:
            print(f"❌ Error loading icon: {e}")
            return 1
    else:
        print(f"❌ Icon file not found")
        return 1

if __name__ == "__main__":
    test_taskbar_icon() 