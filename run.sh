#!/bin/bash
# Script de lanzamiento rápido para Lutris Visual Manager

echo "🎮 Lutris Visual Manager"
echo "========================"
echo ""

# Verificar si Lutris está corriendo
if pgrep -x "lutris" > /dev/null; then
    echo "⚠️  ADVERTENCIA: Lutris está corriendo"
    echo "   Se recomienda cerrar Lutris antes de hacer cambios"
    echo ""
    read -p "¿Continuar de todos modos? (s/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Operación cancelada"
        exit 1
    fi
fi

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Ejecutar la aplicación
python3 main.py
