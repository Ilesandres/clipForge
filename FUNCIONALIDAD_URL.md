# 🌐 Funcionalidad de URLs - ClipForge

## 📋 Descripción

ClipForge ahora incluye la capacidad de procesar videos directamente desde URLs de plataformas populares como YouTube, Twitch y Kick. Esta funcionalidad permite:

- ✅ **Validar URLs** de videos en tiempo real
- ✅ **Obtener información** del video (título, duración, creador, etc.)
- ✅ **Procesar clips** sin descargar el video completo
- ✅ **Soporte multiplataforma** (YouTube, Twitch, Kick)
- ✅ **Interfaz intuitiva** con pestañas separadas

## 🚀 Instalación

### Dependencias Requeridas

Para usar la funcionalidad de URLs, necesitas instalar dependencias adicionales:

```bash
# Instalación automática
install_url_deps.bat

# O instalación manual
pip install yt-dlp>=2023.12.30
pip install requests>=2.31.0
```

### Verificación

Ejecuta el script de prueba para verificar que todo funciona:

```bash
python test_url_functionality.py
```

## 🎯 Plataformas Soportadas

| Plataforma | Estado | Icono | Ejemplo de URL |
|------------|--------|-------|----------------|
| **YouTube** | ✅ Soportado | 📺 | `https://www.youtube.com/watch?v=...` |
| **Twitch** | ✅ Soportado | 🎮 | `https://www.twitch.tv/videos/...` |
| **Kick** | ✅ Soportado | 🥊 | `https://kick.com/video/...` |
| **Otras** | ❌ No soportado | ❓ | Mensaje de error informativo |

## 🖥️ Uso de la Interfaz

### 1. Acceder a la Funcionalidad

1. Abre ClipForge
2. Haz clic en la pestaña **"🌐 Desde URL"**
3. La interfaz se divide en secciones claras

### 2. Procesar un Video

#### Paso 1: Ingresar URL
- Pega la URL del video en el campo correspondiente
- Haz clic en **"🔍 Obtener Información"**
- El sistema validará la URL y mostrará información del video

#### Paso 2: Configurar Procesamiento
- **Duración de Clips**: Selecciona la duración deseada (15s, 30s, 60s, etc.)
- **Carpeta de Salida**: Configura dónde guardar los clips
- **Tiempo Estimado**: Se calcula automáticamente

#### Paso 3: Iniciar Procesamiento
- Haz clic en **"🚀 Iniciar Procesamiento"**
- Observa el progreso en tiempo real
- Los clips se guardan automáticamente

### 3. Información Mostrada

La interfaz muestra información detallada del video:

- 📺 **Plataforma**: YouTube, Twitch, Kick
- 📝 **Título**: Nombre del video
- ⏱️ **Duración**: Tiempo total del video
- 👤 **Creador**: Autor del contenido
- 👁️ **Vistas**: Número de reproducciones
- ⏰ **Tiempo Estimado**: Duración aproximada del procesamiento

## 🔧 Características Técnicas

### Arquitectura

```
URLWindow (GUI)
    ↓
URLClipProcessor (Lógica de procesamiento)
    ↓
URLProcessor (Validación y descarga)
    ↓
yt-dlp (Descarga de videos)
```

### Reutilización de Código

La nueva funcionalidad reutiliza componentes existentes:

- ✅ **ConfigManager**: Configuración persistente
- ✅ **FileUtils**: Utilidades de archivos
- ✅ **VideoSplitter**: Lógica de procesamiento de clips
- ✅ **Estilos y temas**: Consistencia visual

### Procesamiento Optimizado

- 🚀 **Descarga por segmentos**: No descarga el video completo
- 💾 **Archivos temporales**: Limpieza automática
- ⚡ **Procesamiento paralelo**: Múltiples clips simultáneos
- 🔄 **Manejo de errores**: Recuperación robusta

## 📁 Organización de Archivos

Los clips se organizan de la misma manera que los archivos locales:

```
Documents/ClipForge/clips/
├── [Título del Video]/
│   ├── [Título]_clip_001_30s.mp4
│   ├── [Título]_clip_002_30s.mp4
│   └── ...
└── ...
```

## 🛠️ Solución de Problemas

### Error: "Plataforma no soportada"

**Causa**: URL de una plataforma no soportada
**Solución**: 
- Verifica que la URL sea de YouTube, Twitch o Kick
- Espera futuras actualizaciones para más plataformas

### Error: "No se pudo obtener información"

**Causas posibles**:
- URL incorrecta o video privado
- Problemas de conectividad
- Video eliminado o restringido

**Soluciones**:
1. Verifica que la URL sea correcta
2. Asegúrate de que el video sea público
3. Revisa tu conexión a internet
4. Intenta con otro video

### Error: "Dependencias faltantes"

**Solución**:
```bash
# Ejecuta el instalador
install_url_deps.bat

# O instala manualmente
pip install yt-dlp requests
```

### Procesamiento Lento

**Causas**:
- Video muy largo
- Conexión lenta
- Muchos clips a procesar

**Optimizaciones**:
- Usa duraciones de clips más largas
- Procesa videos más cortos
- Verifica tu velocidad de internet

## 🔮 Próximas Mejoras

### Plataformas Adicionales
- [ ] Vimeo
- [ ] Dailymotion
- [ ] Facebook Videos
- [ ] Instagram Reels

### Funcionalidades Avanzadas
- [ ] Descarga de listas de reproducción
- [ ] Procesamiento por lotes de URLs
- [ ] Configuración de calidad de video
- [ ] Extracción de subtítulos

### Optimizaciones
- [ ] Caché de información de videos
- [ ] Descarga en segundo plano
- [ ] Compresión inteligente
- [ ] Procesamiento distribuido

## 📊 Estadísticas de Uso

### Información Recopilada
- ✅ **Ninguna**: No se recopila información personal
- ✅ **Solo local**: Todo se procesa en tu computadora
- ✅ **Sin tracking**: No hay seguimiento de uso

### Privacidad
- 🔒 **URLs**: Se procesan localmente
- 🔒 **Videos**: No se almacenan en servidores externos
- 🔒 **Configuración**: Solo en tu computadora

## 🆘 Soporte

### Documentación
- **README.md**: Documentación principal
- **INSTALACION.md**: Guía de instalación
- **SOLUCION_ERRORES.md**: Solución de problemas

### Pruebas
```bash
# Probar funcionalidad de URLs
python test_url_functionality.py

# Probar aplicación completa
python test_app.py
```

### Reportar Problemas
Si encuentras problemas con la funcionalidad de URLs:

1. Ejecuta `test_url_functionality.py`
2. Revisa los logs en la aplicación
3. Verifica tu conexión a internet
4. Prueba con diferentes URLs

---

**ClipForge** - Procesando videos desde URLs con la misma precisión y facilidad que archivos locales 🎬🌐 