# Roadmap de Desarrollo — Demo Vertical Slice
**Proyecto:** Vaelith Arken (título de trabajo)
**Alcance de esta demo:** Intro jugable → Level 1 → Boss 1 → Desenlace de demo
**Motor:** Godot · **Arte:** Aseprite (+ Blender para props 3D→sprite) · **Audio:** Suno · **Orquestación:** Claude Code

---

## Cómo leer este roadmap

- **Etapas** = macro-hitos, secuenciales en su mayoría (una habilita a la siguiente).
- **Fases** = pasos concretos dentro de cada etapa, con su entregable.
- El orden de las etapas está pensado para llegar cuanto antes a algo **jugable de punta a punta** (aunque sea feo) y recién después pulir — evita el error clásico de pulir la Etapa 2 antes de saber si el juego se siente bien.
- No incluyo estimaciones de tiempo en días/semanas: son datos que dependen de tu disponibilidad real y prefiero no inventarlos. Si querés, en la próxima sesión los estimamos juntos etapa por etapa.

---

## ETAPA 0 — Preproducción

**Objetivo:** dejar por escrito las decisiones de diseño antes de tocar el motor, para que Claude Code tenga un documento de referencia fijo en vez de decisiones que cambian sobre la marcha.

- **Fase 0.1 — Game Design Document (GDD) mínimo viable**
  Consolidar en un solo documento: pitch, pilares de gameplay, controles, stats base de Vaelith, sistema de "penitencia" al morir, alcance exacto de la demo. Se arma a partir del brainstorming ya hecho.
  *Entregable:* `GDD.md`

- **Fase 0.2 — Setup de herramientas y pipeline**
  Instalar/verificar Godot, Aseprite (o Libresprite si hay tema de licencia), estructura de carpetas del proyecto (`/scenes`, `/scripts`, `/assets/sprites`, `/assets/audio`, `/assets/tilesets`), y control de versiones (Git local, aunque sea sin remoto todavía).
  *Entregable:* proyecto Godot vacío con estructura de carpetas y primer commit.

- **Fase 0.3 — Moodboard y guía de estilo visual**
  Formalizar la paleta a partir de "Estetica ideal.jpeg": paleta fría (azul/violeta/negro) + un único acento cálido reservado para elementos sagrados/interactuables. Definir resolución de sprite base (ej. 32x32 o 48x48) y tamaño de cámara/pixel scaling.
  *Entregable:* `guia_estilo_visual.md` + paleta de colores en hex.

- **Fase 0.4 — Diseño técnico del personaje**
  Traducir la ficha de Vaelith (STR 18, HP 20, AC 21/23 con escudo) a valores de gameplay: velocidad de movimiento, altura de salto, frames de invulnerabilidad, daño de cada ataque, cooldown del escudo.
  *Entregable:* tabla de stats jugables.

---

## ETAPA 1 — Fundamentos técnicos (Core Systems)

**Objetivo:** un rectángulo que se mueve, salta, golpea y puede morir. Sin arte final todavía.

- **Fase 1.1 — Movimiento base**
  CharacterBody2D con correr, saltar, caída, coyote time, colisión con el suelo/paredes. Sin control aéreo o con control mínimo (decisión de diseño clave, estilo Volgarr).

- **Fase 1.2 — Cámara**
  Cámara side-scroll con límites de nivel, sin lag excesivo, con un poco de "lookahead" en la dirección de movimiento.

- **Fase 1.3 — Sistema de combate base**
  Hitboxes/hurtboxes, ataque simple con arma (placeholder), sistema de bloqueo con escudo, frames de invulnerabilidad al recibir daño.

- **Fase 1.4 — Sistema de vida, daño y muerte**
  Barra de vida, daño de enemigos, muerte del jugador, y el gancho narrativo/mecánico de "penitencia": qué pasa exactamente cuando morís (dónde respawneás, qué se corrompe en el nivel).

- **Fase 1.5 — Prototipo jugable interno**
  Nivel de pruebas ("caja de arena") con plataformas, un enemigo dummy y un dummy de daño, solo para validar que el movimiento y el combate se sienten bien antes de invertir en arte.
  *Criterio de aceptación:* podés correr, saltar, golpear y morir sin bugs bloqueantes.

---

## ETAPA 2 — Arte y animación del protagonista

**Objetivo:** Vaelith con sprite final en el prototipo de la Etapa 1.

- **Fase 2.1 — Sprite sheet base**
  Idle, correr, salto (subida/aire/caída), landing.

- **Fase 2.2 — Animaciones de combate**
  Ataque alto, ataque bajo, bloqueo con escudo, embestida (Shove, ya la tenés diseñada narrativamente), recibir daño.

- **Fase 2.3 — Animación de muerte/resurrección**
  Ligada al lore de Returned: no es un "game over" genérico, es una animación específica que refuerza la premisa.

- **Fase 2.4 — Integración en Godot**
  AnimationPlayer/AnimationTree, blend entre estados, ajuste de hitboxes por frame de animación.
  *Criterio de aceptación:* el prototipo de la Etapa 1 corre con el arte final del personaje y se ve consistente.

---

## ETAPA 3 — Intro / Prólogo jugable

**Objetivo:** las primeras escenas del jugador, adaptando "Despertar en la oscuridad".

- **Fase 3.1 — Guion y storyboard**
  Adaptar el prólogo ya escrito (el despertar entre ruinas, la espada, la daga, el fogonazo de recuerdos) a un guion de escenas jugables/cinemáticas concretas, con decisión de qué se cuenta con texto, qué con cinemática y qué jugando directamente.

- **Fase 3.2 — Escena de apertura**
  Implementación de la secuencia: despertar, primeros pasos, primer objeto interactuable (la puerta con el símbolo).

- **Fase 3.3 — Tutorial implícito**
  Enseñar movimiento y combate sin pantallas de texto invasivas (obstáculos que fuerzan a aprender salto, un enemigo débil que enseña ataque/bloqueo).

- **Fase 3.4 — Transición a Level 1**
  Gancho narrativo claro (el camino hacia el sendero o la cripta) que conecta sin cortes bruscos.
  *Criterio de aceptación:* de principio a fin, la intro se juega sin intervención manual tuya, con arte y controles finales.

---

## ETAPA 4 — Level 1 (diseño y construcción)

**Objetivo:** el primer nivel completo, jugable de punta a punta.

- **Fase 4.1 — Layout en papel**
  Mapa del nivel: ritmo de plataformas/combate, ubicación de checkpoints, curva de dificultad, dónde aparece el primer fragmento de memoria.

- **Fase 4.2 — Tileset y props**
  Piedra, ruinas, vegetación muerta, elementos góticos del moodboard. Evaluar qué props conviene modelar en Blender y renderizar a sprite vs. pixelear directo en Aseprite.

- **Fase 4.3 — Construcción en Godot**
  TileMap, colisiones, triggers de checkpoint, zonas de transición.

- **Fase 4.4 — Poblamiento de enemigos**
  Colocación de los enemigos regulares (definidos en Etapa 5) siguiendo el ritmo diseñado en 4.1.

- **Fase 4.5 — Atmósfera**
  Iluminación (Light2D/CanvasModulate), partículas ambientales (ceniza, niebla), parallax de fondo.

- **Fase 4.6 — Testing de ritmo y dificultad**
  Playtesting propio, ajuste de posiciones de enemigos y checkpoints.
  *Criterio de aceptación:* nivel jugable de inicio a fin, con dificultad intencional y sin softlocks.

---

## ETAPA 5 — Enemigos regulares

**Objetivo:** 2–3 tipos de enemigo para poblar Level 1, con lectura clara de patrones (filosofía SLAIN/Volgarr: pocos pero letales).

- **Fase 5.1 — Diseño de comportamiento**
  Patrones de ataque, telegrafiado, ventanas de contraataque, para cada tipo.

- **Fase 5.2 — Arte y animación**
  Sprite sheets por enemigo.

- **Fase 5.3 — IA en Godot**
  Máquinas de estado simples (idle/patrulla/ataque/aturdido).

- **Fase 5.4 — Balance**
  Ajuste de vida/daño en función del daño real de Vaelith definido en Fase 0.4.
  *Criterio de aceptación:* cada enemigo se siente distinto de resolver, no son "el mismo sprite con otro color".

---

## ETAPA 6 — Boss 1

**Objetivo:** el primer jefe, usando como base narrativa el "guerrero-espejo" ya planteado en tus notas (enemigo que reconoce la forma de pelear de Vaelith).

- **Fase 6.1 — Diseño de patrones y fases**
  Ataques, telegrafiado, número de fases (ej. cambia de comportamiento al 50% de vida), ventanas de punición.

- **Fase 6.2 — Arte y animación del boss**
  Sprite sheet completo, más grande/detallado que los enemigos regulares.

- **Fase 6.3 — Arena de combate**
  Espacio diseñado específicamente para este boss (tamaño, si hay hazards en el piso, cámara fija o con seguimiento).

- **Fase 6.4 — IA/State machine del boss**
  Implementación en Godot de las fases y transiciones.

- **Fase 6.5 — Integración narrativa**
  Diálogo previo/durante/post pelea (ya tenés el tono y las líneas de referencia en el PDF del prólogo), entrega del fragmento de memoria al ganar.

- **Fase 6.6 — Balance y testing**
  Ajuste de dificultad, verificar que la pelea sea "dura pero justa" (lectura clara de patrones, sin hits imposibles de esquivar).
  *Criterio de aceptación:* la pelea es vencible de forma consistente una vez que el jugador aprende los patrones, no por suerte.

---

## ETAPA 7 — Desenlace de la demo

**Objetivo:** cerrar la demo con un gancho, no con un corte abrupto.

- **Fase 7.1 — Guion del desenlace**
  Qué revela el fragmento de memoria del Boss 1, qué pregunta queda abierta para "el juego completo".

- **Fase 7.2 — Escena final**
  Cinemática o secuencia jugable corta post-boss.

- **Fase 7.3 — Pantalla de cierre de demo**
  Mensaje de "fin de la demo" con logo/estilo consistente, evitando que se sienta como un placeholder.
  *Criterio de aceptación:* alguien que juega la demo entiende que fue una experiencia completa e intencional, no un build cortado a la mitad.

---

## ETAPA 8 — Audio

**Objetivo:** música y sonido para intro, Level 1, Boss 1 y desenlace.

- **Fase 8.1 — Composición vía Suno**
  Tema de intro (contemplativo/misterioso), tema de exploración de Level 1, tema de combate del boss, tema/motivo del desenlace.

- **Fase 8.2 — SFX**
  Pasos, golpes de espada, impacto de escudo, sonidos ambientales, voz/grito del boss si corresponde.

- **Fase 8.3 — Integración en Godot**
  AudioStreamPlayer, mezcla de volúmenes, transiciones dinámicas (ej. la música sube de intensidad al entrar en combate con el boss).
  *Nota:* puede correr en paralelo con las Etapas 4–6 una vez cerrado el GDD, no depende de que el nivel esté terminado.

---

## ETAPA 9 — UI/UX

- **Fase 9.1 — HUD**
  Barra de vida, indicador de "penitencia"/corrupción del nivel.

- **Fase 9.2 — Menús**
  Pantalla de título, menú de pausa, opciones básicas (volumen).

- **Fase 9.3 — Sistema de diálogo**
  Cajas de texto para la intro y el boss, con el estilo ya definido en el prólogo (texto sobrio, sin exceso de iconografía).

---

## ETAPA 10 — QA y pulido

- **Fase 10.1 — Playtesting interno**
  Recorridos completos de intro→Level 1→Boss 1→desenlace, tomando nota de fricciones.

- **Fase 10.2 — Bugfixing**
  Resolución de bugs detectados, priorizados por severidad.

- **Fase 10.3 — Balance final**
  Ajustes finos de dificultad con la experiencia completa ya integrada.

- **Fase 10.4 — Optimización**
  Revisión de rendimiento (framerate estable, tiempos de carga).

---

## ETAPA 11 — Empaquetado y entrega

- **Fase 11.1 — Build de la demo**
  Export de Godot para Windows.

- **Fase 11.2 — Documentación de entrega**
  README con controles, requisitos, y alcance de la demo.

- **Fase 11.3 — Preparación para subir/compartir**
  Organización del repo para GitHub (según tu flujo habitual de proyectos personales), sin credenciales ni archivos temporales sensibles.

---

## Resumen de dependencias clave

- Etapas **0 → 1 → 2** son estrictamente secuenciales (no tiene sentido animar arte final sobre un movimiento que todavía puede cambiar).
- Etapa **3 (Intro)** y Etapa **4 (Level 1)** pueden dividirse en paralelo una vez cerrada la Etapa 2, si en algún momento sumás más manos (o más "agentes" de Claude Code trabajando en paralelo sobre distintas escenas).
- Etapa **5 (Enemigos)** debe estar lista antes de cerrar la Fase 4.4.
- Etapa **6 (Boss)** depende de que el combate base (Etapa 1.3) esté sólido — es la etapa que más se resiente si el combate base no está bien probado antes.
- Etapa **8 (Audio)** es la más flexible en el tiempo: puede arrancar en paralelo desde que el GDD está cerrado.
- Etapas **10 y 11** cierran el proyecto y dependen de que todo lo anterior esté integrado.
