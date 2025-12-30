"""
Ventana de selección de instalación de Lutris (Nativa o Flatpak)
Versión moderna con CustomTkinter y Material Design
"""
import customtkinter as ctk
import os
from ui import theme


class InstallationSelector:
    def __init__(self):
        """Ventana para seleccionar entre instalación Nativa o Flatpak de Lutris"""
        self.selected_mode = None
        
        # Rutas de las bases de datos
        self.PATH_NATIVE_DB = os.path.expanduser("~/.local/share/lutris/pga.db")
        self.PATH_FLATPAK_DB = os.path.expanduser("~/.var/app/net.lutris.Lutris/data/lutris/pga.db")
        
        # Detectar qué instalaciones existen
        self.native_exists = os.path.exists(self.PATH_NATIVE_DB)
        self.flatpak_exists = os.path.exists(self.PATH_FLATPAK_DB)
        
        # Aplicar tema
        theme.apply_theme()
        
        # Crear ventana
        self.window = ctk.CTk()
        self.window.title("Lutris Visual Manager")
        self.window.geometry("700x450")
        self.window.resizable(False, False)
        
        # Color de fondo
        self.window.configure(fg_color=theme.PRIMARY_BG)
        
        # Centrar ventana
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.window.update_idletasks()
        width = 700
        height = 450
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Configura la interfaz de la ventana"""
        # Frame principal con padding
        main_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=theme.PADDING_L, pady=theme.PADDING_L)
        
        # Título principal
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"{theme.ICONS['game']} Lutris Visual Manager",
            font=theme.FONT_TITLE,
            text_color=theme.TEXT_PRIMARY
        )
        title_label.pack(pady=(0, theme.PADDING_S))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Selecciona tu instalación de Lutris",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, theme.PADDING_XL))
        
        # Frame para las opciones (grid horizontal)
        options_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        options_frame.pack(fill="both", expand=True, pady=theme.PADDING_M)
        
        # Configurar grid para 2 columnas
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)
        
        # Opción 1: Nativa (columna 0)
        self.create_option_card(
            options_frame,
            icon=theme.ICONS['native'],
            title="Instalación Nativa",
            description="~/.local/share/lutris/",
            exists=self.native_exists,
            command=lambda: self.select_mode("NATIVO"),
            column=0
        )
        
        # Opción 2: Flatpak (columna 1)
        self.create_option_card(
            options_frame,
            icon=theme.ICONS['flatpak'],
            title="Instalación Flatpak",
            description="~/.var/app/net.lutris.Lutris/",
            exists=self.flatpak_exists,
            command=lambda: self.select_mode("FLATPAK"),
            column=1
        )
        
        # Si no hay instalaciones
        if not self.native_exists and not self.flatpak_exists:
            warning_frame = ctk.CTkFrame(
                main_frame,
                fg_color=theme.CARD_BG,
                corner_radius=theme.RADIUS_M,
                border_width=1,
                border_color=theme.WARNING
            )
            warning_frame.pack(fill="x", pady=theme.PADDING_M)
            
            warning_label = ctk.CTkLabel(
                warning_frame,
                text=f"{theme.ICONS['warning']} No se detectó ninguna instalación de Lutris",
                font=theme.FONT_BODY,
                text_color=theme.WARNING
            )
            warning_label.pack(pady=theme.PADDING_M)
            
            # Usar configuración por defecto después de 2 segundos
            self.window.after(2000, lambda: self.select_mode("NATIVO_DEFAULT"))
    
    def create_option_card(self, parent, icon, title, description, exists, command, column):
        """Crea una card moderna para cada opción"""
        # Determinar colores según disponibilidad
        if exists:
            fg_color = theme.CARD_BG
            border_color = theme.BORDER
            hover_color = theme.TERTIARY_BG
            text_color = theme.TEXT_PRIMARY
            status_text = f"{theme.ICONS['check']} Detectada"
            status_color = theme.SUCCESS
        else:
            fg_color = theme.SECONDARY_BG
            border_color = theme.BORDER
            hover_color = theme.SECONDARY_BG
            text_color = theme.TEXT_DISABLED
            status_text = f"{theme.ICONS['close']} No encontrada"
            status_color = theme.TEXT_DISABLED
        
        # Frame principal de la card
        card_frame = ctk.CTkFrame(
            parent,
            fg_color=fg_color,
            corner_radius=theme.RADIUS_M,
            border_width=2,
            border_color=border_color
        )
        card_frame.grid(row=0, column=column, padx=theme.PADDING_S, pady=0, sticky="nsew")
        
        # Frame interno con padding
        inner_frame = ctk.CTkFrame(
            card_frame,
            fg_color="transparent"
        )
        inner_frame.pack(fill="both", expand=True, padx=theme.PADDING_M, pady=theme.PADDING_L)
        
        # Icono grande centrado
        icon_label = ctk.CTkLabel(
            inner_frame,
            text=icon,
            font=("Arial", 64),
            text_color=text_color
        )
        icon_label.pack(pady=(theme.PADDING_M, theme.PADDING_S))
        
        # Título
        title_label = ctk.CTkLabel(
            inner_frame,
            text=title,
            font=theme.FONT_HEADING,
            text_color=text_color,
            wraplength=250
        )
        title_label.pack(pady=(0, theme.PADDING_XS))
        
        # Descripción
        desc_label = ctk.CTkLabel(
            inner_frame,
            text=description,
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_SECONDARY if exists else theme.TEXT_DISABLED,
            wraplength=250
        )
        desc_label.pack(pady=(0, theme.PADDING_S))
        
        # Estado
        status_label = ctk.CTkLabel(
            inner_frame,
            text=status_text,
            font=theme.FONT_BODY_BOLD,
            text_color=status_color
        )
        status_label.pack(pady=(theme.PADDING_XS, 0))
        
        # Hacer toda la card clickeable si existe
        if exists:
            # Configurar cursor
            for widget in [card_frame, inner_frame, icon_label, title_label, desc_label, status_label]:
                widget.configure(cursor="hand2")
                widget.bind("<Button-1>", lambda e: command())
            
            # Efectos hover
            def on_enter(e):
                card_frame.configure(border_color=theme.BORDER_HOVER, fg_color=hover_color)
            
            def on_leave(e):
                card_frame.configure(border_color=border_color, fg_color=fg_color)
            
            for widget in [card_frame, inner_frame, icon_label, title_label, desc_label, status_label]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
    
    def select_mode(self, mode):
        """Selecciona el modo y cierra la ventana"""
        self.selected_mode = mode
        self.window.quit()
        self.window.destroy()
    
    def run(self):
        """Ejecuta la ventana y retorna el modo seleccionado"""
        self.window.mainloop()
        return self.selected_mode


def get_installation_choice():
    """
    Función de conveniencia para obtener la elección del usuario
    
    Returns:
        str: 'NATIVO', 'FLATPAK' o 'NATIVO_DEFAULT'
    """
    selector = InstallationSelector()
    return selector.run()


if __name__ == "__main__":
    # Prueba
    choice = get_installation_choice()
    print(f"Modo seleccionado: {choice}")
