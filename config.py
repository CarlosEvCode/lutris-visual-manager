"""
Configuración global del Lutris Visual Manager
"""
import os
import sys

# ==========================================
# 🔑 API KEY
# ==========================================
STEAMGRIDDB_API_KEY = "4e712a33643639391ac4f80886ace444"

# ==========================================
# 📁 RUTAS DE LUTRIS (DETECCIÓN AUTOMÁTICA)
# ==========================================
# Importar el detector universal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lutris_detector import get_lutris_paths

# Esta función se llamará después de obtener el modo del usuario
def configure_lutris_paths(mode=None):
    """
    Configura las rutas de Lutris basado en el modo seleccionado
    
    Args:
        mode: 'NATIVO', 'FLATPAK' o 'NATIVO_DEFAULT'
    """
    global DB_PATH, COVERS_DIR, BANNERS_DIR, LUTRIS_ICONS_DIR, SYSTEM_ICONS_DIR
    
    print("🔍 Configurando rutas de Lutris...")
    _paths = get_lutris_paths(interactive=False, mode=mode)
    
    DB_PATH = _paths['db_path']
    COVERS_DIR = _paths['covers_dir']
    BANNERS_DIR = _paths['banners_dir']
    LUTRIS_ICONS_DIR = _paths['lutris_icons_dir']
    SYSTEM_ICONS_DIR = _paths['system_icons_dir']
    
    # Imprimir resumen
    print("\n" + "="*60)
    print(f"✅ CONFIGURACIÓN {_paths['mode']}")
    print("="*60)
    print(f"DB:       {DB_PATH}")
    print(f"Covers:   {COVERS_DIR}")
    print(f"Banners:  {BANNERS_DIR}")
    print(f"Icons:    {LUTRIS_ICONS_DIR}")
    print(f"Sistema:  {SYSTEM_ICONS_DIR}")
    print("="*60 + "\n")

# Variables globales (se configurarán después)
DB_PATH = None
COVERS_DIR = None
BANNERS_DIR = None
LUTRIS_ICONS_DIR = None
SYSTEM_ICONS_DIR = None

# ==========================================
# 🎨 CONFIGURACIÓN DE LA INTERFAZ
# ==========================================
WINDOW_TITLE = "Lutris Visual Manager"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

# Tamaños de miniaturas en la interfaz principal
THUMBNAIL_WIDTH = 150
THUMBNAIL_HEIGHT = 200  # Para covers (600x900)
BANNER_THUMBNAIL_WIDTH = 300
BANNER_THUMBNAIL_HEIGHT = 100  # Para banners (heroes)
ICON_THUMBNAIL_SIZE = 64

# Tamaños de imágenes en el selector
SELECTOR_THUMB_WIDTH = 200
SELECTOR_THUMB_HEIGHT = 280

# ==========================================
# 🎮 PLATAFORMAS SOPORTADAS
# ==========================================
# Mapeo de runner -> nombre amigable
PLATFORMS = {
    "mame": "Arcade (MAME)",
    "duckstation": "PlayStation 1",
    "pcsx2": "PlayStation 2",
    "citra": "Nintendo 3DS",
    "cemu": "Nintendo Wii U",
}

# ==========================================
# 🛡️ FILTROS ANTI-DMCA
# ==========================================
# Runners de Nintendo que necesitan filtro más agresivo
NINTENDO_RUNNERS = ["citra", "cemu"]

# Cuántas imágenes saltar para cada tipo
SKIP_COUNT = {
    "cover": 1,
    "banner": 2,  # Más agresivo para banners de Nintendo
    "icon": 1
}

# ==========================================
# 🔄 CACHE
# ==========================================
CACHE_DIR = os.path.expanduser("~/.cache/lutris_visual_manager/")
os.makedirs(CACHE_DIR, exist_ok=True)
