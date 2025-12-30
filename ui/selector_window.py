"""
Ventana de selección de imágenes desde SteamGridDB
Versión moderna con CustomTkinter y Material Design
"""
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import threading
from typing import Callable
import config
from utils.api import SteamGridDBAPI
from utils.image_manager import ImageManager
from ui import theme


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
        self.selected_card = None
        
        # Crear ventana
        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Seleccionar {self.get_type_name()} - {game_name}")
        self.window.geometry("1000x700")
        self.window.configure(fg_color=theme.PRIMARY_BG)
        
        # Hacer modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        self.load_images()
    
    def get_type_name(self):
        """Obtiene el nombre amigable del tipo de imagen"""
        names = {'cover': 'Cover', 'banner': 'Banner', 'icon': 'Icono'}
        return names.get(self.image_type, 'Imagen')
    
    def get_type_icon(self):
        """Obtiene el icono del tipo de imagen"""
        icons = {'cover': theme.ICONS['cover'], 'banner': theme.ICONS['banner'], 'icon': theme.ICONS['icon']}
        return icons.get(self.image_type, theme.ICONS['image'])
    
    def setup_ui(self):
        """Configura la interfaz de la ventana"""
        # Header
        header = ctk.CTkFrame(
            self.window,
            fg_color=theme.SECONDARY_BG,
            corner_radius=0,
            height=80
        )
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Contenido del header
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(expand=True, fill="both", padx=theme.PADDING_L)
        
        # Título del juego
        game_label = ctk.CTkLabel(
            header_content,
            text=f"{theme.ICONS['game']} {self.game_name}",
            font=theme.FONT_SUBTITLE,
            text_color=theme.TEXT_PRIMARY
        )
        game_label.pack(anchor="w", pady=(theme.PADDING_S, 0))
        
        # Subtítulo
        subtitle = ctk.CTkLabel(
            header_content,
            text=f"Selecciona un {self.get_type_name().lower()} {self.get_type_icon()}",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", pady=(theme.PADDING_XS, 0))
        
        # Área de scroll para las imágenes
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.window,
            fg_color="transparent",
            scrollbar_button_color=theme.SCROLLBAR,
            scrollbar_button_hover_color=theme.HOVER_BG
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=theme.PADDING_M, pady=theme.PADDING_M)
        
        # Habilitar scroll con ruedita del mouse
        self.enable_mousewheel_scroll(self.scrollable_frame)
        
        # Label de carga
        self.loading_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="transparent"
        )
        self.loading_frame.pack(expand=True, fill="both")
        
        loading_icon = ctk.CTkLabel(
            self.loading_frame,
            text=theme.ICONS['refresh'],
            font=("Arial", 64),
            text_color=theme.ACCENT_BLUE
        )
        loading_icon.pack(pady=(150, theme.PADDING_M))
        
        self.loading_label = ctk.CTkLabel(
            self.loading_frame,
            text="Cargando imágenes...",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_SECONDARY
        )
        self.loading_label.pack()
        
        # Footer con botones
        footer = ctk.CTkFrame(
            self.window,
            fg_color=theme.SECONDARY_BG,
            corner_radius=0,
            height=70
        )
        footer.pack(fill="x")
        footer.pack_propagate(False)
        
        button_container = ctk.CTkFrame(footer, fg_color="transparent")
        button_container.pack(expand=True, fill="both", padx=theme.PADDING_L, pady=theme.PADDING_M)
        
        # Botón cancelar
        cancel_btn = ctk.CTkButton(
            button_container,
            text=f"{theme.ICONS['close']} Cancelar",
            **theme.get_button_secondary_colors(),
            command=self.window.destroy,
            width=120,
            height=theme.BUTTON_HEIGHT,
            font=theme.FONT_BODY
        )
        cancel_btn.pack(side="right", padx=theme.PADDING_XS)
        
        # Botón aplicar
        self.apply_button = ctk.CTkButton(
            button_container,
            text=f"{theme.ICONS['check']} Aplicar",
            **theme.get_button_colors(),
            command=self.apply_selection,
            state="disabled",
            width=120,
            height=theme.BUTTON_HEIGHT,
            font=theme.FONT_BODY
        )
        self.apply_button.pack(side="right", padx=theme.PADDING_XS)
        
        # Contador de imágenes
        self.image_counter = ctk.CTkLabel(
            button_container,
            text="",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_SECONDARY
        )
        self.image_counter.pack(side="left")
    
    def load_images(self):
        """Carga las imágenes desde la API en un hilo separado"""
        def load():
            self.images_data = self.api.get_images(self.game_id, self.image_type, 
                                                   self.runner, limit=20)
            self.window.after(0, self.display_images)
        
        threading.Thread(target=load, daemon=True).start()
    
    def display_images(self):
        """Muestra las imágenes en una cuadrícula moderna"""
        # Limpiar loading
        self.loading_frame.destroy()
        
        if not self.images_data:
            self.show_empty_state()
            return
        
        self.image_counter.configure(text=f"{len(self.images_data)} imágenes encontradas")
        
        # Determinar tamaño de miniaturas y columnas según el tipo
        if self.image_type == 'cover':
            thumb_width, thumb_height = 200, 280  # Proporción 2:3, más grande
            columns = 4
            card_padding = theme.PADDING_S
        elif self.image_type == 'banner':
            thumb_width, thumb_height = 400, 140  # Proporción ~3:1, más grande
            columns = 2
            card_padding = theme.PADDING_M
        else:  # icon
            thumb_width, thumb_height = 128, 128
            columns = 5
            card_padding = theme.PADDING_S
        
        # Crear contenedor con grid
        grid_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, padx=theme.PADDING_M, pady=theme.PADDING_M)
        
        # Crear grid de imágenes
        for idx, img_data in enumerate(self.images_data):
            row = idx // columns
            col = idx % columns
            
            # Card para cada imagen
            self.create_image_card(grid_container, img_data, thumb_width, thumb_height, idx, row, col, card_padding)
        
        # Configurar pesos de columnas para que se distribuyan uniformemente
        for i in range(columns):
            grid_container.grid_columnconfigure(i, weight=1, uniform="column")
    
    def create_image_card(self, parent, img_data, width, height, index, row, col, padding):
        """Crea una card para cada imagen con efecto hover"""
        # Frame de la card con tamaño fijo
        card = ctk.CTkFrame(
            parent,
            fg_color=theme.CARD_BG,
            corner_radius=theme.RADIUS_M,
            border_width=2,
            border_color=theme.BORDER,
            width=width + (padding * 4),
            height=height + 60  # Espacio extra para el badge y padding
        )
        card.grid(row=row, column=col, padx=padding, pady=padding, sticky="n")
        card.grid_propagate(False)  # Evitar que se redimensione
        
        # Frame interno para centrar contenido
        inner_frame = ctk.CTkFrame(card, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=padding, pady=padding)
        
        # Badge de índice en la parte superior
        badge_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", height=30)
        badge_frame.pack(fill="x", pady=(0, theme.PADDING_XS))
        
        badge = ctk.CTkLabel(
            badge_frame,
            text=f"#{index + 1}",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_PRIMARY,
            fg_color=theme.ACCENT_BLUE,
            corner_radius=12,
            width=40,
            height=24
        )
        badge.pack(side="left")
        
        # Contenedor para la imagen (centrado)
        img_frame = ctk.CTkFrame(
            inner_frame,
            fg_color=theme.SECONDARY_BG,
            corner_radius=theme.RADIUS_S,
            width=width,
            height=height
        )
        img_frame.pack(expand=True)
        img_frame.pack_propagate(False)
        
        # Placeholder mientras carga
        placeholder = ctk.CTkLabel(
            img_frame,
            text=theme.ICONS['download'],
            font=("Arial", 32),
            text_color=theme.TEXT_DISABLED
        )
        placeholder.place(relx=0.5, rely=0.5, anchor="center")
        
        # Hacer la card completamente clickeable
        def on_click(event=None):
            self.select_image(img_data['url'], card, index)
            return "break"  # Evitar propagación
        
        # Bind a todos los widgets para mejor experiencia
        for widget in [card, inner_frame, img_frame, badge_frame, badge, placeholder]:
            widget.bind("<Button-1>", on_click)
            widget.configure(cursor="hand2")
        
        # Efectos hover - aplicar a todos los widgets
        def on_enter(event):
            if card != self.selected_card:
                card.configure(border_color=theme.BORDER_HOVER, fg_color=theme.TERTIARY_BG)
        
        def on_leave(event):
            if card != self.selected_card:
                card.configure(border_color=theme.BORDER, fg_color=theme.CARD_BG)
        
        # Bind hover a todos los widgets para mejor experiencia
        for widget in [card, inner_frame, img_frame, badge_frame, badge, placeholder]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        # Cargar miniatura en hilo separado
        def load_thumb():
            try:
                thumb = self.image_manager.download_thumbnail(img_data['thumb'], (width, height))
                if thumb:
                    # Usar CTkImage para compatibilidad
                    ctk_image = ctk.CTkImage(light_image=thumb, dark_image=thumb, size=(width, height))
                    self.window.after(0, lambda: self.update_thumbnail(placeholder, ctk_image, img_frame))
            except Exception as e:
                print(f"Error cargando miniatura: {e}")
        
        threading.Thread(target=load_thumb, daemon=True).start()
    
    def update_thumbnail(self, placeholder, ctk_image, img_frame):
        """Actualiza el placeholder con la imagen cargada"""
        try:
            placeholder.configure(image=ctk_image, text="")
            # Guardar referencia en el frame de imagen
            img_frame.ctk_image = ctk_image
        except:
            pass
    
    def show_empty_state(self):
        """Muestra un estado vacío cuando no hay imágenes"""
        empty_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="transparent"
        )
        empty_frame.pack(expand=True, fill="both")
        
        icon = ctk.CTkLabel(
            empty_frame,
            text=theme.ICONS['error'],
            font=("Arial", 64),
            text_color=theme.ERROR
        )
        icon.pack(pady=(150, theme.PADDING_M))
        
        message = ctk.CTkLabel(
            empty_frame,
            text=f"No se encontraron {self.get_type_name().lower()}s para este juego",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_SECONDARY
        )
        message.pack()
        
        self.image_counter.configure(text="0 imágenes")
    
    def select_image(self, url, card, index):
        """Maneja la selección de una imagen"""
        # Deseleccionar anterior
        if self.selected_card:
            self.selected_card.configure(
                border_color=theme.BORDER,
                fg_color=theme.CARD_BG,
                border_width=2
            )
        
        # Seleccionar nueva
        card.configure(
            border_color=theme.ACCENT_BLUE,
            fg_color=theme.TERTIARY_BG,
            border_width=3
        )
        self.selected_card = card
        self.selected_url = url
        
        # Habilitar botón aplicar
        self.apply_button.configure(state="normal")
        
        # Actualizar contador
        self.image_counter.configure(
            text=f"{theme.ICONS['check']} Imagen #{index + 1} seleccionada",
            text_color=theme.SUCCESS
        )
    
    def enable_mousewheel_scroll(self, widget):
        """Habilita el scroll con la ruedita del mouse"""
        def _on_mousewheel(event):
            try:
                widget._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        def _on_scroll_up(event):
            try:
                widget._parent_canvas.yview_scroll(-1, "units")
            except:
                pass
        
        def _on_scroll_down(event):
            try:
                widget._parent_canvas.yview_scroll(1, "units")
            except:
                pass
        
        # Guardar referencias para poder desvincular después
        self._mousewheel_binding = _on_mousewheel
        self._scroll_up_binding = _on_scroll_up
        self._scroll_down_binding = _on_scroll_down
        
        # Bind del evento mousewheel solo a esta ventana
        self.window.bind("<MouseWheel>", _on_mousewheel)
        self.window.bind("<Button-4>", _on_scroll_up)
        self.window.bind("<Button-5>", _on_scroll_down)
        
        # Desvincular al cerrar la ventana
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Limpia los bindings antes de cerrar la ventana"""
        try:
            # Desvincular eventos
            self.window.unbind("<MouseWheel>")
            self.window.unbind("<Button-4>")
            self.window.unbind("<Button-5>")
        except:
            pass
        
        self.window.destroy()
    
    def apply_selection(self):
        """Aplica la selección y cierra la ventana"""
        if self.selected_url:
            self.on_select_callback(self.slug, self.image_type, self.selected_url)
            self.on_closing()
