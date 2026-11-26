# La planilla de Vaelith dentro del juego (evaluación del 25/11/2026)

**Pedido de Marcos:** que **toda la planilla del personaje** quede reflejada en el sistema del juego, con una sección más RPG (stats para distribuir) y la interfaz adecuada.

**Fuentes:**
- `80-creativo/juegos/vaelith-arken/Ideas base para el juego/`:
  - `Vaelith Arken - Nivel 1 (ES).pdf`;
  - `Vaelith Arken — Registro del Osario.pdf`;
  - `Vaelith Arken — Planilla.pdf`.
- Lo ya programado: `docs/sistemas.md` y `FichaComponent`.

**Criterio:** se usa la regla real de PF2e (Remaster) siempre que se pueda jugar en tiempo real. Donde no se puede, se traduce y queda anotado. Nada se inventa con nombre de regla de PF2e: si una dote no existe en el libro, se llama distinto.

## 1. Qué de la ficha ya está en el juego
| De la ficha | En el juego (`FichaComponent`) |
|---|---|
| Atributos Fue +4, Des +1, Con +2, Int +0, Sab +2, Car +2 | Fijos; afectan daño, PG, percepción y foco |
| PG 20 (8 ascendencia + 10 clase + Con) | ✅ |
| Escudo: dureza 5, 20 PG, se rompe a 10 | ✅, literal |
| Tres acciones y penalización por ataque múltiple | ✅, en tiempo real (marcas que se recargan) |
| Diehard (trasfondo Retornado) | ✅, simplificado |
| Saber del Osario (trasfondo) | ✅, solo la ficha de debilidades del enemigo |
| Reacción de la Justicia (Golpe de retribución) | ✅, al bloquear justo |
| Imponer las Manos, 1 punto de foco (Car) | ✅ |
| Visión en la penumbra (Aiuvarin) | ✅ |
| Preceptos (destruir muertos, dar descanso) | ✅, a medias, con la **Gracia** |

## 2. Qué falta y cómo entra (en orden de valor)
### 2.1 Competencias y números reales (la columna vertebral)
- Cada valor sale de **atributo + rango + nivel**, con los rangos Entrenado, Experto, Maestro y Legendario (+2/+4/+6/+8 + nivel).
- Valores de nivel 1 según la ficha:
  - **Clase de Armadura 21**;
  - salvaciones **Fortaleza +7, Reflejos +6, Voluntad +7**;
  - **Percepción +7**;
  - **CD de clase 17**;
  - **espada larga +7 (1d8+4)** y **daga +7 (1d4+4)**.
- Hoy esos números no existen en el código. Entran como datos del `FichaComponent` y se recalculan al subir de nivel.

### 2.2 Grados de éxito (la regla central de PF2e, adaptada)
- **Ataques enemigos:** tirada **oculta** de d20 + ataque contra la CA de Vaelith, con los 4 grados de PF2e:
  - fallo crítico y fallo: el golpe roza o no entra;
  - éxito: daño normal;
  - crítico: el doble.
- Así **la CA importa**: una armadura mejor se nota. El bloqueo y el bloqueo perfecto siguen siendo habilidad del jugador y van **antes** de la tirada.
- **Ataques de Vaelith:** sin tirada. El impacto lo decide la colisión, porque una tirada de acierto en tiempo real frustra.
  - El **crítico** existe contra un enemigo **desprevenido**: después de una Embestida, de un bloqueo perfecto o por la espalda.
  - Es la regla de "+10 sobre la CA", traducida.
- **Salvaciones contra efectos:** el miedo del espectro (Voluntad → *Asustado*), el agarre del zombi (Reflejos o Atletismo para soltarse) y la peste (Fortaleza → *Debilitado*). Se resuelven con d20 oculto contra la CD del enemigo.

### 2.3 Condiciones reales
- **Moribundo y Herido**, tal como están en la ficha. Reemplazan al Diehard simplificado:
  - al caer, *Moribundo 1* (Diehard: muere en 5, no en 4);
  - cada vez que se levanta, *Herido* sube 1;
  - la próxima caída empieza en Moribundo + Herido.
  - Es la regla real y vuelve tenso cada combate sin inventar nada.
- **Asustado** (penaliza todo), **Desprevenido** (−2 CA), **Debilitado** (Fuerza) y **Aturdido**. Cada una se ve con un ícono en el HUD.

### 2.4 Habilidades fuera del combate (exploración y pueblo)
- Las habilidades de la ficha pasan a ser **pruebas contra una CD**, también con d20 oculto y grados. Pharasma narra el resultado con su voz, nunca con un número en pantalla.
- **Estas pruebas reemplazan a los "Saber del Osario" que la revisión externa pedía inventar.**

| Habilidad | Uso en el slice |
|---|---|
| **Saber del Osario** | Diagnóstico de cadáveres (fase C), cuyo grado de éxito define cuánto dice Pharasma |
| **Religión** | Leer altares, inscripciones y símbolos de Pharasma |
| **Medicina** | *Tratar heridas* fuera de combate: 10 minutos de juego, cura sin altar, una vez por zona |
| **Atletismo** | Embestida (ya existe), trepar y saltar el barranco del arroyo |
| **Intimidación** | *Desmoralizar*: 1 acción, el enemigo queda *Asustado* (los no-muertos sin mente son inmunes, como en PF2e) |
| **Diplomacia / Engaño** | **Pueblo**: hablar con el primer NPC; el grado de éxito cambia qué dice de Vaelith |
| **Percepción** (pasiva) | Encontrar pasajes, restos o una tumba distinta sin marcarlos en el HUD |
| **Supervivencia** | Leer el rastro en el bosque oscuro, como alternativa a las estatuas |

### 2.5 Anatema y expiación (el credo con dientes, regla real del campeón)
- **Anatema de la ficha:**
  - crear muertos vivientes;
  - profanar cadáveres;
  - **robar de los muertos de mala fe**.
- En PF2e, el campeón que rompe el anatema **pierde su foco y sus poderes de campeón hasta expiar**. Acá:
  - **la tentación (fase E) cuesta eso**: sin Imponer las Manos hasta hacer *expiación* en un altar;
  - **robar de los muertos:** algunos cadáveres tienen monedas o un objeto. Tomarlos es anatema; dejarlos o enterrarlos suma Gracia. Es la mecánica de loot más coherente con el personaje.
- Las señales canon de desagrado de Pharasma (sabor a tierra, escalofrío) avisan que la acción está por romper el anatema.

### 2.6 Puntos de Héroe = favor de Pharasma
- En la ficha: "gana 1 por sesión; gastá 1 para repetir una tirada, gastá todos para evitar la muerte".
- En el juego se ganan con actos del credo (liberar un alma, dar descanso) y se gastan así:
  - **1 punto:** repetir una prueba fallada (habilidad o salvación);
  - **todos:** al morir, Pharasma lo devuelve **sin penitencia**.
- Une la Gracia y la muerte narrativa ("Todavía no.") con una regla real.

### 2.7 Progresión real hasta nivel 5: los stats para distribuir
Los 4 recuerdos ya suben de nivel. Se cambia **qué da** cada nivel, según la tabla real del campeón:

| Nivel | Lo da | Qué elige el jugador |
|---|---|---|
| 1 | Inicio | Nada (ficha fija; Ambición natural ya otorgó su dote) |
| 2 | Recuerdo I | 1 dote de clase + 1 dote de habilidad |
| 3 | Recuerdo II | 1 dote general + **1 aumento de habilidad** (Entrenado → Experto) |
| 4 | Recuerdo III | 1 dote de clase + 1 dote de habilidad |
| 5 | El último día, antes de la Sombra | **4 mejoras de atributo** + 1 dote de ascendencia + 1 aumento de habilidad |

- El **nivel 5 es la "distribución de stats"** que pide Marcos, y cae justo cuando Vaelith recuerda todo.
- En PF2e, las 4 mejoras van a 4 atributos distintos y valen +1 si el atributo ya está en +4 o más. Narrativamente: recuperar quién era lo vuelve más fuerte, y la decisión de en qué es suya.
- **Revisar canon:** las dotes de `sistemas.md` §8 (*Escudo veloz*, *Golpe vital*, *Retribución mayor*, *Muro de escudo*, *Aura de Pharasma*) hay que contrastarlas con el Player Core 2. Las que no existan con ese nombre se reemplazan por las reales del campeón de nivel 2 y 4, o se renombran como propias.

### 2.8 Inventario, carga y riqueza (mínimo)
- **Carga:** máximo 5 + Fue = 9 sin penalización; con más, Vaelith queda *Sobrecargado* (−velocidad). Pocos objetos, así que casi nunca pesa, pero existe.
- **Consumibles canon:**
  - **frascos de agua bendita** (los pharasmitas los llevan siempre): se arrojan contra no-muertos y hacen daño vital;
  - pociones de curación.
- **Riqueza (pc/pp/po):** solo tiene uso si el pueblo comercia. Si no, queda fuera del slice.

### 2.9 Aura del campeón (4,5 m) y velocidad
- **Aura:** un halo tenue alrededor de Vaelith, en la luz violeta de Pharasma, que entra en el lenguaje de luz. Los espíritus atados dentro del aura se ven aunque sean invisibles.
- **Velocidad:** la de la ficha con armadura pesada. Ya define el ritmo de marcha.

## 3. La interfaz: la planilla es el Registro del Osario
La planilla no se muestra como menú de RPG genérico. Es **el registro que Pharasma lleva del alma de Vaelith**: es diegética y coherente con el título del PDF ("Alma catalogada por Pharasma").

Se abre con **Tab** y el tiempo se detiene. Tiene 4 páginas que siguen las de la ficha de PF2e:
1. **El alma:** atributos, defensas (CA, salvaciones, PG, escudo), percepción y golpes. Los números que vienen de rango + atributo + nivel se ven al pasar el cursor.
2. **Lo aprendido:** habilidades con su rango (marcas E, X, M y L como en la ficha) y dotes por nivel.
3. **Lo que carga:** inventario, carga, consumibles y riqueza.
4. **El credo y la deuda:**
   - deidad, preceptos y anatema;
   - Gracia y favor (Puntos de Héroe);
   - **memorias**, con las entradas bloqueadas "por juicio de Pharasma" que se desbloquean con los recuerdos.

**Pantalla de subida de nivel.** Al cerrar un recuerdo, Pharasma "le devuelve" algo. Se elige:
- dote: tarjetas con el ícono de acción de PF2e (◆, ◆◆, ↺);
- aumento de habilidad;
- en nivel 5, las 4 mejoras.

**Tecnología:** UMG construido en C++, la misma base que la fase F. El estilo es tinta sobre pergamino oscuro, con la espiral de plata y azul.

## 4. Riesgos y decisiones
- **Dados ocultos:** son la forma de que la CA y las salvaciones existan sin mostrar tiradas. Riesgo: si la varianza se siente injusta, el crítico enemigo pasa a determinista (ataque + 10 ≥ CA). Se mide jugando.
- **Licencia (para el futuro):** las **reglas** de PF2e Remaster están bajo la licencia ORC y se pueden usar. **Pharasma, Golarion y Aroden** son propiedad de Paizo. Para un juego no comercial se usa la *Community Use Policy*; **si algún día se vende, hay que renombrar la diosa y el mundo**. No bloquea nada hoy.
- **Tamaño:** es el bloque más grande del roadmap. Por eso se parte en cuatro fases (R1–R4) y cada una deja el juego jugable.

## 5. Segunda revisión externa (26/11): qué se suma
La revisión llega a la misma conclusión que la fase R ("la hoja es la arquitectura del juego") y pide ubicarla antes del contenido. Eso ya está: R1 y R2 van antes de C y E. Se suma lo que es nuevo y coherente:

**Principio rector (se adopta):** *toda mecánica importante tiene que decir algo sobre Vaelith.*
- Un Registro del Osario sí; un inventario genérico, no.
- La Gracia de Pharasma sí; un karma, no.
- La memoria residual de la necromancia sí; una magia genérica, no.

### 5.1 Obstáculos con varias soluciones (pruebas contextuales)
`Interactuable` pasa de una sola acción ([E]) a **opciones según la ficha**. La reja de la tentación, por ejemplo:
- **Atletismo** (Fue): levantarla a la fuerza;
- **Saber del Osario**: entender por qué la sellaron y dónde está el mecanismo;
- **Religión**: el sello de Pharasma se abre rezando;
- **una llave u objeto**, si se encontró;
- **Levantar el cadáver** (anatema).

Así "Dar descanso" deja de ser la opción mala: existe otro camino, pero **cuesta más**. Levantar es tentador porque es inmediato.

### 5.2 Inteligencia +0 y memoria residual (regla de la casa, rotulada como tal)
- En PF2e, los Saberes usan Inteligencia, así que el Saber del Osario de Vaelith es flojo (+0 de Int, +3 por entrenado).
- **Regla propia:** cada recuerdo recuperado suma +1 al Saber del Osario. Vaelith no es más listo: **recuerda cosas que no sabe explicar**.
- Lo narra Pharasma: "No sabés qué significa ese símbolo. Sabés cómo funciona."

### 5.3 Saber del Osario clasifica lo que ve (fase C)
- El diagnóstico usa la clasificación del Registro del Osario:
  - cadáver en paz → **Respeto**;
  - espíritu que necesita cruzar → **Compasión**;
  - fantasma atrapado → **Liberación**;
  - no-muerto que eligió existir → **Enemigo**;
  - nigromante → **Amenaza**.
- El juego clasifica, pero **no ordena qué hacer**.
- **Con grado de éxito alto**, el diagnóstico puede terminar en "Yo hice esto." Es la revelación por mecánica.

### 5.4 Retornado: Ecos de la muerte (regla de la casa)
Donde alguien murió hace poco, Vaelith percibe un eco: un sonido, una silueta o una frase de Pharasma. Se apoya en "Sentir la muerte" (Sab), que ya existe. Su costo es bajo y sirve para contar historias de fondo sin NPC.

### 5.5 Tres ejes en lugar de uno: Gracia, Memoria y Corrupción
| Eje | Qué mide | Ya existe |
|---|---|---|
| **Gracia** | Cuánto cumple la penitencia | Sí |
| **Memoria** | Cuánto recuperó (recuerdos y nivel) | Sí, como nivel |
| **Corrupción** | Cuánto repite al viejo Vaelith (anatema, tentación, ecos oscuros) | **Nuevo**: un contador |

El primer triage descartó la corrupción porque era una barra de poder. Ahora entra como **consecuencia** del anatema, no como recurso a llenar.

**Finales.** Hoy hay tres (gracia, neutro, deuda); pasan a resolverse por los tres ejes:
- **Guardián:** Gracia alta y Corrupción baja.
- **Penitente:** Memoria alta y Gracia media o alta. Acepta su pasado y completa la deuda.
- **Nigromante:** Corrupción alta. El pasado recupera el control.

Se reutilizan las 3 escenas de final que ya existen, con reescritura.

### 5.6 Dos caminos de dotes: Camino de Pharasma y Eco de Arken (R3)
- En los niveles 2 y 4, la dote se elige de **dos mazos**:
  - **Camino de Pharasma:** dotes reales del campeón de PF2e;
  - **Eco de Arken:** técnicas que vuelven con la memoria, como una finta, un golpe sucio o una sola forma de necromancia menor. Son reglas de la casa con nombre propio, nunca con nombre de PF2e.
- Elegir un Eco sube la **Corrupción**. Así la pregunta "¿esta habilidad es del héroe que soy o del monstruo que fui?" queda en la progresión.
- **Coherencia con el canon:** Pharasma le quitó la magia, así que los Ecos son **memoria del cuerpo y del oficio**, no conjuros. La única necromancia posible es la de la tentación.

### 5.7 Queda para la fase H (pide NPC vivos)
- La justicia como dilema con un bandido herido: matar, interrogar, liberar, entregar o ayudar.
- Las reacciones de NPC según Carisma + reputación + memoria del NPC.

El pueblo del slice es el primer lugar donde se prueba esto (decisión 4 de Marcos).
