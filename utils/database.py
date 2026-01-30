"""
Módulo para interactuar con la base de datos de Lutris
"""
import sqlite3
from typing import List, Dict, Optional
import config

class LutrisDatabase:
    def __init__(self):
        self.db_path = config.DB_PATH
        
    def _connect(self):
        """Crea una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def get_runners(self) -> List[str]:
        """Obtiene la lista de runners únicos que tienen juegos instalados"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT runner 
            FROM games 
            WHERE installed = 1 AND runner IS NOT NULL
            ORDER BY runner
        """)
        runners = [row[0] for row in cursor.fetchall()]
        conn.close()
        return runners
    
    def get_games_by_runner(self, runner: str) -> List[Dict]:
        """Obtiene todos los juegos de un runner específico"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, slug, name, platform, configpath,
                   has_custom_coverart_big, has_custom_banner, has_custom_icon
            FROM games 
            WHERE runner = ? AND installed = 1
            ORDER BY name
        """, (runner,))
        
        games = []
        for row in cursor.fetchall():
            games.append({
                'id': row[0],
                'slug': row[1],
                'name': row[2],
                'platform': row[3],
                'configpath': row[4],
                'has_cover': bool(row[5]),
                'has_banner': bool(row[6]),
                'has_icon': bool(row[7])
            })
        
        conn.close()
        return games
    
    def update_game_images(self, game_id: int, game_name: str):
        """Actualiza los flags de imágenes personalizadas de un juego"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE games
            SET has_custom_banner=1, 
                has_custom_icon=1, 
                has_custom_coverart_big=1,
                name=?,
                sortname=?
            WHERE id=?
        """, (game_name, game_name, game_id))
        conn.commit()
        conn.close()
    
    def update_game_name(self, game_id: int, new_name: str):
        """Actualiza solo el nombre y sortname de un juego (corrección de metadatos)"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE games
            SET name=?,
                sortname=?
            WHERE id=?
        """, (new_name, new_name, game_id))
        conn.commit()
        conn.close()

    def get_game_by_id(self, game_id: int) -> Optional[Dict]:
        """Obtiene un juego específico por su ID"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, slug, name, runner, platform
            FROM games 
            WHERE id = ?
        """, (game_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'slug': row[1],
                'name': row[2],
                'runner': row[3],
                'platform': row[4]
            }
        return None
