# Guía de Estilo Visual

## 1. Paleta base
Extraída algorítmicamente (cuantización de color, 14 colores dominantes) de
`Estetica ideal.jpeg`, ordenada por peso/frecuencia en la imagen:

| Color | Hex | Uso sugerido |
|---|---|---|
| ⬛ | `#010901` | Negro base / sombras profundas |
| 🟦 | `#2B2E56` | Azul-violeta principal (arquitectura, fondos) |
| 🟥 | `#B41F1C` | **Único acento cálido** — reservar para sangre, peligro, elementos sagrados críticos |
| 🟦 | `#11222E` | Azul oscuro secundario (sombras de piedra) |
| 🟦 | `#07424F` | Verde-azulado (musgo, hielo, atmósfera) |
| 🟪 | `#3A5184` | Azul medio (luz de luna, reflejos) |
| 🟦 | `#162C3D` | Azul oscuro terciario |
| ⬛ | `#0C1A1C` | Negro-verdoso (fondo profundo) |
| 🟪 | `#766DBC` | Violeta claro (magia, brillo sobrenatural) |
| ⬛ | `#02100E` | Negro-verdoso profundo |
| ⬛ | `#041917` | Negro-azulado profundo |
| 🟪 | `#3B4272` | Azul-violeta medio |
| 🟪 | `#352037` | Violeta oscuro (transición día/noche) |
| 🟪 | `#493165` | Violeta medio (cielo, niebla) |

**Regla de acento único:** de los 14 colores, solo `#B41F1C` (rojo) rompe la gama
fría. Se reserva exclusivamente para: sangre, peligro inminente (telegrafiado de
ataques de boss), y elementos "sagrados" de Pharasma que deban resaltar. No usar
rojo decorativamente — si todo es acento, nada lo es.

**Dorado apagado (a definir en producción):** falta un tono cálido secundario para
lo "sagrado no urgente" (símbolos de Pharasma, checkpoints). Sugerido: derivar un
dorado desaturado (`#8A7040` aprox.) para que no compita visualmente con el rojo
de peligro. Ajustar con muestra real en Aseprite antes de fijarlo.

## 2. Resolución y escala de sprite
- Resolución de referencia de cámara: **1280x720**, con pixel scaling en modo
  "viewport" (ya configurado en `project.godot`).
- Tamaño base de sprite del protagonista: **32x48 px** (necesita más alto que ancho
  por la armadura completa y el escudo).
- Tile base del tileset: **16x16 px** (estándar, permite variación de detalle sin
  sprites gigantes).
- Filtro de textura: **nearest-neighbor** (ya seteado en `project.godot` —
  `default_texture_filter=0`), para evitar blur en los píxeles.

## 3. Filosofía de animación
- Pocos frames, mucho peso (referencia: Volgarr/SLAIN, no fluidez hiperrealista).
- Idle: 2-4 frames. Correr: 6-8 frames. Ataques: 3-5 frames con un frame de
  "anticipación" claro antes del golpe (importante para que el jugador pueda
  cancelar/leer el movimiento).
- Cada animación de daño debe durar lo mismo que los i-frames de invulnerabilidad
  (a definir en `stats_personaje.md`) para que el feedback visual sea honesto.

## 4. Composición de nivel
- Máximo 2-3 planos de profundidad con parallax (fondo lejano, fondo medio, capa
  jugable) para no saturar la lectura en una paleta tan oscura.
- Elementos interactuables (palancas, cofres, símbolos) llevan el dorado apagado
  para diferenciarse del entorno sin romper la atmósfera.

## 5. Herramientas
- LibreSprite (portátil, ya disponible en `Herramientas/`) para todo el pixel art
  2D directo.
- Blender (a instalar) reservado para props que se beneficien de un render 3D
  bajado a sprite (columnas, elementos arquitectónicos complejos), no para
  personajes ni animaciones de combate.
