"""
Diálogos personalizados con tema Material Design
"""
import customtkinter as ctk
from ui import theme


class CustomDialog:
    """Diálogo personalizado con tema moderno"""
    
    def __init__(self, parent, title, message, dialog_type="info", buttons=None):
        """
        Crea un diálogo personalizado
        
        Args:
            parent: Ventana padre
            title: Título del diálogo
            message: Mensaje a mostrar
            dialog_type: 'info', 'success', 'warning', 'error', 'question'
            buttons: Lista de tuplas (texto, callback) o None para botón OK por defecto
        """
        self.result = None
        
        # Crear ventana
        self.window = ctk.CTkToplevel(parent)
        self.window.title(title)
        self.window.geometry("450x250")
        self.window.configure(fg_color=theme.PRIMARY_BG)
        self.window.resizable(False, False)
        
        # Hacer modal (después de hacer visible)
        self.window.transient(parent)
        
        # Centrar ventana
        self.center_window(parent)
        
        # Determinar icono y color según tipo
        icons = {
            'info': (theme.ICONS['info'], theme.INFO),
            'success': (theme.ICONS['success'], theme.SUCCESS),
            'warning': (theme.ICONS['warning'], theme.WARNING),
            'error': (theme.ICONS['error'], theme.ERROR),
            'question': ('❓', theme.ACCENT_BLUE)
        }
        
        icon, color = icons.get(dialog_type, icons['info'])
        
        self.setup_ui(icon, color, title, message, buttons)
        
        # Hacer grab después de que la ventana sea visible
        self.window.after(100, lambda: self.window.grab_set())
        
        # Esperar a que se cierre
        self.window.wait_window()
    
    def center_window(self, parent):
        """Centra la ventana sobre el padre"""
        self.window.update_idletasks()
        
        # Obtener posición y tamaño del padre
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # Calcular posición centrada
        width = 400
        height = 200
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self, icon, color, title, message, buttons):
        """Configura la interfaz del diálogo"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=theme.PADDING_L, pady=theme.PADDING_L)
        
        # Icono grande
        icon_label = ctk.CTkLabel(
            main_frame,
            text=icon,
            font=("Arial", 48),
            text_color=color
        )
        icon_label.pack(pady=(theme.PADDING_M, theme.PADDING_S))
        
        # Mensaje
        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=theme.FONT_BODY,
            text_color=theme.TEXT_PRIMARY,
            wraplength=350,
            justify="center"
        )
        message_label.pack(pady=theme.PADDING_M)
        
        # Frame de botones
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=(theme.PADDING_M, 0), fill="x")
        
        # Crear botones
        if buttons is None:
            # Botón OK por defecto
            ok_btn = ctk.CTkButton(
                button_frame,
                text="Aceptar",
                **theme.get_button_colors("primary"),
                command=lambda: self.close(True),
                width=120,
                height=theme.BUTTON_HEIGHT,
                font=theme.FONT_BODY
            )
            ok_btn.pack()
        else:
            # Botones personalizados
            for i, (btn_text, btn_callback) in enumerate(buttons):
                # Primer botón (Sí) estilo primario, segundo (No) estilo secundario
                btn_style = "primary" if i == 0 else "secondary"
                btn = ctk.CTkButton(
                    button_frame,
                    text=btn_text,
                    **theme.get_button_colors(btn_style),
                    command=lambda cb=btn_callback: self.close(cb),
                    width=120,
                    height=theme.BUTTON_HEIGHT,
                    font=theme.FONT_BODY
                )
                btn.pack(side="left", padx=theme.PADDING_S, expand=True)
        
        # Enter para cerrar
        self.window.bind("<Return>", lambda e: self.close(True))
        self.window.bind("<Escape>", lambda e: self.close(False))
    
    def close(self, result):
        """Cierra el diálogo con un resultado"""
        self.result = result
        self.window.grab_release()
        self.window.destroy()


def show_info(parent, title, message):
    """Muestra un diálogo informativo"""
    dialog = CustomDialog(parent, title, message, "info")
    return dialog.result


def show_success(parent, title, message):
    """Muestra un diálogo de éxito"""
    dialog = CustomDialog(parent, title, message, "success")
    return dialog.result


def show_warning(parent, title, message):
    """Muestra un diálogo de advertencia"""
    dialog = CustomDialog(parent, title, message, "warning")
    return dialog.result


def show_error(parent, title, message):
    """Muestra un diálogo de error"""
    dialog = CustomDialog(parent, title, message, "error")
    return dialog.result


def show_question(parent, title, message):
    """Muestra un diálogo de pregunta con botones Sí/No"""
    buttons = [
        ("Sí", True),
        ("No", False)
    ]
    dialog = CustomDialog(parent, title, message, "question", buttons)
    return dialog.result
