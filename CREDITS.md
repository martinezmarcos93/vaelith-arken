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
  a enemigo/mini-jefe tipo "acólito corrupto". Evil Wizard 2 es el placeholder
  ya usado en `Player.tscn` (`_placeholder_evil_wizard2_frames.tres`); Boss 1
  (`Boss1.tscn`) reutiliza ese mismo `SpriteFrames` para su arte temporal,
  autorizado en `docs/diseno_boss1.md` para probar la IA sin esperar el
  sprite final de Vaelith.

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
  con hechizo de calavera), Hurt (5f), Death (10f). 128x128 por frame.
  **Reemplazado el 2026-08-26** en `NoMuertoErrante.tscn` por Skeleton Warrior
  (CraftPix, ver "Nueva tanda" más abajo) — silueta ósea es más legible como
  "no-muerto errante" que un mago. Ya no se usa en ninguna escena; se conserva
  extraído en `Herramientas/Pixelherramientas/` por si se reconsidera para
  otro rol (el set de ataques 1/2/3 sigue siendo más completo que el del
  esqueleto).

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
  disponible como referencia/placeholder de ambiente, **superado por la música
  propia de Suno** (abajo), no como música final.

- **Música propia (Suno) — 2026-08-27** — `assets/audio/music/` (`intro*.mp3`,
  `level1*.mp3`, `boss*.mp3`).
  Generada por Marcos con Suno a partir de los prompts de `docs/lista_audio.md`
  §1. **Contenido propio del proyecto**, no de terceros. Cada tema con 2
  versiones hasta elegir la definitiva (ver `assets/audio/README.md`).
  Nota de licencia de Suno: la propiedad/uso comercial de las generaciones
  depende del plan de la cuenta de Suno al generarlas — Marcos lo tiene
  presente.

### SFX — selección curada de 3 packs gratuitos de itch.io (2026-08-27)

Solo se trajeron al repo los archivos que usa la demo (ver `docs/lista_audio.md`
y `assets/audio/sfx/`), renombrados por función. **No se sube el pack completo.**
Los `.zip` originales quedan fuera del repo (`PHARASMA/Sound Effects/`).

- **Free Fantasy SFX Pack (TomMusic)** — `tommusic.itch.io/free-fantasy-200-sfx-pack`
  Usado: pasos en piedra (Stone Chain), salto/caída, swings y bloqueos de
  espada, parry, impactos, puertas/rejas/cerrojo, "mine", loops de cueva /
  antorcha / arroyo. Archivos en `assets/audio/sfx/{player,combat,world,ambient}/`.
  Licencia (página de itch): **royalty-free, uso comercial permitido, crédito
  apreciado pero no obligatorio; prohibido reventa/redistribución del pack.**

- **Sword Combat Sound Effects Pack — FREE VERSION (Hove Audio)** —
  `hoveaudio.itch.io/sword-combat-sound-effects-pack-free-version`
  Usado: choque de hojas metálicas, estocada con "gore", whooshes, ring FX de
  telegrafiado, y **voicelines** (gruñidos de esfuerzo y de daño) para Vaelith
  y el boss. En `assets/audio/sfx/{combat,player}/`.
  Licencia: tag **"Royalty Free"** de itch + el autor confirmó en comentarios
  que no hace falta crédito. **Sin texto de licencia formal en el pack** — para
  uso comercial serio conviene confirmar con el autor (`kade@hoveaudio.com`).

- **Horror Ambiences SFX Pack — FREE VERSION (Hove Audio)** —
  `hoveaudio.itch.io/horror-ambiences-sound-effects-pack-free-version`
  Usado: 1 archivo — "Not Alone" (versión dry) como drone de presencia
  (`assets/audio/sfx/ambient/presence_drone.wav`). La versión free trae solo 3
  ambiences, poco aprovechables para fantasía gótica. Misma nota de licencia
  que el pack de espadas de Hove (royalty-free por tag, sin texto formal).

**Redistribución en repo público**: se sigue el mismo criterio que con los
sprites de packs (CraftPix Free, etc.) ya integrados — se commitean solo los
archivos usados en el juego, documentados acá, no el pack fuente. Si hiciera
falta ser más estricto se puede `gitignore` `assets/audio/sfx/` y mantenerlo
local.

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

## Tercera tanda (2026-08-26) — escaneo de ~35 packs nuevos en Herramientas/,
## integración selectiva (Marcos pidió no ser tan estricto descartando: hace
## falta variedad para decorar/cubrir todo el nivel, el desafío actual es
## estético). Duplicados exactos de packs ya integrados y packs ya rechazados
## (top-down, etc.) se dejaron sin borrar a propósito, a pedido explícito.

- **Skeleton Warrior (CraftPix, "Free Skeleton Pixel Art Sprite Sheets")** —
  `assets/sprites/enemies/skeleton_warrior_craftpix_free/`
  ✅ **Integrado y wireado**: reemplaza a Necromancer como arte del "No-muerto
  errante" en `NoMuertoErrante.tscn` (ver entrada de Necromancer arriba).
  Animaciones: Idle (7f), Walk (7f), Attack 1/2/3 (5/6/4f), Hurt (2f), Dead
  (4f), 128x128 por frame, `_frames.tres` armado a mano (mismo patrón
  `AtlasTexture` que ya usaban Necromancer/Boss1). Offset/escala del
  `AnimatedSprite2D` recalculados con la misma técnica de `getbbox()` de PIL
  que Boss1/Necromancer (ver `docs/vaelith_arken_godot_gotchas` en memoria):
  el sprite queda perfectamente centrado en X (bbox casi exacto al centro de
  la celda) y con los pies tocando el borde inferior de la celda — offset
  final `(0, -38)`, escala `0.8`. Verificado headless (las 5 escenas de la
  demo + `NoMuertoErrante.tscn` cargan sin error), **falta la confirmación
  visual de Marcos jugando** (mismo paso final que todo sprite nuevo previo).
  Licencia CraftPix Free: comercial OK, sin atribución, no revender fuente.
  El pack trae además Skeleton_Archer y Skeleton_Spearman sin usar todavía
  (extraídos en `Herramientas/Pixelherramientas/_extracted/`).

- **Dungeon props (CraftPix, "Free Pixel Dungeon Props and Objects")** —
  `assets/sprites/tilesets/dungeon_props_craftpix_free/`
  ✅ Integrado como decoración de `Level1.tscn` (props nuevos: raíces/árbol
  muerto, mesa con velas, jarrón de cristal, estantería con libros/frascos —
  ver nodos `PropRoot1/2`, `PropTable1`, `PropJar1/2`, `PropShelf1` en
  `Level1.tscn`, distribuidos en los tramos B, C, F y la aproximación a
  BossArena que estaban visualmente vacíos). El pack original venía como
  hojas compuestas (`Objects.png`, etc.), no piezas sueltas — se cortaron
  automáticamente por detección de componentes conexos (script ad-hoc con
  PIL/numpy) en 67 piezas individuales (`obj_01.png`...`obj_67.png`),
  revisadas visualmente en conjunto (contact sheet) antes de copiar: raíces,
  frascos/cristales, mesas/estanterías, libros, pociones, plantas — paleta
  azul-teal/madera oscura que calza directo con `guia_estilo_visual.md`, sin
  necesitar recoloreo. Solo se usó una selección en esta pasada; el resto
  queda disponible para seguir decorando. Licencia CraftPix Free (comercial
  OK, sin atribución, no revender fuente suelta).

- **Rocas de cueva (CraftPix, subset "cave_rocks" de "Free Rocks Pixel Art
  Asset Pack")** — `assets/sprites/tilesets/cave_rocks_craftpix_free/`
  ✅ Integrado (`PropRockPile1/2` en `Level1.tscn`, tramo F). Gris-azulado
  oscuro, encaja directo con el núcleo de la paleta. El pack completo trae
  además variantes canyon/desert/ice/snowy (paleta cálida o fuera de tono)
  que no se integraron. Licencia CraftPix Free.

- **Bringer-of-Death (Clembod, itch.io)** —
  `assets/sprites/enemies/bringer_of_death_clembod_free/`
  Segador encapuchado, paleta violeta/gris/humo — encaja muy bien con
  `guia_estilo_visual.md` (violeta `#766DBC` de magia/brillo sobrenatural) y
  temáticamente con el motivo de muerte/no-muerte del juego. Animaciones
  completas: Idle (7f), Attack (10f), Cast (9f), Hurt (3f), Death (10f).
  ✅ **Licencia confirmada** (`License.txt` del pack): uso comercial y
  personal permitido, modificable, crédito no obligatorio (agradecido),
  prohibida la reventa/redistribución.
  ✅ **Wireado 2026-08-26** como `scenes/enemies/BringerOfDeath.tscn` (mismo
  script compartido `enemy_regular.gd`, sin animación de caminar propia en el
  pack — `anim_move` reutiliza `idle`, mismo patrón que `anim_vulnerable`).
  Colocado como aparición **única** en `Level1.tscn` (`BringerOfDeath1`,
  x=3220, en la aproximación a BossArena, antes del Boss1) con vida/daño
  ligeramente mayores que los enemigos regulares (max_health=6 vs 4) para que
  se lea como un guardián especial, no un tercer enemigo genérico repetido —
  atenúa a propósito la tensión con la filosofía "pocos enemigos, nada de
  relleno" de `docs/diseno_enemigos.md` (una única aparición, no una
  población nueva). Offset/escala calculados igual que el Skeleton
  (`getbbox()` de PIL): el canvas de 140x93 por frame NO está centrado en el
  personaje (queda corrido a la derecha, para que Attack/Cast no salten al
  cambiar de frame) — offset final `(-36, -21)`, escala `0.85`. Verificado
  headless (escena individual + `Level1.tscn` cargan sin error), **falta
  confirmación visual jugando**.

- **Dungeon Platformer Tileset (CraftPix, "Free Dungeon Platformer Pixel Art
  Tileset")** — `assets/sprites/tilesets/dungeon_platformer_craftpix_free/`
  Único tileset **side-scroller** nuevo de esta tanda (todo lo demás
  encontrado en `Herramientas/` es top-down o ya estaba integrado). Se
  copiaron las 36 piezas de `Tiles_rock/` más `chest.png`/`door.png`/
  `bridge1-3.png` de `Details/`. Se descartó `Tiles_lava/` (paleta
  naranja-cálida incompatible) y los fondos `Background/Bright,Pale`.
  ✅ **Recoloreado y aplicado 2026-08-26**: en vez de LibreSprite manual, se
  armó un script ad-hoc (PIL/numpy) que remapea cada píxel de las 41 piezas
  copiadas a la paleta más cercana de `guia_estilo_visual.md` (núcleo +
  extendida, excluyendo los 3 acentos cálidos a propósito, para no diluirlos)
  por distancia euclídea en RGB — resultado revisado visualmente antes de
  aplicar (piedra tostada → piedra azul-violeta/índigo, coherente con el
  resto del elenco). `tile2.png` (recolored) reemplaza el `ColorRect` plano
  de las 14 plataformas normales de `Level1.tscn` (todas menos
  `TramoC_HazardGround`, que mantiene el rojo de advertencia, y `SafetyFloor`)
  vía `TextureRect` + `stretch_mode=TILE`, sin tocar ninguna `CollisionShape2D`
  — cero riesgo para la física. `BossArena` usa la misma textura con
  `modulate` más oscuro para diferenciarse como piso especial. Licencia
  CraftPix Free.

- **Fondo de nivel — Fantasy 2D Battlegrounds, "Battleground1" variante Pale
  (CraftPix)** — `assets/sprites/backgrounds/battleground1_pale_craftpix_free/`
  ✅ **Integrado 2026-08-26** como `ParallaxBackground` en `Level1.tscn`
  (nodo `Background`, 3 capas: `sky.png`, `ruins_bg.png`, `ruins.png` con
  `motion_scale` 0.05/0.2/0.4 y `motion_mirroring` horizontal para repetir sin
  cortes a lo largo de los ~3700px del nivel). Es un cementerio con lápidas y
  árboles muertos en tonos teal/verde oscuro **ya alineado** con la paleta de
  `guia_estilo_visual.md` — no necesitó recoloreo, a diferencia del tileset.
  El pack completo trae 4 battlegrounds (interiores/exteriores, variantes
  Bright/Pale); solo se usó Battleground1/Pale. Licencia CraftPix Free.

- **Props chicos adicionales (mismo pack `dungeon_props_craftpix_free` de
  arriba)** — `obj_09` (tocón/raíz), `obj_30` (libro), `obj_47` (planta),
  `obj_44` (poción) — sumados en `Level1.tscn` (`PropStump1`, `PropBook1`,
  `PropPlant1`, `PropPotion1`) en el Tramo A y zona D/E que seguían con poca
  decoración.

**Limpieza 2026-08-26**: se borraron de `Herramientas/Pixelherramientas/`
(zip + carpeta extraída) los packs que eran duplicados exactos de assets ya
integrados (Evil Wizard, Evil Wizard 2, Necromancer suelto, Ghost and Skull,
GothicVania Town ×2, Kenney 1-bit, Effect and Bullet 16x16, dungeon
sidescroller Raou, Tilemap_less_definition, seamless patterns,
free-undead-loot-icons) o packs con motivo de rechazo ya confirmado sin
ambigüedad (FreeKnight_v1 sin licencia, el kit roguelike top-down, el
undead-tileset top-down ya rechazado dos veces). Se conservó todo lo demás
(bosques, Mossy Assets, Plant Animations, Legacy-Dungeon, Slimes, Undead
executioner, wizard/knight/vampire-locations de CraftPix, `tilemap.zip`,
Skeletons_Free_Pack) a pedido explícito de Marcos — variedad disponible para
seguir decorando/cubriendo el nivel aunque hoy no se haya usado.

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

### Tercera tanda — eliminados el 2026-08-21 (buscando textura de piso)
Se bajaron a pedido explícito de una búsqueda de textura de piso real para
Level 1. Ninguno resultó aplicable — medio equivocado en la mayoría de los
casos, no un tema de curación fina como las tandas anteriores.
- **Torment Textures.zip / Torment Textures 1.1.rar** — texturas de **Quake**
  (`.wad`, paleta de Quake, `.bmp`). Formato/motor 3D viejo, no pixel art,
  no aplica a un juego 2D en Godot.
- **textures.zip** — mapas **PBR** (albedo/normal/roughness/metallic +
  preview `.glb`) para render 3D realista. Choca por completo con la
  estética pixel art del juego.
- **PSD.zip** — 16 PSD (Brick, Stone, Marble, Grass, Dirt, Paving Tiles...).
  No se pudo previsualizar el PSD directamente, pero los nombres apuntan al
  mismo problema de medio equivocado (texturas pintadas/realistas, no
  pixel art).
- **256x256 Pixel Textures.rar** — la misma familia que `PSD.zip` (Brick,
  Cement, Dirt, Carpet...) exportada a PNG plano. Instalado 7-Zip para poder
  abrirlo (no había extractor de `.rar` en el sistema) y confirmado
  visualmente: son texturas pintadas realistas y seamless, no pixel art —
  sin borde de píxel duro, incompatibles con el filtro nearest-neighbor y
  la paleta fría de `docs/guia_estilo_visual.md` aunque el nombre diga
  "Pixel".
- **Pixel Plants.zip** (Bushes/Flowers/Trees) — sí es pixel art, pero de
  paleta muy saturada y vibrante (estilo granja/fantasía "cute"). No calza
  con la paleta fría gótica de `docs/guia_estilo_visual.md`.
- **free pack.zip** — sprite sheet de NPCs humanos y animales de granja
  (vaca, cerdo, gallina). Fuera de tema por completo — el juego no tiene
  NPCs ni animales en su alcance (`docs/GDD.md`).
- **seamless patterns (1).zip** — duplicado byte a byte de
  `seamless patterns.zip` (ya integrado como
  `textures_seamless_unverified_license/`, licencia sin verificar).
- **separate.zip** — mismo contenido de `seamless patterns.zip` desagregado
  en 1218 archivos sueltos, ya descartado en la entrada original.
- **Textures-16.png / textures_02_08_25.png** — vueltos a descargar sin
  saberlo que ya estaban descartados (ver "Descartado", entrada original).

## Evaluado, sin uso actual (fuera de alcance de la demo)

- **Free-Undead-Loot-Pixel-Art-Icons (CraftPix)** — 48 íconos de loot
  (calaveras, corazones, pociones, huesos, trofeos). Calidad y licencia
  igual de válidas que el resto de CraftPix (uso comercial OK, sin
  atribución). `docs/GDD.md` sigue excluyendo un sistema de **inventario**
  de esta demo, pero un coleccionable de puntaje (sin equipar/usar items)
  no es eso — ver entrada de `skull_icon.png` en "Nueva tanda" mas abajo,
  que sí se integró. El resto de los 47 íconos (corazones, pociones,
  huesos, trofeos) sigue sin uso, se conserva extraído en
  `Herramientas/Pixelherramientas/_extracted/free-undead-loot-pixel-art-icons/`.

## Coleccionables de Level1 (integrado)

- **Ícono de calavera (CraftPix, mismo pack que arriba)** —
  `assets/sprites/ui/skull_collectible_craftpix_free/skull_icon.png`
  (`Icon1.png` del pack original). Usado como coleccionable de puntaje en
  ramas opcionales de plataformeo — no es un ítem de inventario, solo
  suma a un contador visible en el HUD.

## Arte propio generado por IA (2026-08-27) — reemplaza los 4 placeholders
## de terceros de personajes principales

Marcos generó (fuera de este chat, con otra herramienta) hojas de referencia
en `Pixel Art Proyect/Sprites/` para Vaelith, el Boss (guerrero-espejo), el
No-muerto errante y el Espíritu atado, con animaciones etiquetadas que
calzan con `docs/lista_assets_pixel_art.md` y `docs/diseno_enemigos.md`.
**No es arte de terceros con licencia — es contenido propio del proyecto**,
pero se documenta acá por la misma razón que el resto de este archivo: dejar
constancia de dónde salió cada sprite y qué tan "terminado" está.

**Advertencia técnica importante**: estas hojas son composiciones de IA
(lienzo 1536×1024, sin grid real), no spritesheets recortados. Cada
animación se extrajo con un script propio (Python/PIL): detección de
componentes conexos por canal alpha para separar cada pose, más un paso que
**re-ancla cada frame a un mismo pie/centro fijo** (en vez de confiar en la
alineación del lienzo original) — esto es lo que evita el "tembleque" de
1-2px o peor que se veía al medir las hojas a ojo. Verificado headless en las
12 escenas relevantes (jugador, los 4 enemigos, los 5 pasos de la demo,
Checkpoint y MemoryFragment) sin errores de carga.

**Recorte de alcance de esta pasada** (no se extrajo cada animación de cada
hoja, ver detalle por personaje): se priorizaron las animaciones que los
scripts (`player.gd`, `boss1.gd`, `enemy_regular.gd`) realmente reproducen.
Donde la hoja no traía una animación necesaria, se reutilizó otra ya
extraída (ej. "salto" y "caída" de Vaelith reusan los mismos frames) — es
una mejora real sobre el placeholder anterior, no el resultado final.

- **Vaelith** — `assets/sprites/player/vaelith_custom/`. Extraído de
  `Sprites/Vaelith.png`: `idle`(4), `run`/caminar(8), `attack1`/ataque
  alto(5, recortado de 8 por arcos de espada rojos que se fusionaban con el
  personaje en la detección automática), `dead`/muerte(6, se descartaron 2
  frames finales que en realidad eran del inicio de "Resurrección"
  contaminando el recorte). `jump`, `fall`, `attack2` y `hurt` reutilizan
  `run`/`idle`/`attack1` respectivamente (sin extraer todavía). Reemplaza
  `_placeholder_evil_wizard2_frames.tres` en `Player.tscn`. Offset/escala:
  `(0,-31)` / `0.5`, calculado (no medido a ojo) para que el pie caiga
  exacto en el borde de la `CollisionShape2D` (28×44).

- **Boss 1 / guerrero-espejo** — `assets/sprites/enemies/espejo_boss_custom/`.
  De `Sprites/Espejo.png`: `idle`(4), `run`(7), `hurt`(4). `attack1` y
  `attack2` son el MISMO set de 6 frames (la hoja no separaba claramente
  "ataque alto" de "ataque bajo" como sí hacía la de Vaelith — se prefirió
  un ataque único limpio antes que dos ataques con frames rotos). Reemplaza
  el mismo placeholder de Evil Wizard 2 que antes compartía con el jugador.
  Offset/escala: `(0,-31)` / `0.5` (misma fórmula, colisión 28×44).

- **No-muerto errante** — `assets/sprites/enemies/no_muerto_errante_custom/`.
  De `Sprites/No muerto errante.png` (que además ya traía una etiqueta
  "SPRITE SHEET 32×48" — aspiracional, la hoja real es de mucho más
  detalle/resolución que eso): `idle`(7), `walk`(9), `attack1`/espadazo(6),
  `vulnerable`/post-ataque(7), `death`(7). Reemplaza a Skeleton Warrior
  (CraftPix, integrado ayer) — ver su propia entrada arriba, que ya quedó
  documentada como "reemplazada" una vez más. Offset/escala: `(0,-35)` /
  `0.6` (colisión 26×42).

- **Espíritu atado** — `assets/sprites/enemies/espiritu_atado_custom/`. De
  `Sprites/espiritu atado.png`: `idle`(8), `attack1`/lunge(6),
  `vulnerable`(4), `death`(4). Esta hoja usa siluetas fantasmales con humo
  que SE TOCAN entre frames vecinos (a diferencia de las armaduras sólidas
  de los otros 3 personajes) — la detección automática de componentes
  conexos fusionaba filas enteras en un solo blob, así que se usó división
  por ancho fijo en su lugar (menos precisa, puede haber leve sangrado de
  un frame al de al lado). Reemplaza a Ghost+Skull (Fatal AI Gaming).
  Offset/escala: `(0,-38)` / `0.6` (colisión 18×26).

**Entorno** (de `Sprites/Nivel 1 II.png`, `Puerta de la cripta 1.png`,
`Checkpoint altar de penitenci.png`, `Fragmento de memoria.png`):
- Fondo de parallax de `Level1.tscn` reemplazado: las 3 capas de
  `battleground1_pale_craftpix_free/` (CraftPix, integrado ayer) por
  `assets/sprites/backgrounds/nivel1_custom_parallax/capa{1,2,3}.png` —
  un castillo bajo la luna específicamente pensado para este nivel, en vez
  de un cementerio genérico. El pack de CraftPix queda sin uso pero no se
  borró.
- `scenes/level/Checkpoint.tscn`: ya no tenía ningún sprite (solo el
  `Area2D` de colisión) — se agregó `assets/sprites/props/
  checkpoint_altar_custom/altar.png` como primer sprite visual real del
  checkpoint.
- `scenes/level/MemoryFragment.tscn`: pasó de un cristal estático
  (`cave_props_craftpix_free`, teñido violeta a mano) a una animación real
  de 4 frames (`assets/sprites/props/memory_fragment_custom/`).
- `PropCryptDoor` nuevo en `Level1.tscn`: la puerta de la cripta (con el
  símbolo de Pharasma) como decoración de fondo (`z_index=-1`) detrás del
  Boss1 en BossArena — puramente visual, sin colisión ni lógica de puerta
  real todavía.

**Sin usar todavía de esta tanda** (quedan en `Sprites/`, no se tocaron):
el resto de animaciones no listadas arriba de cada personaje (salto/ataque2/
aturdido/resurrección reales, no reutilizados), el piso agrietado completo
(`Piso agrietado.png` — hoy el hazard del Tramo C sigue siendo el
`ColorRect` rojo original), el indicador de Penitencia/Corrupción
(`Penitencia corrupcion.png` — no existe ese sistema en el código todavía,
es UI para una mecánica no implementada), la Arena del Boss como set
completo (`Arena del boss.png`, se usó implícitamente solo referencia de
mood), y `Puerta de la cripta 2.png` (variantes/desglose adicional de la
puerta). La carpeta `Sprites/Base/` (renombrada por Marcos a `descarte/`)
se ignoró a propósito, a pedido explícito.

**UI de menús** (de `PHARASMA/Sprites/`, tanda del 2026-08-27):
- `assets/sprites/ui/title/title_logo.png` — emblema "Vaelith Arken" (RGBA
  2167×725, ya venía con alfa). Reemplaza el `Label` de texto plano
  `"VAELITH ARKEN"` en `scenes/ui/TitleScreen.tscn` por un `TextureRect`.
- `assets/sprites/ui/menu_plates/` — 6 placas góticas (header + botones),
  con el texto horneado en la imagen. Se separaron de una hoja única sobre
  fondo blanco plano (1536×1024, sin alfa) con un script propio (Python/PIL):
  máscara de fondo por cercanía al blanco + flood-fill desde los bordes del
  recorte (transparenta solo el fondo exterior, no el panel oscuro interior
  ni el texto dorado), despeckle y recorte al bbox del alfa. Ver
  `menu_plates/FUENTE.txt`.
  - `TitleScreen.tscn`: `iniciar_partida` / `salir_del_juego` reemplazan los
    `Button` con texto (`StartButton` / `QuitButton` → `TextureButton`).
    `menu_principal` queda extraída pero sin usar (redundante con el logo).
  - `PauseMenu.tscn`: `menu_de_pausa` (header), `continuar_partida` /
    `regresar_menu_principal` (botones). El `Panel` `ColorRect` azul plano
    pasó a `Control` transparente (las placas traen su propio marco).
- Import con `mipmaps/generate=true` + `texture_filter` linear-mipmap en los
  nodos, para que el downscale de estas texturas grandes se vea nítido.
- `assets/sprites/ui/cursor/` — cursor de mouse propio, extraído de
  `PHARASMA/Sprites/Puntero.png` (hoja con alfa, generada por Marcos con IA).
  8 estados (normal / hover / click / precisión / ocupado / interactuable /
  enemigo / no-disponible), recortados y escalados a 44–62 px. `CursorManager`
  (autoload) los asigna a los shapes de Godot. **Contenido propio, sin
  atribución.**
- `assets/sprites/ui/dialogue/` — 2 marcos de caja de diálogo extraídos de
  `source_sheets/ui/dialogue_box_frames.png` (fondo blanco, mismo key por
  flood-fill que las placas). `options_frame.png` (barra ancha) reemplaza el
  `ColorRect` plano de `DialogueBox.tscn` como `NinePatchRect`;
  `narration_frame.png` (caja alta con calavera) queda para los momentos de
  narración/fragmento de memoria (Fase 8).

## Cuarta tanda (2026-08-28) — GothicVania Cemetery + tipografía

- **GothicVania Cemetery (Ansimuz)** — `assets/sprites/tilesets/gothicvania_cemetery_CC0/`
  Fuente: `ansimuz.itch.io/gothicvania-cemetery`.
  Licencia: **CC0** confirmada (`public-license.pdf` incluido, sin
  restricciones de uso ni atribución) — mismo autor y misma licencia que
  `gothicvania_town_CC0` (arriba). Resuelve el bloqueante de
  `docs/ASSETS_PENDIENTES.md` (reemplazo de `dead_trees_atlas.png`, que no
  era recortable) y desbloquea la Fase 3 de `docs/roadmap_level1_largo.md`.
  Se integraron `layers/` (parallax: cielo+luna, montañas, silueta de
  cementerio), `sliced-objects/` (árboles, arbustos, plataformas de piedra,
  estatua — ya venían recortados por el autor) y `tileset.png`/
  `tileset-sliced.png` (sin armar como `TileSet` todavía). Se descartaron
  `Characters/` (el proyecto usa su propio elenco), `PSD/` y `Phaser Demo/`.
  Detalle completo en el `README.md` de la carpeta.

- **Gothic Pixels (Akezhar)** — `assets/fonts/Gothic Pixels.ttf`
  Fuente: `akezhar.itch.io/gothic-pixels`.
  Licencia: **CC0** confirmada en la página del producto ("puede usarse
  como quieras, para uso comercial y no comercial").
  Aplicada como fuente global del proyecto (`project.godot` →
  `[gui] theme/custom_font`), reemplaza la fuente default de Godot en toda
  la UI sin tocar cada escena. Import ajustado a mano (antialiasing/hinting/
  subpixel desactivados) para que se vea nítida como pixel art — el
  importador de Godot por defecto la suaviza como tipografía normal.

## Pendientes de descarga manual (bloqueados por flujo de compra de itch.io)

El resto de los candidatos de `docs/lista_assets_pixel_art.md` y
`docs/lista_audio.md` (UI, VFX, SFX, tileset alternativo gótico, etc.) siguen
pendientes de que se bajen manualmente — itch.io y CraftPix gatean la
descarga detrás de un flujo JS con sesión de navegador que no es scripteable
de forma confiable. A medida que se agreguen a `Herramientas/Pixelherramientas/`,
se integran y documentan acá.
