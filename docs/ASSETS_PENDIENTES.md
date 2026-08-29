# Assets pendientes

Registro de assets que **no pueden extraerse limpiamente** con el pipeline
CLI (PIL / componentes conexos / matting de alfa) y necesitan preparación
gráfica externa antes de integrarse a Godot.

Regla (CLAUDE.md del proyecto + instrucción de Marcos 2026-08-28): cuando una
lámina requiere separación, transparencia, reconstrucción o generación, Claude
**se detiene y lo anota acá** con el detalle de qué se necesita. No se improvisa
una extracción degradada.

Formato de entrega preferido: **PNG con fondo transparente, recortado (trim) al
contenido, un archivo por pieza**. Alternativa aceptable: una grilla uniforme
con celdas de tamaño fijo + un manifiesto (nombre por celda); en ese caso indicar
el tamaño de celda y Claude la corta.

---

## Bloqueantes activos

### 2. Torre del nigromante — batches preparados por Marcos (2026-08-28)

Marcos preparó 4 zips en `Documents/Marcos/PHARASMA/Sprites/`
(`vaelith_torre_architecture_batch01`, `_props_batch01`, `_fire_batch01`,
`_vfx_batch02`) extraídos de las láminas IA. Estado tras revisión:

#### 2a. `architecture_batch01` — ✅ LIMPIO, integrado
16 PNG RGBA transparentes, recortados uno por pieza. `arched_door`,
`ruined_arch`, `tall_arch`, `column_plain/twisted/draped`, `barred_gate` x3,
`spiral_staircase`, `altar` x2, `balcony_segment`, `gargoyle`, `rubble_pile` x2.
Copiado a `assets/sprites/props/vaelith_torre/architecture/`.

#### 2b. `props_batch01` — 🟡 MAYORMENTE USABLE, integrado
12 PNG. Objeto único y usable: `ritual_table_01/02`,
`failed_experiment_corpse_01`, `skull_01`, `skull_bones_cluster_01`,
`stone_blocks_01/02`. Con restos menores (tira lateral / fragmento de banner,
tolerable): `bone_pile_01`, `failed_experiment_corpse_02`, `rubble_pile_01/02`,
`stone_rubble_03`. Copiado a `assets/sprites/props/vaelith_torre/props/`.

#### 2c. `fire_batch01` — ❌ RE-CORTE PENDIENTE
16 PNG, pero **cada archivo contiene varios objetos + un fragmento del banner
de categoría** horneado (negro, con texto: "ANTORCHAS DE PARED",
"CANDELABROS", "VELAS", etc.). No son sprites sueltos. `wall_torch_01` = fila
de 6 antorchas + banner. `candles_0x` = 3-4 grupos de velas + banner.
`brazier_0x`, `candelabrum_0x`, `hanging_lantern_0x` = 2-3 objetos cada uno.
**Necesito**: un PNG por objeto, sin banners. Objetos concretos que quiero:
- 1 antorcha de pared encendida (+ 2-3 frames de llama si es fácil)
- 1 brasero de piso cálido, 1 brasero de piso violeta
- 1 candelabro de pie, 1 grupo de velas
- 1 farol colgante
Único casi-limpio: `brazier_violet_01` (2 blobs, el principal sirve).

#### 2d. `vfx_batch02` — ❌ RE-CORTE PENDIENTE
24 PNG, mismo problema: cada archivo = 2-4 variantes del efecto + fragmento de
banner ("AURAS / HALOS", "FUEGO VIOLETA / CORRUPCIÓN", "PROYECCIONES / LUZ EN
SUELO", "LLAMAS ESPECTRALES", "HUMO", ...). **Necesito** un PNG por efecto:
- `corruption_flame` (llama violeta) — 1 estático + tira de frames si se puede
- `floor_projection_violet` (decal circular de luz en piso) — 1
- `spectral_flame_violet` — 1
- `smoke_gray` — 1
(el resto — azul/rojo/naranja — no lo necesita la Torre; sí más adelante.)

Mientras 2c/2d no estén re-cortados, la iluminación de la Torre se hace con
**`PointLight2D` procedural** (ya funciona en el prototipo) — nada de fuego
horneado a medias.

#### 2e. `vaelith_torre_fire_vfx_final.zip` (2026-08-28, 2º intento) — parcial
11 PNG con los nombres pedidos, pero **6 siguen con banner o vecinos**:

| Archivo | Estado | Detalle |
|---|---|---|
| `torre_floor_brazier_warm` | ✅ limpio | brasero cálido de piso, un objeto. Integrable tal cual. |
| `torre_floor_brazier_violet` | 🟡 trim | objeto principal OK; punta ajena 34×43 @(36,0) — recorte rectangular simple. |
| `torre_wall_torch` | 🟡 trim | antorcha OK; fragmento de banner 13×22 @(48,0) — recorte simple. |
| `vfx_corruption_flame_violet_static` | 🟡 trim | llama violeta OK; bits menores — recorte simple. |
| `vfx_smoke_gray` | 🟡 trim | pluma de humo OK; llama azul ajena a la izq. (x0–30) + speck de banner — recorte. |
| `torre_candelabrum` | ❌ | banner 68×22 @(32,0) + vecino 9×65 @(91,48). |
| `torre_candle_group` | ❌ | 4 grupos de velas distintos (2 arriba, 2 abajo), uno es otra vela oscura. |
| `torre_hanging_lantern` | ❌ | 2 faroles apilados + estructura violeta ajena 18×65 @(62,0). |
| `vfx_corruption_flame_violet_strip` | ❌ | banner 105×20 @(0,0) + 2 llamas distintas lado a lado — no es tira de frames uniforme. |
| `vfx_floor_projection_violet` | ❌ | 4 proyecciones (cono violeta, cono azul, pentagrama, anillo naranja) + banner. |
| `vfx_spectral_flame_violet` | ❌ | banner 80×18 @(0,0) + llama violeta + fragmentos azul/rojo. |

#### 2f. `vaelith_torre_fire_vfx_recut_final.zip` (2026-08-28, 3er intento) — ✅ RESUELTO
10 PNG (sin `corruption_flame_violet_strip`: la fuente no tiene tira uniforme y
no se inventa). 5 venían limpios; a los otros 5 se les hizo un **recorte
rectangular manual** para dejar un solo objeto (tenían un vecino separado en el
canvas): `candle_group` (se quedó la vela superior), `floor_brazier_violet` (se
quedó el cuenco violeta, se sacó la torre-pira), `hanging_lantern` (se quedó el
farol, se sacó la caja de abajo), `floor_projection_violet` (se quedó el círculo
ritual violeta), `spectral_flame_violet` (se quedó la llama violeta),
`corruption_flame_violet_static` (se quedó la llama inferior).

**Integrado** a `assets/sprites/props/vaelith_torre/fire/` y `.../vfx/`.
La llama de corrupción animada se resuelve con `PointLight2D` pulsante hasta
tener una tira de frames real.

**Estado global Torre**: architecture ✅ · props 🟡 ✅ · fire ✅ · vfx ✅ ·
`corruption_flame` animada = pendiente (procedural mientras tanto).

---

## Resueltos / sin acción

- **Bosque / cementerio — `gothicvania-cemetery-files.zip` (resuelto 2026-08-28).**
  Marcos lo bajó de `ansimuz.itch.io/gothicvania-cemetery` (CC0) e integrado en
  `assets/sprites/tilesets/gothicvania_cemetery_CC0/` (parallax en `layers/`,
  props ya recortados en `sliced-objects/`, tileset sin armar todavía). Detalle
  en el `README.md` de esa carpeta. **Desbloquea la Fase 3** del
  `roadmap_level1_largo` — falta diseñar el sector en sí (tilemap + spawns +
  gauntlet), no es parte de este paso.
- **Tipografía Gothic Pixels (Akezhar, CC0) — integrada 2026-08-28.** Bajada
  por Marcos, en `assets/fonts/Gothic Pixels.ttf`, aplicada como fuente global
  del proyecto (`project.godot` → `[gui] theme/custom_font`). Import con
  antialiasing/hinting/subpixel desactivados para que se vea nítida como
  fuente de pixel art (no lo hace por defecto el importador de Godot).
- `level1_ruins_tileset.png` / `_v2` — referencia de Marcos, no grid. Reemplazado
  por `dungeon_raou_free_commercial_ok/raou_tileset.tres`.
- `funerary_ruins_tileset.png` — misma clase. Cubierto por Raou para el piso/muro
  base de la Torre.
- `wandering_undead_sheet.png` / `bound_spirit_sheet.png` — re-extracción
  **diferida** (no bloquea Torre; los enemigos actuales no tienen bug de mapeo).
  El halo gris de `EspirituAtado` es defecto de extracción preexistente.
