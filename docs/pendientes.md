# Pendientes (para ver más tarde)

## Lista de Marcos (25/11, noche) — para implementar
Estructura aprobada: zona 1 catacumbas → zona 2 cementerio → zona 3 bosque → zona 4 torre final, con el pueblo a lo lejos. Ahora toca afinar detalle.
1. **Narradora: Pharasma.** Todos los textos del guion se reescriben desde su punto de vista. Da información vaga, tanto al jugador como a Vaelith.
2. **Coherencia del guion.** Cada texto tiene que corresponder con lo que pasa de verdad en pantalla: nada que contradiga lo que se ve, lo que ya ocurrió o el orden en que se puede recorrer.
3. **HECHO (25/11).** **Sin ataques durante un texto.** Mientras un texto o una interacción bloquean el control, los monstruos no atacan. Pausar su IA y su daño durante el bloqueo, o congelarlos.
4. **HECHO (25/11).** **Adelantar o saltear con E.** Durante un texto, E completa la línea en curso; si ya está completa, pasa a la siguiente. Que no dispare además la interacción que tengas en la mira.
5. **Assets que faltan para la coherencia estética:** la lista de compras vive en `docs/assets-a-buscar.md`. Ejemplos: el agua de la catacumba y las rejas o puertas trabadas, que hoy son un plano o un cubo azul; zombi, fantasma y la Sombra, que siguen siendo maniquíes.
6. **Interfaz propia en Unreal.** Reemplazar todo lo reciclado del Godot pixel art: barra de vida, barra de energía/escudo, espirales de Foco, íconos, placas y carteles del menú ("La espada de Pharasma", "Nueva partida", "Continuar", etc.), pausa y diálogo.
   - Se conserva el estilo: marco gótico dorado, hueso y violeta de Pharasma.
   - Se migra la tecnología: hoy se dibuja a mano en `VaelithHUD.cpp` con PNG del proyecto Godot. Evaluar UMG (widgets) con texturas y materiales propios, hechos para alta resolución.
7. **Bug, despertar: HECHO (25/11).** El cuerpo copia el yaw del control, y el despertar sumaba la mirada lateral al yaw del cuerpo cada cuadro. Medido: llegaba a −122°. Ahora oscila ±12° alrededor del yaw fijo de la losa.
8. **Bug, Esc en partida: HECHO (25/11).** Sí pausaba, pero "recién apretada" seguía en verdadero un cuadro más, así que despausaba al instante. `TeclaNueva()` consume cada pulsación una sola vez (Esc, Enter y 1/2). Captura del menú de pausa verificada.
   - Detalle visual para la fase 5: la línea de diálogo se dibuja detrás del menú de pausa.
(Marcos sigue pensando; se suman ítems acá.)

## Visual
- Kit de catacumba: bóveda y pared con nichos HECHOS por Claude (Codex falló 2 rondas).
  Faltan arco de paso y reja modelada (hoy la reja es un cubo metálico).
- Los muros curvos de la torre de Codex (`SM_Torre_Muro_*`) exportan con caras invertidas;
  la torre se arma con cubos. Arreglar el script si se quieren usar.
- Esqueleto propio HECHO (25/11). Zombi: sigue el maniquí teñido; falta un zombi riggeado
  (Mixamo, lo baja Marcos). El verdugo quedó como estatua (brazos fuera de pose A).
- Licencias de los assets de Sketchfab: anotar autor y licencia en CREDITS.md antes de publicar.
- Escudo en primera persona se lee como tabla de canto: evaluar `old-medieval-shield` reteñido.
- Antorchas escaneadas en la catacumba: verificar orientación de cerca.
- Re-medir rendimiento con la máquina libre (MEDIR_ARGS en medir.sh).
- Escalera de la torre y piso superior (las piezas existen; no se colocaron).

## Juego
- Salida de la catacumba: la causa era que la urna (recuerdo 1 → reja 2) no mostraba el cartel. ARREGLADO 25/11 (mira real). Falta confirmarlo con teclado.
- Probar con teclado el exterior nuevo: tiempo del recorrido, dificultad para hallar la torre, puente.
- Espada nueva y esqueleto HECHOS (25/11). Falta: tajo con más peso/estela y zombi.
- Falta probar con teclado: centinela, elegir dote con 1/2 (el combate ya está aprobado).
- Pantalla de opciones (sensibilidad, volumen) — el menú solo tiene iniciar/continuar/salir.
- `Ascendencia Aiuvarin` como visión en penumbra: hoy es una luz suave; evaluar shader.

## Técnico
- Segfault del editor al cerrar con `quit_editor()` (después de guardar; no pierde datos).
- Las placas del menú y las barras son PNG del proyecto Godot (arte generado por Marcos con IA).
- Ramas de Codex en `~/src/vaelith-assets-sandbox` (`opencode/2026-11-25-*`): el merge es de Marcos.

### Ajustes después de la prueba de Marcos (25/11, noche)
- HECHO: el menú de pausa no mostraba el cursor. Ahora suelta la captura del ratón y lo centra sobre "Continuar". Falta que Marcos lo confirme jugando: la captura no muestra el cursor del sistema.
- HECHO: el fondo de la pausa es negro (0,9). Antes se colaba la noche azul.
- HECHO: la ayuda de controles dice "E o Enter adelantar texto".
- PENDIENTE (Marcos, "más tarde"): al despertar todavía hay un detalle de cámara, aunque ya no gira. Hay que precisar cuál.
