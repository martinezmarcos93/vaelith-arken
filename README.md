# Vaelith Arken — Unreal (primera persona)

Adaptación de Vaelith Arken a un RPG de acción 3D en primera persona en Unreal
Engine 5.8, a la manera de los RPG de mundo abierto (sin copiar ningún juego
existente: historia, personajes y diseño son propios).

- **Proyecto original (Godot, 2D pixel art):**
  `/media/marcos/A68072A880727F1D/01-Marcos/00-Programacion/mmac-dev-lab/80-creativo/juegos/vaelith-arken/vaelith-arken/`
  — queda intacto y es la referencia de diseño y narrativa.
- **Estado:** solo local. **No va a GitHub** (decisión de Marcos, 2026-11-24).
  Sin git por ahora.
- **Por qué en `~/src` (ext4):** Unreal trabaja mal sobre el disco NTFS de datos
  (permisos, symlinks, rendimiento con miles de archivos chicos).

## Stack

- Unreal Engine 5.8 nativo para Linux (`~/Aplicaciones/UE_5.8`), proyecto `VaelithArken.uproject`
  (plantilla First Person + variante Survival Horror).
- Lógica en C++; Blueprints solo como cáscara de datos y configuración.
- Conexión con Claude Code: Unreal MCP oficial de 5.8 (`127.0.0.1:8000/mcp`, arranca
  solo con el editor; cliente mínimo `tools/mcp/ue.sh`). Para importar y construir
  niveles: scripts de Python en `tools/ue/` que corren dentro del editor
  (`tools/ue/correr.sh`). La ejecución remota de Python de Unreal no se usa: en Linux
  exige multicast en la red local.

## Hardware de desarrollo (medido 2026-11-24)

GTX 1060 3 GB (driver 580, Vulkan 1.4), 4 núcleos, 16 GB RAM, Ubuntu 24.04.
Epic recomienda 8 GB de VRAM y 32 GB de RAM; Lumen exige RTX 2000 o superior.
Por eso: sin Lumen, sin sombras virtuales, Nanite solo si la Fase 0 lo permite,
luz precalculada.

## Documentos

- `docs/plan-adaptacion.md` — historia por zonas, fases, alcance y assets.
- `docs/sistemas.md` — sistemas de juego (PF2e en tiempo real).
- `docs/fase0-medicion.md` — rendimiento medido en la GTX 1060.
- `docs/punto-de-control.md` — dónde quedó el trabajo.

## Uso

| Qué | Comando |
|---|---|
| Abrir el editor (o reiniciarlo) | `tools/reiniciar-editor.sh` |
| Compilar C++ y correr tests | `tools/ue/tests.sh` (con el editor cerrado) |
| Correr un script de construcción | `tools/ue/correr.sh tools/ue/<script>.py` (editor cerrado) |
| Medir FPS y VRAM de un nivel | `tools/ue/medir.sh /Game/<ruta del nivel>` |
| Hablar con el MCP | `tools/mcp/ue.sh list_toolsets` (editor abierto) |
| Generar assets en Blender | `~/Aplicaciones/blender-5.3.0/blender -b --factory-startup -P tools/blender/<script>.py -- <salida>` |

Código C++ en `Source/VaelithArken/`. Logs en `~/Aplicaciones/UE_5.8/_logs/`; en modo
juego, Unreal escribe logs y CSV en `~/.config/Epic/UnrealEngine/5.8/Saved/`.
