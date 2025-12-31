# Guía de Compilación de AppImage

## Problema Resuelto

Este proyecto experimentó varios desafíos al intentar crear un AppImage compatible con múltiples distribuciones de Linux. La solución final fue **compilar en la distribución más antigua** (Linux Mint) para garantizar compatibilidad hacia adelante.

## Problemas Encontrados y Soluciones

### 1. Error de Renderizado X11 con Emojis
- **Problema**: Emojis y fuentes grandes causaban `BadLength (poly request too large)` en X11
- **Solución**: Simplificar interfaz, eliminar emojis, reducir tamaños de fuente, usar fuentes del sistema

### 2. Python sin Soporte para PyInstaller
- **Problema**: Python compilado sin `--enable-shared`
- **Solución**: Usar Python del sistema (3.8-3.11) que incluye librerías compartidas

### 3. Conflicto con Pillow y libxcb
- **Problema**: Versiones precompiladas (wheel) de Pillow traían librerías incompatibles
- **Solución**: Compilar Pillow desde fuente: `pip install --no-binary :all: pillow`

### 4. Incompatibilidad libffi entre Distros
- **Problema**: Linux Mint usa `libffi.so.7`, distros modernas usan `libffi.so.8`
- **Solución**: Incluir explícitamente libffi en el AppImage con `--add-binary`

## Regla de Oro

**Siempre compila en la distribución más antigua que quieras soportar.**

- ✅ Compilar en Linux Mint → Funciona en CachyOS/Arch (compatibilidad hacia adelante)
- ❌ Compilar en CachyOS → No funciona en Linux Mint (glibc incompatible)

## Instrucciones de Compilación

### Requisitos Previos (Linux Mint / Ubuntu LTS)

```bash
# Instalar dependencias del sistema
sudo apt install python3 python3-pip python3-tk python3-dev build-essential

# Instalar PyInstaller
pip3 install pyinstaller

# Compilar Pillow desde fuente (IMPORTANTE)
pip3 install --no-binary :all: pillow

# Instalar otras dependencias
pip3 install customtkinter requests
```

### Compilar el AppImage

```bash
# Ejecutar el script de compilación
./build_appimage.sh
```

El AppImage resultante estará en `build/lutris-visual-manager-x86_64.AppImage`

## Notas Técnicas

### Librerías Excluidas del AppImage

Para evitar conflictos con el sistema anfitrión, se excluyen las siguientes librerías gráficas (se usan las del sistema):

- libfontconfig, libfreetype, libexpat, libharfbuzz
- libX11, libxcb, libXau, libXdmcp, libXext, libXrender
- libGL, libdrm, libpng, libz
- libglib, libgobject, libgio, libgmodule, libgthread, libpcre

### Librerías Incluidas

- **libffi**: Necesaria para ctypes (CustomTkinter)
- **Pillow**: Compilada desde fuente con dependencias del sistema

## Distribución

El AppImage generado es compatible con:
- Linux Mint 20.x/21.x
- Ubuntu 20.04 LTS y superiores
- Debian 11 (Bullseye) y superiores
- Arch Linux, Manjaro, CachyOS (distros rolling)
- Fedora, openSUSE (distros modernas)

## Alternativa: Script de Instalación

Si el AppImage presenta problemas, usa el script de instalación local:

```bash
./install.sh
```

Esto instala la aplicación desde el código fuente en `~/.local/share/` y funciona en cualquier distribución con Python 3.8+.
