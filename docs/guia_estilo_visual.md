# Guía de Estilo Visual

## 1. Paleta base
Extraída algorítmicamente (cuantización de color, 14 colores dominantes) de
`Estetica ideal.jpeg`, ordenada por peso/frecuencia en la imagen:

| Color | Hex | Uso sugerido |
|---|---|---|
| ⬛ | `#010901` | Negro base / sombras profundas |
| 🟦 | `#2B2E56` | Azul-violeta principal (arquitectura, fondos) |
| 🟥 | `#B41F1C` | **Único acento cálido** — reservar para sangre, peligro, elementos sagrados críticos |
| 🟦 | `#11222E` | Azul oscuro secundario (sombras de piedra) |
| 🟦 | `#07424F` | Verde-azulado (musgo, hielo, atmósfera) |
| 🟪 | `#3A5184` | Azul medio (luz de luna, reflejos) |
| 🟦 | `#162C3D` | Azul oscuro terciario |
| ⬛ | `#0C1A1C` | Negro-verdoso (fondo profundo) |
| 🟪 | `#766DBC` | Violeta claro (magia, brillo sobrenatural) |
| ⬛ | `#02100E` | Negro-verdoso profundo |
| ⬛ | `#041917` | Negro-azulado profundo |
| 🟪 | `#3B4272` | Azul-violeta medio |
| 🟪 | `#352037` | Violeta oscuro (transición día/noche) |
| 🟪 | `#493165` | Violeta medio (cielo, niebla) |

**Regla madre:** de los 14 colores del núcleo, solo `#B41F1C` (rojo) rompe la
gama fría. No usar cálidos decorativamente — si todo es acento, nada lo es. Esta
regla se mantiene en espíritu abajo, aunque ahora hay tres acentos con roles
distintos en vez de uno solo.

### 1.1 Paleta extendida (variedad dentro de la misma familia)

Reconciliación con `Estetica ideal/Informe_Sistema_Estetica_DarkFantasy.md`, que
midió la paleta agregada sobre las **23 imágenes** de `Estetica ideal/` (el
núcleo de arriba sale de una sola: `Estetica ideal.jpeg`). Es el mismo eje
cromático — negro-verdoso / índigo-azul / violeta / teal —, así que estas
variantes no compiten con el núcleo, lo amplían para dar rango tonal
(iluminación, profundidad, distintas zonas del nivel) sin salir de la identidad
ya fijada.

| Grupo | Núcleo (canon, no tocar) | Variantes extendidas (usar para variar tono/luz) |
|---|---|---|
| Negros | `#010901` `#0C1A1C` `#02100E` `#041917` | `#0f1f12` `#181d14` `#161f13` `#09160b` `#000a01` |
| Azul-índigo | `#2B2E56` `#11222E` `#3A5184` `#162C3D` `#3B4272` | `#313682` `#4947a7` `#4c4793` `#205188` |
| Teal | `#07424F` | `#10423b` |
| Violeta | `#766DBC` `#352037` `#493165` | `#7a36a2` (más saturado — reservar para picos de intensidad mágica, no para uso ambiental parejo) |

**Uso sugerido:** núcleo para lo que define identidad (protagonista, boss, UI —
donde la consistencia entre assets importa más). Extendida para fondos,
iluminación puntual o props donde conviene variar sin salirse de la familia.

### 1.2 Sistema de acentos cálidos (tres roles, no uno)

El análisis de las 23 imágenes sumó un cálido adicional (`#4d1409`, rojo-óxido)
que **no compite** con el rojo de peligro porque cumple una función distinta —
es desaturado y ambiental, no saturado y urgente. Con esto, el acento único pasa
a ser un sistema de tres acentos, cada uno con un rol fijo y no intercambiable:

| Acento | Hex | Rol | Regla de uso |
|---|---|---|---|
| Rojo de peligro | `#B41F1C` | Sangre, amenaza inminente, telegrafiado de ataques | Saturado, puntual, siempre ligado a una amenaza activa en pantalla |
| Rojo-óxido (nuevo) | `#4d1409` | Desgaste ambiental — óxido en armadura, sangre seca, brasas apagadas, madera quemada | Desaturado/oscuro, puede aparecer como textura de fondo porque no se lee como "urgente" |
| Dorado apagado (a definir en producción) | `~#8A7040` (aprox., ajustar con muestra real en Aseprite) | Lo "sagrado no urgente" — símbolos de Pharasma, checkpoints | Cálido pero tibio, nunca tan vivo como el rojo de peligro |

Sigue valiendo la regla madre a nivel de conjunto: los tres cálidos juntos deben
seguir siendo minoría absoluta del cuadro (~70-80% frío, según la medición real
de `Informe_Sistema_Estetica_DarkFantasy.md` §3.2). Si en una escena hay más de
un acento cálido a la vez, cada uno debe ocupar una zona/objeto claramente
distinto — nunca mezclados en el mismo elemento.

### 1.3 Fuera del canon del juego (a propósito)

El corpus de 23 imágenes incluye una cuarta familia temática ("box-art
nostálgico cálido" — pueblo nevado, aurora boreal, fogata; ver
`Informe_Sistema_Estetica_DarkFantasy.md` §3.1) que es deliberadamente cálida y
luminosa, no fría/opresiva. Esa familia queda **fuera del canon visual de
VaelithArken** — rompería la identidad de SLAIN/Volgarr que define este juego.
Es material válido si en algún momento se retoma `Estetica ideal/` para otro fin
(ej. contenido/redes, ver `Estudio_Dark_Fantasy_Codex.md`), pero no debe
filtrarse a prompts ni a arte de este proyecto.

## 2. Resolución y escala de sprite
- Resolución de referencia de cámara: **1280x720**, con pixel scaling en modo
  "viewport" (ya configurado en `project.godot`).
- Tamaño base de sprite del protagonista: **32x48 px** (necesita más alto que ancho
  por la armadura completa y el escudo).
- Tile base del tileset: **16x16 px** (estándar, permite variación de detalle sin
  sprites gigantes).
- Filtro de textura: **nearest-neighbor** (ya seteado en `project.godot` —
  `default_texture_filter=0`), para evitar blur en los píxeles.

## 3. Filosofía de animación
- Pocos frames, mucho peso (referencia: Volgarr/SLAIN, no fluidez hiperrealista).
- Idle: 2-4 frames. Correr: 6-8 frames. Ataques: 3-5 frames con un frame de
  "anticipación" claro antes del golpe (importante para que el jugador pueda
  cancelar/leer el movimiento).
- Cada animación de daño debe durar lo mismo que los i-frames de invulnerabilidad
  (a definir en `stats_personaje.md`) para que el feedback visual sea honesto.

## 4. Composición de nivel
- Máximo 2-3 planos de profundidad con parallax (fondo lejano, fondo medio, capa
  jugable) para no saturar la lectura en una paleta tan oscura.
- Elementos interactuables (palancas, cofres, símbolos) llevan el dorado apagado
  para diferenciarse del entorno sin romper la atmósfera.

## 5. Herramientas
- LibreSprite (portátil, ya disponible en `Herramientas/`) para todo el pixel art
  2D directo.
- Blender (a instalar) reservado para props que se beneficien de un render 3D
  bajado a sprite (columnas, elementos arquitectónicos complejos), no para
  personajes ni animaciones de combate.

## 6. Vocabulario de referencia y moodboards generados

**Importante — esto es para *referencia visual*, no para sprites finales.** Un
generador de imágenes (Midjourney, Leonardo.ai, Gemini) no produce grilla de
píxeles limpia, fondo transparente ni frames de animación consistentes entre
sí. El resultado se guarda en `Estetica ideal/` como moodboard, igual que las
imágenes ya existentes ahí — el sprite jugable se sigue pixeleando a mano en
LibreSprite (ver `docs/analisis_herramientas_ia_pixel_art.md` para el porqué
se descartó automatizar esa parte).

### Vocabulario de estilo
Extraído y verificado de una guía de prompts de Dark Fantasy (Midjourney).
Útil como lenguaje descriptivo tanto para prompts de IA como para briefings
humanos:

- **Referencias de artista:** Frank Frazetta (composiciones audaces, tonos
  cálidos-dramáticos — usar con cuidado, choca con la regla de acento único
  de la paleta), Zdzisław Beksiński (surreal, pesadillesco — útil para
  horror eldritch si aparece más adelante en el lore), Caspar David Friedrich
  (figura solitaria contra paisaje vasto — encaja con el tono "wanderer" de
  Vaelith), Gustave Doré (grabados góticos detallados, blanco y negro).
- **Combos de keywords:** "cinematic lighting, volumetric fog", "matte
  painting, concept art", "chiaroscuro, dramatic shadows", "ancient,
  weathered, moss-covered".

### Cómo generar moodboards con herramientas gratuitas (sin Midjourney)
Midjourney es pago y no está disponible. Alternativas evaluadas (agosto 2026):

| Herramienta | Estado | Límite gratis | Notas |
|---|---|---|---|
| **Leonardo.ai** | ✅ Recomendado | 150 "fast tokens"/día (~25-35 imágenes con el modelo base) | Permite subir imagen de referencia (equivalente al `--profile` de Midjourney) para mantener consistencia visual entre generaciones. **Las imágenes del plan free son públicas** — no subir nada que no querés que se vea. |
| **App de Gemini** (gemini.google.com) | ⚠️ Oportunista, no confiable para un flujo | Google no publica un número fijo; reportes de usuarios varían bastante | No planificar sesiones de trabajo asumiendo una cuota — probar el día que se necesite y ver si responde. |
| **API de Gemini** (`ai.google.dev`) | ❌ Descartada | Generación de imágenes no disponible en tier gratuito (confirmado en docs oficiales) | No sirve para automatizar esto desde Claude Code sin pagar. |

**Prompts de partida para Vaelith** (adaptar subject/scene/details, sin los
parámetros de Midjourney tipo `--chaos`/`--profile`, que no aplican a
Leonardo/Gemini):
- *"A lone armored knight standing before a corrupted gothic gate, cracked
  stone runes glowing faint red, blue-violet fog rolling at his feet,
  cinematic lighting, volumetric fog, chiaroscuro, in the style of Caspar
  David Friedrich, dark fantasy illustration, cold color palette with a
  single warm red accent"*
- *"Close-up of an undead knight's helmet, ivy and moss growing through the
  cracks, faint golden light from a sacred symbol on the chestplate,
  matte painting, concept art, ancient weathered moss-covered armor,
  ominous atmosphere"*

Subir como referencia una de las imágenes ya curadas en `Estetica ideal/`
antes de generar, para mantener la paleta y atmósfera consistentes con lo
que ya se aprobó.
