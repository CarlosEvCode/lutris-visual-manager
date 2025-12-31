"""
Módulo para gestionar imágenes: descarga, conversión y reemplazo
"""
import os
import urllib.request
import shutil
import ssl
from io import BytesIO
from PIL import Image
from typing import Optional
import config

# SSL Bypass
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class ImageManager:
    def __init__(self):
        self.covers_dir = config.COVERS_DIR
        self.banners_dir = config.BANNERS_DIR
        self.icons_lutris_dir = config.LUTRIS_ICONS_DIR
        self.icons_system_dir = config.SYSTEM_ICONS_DIR
        
        # Crear directorios si no existen
        for directory in [self.covers_dir, self.banners_dir, 
                         self.icons_lutris_dir, self.icons_system_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def get_image_paths(self, slug: str) -> dict:
        """Obtiene las rutas de las imágenes de un juego"""
        return {
            'cover': os.path.join(self.covers_dir, f"{slug}.jpg"),
            'banner': os.path.join(self.banners_dir, f"{slug}.jpg"),
            'icon_lutris': os.path.join(self.icons_lutris_dir, f"{slug}.png"),
            'icon_system': os.path.join(self.icons_system_dir, f"lutris_{slug}.png")
        }
    
    def image_exists(self, slug: str, image_type: str) -> bool:
        """Verifica si una imagen existe"""
        paths = self.get_image_paths(slug)
        if image_type == 'cover':
            return os.path.exists(paths['cover'])
        elif image_type == 'banner':
            return os.path.exists(paths['banner'])
        elif image_type == 'icon':
            return os.path.exists(paths['icon_system'])
        return False
    
    def download_image(self, url: str, save_path: str) -> bool:
        """Descarga una imagen desde una URL"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as r:
                with open(save_path, 'wb') as f:
                    f.write(r.read())
            return True
        except Exception as e:
            print(f"Error descargando imagen: {e}")
            return False
    
    def download_and_convert_icon(self, url: str, save_path: str) -> bool:
        """Descarga y convierte un icono a PNG real usando Pillow"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response:
                img_data = response.read()
                image = Image.open(BytesIO(img_data))
                image.save(save_path, "PNG")
            return True
        except Exception as e:
            print(f"Error convirtiendo icono: {e}")
            return False
    
    def replace_image(self, slug: str, image_type: str, url: str) -> bool:
        """
        Reemplaza una imagen del juego descargando desde URL
        
        Args:
            slug: Identificador del juego
            image_type: 'cover', 'banner' o 'icon'
            url: URL de la imagen a descargar
        
        Returns:
            True si se reemplazó exitosamente
        """
        paths = self.get_image_paths(slug)
        
        try:
            if image_type == 'cover':
                # Eliminar la anterior si existe
                if os.path.exists(paths['cover']):
                    os.remove(paths['cover'])
                return self.download_image(url, paths['cover'])
            
            elif image_type == 'banner':
                # Eliminar la anterior si existe
                if os.path.exists(paths['banner']):
                    os.remove(paths['banner'])
                return self.download_image(url, paths['banner'])
            
            elif image_type == 'icon':
                # Eliminar los anteriores si existen
                if os.path.exists(paths['icon_lutris']):
                    os.remove(paths['icon_lutris'])
                if os.path.exists(paths['icon_system']):
                    os.remove(paths['icon_system'])
                
                # Descargar y convertir a PNG
                if self.download_and_convert_icon(url, paths['icon_lutris']):
                    # Copiar al directorio del sistema
                    shutil.copy2(paths['icon_lutris'], paths['icon_system'])
                    return True
                return False
        
        except Exception as e:
            print(f"Error reemplazando imagen: {e}")
            return False
    
    def get_thumbnail(self, slug: str, image_type: str, size: tuple) -> Optional[Image.Image]:
        """
        Obtiene una miniatura de una imagen existente
        
        Args:
            slug: Identificador del juego
            image_type: 'cover', 'banner' o 'icon'
            size: Tupla (width, height) del tamaño deseado
        
        Returns:
            Objeto PIL Image redimensionado o None
        """
        paths = self.get_image_paths(slug)
        
        try:
            if image_type == 'cover' and os.path.exists(paths['cover']):
                img = Image.open(paths['cover'])
            elif image_type == 'banner' and os.path.exists(paths['banner']):
                img = Image.open(paths['banner'])
            elif image_type == 'icon' and os.path.exists(paths['icon_lutris']):
                img = Image.open(paths['icon_lutris'])
            else:
                return None
            
            # Redimensionar manteniendo proporción
            img.thumbnail(size, Image.Resampling.LANCZOS)
            return img
        
        except Exception as e:
            print(f"Error obteniendo miniatura: {e}")
            return None
    
    def download_thumbnail(self, url: str, size: tuple) -> Optional[Image.Image]:
        """Descarga y redimensiona una imagen desde URL (para previews)"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response:
                img_data = response.read()
                img = Image.open(BytesIO(img_data))
                img.thumbnail(size, Image.Resampling.LANCZOS)
                return img
        except Exception as e:
            print(f"Error descargando miniatura: {e}")
            return None
