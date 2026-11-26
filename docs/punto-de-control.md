# Punto de control

<!-- PUNTO-DE-CONTROL -->
- Tarea actual: implementar `docs/roadmap-slice.md` completo, de corrido (autorizado por Marcos el 26/11). Cada fase lleva commit y push a la rama `unreal-5.8` del repo `vaelith-arken`; nunca a main.
- Hechas: A, A2 (cielo, horizonte, pueblo), B (guion de Pharasma), R1 (modelo de la planilla) y R2 (reglas en juego, tentación, anatema).
- Próximo paso: fase C (Ecos de la muerte con Percepción y más diagnósticos). Después D (agua, rejas y piedra), E (cierre de la tentación), F (UI en UMG desde C++ y minimapa), R3 (progresión a nivel 5), R4 (Registro del Osario), G y H (NPC del pueblo).
- Herramientas:
  - `tools/ue/regenerar_nivel.sh` reconstruye el mapa;
  - `tools/ue/capturas_ref.sh <dir>` saca las 8 vistas;
  - `-usar=id#n` usa la opción n de un interactuable;
  - `python3 tools/guion_pharasma.py` regenera el guion.
- Ojo: el sombreado agrupado (clustered) está apagado en DefaultEngine.ini: pintaba de verde las luces dinámicas.
<!-- /PUNTO-DE-CONTROL -->
