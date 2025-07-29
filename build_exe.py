#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for ClipForge executable
Creates a standalone .exe file using PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    """Build ClipForge executable using PyInstaller"""
    
    print("=" * 60)
    print("ClipForge - Build Executable")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=6.10.0"])
    
    # Define build parameters
    main_script = "main.py"
    app_name = "ClipForge"
    icon_path = "assets/clipforge.ico"  # Icon for the application
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name", app_name,             # Executable name
        "--clean",                      # Clean cache
        "--noconfirm",                  # Overwrite without asking
        "--add-data", "config;config",  # Include config directory
        "--add-data", "gui;gui",        # Include gui directory
        "--add-data", "processor;processor",  # Include processor directory
        "--add-data", "utils;utils",    # Include utils directory
        main_script
    ]
    
    # Add icon if available
    if icon_path and os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
    
    print(f"\nBuilding executable: {app_name}.exe")
    print(f"Command: {' '.join(cmd)}")
    print("\nThis may take several minutes...")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("\n" + "=" * 60)
        print("✅ Build completed successfully!")
        print("=" * 60)
        
        # Check if executable was created
        exe_path = Path("dist") / f"{app_name}.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"Executable created: {exe_path}")
            print(f"Size: {size_mb:.1f} MB")
            print(f"\nYou can now run: {exe_path}")
        else:
            print("❌ Executable not found in dist/ directory")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error code {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True

def create_installer_script():
    """Create a simple installer script"""
    
    installer_content = '''@echo off
echo ========================================
echo ClipForge - Instalador
echo ========================================
echo.

REM Check if executable exists
if not exist "dist\\ClipForge.exe" (
    echo ERROR: ClipForge.exe no encontrado
    echo Ejecuta primero: python build_exe.py
    pause
    exit /b 1
)

REM Create desktop shortcut
echo Creando acceso directo en el escritorio...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\ClipForge.lnk'); $Shortcut.TargetPath = '%~dp0dist\\ClipForge.exe'; $Shortcut.Save()"

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo ClipForge se ha instalado correctamente.
echo Puedes ejecutarlo desde el escritorio o desde:
echo %~dp0dist\\ClipForge.exe
echo.
pause
'''
    
    with open("installer.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("✓ Installer script created: installer.bat")

def main():
    """Main build process"""
    
    print("ClipForge - Build Process")
    print("This will create a standalone executable.")
    print()
    
    # Build executable
    if build_executable():
        # Create installer script
        create_installer_script()
        
        print("\n" + "=" * 60)
        print("🎉 Build process completed!")
        print("=" * 60)
        print("\nFiles created:")
        print("- dist/ClipForge.exe (executable)")
        print("- installer.bat (installer script)")
        print("\nTo install:")
        print("1. Run installer.bat")
        print("2. Or copy dist/ClipForge.exe to any location")
        print("\nTo run:")
        print("Double-click ClipForge.exe")
        
    else:
        print("\n❌ Build process failed!")
        print("Check the error messages above.")

if __name__ == "__main__":
    main() 