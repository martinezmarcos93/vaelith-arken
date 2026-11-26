# Revisión externa del video de 6:49 (25/11/2026)

Marcos pasó una revisión hecha por otra IA a partir del video `~/Vídeos/vaelith-2026-11-25-2305.mp4`. Abajo está el triage: qué se adopta, qué ya estaba en el roadmap, qué se difiere y qué no encaja con la historia.

## Corrección de hechos
- **"Elemento morado con una flecha en el lateral izquierdo" (punto 12):** no es del juego. Es una pestaña del escritorio de Marcos. Aparece en el video también sobre el escritorio, antes de que abra la ventana del juego (segundos 0–14). No hay nada que tocar.
- **"Criatura humana blanca" (punto 26):** es el maniquí de Unreal que hoy hace de espectro o zombi. Ya está en la prioridad 1 de `assets-a-buscar.md`, a la espera de que Marcos baje los modelos.

## Se adopta ya (fase 0, limpieza técnica)
| Punto | Qué | Estado |
|---|---|---|
| 1, 48 | Aviso "LIGHTING NEEDS TO BE REBUILT". **Causa:** el juego no hornea luz, pero las luces estaban en Stationary por defecto y el proyecto tenía `r.AllowStaticLighting=True`, un estado intermedio. **Decisión:** iluminación 100 % dinámica: luces Movable y `AllowStaticLighting=False`. No se ocultan los mensajes. | en curso |
| 4 | Motion blur fuerte: se baja a 0,1 (tope 2) | en curso |
| 2, 45 | Oscuridad que pierde información en el bosque oscuro (160–320 s) | después del arreglo de luces, con capturas |
| 39 | Nada de rastros de desarrollo en el menú | se verifica con la captura del menú |

### Regla de iluminación (se adopta como criterio de diseño)
El jugador tiene que poder distinguir siempre:
1. dónde está;
2. por dónde puede pasar;
3. qué puede investigar;
4. qué es peligroso;
5. hacia dónde avanzar.

La oscuridad es fondo; la zona jugable tiene información media y los puntos de interés, alta (punto 45).

### Lenguaje de luz (punto 3), ajustado al juego que ya existe
- **Violeta:** Pharasma. Son su destello en la torre, el farol de las estatuas guía y los recuerdos. Ya existe.
- **Dorado cálido:** lo que se puede tomar o tocar (interactuables). Ya existe a medias; se unifica.
- **Azul frío:** muerte y espectros (luna, brillo del espectro).
- **Rojo o brasa:** peligro y la Sombra.

No se suma el verde enfermizo: no hay necromancia en el bando del jugador (ver abajo).

## Ya estaba en el roadmap (`roadmap-afinado.md`)
- **HUD con jerarquía clara, menú propio (puntos 11 y 39):** fase 5, UMG en C++.
- **Siluetas de enemigos reconocibles (punto 27):** fase 6. Al elegir modelos se suma el criterio "reconocible en negro".
- **Set dressing con historia, vegetación variada y niebla con hitos (puntos 5, 17, 46 y 47):** `assets-a-buscar.md`. La torre con su destello y las estatuas guía ya son hitos.
- **Texto que es pista (punto 15):** coincide con la auditoría del guion. El recuerdo 4 dice "una rueda que gira" y la propuesta ya era **poner la rueda sobre el altar 4**.
- **"El mundo recuerda" (punto 16):** es el sistema de recuerdos que ya existe (urna, altares). La revisión confirma que conviene extenderlo a más objetos.

## Se difiere: ideas de diseño para decidir con Marcos
Son sistemas nuevos y grandes; ninguno se toca sin su OK.
- **Variedad de material de piedra (puntos 19–21):** master material con musgo, suciedad, humedad y macro variación, más decals. Es barato y de alto impacto. **Se propone como fase 4b**, después del agua y las rejas.
- **Sonido reactivo y silencios (puntos 28 y 29):** alto retorno. Pide sonidos ambiente que no tenemos; se suman a la búsqueda.
- **Presencia (punto 30)**, mapa diegético (37 y 38), grimorio como inventario (36), reliquias con historia en lugar de +3 (43 y 44), puzzles con fechas de tumbas (35), muerte que cambia el mundo (33).
- **Vertical slice de 20–30 minutos (punto 41):** el recorrido actual (catacumba → cementerio → bosque → torre) ya tiene esa forma. Lo que falta es pulirlo, no ampliarlo, y eso coincide con el punto 52: no meter más assets antes de la dirección de arte, los materiales y la luz.

## Necromancia: corregido después de la segunda revisión
El primer triage la descartaba entera. Con la biblia a la vista, el análisis cambia: Vaelith **fue** nigromante y el anatema prohíbe crear muertos vivientes y profanar cadáveres. Entonces la necromancia no es una herramienta del campeón, pero sí puede ser una **tentación**: posible, con costo en Gracia, y unida a recuperar recuerdos. Ver la fase E de `roadmap-slice.md`, que decide Marcos.
- **Lo que sigue sin encajar:** que la necromancia sea un arma normal del kit, sin costo, o el verde "de corrupción" como lenguaje de luz del jugador.
- **Mundo abierto (punto 40):** nunca estuvo en el plan.
