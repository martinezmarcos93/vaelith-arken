# Assets pendientes

Registro de assets que **no pueden extraerse limpiamente** con el pipeline
CLI (PIL / componentes conexos / matting de alfa) y necesitan preparación
gráfica externa antes de integrarse a Godot.

Regla (CLAUDE.md del proyecto + instrucción de Marcos 2026-08-28): cuando una
lámina requiere separación, transparencia, reconstrucción o generación, Claude
**se detiene y lo anota acá** con el detalle de qué se necesita. No se improvisa
una extracción degradada.

Formato de entrega preferido: **PNG con fondo transparente, recortado (trim) al
contenido, un archivo por pieza**. Alternativa aceptable: una grilla uniforme
con celdas de tamaño fijo + un manifiesto (nombre por celda); en ese caso indicar
el tamaño de celda y Claude la corta.

---

## Bloqueantes activos

### 1. Bosque / cementerio — `gothicvania-cemetery-files.zip`
- **Estado:** pendiente de descarga manual de Marcos.
- **Fuente:** `ansimuz.itch.io/gothicvania-cemetery` (CC0, $0). itch.io no permite
  descarga por link directo (protección anti-scraping).
- **Bloquea:** Fase 3 del `roadmap_level1_largo` (Sector Bosque + gauntlet).
- **Qué trae:** árboles retorcidos, lápidas, plataformas de piedra, columnas —
  reemplazo ya recortado de `dead_trees_atlas.png`.
- **Nota:** no reconstruir árboles desde `dead_trees_atlas.png` ni improvisar un
  bosque sustituto. Fase 3 queda congelada hasta que el zip esté en el proyecto.

### 2. Torre del nigromante — 3 láminas de composición IA
Las tres viven en `assets/source_sheets/environment/` y son referencia
pictórica (fondo degradé, sin grilla, banners y tira de paleta horneados,
sombras/glow que puentean piezas). No recortables por código.

Bloquean el **dressing definitivo** de Fase 1 (Intro re-vestida) y Fase 2
(Sector Torre) del `roadmap_level1_largo`. *No* bloquean construir el sector con
dressing interino (Raou tileset + props craftpix ya integrados) — ver roadmap de
la sesión.

#### 2a. `props/gothic_architecture_atlas.png`
Piezas necesarias para Torre (transparente, recortadas, una por archivo):
- Columnas / pilastras rotas — 2-3 variantes
- Arco gótico (para vanos y umbral)
- Ventana con reja ("REJAS Y VENTANAS CON REJAS")
- Nicho / altar mural ("NICHOS Y ALTARES MURALES")
- Escalera caracol ("ESCALERAS Y PLATAFORMAS")
- Escombros / ruinas ("ESCOMBROS Y RUINAS") — 2-3 montones
- Aprox. 15-20 piezas.

#### 2b. `props/dark_fantasy_props_bodies_sheet.png`
- Mesas rituales — las 2 con velas / tomos / frascos
- **Cadáver en losa = experimento fallido** — 2 variantes (la figura encadenada
  y la envuelta en raíces/tendones)
- Cráneos sueltos + montones de huesos
- Bloques de piedra tallada
- Aprox. 10-12 piezas. **Omitir** las filas de figura humanoide de arriba
  (referencia de personaje, no props) y la tira de paleta de abajo.

#### 2c. `effects/fire_and_particles_sheet.png`
- Antorchas de pared encendidas — idealmente tira de 3-4 frames de llama
- Braseros de piso ("BRAZEROS")
- **Fuego violeta / corrupción** ("FUEGO VIOLETA / CORRUPCIÓN") — cluster
- Velas / candelabros — 2-3
- Decal de luz proyectada en el piso ("PROYECCIONES / LUZ EN SUELO")
- Lo animado como tira de frames (indicar frames por pieza).

---

## Resueltos / sin acción

- `level1_ruins_tileset.png` / `_v2` — referencia de Marcos, no grid. Reemplazado
  por `dungeon_raou_free_commercial_ok/raou_tileset.tres`.
- `funerary_ruins_tileset.png` — misma clase. Cubierto por Raou para el piso/muro
  base de la Torre.
- `wandering_undead_sheet.png` / `bound_spirit_sheet.png` — re-extracción
  **diferida** (no bloquea Torre; los enemigos actuales no tienen bug de mapeo).
  El halo gris de `EspirituAtado` es defecto de extracción preexistente.
