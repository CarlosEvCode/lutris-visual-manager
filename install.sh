#!/bin/bash
# Script de instalación de Lutris Visual Manager
# Instala la aplicación en ~/.local/share/lutris-visual-manager

set -e

INSTALL_DIR="$HOME/.local/share/lutris-visual-manager"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "📦 Instalando Lutris Visual Manager..."
echo ""

# Crear directorios si no existen
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"

# Copiar archivos del proyecto
echo "📁 Copiando archivos..."
cp -r main.py ui utils config.py lutris_detector.py requirements.txt "$INSTALL_DIR/"
cp appimage/icon.png "$INSTALL_DIR/"

# Crear script launcher
echo "🔧 Creando launcher..."
cat > "$BIN_DIR/lutris-visual-manager" << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/lutris-visual-manager"
python3 main.py "$@"
EOF

chmod +x "$BIN_DIR/lutris-visual-manager"

# Crear archivo .desktop
echo "🖥️  Creando entrada de menú..."
cat > "$DESKTOP_DIR/lutris-visual-manager.desktop" << EOF
[Desktop Entry]
Name=Lutris Visual Manager
Comment=Gestor visual de imágenes para Lutris
Exec=$BIN_DIR/lutris-visual-manager
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Game;Utility;
EOF

# Instalar dependencias si no están instaladas
echo ""
echo "📦 Verificando dependencias..."
if ! python3 -c "import customtkinter" 2>/dev/null; then
    echo "⚠️  CustomTkinter no está instalado. Instalando..."
    pip3 install --user -r "$INSTALL_DIR/requirements.txt"
else
    echo "✅ Dependencias ya instaladas"
fi

echo ""
echo "✅ ¡Instalación completada!"
echo ""
echo "Puedes ejecutar la aplicación de estas formas:"
echo "  1. Busca 'Lutris Visual Manager' en el menú de aplicaciones"
echo "  2. Ejecuta: lutris-visual-manager"
echo ""
echo "Para desinstalar:"
echo "  rm -rf $INSTALL_DIR"
echo "  rm $BIN_DIR/lutris-visual-manager"
echo "  rm $DESKTOP_DIR/lutris-visual-manager.desktop"
