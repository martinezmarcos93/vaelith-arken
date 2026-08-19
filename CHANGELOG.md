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

- Sistema de combate base (`scripts/combat/hitbox.gd`, `hurtbox.gd`):
  ataque alto/bajo con ventanas de daño precisas, bloqueo con degradación
  de postura (rompe al 4to golpe consecutivo), Embestida con knockback y
  aturdimiento, i-frames tras recibir daño.
  Componentes reutilizables para enemigos/boss futuros.
- Muñeco de entrenamiento (`scripts/combat/training_dummy.gd`) en el
  sandbox: recibe golpes del jugador y ataca cada 2s para poder probar
  también el bloqueo.
- Driver de pruebas headless (`scripts/test_driver.gd`) que simula input
  real para validar todo el combate sin necesitar un humano jugando.
- **Bugs reales encontrados y corregidos durante el testing headless:**
  1. `Area2D.monitoring` no vuelve a emitir `area_entered` para
     superposiciones ya existentes al reactivarse — un ataque repetido
     contra un objetivo pegado al cuerpo nunca conectaba.
     `Hitbox.activate()` ahora revisa `get_overlapping_areas()` manualmente.
  2. Input perdido: los inputs de combate solo se procesaban con el
     jugador en el suelo, pero `is_action_just_pressed()` solo es
     verdadero un unico frame — si ese frame coincidia con estar en el
     aire (ej. por el knockback de un golpe recibido), el input se
     perdia para siempre. Se agrego un buffer de input de 0.12s
     (`_poll_input_buffer`) que se consulta en todos los estados y se
     consume recien cuando el jugador puede procesarlo.

### Pending
- Sistema de vida/muerte definitivo y mecánica de "penitencia" (game over → respawn).
- Arte final del protagonista y del Boss 1.
- Construcción real de Level 1 sobre el layout ya diseñado.
