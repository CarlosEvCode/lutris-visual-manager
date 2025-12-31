"""
Tema personalizado Material Design para Lutris Visual Manager
Paleta de colores azul oscuro con acentos modernos
"""

# ==========================================
# 🎨 PALETA DE COLORES - MATERIAL DARK BLUE
# ==========================================

# Colores principales
PRIMARY_BG = "#0d1117"          # Fondo principal (negro-azul muy oscuro)
SECONDARY_BG = "#161b22"        # Fondo secundario (un poco más claro)
TERTIARY_BG = "#1c2128"         # Fondo terciario (cards, frames)
CARD_BG = "#21262d"             # Fondo de cards

# Colores de acento
ACCENT_BLUE = "#58a6ff"         # Azul brillante (botones, links)
ACCENT_BLUE_HOVER = "#79c0ff"   # Azul más claro (hover)
ACCENT_BLUE_DARK = "#388bfd"    # Azul oscuro (pressed)

# Colores de texto
TEXT_PRIMARY = "#c9d1d9"        # Texto principal
TEXT_SECONDARY = "#8b949e"      # Texto secundario
TEXT_DISABLED = "#484f58"       # Texto deshabilitado

# Colores de borde
BORDER = "#30363d"              # Bordes normales
BORDER_HOVER = "#58a6ff"        # Bordes en hover
BORDER_SELECTED = "#1f6feb"     # Bordes seleccionados

# Colores de estado
SUCCESS = "#3fb950"             # Verde éxito
ERROR = "#f85149"               # Rojo error
WARNING = "#d29922"             # Amarillo advertencia
INFO = "#58a6ff"                # Azul información

# Colores especiales
HOVER_BG = "#30363d"            # Fondo hover
SELECTED_BG = "#1f6feb"         # Fondo seleccionado
SCROLLBAR = "#30363d"           # Scrollbar

# ==========================================
# 📏 DIMENSIONES Y ESPACIADO
# ==========================================

CORNER_RADIUS = 10              # Radio de esquinas redondeadas
BORDER_WIDTH = 1                # Ancho de bordes

# ==========================================
# 📐 CONFIGURACIÓN DE CUSTOMTKINTER
# ==========================================

def apply_theme():
    """Aplica el tema personalizado a CustomTkinter"""
    import customtkinter as ctk
    
    # Configurar modo y tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")  # Base, se personalizará

def get_button_colors(style="primary"):
    """Retorna colores para botones según el estilo"""
    if style == "secondary":
        return {
            "fg_color": TERTIARY_BG,
            "hover_color": HOVER_BG,
            "text_color": TEXT_PRIMARY,
            "border_color": BORDER,
            "border_width": 2
        }
    else:  # primary
        return {
            "fg_color": ACCENT_BLUE,
            "hover_color": ACCENT_BLUE_HOVER,
            "text_color": "#ffffff",
            "border_color": BORDER
        }

def get_button_secondary_colors():
    """Retorna colores para botones secundarios (deprecated, usar get_button_colors('secondary'))"""
    return get_button_colors("secondary")

def get_entry_colors():
    """Retorna colores para campos de entrada"""
    return {
        "fg_color": SECONDARY_BG,
        "border_color": BORDER,
        "text_color": TEXT_PRIMARY
    }

def get_frame_colors():
    """Retorna colores para frames"""
    return {
        "fg_color": CARD_BG,
        "border_color": BORDER
    }

def get_label_colors():
    """Retorna colores para labels"""
    return {
        "text_color": TEXT_PRIMARY,
        "fg_color": "transparent"
    }

def get_card_style():
    """Retorna estilo para cards"""
    return {
        "fg_color": CARD_BG,
        "corner_radius": 10,
        "border_width": 1,
        "border_color": BORDER
    }

def get_hover_card_style():
    """Retorna estilo para cards con hover"""
    return {
        "fg_color": TERTIARY_BG,
        "corner_radius": 10,
        "border_width": 2,
        "border_color": BORDER_HOVER
    }

# ==========================================
# 🔤 TIPOGRAFÍA
# ==========================================

# Usar fuente por defecto del sistema para evitar problemas de X11/RENDER
# No especificar familia de fuente permite que Tkinter use la fuente del sistema
FONT_FAMILY = None  # None usa la fuente por defecto de Tkinter

# Crear tuplas de fuentes de manera segura
def _make_font(size, weight=None):
    """Crea tupla de fuente segura para el sistema"""
    if weight:
        return ("TkDefaultFont", size, weight)
    return ("TkDefaultFont", size)

# Títulos - Tamaños reducidos para evitar problemas de X11 en VirtualBox
FONT_TITLE = _make_font(18, "bold")
FONT_SUBTITLE = _make_font(14, "bold")
FONT_HEADING = _make_font(12, "bold")

# Cuerpo
FONT_BODY = _make_font(11)
FONT_BODY_BOLD = _make_font(11, "bold")
FONT_SMALL = _make_font(10)
FONT_TINY = _make_font(9)

# ==========================================
# 📏 ESPACIADO Y DIMENSIONES
# ==========================================

# Padding
PADDING_XL = 30
PADDING_L = 20
PADDING_M = 15
PADDING_S = 10
PADDING_XS = 5

# Corner radius
RADIUS_L = 15
RADIUS_M = 10
RADIUS_S = 5

# Tamaños de elementos
BUTTON_HEIGHT = 36
INPUT_HEIGHT = 40
CARD_MIN_HEIGHT = 100

# ==========================================
# 🎭 ICONOS - Reemplazados por texto para evitar problemas de X11
# ==========================================

ICONS = {
    "game": "",
    "cover": "[Cover]",
    "banner": "[Banner]",
    "icon": "[Icon]",
    "search": "",
    "download": "",
    "upload": "",
    "settings": "",
    "refresh": "",
    "check": "[OK]",
    "close": "[X]",
    "warning": "",
    "error": "",
    "success": "[OK]",
    "info": "",
    "folder": "",
    "image": "",
    "platform": "",
    "native": "[NATIVA]",
    "flatpak": "[FLATPAK]",
}
