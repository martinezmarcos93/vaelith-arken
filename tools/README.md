# tools/

Utilidades de desarrollo. **No forman parte del flujo del juego** (la main scene
es `res://scenes/ui/TitleScreen.tscn`).

| Archivo | Qué es |
|---|---|
| `Main.tscn` + `test_driver.gd` | Sandbox de la Etapa 1.5: un piso, dos plataformas, dummy y enemigos para probar movimiento/combate a mano o con el driver headless. |
| `level1_test_driver.gd` | Smoke test headless de `Level1.tscn` (corre a la derecha + salta) — confirma que nada explota (colisiones, hazard, checkpoints, respawn). No valida ritmo ni dificultad. |
| `Shot.tscn` + `shot.gd` | Captura una UI a PNG sin abrir el editor: `godot --path . --resolution 1280x720 tools/Shot.tscn -- dialogue` (o `pause`). Sale en `user://shot_<modo>.png`. Para diagnosticar layout de HUD/diálogo. |
| `extract_palette.py` | Extrae una paleta dominante de una imagen de referencia (`python tools/extract_palette.py <img> <n>`). Sólo necesita PIL. |
| `img_pipeline/` | Pipeline local y offline para **reparar y recolorear** imágenes a la paleta canónica (`recolor.py` sobre pyxelate, `fix_ai.py` sobre pixelfixer). Entorno propio en venv — ver `tools/img_pipeline/README.md`. Montado el 2026-09-09. |

Movidos acá el 2026-08-27 (Fase 1 de `docs/AUDITORIA_2026-08-27.md`) para sacarlos
de `scenes/` y `scripts/` sin perderlos.
