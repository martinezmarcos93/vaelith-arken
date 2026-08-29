# Roadmap — Level 1 largo (torre → bosque → torre → arena)

> Aprobado 2026-08-27. Reemplaza el Level 1 greybox actual por el recorrido
> completo de la Escena 1 según la visión de Marcos + brief §7/§11.
> Fuente narrativa: `guion_demo.md`. Diseño de sectores: assets de
> `assets/source_sheets/` (auditoría de esta sesión, ver más abajo).

## Visión de la Escena 1

Vaelith **no aparece en medio de la nada**: despierta en las **ruinas de su
vieja torre de nigromante**. Al salir se encuentra varios muertos vivientes
sueltos que antes controlaba. Atraviesa el bosque recolectando memorias hasta
una **segunda torre**, donde combate más, encuentra más memorias y termina
enfrentando a un **constructo que él creó y que replica su personalidad** (el
Guerrero-Espejo).

Reglas transversales:
- Cada sector decorado con lo que le corresponde estéticamente. **Nada colgando
  ni flotando sin sentido** — todo apoyado/motivado (antorchas en pared, huesos
  en el piso, hiedra sobre arcos).
- **Todo el espacio aprovechado**, ningún sector pelado.
- Recolectar **cráneos baja la corrupción** que se acumula cuando Vaelith muere.

## Decisiones cerradas (2026-08-27)

| Tema | Definición |
|---|---|
| Estructura | **Un** Level 1 largo con checkpoints. Corrupción resetea al completar el nivel completo. |
| Frames del despertar | No se rediseñan todavía. La Intro se re-decora como interior de torre; los frames de Vaelith no se tocan. |
| 3 clases de undead | ① Zombi devorado (`zombi_devorado_custom`, extraído) · ② No-muerto errante (`no_muerto_errante_custom`) · ③ Espíritu atado (`espiritu_atado_custom`). Esqueleto (`skeleton_warrior_craftpix`) como 4ª de relleno. Todos mueren en 2 golpes altos. |
| Corrupción | +1 nivel por muerte (máx 3) → +1 enemigo extra y −luz por nivel. Cada cráneo −1. Reset al completar el nivel. |
| Cielo/parallax | `Nuevo cielo.png` (1672×941) reemplaza el atlas de paneles chicos. Profundidad con strips de montaña/silueta encima. |

## Fases

| Fase | Objetivo | Estado |
|---|---|---|
| **0 · Extracción** | ~~`level1_ruins_tileset` → `TileSet` 32×32~~ · `zombie` → AnimatedSprite2D · atlas de props/VFX (árboles, huesos, arquitectura, cementerio, fuego, decals, arena, combat_vfx) a carpetas. Doc roadmap + update auditoría. | zombi ✅ · TileSet Raou ✅ · **arquitectura + props + fire + vfx de la Torre integrados** (`assets/sprites/props/vaelith_torre/`, 2026-08-28) ✅ · **árboles/cementerio integrados** (`assets/sprites/tilesets/gothicvania_cemetery_CC0/`, 2026-08-28) ✅ · arena/combat_vfx pendientes |
| **1 · Parallax + Intro re-vestida** | 5 capas de parallax propias. Intro: mismo guion/frames, escenario = interior de torre (columnas rotas, mesas rituales, cadáver en losa, braseros violetas). | parallax ✅ · **Intro re-vestida ✅** (dressing con arte propio de la Torre; guion/timings/triggers intactos; CanvasModulate placeholder para el pase de gameplay) |
| **2 · Sector Torre** | Tilemap de la torre con el TileSet nuevo. Vaelith arranca dentro/al pie. Puerta con brillo violeta = umbral al bosque. 1-2 espíritus. Fragmento I. | ✅ **`TorreSector.tscn`**: cuarto + pasillo + umbral (barred_gate + luz violeta + `floor_projection_violet`) + 2 espíritus + HUD + safety floor + cámara. Fragmento I = `RecognitionPoint` en la mesa ritual (press-E, único que cuenta en GameState). Flujo: **Intro → TorreSector → Level1.tscn**. El `MemoryFlashTrigger` de la Intro se eliminó (decisión Marcos 2026-08-28): la Intro conserva su narrativa visual pero ya no dispara ni cuenta el Fragmento — vive solo en TorreSector. **Pendiente: pasada visual de Marcos en Godot** — oscuridad del `CanvasModulate`, zoom de cámara, alineación vertical de props con el piso (~30px de float). No se cierra por headless. |
| **3 · Sector Bosque + gauntlet** | Cementerio del bosque: tumbas/ataúdes abiertos = spawns. ≥10 undead, 3 clases, 2 golpes = muerte. Árboles corruptos, troncos, huesos, decals de sangre/huellas. Fragmentos II-III. | 🟡 **desbloqueada** (asset `gothicvania_cemetery_CC0` integrado 2026-08-28) · diseño del sector (tilemap + spawns + gauntlet) todavía sin empezar |
| **4 · Loop corrupción ↔ cráneos** | `GameState.corruption` (0-3). `_die` → +1. `collect_skull()` → −1. `CorruptionController` por tramo: +1 enemigo, baja `PointLight2D`, sube fuego violeta, viñeta. Reset al fin de nivel. Indicador en HUD. | 🟡 núcleo ✅ (GameState + HUD) · `CorruptionController` por tramo pendiente (depende de que existan tramos reales) |
| **5 · Sector 2ª Torre** | Columnas de basalto, mausoleo grande de base, estructuras corruptas. Combate denso (3 clases). Fragmentos IV-VI. Rastro de huellas hacia la arena. | — |
| **6 · Arena del constructo** | `mirror_warrior_arena_sheet`: plataforma circular, estatuas-espejo, escaleras, eclipse corrupto, cara-portal de entrada. Boss `espejo_boss_custom`. "El último día" → Epílogo. | — |
| **7 · VFX combate + pase final** | `combat_vfx` → impacto/parry/destello-narrativo/polvo/muerte. Iluminación motivada (antorchas/braseros + `PointLight2D`). Charcos con reflejo, goteras. Pase de densidad. | — |

Commit atómico por fase. Verificación en Godot antes de "hecho". Si algo falla,
no se propone la fase siguiente.

## Mapa asset → sector (de la auditoría)

| Sector | Hojas fuente |
|---|---|
| Torre del nigromante | `funerary_ruins_tileset`, `gothic_architecture_atlas` (columnas, escalera caracol, ventanas con reja, nichos), `dark_fantasy_props_bodies` (mesas rituales, **cadáver en losa = experimento fallido**), `fire_and_particles` (braseros violetas) |
| Bosque / cementerio (gauntlet) | `gothic_cemetery_sheet` (**tumbas/ataúdes abiertos = spawns**), `skulls_and_bones_atlas`, ~~`dead_trees_atlas`~~ → candidato **GothicVania Cemetery (ansimuz, CC0)**, `gothic_dungeon_decals` (sangre, **huellas**, huesos) |
| Bosque (travesía) | ~~`dead_trees_atlas`~~ (parallax) → candidato **GothicVania Cemetery**, `Nuevo cielo.png` + siluetas de bosque, `rocks_and_ruins_atlas` (arcos naturales), `water_and_wet_terrain` (charcos, agua corrupta), `arcane_corruption_floor_tiles` (progresión) |
| 2ª Torre | `gothic_architecture_atlas`, `rocks_and_ruins_atlas` (columnas basalto), `gothic_cemetery_sheet` (mausoleo grande), `supernatural_corruption_atlas` (estructuras corruptas, raíces oscuras), `fire_and_particles` (fuego violeta) |
| Arena | `mirror_warrior_arena_sheet`, `Nuevo cielo.png` (eclipse), `supernatural_corruption_atlas` (cara-portal, energías), `combat_vfx_sheet` |
| Transversal | decals + huesos + fuego + charcos = "todo cubierto", todo apoyado/motivado |

## A rediseñar por tamaño (flags de la auditoría)

1. ~~Paneles de cielo (~360×200)~~ → resuelto con `Nuevo cielo.png` (1672×941).
2. Capas de parallax de `funerary_ruins_tileset` / `level1_ruins_tileset`
   (~360×180) — aceptable muy al fondo + desenfoque; grandes si se quieren leer.
3. Frames de Vaelith despertando (~50-130px) — **no se rediseñan todavía**
   (decisión). Intro con cámara cercana mientras tanto.
4. Swatches de suelo de `rocks_and_ruins_atlas` (~90px) — usar como detalle, no
   como piso principal. Piso principal: `level1_ruins_tileset` 32×32 +
   `arcane_corruption_floor_tiles` (~120px).

## Abierto

- ¿La corrupción también cambia el epílogo / diálogo final?
- ~~v1 vs v2 de `level1_ruins_tileset`~~ — no aplica: se descartó como fuente del
  `TileSet` (ver Progreso 2026-08-28).
- ~~Descargar `gothicvania-cemetery-files.zip`~~ — resuelto 2026-08-28, ver
  Progreso e integrado en `assets/sprites/tilesets/gothicvania_cemetery_CC0/`.
- Nivel de oscuridad del `CanvasModulate` del prototipo de Torre es de
  muestra — a jugar y ajustar en el editor, no solo evaluar por captura.

## Progreso

**2026-08-27/28 (sesión "hacé todas las implementaciones pendientes"):**
- **Fase 0 (TileSet)**: `level1_ruins_tileset.png` (source_sheets) resultó
  ser referencia visual de Marcos (`docs/prompts_generacion_arte.md` #20),
  no un grid recortable — mismo problema que iba a tener cualquier lámina
  de composición IA. Se usó en su lugar `dungeon_raou_free_commercial_ok/
  Tilesetv3.png`, ya integrado al repo (licencia commercial-ok) pero sin
  uso hasta ahora. Nuevo `assets/sprites/tilesets/dungeon_raou_free_commercial_ok/
  raou_tileset.tres` — primer `TileSet` de Godot del proyecto.
- **Fase 2 (prototipo)**: `scenes/levels/_TorrePrototype.tscn` (prefijo `_`
  = WIP, no reemplaza `Level1.tscn` todavía). Cuarto con pared/piso/columna/
  ventana/farol + pasillo encadenado (`scripts/level/tower_room_builder.gd`,
  pinta el `TileMapLayer` por código para iterar rápido) terminando en un
  umbral de luz fría en vez de pared -- ahí es donde empieza lo no
  construido. `CanvasModulate` + `PointLight2D` (farol cálido, umbral
  violeta, luz de luna) para que el ambiente oscuro real del juego se vea.
  2 `EspirituAtado` (el halo gris de fondo de ese enemigo es un defecto de
  extracción preexistente, no algo de esta sesión -- sigue en "re-extracción
  diferida").
- **Fase 3 (bloqueada)**: `dead_trees_atlas.png` es la misma clase de
  problema que el tileset -- lámina de referencia con fondo pictórico
  compartido, no recortable sin matting de alpha. Se investigó un sustituto
  ya recortado: **GothicVania Cemetery** de ansimuz (CC0, mismo autor que
  `gothicvania_town_CC0` ya integrado) trae árboles retorcidos + lápidas +
  plataformas de piedra + columnas. Pendiente que Marcos lo baje (ver
  Abierto).
- **Fase 4 (núcleo)**: `GameState.corruption` (0-3) + indicador HUD +
  reset al completar nivel. El efecto ambiental por tramo sigue pendiente
  de que existan tramos reales.
- **Bug #1 de la auditoría (pie flotante)**: confirmado visualmente
  (no solo por cálculo) que Bringer y No-muerto flotaban sobre el piso.
  Offsets recalibrados. Espíritu no aplica (`float_sway`, no toca el piso
  por diseño).
- Técnica nueva de verificación visual: capturas vía `PrintWindow` (API de
  Windows) en vez de captura de pantalla completa -- evita fotografiar
  otras ventanas del escritorio por error (pasó una vez con WhatsApp Web,
  corregido en la misma sesión).

**2026-08-28 (sesión "cerrá Fase 1 → Fase 2"):** rama
`feature/level1-sector-torre`, mergeada a `main`.
- **Assets de la Torre**: Marcos preparó externamente y entregó 4 batches
  (arquitectura / props / fire / vfx) a partir de las láminas IA. La
  arquitectura vino limpia; props y fire/vfx necesitaron varias vueltas de
  re-corte (venían con banners de categoría y objetos vecinos horneados).
  38 PNG integrados en `assets/sprites/props/vaelith_torre/{architecture,
  props,fire,vfx}/`. A 6 fire/vfx y 4 props se les hizo un recorte
  rectangular manual para dejar un solo objeto — detalle en
  `docs/ASSETS_PENDIENTES.md §2a-§2f`. **No hay tira de frames** de la llama
  de corrupción (la fuente no la tiene): la animación queda como
  `PointLight2D` pulsante.
- **Fase 1 cerrada**: `Intro.tscn` re-vestida con el arte propio de la
  Torre (columnas, mesa ritual, braseros/antorchas con `PointLight2D`,
  brillo violeta en la puerta-cripta). Guion, timings, triggers y lógica
  intactos salvo el punto siguiente.
- **Fase 2 cerrada**: `_TorrePrototype.tscn` → `scenes/levels/TorreSector.tscn`.
  Cuarto + pasillo + umbral (`barred_gate` + luz violeta + `floor_projection_violet`
  + brasero violeta) → `SceneTransitionTrigger` a `Level1.tscn`. HUD, safety
  floor + `KillZone`, límites de cámara. Flujo nuevo: **Intro → TorreSector
  → Level1**.
- **Fragmento I**: ahora vive SOLO en TorreSector, como `RecognitionPoint`
  en la mesa ritual (press-E → recuerdo de `guion_demo.md` + `collect_memory()`).
  Se eliminó el `MemoryFlashTrigger` de la Intro (era un `DialogueTrigger`
  que mostraba el texto sin contar). Verificado: sin refs colgadas, las 4
  escenas (`Intro`/`TorreSector`/`Level1`/`Epilogue`) cargan headless
  exit 0, contadores y transiciones intactos.
- **Hook epílogo/corrupción**: `GameState.final_corruption` +
  `GameState.complete_level()` (congela el valor antes del reset).
  `level1_controller._on_memory_finished()` lo usa. Sin diálogos nuevos —
  solo deja el número disponible para bifurcar el epílogo más adelante.
- **Pendiente de Marcos (pasada visual en Godot, jugando TorreSector)**:
  oscuridad del `CanvasModulate` (placeholder en Intro y TorreSector),
  zoom de cámara, alineación vertical de props con el piso (~30px de
  float visible en captura). NO se cierra por headless.
- **Fase 3**: sigue congelada. `gothicvania-cemetery-files.zip` está
  descargado en la carpeta externa de Marcos pero NO se integró (su
  instrucción explícita).

**2026-08-28 (sesión "integra todo" — asset del bosque + tipografía):**
- **GothicVania Cemetery integrado**: `assets/sprites/tilesets/
  gothicvania_cemetery_CC0/` (parallax `layers/{background,mountains,
  graveyard}.png`, props ya recortados en `sliced-objects/` — 3 árboles, 2
  arbustos, 4 plataformas de piedra, 1 estatua encapuchada — y `tileset.png`/
  `tileset-sliced.png` sin armar como `TileSet` de Godot todavía). A diferencia
  de las láminas IA de la Torre, este pack CC0 de Ansimuz venía profesionalmente
  pre-recortado (mismo autor que `gothicvania_town_CC0`, ya integrado antes) —
  no hizo falta pipeline de extracción, solo copiar y organizar en `layers/`
  siguiendo la misma convención. **Fase 3 desbloqueada**, pero el diseño del
  sector (tilemap, spawns, gauntlet de ≥10 undead) es un paso aparte, no hecho
  en esta sesión.
- **Tipografía Gothic Pixels integrada**: `assets/fonts/Gothic Pixels.ttf`
  (Akezhar, CC0), aplicada project-wide via `[gui] theme/custom_font` en
  `project.godot` — reemplaza la fuente default de Godot en todos los
  `Control` sin tocar cada escena de UI una por una. Import headless
  reconfigurado a mano (`antialiasing=0`, `hinting=0`,
  `subpixel_positioning=0`, `oversampling=1.0`) porque el importador de TTF
  de Godot por defecto suaviza el font como si fuera tipografía normal,
  lo que arruina el look de pixel art de una fuente diseñada a resolución
  fija.
- Verificado headless: import sin errores + las 5 escenas de la cadena
  (`TitleScreen`, `Intro`, `TorreSector`, `Level1`, `Credits`) cargan sin
  errores de parseo/script con la fuente nueva puesta. **Falta confirmación
  visual de Marcos jugando** (ver la fuente real en las cajas de diálogo/menús,
  no solo que cargue).
