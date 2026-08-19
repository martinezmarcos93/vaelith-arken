# Créditos de assets de terceros

Este archivo lista todo asset que no es 100% original del proyecto, con su
licencia y atribución. Mantener actualizado cada vez que se suma un asset
externo (ver `docs/lista_assets_pixel_art.md` y `docs/lista_audio.md`).

## Arte

- **Ghost sprite (89x88, 2 variantes)** — `assets/sprites/enemies/ghost_opengameart_CC-BY4.0/`
  Fuente: OpenGameArt.org — https://opengameart.org/content/pixel-art-ghost-sprite
  Licencia: **CC-BY 4.0** (requiere atribución explícita en los créditos finales del juego).
  Estado: usado como placeholder para el enemigo "Espíritu atado"
  (`docs/diseno_enemigos.md`) — pendiente evaluar si se reemplaza por arte
  original o se conserva con crédito.

- **Ghost + Skull sprite sheets** — `assets/sprites/enemies/ghost_skull_fatalaigaming_free/`
  Fuente: Fatal AI Gaming (itch.io) — https://fatalaigaming.itch.io/pixelghostskull
  Licencia: **Gratis, sin atribución requerida** ("Feel free to use all assets
  free of charge in any project you like. No attribution is required.").
  No redistribuir reclamando autoría propia. Donación opcional vía Ko-fi
  (no obligatoria).
  Ghost: 52x64px por frame. Skull: 44x40px por frame.
  Estado: segundo candidato/alternativa al placeholder de "Espíritu atado".

- **Dungeon Tileset** — `assets/sprites/tilesets/dungeon_golopin_free/`
  Fuente: Golopin (itch.io) — https://golopin.itch.io/dungeon-tileset
  Licencia: **"Royalty Free" / "DRM Free"** (basado en modificaciones de
  assets de Kenney.nl — Kenney publica sus packs originales bajo CC0, pero
  respetar la licencia específica que declara Golopin en su página).
  Contenido: `tilemap_less_definition.png` (hoja compacta 144x144),
  `preview_example.png` (referencia visual del autor) y 81 piezas
  individuales de 128x128 en `tilemap_objects/` (paredes, puertas, tumbas,
  murciélago, fantasma, cofres, rieles de carrito).
  Estado: candidato principal para el tileset de Level 1 — falta recolorear
  a la paleta de `docs/guia_estilo_visual.md` en LibreSprite (viene con su
  propia paleta, no la nuestra).

## Nueva tanda (revisada, integrada selectivamente)

- **Dungeon Tileset side-scroller (Raou)** — `assets/sprites/tilesets/dungeon_raou_unverified_license/`
  Coincide casi exactamente con la paleta fría de `docs/guia_estilo_visual.md`
  (piedra violeta/negra, tumbas, columnas, ventanas ojivales) — el mejor
  candidato de entorno encontrado hasta ahora.
  ⚠️ **Licencia NO verificada** — el .zip no traía License.txt/readme.
  **No usar en build final** hasta rastrear la página de origen y confirmar
  términos de uso.

- **Evil Wizard / Evil Wizard 2** — `assets/sprites/enemies/evil_wizard_1_CC0/`
  y `evil_wizard_2_CC0/`
  Licencia: **CC-0** confirmada (License.txt incluido en ambos packs).
  Mago encapuchado con bastón de fuego violeta — encaja tonalmente. Candidato
  a enemigo/mini-jefe tipo "acólito corrupto".

- **Necromancer sprite (creativekind)** — `assets/sprites/enemies/necromancer_unverified_license/`
  Silueta oscura con báculo de cristal rojo y animación de disolución/muerte
  con partículas — encaje temático fuerte con el pasado nigromante de Vaelith
  (`Ideas base para el juego/`).
  ⚠️ **Licencia NO verificada** — archivo suelto sin readme. Usar solo como
  referencia visual/de animación hasta confirmar origen y términos.

- **GothicVania Town (Ansimuz)** — `assets/sprites/tilesets/gothicvania_town_CC0/`
  Licencia: **CC0** confirmada (`public-license.pdf` incluido, sin
  restricciones de uso ni atribución).
  Se integraron `layers/` (background, middleground, tileset — ya vienen
  preparados para parallax) y `props.png`. Se descartaron los sprites de NPCs
  de pueblo (bearded/hat-man/oldman/woman) y toda la carpeta `code/` (proyecto
  Phaser.js, no aplica a Godot) por no ser necesarios para esta demo.
  Paleta cálida (marrón/ocre) — requiere recoloreo si se usa como tileset
  principal, o sirve para una zona narrativa distinta (¿pueblo previo a la
  caída?, fuera de alcance de esta demo).

- **Música: "rpg_village02" (Pascal Belisle)** — `assets/audio/music/gothicvania_village_loop_CC-BY/`
  Licencia: **libre con atribución obligatoria** ("free to use... as long as
  you give appropriate credit"). Tono de pueblo/aldea — no calza con el tono
  de combate/exploración de cripta definido en `docs/GDD.md`; se deja
  disponible como referencia/placeholder de ambiente, no como música final.

- **Effect and Bullet 16x16** — `assets/vfx/effect_bullet_16x16_unverified_license/`
  Efectos de fuego/verde/púrpura/agua en 16x16.
  ⚠️ **Licencia NO verificada** — sin readme en el .zip.

- **Kenney 1-Bit Platformer Pack** — `assets/sprites/tilesets/kenney_1bit_blockout_CC0/`
  Licencia: **CC0** confirmada (Kenney siempre publica CC0).
  Se integraron solo las 2 hojas empaquetadas (no los 811 tiles sueltos del
  pack original, para no inflar el repo). **Uso recomendado: greyboxing del
  nivel (Fase 4.1→4.3)**, no arte final — es monocromático (1-bit), no calza
  con la paleta a color del juego.

- **Seamless patterns (16x16, sheet consolidada)** — `assets/sprites/tilesets/textures_seamless_unverified_license/`
  Solo se copió `16x16_SpriteSheet.png` (la hoja final). El .zip original
  traía además una carpeta de caché interna del editor Pixaki con ~3500
  archivos de keyframes intermedios — **deliberadamente no copiada** (no es
  contenido usable, es basura de versionado de otra herramienta). Tampoco se
  integró `separate.zip` (1218 archivos sueltos): es el mismo contenido
  desagregado, la hoja consolidada alcanza.
  ⚠️ **Licencia NO verificada.**

## Descartado (no integrado al proyecto, queda solo en Herramientas/)

- **boss_demon_slime_FREE_v1.0** — paleta cálida (rojo/naranja fuego), rompe
  la regla de acento único de `docs/guia_estilo_visual.md` y no tiene sentido
  narrativo como Boss 1 (que debe reflejar visualmente a Vaelith). Sin
  licencia embebida tampoco. Se guarda como referencia por si el juego suma
  una zona temática de fuego en el futuro.
- **Free-Undead-Tileset-Top-Down-Pixel-Art (CraftPix)** — perspectiva
  **top-down**, incompatible con la vista lateral del juego. Los objetos
  sueltos (huesos, props) podrían rescatarse más adelante, no se hizo la
  curación fina ahora por tiempo. Licencia CraftPix a revisar en
  craftpix.net/file-licenses (los gratuitos suelen pedir atribución).
- **FreeKnight_v1** — pack de caballero muy completo (242 archivos), pero en
  formato GIF (no importable directo a Godot, requiere extraer frames) y sin
  licencia embebida. Guardado como referencia de timing de animación para
  cuando se produzca el arte original de Vaelith — no para usar literal.
- **Textures-16.png** — hoja genérica de texturas variadas (piedra, ladrillo,
  agua, lava, pasto, patrones de color), sin curar para nuestra paleta. No
  integrada; evaluar si hace falta más adelante.

## Descargado pero descartado (no encaja con la estética)

- **Free Desert Enemy Sprite Sheets Pixel Art** — NO integrado al proyecto,
  queda solo en `Herramientas/Pixelherramientas/` sin copiar al repo.
  Contiene: Serpiente, Hiena, Escorpión, Buitre, Momia — temática de desierto
  (paleta cálida arena/tierra), incompatible con la paleta fría gótica del
  juego (`docs/guia_estilo_visual.md`). La Momia podría eventualmente servir
  como referencia de proporciones/animación para un enemigo no-muerto propio,
  pero no como asset final.

## Pendientes de descarga manual (bloqueados por flujo de compra de itch.io)

El resto de los candidatos de `docs/lista_assets_pixel_art.md` y
`docs/lista_audio.md` (UI, VFX, fuente Gothic Pixels, SFX, tileset alternativo
gótico, etc.) siguen pendientes de que se bajen manualmente — itch.io y
CraftPix gatean la descarga detrás de un flujo JS con sesión de navegador que
no es scripteable de forma confiable. A medida que se agreguen a
`Herramientas/Pixelherramientas/`, se integran y documentan acá.
