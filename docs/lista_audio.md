# Lista de Audio (Música y SFX)

Checklist completo cruzado contra `GDD.md`, `guion_intro.md`, `layout_level1.md`,
`diseno_enemigos.md` y `guion_desenlace.md`.

**Leyenda de estado:** igual criterio que `lista_assets_pixel_art.md`
(🔴 Custom obligatorio / 🟡 Placeholder con pack existente / 🟢 Pack existente
resuelve directo).

---

## 1. Música 🔴 Custom obligatorio (vía Suno, plan original)

- [ ] Tema de intro (contemplativo/misterioso)
- [ ] Tema de exploración de Level 1
- [ ] Tema de combate (enemigos regulares)
- [ ] Tema de combate del Boss 1 (con variante de intensidad para transición de fase)
- [ ] Tema del desenlace / gancho final

**Por qué no conviene un pack genérico acá:** la identidad musical del proyecto
(capa coral/sagrada vs. capa de drone/distorsión corrupta, mezcladas dinámicamente
según el nivel de "penitencia") es un pilar de diseño propio — un track suelto de
un pack no puede tener esa lógica de capas. Mantener el plan original: Suno.

**Alternativa de referencia (NO para producción, solo para calibrar tono/mood
al escribir los prompts de Suno):**
- Tag de exploración: [Dark + Music, gratis, itch.io](https://itch.io/game-assets/free/tag-dark/tag-music)
- [(Free) Dark Dungeon Ambient Music Vol. 2 — 13 tracks (juanjo_sound)](https://itch.io/game-assets/free/tag-ambient/tag-horror) (buscar por nombre en itch.io)

---

## 2. SFX de personaje 🟢 Pack existente viable (mayoría genérica)

- [ ] Pasos (piedra)
- [ ] Salto
- [ ] Aterrizaje
- [ ] Ataque alto (swing espada)
- [ ] Ataque bajo (swing espada)
- [ ] Impacto de espada en enemigo
- [ ] Impacto de espada en escudo/bloqueo
- [ ] Embestida (Shove)
- [ ] Recibir daño
- [ ] Muerte / resurrección 🔴 (custom — es un momento narrativo único, no un
      SFX de daño genérico; ver `guion_desenlace.md` para el tono)

**Candidatos encontrados:**
- [Free Fantasy 200 SFX Pack (TomMusic)](https://tommusic.itch.io/free-fantasy-200-sfx-pack) — +20 SFX de espada/arco, +50 de pasos en distintos terrenos (incluye piedra), royalty-free, uso comercial permitido.
- [Sword Combat Sound Effects Pack Free Version (Hove Audio)](https://hoveaudio.itch.io/sword-combat-sound-effects-pack-free-version) — slashes, estocadas, colisiones, whooshes.
- [Footsteps Sounds (The Sound Guild)](https://the-sound-guild.itch.io/footsteps-sounds) — 107 sonidos, incluye piedra.
- [[SFX] Footstep Foley Sound Effect Pack (JDSherbert)](https://jdsherbert.itch.io/footstep-foley-sfx-pack)
- [Swords & Blades Sound Pack](https://thesoundrack.itch.io/swords-blades-sound-pack) — pay-what-you-want.

**Recomendación:** "Free Fantasy 200 SFX Pack" solo resuelve la mayoría de esta
categoría (pasos + espada) en un único pack.

---

## 3. SFX de enemigos 🟢 Pack existente viable

### No-muerto errante
- [ ] Paso / arrastre
- [ ] Gruñido / detección
- [ ] Swing de ataque
- [ ] Impacto
- [ ] Muerte

### Espíritu atado
- [ ] Flotar / drone ambiental
- [ ] Lunge
- [ ] Impacto
- [ ] Muerte / grito

**Candidatos encontrados:**
- [Free Ghost Pixel Art Sprite Sheets (CraftPix)](https://craftpix.net/freebies/free-ghost-pixel-art-sprite-sheets/) trae referencia de animación de "scream" — buscar el pack de audio equivalente del mismo autor/CraftPix.
- Complementar con "Free Fantasy 200 SFX Pack" (ya listado arriba) para golpes/impactos genéricos.
- Buscar puntualmente en itch.io tag "monster" + "sound effects" para gruñidos.

### Boss 1 (guerrero-espejo) 🔴 Custom parcial
- [ ] Líneas de diálogo (si se graban/generan) — ligadas al guion ya escrito
      ("Todavía hacés eso" / "Nunca aprendiste a terminar la finta")
- [ ] Grito de transición de fase
- [ ] Ataques especiales — pueden reusar SFX de espada genéricos del punto 2,
      no hace falta un set 100% nuevo.

---

## 4. SFX ambientales 🟢 Pack existente viable

- [ ] Viento
- [ ] Eco de cueva / cripta
- [ ] Goteo de agua
- [ ] Crujido de piedra
- [ ] Campana lejana (mencionada explícitamente en el prólogo original,
      "Despertar en la oscuridad") 🟡 — buscar puntual, es un detalle
      narrativo con peso, conviene elegir con cuidado el timbre exacto.
- [ ] Ambiente general de nivel (loop de fondo)

**Candidatos encontrados:**
- [EMPTY THRESHOLDS VOL. 1 — Dark Ambient & Drone, gratis](https://itch.io/game-assets/free/tag-ambience/tag-horror) (buscar por nombre en itch.io)
- [Horror Ambiences Sound Effects Pack Free Version (Hove Audio)](https://itch.io/game-assets/free/tag-ambient/tag-horror)
- [Fantasy Dungeon Audio Pack – 5 Music Loops & 50 SFX (con muestras gratis)](https://itch.io/blog/976158/fantasy-dungeon-audio-pack-5-music-loops-50-sfx-for-rpgs-wav-mp3-unityunreal-free-samples)

---

## 5. SFX de UI 🟢 Pack existente viable

- [ ] Selección de menú
- [ ] Confirmar
- [ ] Pausa
- [ ] Fragmento de memoria obtenido (jingle corto) 🔴 (custom — momento
      narrativo, no un "pickup sound" genérico)
- [ ] Daño en HUD (feedback de vida)

La mayoría de los packs de SFX genéricos (incluidos los ya listados arriba)
suelen traer un set básico de UI — no hace falta una búsqueda dedicada extra
salvo que ninguno alcance.

---

## Resumen ejecutivo

| Categoría | Estado | Acción sugerida |
|---|---|---|
| Música | 🔴 Custom | Mantener plan original: Suno, con capas sagrado/corrupto |
| SFX personaje (genéricos) | 🟢 Pack | "Free Fantasy 200 SFX Pack" (TomMusic) resuelve la mayoría |
| SFX personaje (muerte/resurrección) | 🔴 Custom | Encargar aparte, es momento narrativo único |
| SFX enemigos | 🟢 Pack | Complementar con pack de ghost SFX + pack genérico de golpes |
| SFX boss (diálogo) | 🔴 Custom | Depende del guion ya escrito |
| SFX ambientales | 🟢 Pack | "Fantasy Dungeon Audio Pack" o "Horror Ambiences" cubren la mayoría |
| Campana lejana (detalle narrativo) | 🟡 Curado a mano | Elegir con cuidado entre varios candidatos, no el primero que aparezca |
| SFX de UI | 🟢 Pack | Sale de los mismos packs generales |
| Jingle de fragmento de memoria | 🔴 Custom | Encargar aparte, es narrativo |

**Con esto, el audio 100% custom queda acotado a:** toda la música (vía Suno),
la animación sonora de muerte/resurrección, el diálogo del Boss 1, y el jingle
de fragmento de memoria — el resto (pasos, espada, ambiente, UI genérica) puede
resolverse hoy mismo con los packs listados arriba.
