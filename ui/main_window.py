"""
Ventana principal del Lutris Visual Manager
Versión moderna con CustomTkinter y Material Design
"""
import customtkinter as ctk
from PIL import Image
import threading
import config
from utils.database import LutrisDatabase
from utils.api import SteamGridDBAPI
from utils.image_manager import ImageManager
from ui.selector_window import SelectorWindow
from ui import theme
from ui import dialogs


class MainWindow:
    def __init__(self):
        # Aplicar tema
        theme.apply_theme()
        
        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(fg_color=theme.PRIMARY_BG)
        
        # Instancias de utilidades
        self.db = LutrisDatabase()
        self.api = SteamGridDBAPI()
        self.image_manager = ImageManager()
        
        self.current_runner = None
        self.games = []
        self.runner_map = {}
        
        self.setup_ui()
        self.load_runners()
    
    def setup_ui(self):
        """Configura la interfaz principal con sidebar"""
        # Frame principal con dos columnas
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # === SIDEBAR (Izquierda) ===
        self.sidebar = ctk.CTkFrame(
            main_container,
            width=280,
            fg_color=theme.SECONDARY_BG,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        self.setup_sidebar()
        
        # === CONTENIDO PRINCIPAL (Derecha) ===
        content_frame = ctk.CTkFrame(
            main_container,
            fg_color=theme.PRIMARY_BG,
            corner_radius=0
        )
        content_frame.pack(side="right", fill="both", expand=True)
        
        self.setup_content_area(content_frame)
    
    def setup_sidebar(self):
        """Configura el sidebar con logo, selector de plataforma y acciones"""
        # Padding superior
        ctk.CTkLabel(self.sidebar, text="", height=20).pack()
        
        # Logo / Título
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=theme.PADDING_M, padx=theme.PADDING_M)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text=f"{theme.ICONS['game']}",
            font=("Arial", 48),
            text_color=theme.ACCENT_BLUE
        )
        logo_label.pack()
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="Lutris Visual\nManager",
            font=theme.FONT_SUBTITLE,
            text_color=theme.TEXT_PRIMARY,
            justify="center"
        )
        title_label.pack(pady=(theme.PADDING_S, 0))
        
        # Separador
        ctk.CTkFrame(
            self.sidebar,
            height=2,
            fg_color=theme.BORDER
        ).pack(fill="x", pady=theme.PADDING_L, padx=theme.PADDING_M)
        
        # Sección de plataforma
        platform_label = ctk.CTkLabel(
            self.sidebar,
            text=f"{theme.ICONS['platform']} Plataforma",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.TEXT_SECONDARY,
            anchor="w"
        )
        platform_label.pack(padx=theme.PADDING_M, pady=(theme.PADDING_M, theme.PADDING_S), anchor="w")
        
        # Selector de plataforma (ComboBox)
        self.runner_combo = ctk.CTkComboBox(
            self.sidebar,
            **theme.get_entry_colors(),
            command=self.on_runner_selected,
            width=240,
            height=theme.INPUT_HEIGHT,
            corner_radius=theme.RADIUS_S,
            border_width=1,
            button_color=theme.ACCENT_BLUE,
            button_hover_color=theme.ACCENT_BLUE_HOVER,
            dropdown_fg_color=theme.CARD_BG,
            dropdown_hover_color=theme.HOVER_BG,
            dropdown_text_color=theme.TEXT_PRIMARY,
            font=theme.FONT_BODY
        )
        self.runner_combo.pack(padx=theme.PADDING_M, pady=theme.PADDING_S)
        self.runner_combo.set("Selecciona una plataforma...")
        
        # Botón de refrescar
        refresh_btn = ctk.CTkButton(
            self.sidebar,
            text=f"{theme.ICONS['refresh']} Refrescar",
            **theme.get_button_secondary_colors(),
            command=self.refresh_games,
            width=240,
            height=theme.BUTTON_HEIGHT,
            corner_radius=theme.RADIUS_S,
            font=theme.FONT_BODY
        )
        refresh_btn.pack(padx=theme.PADDING_M, pady=theme.PADDING_S)
        
        # Separador
        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=theme.BORDER
        ).pack(fill="x", pady=theme.PADDING_M, padx=theme.PADDING_M)
        
        # Botón de configuración
        settings_btn = ctk.CTkButton(
            self.sidebar,
            text=f"{theme.ICONS['settings']} Configuración",
            **theme.get_button_secondary_colors(),
            command=self.show_settings,
            width=240,
            height=theme.BUTTON_HEIGHT,
            corner_radius=theme.RADIUS_S,
            font=theme.FONT_BODY
        )
        settings_btn.pack(padx=theme.PADDING_M, pady=theme.PADDING_S)
        
        # Espaciador
        ctk.CTkLabel(self.sidebar, text="", height=20).pack(expand=True)
        
        # Info en la parte inferior
        info_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color=theme.CARD_BG,
            corner_radius=theme.RADIUS_M
        )
        info_frame.pack(padx=theme.PADDING_M, pady=theme.PADDING_M, fill="x")
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=f"{theme.ICONS['info']} Cierra Lutris antes\nde hacer cambios",
            font=theme.FONT_SMALL,
            text_color=theme.INFO,
            justify="center"
        )
        info_label.pack(pady=theme.PADDING_S)
        
        # Contador de juegos
        self.games_counter = ctk.CTkLabel(
            self.sidebar,
            text="",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_SECONDARY
        )
        self.games_counter.pack(pady=theme.PADDING_S)
    
    def setup_content_area(self, parent):
        """Configura el área de contenido principal"""
        # Header
        header = ctk.CTkFrame(
            parent,
            fg_color=theme.SECONDARY_BG,
            corner_radius=0,
            height=60
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        self.header_label = ctk.CTkLabel(
            header,
            text="Selecciona una plataforma",
            font=theme.FONT_HEADING,
            text_color=theme.TEXT_PRIMARY
        )
        self.header_label.pack(side="left", padx=theme.PADDING_L, pady=theme.PADDING_M)
        
        # Área de scroll para los juegos
        scroll_frame = ctk.CTkFrame(parent, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # ScrollableFrame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            scroll_frame,
            fg_color="transparent",
            scrollbar_button_color=theme.SCROLLBAR,
            scrollbar_button_hover_color=theme.HOVER_BG
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=theme.PADDING_M, pady=theme.PADDING_M)
        
        # Habilitar scroll con ruedita del mouse
        self.enable_mousewheel_scroll(self.scrollable_frame)
        
        # Mensaje inicial
        self.show_empty_state("Selecciona una plataforma del menú lateral")
    
    def show_empty_state(self, message):
        """Muestra un estado vacío con un mensaje"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        empty_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="transparent"
        )
        empty_frame.pack(expand=True, fill="both")
        
        icon_label = ctk.CTkLabel(
            empty_frame,
            text=theme.ICONS['game'],
            font=("Arial", 64),
            text_color=theme.TEXT_DISABLED
        )
        icon_label.pack(pady=(100, theme.PADDING_M))
        
        message_label = ctk.CTkLabel(
            empty_frame,
            text=message,
            font=theme.FONT_BODY,
            text_color=theme.TEXT_SECONDARY
        )
        message_label.pack()
    
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
        
        if options:
            self.runner_combo.configure(values=options)
            self.games_counter.configure(text=f"{len(options)} plataformas")
    
    def on_runner_selected(self, choice):
        """Maneja la selección de un runner"""
        self.current_runner = self.runner_map.get(choice)
        
        if self.current_runner:
            self.header_label.configure(text=f"{theme.ICONS['platform']} {choice}")
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
        self.show_empty_state(f"{theme.ICONS['refresh']} Cargando juegos...")
        
        # Cargar en hilo separado
        def load():
            self.games = self.db.get_games_by_runner(self.current_runner)
            self.root.after(0, self.display_games)
        
        threading.Thread(target=load, daemon=True).start()
    
    def display_games(self):
        """Muestra los juegos en cards"""
        # Limpiar el frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.games:
            self.show_empty_state(f"{theme.ICONS['warning']} No hay juegos instalados")
            self.games_counter.configure(text="0 juegos")
            return
        
        self.games_counter.configure(text=f"{len(self.games)} juegos")
        
        # Crear una card por cada juego
        for game in self.games:
            self.create_game_card(game)
    
    def create_game_card(self, game):
        """Crea una card moderna para cada juego"""
        # Card principal
        card = ctk.CTkFrame(
            self.scrollable_frame,
            **theme.get_card_style()
        )
        card.pack(fill="x", pady=theme.PADDING_S, padx=theme.PADDING_S)
        
        # Frame interno con padding
        inner_frame = ctk.CTkFrame(card, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=theme.PADDING_M, pady=theme.PADDING_M)
        
        # Sección superior: Nombre del juego
        title_label = ctk.CTkLabel(
            inner_frame,
            text=game['name'],
            font=theme.FONT_HEADING,
            text_color=theme.TEXT_PRIMARY,
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, theme.PADDING_XS))
        
        slug_label = ctk.CTkLabel(
            inner_frame,
            text=f"Slug: {game['slug']}",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_SECONDARY,
            anchor="w"
        )
        slug_label.pack(anchor="w", pady=(0, theme.PADDING_M))
        
        # Separador
        ctk.CTkFrame(
            inner_frame,
            height=1,
            fg_color=theme.BORDER
        ).pack(fill="x", pady=theme.PADDING_S)
        
        # Frame para las imágenes (horizontal)
        images_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        images_frame.pack(fill="x", pady=theme.PADDING_S)
        
        # Cover, Banner, Icon
        self.create_image_section(images_frame, game, 'cover').pack(side="left", expand=True, fill="both", padx=theme.PADDING_XS)
        self.create_image_section(images_frame, game, 'banner').pack(side="left", expand=True, fill="both", padx=theme.PADDING_XS)
        self.create_image_section(images_frame, game, 'icon').pack(side="left", expand=True, fill="both", padx=theme.PADDING_XS)
    
    def create_image_section(self, parent, game, image_type):
        """Crea una sección de imagen con preview y botón"""
        # Determinar configuración según tipo
        if image_type == 'cover':
            thumb_size = (config.THUMBNAIL_WIDTH, config.THUMBNAIL_HEIGHT)
            icon = theme.ICONS['cover']
            label_text = "Cover"
        elif image_type == 'banner':
            thumb_size = (config.BANNER_THUMBNAIL_WIDTH, config.BANNER_THUMBNAIL_HEIGHT)
            icon = theme.ICONS['banner']
            label_text = "Banner"
        else:
            thumb_size = (config.ICON_THUMBNAIL_SIZE, config.ICON_THUMBNAIL_SIZE)
            icon = theme.ICONS['icon']
            label_text = "Icono"
        
        # Frame contenedor
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=theme.TERTIARY_BG,
            corner_radius=theme.RADIUS_S,
            border_width=1,
            border_color=theme.BORDER
        )
        
        # Label del tipo
        type_label = ctk.CTkLabel(
            section_frame,
            text=f"{icon} {label_text}",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_SECONDARY
        )
        type_label.pack(pady=(theme.PADDING_S, theme.PADDING_XS))
        
        # Intentar cargar la imagen
        pil_img = self.image_manager.get_thumbnail(game['slug'], image_type, thumb_size)
        
        if pil_img:
            # Usar CTkImage para compatibilidad con CustomTkinter
            ctk_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=thumb_size)
            img_label = ctk.CTkLabel(
                section_frame,
                image=ctk_image,
                text=""
            )
            img_label.pack(pady=theme.PADDING_XS)
        else:
            # Placeholder
            placeholder = ctk.CTkLabel(
                section_frame,
                text="Sin imagen",
                font=theme.FONT_SMALL,
                text_color=theme.TEXT_DISABLED,
                width=thumb_size[0],
                height=thumb_size[1],
                fg_color=theme.SECONDARY_BG,
                corner_radius=theme.RADIUS_S
            )
            placeholder.pack(pady=theme.PADDING_XS)
        
        # Botón para cambiar
        change_btn = ctk.CTkButton(
            section_frame,
            text="Cambiar",
            **theme.get_button_colors(),
            command=lambda: self.open_selector(game, image_type),
            width=100,
            height=30,
            corner_radius=theme.RADIUS_S,
            font=theme.FONT_SMALL
        )
        change_btn.pack(pady=theme.PADDING_S)
        
        return section_frame
    
    def open_selector(self, game, image_type):
        """Abre la ventana de selección de imágenes"""
        # Buscar el juego en SGDB
        result = self.api.search_game(game['name'])
        
        if result:
            # Abrir ventana de selección
            SelectorWindow(self.root, result['name'], result['id'], 
                          game['slug'], self.current_runner, image_type,
                          self.on_image_selected)
        else:
            dialogs.show_error(
                self.root,
                "Error",
                f"No se encontró '{game['name']}' en SteamGridDB.\n"
                "Intenta renombrar el juego en Lutris."
            )
    
    def on_image_selected(self, slug, image_type, url):
        """Callback cuando se selecciona una imagen"""
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
        dialogs.show_success(
            self.root,
            "Éxito",
            f"{image_type.capitalize()} actualizado correctamente.\n"
            "Reinicia Lutris para ver los cambios."
        )
        # Refrescar la lista
        self.refresh_games()
    
    def on_replace_error(self, image_type):
        """Maneja el error al reemplazar una imagen"""
        dialogs.show_error(
            self.root,
            "Error",
            f"No se pudo actualizar el {image_type}.\n"
            "Verifica tu conexión a internet."
        )
    
    def enable_mousewheel_scroll(self, widget):
        """Habilita el scroll con la ruedita del mouse"""
        def _on_mousewheel(event):
            try:
                if widget.winfo_exists():
                    widget._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        def _on_scroll_up(event):
            try:
                if widget.winfo_exists():
                    widget._parent_canvas.yview_scroll(-1, "units")
            except:
                pass
        
        def _on_scroll_down(event):
            try:
                if widget.winfo_exists():
                    widget._parent_canvas.yview_scroll(1, "units")
            except:
                pass
        
        # Bind solo cuando el mouse está sobre el área de scroll
        def on_enter(e):
            try:
                self.root.bind_all("<MouseWheel>", _on_mousewheel)
                self.root.bind_all("<Button-4>", _on_scroll_up)
                self.root.bind_all("<Button-5>", _on_scroll_down)
            except:
                pass
        
        def on_leave(e):
            try:
                self.root.unbind_all("<MouseWheel>")
                self.root.unbind_all("<Button-4>")
                self.root.unbind_all("<Button-5>")
            except:
                pass
        
        widget._parent_canvas.bind("<Enter>", on_enter)
        widget._parent_canvas.bind("<Leave>", on_leave)
    
    def show_settings(self):
        """Muestra ventana de configuración"""
        from ui.apikey_window import get_api_key
        from utils.config_manager import get_config_manager
        
        config_mgr = get_config_manager()
        current_api_key = config_mgr.get_api_key()
        
        # Solicitar nuevo API Key mostrando el actual
        new_api_key = get_api_key(show_change_option=True, current_key=current_api_key)
        
        if new_api_key and new_api_key != current_api_key:
            # Guardar nuevo API Key
            if config_mgr.set_api_key(new_api_key):
                # Actualizar en config
                config.STEAMGRIDDB_API_KEY = new_api_key
                # Reinicializar API
                self.api = SteamGridDBAPI()
                
                dialogs.show_success(
                    self.root,
                    "API Key actualizado",
                    "El API Key se ha actualizado correctamente.\nYa puedes continuar usando la aplicación."
                )
            else:
                dialogs.show_error(
                    self.root,
                    "Error",
                    "No se pudo guardar el nuevo API Key."
                )
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()
