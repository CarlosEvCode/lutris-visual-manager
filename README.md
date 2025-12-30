# 🎮 Lutris Visual Manager

Aplicación gráfica para gestionar visualmente las imágenes (covers, banners e iconos) de tus juegos en Lutris.

## 📋 Características

- ✅ **Visualización de imágenes actuales**: Ve los covers, banners e iconos de cada juego
- 🔄 **Cambio instantáneo**: Reemplaza imágenes con un solo clic
- 🎯 **Selector intuitivo**: Elige entre múltiples opciones de SteamGridDB
- 🛡️ **Filtro anti-DMCA**: Especialmente optimizado para juegos de Nintendo
- 🎨 **Soporte multi-plataforma**: MAME, PlayStation, Nintendo 3DS, Wii U, etc.

## 🚀 Instalación

### Requisitos

```bash
# Ubuntu/Debian/Mint
sudo apt install python3-tk

# Instalar Pillow
pip install Pillow
```

## 💻 Uso

1. **Cierra Lutris** (importante para evitar conflictos)

2. Ejecuta la aplicación:

```bash
cd proyecto_visual
python3 main.py
```

3. **Selecciona una plataforma** en el menú desplegable superior

4. **Navega por tus juegos** y verás sus imágenes actuales

5. **Haz clic en "Cambiar"** en cualquier imagen (cover, banner o icono)

6. **Selecciona una nueva imagen** de las opciones mostradas

7. **Confirma el cambio** y la imagen se reemplazará automáticamente

8. **Reinicia Lutris** para ver los cambios

## 📁 Estructura del Proyecto

```
proyecto_visual/
├── main.py              # Punto de entrada
├── config.py            # Configuración global
├── ui/
│   ├── main_window.py   # Ventana principal
│   └── selector_window.py # Selector de imágenes
└── utils/
    ├── database.py      # Interacción con Lutris DB
    ├── api.py          # API de SteamGridDB
    └── image_manager.py # Gestión de imágenes
```

## 🎯 Flujo de Uso

```
1. Seleccionar plataforma (ej: Wii U)
   ↓
2. Ver lista de juegos con sus imágenes actuales
   ↓
3. Hacer clic en "Cambiar" (cover, banner o icono)
   ↓
4. Ver opciones de SteamGridDB
   ↓
5. Seleccionar nueva imagen
   ↓
6. Confirmar → La imagen se reemplaza automáticamente
   ↓
7. Reiniciar Lutris
```

## ⚙️ Configuración

Puedes modificar `config.py` para:

- Cambiar rutas de Lutris
- Ajustar tamaños de miniaturas
- Modificar filtros anti-DMCA
- Agregar más plataformas

## 🛡️ Filtro Anti-DMCA

Para juegos de Nintendo (3DS, Wii U), el sistema automáticamente:

- Salta las primeras imágenes (suelen ser avisos DMCA)
- Ordena por puntuación
- Toma las imágenes más votadas

## ⚠️ Importante

- **Cierra Lutris** antes de hacer cambios
- Las imágenes antiguas se eliminan y reemplazan
- Se recomienda hacer un backup de:
  - `~/.local/share/lutris/coverart/`
  - `~/.local/share/lutris/banners/`
  - `~/.local/share/lutris/icons/`

## 🐛 Solución de Problemas

### "No se encuentra la base de datos de Lutris"

- Asegúrate de que Lutris esté instalado
- Verifica que existe: `~/.local/share/lutris/pga.db`

### "No se encontró el juego en SteamGridDB"

- Intenta renombrar el juego en Lutris con un nombre más reconocible
- Ejemplo: "SuperMario3DWorld" → "Super Mario 3D World"

### "Error convirtiendo icono"

- Verifica que Pillow esté instalado: `pip install Pillow`

## 📝 Licencia

Proyecto de código abierto para uso personal.

## 🙏 Créditos

- **SteamGridDB**: Por proporcionar la API de imágenes
- **Lutris**: Por ser un excelente gestor de juegos
