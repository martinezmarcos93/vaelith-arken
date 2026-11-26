# Assets a buscar (lista viva)

Lista de compras para cerrar la coherencia estética. La armé el 25/11 a partir de lo que **hoy es provisorio en el nivel** (revisado en `tools/ue/construir_nivel.py` y `NoMuerto.cpp`) y de lo que pidió Marcos. Se suman ítems a medida que aparecen.

**Criterios para todo lo que se baje**
- **Licencia:** CC0 ideal; CC-BY sirve anotando autor en `CREDITS.md`. Nada "solo uso personal".
- **Formato:** FBX o GLB/glTF, con texturas PBR (color, normal, rugosidad/ORM).
- **Presupuesto** (GTX 1060 3 GB):
  - props hasta ~10k triángulos;
  - personajes hasta ~30k;
  - texturas 2K como máximo.

  Si viene más pesado, el proceso de Blender lo decima.
- **Enemigos:** riggeados y animados. Ideal: **Mixamo** (sirve cualquier modelo humanoide subido ahí) o rig compatible con el maniquí de UE5.
- **Fuentes sugeridas:**
  - Poly Haven y ambientCG para texturas y HDRI (CC0);
  - Fab y Quixel/Megascans para escaneos gratis (verificar licencia);
  - Sketchfab con filtro "Downloadable" + CC;
  - Mixamo para animaciones.

## Prioridad 1: lo que hoy rompe la ilusión
| Qué | Hoy es | Qué buscar |
|---|---|---|
| **Agua quieta de la catacumba** (espejo) | plano azul plano | **Material/textura de agua oscura estancada**. Ideal: normal de ondas suaves + color casi negro. Sirve un pack de "water normal map" de ambientCG/Poly Haven; el reflejo lo resuelvo yo. |
| **Agua del arroyo** del bosque | plano azul plano | La misma textura de agua más un normal de corriente. Opcional: piedras de río y musgo de orilla. |
| **Rejas / puertas trabadas** (las que se abren con la runa o con el recuerdo) | cubo azul metálico | **Reja de hierro forjado** o **puerta de catacumba** (madera reforzada o losa de piedra que baja). 3–4 m de alto y ~4 m de ancho, o algo que se pueda escalar a eso. Si no se encuentra modelo: **textura de hierro oxidado** + textura de **runa grabada en piedra**. |
| **Runa / mecanismo** que abre la puerta | no tiene pieza propia | Placa o losa con runa grabada (modelo o textura con emisivo). |
| **Zombi** | maniquí de Unreal teñido | Zombi humanoide **riggeado** (Mixamo tiene varios), ropa harapienta, de época. |
| **Fantasma / espectro** | maniquí translúcido | Figura con túnica o mortaja que flote (no necesita piernas). Riggeado o con animación de flotar. |
| **La Sombra** (jefe final, Vaelith-espejo) | maniquí con material oscuro | **Caballero con armadura** riggeado: es el reflejo de Vaelith. Se tiñe de negro/violeta. |

## Prioridad 2: catacumba
- **Antorchas de pared con fuego:** efecto de **llama** (partícula o flipbook). El soporte ya está escaneado.
- **Sarcófagos, nichos con huesos y cráneos sueltos** (los cráneos, de a muchos, para el piso).
- **Telarañas** (planos con alfa), **raíces que bajan del techo**, **goteras**.
- **Cadenas colgantes** del techo y para el ancla: un modelo mejor que el actual.
- **Escombros, piedras caídas, polvo** en el piso.
- **Altar de Pharasma:** si aparece uno de mejor calidad, o una estatua chica para encima.
- **Velas y candelabros** para el altar (cera derretida).

## Prioridad 3: cementerio
- **Muro de cementerio** de piedra, con portón de hierro. Hoy el muro del fondo son cubos con el arco escaneado.
- **Cuervos** (animados o posados), **flores secas**, **coronas**.
- **Niebla baja** a ras del piso: partícula o textura de niebla con volumen.
- **Faroles** de cementerio (hierro, vidrio).
- **Pala clavada / tierra removida** para las tumbas abiertas, coherente con "salieron solos".

## Prioridad 4: bosque
- **Árboles vivos realistas** (coníferas y caducos muertos). Ya estaba pendiente. Los abetos actuales son procedurales y de cerca se notan.
- **Helechos, arbustos y pasto alto** con alfa, para cubrir el suelo.
- **Troncos caídos, tocones, hongos.**
- **Rocas grandes con musgo** (Megascans tiene muchas gratis).
- **Luciérnagas o polen** (partícula).

## Prioridad 5: torre final
- **Muros de torre en ruinas:** kit modular de piedra o ladrillo. Hoy son cubos con textura de ladrillo quemado.
- **Escalera de caracol** de piedra (rota).
- **Braseros con fuego:** el mismo efecto de llama que las antorchas.
- **Espejo antiguo o superficie reflectante** para el combate con la Sombra.

## Prioridad 6: lejos y ambiente general
- **Pueblo:** las casas ya están. Faltan luz de ventanas creíble (textura de ventana iluminada) y humo de chimenea (partícula).
- **Cielo nocturno:** HDRI o textura de cielo con luna y nubes (Poly Haven tiene HDRI nocturnos CC0).
- **Sonido ambiente** (si se suma a la búsqueda): viento en árboles, cuervos, agua goteando, campana lejana del pueblo, crujidos.

## Interfaz (cuando toque)
- Las placas del menú y las barras son PNG del proyecto Godot. Si se buscan reemplazos: marcos góticos, tipografía, íconos de dotes.
