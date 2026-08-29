# assets/sprites/tilesets/gothicvania_cemetery_CC0/

GothicVania Cemetery (Luis Zuno / Ansimuz), CC0 (`public-license.pdf`
incluido). Reemplazo del `dead_trees_atlas.png` bloqueado en
`docs/ASSETS_PENDIENTES.md` — desbloquea la Fase 3 (Sector Bosque + gauntlet)
de `docs/roadmap_level1_largo.md`. Mismo autor que `gothicvania_town_CC0/`
(ya integrado), misma convención de carpetas.

Se descartaron `Assets/Characters/` (Hero/Enemies — el proyecto usa su propio
elenco), `Assets/PSD/` (fuente de edición, no se importa a Godot) y
`Assets/Phaser Demo/` (proyecto Phaser.js, no aplica).

## `layers/` — parallax
- `background.png` (384×224) — cielo violeta con luna, ya alineado con la
  paleta de corrupción del juego.
- `mountains.png` (192×179) — silueta de montañas.
- `graveyard.png` (384×123) — silueta de primer plano: lápidas + árboles
  muertos + capilla pequeña.

## `sliced-objects/` — props, un objeto por PNG, ya recortados por el autor
`tree-1/2/3` (166×117 / 166×117 / 176×171), `bush-large` (76×65),
`bush-small` (34×29), `statue` (63×75, figura encapuchada), `stone-1..4`
(~27×39, plataformas de piedra pequeñas).

## `tileset.png` / `tileset-sliced.png` (448×160)
Grid de piso/plataforma con pasto y una columna. Sin `TileSet` de Godot
armado todavía (pendiente para cuando se diseñe el tilemap de la Fase 3,
mismo paso que se hizo con `dungeon_raou_free_commercial_ok/raou_tileset.tres`).

## `objects.png` (992×224) — sin recortar
Hoja suelta con variantes extra (lápidas de otras formas, cruz+pasto,
estatua encapuchada con guadaña, árboles más grandes) que el autor no
pre-recortó en `sliced-objects/`. Se conserva como referencia — recortar bajo
demanda si al diseñar la Fase 3 hace falta una variante puntual que no esté
ya en `sliced-objects/`.
