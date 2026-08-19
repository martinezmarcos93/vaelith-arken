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
