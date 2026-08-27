# Auditoría del proyecto — 2026-08-27

Diagnóstico de solo lectura del estado del repo contra
[`BRIEF_IMPLEMENTACION.md`](BRIEF_IMPLEMENTACION.md). Base: `project.godot`, los
24 scripts de `scripts/`, todas las escenas de `scenes/`, los docs de diseño
(`GDD`, `Roadmap`, `stats_personaje`, `diseno_enemigos`, `layout_level1`,
`guion_demo`, `CHANGELOG`) y el árbol de `assets/`.

---

## 1. Qué YA funciona (jugable)

| Sistema | Estado |
|---|---|
| **Movimiento** | run/aceleración/fricción/salto/coyote/control-aéreo-mínimo según `stats_personaje.md`. Cumple pilar GDD 1. |
| **Combate** | ataque alto/bajo (direccional, ventanas activas), bloqueo frontal + rotura de postura al 4º golpe → stagger, shove (knockback + aturde, sin daño), i-frames. Sin knockback en los ataques (deliberado, testeado). Cumple pilar GDD 2. |
| **Muerte/respawn** | estado `DEAD`, respawn en checkpoint tras delay, i-frames al reaparecer, sin pantalla de Game Over. |
| **Level 1 (greybox)** | 6 tramos A–F, 2 checkpoints, 3 enemigos regulares + BringerOfDeath, rama opcional (Tramo E), hazard (Tramo C), piso de seguridad anti-caída continuo, parallax con arte propio. Límites de cámara por escena. |
| **Intro** | tramo jugable, narración del despertar (Esc 1), flash de memoria (Fragmento I), triggers de símbolo/post-combate/descenso (Esc 4/5/8), 1 enemigo, salida → Level1. |
| **Boss** | approach / ataque alto / ataque bajo / bloqueo / shove, fase 2 al 50 % vida (telegrafiado más corto + shove), rendición a 0 HP (no muere). Narrativa cableada: `BossIntroTrigger` → señal `phase_changed` → señal `surrendered` → recuerdo "El último día" → Epílogo → pantalla de cierre. |
| **UI** | TitleScreen (logo + placas), PauseMenu (placa + botones), Credits, DialogueBox, HUD — todo con arte propio (sesión 2026-08-27). Transiciones con fundido entre todas las escenas. |

---

## 2. Qué funciona PARCIALMENTE

1. **Penitencia / corrupción** (pilar GDD 3, brief §11) — solo respawn. La corrupción por muerte (+enemigos / −luz, reset al completar el nivel) **no está implementada**; `player.gd` lo dice explícito. Arte disponible sin extraer: `penitence_corruption_ui_sheet`, `arcane_corruption_floor_tiles`, `supernatural_corruption_atlas`.
2. **Level 1 como "arqueología"** (brief §7) — hoy es un plataformas greybox. Tiene el esqueleto (enemigos, hazard, rama, fragmentos, aproximación al boss) pero **no** la progresión "Vaelith estuvo aquí": sin verbo reconocimiento, sin cadáveres/mecanismos/símbolos interactivos, sin engendros que reaccionen. Los `DialogueTrigger` agregados ("huellas del constructo") son texto sobre un `Area2D`, no gameplay integrado.
3. **Fragmentos de memoria** (brief §6) — disparan al **cruzar** un `Area2D` → `DialogueBox` con texto plano. El brief pide "escenas breves, traumáticas, fragmentarias" y "como consecuencia de determinadas interacciones". El contenido ya es el guion nuevo; falta el tratamiento visual y el cambio de disparo.
4. **Enemigos que reconocen a Vaelith** (brief §9) — `enemy_regular.gd` es Idle → Alerta → Ataque plano. Sin "observar / reconocer / huir / reaccionar antes de combatir".
5. **Intro** — Esc 1/3/4/5/8 como texto sobre el tramo corto actual. **Esc 6** (presencia espectral) y **Esc 7** (la puerta que no abre al volver) sin escenificar (faltan nodos). **Falta el pickup de armas**: el guion Esc 3 dice "al tomar la espada" pero Vaelith ya la tiene equipada.
6. **Boss como espejo psicológico** (brief §12/§13) — refleja el kit mecánicamente ✓, la revelación está en el diálogo ✓. Pero "reconoce comportamientos del jugador" durante el combate **no** está (la fase 2 solo es más rápida + una línea genérica). Sin fintas.
7. **Cámara** — `player.gd` tiene lookahead funcional **más** configuración muerta duplicada (`camera_lookahead_distance` / `camera_lookahead_lerp_speed` vs. el `position_smoothing` del nodo `Camera2D`). Zoom 2.5 hardcodeado en `Player.tscn`. Por escena solo se overridean límites. Funciona; falta un pase de tuning.

---

## 3. Qué está ROTO / bugs

| # | Bug | Estado |
|---|---|---|
| 1 | **Alineación de pie con el suelo** | Vaelith y boss corregidos (offset `-31` → `-25`). No-muerto (`-35`) y espíritu (`-38`) sin tocar (cálculo < 1 px, pero el reporte fue "nadie"); Bringer sin verificar. **Falta confirmación visual en editor.** |
| 2 | **"Dos Vaeliths" al atacar** | Corregido: `attack1_1.png` era una doble figura de la extracción. **Causa raíz = el pipeline**: las composiciones IA no tienen grid y el etiquetado de componentes conexos fusiona poses adyacentes. Las hojas nuevas repetirán esta clase de bug al re-extraer. |
| 3 | **Animaciones de Vaelith mal mapeadas** en `_frames.tres` | `jump` = frames de `idle`; `fall` = frames de **`attack1`** (saltar/caer muestra un tajo); `attack2` / shove = `idle` (sin ataque visible); `hurt` = frames de **`death`**. Visible en juego. El `vaelith_knight_sheet` nuevo trae jump/block/attack2 reales → re-extracción lo resuelve. |
| 4 | **Boss `fall` = `attack1`** | Mismo problema en `espejo_boss_custom`. |
| 5 | **`Main.tscn` + `test_driver.gd` + `level1_test_driver.gd`** | Sandbox de pruebas fuera del flujo (la main scene es `TitleScreen`). No está roto pero es peso muerto. Decidir: mover a `tools/` o borrar. |
| 6 | **Docs obsoletos** | `guion_intro.md` y `guion_desenlace.md` sin uso. Comentarios stale en `memory_fragment.gd` y `dialogue_box.gd` (citan "Despertar en la oscuridad.pdf", canon reemplazado por `guion_demo.md`). `Roadmap.md` / `CHANGELOG.md` desactualizados (dice/hace). |
| 7 | **DialogueBox** | Panel `ColorRect` plano; sin distinción visual entre narración y voz (el guion mezcla mucho las dos). Arte de marco disponible: `dialogue_box_frames`. |

---

## 4. Qué FALTA para la experiencia del brief

- Toda la capa **LORE ↔ GAMEPLAY integrado** (brief §3/§9): reconocimiento, cadáveres interactivos, espíritus liberables, mecanismos necrománticos, símbolos reconocibles, engendros reactivos, memoria como consecuencia de interacción.
- **Corrupción/penitencia como sistema** (arte listo, mecánica en stub).
- **Pase de arte de Level 1**: hoy `StaticBody2D` + `ColorRect`. Tilesets, arquitectura, cementerio, árboles, cielos, fuego → en `assets/source_sheets/` sin extraer. El `TileSet` de Godot conviene armarlo con el editor abierto (ya lo indica el Roadmap Fase 4.2).
- **Arena del boss** (`mirror_warrior_arena_sheet`) — hoy un `TextureRect` gris.
- **VFX** de golpe / parry / muerte / flash de memoria (`combat_vfx_sheet` sin extraer).
- **Audio** — Etapa 8 intacta (cero archivos, cero buses).

---

## 5. Qué conviene PRESERVAR (arquitectura sana — no tocar la forma, solo extender)

- **Combate hitbox/hurtbox desacoplado** (`class_name`, señales; maneja el caso "ya solapado al activar `monitoring`").
- **Patrón de interacción** `Area2D + body_entered + already_active`, reutilizado en checkpoint / diálogo / memoria / transición de escena / calavera. Es la base natural para el verbo reconocimiento y los objetos interactivos del brief.
- **Autoloads** limpios: `InputSetup` (input map por código), `TransitionManager` (fundido awaitable; maneja árbol pausado en el destino), `DialogueBox` (`show_lines` / `ask_choice` / señal `finished`), `GameState` (contadores, sin guardado — coincide con el GDD), `PauseMenu`.
- **Enemigo genérico** (`enemy_regular.gd` + `@export` por escena: `ground_patrol` vs `float_sway`) y **decoupling boss ↔ narrativa** (el boss emite señales, `level1_controller.gd` decide qué pasa).
- **HUD por grupos** (`get_first_node_in_group`), no por ruta fija → instanciable en cualquier nivel.
- **`guion_demo.md`** como fuente de verdad narrativa (brief §5/§12: no reemplazar el guion por diálogos nuevos).

---

## 6. Plan de implementación por fases

Orden del brief §15 (estabilidad → movimiento → combate → cámara → escenario →
enemigos → interacción → memoria → narrativa → boss → pulido). Regla transversal
(§16): si aparece una falta de asset concreta, detenerse y anotarla en
`docs/ASSETS_PENDIENTES.md`; nada de generación por adelantado.

| Fase | Contenido | Riesgo |
|---|---|---|
| **0 · Contexto persistente** *(docs, sin código)* | `docs/BRIEF_IMPLEMENTACION.md` · `CLAUDE.md` de proyecto (raíz) → brief + guion + auditoría + reglas del repo · cerrar limpieza de docs (obsoletos, `CHANGELOG`, `Roadmap`) · rama `feature/produccion-vertical-slice` | nulo |
| **1 · Estabilidad** | confirmar alineación de pie en editor (todos) · re-extraer `vaelith_knight_sheet` → jump/fall/block/attack2/hurt reales + recalibrar offset; ídem boss (`spectral_knight_violet_sheet`) y los 2 enemigos · decidir `Main.tscn` / test drivers · smoke test headless verde por cambio | medio (re-extracción) |
| **2 · Movimiento** | playtest real de `stats_personaje.md` (nunca se cerró la Fase 1.5) · ajustar salto/coyote/aire si "se siente" mal · documentar | bajo |
| **3 · Combate** | verificar las 4 acciones + postura/stagger/i-frames en juego real · VFX de golpe/parry/muerte desde `combat_vfx_sheet`, disparados por `hitbox` / `_register_block` / `_die` · **sin mecánicas nuevas** | bajo |
| **4 · Cámara** | unificar el lookahead (sacar la config muerta) · zoom/límites/smoothing como parámetros por escena · pase de tuning | bajo |
| **5 · Escenario (arte Level 1)** | `TileSet` de Godot desde `level1_ruins_tileset` (+ rocas/funerarias) en editor · reemplazar greybox por tiles + `gothic_architecture_atlas` + `gothic_cemetery_sheet` + `dead_trees_atlas` + `skulls_and_bones_atlas` · parallax con `gothic_skies_atlas` · fuego/luz con `fire_and_particles_sheet` (`PointLight2D` + sprite) · arena del boss desde `mirror_warrior_arena_sheet` · hazard C = `arcane_corruption_floor_tiles`. Objetivo §7: 1er tercio solo muerte → símbolos que reconoce → mecanismos con su conocimiento → restos de experimentos | alto (volumen) |
| **6 · Enemigos** | estado previo opcional `OBSERVE` / `RECOGNIZE` en `enemy_regular.gd` (`@export reacts_to_vaelith`): beat de observación (+ línea corta opcional) antes de `ATTACK` · re-extraer arte de los 2 enemigos con sus hojas nuevas | medio |
| **7 · Interacción (núcleo brief §3/§9)** | nodo base `InteractableArea` (patrón `Area2D + already_active` + prompt `[E]` + señal `interacted`) · `RecognitionPoint` (mecanismo que Vaelith usa "sin saber por qué" → cambia el recorrido) · `Corpse` (`@export mode: decoración/memoria/espíritu/reanima/info`, un set-piece por modo) · `BoundSpirit` liberable (1–2, sin sistema moral) · `NecromanticMechanism` (palanca reinterpretada). Todo reutiliza DialogueBox/GameState/TransitionManager | medio |
| **8 · Memoria** | `MemoryFragment` pasa a `InteractableArea` (consecuencia de interacción, no walk-through) · tratamiento visual: flash/viñeta/desaturación + panel con marco · mapear los 6 hitos del brief §6 a fragmentos concretos (Intro I; Level 1 II/III/…; boss "El último día") | bajo |
| **9 · Narrativa** | `DialogueBox` con marco real (`dialogue_box_frames`) + distinción narración vs. voz (color/sangría/prefijo `—`) · verificar el hilo completo contra `guion_demo.md` · Esc 6/7 de la Intro con nodos reales (presencia espectral pasiva; círculo ritual desde `supernatural_corruption_atlas`) · pickup de armas en la Intro (`dark_weapons_and_armor_catalog`) | bajo |
| **10 · Boss** | contador de comportamientos del jugador (bloqueos seguidos, spam de ataque alto, uso de shove) → callouts no bloqueantes en fase 2 (líneas ya en el guion: "La espada." / "El escudo." / "La distancia.") · opcional: finta (telegrafiar y cancelar) como variante de fase 2, sin moveset nuevo · re-extraer `spectral_knight_violet_sheet` | medio |
| **11 · Pulido AV** | corrupción/penitencia **solo si lo anterior es sólido** (§11): UI desde `penitence_corruption_ui_sheet` + efecto de nivel (más enemigos / menos luz) + `arcane_corruption_floor_tiles` como decoración progresiva · audio (buses sagrado/corrupto, SFX mínimos, música) · decals/agua/ítems como dressing final | medio |

## Progreso

**2026-08-27 (misma sesión):**
- Fase 0 completa. `Main.tscn` + test drivers → `tools/`.
- **Vaelith re-extraído** (`vaelith_knight_sheet`) — arregla el mapeo roto de
  `_frames.tres` (jump=idle, fall=attack1, attack2=idle, hurt=death). 13
  animaciones, canvas 320×240, offset `-50`. `player.gd` usa `block`/`shove`.
- **Boss re-extraído** (`spectral_knight_violet_sheet`) — mismo arreglo. 12
  animaciones. `boss1.gd`: `shove`/`block`/`stagger` con anim propia.
- **2 enemigos regulares: re-extracción DIFERIDA.** Se intentó 3 pasadas
  (huecos de columna y división en N). Las hojas `wandering_undead_sheet` y
  `bound_spirit_sheet` empaquetan las figuras muy juntas, con estela/FX que
  puentea frames vecinos, y tienen secciones de referencia laterales (HITBOX,
  DETALLE, PALETA) que caen dentro de las cajas de fila. Ninguna pasada dio
  frames promocionables. Como estos enemigos **no tienen el bug de mapeo** que
  tenían Vaelith y el boss (`enemy_regular.gd` ya mapea bien; solo `hurt`
  reusa `idle`), y por la regla del brief §15 ("no rehacer lo que funciona"),
  se dejan los frames actuales. Retomar cuando haya tiempo para un framing
  manual fila por fila (o con el editor para recortar visualmente).
- **Pendiente sin editor**: confirmar alineación de pie de Vaelith y boss en
  movimiento. Bloquea el cierre formal de Fase 1 pero no el avance.
- **Fase 9 (prep)**: `DialogueBox` con marco propio (`options_frame` como
  `NinePatchRect`) + narración (gris) vs. voz (dorado). `narration_frame`
  extraído para Fase 8.
- **Fase 7 (base)**: `InteractableArea` (Area2D + prompt `[E]` + señal
  `interacted` + `one_shot`) y `RecognitionPoint` (el verbo distintivo:
  reconocimiento → señal `acted` → memoria opcional). Con escenas base.
  Infra lista; la primera instancia concreta se pone cuando una sección del
  nivel la necesite (brief §16). `Corpse` / `BoundSpirit` /
  `NecromanticMechanism` pendientes, mismo criterio.

---

## Rework Level 1 largo (2026-08-27, aprobado)

La visión de la Escena 1 se amplió: torre del nigromante → gauntlet de undead
en el bosque (≥10 enemigos, 3 clases, 2 golpes) → travesía recolectando
memorias → 2ª torre → arena del constructo. Plan por fases y mapa asset→sector
en **`docs/roadmap_level1_largo.md`**.

**Fase 0 en curso:**
- ✅ **Zombi devorado** extraído (`zombi_devorado_custom`, 7 anims, `Zombi.tscn`)
  — 3ª clase de undead. Hoja `Zombie.png` bien maquetada (48×64), extracción
  limpia.
- Pendiente Fase 0: `TileSet` 32×32 de `level1_ruins_tileset`, atlas de
  props/VFX (árboles, huesos, arquitectura, cementerio, fuego, decals, arena,
  combat_vfx).
