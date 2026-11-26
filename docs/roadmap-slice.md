# Roadmap: el slice de Vaelith (25/11/2026, noche)

Integra tres fuentes:
1. la lista de Marcos y su roadmap de afinado (`roadmap-afinado.md`, fases 1 y 2 hechas);
2. la revisión externa del video (`revision-video-2026-11-25.md`);
3. la visión narrativa externa: memoria, deuda, tentación y NPC que reconocen a Vaelith.

Reemplaza el orden de `roadmap-afinado.md` desde su fase 3. Ese documento queda como historia de las fases 1 y 2.

**Objetivo (una línea):** un recorrido de 20–30 minutos (catacumba → cementerio → bosque → torre) donde el jugador descubre quién fue Vaelith a través de lo que hace. Visualmente legible, coherente con la biblia del personaje y de calidad alta.

## Lo que ya existe (no se rehace: se aprovecha)
La visión narrativa propone casi todo lo que `docs/sistemas.md` ya implementa. Falta **contarlo**, no construirlo:
| Propuesta | Ya existe como |
|---|---|
| Memoria como mecánica central | 4 recuerdos que suben de nivel y dan dotes (§8). La urna abre caminos |
| Deuda / penitencia jugable | **Gracia**: liberar almas y cubrir cadáveres suma, matar al soldado que no ataca resta (§6). Muertes con "penitencia_1..3" |
| "No todo muerto es enemigo" | El soldado de guardia en el bosque que no ataca |
| Saber del Osario | Ficha de debilidades al ver un tipo de no-muerto (§7) |
| Enemigo que reconoce tu estilo | **La Sombra**: usa tu mismo kit y copia tu última dote (§9) |
| Finales según lo hecho | `final_gracia`, `final_neutro`, `final_deuda` |
| Pharasma como acreedora, no amiga | Voz propuesta en `guion-auditoria.md`: "Te lo devuelvo. No es un regalo." |

## Fases, de lo más simple a lo más complejo
Cada fase cierra con:
- tests 6/6;
- una captura o un log como evidencia;
- la prueba de Marcos con teclado.

### Fase A: limpieza técnica — HECHA 26/11
- ✅ Aviso "LIGHTING NEEDS TO BE REBUILT": causa arreglada (todas las luces dinámicas, `AllowStaticLighting=False`).
- ✅ Motion blur a 0,1. ✅ Fondo negro y cursor en la pausa. ✅ "E o Enter" en la ayuda.
- ⬜ **Recalibrar la luz.** Con el cielo dinámico, el menú quedó plano y los árboles muertos casi blancos. Hay que ajustar la intensidad del cielo y la exposición, con capturas de antes y después.
- ⬜ **Aplicar la regla de legibilidad en el bosque oscuro.** El jugador tiene que ver siempre dónde está, por dónde pasa, qué puede tocar, qué es peligroso y hacia dónde ir.
- ⬜ Detalle de cámara del despertar: Marcos tiene que precisar cuál es.
- ⬜ Volver a medir el rendimiento con todas las luces dinámicas: `tools/ue/medir.sh`.

### Fase A2: cielo, horizonte y pueblo — HECHA 26/11
**Resultado:**
- **Cielo:** cúpula con estrellas y luna en la dirección de la luz de luna (`tools/texturas_cielo.py`, `tools/ue/cielo.py`, M_Cielo con nodo Custom). Fuera del alcance de la niebla.
- **Horizonte:** cerros irregulares en los 4 bordes de `tools/terreno.py`. Ya no se ve la llanura.
- **Pueblo:** a 282 m de la loma, sobre una meseta transitable, con sendero, 13 casas, iglesia, empalizada con puerta, faroles y navegación.
- **Bosque del este:** 700 árboles.
- **Hallazgo:** con las luces dinámicas, el *clustered deferred shading* de Vulkan pintaba de verde las luces puntuales. Se desactivó con `r.UseClusteredDeferredShading=0`.
- **Exposición mínima** −0,9: la noche ya no se aclara como si fuera de día.
- **Medido:** loma 148 FPS (1 % bajo: 80) y pueblo 150 FPS (1 % bajo: 90), con 900–990 MiB de VRAM.
- **Herramientas nuevas:** `tools/ue/regenerar_nivel.sh` y `tools/ue/capturas_ref.sh` (mosaico de 8 vistas).

**Plan original:**
- **Noche estrellada con luna.** Hoy el cielo es solo niebla oscura. Va una cúpula de cielo con estrellas (material propio: campo de estrellas procedural, o HDRI nocturno CC0 de Poly Haven) y una **luna visible**, alineada con la luz direccional que ya hace de luna. Así la dirección de las sombras coincide con lo que se ve.
- **Niebla de fondo que tape la llanura.** Desde la loma y el cementerio se ve el terreno plano hasta el horizonte. Van dos cosas:
  - niebla de altura recalibrada para que el horizonte se funda;
  - un anillo de **cerros y siluetas de bosque lejano** (baratos, sin colisión) que cierren el mundo.
  La niebla tiene que ocultar el borde sin volver ilegible la zona jugable: es la regla de legibilidad de la fase A.
- **Pueblo más cerca.** Hoy está a ~550 m; baja a ~250–300 m de la loma. Como el pueblo entra al slice (decisión 4), se rearma en `construir_nivel.py` como lugar transitable:
  - un camino desde la loma;
  - colisiones;
  - navmesh;
  - el lugar del primer NPC.
  Esto obliga a revisar la niebla (antes alejaba el pueblo para que no lo borrara) y el pasillo de vista.

### Fase B: guion en la voz de Pharasma — HECHA 26/11
**Resultado:**
- `tools/guion_pharasma.py` genera `guion.json`: 46 escenas y 153 líneas en la voz v2. Escenas nuevas: `zona_pueblo`, `guardian_relevado` y los finales Guardián, Penitente y Nigromante.
- **Frase del menú:** "No busca vivir. Busca merecer morir."
- **Bloqueo de control por línea:** campo `bBloquea` en `FLineaGuion` y lista `bloquean` en el guion. Verificado: al tomar las armas, el control queda bloqueado de 12,5 a 26 s y después se libera.
- **Despertar:** "El cuerpo te obedece" cae a los 13,0 s (medido).
- **Incoherencias corregidas en el nivel:**
  - 4 tumbas abiertas junto a la salida;
  - restos y un escudo partido en la celda de `sombra_vista`;
  - la rueda de Pharasma sobre el altar 4 ("Tocar la rueda");
  - el texto del centinela ya no menciona una lanza;
  - la torre habla del arco y del fuego.

**Plan original:**
- Reescribir las 41 escenas. Pharasma es **acreedora y jueza**: presta la vida, no la regala. Así ya está en la muestra de `guion-auditoria.md`.
- **Revelación escalonada:** el jugador sabe lo mismo que Vaelith. El orden es: era conocido → temido → usaba la muerte → tenía seguidores → era el enemigo → sos vos. Los 4 recuerdos y la Sombra cubren ese arco sin escenas nuevas.
- Corregir las incoherencias de la auditoría:
  - tumbas abiertas en la salida;
  - restos con cortes;
  - la lanza del centinela;
  - **la rueda sobre el altar 4**, que además convierte el texto en pista;
  - los tiempos del despertar.
- Las escenas de interacción bloquean el control; las de zona, no.
- La frase eje candidata para el menú: *"No busca vivir. Busca merecer morir."* (hoy dice "Un campeón de Pharasma. Una deuda sin plazo.").

### Fase R: la planilla viva (pedido de Marcos, 25/11). Detalle en `planilla-en-juego.md`
Toda la ficha de PF2e de Vaelith pasa a ser sistema de juego. Se parte en 4 entregas y cada una deja el juego jugable. R1 y R2 van **antes de C y E**, porque el diagnóstico de cadáveres usa las pruebas de habilidad y la tentación usa el anatema.
- **R1, modelo de datos — HECHA 26/11.**
  - Están en `Planilla.h` y en `FichaComponent`:
    - rangos (E/X/M/L);
    - CA, salvaciones, percepción, ataque, CD de clase y habilidades;
    - condiciones con vencimiento;
    - Moribundo/Herido según PF2e, con Diehard en 5;
    - Puntos de Héroe que evitan la muerte;
    - anatema.
  - El test `Vaelith.Ficha.Planilla` verifica la hoja: CA 21, Fort +7, Ref +6, Vol +7, Percepción +7, golpe +7, CD 17. `Vaelith.Planilla.Grados` cubre los grados de éxito. Tests: 8/8.
  - La "corrupción" de las muertes pasó a llamarse **Penitencia** para que "Corrupción" quede como el tercer eje.
- **R1, plan original (C++ + tests):**
  - competencias (E/X/M/L), CA 21, salvaciones, percepción, CD de clase, golpes, habilidades, condiciones, Puntos de Héroe y carga;
  - todo calculado como atributo + rango + nivel;
  - la tabla de dotes en datos editables, como `guion.json`.
- **R2, reglas en juego — HECHA 26/11.**
  - **Ataques enemigos:** tirada oculta de d20 + ataque contra la CA, con los 4 grados ("Esquivado", "Desviado" o crítico doble). Bloque de PF2e por enemigo: zombi +9/CA 14, esqueleto +9/16, espectro +10/15, Sombra +13/21. Zombis y esqueletos son sin mente.
  - **Crítico propio:** contra un enemigo desprevenido (después de aturdirlo) o golpeándolo por la espalda.
  - **Miedo del espectro:** salvación de Voluntad CD 16 que puede dejar *Asustado*.
  - **Acciones nuevas:**
    - Desmoralizar (T, Intimidación; no sirve contra no-muertos sin mente);
    - Tratar heridas (V, Medicina, una vez entre altares);
    - agua bendita (G);
    - poción (C).
  - **Interactuables con varias vías** (`FOpcionInteraccion`, se elige con la rueda). Están en:
    - la reja de la tentación (Atletismo CD 18, Religión CD 16);
    - el muerto junto a la reja (Examinar, Dar descanso, Levantar: anatema);
    - los restos del aventurero (Cubrir, Examinar, Tomar el frasco: anatema);
    - el puesto del centinela (Examinar, Relevar);
    - los huesos del bosque.
  - **Anatema:** se pierde el foco hasta expiar en un altar.
  - **Favor de Pharasma (Puntos de Héroe):** se gana con cada acto del credo. Ante un fallo crítico en una prueba se gasta 1 para repetirla; todos, para no morir.
  - **Tres ejes y finales** Guardián, Penitente y Nigromante (`FinalPorEjes`).
  - **Memoria residual:** +1 al Saber del Osario por recuerdo.
  - Verificado por log con `-usar=id#opción`. Tests: 8/8.
- **R2, plan original:**
  - grados de éxito con d20 oculto para los ataques enemigos y las salvaciones;
  - condiciones reales (Moribundo/Herido, Asustado, Desprevenido, Debilitado);
  - pruebas de habilidad en exploración, narradas por Pharasma;
  - anatema y expiación (robar de los muertos, la tentación);
  - Puntos de Héroe como favor de Pharasma;
  - agua bendita.
- **R3, progresión real hasta nivel 5:** dotes reales del campeón, con el canon revisado contra el Player Core 2, aumentos de habilidad y **las 4 mejoras de atributo en el nivel 5** (la distribución de stats).
- **Sumado por la segunda revisión (26/11, `planilla-en-juego.md` §5):**
  - obstáculos con varias soluciones según la ficha (R2);
  - memoria residual: +1 al Saber del Osario por recuerdo (R2);
  - clasificación Respeto, Compasión, Liberación, Enemigo y Amenaza (C);
  - Ecos de la muerte (C);
  - tres ejes, Gracia, Memoria y **Corrupción**, con finales Guardián, Penitente y Nigromante (R2 y B);
  - dos mazos de dotes, Camino de Pharasma y Eco de Arken (R3).
- **R4, interfaz:** la planilla como **Registro del Osario** (Tab, 4 páginas: el alma, lo aprendido, lo que carga, el credo y la deuda) y la pantalla de subida de nivel. Va **después de la base UMG de la fase F**.

### Fase C: Saber del Osario sobre cadáveres — HECHA 26/11
**Resultado:**
- **Diagnósticos con Saber del Osario** (memoria residual incluida). Cada uno nombra una de las categorías del Registro: Respeto, Compasión, Liberación o Amenaza. Están en:
  - el muerto de la reja (Respeto; con crítico, "lo sabés porque vos también sabías");
  - los restos del aventurero (Respeto);
  - el centinela (Liberación; con crítico, "la orden tiene tu voz");
  - los huesos del bosque (Compasión);
  - los restos cortados (Amenaza).
- **Ecos de la muerte (Retornado):** `ATriggerGuion` con una prueba oculta de Percepción y un solo intento. Hay 5: tumbas abiertas, arroyo, soldado perdido, puerta del pueblo y el primer aventurero en la torre. Verificado: `eco eco_arroyo: Éxito`.

**Plan original:**
- Hoy el Saber del Osario solo da la ficha del enemigo. Se extiende a **cadáveres y restos**: mirar un cuerpo da un diagnóstico vago en la voz de Pharasma ("Murió hace días." "Algo usó este cuerpo." "Su alma sigue acá.").
- Es la versión barata de "la muerte no es siempre enemiga": cada cadáver del nivel pasa a ser contenido sin geometría nueva.
- El guardián del bosque deja de ser un caso aislado: el diagnóstico es lo que avisa que no hay que matarlo.

### Fase D: agua, rejas y piedra — HECHA 26/11
**Resultado:**
- **Texturas por script** (`tools/texturas_d.py`): normal de agua y óxido (color, ARM y normal), todo tileable y sin descargas.
- **Agua:** `M_AguaMaestro` casi negro, liso y reflectante, con dos normales que se desplazan. Instancias `M_Agua_Quieta` (catacumba) y `M_Agua_Corriente` (arroyo).
- **Rejas:** `SM_Reja_Hierro`, de hierro forjado (17 barrotes con punta de lanza, travesaños con remaches, dos barrotes torcidos), y `SM_Losa_Runa` con la espiral emisiva delante de cada reja (`tools/blender/reja.py`). El cubo azul se fue.
- **Piedra:** `M_MundoVariado` agrega variación macro, musgo y humedad. Las 6 instancias de piedra pasaron a este maestro con valores por zona (el piso de la catacumba quedó húmedo).
- **Hallazgo:** el diferido en mosaico (`r.TiledDeferredShading`) también pintaba de verde las luces en Vulkan; se desactivó.
- **Medido:** pueblo 142 FPS, catacumba 138 FPS.

**Plan original:**
- Agua oscura con normal CC0, y una variante con corriente para el arroyo.
- Reja de hierro forjado y losa con runa emisiva, ambas por script de Blender.
- **Master material de piedra** con musgo, suciedad, humedad y macro variación, más decals. Así las paredes repetidas dejan de leerse iguales (puntos 19–21 de la revisión).

### Fase E: tentación — HECHA 26/11 (camino del Ministro: interactuable primero)
**Resultado:**
- **Lugar:** la daga de Pharasma quedó detrás de una reja de hierro forjado en el osario, con un muerto delante.
- **Tres vías:**
  - Forzar (Atletismo CD 18);
  - Rezar ante el sello (Religión CD 16);
  - Levantar al muerto: inmediato, pero anatema, Gracia −1 y Corrupción +1.
- **Dar descanso:** Gracia +1; la reja sigue cerrada ("lo correcto casi nunca es lo corto").
- **Levantar se ve y se siente:** el muerto se incorpora y empuja la reja mientras la pantalla se lava con un recuerdo ("Otra vez." / "Sabías hacerlo. Por eso estás acá.").
- **Expiación:** rezar en un altar devuelve el foco; la Corrupción queda.
- **Queda para después:** el muerto aliado que pelea, si Marcos lo pide al jugarla.

**Plan original:**
La propuesta externa es que el juego tiente al jugador a repetir el pecado de Vaelith. Encaja con la biblia: el **anatema** prohíbe crear muertos vivientes y profanar cadáveres, así que romperlo tiene que ser posible y costar.
- **Un solo punto de tentación** en el slice. Por ejemplo, en el osario un cadáver que se puede *levantar* durante 30 s para abrir camino o pelear, frente a *darle descanso*.
- **Costo:** resta Gracia y dispara un recuerdo ("Otra vez."). La tentación y la memoria quedan unidas: usar el poder viejo te hace recordar.
- Reutiliza `NoMuerto` con bando aliado y el sistema de Gracia. No hace falta un sistema de corrupción con barra.
- Se difiere: barra de corrupción con umbrales, tres valores (Memoria, Deuda, Reputación), "peso del alma" por muerte.

### Fase F: interfaz propia (UMG en C++) — **prioridad de Marcos: dejar atrás el pixel art**
**Regla (Marcos, 25/11):** todo elemento de interfaz se crea con el motor: barras, placas, botones, títulos y minimapa. No queda ningún PNG del proyecto Godot.
- **Barras de vida, foco y escudo:**
  - widgets UMG con material propio (llenado suave, destello al recibir daño, marco gótico generado por script);
  - reemplazan `T_*` del Godot en `VaelithHUD.cpp`.
- **Minimapa (pedido de Marcos):**
  - **Base:** una captura cenital del nivel hecha **una sola vez** desde el editor (SceneCapture ortográfica → textura). Encima, la flecha del jugador y las marcas de altares y estatuas encendidas. Capturar en vivo todos los cuadros costaría FPS en la GTX 1060.
  - **Estilo:** marco circular con la espiral de Pharasma, tinta sobre pergamino oscuro. No es un radar moderno.
  - **Coherencia con la historia:** el mapa **se revela a medida que se explora** (niebla de guerra). Así no le quita a la exploración lo que pedía la revisión ("mapa que se completa").
  - **Zonas:** en la catacumba el minimapa muestra el plano de celdas; afuera, el terreno.

- Va como estaba en `roadmap-afinado.md` fase 5: inventario, maqueta, producción y reemplazo.
- Se suma la revisión: HUD con jerarquía clara (vida → foco → escudo → dotes).
- Se suma la visión: el **Registro del Osario** como pantalla de memorias ("MEMORIA BLOQUEADA — juicio de Pharasma" → "recuperada 25 %"). Reemplaza un inventario convencional.

### Fase G: assets descargados (depende de Marcos)
- Orden de `assets-a-buscar.md`: zombi, la Sombra, fantasma, fuego, muro y torre, árboles vivos.
- **Criterio nuevo:** cada enemigo tiene que reconocerse en silueta negra.
- **Sonido ambiente** con silencios y eventos reactivos (campana, respiración detrás). La revisión lo marca como el mayor retorno por esfuerzo.

### Fase H: expansión narrativa (después del slice; **la decide Marcos**)
Son sistemas grandes que solo valen si el slice funciona:
- NPC que reconocen a Vaelith: el viejo ("un monstruo"), el seguidor ("mi señor"). Hoy no hay NPC, y el pueblo queda a la vista pero no se entra.
- La fortaleza propia, con el mural, la espada con su nombre y la puerta ARKEN.
- Recuerdos falsos, cinco finales, la espada vieja contra la de Pharasma, el aspecto de Vaelith que cambia.
- Mapa diegético, presencia, reputación.

## Decisiones de Marcos (25/11, noche)
1. **Tono de Pharasma: APROBADA la v2** ("me gusta mucho más"). Pharasma habla en primera persona a Vaelith; ver `guion-auditoria.md`. Con eso se puede reescribir el resto del guion (fase B).
2. **Tentación en el slice: SÍ, con el camino del Ministro Dragón.**
   - Primero va como **interactuable con dos opciones**, "Levantar" y "Dar descanso". Levantar abre una reja, resta Gracia y dispara un recuerdo ("Otra vez."). Usa `Interactuable`, la Gracia y los recuerdos; no lleva código de combate nuevo.
   - El muerto aliado que pelea queda para después, si la decisión pesa al jugarla.
3. **Frase eje en el menú: SÍ.** "No busca vivir. Busca merecer morir." reemplaza "Un campeón de Pharasma. Una deuda sin plazo." (`menu_pie` en `guion.json`).
4. **Se entra al pueblo en el slice: SÍ.** El primer NPC que reconoce el nombre de Vaelith pasa de la fase H al slice. Falta diseñar: cuántos NPC, cómo se llega desde la loma y qué cambia en el recorrido.

5. **Planilla completa en el sistema (25/11):** evaluada en `planilla-en-juego.md` y sumada como fase R.
6. **Nuevos pedidos (25/11):**
   - minimapa (fase F);
   - niebla de fondo, noche estrellada con luna y pueblo más cerca (fase A2);
   - interfaz creada con el motor, sin restos del pixel art (fase F).

**Instrucción vigente:** solo anotar, no implementar nada hasta que Marcos diga "empezamos".
