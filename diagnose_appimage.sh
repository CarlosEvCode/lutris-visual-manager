#!/bin/bash
# Script de diagnóstico para AppImage
# Ejecuta esto en la máquina virtual para diagnosticar el problema

echo "🔍 Diagnóstico de compatibilidad de AppImage"
echo "============================================="
echo ""

# Verificar arquitectura
echo "📊 Arquitectura del sistema:"
uname -m
echo ""

# Verificar CPU
echo "🖥️  CPU:"
lscpu | grep -E "Model name|Architecture|CPU op-mode"
echo ""

# Verificar flags de CPU
echo "⚙️  Flags de CPU disponibles:"
grep flags /proc/cpuinfo | head -1 | grep -oE '(sse|sse2|sse3|sse4|avx|avx2|avx512)' | sort -u
echo ""

# Verificar versión de glibc
echo "📚 Versión de glibc:"
ldd --version | head -1
echo ""

# Verificar Python
echo "🐍 Python disponible:"
python3 --version 2>/dev/null || echo "Python3 no encontrado"
echo ""

# Intentar extraer el AppImage
echo "📦 Intentando extraer AppImage..."
if [ -f "lutris-visual-manager-x86_64.AppImage" ]; then
    chmod +x lutris-visual-manager-x86_64.AppImage
    ./lutris-visual-manager-x86_64.AppImage --appimage-extract 2>&1 | head -5
    echo ""
    
    # Verificar el ejecutable extraído
    if [ -f "squashfs-root/usr/bin/lutris-visual-manager" ]; then
        echo "🔍 Información del ejecutable:"
        file squashfs-root/usr/bin/lutris-visual-manager
        echo ""
        
        echo "📋 Dependencias:"
        ldd squashfs-root/usr/bin/lutris-visual-manager 2>&1 | head -10
    fi
else
    echo "❌ No se encontró el AppImage"
fi

echo ""
echo "✅ Diagnóstico completado"
echo ""
echo "💡 Soluciones posibles:"
echo "   1. Actualizar glibc en la VM"
echo "   2. Usar Python 3.11 en lugar de 3.13 para compilar"
echo "   3. Compilar el AppImage dentro de la VM"
