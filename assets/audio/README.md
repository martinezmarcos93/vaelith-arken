# assets/audio/

Ver `docs/lista_audio.md` para el mapa completo (qué SFX dispara en qué señal,
prompts de Suno, integración pendiente).

## music/

Temas generados con Suno a partir de los prompts de `docs/lista_audio.md`.
**Cada tema tiene 2 versiones** (`x.mp3` y `x_b.mp3`) — hay que elegir la
definitiva por tema y borrar la otra:

| Tema | Archivos | Keeper |
|---|---|---|
| Intro — "El despertar" | `intro.mp3` / `intro_b.mp3` | ⬜ por decidir |
| Level 1 — "Las ruinas" | `level1.mp3` / `level1_b.mp3` | ⬜ por decidir |
| Boss — "El Espejo" | `boss.mp3` / `boss_b.mp3` | ⬜ por decidir |

Pendiente: variante de combate de Level 1 y stinger/2 fases del boss (generar
aparte, ver `lista_audio.md` §1). `gothicvania_village_loop_CC-BY/` es un
placeholder viejo, superado por estos.

## sfx/

Selección **curada** de 3 packs gratuitos de itch.io (no los packs completos).
Nombres por función, no por el original. Licencias y atribución en `CREDITS.md`.

- `player/` — pasos (Stone Chain = armadura pesada), salto, caída, whoosh,
  gruñidos de esfuerzo y de daño.
- `combat/` — swings, impactos (carne / gore), bloqueos, parry, choque de
  hojas, ring de telegrafiado.
- `world/` — puertas/rejas/cerrojo (cripta, `RecognitionPoint`), impactos de
  piedra (mecanismos).
- `ambient/` — loops: cueva, antorcha, arroyo; drone de "presencia" (dry, para
  agregarle reverb).

Falta (no está en los packs, ver `lista_audio.md`): **viento** para el arranque
de la Intro, y todos los SFX 🔴 custom (muerte/resurrección de Vaelith, máscara
del boss, jingle de memoria, sting de reconocimiento, etc.).
