# Vaelith Arken (título de trabajo)

Plataformas de acción 2D en pixel art, dificultad alta e intencional —
referencias directas de diseño: **SLAIN** y **Volgarr the Viking**.

Un caballero sin memoria que fue el villano que ahora caza, atravesando un
reino corrompido por su propio antiguo imperio de no-muertos.

## Estado actual

Vertical slice en desarrollo: intro jugable → Level 1 → Boss 1 → desenlace.
Ver progreso detallado en [`CHANGELOG.md`](CHANGELOG.md) y hoja de ruta completa
en [`docs/Roadmap.md`](docs/Roadmap.md).

## Requisitos

- [Godot Engine 4.7.x](https://godotengine.org/) (versión portátil, sin instalación).
- [LibreSprite](https://libresprite.github.io/) o Aseprite, para pixel art.
- Blender (opcional, solo para props 3D→sprite de la Etapa 4.2).

## Cómo abrir el proyecto

1. Abrir Godot.
2. **Import** → seleccionar `project.godot` en la raíz de este repo.
3. F5 para correr la escena principal (sandbox de pruebas de movimiento).

## Controles (borrador, ver `docs/GDD.md` sección 5)

| Acción | Tecla |
|---|---|
| Moverse | A/D o flechas |
| Saltar | Espacio |
| Ataque alto | J |
| Ataque bajo | K |
| Bloquear | L |
| Interactuar | E |

## Estructura del repositorio

```
project.godot        Configuracion del proyecto Godot
scenes/               Escenas (.tscn): player/, enemies/, levels/, ui/
scripts/              GDScript
assets/
  sprites/             player/, enemies/, tilesets/, ui/
  vfx/                 Efectos particulados
  audio/               music/, sfx/
  fonts/
tools/                 Scripts auxiliares de desarrollo (no forman parte del juego)
docs/                  Documentos de diseño (GDD, guiones, roadmap, listas de assets)
CREDITS.md             Licencias y atribucion de assets de terceros
```

## Documentación de diseño

- [`docs/GDD.md`](docs/GDD.md) — pitch, pilares, alcance, controles.
- [`docs/Roadmap.md`](docs/Roadmap.md) — etapas y fases del desarrollo.
- [`docs/guia_estilo_visual.md`](docs/guia_estilo_visual.md) — paleta y reglas de arte.
- [`docs/stats_personaje.md`](docs/stats_personaje.md) — valores jugables (movimiento, combate).
- [`docs/lista_assets_pixel_art.md`](docs/lista_assets_pixel_art.md) y [`docs/lista_audio.md`](docs/lista_audio.md) — checklist de todo el arte/audio necesario, con candidatos de assets de terceros ya investigados.

## Licencia

Sin licencia pública definida todavía — código y assets originales bajo todos
los derechos reservados por defecto. Los assets de terceros usados como
placeholder están documentados con su propia licencia en `CREDITS.md`.

## Créditos

Ver [`CREDITS.md`](CREDITS.md) para atribución de assets de terceros.
