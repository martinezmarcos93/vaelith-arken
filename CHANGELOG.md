# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Este proyecto todavía no tiene versiones publicadas (pre-v0.1, vertical slice
en desarrollo). Ver progreso por etapa en [`docs/Roadmap.md`](docs/Roadmap.md).

## [Unreleased]

### Added — Enemigos regulares con IA real (Etapa 5, sandbox validado)
- `scripts/enemies/enemy_regular.gd`: máquina de estados compartida
  Idle→Alerta→Ataque→Vulnerable→Idle (tal como especifica
  `diseno_enemigos.md`), un solo script con toda la diferencia entre
  "No-muerto errante" y "Espíritu atado" resuelta por `@export` (patrulla en
  tierra vs. vaivén flotante + lunge), sin duplicar código.
- `scenes/enemies/NoMuertoErrante.tscn` / `EspirituAtado.tscn`: placeholder
  de arte temporal (Necromancer CC0-compatible y Ghost gratis, ya
  catalogados en `CREDITS.md`), igual criterio que el placeholder del
  jugador — validar la IA sin esperar arte final.
- **Bug real encontrado y corregido por testing headless:** todos los
  Hurtbox compartían la misma capa de colisión, así que un enemigo podía
  golpear a otro enemigo o al `TrainingDummy` por accidente (fuego amigo).
  Se separó en dos capas (jugador vs. bando enemigo) en `Player.tscn`,
  `TrainingDummy.tscn` y los dos enemigos nuevos.
- **Segundo hallazgo (documentado, no bug):** si `attack_range` es menor que
  la distancia física mínima alcanzable (otro cuerpo sólido en el camino),
  `move_and_slide()` frena al enemigo antes de que la distancia lógica
  dispare el ataque — se queda "pegado" sin atacar nunca. Anotado como
  comentario en `enemy_regular.gd` para la próxima vez que se ajusten estos
  valores en Level 1 real.

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
- Cámara con position smoothing, lookahead en la dirección de movimiento
  (calculado en `player.gd`, reutilizable entre niveles) y límites de nivel
  configurados por escena (override del `Camera2D` en cada `.tscn` de nivel).
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

### Added — Vida, daño y muerte (Etapa 1.4, sandbox validado)
- Vida, daño, i-frames (0.4s) e integración con bloqueo/postura ya existían
  desde el combate base (Etapa 1.3).
- Estado `DEAD` para el jugador: al llegar a 0 HP, la máquina de estados
  queda trabada (sin timer de reversión, a diferencia de `HURT`/`STAGGERED`)
  e ignora golpes posteriores. Corrige un bug real encontrado por testing
  headless: `_die()` solo imprimía un mensaje y dejaba `state=HURT`, que
  vencía por tiempo y volvía a `FREE` sin importar la vida — un "cadáver"
  con 0 HP seguía moviéndose y peleando.
- La penitencia/respawn real (Pharasma devuelve al jugador, corrupción de
  nivel) sigue **fuera de alcance** hasta la Etapa 4, porque depende del
  sistema de checkpoints — hoy `DEAD` es un estado terminal sin respawn,
  suficiente para validar el criterio de aceptación de la Fase 1.5
  ("correr, saltar, golpear y morir sin bugs bloqueantes").

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

### Added — Integración de animación (Etapa 2.4, validada con placeholder)
- `AnimatedSprite2D` reemplaza el rectángulo de color (`Polygon2D`) en
  `Player.tscn`. `player.gd` ahora sincroniza la animación con la máquina
  de estados (`_update_sprite_animation`): idle/run/jump/fall según
  movimiento y suelo, attack1/attack2/hurt/dead según el estado de combate.
- **El sprite es temporal**: reutiliza el pack CC0 "Evil Wizard 2" (pensado
  como enemigo, ver `CREDITS.md`) solo para probar el cableado técnico
  (`AnimatedSprite2D` + `SpriteFrames` + estados) antes de invertir tiempo
  en el sprite sheet final de Vaelith. `shove` y `block` no tienen
  animación propia en el pack — reutilizan `attack2`/`idle` a propósito,
  no es un mapeo definitivo.
- `assets/sprites/player/_placeholder_evil_wizard2_frames.tres` — recurso
  `SpriteFrames` generado a partir de las hojas de sprites de
  `evil_wizard_2_CC0/` (8 animaciones, 46 frames en total).
- Validado headless: mismo test de combate de siempre, sin errores de
  carga de escena/recurso.

### Added — Infraestructura de repo
- `README.md`, `.gitattributes`, `.editorconfig`, `CREDITS.md`.
- Repo conectado a `github.com/martinezmarcos93/vaelith-arken`, rama única
  `main` (la rama de trabajo `feature/vertical-slice-demo` se mergeó y
  borró tras cerrar la Etapa 1).

### Pending — próximos pasos por etapa (ver `docs/Roadmap.md`)
- **Etapa 1: cerrada.** Movimiento, cámara, combate base y vida/muerte
  validados por testing headless (`scripts/test_driver.gd`); criterio de
  aceptación de la Fase 1.5 cumplido.
- **Etapa 4** (no antes): mecánica de "penitencia" real (respawn en
  checkpoint + corrupción de nivel), cuando exista el sistema de
  checkpoints — hoy `DEAD` es terminal, sin respawn.
- **Etapa 2**: sprite sheet final del protagonista (Fases 2.1-2.3). La
  integración técnica (Fase 2.4) ya está resuelta con un placeholder —
  falta el arte real de Vaelith para reemplazar el pack temporal.
- **Etapa 3**: intro jugable real (guion ya escrito en
  `docs/guion_intro.md`, sin implementar).
- **Etapa 4**: construcción real de Level 1 sobre el layout ya diseñado
  (`docs/layout_level1.md`), reemplazando el sandbox de pruebas.
- **Etapa 5**: IA (Fase 5.3) ya implementada y validada en el sandbox — falta
  balance con playtesting real (Fase 5.4) y arte final (Fase 5.2, mismo
  bloqueo narrativo/de tiempo que Vaelith).
- **Etapa 6**: diseño de patrones cerrado (`docs/diseno_boss1.md`, Fase 6.1).
  Faltan arte (6.2, bloqueada por compartir diseño con Vaelith), arena
  (6.3), IA en Godot (6.4) e integración narrativa completa (6.5).
- **Etapa 7**: desenlace de la demo.
- **Etapa 8**: audio (composición vía Suno, SFX final, integración).
- **Etapa 9**: HUD de vida ya implementado (Fase 9.1). Faltan menús (9.2) y
  sistema de diálogo (9.3).
- **Etapa 10-11**: QA, pulido, empaquetado.
