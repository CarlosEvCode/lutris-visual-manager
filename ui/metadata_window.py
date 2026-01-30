"""
Ventana para corregir metadatos (nombre del juego)
"""
import customtkinter as ctk
import threading
from ui import theme, dialogs
from utils.api import SteamGridDBAPI

class MetadataWindow(ctk.CTkToplevel):
    def __init__(self, parent, game_data, db, callback):
        super().__init__(parent)
        self.game_data = game_data
        self.db = db
        self.callback = callback
        self.api = SteamGridDBAPI()
        
        self.title("Corregir Metadatos")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Aplicar tema
        self.configure(fg_color=theme.PRIMARY_BG)
        
        # Iniciar carga de UI con pequeño delay para asegurar renderizado en X11
        self.after(100, self.show_ui)

    def show_ui(self):
        """Muestra la UI y toma control de la ventana"""
        self.setup_ui()
        self.center_window()
        
        # Hacer modal y traer al frente
        self.transient(self.master)
        self.lift()
        self.focus_force()
        try:
            self.grab_set()
        except:
            pass
        


        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=theme.PADDING_L, pady=theme.PADDING_M)
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Corregir Nombre del Juego",
            font=theme.FONT_HEADING,
            text_color=theme.TEXT_PRIMARY
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text=f"Actual: {self.game_data['name']}",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_SECONDARY
        )
        subtitle.pack(anchor="w")

        # Search Bar
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=theme.PADDING_L, pady=theme.PADDING_S)

        self.entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar nombre correcto...",
            height=theme.INPUT_HEIGHT,
            font=theme.FONT_BODY
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, theme.PADDING_S))
        self.entry.bind("<Return>", lambda e: self.search())
        self.entry.insert(0, self.game_data['name'])

        search_btn = ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search,
            width=100,
            height=theme.INPUT_HEIGHT,
            **theme.get_button_colors()
        )
        search_btn.pack(side="right")

        # Results Area
        self.scrollable = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            label_text="Resultados de SteamGridDB"
        )
        self.scrollable.pack(fill="both", expand=True, padx=theme.PADDING_L, pady=theme.PADDING_M)

        # Status Bar
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_SECONDARY
        )
        self.status_label.pack(pady=theme.PADDING_S)

    def search(self):
        query = self.entry.get().strip()
        if not query:
            return

        # Clear existing
        for widget in self.scrollable.winfo_children():
            widget.destroy()

        self.status_label.configure(text="Buscando...", text_color=theme.TEXT_PRIMARY)
        
        def run_search():
            results = self.api.search_game(query) # This returns a single dict or None currently
            # Wait, api.search_game returns ONE result? 
            # Let's check api.py. It uses /search/autocomplete and returns dict {'id':..., 'name':...}
            # We might want a method that returns a LIST of candidates if possible.
            # But based on current api.py, we only have search_game returning one.
            # Let's check api.py again or assume we can implemented search_candidates if needed.
            # actually, /search/autocomplete returns a list of data. 
            # The current implementation in api.py takes data['data'][0]. 
            # I should PROBABLY update api.py to get a list if I want a proper selector.
            # For now, let's stick to what we have or quickly add `search_games` to api.py returning list.
            
            # Re-checking api.py logic seen previously...
            # search_game returns Optional[Dict] (the first match).
            
            # To do this properly, I should add `search_games` (plural) to api.py.
            # But to avoid scope creep, I will stick to what exists OR modify api.py quickly.
            # Modifying api.py is better for UX.
            
            # Let's try to misuse search_game for now? No, that's bad.
            # I will modify api.py in the next step to return list.
            # For this file content, I will assume `api.search_games(query)` exists.
            
            pass 

        # Since I can't effectively write the logic without the API change, 
        # I will write the component assuming `api.search_games` returns a list of dicts.
        # And I will update api.py in the next tool call.
        
        threading.Thread(target=self._perform_search, args=(query,), daemon=True).start()

    def _perform_search(self, query):
        # We need a method that returns list. 
        # I will implement `search_games` in api.py
        try:
            results = self.api.search_games(query) 
            self.after(0, lambda: self.show_results(results))
        except Exception as e:
            self.after(0, lambda: self.show_error(str(e)))

    def show_results(self, results):
        self.status_label.configure(text=f"Encontrados {len(results)} resultados")
        
        if not results:
             lbl = ctk.CTkLabel(self.scrollable, text="No se encontraron resultados")
             lbl.pack(pady=20)
             return

        for game in results:
            self.create_result_card(game)

    def create_result_card(self, game):
        card = ctk.CTkFrame(self.scrollable, fg_color=theme.SECONDARY_BG)
        card.pack(fill="x", pady=5)
        
        # Title
        lbl = ctk.CTkLabel(
            card, 
            text=game['name'], 
            font=theme.FONT_BODY_BOLD
        )
        lbl.pack(side="left", padx=10, pady=10)
        
        # ID
        id_lbl = ctk.CTkLabel(
            card,
            text=f"ID: {game['id']}",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_SECONDARY
        )
        id_lbl.pack(side="left", padx=10)

        # Select Button
        btn = ctk.CTkButton(
            card,
            text="Seleccionar",
            width=80,
            height=24,
            command=lambda: self.select_game(game)
        )
        btn.pack(side="right", padx=10, pady=10)

    def select_game(self, game):
        # Update DB
        try:
            self.db.update_game_name(self.game_data['id'], game['name'])
            
            # Call callback to refresh UI, passing the new SGDB ID
            if self.callback:
                self.callback(game['id'])
                
            self.destroy()
            
        except Exception as e:
            dialogs.show_error(self, "Error", str(e))

    def show_error(self, msg):
        self.status_label.configure(text="Error buscando juegos", text_color=theme.WARNING)
        print(msg)
