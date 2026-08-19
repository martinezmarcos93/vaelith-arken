# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Este proyecto todavía no tiene versiones publicadas (pre-v0.1, vertical slice
en desarrollo).

## [Unreleased]

### Added
- Estructura base del proyecto Godot 4.7 (`project.godot`, carpetas de
  scenes/scripts/assets/docs/tools).
- Movimiento base del jugador (`scripts/player.gd`): control aéreo mínimo,
  coyote time, sin doble salto ni dash — pilar de diseño "salto comprometido".
- Cámara con position smoothing siguiendo al jugador.
- Input map configurado por código (`scripts/input_setup.gd`, autoload).
- Escena sandbox de pruebas de física (`scenes/levels/Main.tscn`).
- Documentación de preproducción completa: GDD, guía de estilo visual (paleta
  extraída algorítmicamente de la referencia estética), stats jugables
  traducidos de la ficha de Pathfinder 2e, guion de intro, layout de Level 1,
  diseño de enemigos regulares, borrador de desenlace.
- Checklist de assets de pixel art y de audio con investigación de packs de
  terceros existentes (itch.io, OpenGameArt, CraftPix).
- Primer asset de terceros integrado: sprite de fantasma (OpenGameArt, CC-BY 4.0)
  como placeholder del enemigo "Espíritu atado".
- `CREDITS.md` para trackear licencias de assets externos.

### Pending
- Sistema de combate base (ataques, bloqueo, embestida, i-frames).
- Sistema de vida/muerte y mecánica de "penitencia".
- Arte final del protagonista y del Boss 1.
- Construcción real de Level 1 sobre el layout ya diseñado.
