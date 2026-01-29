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

# Fix para fuentes de CustomTkinter en AppImage y para X11 en VirtualBox
if getattr(sys, 'frozen', False):
    # Estamos en un ejecutable empaquetado
    os.environ['FONTCONFIG_PATH'] = '/etc/fonts'
    os.environ['FONTCONFIG_FILE'] = '/etc/fonts/fonts.conf'

# Fix para problemas de X11 en VirtualBox (BadLength error)
os.environ['QT_X11_NO_MITSHM'] = '1'
os.environ['_X11_NO_MITSHM'] = '1'
os.environ['XLIB_SKIP_ARGB_VISUALS'] = '1'

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    # Si estamos en un ejecutable empaquetado, asumimos que las dependencias están incluidas
    if getattr(sys, 'frozen', False):
        return True
    
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
    print("🎮 L-Visual-Manager")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Cargar gestor de configuración
    from utils.config_manager import get_config_manager
    config_mgr = get_config_manager()
    
    # Verificar si ya existe un API Key guardado
    saved_api_key = config_mgr.get_api_key()
    
    if saved_api_key:
        print("\n✓ API Key encontrado en configuración")
        api_key = saved_api_key
    else:
        # Solicitar API Key
        print("\n🔑 Solicitando API Key de SteamGridDB...")
        from ui.apikey_window import get_api_key
        
        api_key = get_api_key(show_change_option=False)
        
        if not api_key:
            print("\n❌ No se proporcionó API Key. Saliendo...")
            sys.exit(1)
        
        # Guardar API Key
        if config_mgr.set_api_key(api_key):
            print("✓ API Key guardado correctamente")
        else:
            print("⚠️  No se pudo guardar el API Key (se usará esta sesión)")
    
    # Configurar API Key en config
    import config
    config.STEAMGRIDDB_API_KEY = api_key
    
    # Verificar si hay un modo de instalación guardado
    saved_mode = config_mgr.get_last_installation_mode()
    
    # Mostrar ventana de selección de instalación
    print("\n🔍 Detectando instalaciones de Lutris...")
    from ui.installation_selector import get_installation_choice
    
    selected_mode = get_installation_choice(default_mode=saved_mode)
    
    if not selected_mode:
        print("\n❌ No se seleccionó ninguna instalación. Saliendo...")
        sys.exit(1)
    
    print(f"\n✓ Modo seleccionado: {selected_mode}")
    
    # Guardar el modo seleccionado para la próxima vez
    config_mgr.set_last_installation_mode(selected_mode)
    
    # Configurar rutas de Lutris según el modo seleccionado
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
