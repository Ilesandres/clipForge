# Guía de Instalación - ClipForge

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)
1. **Descarga** el proyecto ClipForge
2. **Haz doble clic** en `install.bat`
3. **Espera** a que se instalen las dependencias
4. **Ejecuta** la aplicación con `run.bat` o `python main.py`

### Opción 2: Instalación Manual
1. **Abre** PowerShell o CMD
2. **Navega** al directorio de ClipForge
3. **Ejecuta**: `pip install -r requirements.txt`
4. **Ejecuta**: `python main.py`

## 📋 Requisitos Previos

### Python 3.7 o Superior
- **Descarga**: https://python.org
- **Instalación**: Marca "Add Python to PATH" durante la instalación
- **Verificación**: Abre CMD y ejecuta `python --version`

### Espacio en Disco
- **Mínimo**: 1 GB libre
- **Recomendado**: 5+ GB para videos grandes

## 🔧 Dependencias

La aplicación requiere las siguientes librerías:

```
PyQt5==5.15.9      # Interfaz gráfica
moviepy==1.0.3     # Procesamiento de video
Pillow==10.0.1     # Manejo de imágenes
pathlib2==2.3.7    # Utilidades de archivos
```

## 🐛 Solución de Problemas

### Error: "No module named 'PyQt5'"
```bash
pip install PyQt5==5.15.9
```

### Error: "No module named 'moviepy'"
```bash
pip install moviepy==1.0.3
```

### Error: "Python no está instalado"
1. Descarga Python desde https://python.org
2. Instala marcando "Add Python to PATH"
3. Reinicia la terminal

### Error: "Permission denied"
Ejecuta PowerShell como Administrador:
```powershell
Set-ExecutionPolicy RemoteSigned
```

### Error: "pip no se reconoce"
1. Reinstala Python marcando "Add Python to PATH"
2. O ejecuta: `python -m pip install -r requirements.txt`

## ✅ Verificación de Instalación

Ejecuta el script de prueba:
```bash
python test_app.py
```

Deberías ver:
```
✓ ConfigManager imported successfully
✓ FileUtils imported successfully
✓ VideoSplitter imported successfully
✓ PyQt5 imported successfully
✓ MainWindow imported successfully
```

## 🎯 Primer Uso

1. **Ejecuta** `python main.py`
2. **Selecciona** videos con "Select Video Files"
3. **Elige** duración de clips (15s, 30s, 60s, etc.)
4. **Configura** carpeta de salida (opcional)
5. **Haz clic** en "Start Processing"

## 📁 Estructura de Carpetas

Después del primer uso, se crearán:

```
Documents/
└── ClipForge/
    ├── config/
    │   └── config.json          # Configuración
    └── clips/                   # Clips procesados
        ├── Video1/
        │   ├── Video1_clip_001_30s.mp4
        │   └── Video1_clip_002_30s.mp4
        └── Video2_20241201_143022/
            └── Video2_clip_001_30s.mp4
```

## 🔄 Actualización

Para actualizar ClipForge:
1. **Descarga** la nueva versión
2. **Reemplaza** los archivos
3. **Ejecuta**: `pip install -r requirements.txt --upgrade`

## 📞 Soporte

Si tienes problemas:
1. **Ejecuta** `python test_app.py` para diagnosticar
2. **Revisa** los logs en la aplicación
3. **Verifica** que tienes Python 3.7+ instalado
4. **Asegúrate** de tener espacio en disco suficiente

---

**¡ClipForge está listo para usar!** 🎬 