# Auditoría técnica — 2026-09-09

Segunda pasada sobre la auditoría de video de Marcos: verifica cada hipótesis
P0/P1 contra el código y la configuración reales. Godot 4.7.2, `main` @ `04e4861`.

Formato: **hipótesis del video → qué dice la implementación → veredicto → fix**.

---

## 1. Pipeline pixel-perfect (P0)

### 1.1 Filtro de textura — **NO es el problema**
- `project.godot`: `rendering/textures/canvas_textures/default_texture_filter=0` (Nearest). ✅
- `.import` de los PNG: `compress/mode=0` (lossless), `mipmaps/generate=false`,
  `process/fix_alpha_border=true`. ✅ Ninguno override-ea el filtro.
- No se encontró ningún nodo con `texture_filter=1` (Linear). *(pendiente: grep
  exhaustivo de `.tscn`, pero los principales están limpios.)*
- **Veredicto:** el blur que se ve NO viene del filtro ni de la importación.

### 1.2 Zoom de cámara NO entero — **CONFIRMADO P0**
- `Player.tscn` → `Camera2D`: `zoom = Vector2(2.5, 2.5)`.
- 2.5× no es entero. Cada píxel de arte se dibuja en 2.5 píxeles de pantalla →
  filas/columnas de píxeles de distinto grosor. **Esta es la causa principal
  del "algunos elementos nítidos, otros no".**
- **Fix:** zoom entero (`2` o `3`). Con base 1280×720 y zoom 3 el área visible
  es 426×240 — chequear que el diseño de nivel entra; si no, zoom 2 (640×360).

### 1.3 Escala de sprite NO entera — **CONFIRMADO P0**
- `Player.tscn` → `AnimatedSprite2D`: `scale = Vector2(0.5, 0.5)`.
- Los frames de personaje (arte IA extraído a ~320 px de contenido) se **reducen
  a la mitad** en runtime. 0.5× sobre pixel art rompe la grilla: 2 píxeles de
  origen → 1 de destino, sin control de cuál. Personaje "mushy" vs tiles nítidos.
- Mismo problema en el boss y enemigos custom (sprites de 320×240 / 220×170).
- **Fix (ligado al roadmap de rebuild de sprites):** `extract.py` debe sacar los
  frames **a la resolución final** (ej. 48–64 px de alto) y dejar el
  `AnimatedSprite2D` en `scale = 1`. Downscalear en runtime es el bug.

### 1.4 Sin pixel snapping + cámara suavizada — **CONFIRMADO P0**
- `project.godot`: **no** hay `rendering/2d/snap/snap_2d_transforms_to_pixel`
  ni `snap_2d_vertices_to_pixel` → ambos en `false` (default).
- `Player.tscn` → `Camera2D`: `position_smoothing_enabled = true`,
  `position_smoothing_speed = 8.0`.
- Cámara lateral que interpola a coordenadas fraccionarias + sin snap = shimmer
  y "flotado" de 1 px en bordes de alto contraste. (El flotado *real* de los
  personajes es aparte, §4.)
- **Fix:** activar `snap_2d_transforms_to_pixel` y `snap_2d_vertices_to_pixel`.
  Evaluar `snap_2d_transforms` a nivel Camera2D. Mantener el smoothing pero con
  el snap el resultado final cae a píxel entero.

### 1.5 Stretch sin escala entera — **CONFIRMADO P0**
- `project.godot`: `window/stretch/mode="viewport"` ✅ pero **no** hay
  `window/stretch/aspect` ni `window/stretch/scale_mode`.
- `scale_mode` en default (`fractional`). A 1280×720 interno → ventana 1920×1030
  el factor es ~1.5× fraccional → toda la imagen se re-escala con interpolación.
- **Fix:** `window/stretch/scale_mode="integer"` + `window/stretch/aspect="keep"`.
  Con eso el juego se dibuja a 1280×720 y se escala ×1 (letterbox) o se elige
  una base menor (640×360) que escale ×2 a 1280 y ×3 a 1920.
- **Decisión de diseño pendiente con Marcos:** base interna. Recomiendo
  **640×360** (escala ×2→1280, ×3→1920, ambos enteros) o **480×270** (×4→1920).
  Hoy 1280×720 no escala entero a 1920.

**Resumen §1:** los 4 sub-P0 de Marcos se confirman salvo el del filtro. El fix
es coordinado: base interna + `scale_mode=integer` + zoom de cámara entero +
`scale=1` en los sprites (vía rebuild) + snap 2D.

---

## 2. Legibilidad / contraste (P0 gameplay)

- `Level1.tscn` → `CanvasModulate color = Color(0.62, 0.58, 0.66, 1)`: multiplica
  toda la escena a ~62% de brillo. Es la causa directa de "todo muy oscuro".
- Iluminación **ya existe**: `PointLight2D` `SurfLight` (energy 0.4, azul frío)
  en plataformas; `RimLight` (energy 0.15–0.17) en **algunos** enemigos
  (`NoMuertoErrante2/3`, `EspirituAtado1`) — **no** en `NoMuertoErrante1`,
  **no en el Player**.
- Zona boss: `color = Color(0.153, 0.055, 0.035, 1)` (fill rojo oscuro).
- **Veredicto:** la infraestructura de luz está, mal calibrada e inconsistente.
- **Fix (P1, bajo esfuerzo — como dijo Marcos):**
  1. Subir `CanvasModulate` a ~`0.72–0.78` (mantener oscuro, sacar el "negro
     absoluto").
  2. **Rim light en el Player** (nodo `PointLight2D` hijo, energy ~0.2, azul
     claro, `light_mask` propio) — separa figura de fondo sin tocar el sprite.
  3. Rim light **consistente en todos los enemigos** (mismo valor).
  4. Regla compositiva de Marcos: fondo 10–30% / gameplay 40–70% / jugador
     60–90% de luminancia en lo importante.

---

## 3. Presentación del Boss (P0/P1 — "el problema más importante" del video)

Estado real, repartido en varios archivos:
- `boss1.gd`: `_ready()` → `state = State.APPROACH` inmediato. **Cero lógica de
  entrada**: no bloquea salidas, no para la cámara, no limpia el escenario, no
  dispara la barra de boss, no cambia música.
- `boss1.gd` **sí** emite buenas señales: `surrendered`, `health_changed`,
  `phase_changed`. La arquitectura de eventos que pide Marcos (§16) **ya existe
  a medias**.
- `level1_controller.gd` escucha esas señales y traduce a beats de guion
  (`phase_changed` → diálogo; `surrendered` → silencio + diálogo + recuerdo +
  epílogo). Es el patrón correcto, sólo que vive en el controller del nivel.
- La entrada actual = `MusicTrigger` (cambia música al entrar a la arena) +
  `BossIntroTrigger` (una línea de diálogo). **Nada más.** El boss simplemente
  ya está ahí y empieza a caminar.
- Telegrafiado del boss (`_update_telegraph_visual`): **tinte rojo sobre el
  sprite entero** durante el windup, no un brillo en el filo. Placeholder.
- Rendición: `sprite.modulate = Color(0.6,0.6,0.6)` (gris) + anim idle. Mínimo.

**Veredicto:** el boss funciona como pelea pero **no tiene "entrada de boss"**.
Los ladrillos (triggers, señales, `level1_controller`) están; falta el momento.

**Fix (P0/P1):** un `BossFightController` (nodo en la arena o extender
`level1_controller`) que al cruzar el umbral:
1. Bloquea salidas (colisión invisible) + `limit_*` de la cámara a la arena.
2. Para al player un instante, cámara fija en la arena.
3. Oculta/atenúa decoración de fondo de la arena (P1 §5 del video).
4. Aparece el boss (desde un lado / cae) + línea breve.
5. Revela la `BossBar` del HUD (hoy está en `HUD.tscn` pero sin coreografía de
   entrada) + cambia música (ya lo hace `MusicTrigger`, mover el timing acá).
6. Emitir `boss_intro_started` / al terminar, `boss_fight_started`.
Sin reescribir `boss1.gd` — solo orquestación externa vía señales.

---

## 4. Personajes flotando — **CONFIRMADO, causa distinta al shimmer**

- Cada frame de `vaelith_custom` tiene el "pie" a distinta Y en su canvas 320×240
  (`run_4.png` 30 px más arriba que el resto). `Player.tscn` usa **un solo**
  `AnimatedSprite2D.offset = Vector2(0, -50)` para todos → la mayoría queda
  desalineada respecto del `CollisionShape2D` (28×44).
- Hay un `ContactShadow` en `position = (0, 21)` que *debería* anclar visualmente,
  pero si el sprite flota, la sombra queda despegada.
- **Fix:** roadmap de rebuild de sprites (`roadmap_rebuild-sprites_2026-09-09`):
  re-extraer con ancla de pie consistente → un `offset` correcto → pies al piso.
  Verificar con `tools/shot.gd` modo `feet` (ya calcula el gap).

---

## 5. HUD pequeña (P1)

- `HUD.tscn` → `PlayerBlock/HealthBar`: **`scale = Vector2(0.6, 0.6)`** — la
  barra se dibuja al 60%. `BossBar/HealthBar`: `scale = 0.828`.
- Font sizes: `SkullCount` 18, `CorruptionLabel` 16, `BossBar/Name` 16.
- `PlayerBlock` ocupa 260×90 px sobre base 1280 (~20% de ancho) — el marco no es
  chico, **el gauge sí** por el `scale 0.6`.
- **Fix (P1):** subir `HealthBar.scale` a ~`0.85–1.0` y reacomodar el layout del
  bloque; +2 px a los font sizes de contadores. Ornamentación intacta.

---

## 6. Diálogo — texto chico / poco contraste (P1)

- `DialogueBox.tscn` → `Panel/Label`: `font_size = 20`,
  `font_color = Color(0.87, 0.87, 0.83)`. **Sin** `line_spacing` override.
  **Sin** shadow/outline en este Label (el HUD sí usa `shadow_offset_y = 1`).
- `Hint`: `font_size = 15`.
- **Fix (P1):** `font_size` 20→22, `theme_override_constants/line_spacing` +3–4,
  agregar `theme_override_constants/shadow_offset_x/y = 1` +
  `shadow_color` oscuro. Subir `font_color` a ~`0.92`.

---

## 7. Narrativa vs acción (P1)

- `level1_controller._on_boss_phase_changed` → `DialogueBox.show_lines([...])`
  **durante la pelea** (el boss sólo tiene `transition_invuln_time = 1.0`s y
  sigue). Confirmado: caja de diálogo contemplativa encima de combate activo.
- **Fix (diseño):** mover el comentario de fase 2 a un bark corto (texto flotante
  sobre el boss, sin pausar) o a después de la pelea. Reservar `DialogueBox`
  (pantalla completa, foco) para los beats sin combate.

---

## 8. Cursor visible en el desenlace — **CONFIRMADO P0**

- `cursor_manager.gd` → `_ready()`: `Input.mouse_mode = Input.MOUSE_MODE_VISIBLE`,
  **forzado y nunca revertido**. Cursor custom siempre visible: gameplay,
  cutscenes y epílogo.
- `epilogue_controller.gd`: **no** oculta el cursor.
- **Fix (P0):** `Input.mouse_mode = MOUSE_MODE_HIDDEN` durante gameplay y
  cutscenes; `VISIBLE` sólo en menús (TitleScreen, PauseMenu). Como mínimo,
  `HIDDEN` en `epilogue_controller._ready()` y en `Intro`.

---

## 9. Transición del epílogo (P0/P1 — "parece que dejó de renderizar")

- `epilogue_controller`: `stop_music(2.0)` + `stop_ambient(2.0)` de entrada →
  9 líneas de diálogo sobre el fondo del epílogo → `fade_out` → label → `fade_in`
  → hold 3s → título. Y `level1_controller._on_boss_surrendered` ya mete
  `stop_music(1.5)` + 2.5s de silencio + 9 líneas + recuerdo (12 líneas) antes.
- Son **~30 líneas de diálogo encadenadas** con silencio total y fundidos. Sin
  un "beat" de freeze/impacto tras la rendición.
- **Fix (P1):** tras `surrendered`: freeze corto (0.3–0.5s, `Engine.time_scale`
  o pausa del boss) → sting sonoro breve → recién ahí el silencio y el texto.
  Recortar/agrupar líneas (§4 del video). Cursor oculto (§8).

---

## 10. Arquitectura (§16 del video)

Estado actual vs. lo propuesto:
- **Autoloads:** `InputSetup, CursorManager, AudioManager, TransitionManager,
  DialogueBox, GameState, MemoryFlash, PauseMenu`. Buena separación. Falta un
  `CameraController` (hoy la cámara vive en `Player.tscn`, sus límites se
  setean por escena).
- **Lógica narrativa fuera de los enemigos:** ✅ en gran parte. `boss1.gd` no
  llama a `DialogueBox` directo — emite señales, `level1_controller` traduce.
  El acoplamiento que queda: `level1_controller` mezcla orquestación de boss +
  música + memoria + transición en un archivo.
- **Eventos del boss:** `surrendered`, `phase_changed`, `health_changed` ya
  existen. Faltan `boss_intro_started` / `boss_fight_started` /
  `boss_phase_transition_started`.
- **Recomendación:** extraer un `scripts/systems/boss_fight_controller.gd`
  (escucha señales del boss, orquesta cámara/lock/HUD/música/diálogo) y dejar
  `level1_controller` sólo con lo del nivel. Mínimo cambio, gran claridad para
  Level 2 / Boss 2.

---

## Plan de acción priorizado

### P0
| # | Qué | Dónde | Esfuerzo |
|---|---|---|---|
| 1 | Base interna fija + `stretch/scale_mode=integer` + `aspect=keep` | `project.godot` (decidir base con Marcos) | Bajo, alto impacto |
| 2 | Zoom de cámara entero (2 o 3) | `Player.tscn` Camera2D | Bajo |
| 3 | `snap_2d_transforms_to_pixel` + `snap_2d_vertices_to_pixel` = true | `project.godot` | Bajo |
| 4 | Sprites a `scale = 1` (via rebuild, no downscale runtime) | roadmap rebuild + `Player.tscn`/enemigos | Medio (depende del rebuild) |
| 5 | Cursor `HIDDEN` en gameplay/cutscenes | `cursor_manager.gd`, `epilogue_controller.gd` | Bajo |
| 6 | Entrada de boss (lock + cámara + reveal + HUD + música) | nuevo `boss_fight_controller.gd` | Medio |
| 7 | Contraste: subir `CanvasModulate`, rim light al Player, rim consistente en enemigos | `Level1.tscn` | Bajo |

### P1
- HUD: `HealthBar.scale` 0.6→~0.9, +2 px a contadores.
- DialogueBox: +2 px font, `line_spacing`, shadow.
- Feedback de combate: hit flash en enemigos al recibir daño (hoy solo SFX +
  knockback; el hitstop/shake ya se agregó al player esta sesión — falta el
  flash y aplicarlo también a los enemigos).
- Boss telegraph: brillo en el filo, no tinte de cuerpo entero.
- Mover el diálogo de fase 2 a bark (no pausar el combate).
- Verticalidad y zonas de descanso en Level 1 (diseño de nivel).
- Diferenciación cromática por zona (composición/luz/densidad, sin tilesets nuevos).
- `boss_fight_controller.gd` + señales nuevas del boss.

### P2
- Microanimaciones ambientales (fuego, niebla, polvo, luces).
- Fundidos más cinematográficos.
- Tipografía fina, ornamentación.
- Secretos / coleccionables en huecos arquitectónicos.

---

## Apéndice — archivos para la revisión

| Pedido | Ruta |
|---|---|
| project | `project.godot` |
| Level 1 | `scenes/levels/Level1.tscn` (+ `scripts/level1_controller.gd`) |
| Player | `scenes/player/Player.tscn` + `scripts/player.gd` |
| Boss | `scenes/enemies/Boss1.tscn` + `scripts/enemies/boss1.gd` |
| Camera2D | dentro de `Player.tscn` (no hay `CameraController` propio) |
| Sprites (import) | `assets/sprites/**/**.png.import` — todos: mode 0, sin mipmaps, `fix_alpha_border=true` |
| Movimiento/colisión | `scripts/player.gd`, `scripts/combat/{hitbox,hurtbox}.gd` |
| Diálogo | `scenes/ui/DialogueBox.tscn` + `scripts/ui/dialogue_box.gd` |
| HUD | `scenes/ui/HUD.tscn` + `scripts/ui/hud.gd` |
| Enemigos regulares | `scripts/enemies/enemy_regular.gd` |
| Transiciones | `scenes/ui/TransitionManager.tscn`, `scripts/ui/transition_manager.gd` |
| Cursor | `scripts/cursor_manager.gd` |
| Epílogo | `scripts/epilogue_controller.gd` |

## Nota metodológica

Verificado leyendo código y `.tscn`/`.import` directamente; corridas headless de
esta sesión confirman que el juego carga y corre sin errores de script. **No
auditado:** FPS/profiler (sin instrumentar), y un grep exhaustivo de
`texture_filter` en todos los `.tscn` (los principales están limpios).
