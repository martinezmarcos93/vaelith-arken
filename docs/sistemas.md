# Sistemas de juego — Pathfinder 2e llevado a tiempo real

Fecha: 2026-11-25. Valores de arranque que se ajustan al jugar.
Fuentes: ficha PF2e Remaster nivel 1 (`80-creativo/juegos/vaelith-arken/Ideas base para el juego/`),
artifact "Registro del Osario" y `stats_personaje.md` del proyecto Godot.

**Criterio:** cada sistema sale de algo que Vaelith tiene en la ficha. No se tiran dados
visibles; el combate es por timing. Lo de PF2e se traduce a números fijos con poca
variación.

## Atributos → qué hacen en el juego

| Atributo | Valor | Efecto |
|---|---|---|
| Fuerza | +4 | Daño de espada y escudo (+4 a todo golpe) |
| Destreza | +1 | Velocidad base de las animaciones (no se mejora en la demo) |
| Constitución | +2 | PG por nivel (10 + 2) y regeneración de acciones |
| Sabiduría | +2 | Percepción: distancia a la que oye no-muertos |
| Carisma | +2 | Puntos de foco: 1 por ahora |
| Inteligencia | +0 | Sin uso (Pharasma le quitó la magia: es coherente) |

## 1. Vida (PG)
- **20 PG** en nivel 1; +12 por nivel.
- **Diehard** (dote de la ficha): al llegar a 0 PG queda *Moribundo*. Durante 3 s, si
  presiona Imponer las Manos o golpea a un enemigo, se levanta con 1 PG. Una vez por altar.
- **Muerte:** vuelve al último altar de Pharasma. El tramo se *corrompe* (+1, máx. 3):
  más niebla y un no-muerto extra. Se limpia al completar la zona.

## 2. Las tres acciones (resistencia)
En PF2e cada turno tiene 3 acciones. Acá son **3 marcas** que se recargan
(1 cada 0,9 s).

| Acción | Costo |
|---|---|
| Tajo (espada larga, 1d8+4 → 5–12) | 1 |
| Tajo potente (cargado, ×1,5 daño) | 2 |
| Golpe de escudo (contundente, 1d4+4) | 1 |
| Embestida (empuja, aturde 0,6 s) | 1 |
| Levantar escudo | 1 (mantenerlo no consume) |
| Esquivar (paso corto) | 1 |

**Penalización por ataque múltiple** (regla central de PF2e): el 2.º golpe dentro de la
misma ventana de 1,5 s hace −20 % de daño, el 3.º −40 %. Castiga el machaque sin inventar
nada.

## 3. Escudo (Bloqueo con escudo de PF2e, literal)
- Escudo de acero: **Dureza 5, 20 PG, se rompe a 10**.
- Bloquear resta 5 al daño (la dureza); el resto lo recibe el **escudo**, no Vaelith.
- Roto (≤10): la dureza baja a 2 y se ve agrietado. Destruido (0): sin escudo hasta el
  próximo altar.
- **Bloqueo perfecto** (0,2 s antes del impacto): daño 0 y **Golpe de retribución**
  gratis (la reacción del campeón de la Justicia).
- Reemplaza la "postura" del diseño de Godot: es el mismo concepto, pero con un número
  que el jugador ve.

## 4. Foco: Imponer las Manos
- **1 punto de foco** (Carisma +2). Se recarga en los altares (Reenfocar).
- Sobre Vaelith: cura **6 PG**.
- Sobre un no-muerto: **daño vital 2d6** (energía de Pharasma). Contra un fantasma es lo
  más eficaz.
- En el nivel 3 sube a 2 puntos de foco.

## 5. No-muertos y daño (debilidades de PF2e)

| Enemigo | Debilidad | Resistencia | Cómo se pelea |
|---|---|---|---|
| Zombi | Cortante 5, vital 5 | — | Lento, aguanta mucho; la espada sirve. Agarra: Embestida para soltarse |
| Esqueleto | Contundente 5, vital 5 | Cortante y perforante 5 | Golpe de escudo o empujarlo contra la pared |
| Fantasma (espíritu atado) | Vital 5 | Inmaterial: la mitad del daño físico | Daga de Pharasma (daño completo) o Imponer las Manos |

Esto le da sentido al escudo como arma y a la daga como objeto sagrado, sin agregar
inventario.

## 6. El credo (decisiones que pesan)
Algunos fantasmas están **atados** a un objeto (cadena, urna, nombre tallado). Destruir
el ancla los **libera** en lugar de matarlos: cada liberación suma **Gracia**.
Enterrar o cubrir cadáveres profanados también suma.
La Gracia cambia una línea del final y la reacción de la Sombra. "Nunca mata
innecesariamente": en el bosque hay un no-muerto que no ataca (un soldado que
sigue de guardia). Matarlo resta Gracia.

## 7. Saber del Osario y percepción
- **Saber del Osario:** al mirar por primera vez a un tipo de no-muerto aparece su
  ficha (debilidades). Así el jugador aprende la tabla del punto 5 jugando.
- **Visión en la penumbra** (Aiuvarin, sangre élfica): en las catacumbas se ve sin
  antorcha, apagado y desaturado. Ahorra luces dinámicas en la GTX 1060.
- **Sentir la muerte** (Sab +2): un susurro direccional avisa de no-muertos a 15 m.

## 8. Memoria = progresión de nivel

| Fragmento | Dónde | Sube a | Elige una dote |
|---|---|---|---|
| I · La creación | Catacumbas | Nivel 2 | *Escudo veloz* (bloquear cuesta 0) o *Golpe vital* (los tajos hacen +1d6 vital contra no-muertos) |
| II · La obediencia | Osario profundo | Nivel 3 | 2.º punto de foco, o *Aura de Pharasma* (los fantasmas se debilitan cerca suyo) |
| III · El propósito | Bosque | Nivel 4 | *Retribución mayor* (el contragolpe aturde) o *Muro de escudo* (dureza 7) |
| El último día | Torre | — | Recuerda todo: la pelea contra la Sombra |

## 9. La Sombra (jefe)
Usa el mismo kit que Vaelith: tres acciones, escudo con dureza y Golpe de retribución.
No comete errores de timing. En la fase 2 copia la última dote que eligió el jugador.
La Gracia acumulada define si al final habla con desprecio o con lástima.

## 10. Altares de Pharasma
Punto de control, recargan el foco, reparan el escudo y aplican Diehard de nuevo.
Uno por zona y uno antes de la Sombra.

## HUD (mínimo)
PG (barra) · escudo (barra chica, se agrieta) · 3 marcas de acción · punto de foco
(espiral de Pharasma). Nada más en pantalla.
