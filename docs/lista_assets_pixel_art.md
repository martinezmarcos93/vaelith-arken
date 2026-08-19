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

## 1. Protagonista — Vaelith Arken 🔴 Custom obligatorio
No hay alternativa: es el personaje central de la historia, con diseño y
animaciones que dependen de su lore específico (armadura, escudo con símbolo de
Pharasma, daga ceremonial). Ningún pack genérico de "knight" lo resuelve sin
quedar genérico.

- [ ] Idle
- [ ] Correr
- [ ] Salto (subida / apex / caída)
- [ ] Aterrizaje
- [ ] Ataque alto (espada larga)
- [ ] Ataque bajo (espada larga)
- [ ] Bloqueo / levantar escudo
- [ ] Embestida (Shove)
- [ ] Recibir daño
- [ ] Muerte / resurrección (animación única, ligada al lore de Returned)

**Referencia útil (no para usar directo, solo de estilo/proporción):**
[FREE - Knight 2D Pixel Art (Mattz Art)](https://xzany.itch.io/free-knight-2d-pixel-art)
— sirve para calibrar proporciones de armadura antes de dibujar el original.

---

## 2. Enemigos regulares 🟡 Placeholder viable → reskin recomendado

### No-muerto errante (melee lento)
- [ ] Idle/patrulla
- [ ] Caminar
- [ ] Anticipación de ataque
- [ ] Ataque
- [ ] Recibir daño / vulnerable
- [ ] Muerte

**Candidatos encontrados:**
- [Skeleton Warriors Pixel Art Monster Asset (sanctumpixel)](https://sanctumpixel.itch.io/skeleton-warriors-pixel-art-monster-asset)
- [2D Pixel Art Skeletal Warrior (Elthen's Pixel Art Shop)](https://elthen.itch.io/2d-pixel-art-skeletal-warrior)
- [Free Enemy Sprite Sheets Pixel Art](https://free-game-assets.itch.io/free-enemy-sprite-sheets-pixel-art)

### Espíritu atado (errático/aéreo)
- [ ] Idle/flotar
- [ ] Lunge (ataque)
- [ ] Recibir daño / vulnerable
- [ ] Muerte

**Candidatos encontrados:**
- ✅ [Pixel Art Ghost Sprite (OpenGameArt)](https://opengameart.org/content/pixel-art-ghost-sprite) — **integrado** en `assets/sprites/enemies/ghost_opengameart_CC-BY4.0/` (CC-BY 4.0).
- ✅ [Pixel Art - Simple Ghost and Skull Sprite sheet (Fatal)](https://fatalaigaming.itch.io/pixelghostskull) — **integrado** en `assets/sprites/enemies/ghost_skull_fatalaigaming_free/` (gratis, sin atribución).
- [Free Ghost Pixel Art Sprite Sheets (CraftPix)](https://craftpix.net/freebies/free-ghost-pixel-art-sprite-sheets/) — 3 fantasmas con movimiento, ataque, muerte, grito. Pendiente.

**Recomendación:** usar estos packs como placeholder para poblar Level 1 y
validar el diseño de comportamiento (Fase 5.1/5.3) ya mismo, sin esperar arte
final. Decidir el reskin recién cuando el resto de la paleta/estilo esté
asentado — puede que ni haga falta si el pack calza bien con la guía de estilo.

---

## 3. Boss 1 — Guerrero-espejo 🔴 Custom obligatorio
Igual que el protagonista: narrativamente **debe** parecerse visualmente a
Vaelith (comparte diseño de armadura/pose), así que no hay pack de terceros que
lo resuelva sin romper la premisa del personaje.

- [ ] Idle
- [ ] Caminar
- [ ] 2-3 patrones de ataque distintos (con anticipación clara)
- [ ] Transición de fase
- [ ] Aturdido / vulnerable
- [ ] Muerte / diálogo final (máscara cayendo, ver `guion_desenlace.md`)

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
| Protagonista | 🔴 Custom | Producción en LibreSprite desde cero |
| Boss 1 | 🔴 Custom | Producción en LibreSprite desde cero (comparte base con protagonista) |
| Enemigos regulares | 🟡 Placeholder | Bajar packs de esqueleto/fantasma ya, decidir reskin después |
| Tileset/entorno | 🟢 Pack | Bajar "Dungeon Tileset" (Golopin) + explorar tag Gothic de itch.io |
| Props narrativos | 🔴 Custom (parcial) | Solo puerta/checkpoint/fragmento; el resto sale del tileset |
| UI/HUD | 🟢 Pack (parcial) | Pack genérico + indicador de penitencia a medida |
| VFX | 🟢 Pack (parcial) | Pack genérico + telegrafiado de ataque y memoria a medida |
| Tipografía | 🟢 Pack | "Gothic Pixels" de Akezhar |

**Con esto, el trabajo de pixel art 100% original queda acotado a:** Vaelith,
Boss 1, y 4-5 props/VFX narrativos puntuales — todo lo demás puede arrancar
como pack de terceros y evaluarse después si necesita reskin.
