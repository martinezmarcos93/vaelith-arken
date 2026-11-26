# Roadmap de afinado (25/11/2026)

Resuelve la lista de Marcos de `docs/pendientes.md` (ítems 1–8), ordenada de lo más sencillo a lo más complejo. Cada fase cierra con:
- tests 6/6;
- una captura o un log que pruebe el arreglo;
- la prueba con teclado de Marcos.

| Fase | Ítems | Qué | Depende de Marcos | Tamaño |
|---|---|---|---|---|
| 1 | 8, 7 | Bugs: Esc y giro del despertar | no | chico |
| 2 | 4, 3 | Control de los textos: E adelanta; nadie ataca durante un texto | no | chico |
| 3 | 1, 2 | Guion en la voz de Pharasma, coherente con el juego | aprobar el tono | medio |
| 4 | 5 (parte) | Agua y rejas reales sin esperar descargas | no | medio |
| 5 | 6 | Interfaz propia | aprobar una maqueta | grande |
| 6 | 5 (resto) | Enemigos y decorado descargados | **sí** (bajar assets) | según llegue |

## Fase 1: bugs chicos (7, 8) — HECHA 25/11
Además apareció un bug mayor: **`M_PBR` no compilaba en el juego** (Vulkan). El parámetro ORM estaba como Linear Color con una textura por defecto sRGB. Por eso los 37 modelos externos (lápidas, estatua, casas, árboles podados, espada, esqueleto…) se veían en el juego con el material por defecto gris; en el editor sí compilaba. Corregido: muestreo Masks y defecto lineal, también en `importar_externos.py`. Verificado: 0 fallos de material en el log del juego.
Herramientas de prueba nuevas:
- `-teclas=Escape@40` inyecta teclas reales por Slate;
- `-ir=x,y,z,yaw,pitch` acepta pitch;
- `CAPTURA_X/CAPTURA_Y` en `capturar.sh`: la ventana tiene que entrar en la pantalla de 1360×768, o el motor aborta al capturar.

- **Esc no abre la pausa.**
  - El código existe: `VaelithGameMode.cpp:580`.
  - Reproducir con log: si la tecla llega al controlador, en qué `Modo` está el juego, o si algo la consume.
  - Arreglar la causa y verificar que Continuar y Salir funcionen.
- **Giro de 360° al despertar.**
  - Registrar yaw y pitch de control cuadro a cuadro durante `ActualizarDespertar`. Sospecha: un ángulo que se envuelve.
  - Corregirlo para que solo se incorpore.

## Fase 2: control de los textos (4, 3) — HECHA 25/11
- **E con una escena en curso:** adelanta la línea; entre dos líneas, trae la siguiente. Enter hace lo mismo. Sin escena, la E interactúa.
  - Verificado: la E sobre la urna activa el recuerdo sin saltear su primera línea, y cada E siguiente adelanta una.
- **Tregua:** con `bControlBloqueado` los no-muertos se quedan quietos, y quien amagaba o golpeaba pasa a recuperación.
  - Verificado: 42 s junto a un esqueleto y un espectro durante el recuerdo 2 sin perder PG. Con control, los mismos enemigos lo matan en 6 s.
- **Ojo para la fase 3:** las escenas que corren con control (la introducción, por ejemplo) no bloquean. Si hay enemigos cerca, pegan mientras el texto está en pantalla. Al auditar el guion, decidir cuáles escenas bloquean.
- **Pruebas:** el log del juego registra cada línea (`[vaelith] linea T=…`) y los PG en el reloj. `-ir` espera a que termine el despertar antes de teletransportar.

Hoy una línea se adelanta con **Enter** (`VaelithGameMode.cpp:587`) y la escena bloquea a Vaelith con `bControlBloqueado`, pero los enemigos siguen activos.
- **E adelanta.**
  - La primera E completa o salta la línea actual; las siguientes pasan de línea.
  - Mientras haya un texto, la E no activa el objeto en la mira.
  - Enter queda como alternativa.
- **Tregua durante el texto.**
  - Mientras el control esté bloqueado por una escena, los no-muertos no atacan y no hacen daño. Esperan en su lugar y retoman al terminar.
  - Una sola regla en `NoMuerto`: si el jugador está bloqueado, no ataca.
  - Sirve también para el despertar y los recuerdos.

## Fase 3: Pharasma narra (1, 2)
1. **Inventario.** Una tabla de las 41 escenas con:
   - dónde se disparan (trigger, objeto o evento);
   - qué estado del juego garantizan (qué ya pasó, qué se ve en pantalla);
   - el texto actual.
2. **Auditoría de coherencia.** Marcar cada texto que contradice lo que se ve, lo que ya ocurrió o el orden posible del recorrido.
3. **Muestra de tono.** Reescribir 4 escenas: despertar, primer recuerdo, cementerio y vista del pueblo. Pharasma habla, vaga y de arriba, a Vaelith y al jugador. **Marcos aprueba el tono.**
4. **El resto.** Reescribir las 37 escenas restantes con el tono aprobado. Si algún texto queda en primera persona de Vaelith, se decide uno por uno.

## Fase 4: agua y rejas reales (sin esperar descargas)
- **Agua.**
  - Material de agua oscura y estancada: color casi negro, reflejo, ondas suaves animadas y borde que se funde con el piso.
  - Normal map CC0 de Poly Haven o ambientCG.
  - Variante con corriente para el arroyo.
- **Rejas y puerta trabada.**
  - Reja de hierro forjado modelada por script en Blender: barrotes, travesaños y puntas, con textura de hierro oxidado.
  - Losa con runa grabada emisiva para el mecanismo.
  - Reemplazan los cubos azules en `construir_nivel.py`.

## Fase 5: interfaz propia (6)
**Decisión (Marcos, 25/11):** apuntar a la calidad alta aunque sea más arriesgado. La interfaz pasa a **UMG** (escalado por resolución, anclas, animaciones, materiales), con los widgets **construidos en C++** (`UUserWidget` que arma su árbol en código). Así se mantiene editable y comprobable por script, que era la advertencia del Ministro Dragón.
1. **Inventario.** Todo lo que hoy es PNG del Godot:
   - barras de vida y escudo, espirales de Foco e íconos;
   - placas del menú, la pausa, el diálogo y los avisos;
   - los títulos ("La espada de Pharasma", "Nueva partida", etc.).
2. **Maqueta** de la pantalla de juego y del menú, en el mismo estilo (marco gótico dorado, hueso, violeta de Pharasma) y en alta resolución. **Marcos aprueba.**
3. **Producción.**
   - Texturas propias: generadas por script (vector o Blender), así se pueden reajustar y no quedan dependientes del arte viejo.
   - Barras animadas por material: llenado suave y destello al recibir daño.
4. **Reemplazo pieza por pieza** y retiro de los PNG del Godot.

## Fase 6: assets descargados (5)
Lista en `docs/assets-a-buscar.md`. A medida que Marcos baja cosas, entran por el proceso existente:
- se cargan en `tools/blender/externos.json`;
- los procesa `preparar_assets.py`;
- los importa `importar_externos.py`.

Orden de valor:
1. zombi;
2. la Sombra;
3. fantasma;
4. fuego de antorchas y braseros;
5. muro del cementerio y kit de la torre;
6. árboles vivos.
