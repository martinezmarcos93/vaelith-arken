# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Este proyecto todavía no tiene versiones publicadas (pre-v0.1, vertical slice
en desarrollo). Ver progreso por etapa en [`docs/Roadmap.md`](docs/Roadmap.md).

## [Unreleased]

### 2026-08-27 (cont. 2) — Audio, UI con arte propio, ataque con mouse, arranque de Level 1 largo

- **Audio (Etapa 8, completa)**: buses sagrado/corrupto + `AudioManager`
  (música por escena) + SFX curados (Suno) cableados a las señales de juego
  (golpes, pasos, salto, aterrizaje). `docs/lista_audio.md` reescrito al
  estado real.
- **UI/UX**: cursor de mouse propio (`CursorManager`), HUD rehecho con la
  estética del diálogo/menú + láminas de penitencia/corrupción (todavía sin
  lógica de corrupción detrás — solo el visual), logo + subtítulo "La espada
  de Pharasma" en el menú principal.
- **Combate**: atacar con clic izquierdo del mouse como ataque principal.
- **Fixes**: pase de arte de la Intro (fuera el escenario gris/debug), cursor
  y caja de diálogo y pausa sobre negro (informe visual P0).
- **Level 1 largo (aprobado, ver `docs/roadmap_level1_largo.md`)**: arranca
  el reemplazo del Level 1 greybox por el recorrido completo torre → bosque
  → 2ª torre → arena. Fase 0: zombi devorado extraído (3ª clase de undead).
  Fase 1: parallax con `Nuevo cielo.png` (reemplaza los paneles chicos
  borrosos).

### 2026-08-27 — Arte de UI propio, rework narrativo y arranque de producción

- **UI con arte propio**: `title_logo` + 6 placas de menú extraídas de una hoja
  única; `TitleScreen.tscn` y `PauseMenu.tscn` pasan de `Label`/`Button` a
  `TextureRect`/`TextureButton`. `CREDITS.md` actualizado.
- **Rework narrativo (Fases 1–3 de la auditoría)**: `guion_intro_reescrito.md` →
  `guion_demo.md`, ahora fuente de verdad de toda la demo. Se descarta el canon
  de la sesión de mesa (Pharasma como visión, Tomás, el padre).
  - Intro: Escena 1 "El despertar", Fragmento I (la creación del constructo),
    triggers de símbolo/post-combate/descenso.
  - Level 1: fuera la visión de Pharasma ×3; `MemoryFragment2` → Fragmento II
    (la obediencia), `MemoryFragment1` → Fragmento III (el propósito); triggers
    de huellas del constructo.
  - Boss "El Espejo": `BossIntroTrigger`, `phase_changed` → "Lo que Vaelith
    olvidó", `surrendered` → "La identidad" + recuerdo "El último día".
  - Epílogo "Regreso al presente" + pantalla de cierre en tres tiempos
    ("La deuda continúa." → "VAELITH ARKEN" → "El muerto recuerda.").
- **Bugs**:
  - "Dos Vaeliths" al atacar: `attack1_1.png` era una doble figura de la
    extracción IA — frame reconstruido.
  - Sprites flotando sobre el suelo: `offset` del `AnimatedSprite2D` de Vaelith
    y del Boss `-31` → `-25` (falta confirmación fina en editor; los otros
    personajes quedan pendientes).
  - "Siempre la misma memoria": era que todos los nodos tenían el mismo texto
    placeholder — resuelto con el rework de textos.
- **Assets**: 47 hojas de arte propio traídas a `assets/source_sheets/`
  (organizadas por categoría, `.gdignore`) como material fuente sin extraer.
- **Producción**: `docs/BRIEF_IMPLEMENTACION.md`, `docs/AUDITORIA_2026-08-27.md`
  y `CLAUDE.md` de proyecto. El roadmap por Etapas queda como referencia
  histórica; el trabajo activo sigue el plan por Fases de la auditoría.
- `docs/guion_intro.md` y `docs/guion_desenlace.md` marcados como obsoletos.

### 2026-08-27 (cont.) — Producción vertical slice, Fases 0–1 y prep 7/9

Trabajo hecho en `feature/produccion-vertical-slice`, mergeado a `main` con
autorización de Marcos. **Pendiente de verificación visual** (no se pudo abrir
el editor en la sesión).

- **Fase 0**: brief + auditoría + `CLAUDE.md`. `Main.tscn` + test drivers →
  `tools/`.
- **Fase 1 — re-extracción de sprites** desde las hojas nuevas de
  `source_sheets/`:
  - **Vaelith** (`vaelith_knight_sheet`): arregla el mapeo roto de
    `_frames.tres` (jump=idle, fall=attack1, attack2=idle, hurt=death). 13
    animaciones, canvas 320×240, `offset` `-50`. `player.gd` usa `block`/`shove`.
  - **Boss El Espejo** (`spectral_knight_violet_sheet`): mismo arreglo. 12
    animaciones. `boss1.gd`: `shove`/`block`/`stagger` con anim propia.
  - Los 2 enemigos regulares: re-extracción **diferida** (no tienen el bug de
    mapeo; sus hojas resisten el recorte automático).
- **Fase 9 (prep)**: `DialogueBox` con marco propio (`options_frame` como
  `NinePatchRect`, extraído de `dialogue_box_frames`) + narración (gris) vs.
  voz hablada (dorado). `narration_frame` extraído para Fase 8.
- **Fase 7 (base)**: `InteractableArea` (Area2D + prompt `[E]` + señal
  `interacted` + `one_shot`) y `RecognitionPoint` (reconocimiento → señal
  `acted` → memoria opcional), con escenas base. Nada lo instancia todavía.
- **Fase 8 (prep)**: autoload `MemoryFlash` — flash pálido + drenaje de color
  al recoger un fragmento (escucha `GameState.memory_collected`), para que los
  recuerdos se sientan como escenas y no como texto.

### Added — Level 1 construido en Godot (Fase 4.3, greybox)
- `docs/layout_level1.md` (Fase 4.1) ya existia completo de una sesion
  anterior pero no estaba marcado en `docs/Roadmap.md` -- discrepancia
  dice/hace detectada y corregida al retomar el trabajo.
- `scenes/levels/Level1.tscn`: los 6 tramos A-F del layout, construidos como
  greybox real (StaticBody2D con colision, sin TileMap/TileSet todavia --
  los tilesets integrados siguen siendo PNGs sueltos, recortarlos en un
  TileSet de Godot conviene hacerlo con el editor abierto, no a ciegas por
  texto). Incluye los 2 checkpoints, los 3 enemigos regulares del Tramo B/D
  (`docs/diseno_enemigos.md`), la rama opcional del Tramo E, y los 8 props
  de `cave_props_craftpix_free` como decoracion (la fogata ritual marca el
  umbral del Boss 1).
- `scripts/level/hazard.gd` + `scenes/level/Hazard.tscn`: pieza nueva que
  faltaba para el hazard estatico del Tramo C -- reutiliza `Hitbox` pero se
  reactiva sola en ciclo (un hazard no tiene "dueño" que llame `activate()`
  como un ataque puntual).
- **Bug real encontrado y corregido por testing headless**
  (`scripts/level1_test_driver.gd`, smoke test descartable): un salto
  fallido hace caer al jugador para siempre -- el proyecto no tiene sistema
  de muerte por caida. Se agrego un piso de seguridad continuo debajo de
  todo el nivel y se ajusto el salto mas exigente (Tramo A -> B, gap de 80px
  bajado a 60px) para no depender de ese piso de emergencia en el uso normal.

### Added — Curación de assets: cave props + evaluación de loot icons
- Resuelta la decisión pendiente sobre `Free-Top-Down-Pixel-Art-Cave-Objects`:
  se evaluaron visualmente los props individuales (varios nombres de archivo
  del pack están mal etiquetados) y se integraron 8 a
  `assets/sprites/tilesets/cave_props_craftpix_free/` — cristales, hongos,
  tótem, cráneo, restos óseos, estatua y una fogata ritual (mal nombrada
  "Gates" en el pack original) que es candidata fuerte a "acento cálido" de
  `docs/guia_estilo_visual.md`. Documentado en `CREDITS.md`.
- Extraído y evaluado por primera vez `free-undead-loot-pixel-art-icons.zip`
  (nunca se había descomprimido): 48 íconos de loot de buena calidad y
  licencia, pero `docs/GDD.md` excluye explícitamente el sistema de
  inventario del alcance de la demo — no se integró a `assets/` por eso, se
  deja documentado para el juego completo.

### Added — Checkpoint y respawn automático (Fase 4.3, penitencia parcial)
- `scripts/level/checkpoint.gd` + `scenes/level/Checkpoint.tscn`: Area2D que
  al ser tocada por el jugador (grupo `"player"`) actualiza su punto de
  respawn. Reutilizable en cualquier nivel.
- `player.gd`: `set_checkpoint()` (llamado por el checkpoint),
  `respawn_delay`/`respawn_iframes` exportados, y `_process_dead()` ahora
  dispara `_respawn()` automáticamente en vez de dejar `DEAD` como estado
  terminal para siempre. Resuelve el "penitencia pendiente" que quedaba
  abierto desde la Fase 1.4.
- **Alcance explícito:** esto resuelve el respawn en sí. La corrupción de
  nivel progresiva de "penitencia" (`docs/stats_personaje.md`: +1 nivel de
  corrupción por muerte, más enemigos/menos luz) sigue sin implementar —
  depende de tramos reales con dificultad ajustable, no del mecanismo de
  respawn.
- Validado headless: `test_driver.gd` ahora deja morir a Vaelith, espera el
  respawn automático, y confirma que puede volver a moverse (vuelve a
  `FREE`, vida restaurada al máximo).

### Added — Enemigos regulares con IA real (Etapa 5, sandbox validado)
- `scripts/enemies/enemy_regular.gd`: máquina de estados compartida
  Idle→Alerta→Ataque→Vulnerable→Idle (tal como especifica
  `diseno_enemigos.md`), un solo script con toda la diferencia entre
  "No-muerto errante" y "Espíritu atado" resuelta por `@export` (patrulla en
  tierra vs. vaivén flotante + lunge), sin duplicar código.
- `scenes/enemies/NoMuertoErrante.tscn` / `EspirituAtado.tscn`: placeholder
  de arte temporal (Necromancer CC0-compatible y Ghost gratis, ya
  catalogados en `CREDITS.md`), igual criterio que el placeholder del
  jugador — validar la IA sin esperar arte final.
- **Bug real encontrado y corregido por testing headless:** todos los
  Hurtbox compartían la misma capa de colisión, así que un enemigo podía
  golpear a otro enemigo o al `TrainingDummy` por accidente (fuego amigo).
  Se separó en dos capas (jugador vs. bando enemigo) en `Player.tscn`,
  `TrainingDummy.tscn` y los dos enemigos nuevos.
- **Segundo hallazgo (documentado, no bug):** si `attack_range` es menor que
  la distancia física mínima alcanzable (otro cuerpo sólido en el camino),
  `move_and_slide()` frena al enemigo antes de que la distancia lógica
  dispare el ataque — se queda "pegado" sin atacar nunca. Anotado como
  comentario en `enemy_regular.gd` para la próxima vez que se ajusten estos
  valores en Level 1 real.

### Added — Preproducción (Etapa 0, completa)
- Estructura base del proyecto Godot 4.7 (`project.godot`, carpetas de
  scenes/scripts/assets/docs/tools).
- GDD, guía de estilo visual (paleta extraída algorítmicamente de la
  referencia estética), stats jugables traducidos de la ficha de
  Pathfinder 2e, guion de intro, layout de Level 1, diseño de enemigos
  regulares, borrador de desenlace.

### Added — Movimiento y cámara (Etapa 1.1/1.2, completa)
- Movimiento base del jugador (`scripts/player.gd`): control aéreo mínimo,
  coyote time, sin doble salto ni dash — pilar de diseño "salto comprometido".
- Cámara con position smoothing, lookahead en la dirección de movimiento
  (calculado en `player.gd`, reutilizable entre niveles) y límites de nivel
  configurados por escena (override del `Camera2D` en cada `.tscn` de nivel).
- Input map configurado por código (`scripts/input_setup.gd`, autoload):
  mover, saltar, atacar alto/bajo, bloquear, embestida, interactuar.
- Escena sandbox de pruebas de física (`scenes/levels/Main.tscn`).

### Added — Combate base (Etapa 1.3, completa)
- Hitbox/Hurtbox reutilizables (`scripts/combat/`) para jugador, enemigos y
  boss futuros.
- Ataque alto (daño 2) y bajo (daño 1) con ventanas de daño precisas, sin
  knockback por decisión de diseño validada por testing.
- Bloqueo con degradación de postura: rompe al 4to golpe consecutivo
  (umbral configurable), entra en Staggered vulnerable 0.8s.
- Embestida: sin daño, knockback 300, aturde al objetivo 0.6s.
- I-frames de 0.4s tras recibir daño.
- Muñeco de entrenamiento (`TrainingDummy`) en el sandbox: recibe golpes y
  contraataca cada 2s para poder validar también el bloqueo.
- Driver de pruebas headless (`scripts/test_driver.gd`) que simula input
  real (`Input.action_press/release`) y ejercita todo el combate de punta
  a punta sin necesitar un humano jugando — corre con
  `Godot --headless --quit-after N` y se lee por consola.
- **2 bugs reales encontrados y corregidos por el testing headless:**
  1. `Area2D.monitoring` no vuelve a emitir `area_entered` para
     superposiciones ya existentes al reactivarse — un ataque repetido
     contra un objetivo pegado al cuerpo nunca conectaba.
     `Hitbox.activate()` ahora revisa `get_overlapping_areas()` manualmente.
  2. Input de un solo frame perdido si coincidía con estar en el aire
     (ej. por el knockback de un golpe recibido) — se agregó un buffer de
     input de 0.12s (`_poll_input_buffer`), consultado en todos los
     estados y consumido recién cuando el jugador puede procesarlo.

### Added — Vida, daño y muerte (Etapa 1.4, sandbox validado)
- Vida, daño, i-frames (0.4s) e integración con bloqueo/postura ya existían
  desde el combate base (Etapa 1.3).
- Estado `DEAD` para el jugador: al llegar a 0 HP, la máquina de estados
  queda trabada (sin timer de reversión, a diferencia de `HURT`/`STAGGERED`)
  e ignora golpes posteriores. Corrige un bug real encontrado por testing
  headless: `_die()` solo imprimía un mensaje y dejaba `state=HURT`, que
  vencía por tiempo y volvía a `FREE` sin importar la vida — un "cadáver"
  con 0 HP seguía moviéndose y peleando.
- La penitencia/respawn real (Pharasma devuelve al jugador, corrupción de
  nivel) sigue **fuera de alcance** hasta la Etapa 4, porque depende del
  sistema de checkpoints — hoy `DEAD` es un estado terminal sin respawn,
  suficiente para validar el criterio de aceptación de la Fase 1.5
  ("correr, saltar, golpear y morir sin bugs bloqueantes").

### Added — Assets de terceros (investigación + integración selectiva)
- Checklist completo de pixel art y audio con candidatos investigados
  (itch.io, OpenGameArt, CraftPix) — ver `docs/lista_assets_pixel_art.md`
  y `docs/lista_audio.md`.
- Integrados y con licencia **confirmada**: Ghost sprite (OpenGameArt,
  CC-BY 4.0), Ghost+Skull (Fatal AI Gaming, gratis), Dungeon Tileset
  (Golopin, royalty-free), Evil Wizard 1/2 (CC0), GothicVania Town +
  música de ambiente (Ansimuz, CC0 / atribución), Dungeon Tileset
  side-scroller (Raou, comercial permitido), Effect and Bullet 16x16
  (BDragon1727, donationware), Kenney 1-Bit Platformer (CC0, solo para
  greybox de nivel), Necromancer (CreativeKind, comercial permitido).
- Marcados como **licencia sin confirmar** (no usar en build final):
  Seamless patterns (fuente no identificada).
- Evaluados y descartados por no encajar con la estética o el género
  (top-down vs. side-scroller, paleta cálida de fuego, formato no
  importable): boss_demon_slime, Free-Undead-Tileset-Top-Down, FreeKnight_v1,
  texturas genéricas sin curar, desert enemy pack — detalle completo y
  razones en `CREDITS.md`.

### Added — Integración de animación (Etapa 2.4, validada con placeholder)
- `AnimatedSprite2D` reemplaza el rectángulo de color (`Polygon2D`) en
  `Player.tscn`. `player.gd` ahora sincroniza la animación con la máquina
  de estados (`_update_sprite_animation`): idle/run/jump/fall según
  movimiento y suelo, attack1/attack2/hurt/dead según el estado de combate.
- **El sprite es temporal**: reutiliza el pack CC0 "Evil Wizard 2" (pensado
  como enemigo, ver `CREDITS.md`) solo para probar el cableado técnico
  (`AnimatedSprite2D` + `SpriteFrames` + estados) antes de invertir tiempo
  en el sprite sheet final de Vaelith. `shove` y `block` no tienen
  animación propia en el pack — reutilizan `attack2`/`idle` a propósito,
  no es un mapeo definitivo.
- `assets/sprites/player/_placeholder_evil_wizard2_frames.tres` — recurso
  `SpriteFrames` generado a partir de las hojas de sprites de
  `evil_wizard_2_CC0/` (8 animaciones, 46 frames en total).
- Validado headless: mismo test de combate de siempre, sin errores de
  carga de escena/recurso.

### Added — Infraestructura de repo
- `README.md`, `.gitattributes`, `.editorconfig`, `CREDITS.md`.
- Repo conectado a `github.com/martinezmarcos93/vaelith-arken`, rama única
  `main` (la rama de trabajo `feature/vertical-slice-demo` se mergeó y
  borró tras cerrar la Etapa 1).

### Pending — trackers vivos

Esta sección por Etapas quedó desactualizada (ver `docs/Roadmap.md`, marcado
como referencia histórica desde el 2026-08-27). El trabajo pendiente real se
sigue en dos documentos que SÍ se mantienen al día:

- **`docs/AUDITORIA_2026-08-27.md`** — estado actual del código (qué
  funciona / parcial / roto / falta) + plan por Fases 0–11 de producción.
- **`docs/roadmap_level1_largo.md`** — plan de fases del rediseño de Level 1
  (torre → bosque → 2ª torre → arena), con su propia sección de Progreso.
