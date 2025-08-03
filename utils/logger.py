#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Logger for ClipForge
Redirects console output to GUI log windows
"""

import sys
import io
from datetime import datetime
from typing import Optional, Callable
from PyQt5.QtCore import QObject, pyqtSignal


class GUILogger(QObject):
    """Custom logger that redirects output to GUI"""
    
    # Signal to emit log messages to GUI
    log_message_signal = pyqtSignal(str)
    
    def __init__(self, gui_callback: Optional[Callable] = None):
        """Initialize GUI logger"""
        super().__init__()
        self.gui_callback = gui_callback
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.log_buffer = []
        self.max_buffer_size = 1000  # Keep last 1000 messages
        
    def set_gui_callback(self, callback: Callable):
        """Set GUI callback function"""
        self.gui_callback = callback
        
    def write(self, text: str):
        """Write text to both console and GUI"""
        # Write to original stdout first (with safety check)
        if self.original_stdout is not None:
            try:
                self.original_stdout.write(text)
                self.original_stdout.flush()
            except (AttributeError, OSError):
                # Fallback if stdout is not available
                pass
        
        # Only process non-empty lines
        if text.strip():
            # Add timestamp and format for GUI
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {text.strip()}"
            
            # Add to buffer
            self.log_buffer.append(formatted_message)
            if len(self.log_buffer) > self.max_buffer_size:
                self.log_buffer.pop(0)
            
            # Send to GUI if callback is available
            if self.gui_callback:
                try:
                    self.gui_callback(formatted_message)
                except Exception as e:
                    # Fallback to signal if callback fails
                    self.log_message_signal.emit(formatted_message)
            else:
                # Use signal as fallback
                self.log_message_signal.emit(formatted_message)
    
    def flush(self):
        """Flush the output"""
        if self.original_stdout is not None:
            try:
                self.original_stdout.flush()
            except (AttributeError, OSError):
                pass
    
    def get_log_buffer(self) -> list:
        """Get current log buffer"""
        return self.log_buffer.copy()
    
    def clear_buffer(self):
        """Clear log buffer"""
        self.log_buffer.clear()
    
    def start_capture(self):
        """Start capturing console output"""
        sys.stdout = self
        sys.stderr = self
    
    def stop_capture(self):
        """Stop capturing console output"""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr


class ConsoleCapture:
    """Context manager for capturing console output"""
    
    def __init__(self, gui_callback: Optional[Callable] = None):
        """Initialize console capture"""
        self.logger = GUILogger(gui_callback)
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
    
    def __enter__(self):
        """Enter context - start capture"""
        self.logger.start_capture()
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - stop capture"""
        self.logger.stop_capture()


# Global logger instance
_global_logger = None


def get_global_logger() -> GUILogger:
    """Get global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = GUILogger()
    return _global_logger


def set_global_gui_callback(callback: Callable):
    """Set global GUI callback"""
    logger = get_global_logger()
    logger.set_gui_callback(callback)


def start_global_capture():
    """Start global console capture"""
    logger = get_global_logger()
    logger.start_capture()


def stop_global_capture():
    """Stop global console capture"""
    logger = get_global_logger()
    logger.stop_capture()


def log_to_gui(message: str):
    """Log message to GUI"""
    logger = get_global_logger()
    logger.write(message + "\n") 