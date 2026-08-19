# Layout de Level 1 — "El Sendero del Umbral"

Diseño en papel (sin arte ni código todavía). Continúa directamente desde el final
de la intro (el sendero descendente hacia los árboles/humo mencionado en el
prólogo original).

## Estructura general
Nivel lineal de 6 tramos, dificultad ascendente, terminando en un checkpoint
previo a la arena del Boss 1.

```
[Intro] → A → B → C → D → E → F → [Arena Boss 1]
```

## Tramo A — Descenso seguro (plataformas puras)
- Objetivo: consolidar el aprendizaje de salto de la intro con desniveles algo
  más exigentes, sin enemigos.
- Elementos: 3-4 plataformas de piedra en descenso, un salto que requiere coyote
  time bien ejecutado (sin ser injusto).

## Tramo B — Primer combate real
- Un único "No-muerto errante" en terreno plano.
- Objetivo: forzar el uso de bloqueo (no se puede esquivar simplemente saltando
  por encima, el pasillo es estrecho).

## Tramo C — Plataformas + hazard ambiental
- Sin enemigos. Introduce un hazard estático (ej. un tramo de piso roto/pinchos
  góticos) que exige precisión de salto ya sin red de seguridad de coyote time
  generoso.
- Aquí es donde el "control aéreo nulo" del diseño se pone a prueba en serio.

## Tramo D — Combate combinado
- Dos "No-muertos errantes" + un "Espíritu atado" (ver `diseno_enemigos.md`)
  atacando desde ángulos distintos.
- Objetivo: enseñar la Embestida (Shove) como herramienta para separar enemigos
  antes de que rodeen al jugador.
- Checkpoint inmediatamente después de este tramo.

## Tramo E — Zona opcional / fragmento de memoria
- Ruta secundaria corta (no obligatoria) con mayor dificultad de plataformas,
  premiando con un fragmento de memoria adicional (asset de lore, no mecánico,
  para no desbalancear la demo).
- Refuerza el pilar de "la memoria como progresión narrativa" sin bloquear el
  avance principal.

## Tramo F — Aproximación a la cripta
- Tramo corto, sin combate, con fuerte carga atmosférica (niebla, iluminación
  descendente) para preparar el tono antes del boss.
- Termina en un checkpoint fijo justo antes de la arena.

## Checkpoints
- Checkpoint 1: inicio de Tramo D (después de superar C).
- Checkpoint 2: entrada a la arena del Boss 1 (fin de Tramo F).
- Morir dentro de A-C vuelve al inicio del nivel; morir en D-F vuelve a
  Checkpoint 1. Esto es intencional para que el nivel tenga peso real las
  primeras veces, sin volverse repetitivo después del primer checkpoint.

## Pendiente para cuando exista el prototipo de Etapa 1
Los tiempos/distancias exactas de cada salto dependen de los valores reales de
`stats_personaje.md` una vez jugables — este documento define **intención de
diseño**, no coordenadas finales de nivel.
