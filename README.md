# ClipForge - Video Clipping Tool

ClipForge es una aplicación de escritorio para Windows que permite procesar videos largos y dividirlos en clips de duración personalizable. La aplicación está desarrollada en Python con una interfaz gráfica moderna usando PyQt5.

## 🚀 Características

- **Interfaz de escritorio moderna**: GUI intuitiva y fácil de usar
- **Procesamiento de videos largos**: Soporte para videos de cualquier duración
- **Duración personalizable**: Opciones de 15, 20, 30, 45, 60, 90 y 120 segundos
- **Configuración persistente**: Guarda automáticamente las preferencias del usuario
- **Organización automática**: Crea carpetas por video con nombres únicos
- **Múltiples formatos**: Soporta MP4, AVI, MOV, MKV, WMV, FLV, WebM y más
- **Procesamiento en segundo plano**: No bloquea la interfaz durante el procesamiento
- **Logs detallados**: Información completa del proceso de división

## 📋 Requisitos

- Windows 10 o superior
- Python 3.7 o superior
- Espacio en disco suficiente para los videos procesados

## 🛠️ Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <repository-url>
cd ClipForge
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python main.py
```

### 4. Aplicacion de escritorio 
[aquí 👌](https://github.com/Ilesandres/clipForge/dist/ClipForge.exe)

## 📁 Estructura del Proyecto

```
ClipForge/
├── main.py                  # Punto de entrada de la aplicación
├── requirements.txt         # Dependencias del proyecto
├── README.md               # Este archivo
├── config/                 # Gestión de configuración
│   ├── __init__.py
│   └── config_manager.py   # Manejo de configuración JSON
├── gui/                    # Interfaz de usuario
│   ├── __init__.py
│   └── main_window.py      # Ventana principal de la aplicación
├── processor/              # Procesamiento de video
│   ├── __init__.py
│   └── video_splitter.py   # Lógica de división de videos
└── utils/                  # Utilidades
    ├── __init__.py
    └── file_utils.py       # Utilidades de archivos y carpetas
```

## 🎯 Uso

### 1. Iniciar la aplicación
- Ejecuta `python main.py`
- La aplicación se abrirá con la configuración guardada anteriormente

### 2. Seleccionar videos
- Haz clic en "Select Video Files" para elegir los videos a procesar
- Los videos aparecerán en la lista de archivos
- Selecciona un video para ver su información (duración, tamaño, resolución)

### 3. Configurar opciones
- **Duración de clips**: Selecciona la duración deseada (15s, 20s, 30s, etc.)
- **Ruta de salida**: Usa la predeterminada o selecciona una carpeta personalizada
- La configuración se guarda automáticamente

### 4. Procesar videos
- Haz clic en "Start Processing" para comenzar
- El progreso se muestra en la barra de progreso
- Los logs aparecen en tiempo real
- Los resultados se muestran al finalizar

## 📂 Organización de Archivos

### Carpeta de configuración
```
Documents/ClipForge/config/
└── config.json             # Configuración de la aplicación
```

### Carpeta de clips
```
Documents/ClipForge/clips/
├── Video1/                 # Carpeta por video
│   ├── Video1_clip_001_30s.mp4
│   ├── Video1_clip_002_30s.mp4
│   └── ...
├── Video2_20241201_143022/ # Si hay nombres duplicados
│   ├── Video2_clip_001_30s.mp4
│   └── ...
└── ...
```

## ⚙️ Configuración

El archivo `config.json` contiene:

```json
{
    "output_path": "C:\\Users\\Usuario\\Documents\\ClipForge\\clips",
    "last_duration": 30,
    "available_durations": [15, 20, 30, 45, 60, 90, 120],
    "window_size": {"width": 800, "height": 600},
    "window_position": {"x": 100, "y": 100},
    "theme": "default",
    "auto_create_folders": true,
    "overwrite_existing": false
}
```

## 🔧 Desarrollo

### Arquitectura
La aplicación sigue el patrón MVC (Model-View-Controller):
- **Model**: `ConfigManager`, `VideoSplitter`, `FileUtils`
- **View**: `MainWindow` (GUI)
- **Controller**: Lógica de conexión entre modelo y vista

### Clases principales
- `ConfigManager`: Gestión de configuración persistente
- `VideoSplitter`: Procesamiento y división de videos
- `FileUtils`: Utilidades para manejo de archivos
- `MainWindow`: Interfaz gráfica principal
- `ProcessingThread`: Procesamiento en segundo plano

### Mejores prácticas implementadas
- **Separación de responsabilidades**: Cada clase tiene una función específica
- **Reutilización de código**: Métodos estáticos en `FileUtils`
- **Manejo de errores**: Try-catch en operaciones críticas
- **Configuración persistente**: JSON con valores por defecto
- **Interfaz responsiva**: Procesamiento en hilos separados

## 🐛 Solución de Problemas

### Error: "No module named 'moviepy'"
```bash
pip install moviepy
```

### Error: "No module named 'PyQt5'"
```bash
pip install PyQt5
```

### Videos no se procesan
- Verifica que el formato sea compatible
- Asegúrate de tener suficiente espacio en disco
- Revisa los logs para errores específicos

### La aplicación no inicia
- Verifica que Python 3.7+ esté instalado
- Instala todas las dependencias: `pip install -r requirements.txt`
- Revisa que no haya conflictos con otras versiones de Python

## 📝 Logs

Los logs muestran:
- Archivos seleccionados
- Progreso del procesamiento
- Errores y advertencias
- Resultados finales

## 🔄 Próximas Mejoras

- [ ] Procesamiento de múltiples videos en lote
- [ ] Previsualización de clips
- [ ] Más opciones de codificación
- [ ] Soporte para más formatos de salida
- [ ] Integración con servicios en la nube
- [ ] Modo oscuro/claro
- [ ] Atajos de teclado

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Si encuentras problemas o tienes sugerencias:
1. Revisa la sección de solución de problemas
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

---

**ClipForge** - Forjando clips de forma precisa, rápida y configurable 🎬 