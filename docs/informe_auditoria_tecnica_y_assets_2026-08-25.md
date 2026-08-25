# Informe de auditoría técnica y estrategia de assets

**Fecha:** 2026-08-25  
**Alcance:** revisión estática del vertical slice de Vaelith Arken.

## Resumen ejecutivo

La base técnica es apropiada para un vertical slice: hay escenas separadas,
scripts con responsabilidades razonables, documentación de diseño amplia y las
referencias internas de recursos son consistentes. Se verificaron 93 referencias
`res://` sin rutas faltantes.

El riesgo principal no es que falten assets gratuitos: es que los assets de
terceros están cumpliendo, a la vez, el papel de placeholder, biblioteca de
referencia y posible arte final. Para que el juego tenga identidad y una cadena
de licencias clara, Vaelith, el Guerrero-Espejo, enemigos clave y el tileset
principal deben pasar a ser assets propios.

Esta fue una revisión estática. No se ejecutó el proyecto porque Godot no estaba
disponible en el entorno de revisión.

## Hallazgos técnicos

### Críticos

1. **El bloqueo no es direccional.**
   - `player.gd` y `boss1.gd` bloquean cualquier golpe mientras el estado es
     `BLOCK`, también los impactos que llegan desde atrás.
   - Esto contradice el combate direccional y el bloqueo frontal definidos en
     `GDD.md` y `stats_personaje.md`.
   - Acción propuesta: comparar la dirección entrante con `facing` antes de
     registrar el bloqueo; los impactos traseros deben dañar normalmente.

2. **La embestida no aplica el stagger diseñado.**
   - `Hitbox` transmite `stagger_time`, pero jugador, enemigos y boss no lo
     consumen como estado de juego.
   - El shove del Boss 1, que en fase 2 debe romper la guardia, hoy entra como
     un hit de daño cero: empuja al jugador, lo deja en `HURT` durante 0,3 s y
     le concede i-frames, en vez de dejarlo en `STAGGERED` durante 0,6 s.
   - Acción propuesta: priorizar `stagger_time > 0` en el receptor del golpe y
     transicionar al estado de stagger. Definir explícitamente si una guardia
     bloquea o es rota por esa clase de golpe.

### Medios

3. **Los enemigos no reaccionan al daño.**
   - `enemy_regular.gd` exporta animación de hurt y recibe `stagger_time`, pero
     no usa ninguno: al recibir daño puede continuar su ataque.
   - Acción propuesta: agregar estados `HURT`/`STAGGERED`, o eliminar esos
     exports si el comportamiento es una decisión deliberada.

4. **El Espíritu atado conserva velocidad vertical tras su lunge.**
   - Durante `VULNERABLE` se frena solo `velocity.x`; la componente vertical
     permanece hasta que vuelva a idle.
   - Acción propuesta: desacelerar el vector completo o fijar el punto de
     vulnerabilidad al terminar el lunge.

5. **El dummy de entrenamiento puede finalizar un ataque después de morir.**
   - Si muere durante `attack_windup`, su `Hitbox` queda activa hasta que
     termina el `await`.
   - Acción propuesta: desactivar el hitbox al morir y comprobar que siga vivo
     antes de activar o finalizar una secuencia de ataque.

## Incoherencias de documentación

- `GDD.md` indica que el ataque bajo puede ejecutarse con "abajo + J", pero
  `input_setup.gd` solo registra la tecla `K`; no existe esa combinación.
- El `CHANGELOG.md` marca como pendientes la intro, IA del boss, menús y
  diálogo, aunque ya existen implementaciones en el repositorio. Debe
  actualizarse para que roadmap, changelog y código vuelvan a coincidir.
- La penitencia está definida como pilar (corrupción incremental por muerte),
  pero por ahora solo está implementado el respawn. Es una deuda de producto
  explícita, no un bug accidental.

## Código repetido y deuda de arquitectura

- `checkpoint.gd`, `dialogue_trigger.gd`, `memory_fragment.gd`,
  `scene_transition_trigger.gd` y `skull_collectible.gd` repiten el patrón
  `Area2D` + `body_entered` + grupo `player` + `already_active`.
  Conviene extraer una base `PlayerTrigger` o un componente común.
- `player.gd` y `boss1.gd` replican partes sensibles del combate. Un recurso de
  configuración de ataques o un componente reutilizable de combatiente evitaría
  que timings, bloqueo y stagger se desalineen.
- Se encontraron tres pares de PNG idénticos en packs de terceros. El impacto
  de tamaño es mínimo, pero confirma que los packs deben tratarse como una
  biblioteca separada del arte de producción.

## Estrategia: assets propios

Sí, el proyecto puede y debería gestionar assets propios. Ya tiene decisiones
de producción suficientes para hacerlo: sprite principal de 32x48 px, tile
base de 16x16 px, paleta fría y reglas de acento cálido documentadas.

### Estructura recomendada

```text
assets/
  game/          # PNGs propios, finales y usados por el juego
  third_party/   # Placeholders y packs externos, con licencia y atribución
art/
  source/        # .aseprite/.ora, paletas, bocetos y hojas editables
  manifest.md    # autor, estado, fuente, licencia y escenas que lo usan
```

Cada asset propio debe registrar como mínimo: identificador, autor, archivo
fuente editable, PNG exportado, fecha, estado (boceto/final) y escenas que lo
consumen. Cada asset de terceros debe conservar URL, licencia, texto de
atribución y condición de redistribución.

### Orden de reemplazo

1. Vaelith: idle, run, jump/fall, ataques alto y bajo, block, shove, hurt y
   death.
2. Guerrero-Espejo: variación propia del diseño de Vaelith; así se sostiene la
   premisa narrativa de que es un reflejo del jugador.
3. Tileset de cripta de 16x16 y props indispensables para Level 1.
4. No-muerto errante y Espíritu atado.
5. UI, VFX y audio finales.

LibreSprite/Aseprite debe ser el origen del pixel art final. Las herramientas
generativas pueden usarse para moodboards, briefs y exploración de siluetas,
pero no sustituyen hojas de sprites consistentes, editables y con animaciones
controladas.

## Regla de licencias

Los placeholders comunitarios pueden permanecer durante el desarrollo, pero no
deben mezclarse con la carpeta de assets finales. En particular, el repositorio
marca `textures_seamless_unverified_license` como licencia no verificada: no
debe incluirse en una build pública hasta identificar fuente y términos.

## Prioridad de trabajo recomendada

1. Corregir bloqueo direccional y stagger.
2. Playtestear el combate con esos cambios.
3. Crear el manifiesto y estructura de fuentes de arte.
4. Producir el primer sprite sheet propio de Vaelith.
5. Reemplazar el placeholder del Boss 1 a partir de ese mismo lenguaje visual.
