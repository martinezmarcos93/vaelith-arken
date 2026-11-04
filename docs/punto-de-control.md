# Punto de control

<!-- PUNTO-DE-CONTROL -->
**Tarea actual:** retomar Vaelith Arken tras el relevamiento visual del 2026-11-04
(`docs/RELEVAMIENTO_2026-11-04.md`).

**Próximo paso:** que Marcos elija qué arreglar primero. Propuesta: los tres
baratos (piso con 13 px transparentes, usar `walk` en vez de `run`, sacar
`BringerOfDeath1`), después definir la densidad de píxel única y recién ahí
sumar efectos con pixelfx.

**Bloqueos:** decisión sobre los personajes (re-extraer / redibujar / pack).

**Archivos en curso:** `CLAUDE.md` (excepción pixelfx + entorno Linux),
`docs/RELEVAMIENTO_2026-11-04.md`, `docs/relevamiento_2026-11-04/`. Sin commitear.

**Entorno:** Godot 4.7.2 Linux en `~/Aplicaciones/godot/`. Capturas sin ventana
de juego: `tools/relevamiento/` (`capturas.gd`, `captura_escena.gd`, y en Python `frames.py`, `recortes.py`, `coherencia.py`, `contact.py`) (cargar escena, mover al jugador, guardar
`root.get_texture().get_image()`).

**Preguntas abiertas:** ¿personajes con arte IA o pixel art real?
<!-- /PUNTO-DE-CONTROL -->
