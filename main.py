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
    
    # Set application icon
    icon_path = Path(__file__).parent / "assets" / "clipforge.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
        print(f"Application icon set from: {icon_path}")
    else:
        print(f"Warning: Icon file not found at {icon_path}")
    
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