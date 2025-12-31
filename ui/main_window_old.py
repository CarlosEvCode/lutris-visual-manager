"""
Ventana principal del Lutris Visual Manager
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import config
from utils.database import LutrisDatabase
from utils.api import SteamGridDBAPI
from utils.image_manager import ImageManager
from ui.selector_window import SelectorWindow

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        
        self.db = LutrisDatabase()
        self.api = SteamGridDBAPI()
        self.image_manager = ImageManager()
        
        self.current_runner = None
        self.games = []
        
        self.setup_ui()
        self.load_runners()
    
    def setup_ui(self):
        """Configura la interfaz principal"""
        # Frame superior con selección de plataforma
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="🎮 Lutris Visual Manager", 
                 font=('Arial', 16, 'bold')).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(top_frame, text="Plataforma:").pack(side=tk.LEFT, padx=10)
        
        self.runner_var = tk.StringVar()
        self.runner_combo = ttk.Combobox(top_frame, textvariable=self.runner_var, 
                                         state='readonly', width=30)
        self.runner_combo.pack(side=tk.LEFT, padx=5)
        self.runner_combo.bind('<<ComboboxSelected>>', self.on_runner_selected)
        
        ttk.Button(top_frame, text="🔄 Refrescar", 
                  command=self.refresh_games).pack(side=tk.LEFT, padx=10)
        
        # Frame principal con scroll
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Canvas con scrollbar
        self.canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Label inicial
        self.info_label = ttk.Label(self.scrollable_frame, 
                                    text="👆 Selecciona una plataforma arriba", 
                                    font=('Arial', 12))
        self.info_label.pack(pady=50)
        
        # Barra de estado
        self.status_bar = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_runners(self):
        """Carga la lista de runners disponibles"""
        runners = self.db.get_runners()
        
        # Crear lista de opciones amigables
        options = []
        self.runner_map = {}
        for runner in runners:
            friendly_name = config.PLATFORMS.get(runner, runner.capitalize())
            options.append(friendly_name)
            self.runner_map[friendly_name] = runner
        
        self.runner_combo['values'] = options
        
        if options:
            self.status_bar.config(text=f"✓ {len(options)} plataformas encontradas")
    
    def on_runner_selected(self, event=None):
        """Maneja la selección de un runner"""
        friendly_name = self.runner_var.get()
        self.current_runner = self.runner_map.get(friendly_name)
        
        if self.current_runner:
            self.load_games()
    
    def refresh_games(self):
        """Refresca la lista de juegos"""
        if self.current_runner:
            self.load_games()
    
    def load_games(self):
        """Carga los juegos del runner seleccionado"""
        # Limpiar el frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Mostrar mensaje de carga
        loading = ttk.Label(self.scrollable_frame, text="🔄 Cargando juegos...", 
                           font=('Arial', 12))
        loading.pack(pady=50)
        
        self.status_bar.config(text=f"Cargando juegos de {self.runner_var.get()}...")
        
        # Cargar en hilo separado
        def load():
            self.games = self.db.get_games_by_runner(self.current_runner)
            self.root.after(0, self.display_games)
        
        threading.Thread(target=load, daemon=True).start()
    
    def display_games(self):
        """Muestra los juegos en la interfaz"""
        # Limpiar el frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.games:
            ttk.Label(self.scrollable_frame, 
                     text="❌ No hay juegos instalados para esta plataforma", 
                     font=('Arial', 12)).pack(pady=50)
            self.status_bar.config(text="Sin juegos")
            return
        
        self.status_bar.config(text=f"✓ {len(self.games)} juegos encontrados")
        
        # Crear una fila por cada juego
        for game in self.games:
            self.create_game_row(game)
    
    def create_game_row(self, game):
        """Crea una fila con la información de un juego"""
        # Frame principal de la fila
        row_frame = ttk.Frame(self.scrollable_frame, relief=tk.RAISED, borderwidth=1)
        row_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame izquierdo con nombre
        info_frame = ttk.Frame(row_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(info_frame, text=game['name'], 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Slug: {game['slug']}", 
                 font=('Arial', 9), foreground='gray').pack(anchor=tk.W)
        
        # Frame derecho con las imágenes
        images_frame = ttk.Frame(row_frame)
        images_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Cover
        cover_frame = self.create_image_preview(images_frame, game, 'cover')
        cover_frame.pack(side=tk.LEFT, padx=5)
        
        # Banner
        banner_frame = self.create_image_preview(images_frame, game, 'banner')
        banner_frame.pack(side=tk.LEFT, padx=5)
        
        # Icon
        icon_frame = self.create_image_preview(images_frame, game, 'icon')
        icon_frame.pack(side=tk.LEFT, padx=5)
    
    def create_image_preview(self, parent, game, image_type):
        """Crea un preview de una imagen con botón para cambiar"""
        frame = ttk.Frame(parent)
        
        # Determinar tamaños
        if image_type == 'cover':
            thumb_size = (config.THUMBNAIL_WIDTH, config.THUMBNAIL_HEIGHT)
            label_text = "📦 Cover"
        elif image_type == 'banner':
            thumb_size = (config.BANNER_THUMBNAIL_WIDTH, config.BANNER_THUMBNAIL_HEIGHT)
            label_text = "🖼️ Banner"
        else:  # icon
            thumb_size = (config.ICON_THUMBNAIL_SIZE, config.ICON_THUMBNAIL_SIZE)
            label_text = "🎮 Icono"
        
        ttk.Label(frame, text=label_text, font=('Arial', 9)).pack()
        
        # Intentar cargar la imagen
        pil_img = self.image_manager.get_thumbnail(game['slug'], image_type, thumb_size)
        
        if pil_img:
            photo = ImageTk.PhotoImage(pil_img)
            img_label = tk.Label(frame, image=photo, relief=tk.SOLID, borderwidth=1)
            img_label.image = photo  # Mantener referencia
            img_label.pack(pady=2)
        else:
            # Placeholder si no existe
            placeholder = tk.Label(frame, text="Sin imagen", 
                                  width=15, height=8 if image_type == 'cover' else 4,
                                  relief=tk.SOLID, borderwidth=1, bg='#ddd')
            placeholder.pack(pady=2)
        
        # Botón para cambiar
        ttk.Button(frame, text="Cambiar", 
                  command=lambda: self.open_selector(game, image_type)).pack(pady=2)
        
        return frame
    
    def open_selector(self, game, image_type):
        """Abre la ventana de selección de imágenes"""
        self.status_bar.config(text=f"Buscando {game['name']} en SteamGridDB...")
        
        # Buscar el juego en SGDB
        result = self.api.search_game(game['name'])
        
        if result:
            self.status_bar.config(text=f"✓ Encontrado: {result['name']}")
            # Abrir ventana de selección
            SelectorWindow(self.root, result['name'], result['id'], 
                          game['slug'], self.current_runner, image_type,
                          self.on_image_selected)
        else:
            messagebox.showerror("Error", 
                               f"No se encontró '{game['name']}' en SteamGridDB.\n"
                               "Intenta renombrar el juego en Lutris.")
            self.status_bar.config(text="❌ Juego no encontrado")
    
    def on_image_selected(self, slug, image_type, url):
        """Callback cuando se selecciona una imagen"""
        self.status_bar.config(text=f"Descargando {image_type}...")
        
        # Reemplazar la imagen en un hilo separado
        def replace():
            success = self.image_manager.replace_image(slug, image_type, url)
            
            if success:
                # Actualizar la DB
                game = next((g for g in self.games if g['slug'] == slug), None)
                if game:
                    self.db.update_game_images(game['id'], game['name'])
                
                self.root.after(0, lambda: self.on_replace_success(image_type))
            else:
                self.root.after(0, lambda: self.on_replace_error(image_type))
        
        threading.Thread(target=replace, daemon=True).start()
    
    def on_replace_success(self, image_type):
        """Maneja el éxito al reemplazar una imagen"""
        self.status_bar.config(text=f"✓ {image_type.capitalize()} actualizado")
        messagebox.showinfo("Éxito", 
                          f"{image_type.capitalize()} actualizado correctamente.\n"
                          "Reinicia Lutris para ver los cambios.")
        # Refrescar la lista
        self.refresh_games()
    
    def on_replace_error(self, image_type):
        """Maneja el error al reemplazar una imagen"""
        self.status_bar.config(text=f"❌ Error actualizando {image_type}")
        messagebox.showerror("Error", 
                           f"No se pudo actualizar el {image_type}.\n"
                           "Verifica tu conexión a internet.")
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()
