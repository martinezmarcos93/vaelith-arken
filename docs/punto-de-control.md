# Punto de control

<!-- PUNTO-DE-CONTROL -->
**Tarea actual:** dirección artística v2 en `feat/direccion-artistica` (pusheada),
encima de `fix/coherencia-visual`. Detalle: `CHANGELOG.md` 2026-11-04 (cont.).

**Próximo paso:** que Marcos juegue y apruebe; después merge de
`fix/coherencia-visual` y luego `feat/direccion-artistica` a `main`.

**Hecho además:** tipografía en tamaño nativo (16/32/48) sin antialias,
plataformas en sillares irregulares, círculo de runas en la Torre.
Evidencia: `docs/relevamiento_2026-11-04/v2_antes.png` / `v2_despues.png`.

**Pendiente (menor):** el dorado "sagrado" sigue sin hex en la guía; los
arcos de fondo de la Intro están agrandados x1,7-2,6 (se ven blandos, quedan
tapados por la bruma); el ícono de calavera es de otro pack (sombreado liso).

**Orquestador:** encargos en `_encargos/vaelith-arken/` (va-01..05) y
`BITACORA.md` ahí. Antigravity no puede editar sin `permissions.allow` en el
host (decisión de Marcos). Oráculo: `bash tools/relevamiento/oraculo.sh`;
dentro de los sandboxes de los motores Godot no corre: usan los `check_*.py`.

**Entorno:** Godot 4.7.2 en `~/Aplicaciones/godot/`; clon ext4 para los
trabajadores en `~/src/vaelith-arken`; pixelfx clonado en el scratchpad (re-clonar
de github.com/patch-gg/pixelfx si hace falta).
<!-- /PUNTO-DE-CONTROL -->
