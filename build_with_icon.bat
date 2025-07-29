@echo off
echo ========================================
echo ClipForge - Build with Icon
echo ========================================
echo.

REM Check if icon exists
if not exist "assets\clipforge.ico" (
    echo ERROR: Icon file not found: assets\clipforge.ico
    echo Please ensure the icon file exists.
    pause
    exit /b 1
)

echo Icon found: assets\clipforge.ico
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller>=6.10.0
)

echo Building ClipForge executable with icon...
echo This may take several minutes...
echo.

REM Build the executable with icon
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
echo Icon included: assets\clipforge.ico
echo.
echo To run ClipForge:
echo 1. Double-click dist\ClipForge.exe
echo 2. Or copy it to any location
echo.
echo The executable will have the ClipForge icon!
echo.
pause 