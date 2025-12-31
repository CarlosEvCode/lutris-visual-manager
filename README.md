# 🎮 Lutris Visual Manager

Aplicación gráfica para gestionar visualmente las imágenes (covers, banners e iconos) de tus juegos en Lutris.

## 📋 Características

- ✅ **Visualización de imágenes actuales**: Ve los covers, banners e iconos de cada juego
- 🔄 **Cambio instantáneo**: Reemplaza imágenes con un solo clic
- 🎯 **Selector intuitivo**: Elige entre múltiples opciones de SteamGridDB
- 🛡️ **Skip Notices**: Omite avisos de copyright en búsqueda de imágenes
- 🎨 **Soporte multi-plataforma**: MAME, PlayStation, Nintendo 3DS, Wii U, etc.

## 🚀 Instalación

### Opción 1: Instalación Local (Recomendada)

```bash
git clone https://github.com/CarlosEvCode/lutris-visual-manager.git
cd lutris-visual-manager
./install.sh
```

Esto instalará la aplicación en `~/.local/share/lutris-visual-manager` y creará un lanzador en tu menú de aplicaciones.

### Opción 2: AppImage

Descarga el AppImage desde [Releases](https://github.com/CarlosEvCode/lutris-visual-manager/releases) y ejecútalo:

```bash
chmod +x lutris-visual-manager-x86_64.AppImage
./lutris-visual-manager-x86_64.AppImage
```

**Nota**: El AppImage se compila en Linux Mint para máxima compatibilidad. Ver [COMPILACION.md](COMPILACION.md) para detalles técnicos.

### Opción 3: Ejecutar desde Código Fuente

```bash
# Requisitos
sudo apt install python3-tk  # Ubuntu/Debian/Mint

# Instalar dependencias Python
pip install -r requirements.txt

# Ejecutar
./run.sh
```

### API Key de SteamGridDB

Esta aplicación requiere un API Key de SteamGridDB para buscar imágenes. Es **gratuito** y fácil de obtener:

1. Visita: [https://www.steamgriddb.com/profile/preferences/api](https://www.steamgriddb.com/profile/preferences/api)
2. Inicia sesión o crea una cuenta (gratis)
3. Genera un nuevo API Key
4. **Solo la primera vez**, la aplicación te pedirá el API Key

**Configuración persistente:**
- Tu API Key se guarda de forma segura en `~/.config/lutris-visual-manager/config.json`
- Solo necesitas ingresarlo una vez
- Permisos 600 (solo tú puedes leer/escribir el archivo)
- Puedes cambiar tu API Key desde el botón "Configuración" en la aplicación

**Nota de seguridad**: Cada usuario debe usar su propio API Key. No compartas tu API Key con nadie.

## 💻 Uso

1. **Cierra Lutris** (importante para evitar conflictos)

2. Ejecuta la aplicación:

```bash
cd proyecto_visual
./run.sh
# o alternativamente:
python3 main.py
```

3. **Ingresa tu API Key** de SteamGridDB (solo la primera vez)

4. **Selecciona tu tipo de instalación** de Lutris: Native o Flatpak (se recordará para la próxima vez)

5. **Selecciona una plataforma** en el menú desplegable del sidebar izquierdo

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

### Archivos de configuración

La aplicación guarda tu configuración en:
- `~/.config/lutris-visual-manager/config.json`
  - API Key de SteamGridDB
  - Último modo de instalación usado (Native/Flatpak)
  - Permisos 600 (solo tu usuario puede acceder)

### Cambiar API Key

1. Abre la aplicación
2. Click en "⚙️ Configuración" en el sidebar
3. Ingresa tu nuevo API Key

### Personalización adicional

Puedes modificar `config.py` para:

- Cambiar rutas de Lutris
- Ajustar tamaños de miniaturas
- Modificar filtros Skip Notices
- Agregar más plataformas

## 📦 Distribución

¿Quieres distribuir esta aplicación? Consulta [PACKAGING.md](PACKAGING.md) para:
- Crear AppImage
- Compilar con PyInstaller
- Empaquetar como Flatpak/Snap
- Instrucciones detalladas para cada método

## 🛡️ Skip Notices

Para juegos de Nintendo (3DS, Wii U), el sistema automáticamente:

- Salta las primeras imágenes (suelen ser avisos de copyright)
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

### "Instrucción ilegal" al ejecutar AppImage

Este error puede ocurrir en sistemas más antiguos o máquinas virtuales:

**Solución 1** - Recompilar en tu sistema:
```bash
git clone https://github.com/CarlosEvCode/lutris-visual-manager
cd lutris-visual-manager
./build_appimage.sh
```

**Solución 2** - Ejecutar desde código fuente:
```bash
git clone https://github.com/CarlosEvCode/lutris-visual-manager
cd lutris-visual-manager
pip install -r requirements.txt
./run.sh
```

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles

## 🙏 Créditos

- **SteamGridDB**: Por proporcionar la API de imágenes
- **Lutris**: Por ser un excelente gestor de juegos
