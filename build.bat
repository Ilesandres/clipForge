@echo off
echo ========================================
echo ClipForge - Build Executable
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller>=6.10.0
)

echo Building ClipForge executable...
echo This may take several minutes...
echo.

REM Build the executable
pyinstaller --onefile --windowed --name ClipForge --icon=assets/clipforge.ico --clean --noconfirm --add-data "config;config" --add-data "gui;gui" --add-data "processor;processor" --add-data "utils;utils" main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable created: dist\ClipForge.exe
echo.
echo To run ClipForge:
echo 1. Double-click dist\ClipForge.exe
echo 2. Or copy it to any location
echo.
pause 