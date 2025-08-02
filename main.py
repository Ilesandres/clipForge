#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClipForge - Video Clipping Application
Main entry point for the application
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow
from config.config_manager import ConfigManager


def main():
    """Main application entry point"""
    # Create QApplication instance
    app = QApplication(sys.argv)
    app.setApplicationName("ClipForge")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("ClipForge")
    
    # Set application icon with improved configuration
    icon_path = Path(__file__).parent / "assets" / "clipforge_multi.ico"
    if not icon_path.exists():
        # Fallback to other icons
        icon_path = Path(__file__).parent / "assets" / "clipforge-16x16.ico"
        if not icon_path.exists():
            icon_path = Path(__file__).parent / "assets" / "clipforge.ico"
    
    if icon_path.exists():
        try:
            # Create QIcon object
            icon = QIcon(str(icon_path))
            
            # Check if icon is valid
            if not icon.isNull():
                # Set application icon
                app.setWindowIcon(icon)
                print(f"✅ Application icon set successfully from: {icon_path}")
                print(f"✅ Icon sizes available: {icon.availableSizes()}")
            else:
                print(f"⚠️ Warning: Icon file exists but is invalid: {icon_path}")
        except Exception as e:
            print(f"⚠️ Warning: Error setting application icon: {e}")
    else:
        print(f"⚠️ Warning: Icon file not found at {icon_path}")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Create and show main window
    main_window = MainWindow(config_manager)
    main_window.show()
    
    # Start application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 