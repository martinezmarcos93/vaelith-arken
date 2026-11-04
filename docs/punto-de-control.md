# Punto de control

<!-- PUNTO-DE-CONTROL -->
**Tarea actual:** coherencia visual terminada en la rama `fix/coherencia-visual`
(commits sobre `main`, sin push). Detalle: `CHANGELOG.md` 2026-11-04 y
`docs/RELEVAMIENTO_2026-11-04.md` § "Estado tras los arreglos".

**Próximo paso:** que Marcos juegue la demo con ventana y diga si el resultado
le cierra; si sí, merge a `main` (es cambio visible → PR o merge con su OK).

**Bloqueos:** ninguno.

**Herramientas nuevas:**
- `tools/sprite_pipeline/`: `extraer_poses.py` + un `.json` por personaje
  (re-extraer de la lámina), `armar_frames.py` (SpriteFrames),
  `hornear_escalas.py` (escala → textura), `hoja_a_frames.py` y
  `fuego_animado.py` (hojas de pixelfx → AnimatedSprite2D), `pinches.py`.
- `tools/img_pipeline/mapa_degradado.py`: recolor que conserva luces/sombras.
- `tools/relevamiento/`: capturas sin ventana, `props_flotantes.gd`,
  `apoyar_props.py`, `cruzar_level1.gd` (cruce automático), medidores Python.

**Entorno:** Godot 4.7.2 Linux en `~/Aplicaciones/godot/`. pixelfx clonado
fuera del repo (se re-renderiza con el comando del commit `feat(fx)`).

**Preguntas abiertas:** ¿el Zombi entra en algún nivel o se archiva? ¿Sumar
más efectos de pixelfx (chispa de golpe en enemigos = P1 de la auditoría)?
<!-- /PUNTO-DE-CONTROL -->
