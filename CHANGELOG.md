# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Este proyecto todavía no tiene versiones publicadas (pre-v0.1, vertical slice
en desarrollo). Ver progreso por etapa en [`docs/Roadmap.md`](docs/Roadmap.md).

## [Unreleased]

### Added — Preproducción (Etapa 0, completa)
- Estructura base del proyecto Godot 4.7 (`project.godot`, carpetas de
  scenes/scripts/assets/docs/tools).
- GDD, guía de estilo visual (paleta extraída algorítmicamente de la
  referencia estética), stats jugables traducidos de la ficha de
  Pathfinder 2e, guion de intro, layout de Level 1, diseño de enemigos
  regulares, borrador de desenlace.

### Added — Movimiento y cámara (Etapa 1.1/1.2, completa)
- Movimiento base del jugador (`scripts/player.gd`): control aéreo mínimo,
  coyote time, sin doble salto ni dash — pilar de diseño "salto comprometido".
- Cámara con position smoothing siguiendo al jugador.
- Input map configurado por código (`scripts/input_setup.gd`, autoload):
  mover, saltar, atacar alto/bajo, bloquear, embestida, interactuar.
- Escena sandbox de pruebas de física (`scenes/levels/Main.tscn`).

### Added — Combate base (Etapa 1.3, completa)
- Hitbox/Hurtbox reutilizables (`scripts/combat/`) para jugador, enemigos y
  boss futuros.
- Ataque alto (daño 2) y bajo (daño 1) con ventanas de daño precisas, sin
  knockback por decisión de diseño validada por testing.
- Bloqueo con degradación de postura: rompe al 4to golpe consecutivo
  (umbral configurable), entra en Staggered vulnerable 0.8s.
- Embestida: sin daño, knockback 300, aturde al objetivo 0.6s.
- I-frames de 0.4s tras recibir daño.
- Muñeco de entrenamiento (`TrainingDummy`) en el sandbox: recibe golpes y
  contraataca cada 2s para poder validar también el bloqueo.
- Driver de pruebas headless (`scripts/test_driver.gd`) que simula input
  real (`Input.action_press/release`) y ejercita todo el combate de punta
  a punta sin necesitar un humano jugando — corre con
  `Godot --headless --quit-after N` y se lee por consola.
- **2 bugs reales encontrados y corregidos por el testing headless:**
  1. `Area2D.monitoring` no vuelve a emitir `area_entered` para
     superposiciones ya existentes al reactivarse — un ataque repetido
     contra un objetivo pegado al cuerpo nunca conectaba.
     `Hitbox.activate()` ahora revisa `get_overlapping_areas()` manualmente.
  2. Input de un solo frame perdido si coincidía con estar en el aire
     (ej. por el knockback de un golpe recibido) — se agregó un buffer de
     input de 0.12s (`_poll_input_buffer`), consultado en todos los
     estados y consumido recién cuando el jugador puede procesarlo.

### Added — Assets de terceros (investigación + integración selectiva)
- Checklist completo de pixel art y audio con candidatos investigados
  (itch.io, OpenGameArt, CraftPix) — ver `docs/lista_assets_pixel_art.md`
  y `docs/lista_audio.md`.
- Integrados y con licencia **confirmada**: Ghost sprite (OpenGameArt,
  CC-BY 4.0), Ghost+Skull (Fatal AI Gaming, gratis), Dungeon Tileset
  (Golopin, royalty-free), Evil Wizard 1/2 (CC0), GothicVania Town +
  música de ambiente (Ansimuz, CC0 / atribución), Dungeon Tileset
  side-scroller (Raou, comercial permitido), Effect and Bullet 16x16
  (BDragon1727, donationware), Kenney 1-Bit Platformer (CC0, solo para
  greybox de nivel), Necromancer (CreativeKind, comercial permitido).
- Marcados como **licencia sin confirmar** (no usar en build final):
  Seamless patterns (fuente no identificada).
- Evaluados y descartados por no encajar con la estética o el género
  (top-down vs. side-scroller, paleta cálida de fuego, formato no
  importable): boss_demon_slime, Free-Undead-Tileset-Top-Down, FreeKnight_v1,
  texturas genéricas sin curar, desert enemy pack — detalle completo y
  razones en `CREDITS.md`.

### Added — Infraestructura de repo
- `README.md`, `.gitattributes`, `.editorconfig`, `CREDITS.md`.
- Repo conectado a `github.com/martinezmarcos93/vaelith-arken`, rama única
  `main` (la rama de trabajo `feature/vertical-slice-demo` se mergeó y
  borró tras cerrar la Etapa 1).

### Pending — próximos pasos por etapa (ver `docs/Roadmap.md`)
- **Etapa 1.4**: sistema de vida/muerte definitivo y mecánica de
  "penitencia" real (game over → respawn con corrupción de nivel). Hoy
  solo existe vida/daño/i-frames; morir imprime un mensaje, no respawnea.
- **Etapa 1.5**: consolidar el sandbox actual como prototipo formal
  (ya cumple la función informalmente).
- **Etapa 2**: arte y animación final del protagonista (hoy es un
  rectángulo de color placeholder).
- **Etapa 3**: intro jugable real (guion ya escrito en
  `docs/guion_intro.md`, sin implementar).
- **Etapa 4**: construcción real de Level 1 sobre el layout ya diseñado
  (`docs/layout_level1.md`), reemplazando el sandbox de pruebas.
- **Etapa 5**: enemigos regulares con IA real (hoy solo existe el dummy
  de pruebas, no enemigos jugables).
- **Etapa 6**: Boss 1 (diseño, arte, arena, IA, narrativa).
- **Etapa 7**: desenlace de la demo.
- **Etapa 8**: audio (composición vía Suno, SFX final, integración).
- **Etapa 9**: UI/UX (HUD, menús, diálogo).
- **Etapa 10-11**: QA, pulido, empaquetado.
