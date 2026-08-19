# Game Design Document — Vaelith Arken (título de trabajo)

## 1. Pitch
Un caballero sin memoria que fue el villano que ahora caza, atravesando un reino corrompido
por su propio antiguo imperio de no-muertos, en plataformas 2D de precisión con combate
pesado y "penitencia" en vez de vidas. Referencias directas de diseño: **SLAIN** y
**Volgarr the Viking**.

## 2. Género y plataforma
- Género: plataformas de acción 2D, dificultad alta e intencional.
- Plataforma objetivo de la demo: Windows (PC).
- Motor: Godot 4.7.

## 3. Pilares de diseño
1. **Movimiento sin margen de error.** Control aéreo mínimo o nulo. Cada salto es una
   decisión comprometida, no un ajuste en el aire.
2. **Combate direccional, no button-mashing.** Ataques altos/bajos, bloqueo con escudo,
   embestida (Shove) para crear aperturas. Pocos enemigos, pero cada uno exige lectura.
3. **Penitencia en vez de vidas infinitas.** Morir no es un game over genérico: Pharasma
   te devuelve, pero el nivel se corrompe progresivamente con cada muerte (más enemigos,
   menos luz) hasta completarlo limpio.
4. **La memoria como progresión narrativa.** Cada boss derrotado libera un fragmento de
   recuerdo del antiguo Vaelith, que resignifica zonas ya recorridas.

## 4. Alcance de la demo (vertical slice)
- Intro jugable (adaptación de "Despertar en la oscuridad").
- Level 1 completo (plataformas + 2 tipos de enemigo regular).
- Boss 1 (el "guerrero-espejo").
- Desenlace de la demo con gancho narrativo.

Fuera de alcance para esta demo: sistema de inventario, mapa de mundo, múltiples armas,
múltiples niveles, sistema de guardado entre sesiones (puede resolverse con un solo
checkpoint por nivel).

## 5. Controles (borrador, sujeto a playtesting)
| Acción | Input (teclado, borrador) |
|---|---|
| Moverse | A / D o flechas izquierda/derecha |
| Saltar | Espacio |
| Ataque alto | J |
| Ataque bajo | K (mantener abajo + J también sirve) |
| Bloquear/levantar escudo | Mantener L |
| Embestida (Shove) | L + dirección (doble tap o botón dedicado a definir) |
| Interactuar | E |
| Pausa | Esc |

## 6. Protagonista
Vaelith Arken (alias Eryndor Vale). Ficha completa de referencia en
`Ideas base para el juego/`. Combate con espada larga + escudo como set principal;
la daga ceremonial de Pharasma queda reservada como arma secundaria desbloqueable.

## 7. Referencias de arte y sonido
- Arte: ver `guia_estilo_visual.md`.
- Audio: composición vía Suno, dos capas (sagrado/coral vs. corrupto/distorsión) que se
  mezclan según el nivel de "penitencia" del nivel.

## 8. Estado del documento
Este GDD es la versión mínima viable para arrancar producción. Se actualiza a medida que
el prototipo (Etapa 1) confirme o contradiga decisiones de diseño.
