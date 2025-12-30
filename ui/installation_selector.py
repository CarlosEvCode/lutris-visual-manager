"""
Ventana de selección de instalación de Lutris (Nativa o Flatpak)
"""
import tkinter as tk
from tkinter import ttk
import os


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
        
        # Crear ventana
        self.window = tk.Tk()
        self.window.title("Lutris Visual Manager - Selección de Instalación")
        self.window.geometry("550x300")
        self.window.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Configura la interfaz de la ventana"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="🎮 Lutris Visual Manager",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            main_frame,
            text="Selecciona la instalación de Lutris que deseas usar:",
            font=('Arial', 11)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame para las opciones
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Opción 1: Nativa
        self.native_button = self.create_option_button(
            options_frame,
            "🐧 Instalación Nativa",
            "~/.local/share/lutris/",
            self.native_exists,
            lambda: self.select_mode("NATIVO"),
            row=0
        )
        
        # Opción 2: Flatpak
        self.flatpak_button = self.create_option_button(
            options_frame,
            "📦 Instalación Flatpak",
            "~/.var/app/net.lutris.Lutris/",
            self.flatpak_exists,
            lambda: self.select_mode("FLATPAK"),
            row=1
        )
        
        # Si solo hay una opción disponible, mostrar mensaje
        if not self.native_exists and not self.flatpak_exists:
            error_label = ttk.Label(
                main_frame,
                text="⚠️  No se detectó ninguna instalación de Lutris",
                font=('Arial', 10),
                foreground='red'
            )
            error_label.pack(pady=10)
            
            # Usar configuración por defecto después de 2 segundos
            self.window.after(2000, lambda: self.select_mode("NATIVO_DEFAULT"))
    
    def create_option_button(self, parent, title, path, exists, command, row):
        """Crea un botón de opción con estilo"""
        # Frame para el botón
        frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5, padx=10)
        
        # Configurar colores según si existe
        if exists:
            bg_color = '#2d5016'  # Verde oscuro
            fg_color = '#90EE90'  # Verde claro
            status = "✓ Detectada"
        else:
            bg_color = '#3a3a3a'  # Gris oscuro
            fg_color = '#888888'  # Gris
            status = "✗ No encontrada"
        
        # Botón principal
        button = tk.Button(
            frame,
            text=f"{title}\n{path}\n{status}",
            command=command if exists else None,
            font=('Arial', 10, 'bold'),
            bg=bg_color,
            fg=fg_color,
            activebackground='#3d6b1f' if exists else bg_color,
            activeforeground='white' if exists else fg_color,
            relief=tk.FLAT,
            cursor='hand2' if exists else 'arrow',
            state=tk.NORMAL if exists else tk.DISABLED,
            padx=20,
            pady=15,
            justify=tk.LEFT
        )
        button.pack(fill=tk.BOTH, expand=True)
        
        # Efecto hover (solo si existe)
        if exists:
            def on_enter(e):
                button.config(bg='#3d6b1f')
            
            def on_leave(e):
                button.config(bg=bg_color)
            
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        # Configurar expansión
        parent.grid_columnconfigure(0, weight=1)
        
        return button
    
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
