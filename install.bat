@echo off
echo ========================================
echo ClipForge - Video Clipping Tool
echo ========================================
echo.
echo Instalando dependencias...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.7 o superior desde https://python.org
    pause
    exit /b 1
)

echo Python encontrado. Instalando dependencias...
echo.

REM Install dependencies
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Error al instalar las dependencias
    echo Intenta ejecutar: pip install -r requirements.txt manualmente
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalacion completada exitosamente!
echo ========================================
echo.
echo Para ejecutar ClipForge:
echo   python main.py
echo.
echo O simplemente haz doble clic en main.py
echo.
pause 