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
import random
import time
import urllib.error

# SSL Bypass
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Lista de User-Agents para rotación (Bypass WAF/Fortinet)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

class SteamGridDBAPI:
    def __init__(self):
        self.api_key = config.STEAMGRIDDB_API_KEY
        self.base_url = "https://www.steamgriddb.com/api/v2"
        # Authorization header se mantiene, User-Agent se rota dinámicamente
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
    
    def _make_request(self, url_or_request, retry_count=3):
        """
        Realiza una petición HTTP robusta con:
        - Rotación de User-Agent
        - Manejo de Rate Limiting (429) y errores 403
        - Reintentos exponenciales
        """
        req = url_or_request
        if isinstance(req, str):
            req = urllib.request.Request(req)
        
        # Rotar User-Agent
        ua = random.choice(USER_AGENTS)
        req.add_header('User-Agent', ua)
        # Asegurar Authorization (si no está ya en los headers del objeto Request)
        if not req.has_header('Authorization'):
            req.add_header('Authorization', f'Bearer {self.api_key}')
        
        delay = 1
        for attempt in range(retry_count + 1):
            try:
                # Pequeño delay global (jitter) para evitar patrones de bot
                time.sleep(0.5 + random.random() * 0.5)
                
                return urllib.request.urlopen(req, context=ctx, timeout=30)
            
            except urllib.error.HTTPError as e:
                print(f"DEBUG: HTTP Error {e.code} for {req.full_url}")
                if e.code == 429: # Rate Limit
                    wait_time = delay * (2 ** attempt)
                    print(f"⚠️ Rate limit (429). Esperando {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                elif e.code == 403: # Forbidden
                    print(f"❌ Error 403 Forbidden. Intento {attempt+1}/{retry_count+1}")
                    if attempt < retry_count:
                        time.sleep(delay * 2)
                        continue
                    else:
                        print("   Posible bloqueo de seguridad (WAF/Fortinet).")
                        raise e
                elif e.code in [500, 502, 503, 504]: # Server Error
                    time.sleep(delay)
                    continue
                else:
                    raise e
            except Exception as e:
                print(f"⚠️ Error de conexión: {e}")
                if attempt < retry_count:
                    time.sleep(delay)
                    continue
                raise e
        raise Exception("Max retries exceeded")
    
    def search_game(self, query: str) -> Optional[Dict]:
        """Busca un juego en SteamGridDB"""
        url = f"{self.base_url}/search/autocomplete/{urllib.parse.quote(query)}"
        try:
            req = urllib.request.Request(url) # Headers se añaden en _make_request
            with self._make_request(req) as r:
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
            req = urllib.request.Request(url) # Headers se añaden en _make_request
            with self._make_request(req) as r:
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
