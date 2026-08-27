# Lista de Audio (Música y SFX)

Checklist de audio de la demo, cruzado contra `BRIEF_IMPLEMENTACION.md`,
`AUDITORIA_2026-08-27.md`, `guion_demo.md`, `GDD.md` y el estado real del código
(`player.gd`, `boss1.gd`, `enemy_regular.gd`, `level1_controller.gd`,
`epilogue_controller.gd`, autoload `MemoryFlash`, `RecognitionPoint`).

**Leyenda de estado:**
🔴 Custom obligatorio (momento narrativo único) ·
🟡 Curado a mano de un pack (elegir timbre con cuidado) ·
🟢 Cualquier pack genérico resuelve.

Identidad musical (pilar de diseño del GDD): **dos capas — coral/sagrada vs.
drone/distorsión corrupta — mezcladas dinámicamente** según el nivel de
"penitencia". Referencias de tono: SLAIN!, Castlevania (SotN), Dark Souls,
Bloodborne, Diablo.

---

## 1. Música 🔴 — prompts de Suno

Todos **instrumentales** (Suno mete voces con letra si no se aclara: poner
`[Instrumental]` + "no vocals / wordless choir only"). Suno corta ~2 min (v4) /
~4 min (v4.5): generar la sección y loopear en Godot. Guardar **stems** si se
puede (sirven para el mix dinámico sagrado/corrupto). Generar 3–4 tomas y elegir.

### 1.1 · Intro — "El despertar"

**Style (campo Style):**
`dark ambient, gothic sacred, mournful, wordless female choir, sub bass drone, solo cello, tolling bell, slow, rubato, minor, cinematic, no drums, instrumental`

**Descripción:**
> Vaelith despierta sobre piedra cubierta de ceniza, sin memoria, con frío en los
> huesos. Empieza casi en silencio: viento, respiración, un drone de sub-bajo
> apenas audible. Alrededor de los 20–30 s entra un coro femenino sin palabras,
> muy lejano, y un violonchelo solo con frases lentas y quebradas. Una campana
> grave suena una sola vez, con mucho reverb. En el minuto y medio, una
> disonancia breve y fría (cluster de cuerdas, campana desafinada) = un fragmento
> de memoria que irrumpe; se disipa y todo vuelve a una sola nota sostenida.
> Contemplativo, funerario, inquietante. Sin percusión rítmica, nada épico. La
> capa "sagrada" domina pero suena enferma.

**Parámetros:** ~55–62 BPM (sin pulso marcado) · menor / eólico o frigio ·
1:30–2:30 · **evitar:** batería, guitarras, sintes brillantes, cualquier cosa
heroica.

### 1.2 · Level 1 — "El sendero del umbral" (exploración + combate leve)

**Style:**
`gothic doom, dark fantasy, church organ, low latin choir, detuned distorted guitar drone, tremolo strings, taiko toms, chains percussion, harpsichord motif, mid tempo, minor, tritone, loopable, instrumental`

**Descripción:**
> El jugador cruza una ruina que revela que Vaelith estuvo ahí: cadáveres,
> símbolos que reconoce sin saber por qué, mecanismos necrománticos. Base de
> exploración: pedal de órgano de iglesia, coro grave (sílabas tipo latín, sin
> letra real), y debajo un drone de guitarra distorsionada y desafinada que
> corrompe la armonía. Cuerdas en trémolo, toms graves y percusión metálica
> (cadenas, yunque) marcando un pulso lento y pesado. Un motivo corto de clave
> aparece y desaparece. Debe loopear sin final. Que se sienta como dos músicas
> peleando: la sagrada y la corrupta. Deliberado, denso, amenazante — no
> frenético.

**Variante de combate (generar aparte, mismo material):** subir intensidad —
entran toms/batería marcial, la guitarra distorsionada al frente, coro más
agresivo. Misma tonalidad y tempo para poder crossfade contra la base.

**Parámetros:** ~85–95 BPM · menor con movimiento cromático, tritono presente ·
1:30–2:00 loopeable · **evitar:** finales resueltos, secciones alegres, breaks de
EDM.

### 1.3 · Boss — "El Espejo" (Guerrero-Espejo)

**Style:**
`epic gothic metal, dark orchestra, aggressive SATB choir, downtuned rhythm guitar, controlled double kick, brass stabs, staccato strings, pipe organ, war drums, 4-note mirror motif, phrygian dominant, tritone, two phases, instrumental`

**Descripción:**
> Vaelith pelea contra una versión más experimentada de sí mismo — un constructo
> que él creó y que conoce su forma de luchar. **Fase 1 "el reflejo":** marcial y
> conducida — coro completo agresivo, guitarra rítmica afinada grave, estocadas
> de metales orquestales, cuerdas staccato, órgano, tambores de guerra. Un motivo
> reconocible de 4 notas ("el espejo") que se repite. **Fase 2 "lo que Vaelith
> olvidó":** más rápido y disonante, la capa corrupta rompe la barrera — el
> motivo de 4 notas ahora suena invertido / al revés (el boss "aprende"), el coro
> pasa de cantar a gemir, half-time drops bruscos. Terminar con un **corte seco a
> silencio** (cae la máscara, empieza el diálogo). Sin outro épico.

**Parámetros:** Fase 1 ~130–145 BPM · Fase 2 ~150–160 BPM con caídas a half-time
· menor / frigio dominante, mucho tritono · generar Fase 1, Fase 2 y un stinger
de intro (los dos se enfrentan: silencio, luego un acorde de órgano) por
separado · **evitar:** voces con letra, breakdowns de metalcore moderno,
triunfalismo, fade-out (hace falta corte seco).

### 1.4 · Silencios que la música debe respetar (del guion)

- Arranque de la Intro: solo viento, **sin música** hasta la Escena 8.
- Post-rendición del boss: **2–3 s de silencio total** antes de cualquier corte.
- Epílogo ("Regreso al presente" + pantalla de cierre): fundido lento, **sin
  música nueva**.

### 1.5 · Estado de tracks

- [ ] 1.1 Intro
- [ ] 1.2 Level 1 — exploración (loop)
- [ ] 1.2b Level 1 — variante de combate
- [ ] 1.3 Boss — stinger de intro
- [ ] 1.3 Boss — Fase 1 (loop)
- [ ] 1.3 Boss — Fase 2 (loop)

**Referencia de tono (NO para producción, solo para calibrar):**
- [Dark + Music, gratis, itch.io](https://itch.io/game-assets/free/tag-dark/tag-music)
- "(Free) Dark Dungeon Ambient Music Vol. 2 — 13 tracks (juanjo_sound)" (buscar por nombre en itch.io)

---

## 2. SFX de personaje (Vaelith) — `player.gd`

| SFX | Dispara en | Prio |
|---|---|---|
| Pasos sobre piedra (2–4 variantes) | movimiento con `is_on_floor()` | 🟢 |
| Salto (esfuerzo + tela/armadura) | estado → salto | 🟢 |
| Aterrizaje (peso, "tank") | vuelve a `is_on_floor()` tras caer | 🟢 |
| Swing espada — ataque alto | `ATTACK_HIGH` | 🟢 |
| Swing espada — ataque bajo (más corto) | `ATTACK_LOW` | 🟢 |
| Impacto espada → carne/hueso | `Hitbox` conecta en enemigo | 🟢 |
| Impacto espada → escudo (bloqueo) | `_register_block()` | 🟡 |
| Rotura de postura (guardia rota) | 4º bloqueo seguido → `STAGGERED` | 🟡 |
| Embestida / Shove (whoosh grave + esfuerzo) | `SHOVE` | 🟢 |
| Recibir daño (gruñido + impacto en armadura) | `_take_damage()` | 🟢 |
| **Muerte** (colapso pesado + eco, no genérico) | `_die()` | 🔴 |
| **Resurrección / respawn** (inhalación, susurro sagrado, campana — Pharasma) | `_respawn()` | 🔴 |

---

## 3. SFX de enemigos regulares — `enemy_regular.gd`

### No-muerto errante
| SFX | Dispara en | Prio |
|---|---|---|
| Arrastre / paso óseo | `ALERT` (aproximación) | 🟡 |
| Detección (chasquido / gruñido seco) | `IDLE → ALERT` | 🟡 |
| Anticipación de espadazo (tensión de arma) | `ATTACK` windup | 🟢 |
| Impacto recibido | `_on_hurt()` | 🟢 |
| Destrucción (huesos cayendo) | `_die()` | 🟡 |

### Espíritu atado
| SFX | Dispara en | Prio |
|---|---|---|
| Drone de flotación (loop posicional) | `IDLE` / `ALERT` (`float_sway`) | 🟡 |
| Lunge (siseo agudo con doppler) | `ATTACK` | 🟡 |
| Impacto recibido (etéreo) | `_on_hurt()` | 🟢 |
| Disipación / grito ahogado | `_die()` | 🔴 |

### BringerOfDeath (guardián único pre-arena)
| SFX | Dispara en | Prio |
|---|---|---|
| Presencia (drone grave único) | al entrar a su zona | 🟡 |

---

## 4. SFX del Boss "El Espejo" — `boss1.gd` + `level1_controller.gd`

| SFX | Dispara en | Prio |
|---|---|---|
| Aparición: pasos + silencio (no ataca todavía) | `BossIntroTrigger` | 🔴 |
| Swing alto / bajo / shove del boss | `ATTACK_HIGH/LOW/SHOVE` | 🟢 (reusar SFX de Vaelith con pitch/reverb distinto) |
| Telegrafiado de fase 1 (brillo del filo) | `_update_telegraph_visual()` | 🟡 |
| **Máscara se agrieta — transición a fase 2** | `_enter_transition()` / señal `phase_changed` | 🔴 |
| Bloqueo (guardia especular) | `BLOCK` / `_register_block()` | 🟢 |
| **Rendición — baja el arma, la máscara toca el suelo** + luego silencio total (2–3 s) | `_surrender()` | 🔴 |
| "Voz" / aliento del boss por línea (si no se graban voces reales) | cada `DialogueBox.show_lines` del boss en `level1_controller` | 🔴 |

Notas: el boss **no muere**, se rinde — no hay "boss death SFX" genérico; es
`_surrender()` + silencio. Las líneas ya están en `guion_demo.md` ("Todavía hacés
eso" / "Cargás primero" / "Eso es lo que viniste a recordar").

---

## 5. SFX del sistema de memoria — `MemoryFlash` (autoload) + `RecognitionPoint` + `MemoryFragment`

| SFX | Dispara en | Prio |
|---|---|---|
| **Fragmento de memoria obtenido** (whoosh + sting frío + coro invertido corto — NO un "pickup" genérico) | `GameState.memory_collected` → `MemoryFlash.flash()` | 🔴 |
| **Reconocimiento** ("tu cuerpo sabe") — pulso sordo, sub-bass + campanita desafinada | `RecognitionPoint._do_interact()` | 🔴 |
| Vaelith ejecuta la acción reconocida (girar rueda / mecanismo necromántico) | `RecognitionPoint` señal `acted` | 🟡 |
| Presencia espectral que observa (Esc. 6 de la intro, no ataca) | trigger de esa escena (pendiente de crear) | 🔴 |

---

## 6. SFX ambientales (loops posicionales) — Intro / Level 1 / arena

| SFX | Dónde | Prio |
|---|---|---|
| Viento (loop) — arranque de la Intro, sin música | `intro_controller._ready` | 🟢 |
| Eco de cripta / sala grande (reverb bed) | Level 1 tramo F + arena | 🟢 |
| Goteo de agua | tramos húmedos | 🟢 |
| Crujido de piedra / estructura asentándose | random en Level 1 | 🟢 |
| **Campana lejana** (detalle del prólogo) | Intro + transición a Level 1 | 🟡 |
| Fuego / antorchas (loop) | props de `fire_and_particles` al integrarse | 🟢 |
| Fortaleza en llamas (flashback "El último día") | recuerdo del boss en `level1_controller` | 🟡 (fuego + sirenas + gritos lejanos, mezcla baja) |
| Corrupción / drone arcano | focos de corrupción (sistema aún no implementado) | 🔴 |

---

## 7. SFX de UI — `title_screen.gd`, `pause_menu.gd`, `dialogue_box.gd`, `hud.gd`, `credits_controller.gd`, `transition_manager.gd`

| SFX | Dispara en | Prio |
|---|---|---|
| Navegar menú (hover / foco de botón) | `grab_focus` en Title/Pause/Credits | 🟢 |
| Confirmar (Iniciar / Continuar / Salir) | `pressed` | 🟢 |
| Abrir menú de pausa | `PauseMenu._try_open()` | 🟢 |
| Cerrar pausa / reanudar | `_close()` | 🟢 |
| Avance de línea de diálogo (blip suave, no "typewriter" chillón) | `DialogueBox._advance()` | 🟡 |
| Aparición del marco de diálogo (roce piedra/metal muy corto) | `DialogueBox.show_lines()` | 🟡 |
| Daño en HUD (pulso grave sordo) | `hud._on_health_changed` al bajar | 🟢 |
| Calavera recogida | `skull_collectible.gd` | 🟢 |
| Checkpoint activado (acorde sacro corto — Pharasma te marca) | `checkpoint.gd` | 🟡 |
| Transición entre escenas (swell + caída de reverb) | `TransitionManager.goto_scene` | 🟡 |
| Pantalla de cierre ("La deuda continúa" → "VAELITH ARKEN") — golpe grave único + cola larga | `epilogue_controller` | 🔴 |

---

## 8. Resumen ejecutivo

### 8.1 · Custom obligatorio (🔴)

**Música:** los 3 temas (§1) + variante de combate de Level 1 + stinger y 2 fases
del boss = **6 tracks**.

**SFX custom (11):**
1. Muerte de Vaelith
2. Resurrección / respawn
3. Disipación del espíritu atado
4. Máscara se agrieta (fase 2 del boss)
5. Rendición del boss + silencio
6. Presencia del boss al aparecer
7. "Voz" / aliento del boss por línea
8. Jingle de fragmento de memoria (`MemoryFlash`)
9. Sting de reconocimiento (`RecognitionPoint`)
10. Presencia espectral (Esc. 6 de la intro)
11. Golpe de la pantalla de cierre

### 8.2 · Resuelto con packs (🟢 / 🟡)

Pasos, espada, impactos, ambiente, UI, pickups → estos packs cubren la mayoría:

| Pack | Cubre | Licencia |
|---|---|---|
| [Free Fantasy 200 SFX Pack (TomMusic)](https://tommusic.itch.io/free-fantasy-200-sfx-pack) | +20 SFX de espada, +50 de pasos (incl. piedra), UI básica | royalty-free, uso comercial |
| [Sword Combat Sound Effects Pack — Free (Hove Audio)](https://hoveaudio.itch.io/sword-combat-sound-effects-pack-free-version) | slashes, estocadas, colisiones, whooshes | free |
| [Horror Ambiences Sound Effects Pack — Free (Hove Audio)](https://hoveaudio.itch.io/horror-ambiences-sound-effects-pack-free-version) | viento, drones, eco de cripta, texturas | free |
| [Footsteps Sounds (The Sound Guild)](https://the-sound-guild.itch.io/footsteps-sounds) | 107 pasos, incl. piedra (alternativa/complemento) | ver página |
| [Free Fantasy UI SFX](https://itch.io/game-assets/free/tag-sound-effects/tag-user-interface) | selección/confirmar/pausa (si los de arriba no alcanzan) | ver por pack |

**Descarga:** itch.io gatea la descarga detrás de un flujo JS con sesión de
navegador — no es scripteable de forma confiable (misma nota que en `CREDITS.md`,
sección "Pendientes de descarga manual"). Bajarlos a mano y dejarlos en
`Herramientas/Pixelherramientas/` o equivalente; al integrarlos se documentan en
`CREDITS.md` con licencia y atribución.

### 8.3 · Integración en Godot (pendiente, Etapa 8 / Fase 11 de la auditoría)

- Buses de audio: `Master` → `Music` (con dos sub-buses `Music_Sacred` /
  `Music_Corrupt` para el mix dinámico) → `SFX` → `Ambient` → `UI`.
- Autoload `AudioManager` (aún no existe): reproducir música por escena,
  crossfade entre exploración/combate, y ajustar el balance sacred/corrupt según
  un futuro nivel de "penitencia".
- SFX de personaje/enemigo: `AudioStreamPlayer2D` hijo de cada escena, disparado
  desde las señales que ya existen (`Hitbox`, `hurt`, `_die`, `phase_changed`,
  `surrendered`, `memory_collected`, `interacted`).
