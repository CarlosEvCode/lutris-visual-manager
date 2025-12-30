#!/bin/bash
# Build AppImage con máxima compatibilidad usando Docker
# Usa Ubuntu 20.04 con Python 3.11 para compatibilidad universal

set -e

echo "🐳 Construyendo AppImage compatible con Docker"
echo "==============================================="
echo ""

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    echo "Instala con: sudo pacman -S docker"
    exit 1
fi

# Verificar que el servicio Docker esté corriendo
if ! sudo docker info &> /dev/null; then
    echo "❌ Docker no está corriendo"
    echo "Inicia con: sudo systemctl start docker"
    exit 1
fi

echo "✅ Docker disponible"
echo ""

# Crear Dockerfile temporal
cat > /tmp/Dockerfile.lutris << 'EOF'
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3-tk \
    wget \
    file \
    && rm -rf /var/lib/apt/lists/*

# Instalar PyInstaller
RUN pip3 install pyinstaller pillow customtkinter packaging

WORKDIR /app

# Script de build
COPY . /app/

CMD ["bash", "/app/build_appimage.sh"]
EOF

echo "📦 Construyendo en contenedor Docker..."
echo ""

# Construir y ejecutar
sudo docker build -t lutris-appimage-builder -f /tmp/Dockerfile.lutris .
sudo docker run --rm -v "$(pwd)/build:/app/build" lutris-appimage-builder

echo ""
echo "✅ Build completado en Docker"
echo "📍 AppImage en: build/lutris-visual-manager-x86_64.AppImage"

# Limpiar
rm /tmp/Dockerfile.lutris
