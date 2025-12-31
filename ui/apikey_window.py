"""
Ventana para solicitar el API Key de SteamGridDB
"""
import customtkinter as ctk
from ui import theme
import os

# Configurar CustomTkinter para evitar problemas de X11
os.environ.setdefault('TK_SILENCE_DEPRECATION', '1')

# Configurar escalado de fuentes para reducir carga en X11
try:
    ctk.deactivate_automatic_dpi_awareness()
except:
    pass

class APIKeyWindow:
    def __init__(self, show_change_option=False, current_key=None):
        """
        Args:
            show_change_option: Si es True, muestra opción para cambiar API Key existente
            current_key: API Key actual a mostrar en el campo (opcional)
        """
        self.api_key = None
        self.show_change_option = show_change_option
        self.current_key = current_key
        self.window = ctk.CTk()
        self.window.title("API Key - SteamGridDB")
        self.window.geometry("600x450")
        self.center_window(600, 450)
        
        # Configurar el tema
        ctk.set_appearance_mode("dark")
        self.window.configure(fg_color=theme.PRIMARY_BG)
        
        # Prevenir cierre con X
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        self.create_widgets()
    
    def center_window(self, width, height):
        """Centra la ventana en la pantalla"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal con padding
        main_frame = ctk.CTkFrame(
            self.window,
            fg_color=theme.PRIMARY_BG,
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=theme.PADDING_L, pady=theme.PADDING_L)
        
        # Título - SIN EMOJIS para evitar problemas de X11
        title_text = "API Key de SteamGridDB"
        if self.show_change_option:
            title_text = "Cambiar API Key"
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=title_text,
            font=theme.FONT_TITLE,
            text_color=theme.TEXT_PRIMARY
        )
        title_label.pack(pady=(0, theme.PADDING_M))
        
        # Descripción
        desc_text = (
            "Para usar esta aplicacion, necesitas un API Key de SteamGridDB.\n"
            "Es gratuito y te permite buscar imagenes para tus juegos."
        )
        desc_label = ctk.CTkLabel(
            main_frame,
            text=desc_text,
            font=theme.FONT_BODY,
            text_color=theme.TEXT_SECONDARY,
            justify="center",
            wraplength=500
        )
        desc_label.pack(pady=(0, theme.PADDING_M))
        
        # Frame de instrucciones
        instructions_frame = ctk.CTkFrame(
            main_frame,
            fg_color=theme.SECONDARY_BG,
            corner_radius=theme.CORNER_RADIUS
        )
        instructions_frame.pack(fill="x", pady=(0, theme.PADDING_M))
        
        instructions_title = ctk.CTkLabel(
            instructions_frame,
            text="Como obtener tu API Key:",
            font=theme.FONT_HEADING,
            text_color=theme.ACCENT_BLUE,
            anchor="w"
        )
        instructions_title.pack(anchor="w", padx=theme.PADDING_M, pady=(theme.PADDING_M, theme.PADDING_XS))
        
        steps = [
            "1. Visita: https://www.steamgriddb.com/profile/preferences/api",
            "2. Inicia sesión o crea una cuenta (gratis)",
            "3. Genera un nuevo API Key",
            "4. Copia el API Key y pégalo abajo"
        ]
        
        for step in steps:
            step_label = ctk.CTkLabel(
                instructions_frame,
                text=step,
                font=theme.FONT_SMALL,
                text_color=theme.TEXT_SECONDARY,
                anchor="w"
            )
            step_label.pack(anchor="w", padx=theme.PADDING_L, pady=2)
        
        instructions_frame.pack_configure(pady=(0, theme.PADDING_M))
        
        # Input del API Key
        input_label = ctk.CTkLabel(
            main_frame,
            text="Ingresa tu API Key:" if not self.current_key else "API Key actual:",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_PRIMARY,
            anchor="w"
        )
        input_label.pack(anchor="w", pady=(0, theme.PADDING_XS))
        
        self.api_key_entry = ctk.CTkEntry(
            main_frame,
            height=40,
            font=theme.FONT_BODY,
            fg_color=theme.SECONDARY_BG,
            border_color=theme.BORDER,
            text_color=theme.TEXT_PRIMARY,
            placeholder_text="Ej: 1a2b3c4d5e6f7g8h9i0j..."
        )
        self.api_key_entry.pack(fill="x", pady=(0, theme.PADDING_M))
        
        # Si hay un API Key actual, mostrarlo
        if self.current_key:
            self.api_key_entry.insert(0, self.current_key)
        
        self.api_key_entry.focus()
        
        # Bind Enter key
        self.api_key_entry.bind("<Return>", lambda e: self.on_continue())
        
        # Nota sobre seguridad - SIN EMOJI
        security_note = ctk.CTkLabel(
            main_frame,
            text="Tu API Key se guardara de forma segura en ~/.config/lutris-visual-manager/",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_SECONDARY,
            wraplength=500
        )
        security_note.pack(pady=(0, theme.PADDING_M))
        
        # Frame de botones
        buttons_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        buttons_frame.pack(fill="x", pady=(theme.PADDING_M, 0))
        
        # Botón Cancelar
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            height=40,
            font=theme.FONT_BODY,
            **theme.get_button_colors("secondary"),
            command=self.on_cancel
        )
        cancel_button.pack(side="left", fill="x", expand=True, padx=(0, theme.PADDING_S))
        
        # Botón Continuar
        continue_button = ctk.CTkButton(
            buttons_frame,
            text="Continuar",
            height=40,
            font=theme.FONT_BODY,
            **theme.get_button_colors("primary"),
            command=self.on_continue
        )
        continue_button.pack(side="right", fill="x", expand=True, padx=(theme.PADDING_S, 0))
    
    def on_continue(self):
        """Valida y guarda el API Key"""
        api_key = self.api_key_entry.get().strip()
        
        if not api_key:
            self.show_error("Por favor ingresa un API Key válido")
            return
        
        if len(api_key) < 20:
            self.show_error("El API Key parece ser demasiado corto. Verifica que lo hayas copiado completo.")
            return
        
        self.api_key = api_key
        self.window.quit()
        self.window.destroy()
    
    def on_cancel(self):
        """Cancela y cierra la aplicación"""
        self.api_key = None
        self.window.quit()
        self.window.destroy()
    
    def show_error(self, message):
        """Muestra un mensaje de error"""
        from ui.dialogs import show_error
        show_error(self.window, "Error de validación", message)
    
    def show(self):
        """Muestra la ventana y retorna el API Key"""
        self.window.mainloop()
        return self.api_key


def get_api_key(show_change_option=False, current_key=None):
    """
    Muestra la ventana de API Key y retorna el key ingresado
    
    Args:
        show_change_option: Si es True, indica que se está cambiando un API Key existente
        current_key: API Key actual a mostrar en el campo (opcional)
    
    Returns:
        str: API Key ingresado o None si se canceló
    """
    window = APIKeyWindow(show_change_option=show_change_option, current_key=current_key)
    return window.show()
