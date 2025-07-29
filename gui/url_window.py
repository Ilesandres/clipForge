#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL Processing Window for ClipForge
Handles video processing from URLs
"""

import sys
from pathlib import Path
from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QProgressBar, QTextEdit,
    QGroupBox, QMessageBox, QFrame, QSplitter, QListWidget,
    QListWidgetItem, QApplication, QStyle
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon

from processor.url_clip_processor import URLClipProcessor
from utils.file_utils import FileUtils


class URLProcessingThread(QThread):
    """Thread for URL video processing"""
    
    progress_updated = pyqtSignal(int)
    processing_finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    preview_ready = pyqtSignal(dict)
    
    def __init__(self, url: str, output_path: Path, clip_duration: int, mode: str = 'process'):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.clip_duration = clip_duration
        self.mode = mode  # 'preview' or 'process'
        self.processor = URLClipProcessor(self.progress_updated.emit)
    
    def run(self):
        """Run URL processing"""
        try:
            if self.mode == 'preview':
                # Get video preview
                preview = self.processor.get_video_preview(self.url)
                self.preview_ready.emit(preview)
            else:
                # Process video
                result = self.processor.process_url_video(
                    self.url, 
                    self.output_path, 
                    self.clip_duration
                )
                self.processing_finished.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))


class URLWindow(QWidget):
    """Window for URL video processing"""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.processing_thread = None
        self.current_url = ""
        
        self.init_ui()
        self.setup_connections()
        self.load_config()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("ClipForge - Procesar desde URL")
        self.setMinimumSize(900, 700)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("🌐 Procesar Videos desde URL")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # URL input group
        url_group = QGroupBox("📋 Información del Video")
        url_layout = QGridLayout(url_group)
        
        # URL input
        url_layout.addWidget(QLabel("URL del Video:"), 0, 0)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        url_layout.addWidget(self.url_input, 0, 1)
        
        # Preview button
        self.preview_btn = QPushButton("🔍 Obtener Información")
        self.preview_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        url_layout.addWidget(self.preview_btn, 0, 2)
        
        main_layout.addWidget(url_group)
        
        # Video info group
        self.video_info_group = QGroupBox("📺 Información del Video")
        self.video_info_layout = QGridLayout(self.video_info_group)
        
        # Video info labels
        self.platform_label = QLabel("Plataforma: -")
        self.title_label = QLabel("Título: -")
        self.duration_label = QLabel("Duración: -")
        self.uploader_label = QLabel("Creador: -")
        self.views_label = QLabel("Vistas: -")
        
        self.video_info_layout.addWidget(self.platform_label, 0, 0)
        self.video_info_layout.addWidget(self.title_label, 0, 1)
        self.video_info_layout.addWidget(self.duration_label, 1, 0)
        self.video_info_layout.addWidget(self.uploader_label, 1, 1)
        self.video_info_layout.addWidget(self.views_label, 2, 0)
        
        # Initially hide video info
        self.video_info_group.setVisible(False)
        main_layout.addWidget(self.video_info_group)
        
        # Processing settings group
        settings_group = QGroupBox("⚙️ Configuración de Procesamiento")
        settings_layout = QGridLayout(settings_group)
        
        # Clip duration
        settings_layout.addWidget(QLabel("Duración de Clips:"), 0, 0)
        self.duration_combo = QComboBox()
        self.duration_combo.addItems([f"{d}s" for d in self.config_manager.get_available_durations()])
        settings_layout.addWidget(self.duration_combo, 0, 1)
        
        # Output path
        settings_layout.addWidget(QLabel("Carpeta de Salida:"), 1, 0)
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setReadOnly(True)
        settings_layout.addWidget(self.output_path_edit, 1, 1)
        
        self.browse_output_btn = QPushButton("📁 Explorar")
        settings_layout.addWidget(self.browse_output_btn, 1, 2)
        
        # Estimated time
        self.estimated_time_label = QLabel("Tiempo estimado: -")
        settings_layout.addWidget(self.estimated_time_label, 2, 0, 1, 2)
        
        main_layout.addWidget(settings_group)
        
        # Processing group
        processing_group = QGroupBox("🔄 Procesamiento")
        processing_layout = QVBoxLayout(processing_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        processing_layout.addWidget(self.progress_bar)
        
        # Process button
        self.process_btn = QPushButton("🚀 Iniciar Procesamiento")
        self.process_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.process_btn.setEnabled(False)
        processing_layout.addWidget(self.process_btn)
        
        main_layout.addWidget(processing_group)
        
        # Log and results
        splitter = QSplitter(Qt.Horizontal)
        
        # Log group
        log_group = QGroupBox("📝 Log de Procesamiento")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(150)
        self.log_text.setMaximumHeight(200)
        self.log_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.log_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        log_layout.addWidget(self.log_text)
        
        # Clear log button
        clear_log_btn = QPushButton("🗑️ Limpiar Log")
        clear_log_btn.clicked.connect(self.log_text.clear)
        log_layout.addWidget(clear_log_btn)
        
        splitter.addWidget(log_group)
        
        # Results group
        results_group = QGroupBox("📊 Resultados")
        results_layout = QVBoxLayout(results_group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(150)
        self.results_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.results_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        results_layout.addWidget(self.results_text)
        
        splitter.addWidget(results_group)
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_label = QLabel("Listo para procesar videos desde URL")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.preview_btn.clicked.connect(self.preview_video)
        self.browse_output_btn.clicked.connect(self.browse_output_path)
        self.process_btn.clicked.connect(self.start_processing)
        self.duration_combo.currentTextChanged.connect(self.update_estimated_time)
        self.url_input.textChanged.connect(self.on_url_changed)
    
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
    
    def on_url_changed(self):
        """Handle URL input changes"""
        url = self.url_input.text().strip()
        if url:
            self.preview_btn.setEnabled(True)
        else:
            self.preview_btn.setEnabled(False)
            self.video_info_group.setVisible(False)
            self.process_btn.setEnabled(False)
    
    def preview_video(self):
        """Preview video information"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Por favor ingresa una URL válida.")
            return
        
        self.log_message(f"Obteniendo información de: {url}")
        self.preview_btn.setEnabled(False)
        self.status_label.setText("Obteniendo información del video...")
        
        # Start preview thread
        self.processing_thread = URLProcessingThread(
            url, 
            Path(self.output_path_edit.text()), 
            30,  # Default duration for preview
            'preview'
        )
        self.processing_thread.preview_ready.connect(self.show_video_preview)
        self.processing_thread.error_occurred.connect(self.preview_error)
        self.processing_thread.start()
    
    def show_video_preview(self, preview: dict):
        """Show video preview information"""
        if not preview['valid']:
            QMessageBox.warning(self, "Error", preview['error'])
            self.preview_btn.setEnabled(True)
            self.status_label.setText("Error al obtener información del video")
            return
        
        # Update video info
        self.platform_label.setText(f"Plataforma: {preview['platform_icon']} {preview['platform']}")
        self.title_label.setText(f"Título: {preview['title']}")
        self.duration_label.setText(f"Duración: {preview['duration_formatted']}")
        self.uploader_label.setText(f"Creador: {preview['uploader']}")
        self.views_label.setText(f"Vistas: {preview['view_count']:,}")
        
        # Show video info group
        self.video_info_group.setVisible(True)
        
        # Update estimated time
        self.update_estimated_time()
        
        # Enable process button
        self.process_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        
        self.log_message(f"✅ Información obtenida: {preview['title']}")
        self.status_label.setText("Video listo para procesar")
    
    def preview_error(self, error: str):
        """Handle preview error"""
        QMessageBox.critical(self, "Error", f"Error al obtener información: {error}")
        self.preview_btn.setEnabled(True)
        self.status_label.setText("Error al obtener información del video")
    
    def update_estimated_time(self):
        """Update estimated processing time"""
        if hasattr(self, 'current_preview') and self.current_preview.get('valid'):
            duration = self.current_preview['duration']
            clip_duration = int(self.duration_combo.currentText().replace('s', ''))
            
            processor = URLClipProcessor()
            estimated_time = processor.estimate_processing_time(duration, clip_duration)
            self.estimated_time_label.setText(f"Tiempo estimado: {estimated_time}")
    
    def browse_output_path(self):
        """Browse for output directory"""
        from PyQt5.QtWidgets import QFileDialog
        
        current_path = self.output_path_edit.text()
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar Carpeta de Salida",
            current_path
        )
        
        if directory:
            self.output_path_edit.setText(directory)
            self.config_manager.set_output_path(directory)
            self.log_message(f"Carpeta de salida cambiada a: {directory}")
    
    def start_processing(self):
        """Start URL video processing"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Por favor ingresa una URL válida.")
            return
        
        output_path = Path(self.output_path_edit.text())
        if not output_path.exists():
            try:
                output_path.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                QMessageBox.critical(self, "Error", f"No se pudo crear la carpeta de salida: {e}")
                return
        
        # Get duration
        duration_text = self.duration_combo.currentText()
        duration = int(duration_text.replace('s', ''))
        
        # Save duration to config
        self.config_manager.set_last_duration(duration)
        
        # Disable controls
        self.process_btn.setEnabled(False)
        self.preview_btn.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        QApplication.processEvents()  # Force initial GUI update
        
        # Start processing thread
        self.processing_thread = URLProcessingThread(
            url, 
            output_path, 
            duration,
            'process'
        )
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.processing_finished.connect(self.processing_finished)
        self.processing_thread.error_occurred.connect(self.processing_error)
        self.processing_thread.start()
        
        self.log_message(f"Iniciando procesamiento: {url}")
        self.status_label.setText("Procesando video desde URL...")
    
    def update_progress(self, value: int):
        """Update progress bar"""
        try:
            if isinstance(value, (int, float)):
                progress_value = int(value)
                progress_value = max(0, min(100, progress_value))
                self.progress_bar.setValue(progress_value)
                self.status_label.setText(f"Procesando... {progress_value}%")
                QApplication.processEvents()  # Force GUI update
                print(f"GUI Progress updated: {progress_value}%")
            else:
                print(f"Invalid progress value: {value} (type: {type(value)})")
        except Exception as e:
            print(f"Error updating progress: {e}")
            self.progress_bar.setValue(0)
            self.status_label.setText("Procesando...")
    
    def processing_finished(self, result: dict):
        """Handle processing completion"""
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        
        if result.get('success', False):
            self.log_message("✅ Procesamiento completado exitosamente!")
            self.show_processing_results(result)
        else:
            error_msg = result.get('error', 'Error desconocido')
            self.log_message(f"❌ Procesamiento falló: {error_msg}")
            QMessageBox.critical(self, "Error", f"Error de procesamiento: {error_msg}")
        
        self.status_label.setText("Listo")
    
    def processing_error(self, error: str):
        """Handle processing error"""
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        
        self.log_message(f"❌ Error: {error}")
        QMessageBox.critical(self, "Error", f"Error de procesamiento: {error}")
        self.status_label.setText("Error - Listo")
    
    def show_processing_results(self, result: dict):
        """Show processing results"""
        results_text = f"Resultados del Procesamiento:\n\n"
        results_text += f"URL: {result.get('url', 'N/A')}\n"
        results_text += f"Plataforma: {result.get('platform', 'N/A')}\n"
        results_text += f"Título: {result.get('video_title', 'N/A')}\n"
        results_text += f"Carpeta de Salida: {result.get('output_folder', 'N/A')}\n"
        results_text += f"Clips Creados: {result.get('clips_created', 0)}/{result.get('total_clips_attempted', 0)}\n"
        results_text += f"Duración del Video: {FileUtils.format_duration(result.get('input_duration', 0))}\n"
        results_text += f"Duración de Clips: {result.get('clip_duration', 0)}s\n"
        results_text += f"Tamaño Total: {FileUtils.format_file_size(result.get('output_size', 0))}\n"
        results_text += f"Creador: {result.get('uploader', 'N/A')}\n"
        results_text += f"Vistas: {result.get('view_count', 0):,}\n"
        
        self.results_text.setText(results_text)
        
        # Auto-scroll to top
        cursor = self.results_text.textCursor()
        cursor.movePosition(cursor.Start)
        self.results_text.setTextCursor(cursor)
    
    def log_message(self, message: str):
        """Add message to log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
        # Auto-scroll to bottom
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.End)
        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible() 