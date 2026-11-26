# Plan de adaptación — Vaelith Arken en primera persona

Fecha: 2026-11-24. Fase 0 medida el 2026-11-25; el resto todavía no está probado.

## Qué se mantiene del original

- Historia y personajes: Vaelith, Pharasma, los no-muertos, el Guerrero-Espejo.
- Fuente narrativa: `docs/guion_demo.md` del proyecto Godot.
- Pilares: combate direccional (alto/bajo, bloqueo con escudo, embestida),
  penitencia al morir (el tramo se corrompe), la memoria como progresión.
- Diseño base: `GDD.md`, `stats_personaje.md`, `diseno_enemigos.md`,
  `diseno_boss1.md`, `guia_estilo_visual.md` (paleta fría + tres acentos cálidos).

## Qué cambia

- 2D lateral → 3D en primera persona.
- El arte 2D no se reutiliza como modelos; sí como referencia de estilo y paleta.

## Historia por zonas (acordada con Marcos el 2026-11-25)

| Zona | Qué pasa | Enemigos | Memoria |
|---|---|---|---|
| 1. Catacumbas | Despierta en la losa, encuentra espada, escudo y la daga de Pharasma; huye | Zombis, esqueletos | I · La creación (reconoce símbolos que nunca estudió) |
| 2. Osario profundo | Las catacumbas lo persiguen; almas atadas que puede liberar | Esqueletos, fantasmas | II · La obediencia (muertos marchando bajo su estandarte) |
| 3. Bosque | Sale de noche, con niebla; restos de su viejo ejército; la torre como faro | Pocos y aislados; un guardián no-muerto que no ataca | III · El propósito (su nombre escrito) |
| 4. Torre derruida | Sube por las ruinas de su fortaleza; recuerda la verdad (Pharasma, el juicio, la deuda) | La Sombra: su propio aspecto y su mismo kit | El último día |

Primera persona: el jugador nunca ve su cara. Para que la Sombra impacte se siembra
antes cómo es Vaelith: manos y escudo siempre visibles, un reflejo en agua en las
catacumbas, una sombra en la pared que se mueve medio segundo tarde.

Sistemas de juego: `docs/sistemas.md`.

## Alcance inicial

Esas cuatro zonas, no un mundo abierto. Se amplía solo si el hardware lo aguanta.

## Fases

0. **Medir:** HECHO 2026-11-25 (`docs/fase0-medicion.md`). Bosque de 300 árboles a
   185 FPS y 0,9 GB de VRAM: el bosque no limita.
1. **Sensación de control:** cámara, movimiento, salto y combate cuerpo a cuerpo
   en un cuarto de pruebas.
2. **La cripta:** mazmorra modular, antorchas con luz precalculada, un no-muerto con IA.
3. **Narrativa:** recuerdos, interacción con cadáveres, penitencia que oscurece el nivel.
4. **Exterior:** terreno chico con niebla para limitar la distancia visible.
5. **Cierre:** Guerrero-Espejo, desenlace, audio, empaquetado.

## Estética recomendada

Fantasía oscura estilizada: low-poly (Quaternius), texturas 1–2K, niebla y luz
precalculada. Megascans solo para piezas puntuales (pesado para 3 GB de VRAM).

## Assets gratuitos verificados (2026-11-24)

| Recurso | Uso | Licencia |
|---|---|---|
| Megascans (Fab) | Rocas, ruinas, suelos | Gratis desde nov-2026, Fab Standard |
| Game Animation Sample (Fab) | 500+ animaciones de locomoción, UE 5.8 | Gratis de Epic (tercera persona) |
| Quaternius (quaternius.com) | Medieval, RPG, mazmorra, armas, caballero | CC0 |
| Universal Animation Library (Quaternius) | 120+ animaciones humanoides | CC0 (versión estándar) |
| Kenney 3D | Mazmorra modular, cementerio, cuevas | CC0 |
| Poly Haven / ambientCG | Texturas PBR, HDRI | CC0 |

Sin verificar: Mixamo (página de licencia bloqueada). Packs medievales que Fab
regaló en 2025–2026: revisar si quedaron en la biblioteca de Marcos.

Regla: anotar cada asset que entre en `CREDITS.md` con origen y licencia.

## Decisiones técnicas (2026-11-25)

- **Lógica en C++** (`Source/VaelithArken/`), Blueprints para datos y ajuste. Razón:
  el código es texto que se revisa, se testea (`tools/ue/tests.sh`) y se versiona;
  armar grafos de Blueprint con herramientas cuesta más y no deja diff legible.
  Compilar el módulo tarda ~70 s en esta máquina.
- **Proyecto creado copiando la plantilla** First Person + packs compartidos
  (Characters, LevelPrototyping, Input) + variante Survival Horror (antorcha, carrera,
  mapa oscuro) en sus carpetas de montaje.
- **Python dentro del editor** con `-ExecutePythonScript` (`tools/ue/correr.sh`).
  Descartado: la ejecución remota de Unreal (multicast en la LAN) y un receptor
  propio por socket (el modo automático lo bloqueó por ser una puerta de ejecución).
- **MCP oficial** con toolsets de editor, IA, StateTree, UMG, PCG, configuración y
  tests. Analytics del plugin MCP desactivado en `DefaultEngine.ini`.
