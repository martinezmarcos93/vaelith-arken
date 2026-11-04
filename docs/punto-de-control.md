# Punto de control

<!-- PUNTO-DE-CONTROL -->
**Tarea actual:** ninguna en curso. Coherencia visual y dirección artística v2
mergeadas a `main` (7efb68b) el 2026-11-04; ramas temporales borradas (local,
remoto y clon ext4). Detalle: `CHANGELOG.md` 2026-11-04 y handoff del día.

**Próximo paso (cuando se retome):** elegir entre los pendientes menores o
seguir con contenido (niveles, combate). Antes de tocar arte: `CLAUDE.md`
(excepción pixelfx, nunca escalar nodos: `hornear_escalas.py`).

**Pendiente (menor):** el dorado "sagrado" sin hex en la guía v2 (hoy usa
`#B41F1C`); arcos de fondo de la Intro agrandados x1,7-2,6 (blandos, tapados
por bruma); ícono de calavera de otro pack (sombreado liso); Zombi sin uso.

**Bloqueado por:** nada. Antigravity necesita `permissions.allow` en el host
para editar desatendido (decisión de Marcos, sin tomar).

**Verificación:** `bash tools/relevamiento/oraculo.sh` → "ORACULO OK";
`tools/relevamiento/cruzar_level1.gd` cruza Level1 hasta el boss.
Dentro de los sandboxes de los motores Godot no corre: usan los `check_*.py`.

**Entorno:** Godot 4.7.2 en `~/Aplicaciones/godot/`; clon ext4 para trabajadores
en `~/src/vaelith-arken` (en `main`, sin worktrees); pixelfx: re-clonar de
github.com/patch-gg/pixelfx si hace falta.
<!-- /PUNTO-DE-CONTROL -->
