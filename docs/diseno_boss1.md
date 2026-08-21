# Diseño de Boss 1 — El Guerrero-Espejo (Fase 6.1)

**Estado:** diseño de patrones y fases, valores de partida (no definitivos —
se ajustan con playtesting real una vez implementado, igual que
`stats_personaje.md`). Consume `GDD.md`, `guion_desenlace.md` (líneas ya
escritas: *"Todavía hacés eso"* / *"Nunca aprendiste a terminar la finta"*),
`diseno_enemigos.md` (convención de máquina de estados y ventanas de
punición) y `stats_personaje.md` (valores del kit de Vaelith que este boss
imita).

## Concepto central: imita, no inventa

El gancho narrativo ya definido es que el guerrero-espejo **reconoce la
forma de pelear de Vaelith** — no es un enemigo con moveset propio, es un
espejo del propio jugador. Esto se traduce mecánicamente de forma literal:
**sus ataques son versiones espejadas/escaladas del kit de Vaelith**
(`attack_high`, `attack_low`, `shove`, bloqueo), no un set nuevo. Esto tiene
una ventaja de diseño además de narrativa: reutiliza directamente los
tiempos y hitboxes ya validados en `player.gd` como punto de partida, en vez
de inventar timings desde cero.

El jugador, al pelear contra este boss, está literalmente peleando contra
una versión de sí mismo — la dificultad no viene de un moveset exótico, sino
de que el boss **no comete los errores de timing que sí puede cometer un
jugador humano**.

## Estructura: 2 fases por vida (umbral 50%)

### Fase 1 (100% → 50% HP) — "El espejo aprende"
El boss abre replicando el kit básico de Vaelith, con timings ligeramente
más generosos que el original (para que la primera fase sea legible y
enseñe el patrón antes de acelerarlo en fase 2).

| Ataque | Espejo de | Telegrafiado | Ventana de punición |
|---|---|---|---|
| Tajo alto | `attack_high` de Vaelith | brillo rojo (`#B41F1C`) en el filo, 0.5s antes del golpe | 0.7s tras el golpe, boss "abierto" |
| Tajo bajo | `attack_low` de Vaelith | el boss se agacha visiblemente 0.4s antes | 0.6s tras el golpe |
| Guardia especular | bloqueo de Vaelith | el boss levanta el escudo — **no ataca mientras bloquea**, imita el mismo patrón de "postura" (rompe al 4to golpe consecutivo, igual que el jugador, ver `stats_personaje.md`) | postura rota = 0.8s vulnerable, idéntico al jugador |

**Regla de fase 1:** nunca encadena dos ataques sin la ventana de punición
intermedia — mismo principio que los enemigos regulares
(`diseno_enemigos.md`), para que la curva de dificultad no dé un salto
injusto entre "enemigo regular" y "boss".

### Transición de fase (50% HP)
- La máscara del guerrero-espejo se agrieta visiblemente (telegrafía la
  transición sin ambigüedad — importante para que el jugador entienda
  "esto cambió de fase", no "esto es un bug").
- Breve ventana de invulnerabilidad del boss (~1s) mientras se reposiciona
  al centro de la arena — evita que el jugador cancele la transición a
  traición con un golpe gratis, mecánica estándar de boss fights por una
  razón (frustra menos que lo contrario).
- Silencio/quiebre de música de 1-2s (coherente con el recurso ya usado en
  `guion_desenlace.md` para el post-combate — establece el lenguaje visual
  y sonoro de "esto es un momento importante" antes de que ocurra en el
  desenlace).

### Fase 2 (50% → 0% HP) — "El espejo se rompe"
Los mismos tres ataques de fase 1, pero:
- **Timings más ajustados** (telegrafiado 30% más corto) — el espejo ya
  "aprendió" el ritmo del jugador y responde más rápido.
- **Embestida especular** (nueva, imita `shove` de Vaelith): sin daño,
  knockback fuerte, rompe la guardia si el jugador está bloqueando en ese
  momento — fuerza al jugador a *no* apoyarse solo en bloqueo indefinido en
  fase 2, empujándolo hacia el esquive con movimiento (mismo objetivo de
  diseño que el "Espíritu atado" en `diseno_enemigos.md`, escalado a boss).
- **Sin ataque nuevo "inventado"**: deliberado. Añadir un moveset propio
  rompería la premisa de "es un espejo, no un monstruo nuevo" — la
  dificultad de fase 2 viene de la velocidad y de forzar variedad de
  respuesta, no de un ataque sorpresa sin telegrafiado.

## Vida y balance (valores de partida)
- Vida: **~4x la vida de Vaelith** (20 HP equivalentes a golpes de
  `attack_high`), ajustar con playtesting — la referencia es que una pelea
  "dura pero justa" según el pilar de diseño ronde 1.5-3 minutos con
  ejecución limpia.
- Daño de cada ataque espejado: igual al daño que ese mismo ataque le hace
  al jugador cuando lo usa Vaelith (tajo alto 2, tajo bajo 1, embestida sin
  daño/con stagger) — refuerza la simetría narrativa: el boss no golpea
  "más fuerte porque es boss", golpea con la misma fuerza que Vaelith.

## Lo que este documento NO resuelve (fuera de alcance de Fase 6.1)
- **Fase 6.2** (arte): el boss comparte diseño de armadura/pose con Vaelith
  (ya anotado como bloqueo en `lista_assets_pixel_art.md` — 100% custom,
  no hay pack de terceros válido). No se puede avanzar sin el sprite de
  Vaelith primero, por la razón narrativa, no técnica.
  Sin embargo, el reciclado de patrones de fase 1 (attack_high/attack_low/
  bloqueo) se puede placeholear con el mismo pack CC0 usado para Vaelith
  (`evil_wizard_2_CC0`, ver `CHANGELOG.md`) para probar la IA en Godot sin
  esperar el arte — igual que se hizo con el jugador.
- **Fase 6.3** (arena): tamaño y hazards del espacio de combate, no
  definido acá — depende de layout real, se resuelve junto con la
  construcción de Level 1 (Etapa 4).
- **Fase 6.5** (integración narrativa completa): el diálogo post-combate ya
  está esbozado en `guion_desenlace.md`, pero queda pendiente decidir en
  qué momento exacto de fase 2 (si en algún momento) el boss también habla
  *durante* la pelea, no solo al final.
