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

- **Dungeon Tileset side-scroller (Raou)** — `assets/sprites/tilesets/dungeon_raou_free_commercial_ok/`
  Fuente: https://raou.itch.io/dark-dun ("Dark Dungeon - Side-Scroller Tileset")
  Coincide casi exactamente con la paleta fría de `docs/guia_estilo_visual.md`
  (piedra violeta/negra, tumbas, columnas, ventanas ojivales) — el mejor
  candidato de entorno encontrado hasta ahora.
  ✅ **Licencia confirmada** (respuesta del autor en los comentarios de la
  página): uso comercial permitido ("Yes you can :D"), atribución apreciada
  pero no obligatoria. Única restricción: no redistribuir el tileset en sí
  (ni exportarlo/compartirlo desde editores que lo permitan) — el juego
  final puede usarlo, pero no se puede repartir el .png suelto como asset.

- **Evil Wizard / Evil Wizard 2** — `assets/sprites/enemies/evil_wizard_1_CC0/`
  y `evil_wizard_2_CC0/`
  Licencia: **CC-0** confirmada (License.txt incluido en ambos packs).
  Mago encapuchado con bastón de fuego violeta — encaja tonalmente. Candidato
  a enemigo/mini-jefe tipo "acólito corrupto".

- **Necromancer sprite (creativekind)** — `assets/sprites/enemies/necromancer_creativekind_free_commercial_ok/`
  Fuente: https://creativekind.itch.io/necromancer-free ("Necromancer (Free)")
  Silueta oscura con báculo de cristal rojo y animación de disolución/muerte
  con partículas — encaje temático fuerte con el pasado nigromante de Vaelith
  (`Ideas base para el juego/`).
  ✅ **Licencia confirmada** (texto completo en `License.txt` del paquete):
  uso permitido tanto en proyectos comerciales como no comerciales,
  modificable libremente. **Prohibida la distribución o reventa del asset
  en sí.** El autor pide como favor (no como condición de la licencia)
  revisar su juego "Pixel Mage Survival" en Play Store — sin costo, no es
  un requisito de uso.
  Animaciones disponibles: Idle/Run (8f), Attack 1/2 (13f), Attack 3 (17f,
  con hechizo de calavera), Hurt (5f), Death (10f). 128x128 por frame —
  ya viene con set de ataques más completo que los otros placeholders de
  enemigos, buen candidato a subir de "referencia" a "enemigo real" del
  Level 1 o incluso a base visual de un mini-jefe.

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

- **Effect and Bullet 16x16 (BDragon1727)** — `assets/vfx/effect_bullet_16x16_bdragon1727_donationware/`
  Fuente: https://bdragon1727.itch.io/free-effect-and-bullet-16x16
  Efectos de fuego/verde/púrpura/agua en 16x16.
  ✅ **Licencia confirmada**: gratis para proyectos no comerciales; para uso
  comercial pide "contribute (any value)" (donationware, no un bloqueo
  real). Modificación permitida. **Prohibida la reventa/redistribución**
  del asset en sí.

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
  ⚠️ **Licencia NO verificada** — Marcos no recuerda el sitio de origen
  exacto. No usar en build final hasta poder identificar la fuente.

- **Cave props (CraftPix, selección de "Free-Top-Down-Pixel-Art-Cave-Objects")**
  — `assets/sprites/tilesets/cave_props_craftpix_free/`
  Pese al nombre del pack (mayormente top-down), 8 props sueltos se ven bien
  también en vista lateral y calzan con `docs/guia_estilo_visual.md`. Se
  evaluaron visualmente uno por uno (varios nombres de archivo del pack
  original están mal etiquetados — no confiar en el nombre sin abrir el
  PNG) y se integraron:
  - `white_crystal_dark_shadow1.png` / `Blue-green_crystal_dark_shadow1.png`
    — cristales, decoración de cripta.
  - `mushroom2_light_shadow1.png` — hongos, vegetación muerta/corrupta.
  - `Dark_totem_dark_shadow2.png` — ídolo/máscara con cuernos, acento rojo.
  - `Demon_scull_dark_shadow.png` — cráneo con cuernos, decoración ósea.
  - `Dinosaur_skeleton_part1_dark_shadow.png` — restos óseos ambientales.
  - `caveman_statue_dark_shadow1.png` — estatua oscura, guardián de fondo.
  - `Gates_dark_shadow3.png` — **pese al nombre, es una fogata/brasero
    ritual** (roca en círculo con fuego), no un portón. Candidato fuerte a
    "acento cálido" de `guia_estilo_visual.md` (elemento sagrado/interactuable).
  Licencia CraftPix Free confirmada: uso comercial permitido, sin
  atribución requerida, solo prohíbe revender los archivos fuente sueltos
  (`License.txt` copiado junto a los props). El resto del pack (criaturas
  top-down: escorpiones, arañas-demonio) no se integró — no aplica a vista
  lateral. Fuente completa se conserva en
  `Herramientas/Pixelherramientas/_extracted/Free-Top-Down-Cave-Objects/`
  por si hace falta revisar más props a futuro.

## Descartado (evaluado y NO integrado — eliminado de Herramientas/ el 2026-08-19)

Estos packs se revisaron, se decidió no usarlos, y **se borraron físicamente**
de `Herramientas/Pixelherramientas/` (tanto los .zip originales como las
carpetas extraídas) a pedido explícito. Se deja constancia acá por si en
algún momento conviene reevaluarlos — habría que volver a descargarlos.

- **boss_demon_slime_FREE_v1.0** — paleta cálida (rojo/naranja fuego), rompe
  la regla de acento único de `docs/guia_estilo_visual.md` y no tiene sentido
  narrativo como Boss 1 (que debe reflejar visualmente a Vaelith). Candidato
  a reconsiderar solo si el juego suma una zona temática de fuego.
- **Free-Undead-Tileset-Top-Down-Pixel-Art (CraftPix)** — perspectiva
  **top-down**, incompatible con la vista lateral del juego.
- **FreeKnight_v1** — pack de caballero completo (242 archivos) en formato
  GIF (no importable directo a Godot) y sin licencia embebida.
- **Free Desert Enemy Sprite Sheets Pixel Art** — temática de desierto
  (Serpiente, Hiena, Escorpión, Buitre, Momia), paleta cálida incompatible
  con la estética fría gótica del juego.
- **Textures-16.png / textures_02_08_25.png** — dos archivos prácticamente
  idénticos (misma hoja genérica de texturas variadas: piedra, ladrillo,
  agua, lava, pasto, patrones de color), sin curar para nuestra paleta.

### Segunda tanda — eliminados el 2026-08-21
- **Free-Undead-Tileset-Top-Down-Pixel-Art (CraftPix)** — vuelto a descargar
  sin saberlo que ya estaba descartado (ver entrada de arriba, mismo motivo:
  top-down). Confirmado visualmente de nuevo antes de re-eliminar.
- **Free-Cursed-Land-Top-Down-Pixel-Art-Tileset (CraftPix)** — top-down
  (mismo tipo de autotile de piso visto desde arriba) **y** paleta cálida
  marrón-rojiza (tierra/carne corrupta), incompatible en dos ejes distintos
  con `docs/guia_estilo_visual.md`.

## Evaluado, sin uso actual (fuera de alcance de la demo)

- **Free-Undead-Loot-Pixel-Art-Icons (CraftPix)** — 48 íconos de loot
  (calaveras, corazones, pociones, huesos, trofeos). Calidad y licencia
  igual de válidas que el resto de CraftPix (uso comercial OK, sin
  atribución), pero `docs/GDD.md` deja explícito que el sistema de
  inventario está **fuera de alcance de esta demo**. No se integró a
  `assets/` por ese motivo, no por calidad. Se conserva extraído en
  `Herramientas/Pixelherramientas/_extracted/free-undead-loot-pixel-art-icons/`
  para cuando el juego completo (post-demo) sume inventario/objetos.

## Pendientes de descarga manual (bloqueados por flujo de compra de itch.io)

El resto de los candidatos de `docs/lista_assets_pixel_art.md` y
`docs/lista_audio.md` (UI, VFX, fuente Gothic Pixels, SFX, tileset alternativo
gótico, etc.) siguen pendientes de que se bajen manualmente — itch.io y
CraftPix gatean la descarga detrás de un flujo JS con sesión de navegador que
no es scripteable de forma confiable. A medida que se agreguen a
`Herramientas/Pixelherramientas/`, se integran y documentan acá.
