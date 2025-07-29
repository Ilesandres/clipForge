# 🚀 Crear Ejecutable - ClipForge

## ✅ PyInstaller Instalado

**Versión**: 6.14.2
**Estado**: ✅ Listo para crear ejecutable

## 🛠️ Opciones para Crear el Ejecutable

### Opción 1: Script Automático (Recomendado)
```bash
# Doble clic en build.bat
# O ejecuta:
build.bat
```

### Opción 2: Script Python
```bash
python build_exe.py
```

### Opción 3: Comando Manual
```bash
pyinstaller --onefile --windowed --name ClipForge --clean --noconfirm --add-data "config;config" --add-data "gui;gui" --add-data "processor;processor" --add-data "utils;utils" main.py
```

## 📁 Archivos que se Crearán

Después del build exitoso:
```
ClipForge/
├── dist/
│   └── ClipForge.exe          # Ejecutable principal
├── build/                     # Archivos temporales
└── ClipForge.spec            # Especificación de build
```

## ⚙️ Características del Ejecutable

- ✅ **Archivo único**: Todo incluido en un .exe
- ✅ **Sin consola**: Interfaz gráfica únicamente
- ✅ **Portable**: Funciona en cualquier PC con Windows
- ✅ **Independiente**: No requiere Python instalado

## 🎯 Para Usar el Ejecutable

### Instalación:
1. **Copia** `dist/ClipForge.exe` a cualquier carpeta
2. **Ejecuta** haciendo doble clic
3. **¡Listo!** No necesita instalación

### Distribución:
- **Comparte** el archivo .exe directamente
- **Funciona** en Windows 10/11 sin dependencias
- **Tamaño**: ~50-100 MB (dependiendo de las librerías)

## 🔧 Opciones de Build

### Build Básico:
```bash
pyinstaller --onefile --windowed main.py
```

### Build Completo (Recomendado):
```bash
pyinstaller --onefile --windowed --name ClipForge --icon=assets/clipforge.ico --clean --noconfirm --add-data "config;config" --add-data "gui;gui" --add-data "processor;processor" --add-data "utils;utils" main.py
```

### Build con Icono Personalizado:
```bash
pyinstaller --onefile --windowed --icon=assets/clipforge.ico --name ClipForge main.py
```

## 🐛 Solución de Problemas

### Error: "PyInstaller not found"
```bash
pip install pyinstaller>=6.10.0
```

### Error: "Module not found"
- Verifica que todas las dependencias estén instaladas
- Ejecuta: `pip install -r requirements.txt`

### Error: "Executable too large"
- Usa `--onefile` para un solo archivo
- Usa `--onedir` para una carpeta con archivos

### Error: "Missing DLL"
- Asegúrate de usar `--add-data` para incluir módulos
- Verifica que FFmpeg esté incluido

## 📊 Comparación de Tamaños

| Opción | Tamaño | Ventajas | Desventajas |
|--------|--------|----------|-------------|
| `--onefile` | ~50-100 MB | Portable, fácil distribución | Inicio más lento |
| `--onedir` | ~100-200 MB | Inicio rápido | Múltiples archivos |

## 🎬 Funcionalidades del Ejecutable

- ✅ **Todas las funciones** de la aplicación original
- ✅ **Configuración persistente** en Documents/ClipForge/
- ✅ **Procesamiento de video** completo
- ✅ **Interfaz gráfica** moderna
- ✅ **Logs y resultados** detallados

## 📞 Soporte

Si el build falla:
1. Verifica que Python 3.13 esté instalado
2. Ejecuta: `pip install -r requirements.txt`
3. Intenta el build manual
4. Revisa los logs de error

---

**¡Tu ejecutable de ClipForge estará listo en minutos!** 🚀✨ 