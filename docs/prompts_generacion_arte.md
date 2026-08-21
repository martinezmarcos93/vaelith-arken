# Lista de Assets + Prompts de Generación

Cruce de `lista_assets_pixel_art.md` (qué falta y su estado), `diseno_enemigos.md`,
`diseno_boss1.md`, `layout_level1.md`, `GDD.md` y `guia_estilo_visual.md`, con un
prompt de generación de imagen adjunto a cada ítem. Vocabulario de prompt tomado
del sistema estudiado en `Estetica ideal/Estudio_Dark_Fantasy_Codex.md` (fórmula
de 5 bloques, referencias de artista, profile code de Midjourney), adaptado a la
**paleta propia del juego** (`guia_estilo_visual.md`), no a la paleta de ese PDF
de terceros — son dos investigaciones distintas, no mezclar los hex de una con la
otra.

## Regla de uso — leer antes de generar nada

Esto **no reemplaza** la decisión ya tomada en `guia_estilo_visual.md` §6: un
generador de imágenes no produce grilla de píxeles limpia, fondo transparente ni
frames de animación consistentes. Para todo lo que es **sprite animado**
(personajes, enemigos, VFX con frames), el resultado de estos prompts es
**referencia visual para pixelear a mano en LibreSprite**, no el asset final.

Para **texturas/fondos estáticos** (tileset, parallax, arena) sin requisito de
transparencia ni frames, generar + el pipeline de dithering descrito en
`Estetica ideal/Informe_Sistema_Estetica_DarkFantasy.md` §6.2 (reducción de
paleta + Floyd-Steinberg) es técnicamente viable como *posible* asset semi-final,
no solo referencia — pero eso es una ampliación de alcance que no está decidida
todavía. Tratarlo como referencia hasta que decidas explícitamente lo contrario.

**Herramienta:** Leonardo.ai (gratis, permite imagen de referencia — ver
`guia_estilo_visual.md` §6). Los prompts están en inglés (mejor comprensión de
los modelos) en formato universal, sin sintaxis de Midjourney. Si en algún
momento pagás Midjourney, sumá `--profile s7q3uzu` (perfil "Pixel Art Dark
Fantasy" verificado en `Estudio_Dark_Fantasy_Codex.md` §2.5) al final de
cualquiera de estos prompts.

## Bloque de estilo común

Todos los prompts de abajo asumen este bloque agregado al final (no lo repito
en cada uno, salvo variación puntual):

```
STYLE: dark fantasy pixel-art game concept art, 16-bit retro RPG box-art
tradition (Amiga/DOS/SNES era covers), painterly, in the spirit of Caspar
David Friedrich (lone figure against vast landscape) and Gustave Doré
(gothic engraving detail); cinematic lighting, volumetric fog, matte
painting, chiaroscuro, dramatic shadows, ancient weathered moss-covered
stone. Frank Frazetta only as compositional-boldness reference, not for
color (his warm palette conflicts with this project's cold palette).

PALETTE: cold-dominant — near-black (#010901, extended range #0f1f12/
#181d14/#000a01 for tonal variety), blue-violet (#2B2E56, #3A5184,
#3B4272, extended #313682/#4947a7/#205188), dark teal (#07424F, extended
#10423b), deep violet (#766DBC, #493165, #352037, extended #7a36a2 for
high-intensity magic moments only). Three warm accents, each with a fixed
non-interchangeable role, always a small minority of the frame (~70-80%
cold): (1) danger red #B41F1C — saturated, only for active
threat/blood/attack telegraphs; (2) rust-red #4d1409 — desaturated,
environmental wear/decay (rust, dried blood, dead embers), CAN appear as
ambient texture since it doesn't read as "urgent"; (3) muted gold ~#8A7040
— sacred/non-urgent only (Pharasma symbols, checkpoints). See
`guia_estilo_visual.md` §1.1-1.2 for the full derivation.

NEGATIVE: bright cheerful colors, evenly distributed warm tones,
photorealism, anime, cel-shading, glossy plastic surfaces, modern sci-fi
elements, clean vector line art, oversaturation.
```

**Consistencia entre generaciones:** subí como imagen de referencia una de las
ya curadas en `Estetica ideal/` (o una generación previa ya aprobada) antes de
generar la siguiente — mantiene paleta y atmósfera coherentes en vez de
depender solo del texto.

---

## SPRITES

### Personaje

#### 1. Vaelith Arken (protagonista) — 🔴 Custom obligatorio
**Uso:** referencia de proporción/armadura para pixelear a mano (32x48px base).
Ya existe una referencia de proporción no-final: [FREE - Knight 2D Pixel Art
(Mattz Art)](https://xzany.itch.io/free-knight-2d-pixel-art) — usar el prompt de
abajo para afinar el diseño específico del lore antes de dibujar.

```
SUBJECT: A lone armored knight, full plate armor scarred and weathered,
a kite shield bearing a faint carved symbol of Pharasma (a spiral/hourglass
motif), a longsword held low, a ceremonial dagger sheathed at the hip.
Face mostly hidden by a battered helm, hint of pale "returned from death"
skin at the jaw.
SCENE: standing alone on a cracked stone path in a corrupted gothic ruin,
fog at his feet, faint blue-violet moonlight from above.
DETAILS: ivy growing through cracks in the armor joints, a single faint
red glow line where the sword meets the hilt (foreshadows attack
telegraph color), no other warm color anywhere in frame.
```

#### 2. Boss 1 — Guerrero-Espejo — 🔴 Custom obligatorio
**Uso:** referencia — comparte diseño de armadura/pose con Vaelith
(`diseno_boss1.md`), no se puede resolver sin el diseño de Vaelith primero.
Generar recién después de aprobar el prompt #1.

```
SUBJECT: A mirrored version of [the same knight described in prompt #1],
but corrupted — the armor is cracked with a stylized mask over the helm
that shows visible fracture lines (telegraphs the phase-transition at 50%
HP described in diseno_boss1.md), same kite shield with the Pharasma
symbol now inverted/corrupted, same longsword stance.
SCENE: standing in a ruined ceremonial hall, twin braziers flanking a
cracked ceremonial floor, near-symmetrical composition (this boss is
literally a mirror of the player).
DETAILS: the mask crack glows faint red only along the fracture line,
otherwise identical cold palette to Vaelith — the point is that they look
like the same person, not two designs.
```

#### 3. No-muerto errante (enemigo regular A) — 🟡 Placeholder ya integrado
**Estado:** resuelto con el pack `necromancer_creativekind_free_commercial_ok`
(`assets/sprites/enemies/`, CC, uso comercial permitido) — ya en uso en
`NoMuertoErrante.tscn`. Prompt solo si en algún momento se decide reskin propio.

```
SUBJECT: A slow shambling undead warrior in corroded plate armor
(rust-red #4d1409 undertone on the metal, not the vivid danger red),
rusted longsword raised in a slow telegraphed swing, hollow glowing eye
sockets.
SCENE: patrolling a narrow stone corridor, dim ambient light.
DETAILS: the sword catches a brief SATURATED red glow (#B41F1C, distinct
from the rust undertone) 0.4s before the swing — this glow IS the
gameplay telegraph, must read clearly even in a dark cold palette.
```

#### 4. Espíritu atado (enemigo regular B) — 🟡 Placeholder ya integrado
**Estado:** resuelto con `ghost_skull_fatalaigaming_free` (gratis, sin
atribución) — ya en uso en `EspirituAtado.tscn`. Prompt solo para eventual
reskin.

```
SUBJECT: A translucent bound spirit, chained wisps of ethereal energy
trailing from its limbs as if restrained against its will, faint humanoid
shape barely holding form.
SCENE: floating in a vertical drifting pattern in a narrow ruined chamber.
DETAILS: pale blue-violet translucency (#766DBC tint), no red — this
enemy's threat reads through erratic movement, not a color telegraph
(diseno_enemigos.md), keep it visually gentler/sadder than menacing.
```

### Elemento

#### 5. Barra de vida (HUD) — 🟢 Pack viable
```
SUBJECT: A gothic-framed health bar UI element, ornate carved stone or
aged bronze frame, fill in deep red (#B41F1C) against a near-black
background panel.
DETAILS: worn/weathered edges, small skull or blade motif at one end,
no gloss/bevel (flat pixel-art readable at small HUD size).
```

#### 6. Indicador de penitencia/corrupción del nivel — 🔴 Custom
**Nota:** mecánica única del juego (`GDD.md` pilar 3), ningún pack genérico lo
resuelve conceptualmente. Color exacto sin definir todavía.

```
SUBJECT: A small gothic icon/meter representing accumulating corruption —
concept: a cracked hourglass or a spreading dark stain filling a vessel,
tied visually to the Pharasma symbol.
DETAILS: starts near-black/clean, fills with a corrupted violet-red mix as
it increases — needs a distinct silhouette from the health bar so players
never confuse the two at a glance.
```

#### 7. Marco de diálogo — 🟢 Pack viable
```
SUBJECT: A gothic dialogue box frame, dark stone or aged parchment-on-iron
texture, thin carved border, corners with small worn engravings.
DETAILS: sober, low ornamentation (guion_intro.md tone: "texto sobrio, sin
exceso de iconografía") — legible over dark backgrounds.
```

#### 8. Menú principal / 9. Menú de pausa — 🟢 Pack viable
```
SUBJECT: A dark fantasy game main-menu background — a distant silhouette
of the corrupted gothic ruin from the game's opening, low fog, single
moon.
SCENE: same cold palette, composition leaves clear negative space at
center-bottom for menu buttons.
DETAILS: extremely restrained — this screen is seen the longest, avoid
visual fatigue; no red accent here at all (reserve it for gameplay danger
only).
```

#### 10. Cursor / selector de menú — 🟢 Pack viable
```
SUBJECT: A small gothic cursor icon — a stylized dagger point or carved
bone marker.
DETAILS: single small shape, must read clearly at tiny UI scale, cold
palette with no red.
```

#### 11. Impacto de espada (VFX) — 🟢 Pack viable
**Nota:** ya hay un pack genérico integrado (`effect_bullet_16x16_bdragon1727`)
que puede resolver esto directo o servir de base; prompt solo si no calza.
```
SUBJECT: A short sharp sword-impact spark burst, 3-4 frame pixel-art VFX.
DETAILS: cold white-blue core flash, no red (red is reserved for
danger/telegraph, not player-caused impact — avoid ambiguity).
```

#### 12. Chispa de bloqueo/parry (VFX) — 🟢 Pack viable
```
SUBJECT: A metallic shield-block spark burst, brighter and more angular
than the sword impact (#11), reads as "successful defense".
DETAILS: blue-white sparks radiating outward, quick 3-frame burst.
```

#### 13. Polvo al aterrizar/correr (VFX) — 🟢 Pack viable
```
SUBJECT: Small ground dust puffs, muted grey-violet, low-key.
DETAILS: subtle, must not distract from combat readability.
```

#### 14. Brillo de telegrafiado de ataque (enemigo) — 🔴 Custom
**Nota:** color y timing son parte del "lenguaje de lectura justa" del combate
(`lista_assets_pixel_art.md` §7) — no delegar a un pack genérico.
```
SUBJECT: A tight red (#B41F1C) glow/edge-light effect that outlines a
weapon 0.4-0.5s before an enemy attack lands.
DETAILS: must be unambiguous against the cold-dark background at a glance
— this is a gameplay-critical readability element, not decoration.
```

#### 15. Destello de fragmento de memoria (VFX narrativo) — 🔴 Custom
```
SUBJECT: A soft violet (#766DBC) particle/glow burst, warm-feeling despite
being cold-hued — signals "narrative reward", distinct from the red danger
glow (#14) and from generic combat sparks.
DETAILS: slower, more ethereal motion than combat VFX.
```

#### 16. Fragmento de memoria (pickup) — 🔴 Custom
```
SUBJECT: A small floating shard/rune object, faintly emitting the violet
glow of item #15, idle bobbing animation (2-4 frames).
SCENE: resting on a stone pedestal or embedded in ruin debris.
DETAILS: must read as "collectible, narrative, safe" — no red, no threat
connotation.
```

#### 17. Puerta con símbolo de la cripta — 🔴 Custom
```
SUBJECT: A massive weathered gothic stone door, carved with the Pharasma
spiral/hourglass symbol at its center, faint muted gold (~#8A7040) glow
along the carved lines (sacred, non-urgent — not the danger red).
SCENE: set into a cracked stone archway, ivy at the base.
DETAILS: symbol must be legible as the same motif used on Vaelith's shield
(#1) — visual continuity of "this is Pharasma's mark".
```

#### 18. Checkpoint (icono/altar) — 🔴 Custom
```
SUBJECT: A small stone altar or standing rune-stone, same muted gold
accent as the door (#17), a subtle upward light beam when active.
DETAILS: distinct silhouette from the memory-fragment pickup (#16) — one
is "save point", the other is "collectible", must not be confusable at a
glance.
```

#### 19. Tipografía — 🟢 Ya resuelto, sin prompt
Sin generación de IA — decisión ya tomada: [Gothic Pixels (Akezhar)](https://akezhar.itch.io/gothic-pixels),
gratis, uso comercial explícito (`lista_assets_pixel_art.md` §8). Pendiente
solo bajarla y verificar legibilidad al tamaño real del HUD.

---

## TEXTURAS

### Escenario

#### 20. Tileset base — piso/paredes/columnas/escaleras (Level 1) — 🟡 Pack integrado, pendiente recolor
**Estado:** `dungeon_golopin_free` y `dungeon_raou_free_commercial_ok` ya
integrados (`CREDITS.md`) — el segundo ("Dark Dungeon Side-Scroller") ya
calza casi exacto con la paleta propia. Prompt solo como referencia si el
recolor en LibreSprite no alcanza y se evalúa generar tileset propio.
```
SUBJECT: A seamless dark gothic dungeon tileset — stone floor, wall,
column and staircase pieces, weathered and cracked.
PALETTE: match exactly the game's cold palette (see bloque común) — this
must tile cleanly, no directional lighting baked in.
```

#### 21. Piso agrietado (hazard, Tramo C) — 🔴 Custom
```
SUBJECT: A cracked, crumbling stone floor tile variant, visibly distinct
from the safe floor tiles (#20) at a glance — deeper cracks, small debris,
rust-red (#4d1409) staining in the deepest cracks (ambient decay, not the
saturated danger red — this is a static hazard, not an active telegraph).
DETAILS: must read as "hazardous" through silhouette/shape first, color is
a secondary cue, since the game's dark palette can't rely on bright
warning colors everywhere.
```

#### 22. Fondo lejano / parallax capa 1 — 🟢 Ya integrado
**Estado:** `gothicvania_town_CC0/layers/background.png`, ya en el proyecto.
Sin prompt necesario salvo reskin.

#### 23. Fondo medio / parallax capa 2 — 🟢 Ya integrado
**Estado:** `gothicvania_town_CC0/layers/middleground.png`, ya en el proyecto.
Sin prompt necesario salvo reskin.

#### 24. Niebla / ceniza ambiental (partículas + textura base) — 🟢 Pack viable
```
SUBJECT: A soft wispy fog/ash texture, semi-transparent, cold blue-grey
tint, suitable for a looping particle system layer.
DETAILS: no hard edges, must read as atmosphere, not a solid object.
```

#### 25. Arena del Boss 1 — 🔴 Custom, orientativo (Fase 6.3 sin cerrar)
**Nota:** `diseno_boss1.md` deja tamaño/hazards de la arena sin definir todavía
— este prompt es de dirección de arte, no de layout final.
```
SUBJECT: A ceremonial ruined hall, near-symmetrical, twin braziers with
cold blue-white flame (not warm fire — keep palette consistent), a cracked
circular floor motif at the center matching the Pharasma symbol.
SCENE: enough open floor space to imply a boss arena, tall broken pillars
framing the sides.
DETAILS: this room should visually rhyme with the door (#17) and
checkpoint (#18) — same sacred-symbol language, now on a much larger
scale and corrupted.
```

### Elemento

#### 26. Antorchas / fuentes de luz — 🟢 Ya integrado
**Estado:** `dungeon_raou_free_commercial_ok/spr_torch.png`, ya en el proyecto.
Sin prompt necesario salvo reskin.

#### 27. Escombros / columnas rotas decorativas — 🟢 Ya integrado
**Estado:** vienen incluidos en el tileset Golopin (81 piezas en
`tilemap_objects/`), ya en el proyecto. Sin prompt necesario.

#### 28. Vegetación muerta / lápidas / huesos (decoración) — 🟡 Parcial
**Estado:** parcialmente cubierto por el tileset Golopin + GothicVania props
(`props.png`). Prompt solo si hace falta variedad adicional.
```
SUBJECT: Small dark-fantasy dungeon set-dressing props — dead twisted
trees, cracked tombstones, scattered bones, moss patches.
DETAILS: must match the cold palette exactly, no warm autumn tones. Rust-
red (#4d1409) is allowed as a subtle weathering undertone (old blood on a
tombstone, rusted grave-iron) — muted gold/danger red are not, both are
reserved for their fixed roles elsewhere.
```

---

## Resumen de qué necesita prompt de verdad

| Categoría | Ítems 🔴 (prompt = obligatorio, custom) | Ítems 🟡/🟢 (prompt = opcional, ya resuelto o reskin futuro) |
|---|---|---|
| Sprites > Personaje | Vaelith (#1), Boss 1 (#2) | No-muerto errante (#3), Espíritu atado (#4) |
| Sprites > Elemento | Indicador de penitencia (#6), telegrafiado (#14), destello de memoria (#15), fragmento de memoria (#16), puerta (#17), checkpoint (#18) | HUD/menús/cursor/VFX genérico (#5, #7-13), tipografía (#19) |
| Texturas > Escenario | Piso agrietado (#21), arena Boss 1 (#25) | Tileset base (#20), parallax (#22, #23), niebla (#24) |
| Texturas > Elemento | — | Antorchas (#26), escombros (#27), decoración (#28) |

**Orden sugerido si vas a generar referencia ahora:** #1 (Vaelith) primero —
todo lo demás custom (#2, #17, #18, #25) depende visualmente de él. Después
#14/#15/#16 (lenguaje de VFX narrativo/telegrafiado, son pocos y muy
reusables). El resto puede esperar sin bloquear nada del roadmap.
