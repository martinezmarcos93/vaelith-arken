# Punto de control

<!-- PUNTO-DE-CONTROL -->
- Tarea actual: pausa pedida por Marcos (25/11, noche). Roadmap nuevo en `docs/roadmap-slice.md`. Integra su lista, la revisión del video y la visión narrativa externa, y reemplaza el orden de `roadmap-afinado.md` desde su fase 3.
- Hecho hoy, después de la prueba de Marcos:
  - pausa con fondo negro y cursor (el cursor no se pudo verificar por captura);
  - "E o Enter" en la ayuda;
  - aviso LIGHTING NEEDS TO BE REBUILT arreglado de raíz (76 luces Movable, `r.AllowStaticLighting=False`, `tools/ue/luces_dinamicas.py`);
  - motion blur 0,1;
  - `tools/grabar_partida.sh` (graba con ffmpeg; el grabador de GNOME cierra el juego).
- Próximo paso: fase A del roadmap. Recalibrar el cielo y la exposición: con el cielo dinámico, el menú quedó plano y los árboles muertos casi blancos (captura del menú del 25/11). Después, legibilidad del bosque oscuro (-ir=9500,50500,1400,157,-5) y volver a medir FPS.
- Decidido por Marcos (25/11): tentación SÍ, como interactuable según el Ministro Dragón; frase eje del menú SÍ; pueblo con NPC en el slice SÍ (ver "Decisiones" en `roadmap-slice.md`).
- Tono de Pharasma v2 APROBADO. Se suman la fase A2 (cielo estrellado, luna, niebla de horizonte, pueblo a 250–300 m y transitable) y, en la fase F, el minimapa y la interfaz 100 % del motor.
- Fase R nueva: la planilla PF2e completa en el juego (`docs/planilla-en-juego.md`). R1 y R2 van antes de C y E; R3 y R4 con la UI.
- **Pausa: no implementar nada hasta que Marcos diga "empezamos".** El orden está en `roadmap-slice.md`.
- Ojo: durante las capturas, alguien pausó y cerró las ventanas del juego. No tocarlas mientras corren.
- Archivos en curso: `docs/roadmap-slice.md`, `docs/revision-video-2026-11-25.md`, `tools/ue/construir_nivel.py` (luces Movable y motion blur).
<!-- /PUNTO-DE-CONTROL -->
