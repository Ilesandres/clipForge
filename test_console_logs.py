#!/usr/bin/env python3
"""
Test script to verify console log capture functionality
"""

import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton
from PyQt5.QtCore import QTimer
from utils.logger import get_global_logger, set_global_gui_callback


class TestLogWindow(QMainWindow):
    """Test window for console log capture"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Console Log Capture")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        # Create test buttons
        test_btn = QPushButton("Test Console Output")
        test_btn.clicked.connect(self.test_console_output)
        layout.addWidget(test_btn)
        
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self.log_text.clear)
        layout.addWidget(clear_btn)
        
        # Setup logger
        self.setup_logger()
        
        # Timer to simulate periodic console output
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_console_output)
        self.timer.start(2000)  # Every 2 seconds
    
    def setup_logger(self):
        """Setup logger to capture console output"""
        try:
            # Set GUI callback for log messages
            set_global_gui_callback(self.log_message)
            
            # Get logger and connect signal
            logger = get_global_logger()
            logger.log_message_signal.connect(self.log_message)
            
            # Start capturing console output
            logger.start_capture()
            
            self.log_message("✅ Logger inicializado - Capturando logs de consola")
        except Exception as e:
            print(f"Error setting up logger: {e}")
    
    def log_message(self, message: str):
        """Add message to log"""
        try:
            self.log_text.append(message)
            
            # Auto-scroll to bottom
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.End)
            self.log_text.setTextCursor(cursor)
            
            # Force GUI update
            QApplication.processEvents()
        except Exception as e:
            print(f"Error in log_message: {e}")
    
    def test_console_output(self):
        """Test various console output types"""
        print("🧪 Testing console output capture...")
        print("✅ This should appear in the GUI log")
        print("⚠️ Warning message test")
        print("❌ Error message test")
        print("📊 Progress: 50%")
        print("🎬 Processing video clip...")
        print("✅ Clip created successfully")
        
        # Test different types of output
        import random
        print(f"🎲 Random number: {random.randint(1, 100)}")
        
        # Test with special characters
        print("🔍 Searching for files...")
        print("📁 Found 15 video files")
        print("⚙️ Configuring settings...")
    
    def simulate_console_output(self):
        """Simulate periodic console output"""
        import random
        messages = [
            "🔄 Processing...",
            "📊 Progress update",
            "✅ Task completed",
            "⚠️ Warning message",
            "📁 File operation",
            "🎬 Video processing",
            "⚙️ System update"
        ]
        
        message = random.choice(messages)
        print(f"{message} - {time.strftime('%H:%M:%S')}")


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Create test window
    window = TestLogWindow()
    window.show()
    
    print("🚀 Test application started")
    print("📝 Console output will be captured and displayed in the GUI")
    print("🔧 Click 'Test Console Output' to see more logs")
    
    # Run the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 