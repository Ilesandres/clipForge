@echo off
echo ========================================
echo ClipForge - Instalar Dependencias URL
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    pause
    exit /b 1
)

echo Instalando dependencias para procesamiento de URLs...
echo.

REM Install yt-dlp
echo Instalando yt-dlp...
pip install yt-dlp>=2023.12.30
if errorlevel 1 (
    echo ERROR: No se pudo instalar yt-dlp
    pause
    exit /b 1
)

REM Install requests
echo Instalando requests...
pip install requests>=2.31.0
if errorlevel 1 (
    echo ERROR: No se pudo instalar requests
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Dependencias instaladas:
echo - yt-dlp: Para descargar videos de YouTube, Twitch, Kick
echo - requests: Para peticiones HTTP
echo.
echo Ahora puedes usar la funcionalidad de URLs en ClipForge!
echo.
pause 