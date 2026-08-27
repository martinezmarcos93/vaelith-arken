# Roadmap — Level 1 largo (torre → bosque → torre → arena)

> Aprobado 2026-08-27. Reemplaza el Level 1 greybox actual por el recorrido
> completo de la Escena 1 según la visión de Marcos + brief §7/§11.
> Fuente narrativa: `guion_demo.md`. Diseño de sectores: assets de
> `assets/source_sheets/` (auditoría de esta sesión, ver más abajo).

## Visión de la Escena 1

Vaelith **no aparece en medio de la nada**: despierta en las **ruinas de su
vieja torre de nigromante**. Al salir se encuentra varios muertos vivientes
sueltos que antes controlaba. Atraviesa el bosque recolectando memorias hasta
una **segunda torre**, donde combate más, encuentra más memorias y termina
enfrentando a un **constructo que él creó y que replica su personalidad** (el
Guerrero-Espejo).

Reglas transversales:
- Cada sector decorado con lo que le corresponde estéticamente. **Nada colgando
  ni flotando sin sentido** — todo apoyado/motivado (antorchas en pared, huesos
  en el piso, hiedra sobre arcos).
- **Todo el espacio aprovechado**, ningún sector pelado.
- Recolectar **cráneos baja la corrupción** que se acumula cuando Vaelith muere.

## Decisiones cerradas (2026-08-27)

| Tema | Definición |
|---|---|
| Estructura | **Un** Level 1 largo con checkpoints. Corrupción resetea al completar el nivel completo. |
| Frames del despertar | No se rediseñan todavía. La Intro se re-decora como interior de torre; los frames de Vaelith no se tocan. |
| 3 clases de undead | ① Zombi devorado (`zombi_devorado_custom`, extraído) · ② No-muerto errante (`no_muerto_errante_custom`) · ③ Espíritu atado (`espiritu_atado_custom`). Esqueleto (`skeleton_warrior_craftpix`) como 4ª de relleno. Todos mueren en 2 golpes altos. |
| Corrupción | +1 nivel por muerte (máx 3) → +1 enemigo extra y −luz por nivel. Cada cráneo −1. Reset al completar el nivel. |
| Cielo/parallax | `Nuevo cielo.png` (1672×941) reemplaza el atlas de paneles chicos. Profundidad con strips de montaña/silueta encima. |

## Fases

| Fase | Objetivo | Estado |
|---|---|---|
| **0 · Extracción** | `level1_ruins_tileset` → `TileSet` 32×32 · `zombie` → AnimatedSprite2D · atlas de props/VFX (árboles, huesos, arquitectura, cementerio, fuego, decals, arena, combat_vfx) a carpetas. Doc roadmap + update auditoría. | zombi ✅ · resto pendiente |
| **1 · Parallax + Intro re-vestida** | 5 capas de parallax propias. Intro: mismo guion/frames, escenario = interior de torre (columnas rotas, mesas rituales, cadáver en losa, braseros violetas). | — |
| **2 · Sector Torre** | Tilemap de la torre con el TileSet nuevo. Vaelith arranca dentro/al pie. Puerta con brillo violeta = umbral al bosque. 1-2 espíritus. Fragmento I. | — |
| **3 · Sector Bosque + gauntlet** | Cementerio del bosque: tumbas/ataúdes abiertos = spawns. ≥10 undead, 3 clases, 2 golpes = muerte. Árboles corruptos, troncos, huesos, decals de sangre/huellas. Fragmentos II-III. | — |
| **4 · Loop corrupción ↔ cráneos** | `GameState.corruption` (0-3). `_die` → +1. `collect_skull()` → −1. `CorruptionController` por tramo: +1 enemigo, baja `PointLight2D`, sube fuego violeta, viñeta. Reset al fin de nivel. Indicador en HUD. | — |
| **5 · Sector 2ª Torre** | Columnas de basalto, mausoleo grande de base, estructuras corruptas. Combate denso (3 clases). Fragmentos IV-VI. Rastro de huellas hacia la arena. | — |
| **6 · Arena del constructo** | `mirror_warrior_arena_sheet`: plataforma circular, estatuas-espejo, escaleras, eclipse corrupto, cara-portal de entrada. Boss `espejo_boss_custom`. "El último día" → Epílogo. | — |
| **7 · VFX combate + pase final** | `combat_vfx` → impacto/parry/destello-narrativo/polvo/muerte. Iluminación motivada (antorchas/braseros + `PointLight2D`). Charcos con reflejo, goteras. Pase de densidad. | — |

Commit atómico por fase. Verificación en Godot antes de "hecho". Si algo falla,
no se propone la fase siguiente.

## Mapa asset → sector (de la auditoría)

| Sector | Hojas fuente |
|---|---|
| Torre del nigromante | `funerary_ruins_tileset`, `gothic_architecture_atlas` (columnas, escalera caracol, ventanas con reja, nichos), `dark_fantasy_props_bodies` (mesas rituales, **cadáver en losa = experimento fallido**), `fire_and_particles` (braseros violetas) |
| Bosque / cementerio (gauntlet) | `gothic_cemetery_sheet` (**tumbas/ataúdes abiertos = spawns**), `skulls_and_bones_atlas`, `dead_trees_atlas` (árboles corruptos, troncos), `gothic_dungeon_decals` (sangre, **huellas**, huesos) |
| Bosque (travesía) | `dead_trees_atlas` (parallax), `Nuevo cielo.png` + siluetas de bosque, `rocks_and_ruins_atlas` (arcos naturales), `water_and_wet_terrain` (charcos, agua corrupta), `arcane_corruption_floor_tiles` (progresión) |
| 2ª Torre | `gothic_architecture_atlas`, `rocks_and_ruins_atlas` (columnas basalto), `gothic_cemetery_sheet` (mausoleo grande), `supernatural_corruption_atlas` (estructuras corruptas, raíces oscuras), `fire_and_particles` (fuego violeta) |
| Arena | `mirror_warrior_arena_sheet`, `Nuevo cielo.png` (eclipse), `supernatural_corruption_atlas` (cara-portal, energías), `combat_vfx_sheet` |
| Transversal | decals + huesos + fuego + charcos = "todo cubierto", todo apoyado/motivado |

## A rediseñar por tamaño (flags de la auditoría)

1. ~~Paneles de cielo (~360×200)~~ → resuelto con `Nuevo cielo.png` (1672×941).
2. Capas de parallax de `funerary_ruins_tileset` / `level1_ruins_tileset`
   (~360×180) — aceptable muy al fondo + desenfoque; grandes si se quieren leer.
3. Frames de Vaelith despertando (~50-130px) — **no se rediseñan todavía**
   (decisión). Intro con cámara cercana mientras tanto.
4. Swatches de suelo de `rocks_and_ruins_atlas` (~90px) — usar como detalle, no
   como piso principal. Piso principal: `level1_ruins_tileset` 32×32 +
   `arcane_corruption_floor_tiles` (~120px).

## Abierto

- ¿La corrupción también cambia el epílogo / diálogo final?
- v1 vs v2 de `level1_ruins_tileset` — a elegir en Fase 0 (v2 tiene paneles más
  limpios).
