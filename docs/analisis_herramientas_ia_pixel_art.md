# Análisis: herramientas de GitHub para pixel art / IA (agosto 2026)

## Contexto

Marcos pegó una respuesta generada por otra IA que recomienda una lista de
repositorios de GitHub para pixel art, algunos manuales y otros con
generación asistida por IA orquestable desde Claude. Ese tipo de texto —
nombres de proyectos concretos con capacidades muy específicas — es
exactamente el patrón donde una IA suele inventar o exagerar detalles
("alucinar"). Antes de darlo por bueno, se verificó cada ítem por separado
vía búsqueda web real.

## Metodología

Para cada herramienta mencionada se buscó: ¿existe el repo?, ¿coincide el
nombre exacto?, ¿la licencia y las capacidades declaradas son las que dice
el texto original? No se instaló ni probó ninguna — es una verificación de
existencia y plausibilidad, no un test funcional.

## Veredicto por herramienta

| Herramienta | Afirmación del texto original | Verificación | Notas |
|---|---|---|---|
| **Pixelorama** | Editor MIT hecho en Godot, exportación automatizable por CLI | ✅ **Confirmado** | Real, maduro, 8.5k+ estrellas, `Orama-Interactive/Pixelorama`, MIT. El proyecto más sólido de toda la lista. |
| **LibreSprite** | Clon libre de Aseprite, GPLv2 | ✅ **Confirmado** (ya lo tenés instalado) | Ya en uso en este proyecto. |
| **"Aseprite MCP Pro"** | "El santo grial": 90+ herramientas, control total de Aseprite/LibreSprite desde Claude, exporta `.tres` de Godot, MIT | ⚠️ **Nombre engañoso** | No existe un proyecto único llamado así. Hay **varios** proyectos separados, de autores distintos y sin relación entre sí, todos llamados genéricamente `aseprite-mcp`/`aseprite_mcp` (rkdfx, Dizzd, diivi) más uno similar llamado `pixel-mcp`/`pixel-plugin` (willibrandon). Ninguno confirmado con "90+ herramientas" ni con el pulido que sugiere "Pro". El texto original probablemente fusionó varios proyectos chicos de hobby en una sola recomendación con nombre inventado. |
| **SpriteBrew** | Generador de sprites con IA, exporta a Godot, AGPL-3.0, open source | ✅ **Confirmado**, con matiz | Repo real (`GAlbanese09/spritebrew`). Pero es el código fuente de un **producto SaaS** (spritebrew.com) — la generación por IA probablemente depende de un backend/API de pago, no es "clonar y listo". |
| **agent-sprite-forge** | Skill de agente para generar sprites/mapas/GIFs desde prompts | ✅ **Confirmado** | Real (`0x0funky/agent-sprite-forge`), explícitamente diseñado para Codex/Claude Code — es el que más se parece a lo que buscás (Claude orquestando la generación). Reportado con ~3.4k estrellas (dato de búsqueda resumida, no verificado dígito a dígito). |
| **Sprite Pipeline (plugin Godot)** | Genera sprites con IA dentro del editor de Godot vía OpenAI | ✅ **Confirmado**, con matiz importante | Real (`fabs133/sprite-pipeline-plugin`), en el Asset Library de Godot. Usa la **API de OpenAI de pago** (BYOK = traés tu propia API key, o "pool" de créditos compartidos) — no es gratis ni local. |
| **Pixel Sprite Monster Generator** | Generador de sprites de monstruos dentro de Godot 4 | ✅ **Confirmado** | Real (`ninetailsrabbit/pixel-sprite-monster-generator`), puerto a Godot 4 del generador procedural de deep-fold. **No usa IA/LLM** — es generación algorítmica por reglas, dato que el texto original no aclaraba. |
| **Pixel Wall-E** | Herramienta "guiada por código" en Godot/C# | ❌ **No se pudo confirmar que exista** | Ninguna búsqueda encontró un proyecto con ese nombre relacionado a Godot/pixel art. Posible invención del texto original — no recomendable dar por cierto sin una fuente directa. |
| **PixelCraft** | Editor de pixel art en navegador, MIT | ✅ **Confirmado** | Real (`rgab1508/PixelCraft`), simple, basado en HTML5 Canvas/PWA. |

## Hallazgos importantes

1. **"Aseprite MCP Pro" no existe como proyecto único.** Es la recomendación con más peso del texto original ("el santo grial") y es justamente la que resultó ser una atribución imprecisa de varios proyectos chicos y no relacionados. Si en algún momento se quiere ese flujo (Claude controlando LibreSprite/Aseprite directo), habría que evaluar `diivi/aseprite-mcp`, `rkdfx/aseprite-mcp`, `Dizzd/aseprite_mcp` o `willibrandon/pixel-mcp` **individualmente**, sin asumir que cualquiera de ellos tiene las 90+ herramientas prometidas.

2. **"Pixel Wall-E" no se pudo verificar.** Se trata como no confiable hasta que aparezca una fuente concreta.

3. **Varias opciones dependen de APIs pagas de terceros (OpenAI).** Sprite Pipeline y probablemente la parte de generación de SpriteBrew necesitan una API key con costo y conexión a un servicio externo — exactamente el tipo de dependencia de red que ya te generó fricción con el SSL de la oficina (ver `Documents/Claude-Vault/Leyes/Red-y-SSL.md`). No es un bloqueante técnico, pero sí una razón para no adoptarlas a la ligera en este entorno.

## Recomendación para el pipeline actual

Ya tenés funcionando: LibreSprite portátil + Blender + Godot portátil + Claude Code orquestando por código/archivos (sin depender de un MCP visual). Con eso como base:

- **No cambies nada todavía.** El pipeline actual (yo escribo/edito `.tscn`/`.gd` y assets directamente, vos revisás en LibreSprite/Godot) ya funciona y quedó demostrado hoy con el sistema de combate.
- **Si en algún momento querés que genere arte nuevo por prompt en vez de editar a mano**, `agent-sprite-forge` es la opción que más se alinea con tu idea original de "Claude orquesta todo" — pero antes de sumarla habría que probarla en un caso chico y revisar qué modelo de imagen usa por debajo (si depende de una API paga, aplica la misma advertencia del punto anterior).
- **Pixelorama** es una alternativa sólida a LibreSprite si en algún momento querés algo con más funciones de animación/tilemap nativas de Godot — no reemplaza nada ahora, pero es una opción confiable si LibreSprite se queda corta.
- Evitaría por ahora cualquier opción que dependa de una API de pago (Sprite Pipeline, probablemente SpriteBrew) mientras no haya una necesidad concreta que LibreSprite/Blender no resuelvan.

## Nota metodológica

Este documento anota únicamente lo verificable por búsqueda a la fecha
(agosto 2026). Antes de instalar o depender de cualquiera de estos
proyectos, corresponde una revisión más profunda (leer el código, probarlo
en un branch aparte) — esto es un análisis de "¿existe y es razonable
confiar en la afirmación?", no una auditoría de seguridad ni de calidad.
