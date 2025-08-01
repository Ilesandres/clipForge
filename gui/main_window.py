#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window for ClipForge
Main GUI interface for the video processing application
"""

import sys
import os
from pathlib import Path
from typing import List, Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QLineEdit, QProgressBar,
    QTextEdit, QFileDialog, QMessageBox, QGroupBox, QSpinBox,
    QFrame, QSplitter, QListWidget, QListWidgetItem, QCheckBox,
    QApplication, QStyle, QSizePolicy, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor

from config.config_manager import ConfigManager
from processor.video_splitter import VideoSplitter
from utils.file_utils import FileUtils
from .url_window import URLWindow


class ProcessingThread(QThread):
    """Thread for video processing to avoid GUI freezing"""
    
    progress_updated = pyqtSignal(int)
    processing_finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, video_path: str, output_path: Path, clip_duration: int):
        super().__init__()
        self.video_path = video_path
        self.output_path = output_path
        self.clip_duration = clip_duration
        self.splitter = VideoSplitter(self._progress_callback)
    
    def _progress_callback(self, value):
        """Callback for progress updates"""
        try:
            # Ensure we emit a valid integer value
            if isinstance(value, (int, float)):
                progress_value = int(value)
                progress_value = max(0, min(100, progress_value))
                print(f"Thread progress callback: {progress_value}%")
                self.progress_updated.emit(progress_value)
            else:
                print(f"Invalid progress value in callback: {value}")
        except Exception as e:
            print(f"Error in progress callback: {e}")
    
    def run(self):
        """Run video processing"""
        try:
            print("Starting video processing thread...")
            result = self.splitter.process_video(
                self.video_path, 
                self.output_path, 
                self.clip_duration
            )
            print("Video processing completed, emitting result...")
            self.processing_finished.emit(result)
        except Exception as e:
            print(f"Error in processing thread: {e}")
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.processing_thread = None
        self.video_files = []
        
        self.init_ui()
        self.load_config()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("ClipForge - Video Clipping Tool")
        self.setMinimumSize(900, 600)
        
        # Set window icon with improved configuration
        icon_path = Path(__file__).parent.parent / "assets" / "clipforge_multi.ico"
        if not icon_path.exists():
            # Fallback to other icons
            icon_path = Path(__file__).parent.parent / "assets" / "clipforge-16x16.ico"
            if not icon_path.exists():
                icon_path = Path(__file__).parent.parent / "assets" / "clipforge.ico"
        
        if icon_path.exists():
            try:
                # Create QIcon object
                icon = QIcon(str(icon_path))
                
                # Check if icon is valid
                if not icon.isNull():
                    # Set window icon
                    self.setWindowIcon(icon)
                    print(f"✅ Main window icon set successfully from: {icon_path}")
                else:
                    print(f"⚠️ Warning: Icon file exists but is invalid: {icon_path}")
            except Exception as e:
                print(f"⚠️ Warning: Error setting main window icon: {e}")
        else:
            print(f"⚠️ Warning: Icon file not found at {icon_path}")
        
        # Set window icon and style
        self.setStyleSheet(self.get_application_style())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Local files tab
        local_tab = self.create_local_tab()
        self.tab_widget.addTab(local_tab, "📁 Archivos Locales")
        
        # URL tab
        self.url_window = URLWindow(self.config_manager)
        self.tab_widget.addTab(self.url_window, "🌐 Desde URL")
        
        main_layout.addWidget(self.tab_widget)
        
        # Create status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Listo para procesar videos")
    
    def create_local_tab(self) -> QWidget:
        """Create the local files processing tab"""
        tab_widget = QWidget()
        layout = QHBoxLayout(tab_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Left panel - Controls
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Log and Progress
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 500])
        
        return tab_widget
    
    def create_left_panel(self) -> QWidget:
        """Create left control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # File selection group
        file_group = QGroupBox("Video Files")
        file_layout = QVBoxLayout(file_group)
        
        # File selection buttons
        file_buttons_layout = QHBoxLayout()
        self.select_files_btn = QPushButton("Select Video Files")
        self.select_files_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogStart))
        self.clear_files_btn = QPushButton("Clear All")
        self.clear_files_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        
        file_buttons_layout.addWidget(self.select_files_btn)
        file_buttons_layout.addWidget(self.clear_files_btn)
        file_layout.addLayout(file_buttons_layout)
        
        # File list
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(200)
        file_layout.addWidget(self.file_list)
        
        layout.addWidget(file_group)
        
        # Settings group
        settings_group = QGroupBox("Processing Settings")
        settings_layout = QGridLayout(settings_group)
        
        # Clip duration
        settings_layout.addWidget(QLabel("Clip Duration:"), 0, 0)
        self.duration_combo = QComboBox()
        self.duration_combo.addItems([f"{d}s" for d in self.config_manager.get_available_durations()])
        settings_layout.addWidget(self.duration_combo, 0, 1)
        
        # Output path
        settings_layout.addWidget(QLabel("Output Path:"), 1, 0)
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setReadOnly(True)
        settings_layout.addWidget(self.output_path_edit, 1, 1)
        
        self.browse_output_btn = QPushButton("Browse")
        settings_layout.addWidget(self.browse_output_btn, 1, 2)
        
        # Video info
        self.video_info_label = QLabel("No video selected")
        self.video_info_label.setWordWrap(True)
        settings_layout.addWidget(self.video_info_label, 2, 0, 1, 3)
        
        layout.addWidget(settings_group)
        
        # Processing group
        processing_group = QGroupBox("Processing")
        processing_layout = QVBoxLayout(processing_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        processing_layout.addWidget(self.progress_bar)
        
        # Process button
        self.process_btn = QPushButton("Start Processing")
        self.process_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.process_btn.setEnabled(False)
        processing_layout.addWidget(self.process_btn)
        
        layout.addWidget(processing_group)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self) -> QWidget:
        """Create right panel for logs and results"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Log group
        log_group = QGroupBox("Processing Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(300)
        log_layout.addWidget(self.log_text)
        
        # Clear log button
        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(self.log_text.clear)
        log_layout.addWidget(clear_log_btn)
        
        layout.addWidget(log_group)
        
        # Results group
        results_group = QGroupBox("Processing Results")
        results_layout = QVBoxLayout(results_group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        
        layout.addWidget(results_group)
        
        return panel
    
    def setup_connections(self):
        """Setup signal connections"""
        self.select_files_btn.clicked.connect(self.select_video_files)
        self.clear_files_btn.clicked.connect(self.clear_video_files)
        self.browse_output_btn.clicked.connect(self.browse_output_path)
        self.process_btn.clicked.connect(self.start_processing)
        self.file_list.itemSelectionChanged.connect(self.update_video_info)
        self.duration_combo.currentTextChanged.connect(self.on_duration_changed)
    
    def load_config(self):
        """Load configuration settings"""
        # Load output path
        output_path = self.config_manager.get_output_path()
        self.output_path_edit.setText(output_path)
        
        # Load last duration
        last_duration = self.config_manager.get_last_duration()
        duration_text = f"{last_duration}s"
        index = self.duration_combo.findText(duration_text)
        if index >= 0:
            self.duration_combo.setCurrentIndex(index)
        
        # Load window size and position
        window_size = self.config_manager.get_window_size()
        self.resize(window_size['width'], window_size['height'])
        
        window_pos = self.config_manager.get_window_position()
        self.move(window_pos['x'], window_pos['y'])
    
    def select_video_files(self):
        """Open file dialog to select video files"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v *.3gp *.ogv *.ts *.mts);;All Files (*)"
        )
        
        if files:
            # Filter only video files
            video_files = [f for f in files if FileUtils.is_video_file(f)]
            
            if video_files:
                self.video_files.extend(video_files)
                self.update_file_list()
                self.process_btn.setEnabled(True)
                self.log_message(f"Added {len(video_files)} video file(s)")
            else:
                QMessageBox.warning(self, "Warning", "No valid video files selected.")
    
    def clear_video_files(self):
        """Clear all selected video files"""
        self.video_files.clear()
        self.file_list.clear()
        self.process_btn.setEnabled(False)
        self.video_info_label.setText("No video selected")
        self.log_message("Cleared all video files")
    
    def update_file_list(self):
        """Update the file list display"""
        self.file_list.clear()
        for file_path in self.video_files:
            filename = Path(file_path).name
            item = QListWidgetItem(filename)
            item.setToolTip(file_path)
            self.file_list.addItem(item)
    
    def browse_output_path(self):
        """Browse for output directory"""
        current_path = self.output_path_edit.text()
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            current_path
        )
        
        if directory:
            self.output_path_edit.setText(directory)
            self.config_manager.set_output_path(directory)
            self.log_message(f"Output path changed to: {directory}")
    
    def update_video_info(self):
        """Update video information display"""
        current_item = self.file_list.currentItem()
        if current_item:
            index = self.file_list.row(current_item)
            if 0 <= index < len(self.video_files):
                video_path = self.video_files[index]
                self.show_video_info(video_path)
    
    def show_video_info(self, video_path: str):
        """Show information about selected video"""
        video_info = FileUtils.get_video_info(video_path)
        if video_info:
            duration_str = FileUtils.format_duration(video_info['duration'])
            size_str = FileUtils.format_file_size(video_info['file_size'])
            resolution = f"{video_info['size'][0]}x{video_info['size'][1]}"
            
            info_text = f"Duration: {duration_str}\n"
            info_text += f"Size: {size_str}\n"
            info_text += f"Resolution: {resolution}\n"
            info_text += f"FPS: {video_info['fps']:.1f}"
            
            self.video_info_label.setText(info_text)
        else:
            self.video_info_label.setText("Could not read video information")
    
    def on_duration_changed(self, duration_text: str):
        """Handle duration selection change"""
        try:
            duration = int(duration_text.replace('s', ''))
            self.config_manager.set_last_duration(duration)
        except ValueError:
            pass
    
    def start_processing(self):
        """Start video processing"""
        if not self.video_files:
            QMessageBox.warning(self, "Warning", "No video files selected.")
            return
        
        output_path = Path(self.output_path_edit.text())
        if not output_path.exists():
            try:
                output_path.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Could not create output directory: {e}")
                return
        
        # Get duration
        duration_text = self.duration_combo.currentText()
        duration = int(duration_text.replace('s', ''))
        
        # Disable controls
        self.process_btn.setEnabled(False)
        self.select_files_btn.setEnabled(False)
        self.clear_files_btn.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_bar.showMessage("Starting processing...")
        
        # Force initial GUI update
        QApplication.processEvents()
        
        # Start processing thread
        self.processing_thread = ProcessingThread(
            self.video_files[0],  # Process first file for now
            output_path,
            duration
        )
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.processing_finished.connect(self.processing_finished)
        self.processing_thread.error_occurred.connect(self.processing_error)
        self.processing_thread.start()
        
        self.log_message(f"Started processing: {Path(self.video_files[0]).name}")
    
    def update_progress(self, value: int):
        """Update progress bar"""
        try:
            # Ensure value is valid
            if isinstance(value, (int, float)):
                progress_value = int(value)
                progress_value = max(0, min(100, progress_value))  # Clamp between 0 and 100
                
                # Update progress bar
                self.progress_bar.setValue(progress_value)
                
                # Update status bar
                self.status_bar.showMessage(f"Processing... {progress_value}%")
                
                # Force GUI update
                QApplication.processEvents()
                
                print(f"GUI Progress updated: {progress_value}%")
            else:
                print(f"Invalid progress value: {value} (type: {type(value)})")
        except Exception as e:
            print(f"Error updating progress: {e}")
            # Set a safe default
            self.progress_bar.setValue(0)
            self.status_bar.showMessage("Processing...")
    
    def processing_finished(self, result: dict):
        """Handle processing completion"""
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.select_files_btn.setEnabled(True)
        self.clear_files_btn.setEnabled(True)
        
        if result['success']:
            self.log_message("Processing completed successfully!")
            self.show_processing_results(result)
        else:
            self.log_message(f"Processing failed: {result['error']}")
            QMessageBox.critical(self, "Error", f"Processing failed: {result['error']}")
        
        self.status_bar.showMessage("Ready")
    
    def processing_error(self, error: str):
        """Handle processing error"""
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.select_files_btn.setEnabled(True)
        self.clear_files_btn.setEnabled(True)
        
        # Log the error
        self.log_message(f"Error: {error}")
        
        # Provide more helpful error messages
        if "'NoneType' object has no attribute 'stdout'" in error:
            error_msg = "Error de procesamiento de video. Esto puede deberse a:\n\n" \
                       "1. El archivo de video está corrupto o no es compatible\n" \
                       "2. Problema con FFmpeg (intente reiniciar la aplicación)\n" \
                       "3. El video es muy largo o complejo\n\n" \
                       "Error técnico: " + error
        elif "could not be found" in error:
            error_msg = "No se pudo encontrar el archivo de video.\n\n" \
                       "Asegúrese de que el archivo existe y no está siendo usado por otra aplicación."
        else:
            error_msg = f"Error de procesamiento: {error}\n\n" \
                       "Intente con un video diferente o reinicie la aplicación."
        
        QMessageBox.critical(self, "Error de Procesamiento", error_msg)
        self.status_bar.showMessage("Error - Listo")
    
    def show_processing_results(self, result: dict):
        """Show processing results"""
        results_text = f"Processing Results:\n\n"
        results_text += f"Input File: {Path(result['input_file']).name}\n"
        results_text += f"Output Folder: {result['output_folder']}\n"
        results_text += f"Clips Created: {result['clips_count']}\n"
        results_text += f"Input Duration: {FileUtils.format_duration(result['input_duration'])}\n"
        results_text += f"Clip Duration: {result['clip_duration']}s\n"
        results_text += f"Input Size: {FileUtils.format_file_size(result['input_size'])}\n"
        results_text += f"Output Size: {FileUtils.format_file_size(result['output_size'])}\n"
        
        self.results_text.setText(results_text)
    
    def log_message(self, message: str):
        """Add message to log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def get_application_style(self) -> str:
        """Get application stylesheet"""
        return """
        QMainWindow {
            background-color: #f0f0f0;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QPushButton {
            background-color: #4a90e2;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #357abd;
        }
        
        QPushButton:pressed {
            background-color: #2d5986;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        
        QProgressBar {
            border: 2px solid #cccccc;
            border-radius: 5px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #4a90e2;
            border-radius: 3px;
        }
        
        QTextEdit {
            border: 1px solid #cccccc;
            border-radius: 3px;
            background-color: white;
        }
        
        QListWidget {
            border: 1px solid #cccccc;
            border-radius: 3px;
            background-color: white;
        }
        
        QLineEdit {
            border: 1px solid #cccccc;
            border-radius: 3px;
            padding: 5px;
            background-color: white;
        }
        
        QComboBox {
            border: 1px solid #cccccc;
            border-radius: 3px;
            padding: 5px;
            background-color: white;
        }
        """
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Save window size and position
        self.config_manager.set_window_size(self.width(), self.height())
        self.config_manager.set_window_position(self.x(), self.y())
        
        # Cancel processing if running
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.terminate()
            self.processing_thread.wait()
        
        event.accept() 