# Lista de Assets de Pixel Art

Checklist completo de todo lo que necesita la demo (intro + Level 1 + Boss 1 +
desenlace), cruzado contra `GDD.md`, `guia_estilo_visual.md`, `layout_level1.md`,
`diseno_enemigos.md` y `stats_personaje.md`.

**Leyenda de estado:**
- 🔴 **Custom obligatorio** — no existe pack que lo resuelva (es específico del
  lore/personaje) o el resultado de usar un pack de terceros rompería la
  identidad del juego.
- 🟡 **Placeholder con pack existente** — usar un asset de terceros para poder
  seguir armando el nivel/prototipo ya, con plan de reemplazo/reskin más
  adelante si hace falta.
- 🟢 **Pack existente resuelve directo** — categorías genéricas donde un asset
  pack de terceros alcanza para producción final, sin necesidad de reskin.

Todos los packs listados abajo son **candidatos encontrados por búsqueda web**,
no confirmados: falta que vos los revises (estilo, licencia exacta, si pide
atribución) antes de bajarlos.

---

## 1. Protagonista — Vaelith Arken 🟡 Custom con IA, integrado 2026-08-27
Ya no es un hueco sin cubrir: Marcos generó una hoja de referencia con IA
(`Sprites/Vaelith.png`) con animaciones etiquetadas, extraídas e integradas
en `assets/sprites/player/vaelith_custom/` (ver CREDITS.md para el detalle
técnico completo). Sigue siendo candidato a reemplazo por arte 100% original
en LibreSprite más adelante si Marcos lo decide — no se cierra la puerta,
pero deja de ser un bloqueante.

- [x] Idle — 4 frames
- [x] Correr — 8 frames
- [ ] Salto (subida / apex / caída) — reutiliza los frames de correr, no
      extraído todavía de la hoja (sí existe ahí: fila "SALTO (5)")
- [ ] Aterrizaje — no extraído (existe en la hoja: fila "ATERRIZAJE (4)")
- [x] Ataque alto (espada larga) — 5 frames
- [ ] Ataque bajo (espada larga) — reutiliza el ataque alto, no extraído
      todavía (existe en la hoja: fila "ATAQUE BAJO (8)")
- [ ] Bloqueo / levantar escudo — sin animación propia en `player.gd`
      (no aplica extraer todavía)
- [ ] Embestida (Shove) — ídem, sin animación propia en el código
- [ ] Recibir daño — reutiliza idle, no extraído todavía (existe en la
      hoja: fila "RECIBIR DAÑO (4)")
- [x] Muerte — 6 frames (resurrección no extraída, existe en la hoja)

**Referencia útil (no para usar directo, solo de estilo/proporción):**
[FREE - Knight 2D Pixel Art (Mattz Art)](https://xzany.itch.io/free-knight-2d-pixel-art)
— sirve para calibrar proporciones de armadura antes de dibujar el original.

---

## 2. Enemigos regulares 🟡 Placeholder viable → reskin recomendado

### No-muerto errante (melee lento) 🟡 Custom con IA, integrado 2026-08-27
- [x] Idle/patrulla — 7 frames
- [x] Caminar — 9 frames
- [ ] Anticipación de ataque — sin uso separado (`enemy_regular.gd` no tiene
      estado propio de telegraph, usa `attack_windup` sobre la misma anim)
- [x] Ataque — 6 frames
- [x] Vulnerable (post-ataque) — 7 frames
- [x] Muerte — 7 frames

Reemplaza a Skeleton Warrior (CraftPix, integrado ayer 2026-08-26). Fuente:
`Sprites/No muerto errante.png` (arte con IA de Marcos). Ver CREDITS.md.

**Candidatos previos (ya no en uso, quedan documentados por si se reconsidera):**
- ✅ [Free Skeleton Pixel Art Sprite Sheets (CraftPix)](https://craftpix.net/freebies/free-skeleton-pixel-art-sprite-sheets/) — integrado 2026-08-26, reemplazado 2026-08-27.
- [Skeleton Warriors Pixel Art Monster Asset (sanctumpixel)](https://sanctumpixel.itch.io/skeleton-warriors-pixel-art-monster-asset)
- [2D Pixel Art Skeletal Warrior (Elthen's Pixel Art Shop)](https://elthen.itch.io/2d-pixel-art-skeletal-warrior)
- [Free Enemy Sprite Sheets Pixel Art](https://free-game-assets.itch.io/free-enemy-sprite-sheets-pixel-art)

### Espíritu atado (errático/aéreo) 🟡 Custom con IA, integrado 2026-08-27
- [x] Idle/flotar — 8 frames
- [x] Lunge (ataque) — 6 frames
- [x] Vulnerable — 4 frames
- [x] Muerte — 4 frames

Reemplaza a Ghost+Skull (Fatal AI Gaming). Fuente: `Sprites/espiritu
atado.png`. Extracción menos precisa que los otros 3 personajes (silueta de
humo, los frames se tocan entre sí — ver nota técnica en CREDITS.md). Sin
animación de "recibir daño / movimiento" separada — reutiliza idle.

**Candidatos previos (ya no en uso):**
- ✅ [Pixel Art Ghost Sprite (OpenGameArt)](https://opengameart.org/content/pixel-art-ghost-sprite) — integrado, reemplazado 2026-08-27.
- ✅ [Pixel Art - Simple Ghost and Skull Sprite sheet (Fatal)](https://fatalaigaming.itch.io/pixelghostskull) — integrado, reemplazado 2026-08-27.
- [Free Ghost Pixel Art Sprite Sheets (CraftPix)](https://craftpix.net/freebies/free-ghost-pixel-art-sprite-sheets/) — 3 fantasmas con movimiento, ataque, muerte, grito. Pendiente.

---

## 3. Boss 1 — Guerrero-espejo 🟡 Custom con IA, integrado 2026-08-27
Igual que el protagonista, ya no es un hueco sin cubrir. Fuente:
`Sprites/Espejo.png` (arte con IA de Marcos, mismo diseño de armadura que
Vaelith en violeta en vez de rojo, cumple la premisa narrativa de "reflejo").
Reemplaza el placeholder de Evil Wizard 2 en `Boss1.tscn`. Ver CREDITS.md.

- [x] Idle — 4 frames
- [x] Caminar — 7 frames
- [ ] 2-3 patrones de ataque distintos — solo 1 patrón por ahora: `attack1`
      y `attack2` usan el mismo set de 6 frames (la hoja no separaba
      claramente "ataque alto" de "ataque bajo")
- [ ] Transición de fase — sin animación dedicada (el código ya maneja la
      transición de fase por lógica/telegraphs, no por sprite)
- [x] Aturdido / vulnerable — `hurt`, 4 frames (existe además una fila
      "ATURDIDO" en la hoja original sin extraer todavía)
- [ ] Muerte / diálogo final — no aplica: el Boss 1 se RINDE, no muere
      (`boss1.gd` ya lo maneja con tinte gris sobre `idle`, ver
      `vaelith_arken_demo_plan` en memoria)

---

## 4. Tileset y entorno (Level 1 — ruinas/cripta/cementerio) 🟢 Pack existente viable

- [ ] Piso / plataformas base
- [ ] Paredes / columnas
- [ ] Escaleras / desniveles
- [ ] Piso agrietado (hazard del Tramo C, ver `layout_level1.md`)
- [ ] Fondo lejano (parallax capa 1)
- [ ] Fondo medio (parallax capa 2)
- [ ] Decoración: lápidas, árboles muertos, huesos, niebla

**Candidatos encontrados:**
- ✅ [Dungeon Tileset (Golopin) — gratis](https://golopin.itch.io/dungeon-tileset) — **integrado** en `assets/sprites/tilesets/dungeon_golopin_free/` (81 piezas individuales + hoja compacta). Pendiente recolorear a la paleta propia en LibreSprite antes de usar en producción.
- ✅ [Free Dungeon Platformer Pixel Art Tileset (CraftPix)](https://craftpix.net/freebies/free-dungeon-platformer-pixel-art-tileset/) — **integrado y recoloreado** en `assets/sprites/tilesets/dungeon_platformer_craftpix_free/` (2026-08-26, recoloreo automático por script contra la paleta de `guia_estilo_visual.md`), reemplaza el `ColorRect` plano de las plataformas normales de `Level1.tscn`. Ver CREDITS.md.
- ✅ [Free Pixel Art Fantasy 2D Battlegrounds (CraftPix)](https://craftpix.net/freebies/free-pixel-art-fantasy-2d-battlegrounds/) — **integrado** (Battleground1/Pale) como fondo de parallax (`Fondo lejano`/`Fondo medio`, ítems de este checklist) en `Level1.tscn`. Cementerio con lápidas, ya en tonos teal/verde compatibles, sin recoloreo. Ver CREDITS.md.
- [Gothicvania Cold Corridors — gratis](https://itch.io/game-assets/free/tag-gothic/tag-pixel-art) (buscar en el tag Gothic+Pixel Art de itch.io)
- Tag general para seguir explorando: [Gothic + Pixel Art + Tileset, gratis](https://itch.io/game-assets/free/tag-gothic/tag-pixel-art/tag-tileset)
- Opción paga de calidad superior si el gratuito no alcanza: [Candle Cathedral - 16x16 Gothic Dungeon Tileset ($7.99)](https://itch.io/game-assets/tag-gothic/tag-pixel-art) (buscar por nombre en itch.io)

**Recomendación:** fuerte candidato a resolverse 100% con pack de terceros —
la paleta de `guia_estilo_visual.md` puede recolorearse sobre estos tilesets en
LibreSprite si no calzan exacto.

---

## 5. Props / interactuables 🟡 Mixto

- [ ] Puerta con símbolo de la cripta 🔴 (custom — es plot-relevant, lleva
      el símbolo específico de Pharasma)
- [ ] Checkpoint (icono/altar) 🔴 (custom — parte de la identidad visual del
      sistema de "penitencia")
- [ ] Fragmento de memoria (pickup, Tramo E) 🔴 (custom — asset narrativo único)
- [ ] Antorchas / fuentes de luz 🟢 (puede resolverse con pack de tileset gótico,
      la mayoría los incluye)
- [ ] Escombros / columnas rotas decorativas 🟢 (idem, viene con el tileset)

---

## 6. UI / HUD 🟢 Pack existente viable (con posible retoque de color)

- [ ] Barra de vida
- [ ] Indicador de "penitencia"/corrupción de nivel 🔴 (custom — mecánica
      propia del juego, ningún pack la va a tener conceptualmente)
- [ ] Marco de diálogo
- [ ] Menú principal
- [ ] Menú de pausa
- [ ] Cursor / selector de menú

**Candidatos encontrados:**
- Tag para explorar: [Dark Fantasy + User Interface, itch.io](https://itch.io/game-assets/tag-dark-fantasy/tag-user-interface)
- [Dark Fantasy Pixel Art World – Tiles, Props & UI (16-bit) — Marco Brito](https://marcomyly.itch.io/dark-fantasy-pixel-art-world-tiles-props-ui-16-bit) (incluye HUD básico)
- Buscar específicamente "Skull UI" y "Gothic pixelated GUI" en itch.io — aparecieron como packs orientados exactamente a este tono (dark fantasy / soulslike).

**Recomendación:** usar un pack de HUD genérico y solo diseñar a medida el
indicador de corrupción/penitencia, que es mecánicamente único del juego.

---

## 7. Efectos especiales (VFX) 🟢 Pack existente viable

- [ ] Impacto de espada en enemigo
- [ ] Chispa de bloqueo (parry/escudo)
- [ ] Polvo al aterrizar / correr
- [ ] Niebla / ceniza ambiental
- [ ] Brillo de telegrafiado de ataque (rojo `#B41F1C`, ver guía de estilo) 🔴
      (custom — el color y timing exactos son parte del lenguaje de "lectura
      justa" del combate, mejor no depender de un asset genérico acá)
- [ ] Destello de fragmento de memoria (violeta `#766DBC`) 🔴 (custom, narrativo)

**Candidatos encontrados:**
- [VFX - SPARKS - Pixel Art Effects (kiddolink)](https://kiddolink.itch.io/vfx-fx-sparks-pixel-art)
- Tag para explorar más: [particle-effects, itch.io](https://itch.io/game-assets/tag-particle-effects) / [Pixel Art + vfx](https://itch.io/game-assets/tag-pixel-art/tag-vfx)

---

## 8. Tipografía 🟢 Pack existente viable

- [ ] Fuente principal de diálogo/UI

**Candidatos encontrados:**
- [Gothic Pixels (Akezhar) — gratis, uso comercial permitido](https://akezhar.itch.io/gothic-pixels)
- [Gothic Pixel Font (dacosta) — pay-what-you-want](https://dacosta.itch.io/gothic-pixel-font/purchase)
- [Gothic Pixelart Font (osadam) — pay-what-you-want](https://osadam.itch.io/gothic-pixelart-font/purchase)

**Recomendación:** "Gothic Pixels" de Akezhar es el candidato más directo —
gratis y con uso comercial explícito. Verificar legibilidad en el tamaño real
del HUD antes de confirmar.

---

## Resumen ejecutivo

| Categoría | Estado | Acción sugerida |
|---|---|---|
| Protagonista | 🟡 Custom con IA (2026-08-27) | Integrado y jugable; falta confirmación visual real y completar salto/aterrizaje/ataque bajo/recibir daño/resurrección |
| Boss 1 | 🟡 Custom con IA (2026-08-27) | Integrado y jugable; ataque alto y bajo comparten el mismo set de frames por ahora |
| Enemigos regulares | 🟡 Custom con IA (2026-08-27) | Ambos integrados; Espíritu atado con extracción menos prolija (silueta de humo) |
| Tileset/entorno | 🟢 Pack + fondo custom | Tileset recoloreado (CraftPix) ya aplicado a las plataformas; fondo de parallax reemplazado por el custom de `Sprites/` |
| Props narrativos | 🟡 Parcial custom con IA | Checkpoint y Fragmento de memoria integrados; puerta de la cripta como decoración de fondo sin lógica real; piso agrietado e indicador de penitencia sin integrar |
| UI/HUD | 🟢 Pack (parcial) | Pack genérico + indicador de penitencia a medida (arte ya existe en `Sprites/Penitencia corrupcion.png`, falta el sistema en código) |
| VFX | 🟢 Pack (parcial) | Pack genérico + telegrafiado de ataque y memoria a medida |
| Tipografía | 🟢 Pack | "Gothic Pixels" de Akezhar |

**Estado actual (2026-08-27):** los 4 personajes principales y varios props
narrativos dejaron de ser huecos de arte gracias a hojas de referencia
generadas con IA por Marcos — quedan integrados y jugables, pero con
recorte de alcance real (ver detalle por personaje arriba y en CREDITS.md).
Sigue abierta la decisión de si esto es el arte final o un paso intermedio
antes de producción 100% original en LibreSprite.
