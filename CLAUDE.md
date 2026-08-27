# CLAUDE.md — Vaelith Arken

Contexto persistente del proyecto para sesiones de Claude Code. (Las reglas
personales de Marcos y del entorno viven en su `~/.claude/CLAUDE.md` global y
mandan por encima de esto.)

## Qué es

Plataformas de acción 2D dark fantasy en **Godot 4.7**. Demo vertical slice:
`INTRO → LEVEL 1 → GUERRERO-ESPEJO → RECUERDO FINAL → FIN`.

Vaelith Arken: elfo drow resucitado, ex-nigromante sin memoria consciente pero
con conocimiento procedural ("su cuerpo sabe lo que su mente olvidó"). Los no
muertos del mundo son consecuencia de sus actos. La historia se descubre
jugando, no leyendo.

## Documentos de verdad (leer antes de trabajar)

| Doc | Para qué |
|---|---|
| `docs/BRIEF_IMPLEMENTACION.md` | objetivo, identidad, principios, alcance, prioridades de producción |
| `docs/AUDITORIA_2026-08-27.md` | estado real del código + plan por fases (0–11) |
| `docs/guion_demo.md` | **fuente de verdad narrativa** — intro + fragmentos de Level 1 + Boss El Espejo + cierre. NO reemplazar por diálogos nuevos. |
| `docs/GDD.md`, `docs/stats_personaje.md`, `docs/diseno_enemigos.md`, `docs/layout_level1.md` | diseño base |
| `docs/guion_intro.md`, `docs/guion_desenlace.md` | **OBSOLETOS** — reemplazados por `guion_demo.md`, se conservan como referencia histórica |

## Principio rector

LORE Y GAMEPLAY INTEGRADOS. No "plataformas + enemigos + diálogos que cuentan la
historia", sino "cada acción del jugador también le revela quién era Vaelith"
(reconocer mecanismos propios, interactuar con cadáveres, liberar espíritus,
reconocer símbolos, engendros que reaccionan, memoria como consecuencia de
interacción).

## Reglas de trabajo

- **No generar assets nuevos.** Usar/adaptar los existentes. Si falta uno
  concreto para una sección: detenerse y anotarlo en `docs/ASSETS_PENDIENTES.md`.
- **No rehacer código que funciona** sin razón concreta. Preservar la
  arquitectura marcada en la auditoría §5.
- **No agregar mecánicas** fuera del brief (nada de doble salto/dash/wall
  jump/inventario/RPG) sin decisión explícita.
- Avanzar **por fases** (auditoría §6), en orden de prioridad. Commits atómicos
  (Conventional Commits), avisar el mensaje antes de cada commit.
- Rama `feature/produccion-vertical-slice` (nunca commitear directo a `main` en
  esta etapa). `git push` **solo** con la frase exacta `autorizo el push`.
- Verificar en Godot antes de dar algo por hecho.

## Entorno / comandos

- Godot: `C:/Users/Usuario Contable/Desktop/Codigo/Godot_v4.7.2-stable_win64.exe`
  (usar el `..._console.exe` para capturar stdout desde Bash).
- Verificación headless:
  - import: `godot --headless --path . --import`
  - cargar una escena: `godot --headless --path . --quit-after 120 res://escena.tscn`
    (chequear el exit code de Godot, no el de un `grep` en el pipe)
- Shell: PowerShell primero; el tool Bash también está disponible. UTF-8 siempre.

## Assets

- `assets/source_sheets/` — composiciones IA de Marcos **sin recortar**
  (`.gdignore` para que Godot no las importe). Organizadas: `characters/`,
  `environment/{tiles,backgrounds,props,effects}/`, `weapons/`, `ui/`,
  `memories/`, `_reference/`. Ver su `README.md`.
- `assets/sprites/` — frames ya extraídos y en uso. **No tocar** salvo que la
  fase lo pida.
- Pipeline de extracción (ejemplo: `assets/sprites/player/vaelith_custom/`):
  Python/PIL — componentes conexos por canal alfa para separar poses + re-ancla
  de cada frame a un pie/centro fijo. Las hojas IA no tienen grid: revisar cada
  pose (poses adyacentes se fusionan). Tras extraer, calibrar el `offset` del
  `AnimatedSprite2D` con la fórmula `offset_y = hb/s - (y1_pie - H/2)`
  (hb = semialto de la caja de colisión, s = escala del nodo, H = alto del
  canvas del frame).

## Estado (2026-08-27)

Fases 1–3 del rework narrativo hechas (intro/Level 1 textos, intercambio del
boss, epílogo + cierre) sobre `main`. Bugs de doble-figura y alineación de pie
corregidos (falta confirmar pie en editor). Arte de UI propio integrado. Hojas
de arte nuevas traídas a `assets/source_sheets/`. Producción arranca por la
**Fase 0** de `docs/AUDITORIA_2026-08-27.md`.
