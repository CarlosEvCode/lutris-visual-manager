"""
Módulo para interactuar con la API de SteamGridDB
"""
import urllib.request
import urllib.parse
import json
import ssl
from typing import List, Dict, Optional
import config

# SSL Bypass
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class SteamGridDBAPI:
    def __init__(self):
        self.api_key = config.STEAMGRIDDB_API_KEY
        self.base_url = "https://www.steamgriddb.com/api/v2"
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
    
    def search_game(self, query: str) -> Optional[Dict]:
        """Busca un juego en SteamGridDB"""
        url = f"{self.base_url}/search/autocomplete/{urllib.parse.quote(query)}"
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                if data.get('success') and data.get('data'):
                    # Retorna el primer resultado
                    return {
                        'id': data['data'][0]['id'],
                        'name': data['data'][0]['name']
                    }
        except Exception as e:
            print(f"Error buscando juego: {e}")
        return None
    
    def get_images(self, game_id: int, image_type: str, runner: str = None, limit: int = 12) -> List[Dict]:
        """
        Obtiene una lista de imágenes de un juego
        
        Args:
            game_id: ID del juego en SteamGridDB
            image_type: 'cover', 'banner' o 'icon'
            runner: Runner del juego (para aplicar filtros Skip Notices)
            limit: Cantidad máxima de resultados
        """
        # Determinar el endpoint según el tipo
        endpoint_map = {
            'cover': '/grids/game/',
            'banner': '/heroes/game/',
            'icon': '/icons/game/'
        }
        
        if image_type not in endpoint_map:
            return []
        
        endpoint = endpoint_map[image_type]
        
        # Construir la URL con parámetros
        params = []
        if image_type == 'cover':
            params.append('dimensions=600x900')
            params.append('styles=alternate,material')
        params.append('sort=score')  # Ordenar por puntuación
        
        url = f"{self.base_url}{endpoint}{game_id}"
        if params:
            url += '?' + '&'.join(params)
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                
                if data.get('success') and data.get('data'):
                    images = []
                    
                    # Aplicar filtro Skip Notices para juegos de Nintendo
                    start_index = 0
                    if runner in config.NINTENDO_RUNNERS:
                        skip_count = config.SKIP_COUNT.get(image_type, 0)
                        start_index = skip_count
                    
                    # Tomar imágenes desde el índice calculado
                    for img in data['data'][start_index:start_index + limit]:
                        images.append({
                            'id': img['id'],
                            'url': img['url'],
                            'thumb': img.get('thumb', img['url'])
                        })
                    
                    return images
        except Exception as e:
            print(f"Error obteniendo imágenes: {e}")
        
        return []
    
    def get_all_images(self, game_id: int, runner: str = None) -> Dict[str, List]:
        """
        Obtiene todas las imágenes (covers, banners, icons) de un juego
        
        Returns:
            Dict con keys 'covers', 'banners', 'icons'
        """
        return {
            'covers': self.get_images(game_id, 'cover', runner),
            'banners': self.get_images(game_id, 'banner', runner),
            'icons': self.get_images(game_id, 'icon', runner)
        }
