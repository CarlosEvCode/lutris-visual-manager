#!/bin/bash
# Script para construir el AppImage de Lutris Visual Manager usando PyInstaller
# Este método es más confiable y compatible con aplicaciones GUI

set -e

echo "🔨 Construyendo Lutris Visual Manager AppImage con PyInstaller"
echo "================================================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que existe el icono
if [ ! -f "appimage/icon.png" ]; then
    echo "❌ Error: No se encontró appimage/icon.png"
    exit 1
fi

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "📦 Activando entorno virtual..."
    source .venv/bin/activate
fi

# Instalar PyInstaller si no está instalado
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "📦 Instalando PyInstaller..."
    pip install pyinstaller
    echo ""
fi

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf dist build
find . -maxdepth 1 -name "*.spec" -delete 2>/dev/null || true
echo ""

# Crear archivo .spec personalizado
echo "📝 Creando archivo .spec personalizado..."
cat > linux_build.spec << 'SPECEOF'
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# Recolectar todos los submódulos de PIL/Pillow
pillow_imports = collect_submodules('PIL')
pillow_datas = collect_data_files('PIL')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        ('/usr/lib/x86_64-linux-gnu/libffi.so.7', '.'),
    ],
    datas=[
        ('ui', 'ui'),
        ('utils', 'utils'),
        ('l_detector.py', '.'),
    ] + pillow_datas, 
    hiddenimports=[
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
        'tkinter',
        'tkinter.ttk',
        'tkinter.constants',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ] + pillow_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Excluir librerías gráficas conflictivas y de sistema
excluded_binaries = [
    'libfontconfig', 
    'libfreetype', 
    'libexpat', 
    'libharfbuzz',
    'libX11',
    # 'libxcb',  # NEEDED for Pillow binary wheels
    # 'libXau',  # NEEDED for Pillow binary wheels
    # 'libXdmcp', # NEEDED for Pillow binary wheels
    'libXext',
    'libXrender',
    'libGL',
    'libdrm',
    'libpng',
    'libz',
    'libglib',
    'libgobject',
    'libgio',
    'libgmodule',
    'libgthread',
    'libpcre',
    # 'libxcb-',  # NEEDED for Pillow binary wheels
    'libxkb',
    # libffi NO se excluye porque la incluimos explícitamente
    'libselinux',
    'libbsd',
    'libmd',
]

new_binaries = []
for (name, path, typecode) in a.binaries:
    should_exclude = False
    for exclusion in excluded_binaries:
        if exclusion in name:
            should_exclude = True
            print(f"🚫 Excluyendo librería conflictiva: {name}")
            break
    
    if not should_exclude:
        new_binaries.append((name, path, typecode))

a.binaries = new_binaries

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='lutris-visual-manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='lutris-visual-manager',
)
SPECEOF

echo ""

# Compilar con PyInstaller usando el .spec personalizado
echo "🔧 Compilando aplicación con PyInstaller (usando .spec personalizado)..."
echo ""

# Variables de entorno para compatibilidad
export PYTHONOPTIMIZE=0
export PYINSTALLER_COMPILE_BOOTLOADER=0

pyinstaller --clean linux_build.spec

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error al compilar con PyInstaller"
    exit 1
fi

echo ""
echo "📦 Creando estructura AppDir..."
echo ""

# Crear estructura AppDir
mkdir -p build/AppDir/usr/bin
mkdir -p build/AppDir/usr/share/applications
mkdir -p build/AppDir/usr/share/icons/hicolor/512x512/apps

# Copiar el directorio completo de la aplicación (--onedir)
cp -r dist/lutris-visual-manager build/AppDir/usr/bin/

# Limpiar librerías conflictivas del directorio compilado
echo "🧹 Eliminando librerías de sistema conflictivas..."
# find build/AppDir/usr/bin/lutris-visual-manager -type f -name "libxcb*" -delete  # Fix for Pillow
# find build/AppDir/usr/bin/lutris-visual-manager -type f -name "libX11*" -delete # Fix for Pillow
find build/AppDir/usr/bin/lutris-visual-manager -type f -name "libfontconfig*" -delete
find build/AppDir/usr/bin/lutris-visual-manager -type f -name "libfreetype*" -delete
find build/AppDir/usr/bin/lutris-visual-manager -type f -name "libGL*" -delete
# NO eliminamos libffi porque la necesitamos para compatibilidad entre distros
echo ""

# Copiar archivos de desktop e icono
cp appimage/l-visual-manager.desktop build/AppDir/
cp appimage/l-visual-manager.desktop build/AppDir/usr/share/applications/
cp appimage/icon.png build/AppDir/l-visual-manager.png
cp appimage/icon.png build/AppDir/usr/share/icons/hicolor/512x512/apps/l-visual-manager.png
cp appimage/icon.png build/AppDir/.DirIcon

# Crear AppRun mejorado
cat > build/AppDir/AppRun << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"

# IMPORTANTE: Priorizar librerías del sistema primero para evitar conflictos
# Esto es crítico para libxcb y otras librerías gráficas
export LD_LIBRARY_PATH="/usr/lib:/usr/lib/x86_64-linux-gnu:/lib/x86_64-linux-gnu:/lib:${HERE}/usr/bin/lutris-visual-manager"

# Limpiar variables que puedan causar conflictos
unset LD_PRELOAD

# Configuración de fuentes del sistema
export FONTCONFIG_PATH=/etc/fonts
export FONTCONFIG_FILE=/etc/fonts/fonts.conf

# Variables X11 para VirtualBox
export QT_X11_NO_MITSHM=1
export _X11_NO_MITSHM=1
export XLIB_SKIP_ARGB_VISUALS=1

# Ejecutar la aplicación
exec "${HERE}/usr/bin/lutris-visual-manager/lutris-visual-manager" "$@"
EOF

chmod +x build/AppDir/AppRun

# Descargar appimagetool si no existe
cd build
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    echo "📥 Descargando appimagetool..."
    wget -q --show-progress "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
    echo ""
fi

echo "🎁 Empaquetando AppImage..."
echo ""

# Crear el AppImage
ARCH=x86_64 ./appimagetool-x86_64.AppImage AppDir lutris-visual-manager-x86_64.AppImage 2>&1 | grep -v "WARNING"

if [ $? -eq 0 ] && [ -f "lutris-visual-manager-x86_64.AppImage" ]; then
    echo ""
    echo "✅ AppImage construido exitosamente!"
    echo ""
    ls -lh lutris-visual-manager-x86_64.AppImage
    echo ""
    echo "📍 Ubicación: build/lutris-visual-manager-x86_64.AppImage"
    echo ""
    echo "🚀 Para probarlo:"
    echo "   ./build/lutris-visual-manager-x86_64.AppImage"
    echo ""
    
    # Limpiar archivos temporales opcionales
    read -p "¿Deseas limpiar archivos temporales? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf AppDir appimagetool-x86_64.AppImage
        cd ..
        rm -rf dist *.spec
        echo "🧹 Limpieza completada"
    fi
else
    echo ""
    echo "❌ Error al empaquetar el AppImage"
    exit 1
fi
