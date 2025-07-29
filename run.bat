@echo off
echo Iniciando ClipForge...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.7 o superior desde https://python.org
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: No se encuentra main.py
    echo Asegurate de estar en el directorio correcto de ClipForge
    pause
    exit /b 1
)

REM Run the application
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Error al ejecutar ClipForge
    echo Verifica que todas las dependencias esten instaladas
    echo Ejecuta: pip install -r requirements.txt
    pause
) 