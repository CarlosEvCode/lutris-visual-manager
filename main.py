#!/usr/bin/env python3
"""
Lutris Visual Manager
Aplicación para gestionar visualmente las imágenes de los juegos en Lutris

Autor: Asistente AI
Fecha: Diciembre 2025
"""

import sys
import os

# Asegurarse de que el directorio actual esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import tkinter
    except ImportError:
        print("❌ Error: Tkinter no está instalado.")
        print("Instala con: sudo apt install python3-tk")
        return False
    
    try:
        from PIL import Image
    except ImportError:
        print("❌ Error: Pillow no está instalado.")
        print("Instala con: pip install Pillow")
        return False
    
    return True

def main():
    """Punto de entrada de la aplicación"""
    print("=" * 50)
    print("🎮 Lutris Visual Manager")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Mostrar ventana de selección de instalación
    print("\n🔍 Detectando instalaciones de Lutris...")
    from ui.installation_selector import get_installation_choice
    
    selected_mode = get_installation_choice()
    
    if not selected_mode:
        print("\n❌ No se seleccionó ninguna instalación. Saliendo...")
        sys.exit(1)
    
    print(f"\n✓ Modo seleccionado: {selected_mode}")
    
    # Configurar rutas de Lutris según el modo seleccionado
    import config
    config.configure_lutris_paths(selected_mode)
    
    # Verificar que la base de datos exista
    if not os.path.exists(config.DB_PATH):
        print(f"❌ Error: No se encuentra la base de datos de Lutris en:")
        print(f"   {config.DB_PATH}")
        print("\n¿Tienes Lutris instalado?")
        sys.exit(1)
    
    print("✓ Base de datos de Lutris encontrada")
    print("✓ Iniciando aplicación...")
    print("\n⚠️  IMPORTANTE: Cierra Lutris antes de hacer cambios")
    print("=" * 50)
    
    # Iniciar la aplicación
    try:
        from ui.main_window import MainWindow
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
