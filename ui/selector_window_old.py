"""
Ventana de selección de imágenes desde SteamGridDB
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
from typing import List, Dict, Callable
import config
from utils.api import SteamGridDBAPI
from utils.image_manager import ImageManager

class SelectorWindow:
    def __init__(self, parent, game_name: str, game_id: int, slug: str, 
                 runner: str, image_type: str, on_select_callback: Callable):
        """
        Ventana para seleccionar una imagen de SteamGridDB
        
        Args:
            parent: Ventana padre
            game_name: Nombre del juego
            game_id: ID del juego en SGDB
            slug: Slug del juego en Lutris
            runner: Runner del juego
            image_type: 'cover', 'banner' o 'icon'
            on_select_callback: Función a llamar cuando se seleccione una imagen
        """
        self.parent = parent
        self.game_name = game_name
        self.game_id = game_id
        self.slug = slug
        self.runner = runner
        self.image_type = image_type
        self.on_select_callback = on_select_callback
        
        self.api = SteamGridDBAPI()
        self.image_manager = ImageManager()
        
        self.images_data = []
        self.selected_url = None
        
        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title(f"Seleccionar {self.get_type_name()} - {game_name}")
        self.window.geometry("900x600")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        self.load_images()
    
    def get_type_name(self):
        """Obtiene el nombre amigable del tipo de imagen"""
        names = {'cover': 'Cover', 'banner': 'Banner', 'icon': 'Icono'}
        return names.get(self.image_type, 'Imagen')
    
    def setup_ui(self):
        """Configura la interfaz de la ventana"""
        # Frame superior con información
        info_frame = ttk.Frame(self.window, padding="10")
        info_frame.pack(fill=tk.X)
        
        ttk.Label(info_frame, text=f"🎮 {self.game_name}", 
                 font=('Arial', 14, 'bold')).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Selecciona un {self.get_type_name().lower()}:", 
                 font=('Arial', 10)).pack(anchor=tk.W)
        
        # Frame con scroll para las imágenes
        canvas_frame = ttk.Frame(self.window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg='#2b2b2b')
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Label de carga
        self.loading_label = ttk.Label(self.scrollable_frame, 
                                       text="🔄 Cargando imágenes...", 
                                       font=('Arial', 12))
        self.loading_label.pack(pady=50)
        
        # Frame de botones
        button_frame = ttk.Frame(self.window, padding="10")
        button_frame.pack(fill=tk.X)
        
        self.apply_button = ttk.Button(button_frame, text="✓ Aplicar", 
                                       command=self.apply_selection, state=tk.DISABLED)
        self.apply_button.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="✗ Cancelar", 
                  command=self.window.destroy).pack(side=tk.RIGHT)
    
    def load_images(self):
        """Carga las imágenes desde la API en un hilo separado"""
        def load():
            self.images_data = self.api.get_images(self.game_id, self.image_type, 
                                                   self.runner, limit=20)
            self.window.after(0, self.display_images)
        
        threading.Thread(target=load, daemon=True).start()
    
    def display_images(self):
        """Muestra las imágenes en una cuadrícula"""
        self.loading_label.destroy()
        
        if not self.images_data:
            ttk.Label(self.scrollable_frame, 
                     text="❌ No se encontraron imágenes", 
                     font=('Arial', 12)).pack(pady=50)
            return
        
        # Determinar tamaño de miniaturas según el tipo
        if self.image_type == 'cover':
            thumb_width, thumb_height = 200, 280
        elif self.image_type == 'banner':
            thumb_width, thumb_height = 350, 120
        else:  # icon
            thumb_width, thumb_height = 128, 128
        
        # Crear grid de imágenes
        columns = 3 if self.image_type != 'icon' else 4
        
        for idx, img_data in enumerate(self.images_data):
            row = idx // columns
            col = idx % columns
            
            frame = ttk.Frame(self.scrollable_frame, relief=tk.RAISED, borderwidth=2)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky=tk.NSEW)
            
            # Descargar miniatura en hilo separado
            self.load_thumbnail(frame, img_data, thumb_width, thumb_height, idx)
        
        # Configurar pesos de columnas
        for i in range(columns):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
    
    def load_thumbnail(self, frame, img_data, width, height, index):
        """Carga una miniatura en un hilo separado"""
        def load():
            pil_img = self.image_manager.download_thumbnail(img_data['thumb'], (width, height))
            if pil_img:
                self.window.after(0, lambda: self.show_thumbnail(frame, pil_img, img_data['url'], index))
        
        threading.Thread(target=load, daemon=True).start()
        
        # Mostrar placeholder mientras carga
        placeholder = ttk.Label(frame, text="⏳ Cargando...")
        placeholder.pack(pady=20)
    
    def show_thumbnail(self, frame, pil_img, url, index):
        """Muestra una miniatura cargada"""
        # Limpiar el frame
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Convertir a PhotoImage
        photo = ImageTk.PhotoImage(pil_img)
        
        # Crear botón con la imagen
        button = tk.Button(frame, image=photo, command=lambda: self.select_image(url, button, index),
                          relief=tk.FLAT, bg='#2b2b2b', activebackground='#3b3b3b')
        button.image = photo  # Mantener referencia
        button.pack()
        
        # Label con número
        ttk.Label(frame, text=f"Opción {index + 1}").pack()
    
    def select_image(self, url, button, index):
        """Selecciona una imagen"""
        self.selected_url = url
        self.apply_button.config(state=tk.NORMAL)
        
        # Visual feedback - destacar el seleccionado
        button.config(relief=tk.SUNKEN, bg='#4a4a4a')
        
        print(f"✓ Imagen {index + 1} seleccionada")
    
    def apply_selection(self):
        """Aplica la selección y cierra la ventana"""
        if self.selected_url:
            # Mostrar diálogo de confirmación
            if messagebox.askyesno("Confirmar", 
                                  f"¿Reemplazar el {self.get_type_name().lower()} actual?"):
                # Llamar al callback con la URL seleccionada
                self.on_select_callback(self.slug, self.image_type, self.selected_url)
                self.window.destroy()
