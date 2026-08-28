# assets/sprites/props/vaelith_torre/

Props de la Torre del nigromante (Sector Torre / Intro re-vestida del
`roadmap_level1_largo`). Preparados por Marcos el 2026-08-28 a partir de las
láminas de composición IA de `assets/source_sheets/environment/` (que **no** son
recortables por código — ver `docs/ASSETS_PENDIENTES.md`).

Todos: PNG RGBA, fondo transparente, recortados por pieza.

## `architecture/` — de `gothic_architecture_atlas.png`
16 piezas: `arched_door`, `ruined_arch`, `tall_arch`, `column_plain/twisted/draped`,
`barred_gate_01/02/03`, `spiral_staircase`, `altar_01/02`, `balcony_segment`,
`gargoyle`, `rubble_pile_01/02`. Limpias, un objeto por archivo.

## `props/` — de `dark_fantasy_props_bodies_sheet.png`
12 piezas: `ritual_table_01/02`, `failed_experiment_corpse_01/02`, `skull_01`,
`skull_bones_cluster_01`, `bone_pile_01`, `stone_blocks_01/02`, `stone_rubble_03`,
`rubble_pile_01/02`.

Batch de la 1ª pasada de Marcos (sin re-cortar). Limpias y usables:
`ritual_table_01/02`, `failed_experiment_corpse_01/02`, `skull_bones_cluster_01`,
`stone_blocks_02`. **Recortadas por Claude (2026-08-28)** para sacarles una
banda superior con figura humanoide / franja de gore de la lámina original:
`rubble_pile_01`, `rubble_pile_02` (quedó muy fina, casi no se usa),
`stone_rubble_03`, `bone_pile_01`. `stone_blocks_01` y `skull_01` traen huesos
extra pegados arriba — usar recortadas o de fondo.

## `fire/` — de `fire_and_particles_sheet.png` (batch `recut_final` + trim)
6 piezas: `candelabrum`, `candle_group`, `wall_torch`, `floor_brazier_warm`,
`floor_brazier_violet`, `hanging_lantern`. Complementan la iluminación
`PointLight2D` procedural; no la reemplazan.

## `vfx/` — de `fire_and_particles_sheet.png`
4 piezas: `corruption_flame_violet_static`, `floor_projection_violet` (círculo
ritual en piso), `spectral_flame_violet`, `smoke_gray`. **No hay tira de frames**
de la llama de corrupción — la fuente no la tiene; la animación se resuelve con
`PointLight2D` pulsante hasta tener frames reales.

Notas de recorte (Claude, 2026-08-28): sobre el batch `recut_final` de Marcos se
hizo un recorte rectangular manual adicional a 5 archivos que aún traían un
objeto vecino separado (`candle_group`, `floor_brazier_violet`, `hanging_lantern`,
`floor_projection_violet`, `spectral_flame_violet`, `corruption_flame_violet_static`)
para dejar un solo objeto por PNG. Detalle en `docs/ASSETS_PENDIENTES.md §2e`.
