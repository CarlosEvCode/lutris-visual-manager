# 📦 Guía de Empaquetado - Lutris Visual Manager

Este documento describe las opciones recomendadas para distribuir Lutris Visual Manager en Linux.

## 🎯 Opciones de Distribución

### 1. **AppImage** (Recomendado) ⭐

**Ventajas:**
- ✅ Un solo archivo ejecutable portable
- ✅ Funciona en la mayoría de distribuciones Linux
- ✅ No requiere instalación
- ✅ El usuario solo descarga y ejecuta
- ✅ Incluye todas las dependencias (Python, CustomTkinter, Pillow, etc.)

**Cómo crear:**

```bash
# 1. Asegúrate de tener el icono en appimage/icon.png
#    Formato: PNG, 512x512 píxeles (o 256x256 mínimo)

# 2. Ejecuta el script de build
./build_appimage.sh

# El script automáticamente:
# - Instala PyInstaller si es necesario
# - Compila la aplicación
# - Descarga appimagetool
# - Empaqueta todo en un AppImage
# - Limpia archivos temporales

# 3. El AppImage se generará en: build/lutris-visual-manager-x86_64.AppImage (~38MB)
```

**Estructura creada:**
```
proyecto_visual/
├── appimage/
│   ├── lutris-visual-manager.desktop  ✅ Archivo de entrada
│   ├── icon.png                        ✅ Icono (512x512 PNG)
│   └── ICON_README.md                  ℹ️  Guía para el icono
├── build_appimage.sh                   ✅ Script automatizado
├── main.py
├── requirements.txt
└── ...
```

**Probar el AppImage:**
```bash
./build/lutris-visual-manager-x86_64.AppImage
```

**Nota técnica:**
- Usa PyInstaller para compilar la aplicación
- Usa appimagetool para empaquetar el AppImage
- El ejecutable final es completamente portable
- No necesita Python instalado en el sistema del usuario

### 2. **PyInstaller** (Binario nativo)

**Ventajas:**
- ✅ Crea un ejecutable nativo
- ✅ Rápido de iniciar
- ✅ Puede incluir todas las dependencias

**Cómo crear:**

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear el ejecutable
pyinstaller --onefile \
  --windowed \
  --name="lutris-visual-manager" \
  --add-data="ui:ui" \
  --add-data="utils:utils" \
  --hidden-import=customtkinter \
  --hidden-import=PIL \
  main.py

# El resultado estará en dist/lutris-visual-manager
```

**Nota:** Puede requerir ajustes para que CustomTkinter funcione correctamente.

### 3. **Flatpak** (Sandbox)

**Ventajas:**
- ✅ Distribución a través de Flathub
- ✅ Actualizaciones automáticas
- ✅ Sandbox de seguridad
- ✅ Gestión de permisos

**Desventajas:**
- ⚠️ Necesita acceso a `~/.local/share/lutris` y `~/.var/app/net.lutris.Lutris`
- ⚠️ Configuración más compleja

**Manifest ejemplo (`net.lutris.VisualManager.yaml`):**
```yaml
app-id: net.lutris.VisualManager
runtime: org.freedesktop.Platform
runtime-version: '23.08'
sdk: org.freedesktop.Sdk
command: lutris-visual-manager

finish-args:
  - --share=ipc
  - --socket=x11
  - --socket=wayland
  - --filesystem=~/.local/share/lutris:rw
  - --filesystem=~/.var/app/net.lutris.Lutris:rw
  - --filesystem=~/.config/lutris-visual-manager:create
  - --share=network

modules:
  - name: python-dependencies
    buildsystem: simple
    build-commands:
      - pip3 install --prefix=/app customtkinter pillow
    
  - name: lutris-visual-manager
    buildsystem: simple
    build-commands:
      - install -D main.py /app/bin/lutris-visual-manager
      - cp -r ui utils /app/bin/
    sources:
      - type: dir
        path: .
```

### 4. **Snap** (Universal)

**Ventajas:**
- ✅ Funciona en Ubuntu y derivadas
- ✅ Actualizaciones automáticas
- ✅ Fácil publicación en Snap Store

**`snapcraft.yaml` ejemplo:**
```yaml
name: lutris-visual-manager
version: '1.0'
summary: Gestor visual de imágenes para Lutris
description: |
  Aplicación gráfica para gestionar las imágenes de tus juegos en Lutris.

base: core22
confinement: strict
grade: stable

apps:
  lutris-visual-manager:
    command: bin/python3 $SNAP/main.py
    plugs:
      - home
      - network
      - desktop
      - x11

parts:
  lutris-visual-manager:
    plugin: python
    source: .
    python-packages:
      - customtkinter
      - pillow
    stage-packages:
      - python3-tk
```

### 5. **Script de instalación** (Método simple)

Para usuarios que prefieren clonar el repo:

```bash
#!/bin/bash
# install.sh

echo "🎮 Instalando Lutris Visual Manager..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Instalar dependencias del sistema
if command -v apt &> /dev/null; then
    sudo apt install python3-tk python3-pip python3-venv -y
elif command -v pacman &> /dev/null; then
    sudo pacman -S tk python-pip --noconfirm
elif command -v dnf &> /dev/null; then
    sudo dnf install python3-tkinter python3-pip -y
fi

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias Python
pip install -r requirements.txt

# Crear lanzador
cat > ~/.local/share/applications/lutris-visual-manager.desktop << EOF
[Desktop Entry]
Name=Lutris Visual Manager
Comment=Gestor visual de imágenes para Lutris
Exec=$(pwd)/run.sh
Path=$(pwd)
Icon=$(pwd)/icon.png
Type=Application
Categories=Game;Utility;
Terminal=false
EOF

echo "✅ Instalación completada!"
echo "Puedes ejecutar: ./run.sh"
```

## 🏆 Recomendación Final

**Para distribución en GitHub:**

1. **Releases con AppImage** ⭐⭐⭐
   - Sube el `.AppImage` en GitHub Releases
   - El usuario solo descarga y ejecuta
   - Incluye instrucciones: `chmod +x lutris-visual-manager.AppImage && ./lutris-visual-manager.AppImage`

2. **Script de instalación** como alternativa
   - Para usuarios que prefieren clonar el repositorio
   - Más control sobre el entorno

3. **PyInstaller** como opción adicional
   - Binario más pequeño que AppImage
   - Puede requerir dependencias del sistema

## 📋 Checklist antes de empaquetar

- [ ] Eliminar cualquier API Key hardcodeado (✅ Ya hecho)
- [ ] Probar en diferentes distribuciones (Ubuntu, Fedora, Arch)
- [ ] Verificar permisos de archivos (`chmod +x`)
- [ ] Documentar dependencias del sistema (tk)
- [ ] Crear archivo `.desktop` con icono
- [ ] Agregar licencia (MIT recomendado)
- [ ] Actualizar README con instrucciones de instalación
- [ ] Crear releases en GitHub con changelog
- [ ] Probar que funciona con Lutris Native y Flatpak

## 🔧 Configuración persistente

✅ **Ya implementado:**
- API Key se guarda en `~/.config/lutris-visual-manager/config.json`
- Permisos 600 (solo lectura/escritura para el usuario)
- Último modo de instalación recordado
- Compatible con cualquier método de empaquetado

## 📚 Recursos adicionales

- [Python AppImage](https://github.com/niess/python-appimage)
- [PyInstaller](https://pyinstaller.org/)
- [Flatpak Documentation](https://docs.flatpak.org/)
- [Snapcraft Documentation](https://snapcraft.io/docs)
