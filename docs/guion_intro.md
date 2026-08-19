# Guion de Intro Jugable

Adaptación de "Despertar en la oscuridad" (`Ideas base para el juego/`) a una
secuencia de plataformas lineal — se abandona la estructura de elección múltiple
(A/B/C/D) del original porque esta demo no es un CYOA, pero se conserva el tono,
los beats narrativos y las mismas revelaciones.

## Escena 1 — El despertar (sin input del jugador, 5-8s)
Fade in sobre Vaelith tendido en piedra negra cubierta de ceniza, columnas rotas
alrededor, cielo gris. Cámara fija, ligero movimiento de "respiración" del personaje.
Sin música todavía — solo ambiente (viento, algo de eco).

## Escena 2 — Primeros pasos (tutorial implícito de movimiento)
El jugador recupera el control. Un camino estrecho a la derecha es la única
dirección navegable (el resto del área está bloqueado por escombros, sin necesidad
de UI que lo explique). Enseña: moverse, un salto simple sobre un desnivel corto.
No hay enemigos todavía.

## Escena 3 — El arma familiar
Al llegar a un punto fijo, Vaelith encuentra la espada y la daga apoyadas junto a
él (activador de área, sin botón de "interactuar" explícito la primera vez —
se recogen automáticamente al pasar, para no interrumpir el ritmo). Fogonazo visual
breve (menos de 1s): silueta de mujer, trono, calaveras, rueda — tal como en el
original. Sin texto explicativo.

## Escena 4 — La puerta con el símbolo (tutorial implícito de combate)
Vaelith llega a la construcción semienterrada con la puerta entreabierta y el
símbolo tallado. Frente a ella, un primer enemigo débil (el "No-muerto errante",
ver `diseño_enemigos.md`) bloquea el paso. Este combate enseña: ataque, bloqueo,
sin urgencia de tiempo (el enemigo es lento y muy telegrafiado).

## Escena 5 — Transición a Level 1
Tras vencer al enemigo, la puerta queda accesible pero **no se abre todavía**
(coherente con el original: "algo dentro de vos se mueve... no es un recuerdo, es
conocimiento"). En vez de entrar por la puerta, el camino continúa hacia el sendero
descendente que ya estaba insinuado en el prólogo original — ese sendero **es**
Level 1. La puerta queda como elemento de misterio/gancho para más adelante
(no se resuelve en esta demo).

## Notas de implementación
- Sin diálogo hablado en la intro — todo el peso narrativo es ambiental y visual,
  consistente con el tono "sobrio" ya definido para el personaje.
- El fogonazo de recuerdos (Escena 3) es el único momento no interactivo dentro de
  la secuencia jugable — debe ser corto para no romper el ritmo de plataformas.
- Esta escena reutiliza los mismos assets de Level 1 (mismo tileset de ruinas),
  no requiere arte exclusivo adicional.
