# Análisis: herramientas de GitHub para edición de sprites, calidad, game feel y orquestación con IA (2026-09-09)

## Contexto

Continuación de `analisis_herramientas_ia_pixel_art.md`. Marcos pidió buscar
herramientas para: (1) editar el pixel art que ya tenemos, (2) corregir errores
de sprites y mejorar su calidad, (3) que las interacciones/animaciones no
parezcan tan toscas, (4) skills y agentes para orquestar el desarrollo de un
juego indie como este.

Cada ítem se verificó por búsqueda web real (existe el repo, licencia, actividad,
si corre offline). **No se instaló ni probó nada** — es verificación de
existencia y plausibilidad. El entorno impone restricciones: Windows, PowerShell,
Python miniconda 3.9, **red con interceptación SSL de Avast** (ver
`Documents/Claude-Vault/Leyes/Red-y-SSL.md`), Godot 4.7. Las skills que tocan
red / instalan deps están **gateadas** (`Leyes/Skills-y-Triggers.md`).

---

## 1. Editar el pixel art que ya tenemos

| Herramienta | Aporte sobre LibreSprite | Licencia / estado | Encaje |
|---|---|---|---|
| **Pixelorama** (`Orama-Interactive/Pixelorama`) | Editor hecho en Godot. Animación con onion-skin, frame tags, tilemap nativo, export a spritesheet/gif/video. Más fuerte en animación y tilemaps que LibreSprite. | MIT, ~9k ★, muy activo | **Alto** — local, sin red. Ya anotado en el análisis previo como alternativa sólida. No reemplaza LibreSprite, lo complementa. |
| Aseprite CLI | Scripting batch (`--batch`, Lua). | Pago | Solo si se compra Aseprite. |

---

## 2. Corregir errores de sprites y mejorar calidad

| Herramienta | Qué hace | Licencia / estado | Encaje |
|---|---|---|---|
| **PixelRefiner** (`HappyOnigiri/PixelRefiner`) | Quita antialiasing ("crispa" bordes borrosos), detecta grilla, conversión de paleta, quita fondo, **genera contorno**, limpieza de ruido, **batch con descarga ZIP**, Web Workers. | MIT, 232 ★, **973 commits, activo** | **Alto**, pero es **web / dev server local** (sin CLI). La web pública (`pixel-refiner.app`) se puede probar sin instalar nada. Correr local necesita `npm install` (SSL). |
| **Pixel-Perfect-Aligner** (`CombinEC-R/Pixel-Perfect-Aligner`) | Plugin de GIMP 3. Re-muestrea a grilla objetivo. Feature clave: **fix de alpha-bleed / halos oscuros** en Godot. También contorno, alpha binario, reducción de paleta (K-Means). | MIT, 7 ★, 5 commits — **inmaduro**, GUI, **sin batch** | **Medio** — la corrección de halo es exactamente lo que sufren los sprites con alpha en Godot, pero el proyecto está muy verde. |
| **sprite-gen** (`aldegad/sprite-gen`) | **Es una skill de Claude/Codex.** Limpieza de croma con unmix de alpha suave, extracción de frames, composición de atlas + manifiesto runtime, recolor, exports a motor. Verbos: `prepare`, `gen-set`, `extract`, `compose-atlas`. | Apache-2.0, 836 ★ | **Medio** — las etapas de *generación* necesitan API de Codex/Grok (paga, red). Las utilidades de extracción/atlas quizá sirven sueltas. **Python 3.10+** (choca con la norma del 3.9). |
| `proper-pixel-art` | Detecta grilla + **paleta compartida entre frames** (anti-flicker). | MIT | Ya evaluado: **necesita Python ≥3.10**, bloqueado por la norma del 3.9. |
| `pixelfixer` | Detección de grilla + reconstrucción. | MIT | **Ya vendorizado** en `tools/img_pipeline/vendor/`. |

---

## 3. Que las animaciones/interacciones no parezcan tan toscas

Son **dos problemas distintos**.

### 3a. Suavizar animaciones (lado asset)

| Herramienta | Qué hace | Licencia / estado | Encaje |
|---|---|---|---|
| **bitmapflow** (`Bauxitedev/bitmapflow`) | Genera **inbetweens por optical flow** (SimpleFlow / DenseRLOF): frames intermedios que suavizan la animación. Entrada/salida: gif, spritesheet, frames sueltos. GUI. | MIT, 463 ★, godot-rust, Windows/Linux | **Medio** — sirve para suavizar ciclos de correr/caminar. Límites: solo movimiento en plano 2D, **no** sirve con cambios de brillo / explosiones / partículas, necesita pixel art sin escalar. El repo muestra error al cargar — mantenimiento incierto. |

### 3b. Game feel (lado Godot — probablemente esto es lo "tosco")

| Addon | Qué da | Licencia / estado |
|---|---|---|
| **Juicee** (`Kelpekk/Juicee`) | Editor visual de grafos estilo *FEEL*. `Juicee.shake_camera(self, 12.0, 0.3)`, `Juicee.hit_stop(self, 0.08)`, springs (squash & stretch), damage numbers, shaders de pantalla. | MIT, 134 ★, addon Godot 4 |
| **Coyote Jump** (`marianokpo/coyote_jump`) / Controller no-code (selodev, itch) | Coyote time, **jump buffering**, altura de salto variable. | Godot 4.x |
| Screen shake / hitstop autoloads | Recetas de código sueltas (kidscancode Godot 4 Recipes). | — |

**Restricción de diseño:** el pilar 1 del GDD es "movimiento sin margen de
error, control aéreo mínimo o nulo". **Coyote time va en contra del diseño.**
Pero jump buffering, hitstop, screen shake y un frame de anticipación claro en
los ataques (ya en `guia_estilo_visual.md` §3) suman "peso" sin traicionar el
diseño SLAIN/Volgarr.

### 3c. Pipeline de import

| Herramienta | Qué hace | Licencia / estado | Encaje |
|---|---|---|---|
| **godot-aseprite-wizard** (`viniciusgerevini/godot-aseprite-wizard`) | Importa tags de Aseprite → animaciones de Godot 4 (`AnimationPlayer` / `SpriteFrames`). Filtro de capas por regex, slices, ping-pong, conversión de duración a FPS. | MIT, **1.4k ★**, maduro, Godot 4 | **Alto ROI** — reemplazaría el armado manual de `_frames.tres`. Necesita el CLI de Aseprite; **falta confirmar compatibilidad con LibreSprite (`--batch`)**. |

---

## 4. Skills y agentes para orquestar un juego indie

| Repo | Qué es | Licencia / estado | Encaje con el estudio |
|---|---|---|---|
| **Coding-Solo/godot-mcp** | MCP server: lanzar editor, correr proyecto en debug, **capturar errores y salida de consola**, crear escenas, agregar nodos, cargar sprites. `claude mcp add godot -- npx @coding-solo/godot-mcp`. | MIT, **5.6k ★**, TS/Node, el más establecido | **GATED** (`npx`/`npm` → SSL). El más seguro para empezar. Resolvería el "no hay Godot en el PATH" que dejó pendiente el pase visual toda la sesión del 09-09. |
| **tugcantopaloglu/godot-mcp** | **157 tools, probado con Godot 4.7** (versión exacta del proyecto). TS/Node, Claude Code. Necesita un autoload en el proyecto. | MIT, 452 ★, activo | **GATED**. Más completo, más nuevo, menos rodado. |
| **Donchitos/Claude-Code-Game-Studios** | Formato **oficial de skills + subagents** de Claude Code. 49 agentes en jerarquía de estudio, 73 slash commands, 12 hooks, targets Godot 4 / Unity / UE5. **Deliberadamente colaborativo**: los agentes preguntan y piden aprobación antes de actuar. | MIT, **24.9k ★** | **Alto como referencia.** Su filosofía "pregunta / aprueba / review gates" calza con `00_Normas_de_Trabajo` §3-4. Adoptarlo entero cambia cómo trabajamos; sirve de modelo para estructurar agentes propios que respeten las normas. |
| **AlterLab-IEU/AlterLab_GameForge** | 34 skills indie dev, formato Claude Code, especialistas por motor, CI validation (486 checks). | MIT, 35 ★ | Versión más chica y curada del anterior. |
| **aaddrick/claude-pipeline** | Pipeline multi-agente con quality gates + **interacción autónoma con GitHub** (crea ramas / PRs / comenta solo). | — | **Choca con `00_Normas` §3 y §5** (notificar antes de cada commit, `git push` solo con la frase exacta). Solo viable con gating fuerte que desarme la parte autónoma. |
| **rohitg00/awesome-claude-code-toolkit** | Catálogo índice (135 agentes, 35 skills, hooks, MCP configs, plugins). | — | Referencia para descubrir más. |

---

## Recomendación

**Sin instalar nada (bajo riesgo):**

1. Estudiar `Claude-Code-Game-Studios` como **modelo** para estructurar agentes /
   skills propios que respeten las normas del estudio (roadmap → aprobación →
   commit atómico → `autorizo el push`). No adoptarlo entero.
2. Probar **PixelRefiner** (web pública, sin instalar) sobre 2-3 frames de
   `assets/sprites/player/vaelith_custom/` — ver si su limpieza de AA + grilla +
   contorno mejora la extracción actual.

**Con autorización (red / SSL, gated):**

3. **godot-aseprite-wizard** — el de más ROI: automatiza el armado de
   animaciones que hoy es manual (`_frames.tres`). Antes: confirmar si
   LibreSprite `--batch` es compatible con el CLI que espera.
4. **Coding-Solo/godot-mcp** — para correr escenas headless, capturar errores y
   tomar screenshots. Desbloquea el pase visual que quedó pendiente.
5. **Juicee** + jump buffering + hitstop — game feel, respetando el pilar de
   "movimiento comprometido" (sin coyote time).

**Backlog:**

- `bitmapflow` para suavizar ciclos de personaje (con sus límites).
- `Pixelorama` como segundo editor para animación / tilemaps.
- `Pixel-Perfect-Aligner` solo si aparece el problema de halos de alpha en Godot.

## Nota metodológica

Igual que el análisis previo: esto anota lo verificable por búsqueda a la fecha
(2026-09-09). Antes de instalar o depender de cualquiera de estos proyectos
corresponde revisión más profunda (leer el código, probarlo en branch aparte).
No es auditoría de seguridad ni de calidad.
