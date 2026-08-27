# Diseño de Enemigos Regulares (Level 1)

Filosofía: pocos enemigos, cada uno con un patrón legible y una lección de
combate específica (referencia SLAIN/Volgarr — nada de hordas ni relleno).

## 1. No-muerto errante (enemigo A — melee lento)
- **Rol:** enseñar bloqueo y timing de ataque.
- **Comportamiento:** patrulla lento en un tramo fijo. Al detectar al jugador,
  se acerca a velocidad constante (más lento que Vaelith) y ejecuta un único
  ataque de espadazo horizontal, con anticipación larga y clara (levanta el arma
  ~0.4s antes de golpear).
- **Vulnerabilidad:** tras el golpe queda "abierto" ~0.6s — ventana de castigo.
- **Vida:** 2 golpes de ataque alto de Vaelith.
- **Telegrafiado:** brillo/tensión en el arma antes del golpe (debe leerse sin
  ambigüedad incluso en la paleta oscura del juego — usar el acento rojo
  `#B41F1C` de la guía de estilo para el brillo de anticipación).

## 2. Espíritu atado (enemigo B — errático/aéreo)
- **Rol:** enseñar a leer patrones no lineales y a usar la Embestida para
  despejar espacio.
- **Comportamiento:** flota en un patrón de vaivén vertical/horizontal simple
  (no persigue directamente), y ataca con un lunge corto cuando el jugador entra
  en su rango. No bloquea con escudo tradicional — el jugador debe esquivar con
  timing de movimiento, no de bloqueo.
- **Vulnerabilidad:** tras el lunge queda inmóvil brevemente en el punto de
  impacto.
- **Vida:** 1-2 golpes (más frágil que el enemigo A, pero más difícil de leer).
- **Nota narrativa:** encaja con los "espíritus atrapados contra su voluntad" de
  la relación de Vaelith con los muertos definida en la ficha — mecánicamente es
  un enemigo, pero deja espacio para tratamiento narrativo distinto a los
  no-muertos "voluntarios" más adelante (fuera de alcance para esta demo, pero
  vale la pena no cerrar la puerta a esa distinción moral en el futuro).

## Estado de implementación (Fase 5.3)
Máquina de estados compartida implementada en `scripts/enemies/enemy_regular.gd`
(un solo script + `@export`, tal como pedía este documento). Validado
headless: detección, aproximación, ataque, ventana vulnerable y muerte
funcionan; `EspirituAtado` no persigue por diseño (confirmado: se queda en
Alerta sin atacar si el jugador nunca entra en `attack_range`, tal como se
especificó arriba).

Arte: Skeleton Warrior (CraftPix Free) para el No-muerto errante — reemplazo
2026-08-26 del placeholder anterior (Necromancer, `creativekind`), que ya no
se usa en ninguna escena (queda documentado en CREDITS.md como "evaluado, sin
uso actual"). Ghost (`fatalaigaming`, gratis) sigue para el Espíritu atado.
Ninguno de los dos es necesariamente la asignación final.

## Nota 2026-08-26: tercer enemigo excepcional (Bringer-of-Death)
Se sumó `scenes/enemies/BringerOfDeath.tscn` (mismo script/máquina de estados
de arriba) como aparición **única** en `Level1.tscn`, guardando la
aproximación a BossArena. Esto tensiona a propósito la regla "pocos enemigos,
nada de relleno": la mitigación elegida es que NO es una población nueva que
se repite por el nivel como los otros dos, sino un único encuentro puntual
(vida/daño algo mayores, lectura de "guardián especial"). Si en algún momento
se decide que rompe el ritmo de la demo, es fácil de sacar (un solo nodo en
`Level1.tscn`) sin tocar el resto del diseño. Ver CREDITS.md para detalle de
arte/licencia.

## Reglas comunes a ambos
- Ningún enemigo regular debe poder atacar dos veces seguidas sin una ventana de
  vulnerabilidad intermedia — es la garantía de que la demo se sienta "dura pero
  justa" y no injusta.
- Ambos enemigos comparten el mismo esqueleto de máquina de estados
  (Idle → Alerta → Ataque → Vulnerable → Idle) para simplificar la Fase 5.3
  (IA en Godot): un solo script base, dos configuraciones de datos distintas.
