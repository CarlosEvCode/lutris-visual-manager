"""
Gestor de configuración persistente para Lutris Visual Manager
Guarda la configuración del usuario en ~/.config/lutris-visual-manager/
"""
import os
import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        # Directorio de configuración siguiendo el estándar XDG
        self.config_dir = Path.home() / ".config" / "lutris-visual-manager"
        self.config_file = self.config_dir / "config.json"
        
        # Crear directorio si no existe
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar configuración
        self.config = self._load_config()
    
    def _load_config(self):
        """Carga la configuración desde el archivo"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error al cargar configuración: {e}")
                return {}
        return {}
    
    def _save_config(self):
        """Guarda la configuración en el archivo"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            # Establecer permisos restrictivos (solo el usuario puede leer/escribir)
            os.chmod(self.config_file, 0o600)
            return True
        except Exception as e:
            print(f"❌ Error al guardar configuración: {e}")
            return False
    
    def get_api_key(self):
        """Obtiene el API Key guardado"""
        return self.config.get('steamgriddb_api_key')
    
    def set_api_key(self, api_key):
        """Guarda el API Key"""
        self.config['steamgriddb_api_key'] = api_key
        return self._save_config()
    
    def clear_api_key(self):
        """Elimina el API Key guardado"""
        if 'steamgriddb_api_key' in self.config:
            del self.config['steamgriddb_api_key']
            return self._save_config()
        return True
    
    def get_last_installation_mode(self):
        """Obtiene el último modo de instalación usado"""
        return self.config.get('last_installation_mode')
    
    def set_last_installation_mode(self, mode):
        """Guarda el último modo de instalación usado"""
        self.config['last_installation_mode'] = mode
        return self._save_config()
    
    def get_window_geometry(self, window_name):
        """Obtiene la geometría guardada de una ventana"""
        geometries = self.config.get('window_geometries', {})
        return geometries.get(window_name)
    
    def set_window_geometry(self, window_name, geometry):
        """Guarda la geometría de una ventana"""
        if 'window_geometries' not in self.config:
            self.config['window_geometries'] = {}
        self.config['window_geometries'][window_name] = geometry
        return self._save_config()
    
    def get_all_config(self):
        """Retorna toda la configuración"""
        return self.config.copy()
    
    def reset_config(self):
        """Resetea toda la configuración"""
        self.config = {}
        return self._save_config()


# Instancia global del gestor de configuración
_config_manager = None

def get_config_manager():
    """Obtiene la instancia global del gestor de configuración"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
