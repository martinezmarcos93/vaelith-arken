# Punto de control

<!-- PUNTO-DE-CONTROL -->
- Tarea actual: roadmap del slice (`docs/roadmap-slice.md`), **en pausa por pedido de Marcos (26/11)** a mitad de la fase F (UI en UMG desde C++).
- Hechas, con push a la rama `unreal-5.8` (nunca a main): A, A2, B, R1, R2, C, D y E. Tests 8/8. Detalle en `docs/handoffs/2026-11-26.md`.
- Próximo paso al retomar:
  1. Bug del verde intermitente en las luces dinámicas, con `depuracion-sistematica`. Métrica: verde medio de la captura del menú > 3.
  2. Terminar F: botones en `USizeBox`, capturas del HUD, la pausa y el minimapa, y borrar los PNG del Godot.
  3. Después R3 (progresión a nivel 5), R4 (Registro del Osario), G y H.
- Bloqueado por: nada. G espera los assets de Marcos.
- Herramientas: `tools/ue/regenerar_nivel.sh`, `tools/ue/capturas_ref.sh`, `-usar=id#n`, `tools/guion_pharasma.py`.
- Preguntas abiertas: ¿la rama `unreal-5.8` se integra alguna vez a main? (decide Marcos).
<!-- /PUNTO-DE-CONTROL -->
