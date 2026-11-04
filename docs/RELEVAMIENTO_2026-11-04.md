# Relevamiento total — 2026-11-04

Hecho con Godot 4.7.2 (Linux) y el método de pixelfx: renderizar, mirar, medir.
Evidencia (capturas, hojas de contacto, tablas) en `docs/relevamiento_2026-11-04/`.

## Resumen

Técnicamente el juego no está roto: importa sin errores y las 27 escenas cargan.
Lo roto es **visual**, y tiene causas medibles. En orden de impacto:

| # | Síntoma que ve Marcos | Causa raíz (verificada) | Arreglo |
|---|---|---|---|
| 1 | Camina por el aire | `tile2.png` (piso, 15 usos) tiene **13 filas transparentes arriba**: la colisión está en el borde de la imagen, la roca visible 13 px más abajo. | Recortar el tile o bajar el visual 13 px en cada plataforma. |
| 2 | Al caminar "falta un frame" | `player.gd:410` reproduce **`run` siempre** (la animación `walk` existe y no se usa), a 90 px/s. `run` es un ciclo de carrera con los pies en el aire y **`run_4` flota 30 px** (15 en juego). | Usar `walk` al moverse; `run_4` re-anclado. |
| 3 | Ciclos que saltan / se cortan | **Frames mal extraídos de las láminas IA**: cuerpo cortado en línea recta y restos de poses vecinas. Jugador 54/77, Boss 54/65, Zombi 25/32, Espíritu 22/22 (este con el fondo gris rectangular de la lámina). | Re-extraer con grilla fija, o reemplazar. |
| 4 | El boss tiene un NPC pegado | Es `BringerOfDeath1` (x=3220), guardián agregado el 26/08 **fuera del guion**, a 15 px del `BossIntroTrigger`. El recolor del 09/09 lo dejó como **silueta violeta plana de 8 colores** con su guadaña como un bloque cuadriculado. | Sacar el nodo (lo prevé `diseno_enemigos.md`). |
| 5 | Sin coherencia visual | Conviven **dos mundos**: arte IA pintado (2.000–350.000 colores: personajes, Torre, fondos, altar, puerta, UI) y pixel art real Craftpix (4–10 colores: tiles, props). Y **escalas de 0,13 a 5,0**: el tamaño del píxel en pantalla varía ~38×. | Ver "Dirección propuesta". |

## Detalle por área

**Jugador** (`Player.tscn`): escala raíz 1,05 y sprite 0,5 (no enteras: P0-4 de la
auditoría del 09/09 sigue abierto). Lienzo 320×240 por frame, figura de ~93 px →
~49 px en pantalla. 4.000–8.000 colores por frame.

**Boss "Guerrero-Espejo"**: mismo pipeline que el jugador, mismos defectos. Al
entrar a la arena queda chico al lado de la puerta de cripta (IA, escala 0,45).
La barra de vida del boss se superpone a la del jugador (dos retratos).

**Escenas**: Intro muestra la HUD durante la cinemática; el fondo a escala 5
deja píxeles gruesos detrás de props finos. TorreSector: muy oscura, personaje
diminuto frente a props grandes. Título y epílogo: correctos.

**Texturas**: tabla completa en `relevamiento_2026-11-04/texturas_colores_escalas.txt`.
Frames por animación: `relevamiento_2026-11-04/frames_cortados.txt` (los
`skeleton_warrior`, `ghost_skull` y `necromancer` son hojas completas: sus
"restos" son los otros frames, falso positivo).

## Dirección propuesta (a decidir)

1. **Arreglos baratos y seguros primero** (1, 2, 4): no tocan arte, se ven ya.
2. **Una sola densidad de píxel**: fijar que 1 píxel de arte = 1 píxel del
   viewport 640×360, escala 1 en todo. El arte IA se re-muestrea **una vez**
   fuera de Godot (pipeline `tools/img_pipeline/`) al tamaño final y se
   cuantiza a la paleta canónica, en vez de escalarlo en el motor.
3. **pixelfx para todo lo que es efecto y ambiente** (fuego, humo, chispas,
   golpes, auras, partículas, transiciones): nace a 1:1 y en paleta, así que
   ayuda a la coherencia en vez de sumar un tercer estilo.
4. **Personajes**: el problema de fondo es que las láminas IA no tienen grilla
   ni consistencia entre poses. Re-extraer mejora el corte pero no la
   animación. Decisión pendiente: re-extraer, redibujar a mano a ~48 px, o
   cambiar a un pack de pixel art real con licencia comercial.
