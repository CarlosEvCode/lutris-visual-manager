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
rm -rf build dist *.spec
echo ""

# Compilar con PyInstaller
echo "🔧 Compilando aplicación con PyInstaller..."
echo ""

# Variables de entorno para compatibilidad
export PYTHONOPTIMIZE=0
export PYINSTALLER_COMPILE_BOOTLOADER=0

pyinstaller --clean \
    --onefile \
    --windowed \
    --name="lutris-visual-manager" \
    --add-data="ui:ui" \
    --add-data="utils:utils" \
    --add-data="lutris_detector.py:." \
    --hidden-import=customtkinter \
    --hidden-import=PIL \
    --hidden-import=PIL._tkinter_finder \
    --hidden-import=tkinter \
    --collect-all=customtkinter \
    --strip \
    --noupx \
    main.py

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

# Copiar el ejecutable
cp dist/lutris-visual-manager build/AppDir/usr/bin/

# Copiar archivos de desktop e icono
cp appimage/lutris-visual-manager.desktop build/AppDir/
cp appimage/lutris-visual-manager.desktop build/AppDir/usr/share/applications/
cp appimage/icon.png build/AppDir/lutris-visual-manager.png
cp appimage/icon.png build/AppDir/usr/share/icons/hicolor/512x512/apps/lutris-visual-manager.png
cp appimage/icon.png build/AppDir/.DirIcon

# Crear AppRun
cat > build/AppDir/AppRun << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "${HERE}/usr/bin/lutris-visual-manager" "$@"
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
