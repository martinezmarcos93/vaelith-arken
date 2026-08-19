# Stats Jugables — Vaelith Arken

Traducción de la ficha de Pathfinder 2e (STR 18, HP 20, AC 21/23, ver
`Ideas base para el juego/`) a valores de gameplay. **Son valores de arranque,
pensados para ajustarse durante el playtesting de la Fase 1.5 — no son definitivos.**

## Movimiento
| Parámetro | Valor inicial | Nota de diseño |
|---|---|---|
| Velocidad de carrera | 90 px/s | Deliberadamente no muy rápida — Vaelith es un tanque con armadura pesada, no un ágil. |
| Aceleración | Alta (llega a velocidad máx. en ~0.1s) | El peso se siente en el salto, no en arrancar a correr. |
| Fricción al frenar | Media | Evita el "patinaje" pero tampoco frena en seco. |
| Altura de salto | ~2.5 tiles (40px de tile → ~100px) | Suficiente para plataformas de nivel, no para escapar de todo. |
| Control aéreo | **Nulo o mínimo** (±10% de ajuste de trayectoria) | Pilar de diseño: el salto es una decisión comprometida (filosofía Volgarr). |
| Coyote time | 0.08s | Margen de gracia estándar, no es parte del "peso", es anti-frustración de input. |
| Caída | Sin doble salto, sin dash aéreo en esta demo | Mantiene el alcance de la demo bajo control. |

## Combate
| Parámetro | Valor inicial | Nota |
|---|---|---|
| Vida (HP) | 5 "golpes" de enemigo básico | Traducción directa de HP 20 vs. daño de enemigo regular (~4 de daño promedio). |
| Ataque alto (espada larga) | Daño alto, velocidad lenta (~0.5s de animación) | Recompensa timing, castiga spam. |
| Ataque bajo (espada larga) | Daño medio, velocidad media | Cubre enemigos agachados/bajos. |
| Bloqueo (escudo) | Reduce 100% del daño frontal mientras se mantiene | Consume "postura": tras 2-3 bloqueos seguidos, se abre una ventana de vulnerabilidad breve. |
| Embestida (Shove) | Sin daño, desplaza al enemigo y lo aturde brevemente | Herramienta de control de espacio, no de daño — coherente con el diseño narrativo ya usado en el prólogo. |
| I-frames al recibir daño | 0.4s | Suficiente para no encadenar dos golpes injustos, no tanto como para invitar a tanquear ataques. |
| Daga ceremonial (arma secundaria) | Rápida, bajo daño, alcance corto | Reservada para desbloqueo narrativo posterior — **fuera del alcance de esta demo** salvo que el diseño de nivel la necesite antes. |

## Sistema de "penitencia" (muerte)
| Parámetro | Valor inicial | Nota |
|---|---|---|
| Al morir | Respawn en el último checkpoint | Sin pantalla de "Game Over" tradicional — narrativamente es Pharasma devolviéndolo. |
| Corrupción por muerte | +1 nivel de corrupción del tramo actual (máx. 3) | Cada nivel de corrupción suma un enemigo extra o reduce visibilidad — a definir en Fase 4.5/4.6 con datos reales de playtesting. |
| Reset de corrupción | Al completar el nivel | La corrupción no se acumula entre niveles distintos en esta demo. |

## Nota metodológica
Estos números son un punto de partida razonado, no un resultado de playtesting real
(todavía no existe). En cuanto el prototipo de Etapa 1 esté jugable, hay que
re-visitar esta tabla con datos de "cómo se siente" en vez de teoría.
