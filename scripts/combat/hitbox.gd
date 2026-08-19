extends Area2D
class_name Hitbox

## Zona de daño activable/desactivable a demanda (por el estado de combate de
## quien la posee, ya sea jugador, enemigo o boss). damage=0 + stagger_time>0
## representa un golpe "de utilidad" (ej. la Embestida): no quita vida, pero
## desequilibra al objetivo.

@export var damage: int = 1
@export var knockback: float = 200.0
@export var stagger_time: float = 0.0

## Quien genera el golpe, para no autoimpactarse y para calcular la
## direccion del knockback. Se asigna desde el dueño (ej. player.gd).
var source: Node2D = null

## Objetivos ya golpeados durante la activacion actual, para no aplicar el
## mismo golpe dos veces (una por el chequeo manual de activate() y otra por
## la señal area_entered si ambas dispararan para la misma area).
var _hit_targets: Array = []

func _ready() -> void:
	monitoring = false
	area_entered.connect(_on_area_entered)

func activate() -> void:
	if monitoring:
		return
	monitoring = true
	_hit_targets.clear()
	# Godot NO vuelve a emitir area_entered para superposiciones que ya
	# existian en el momento de activar monitoring: si el objetivo esta
	# pegado al cuerpo (ej. un dummy quieto), un golpe repetido nunca
	# conectaria sin este chequeo manual.
	for area in get_overlapping_areas():
		_try_hit(area)

func deactivate() -> void:
	monitoring = false

func _on_area_entered(area: Area2D) -> void:
	_try_hit(area)

func _try_hit(area: Area2D) -> void:
	if not (area is Hurtbox):
		return
	var target := area.get_parent()
	if target == source:
		return
	if area in _hit_targets:
		return
	_hit_targets.append(area)
	var direction := Vector2.RIGHT
	if source and target is Node2D:
		direction = (target.global_position - source.global_position).normalized()
		if direction == Vector2.ZERO:
			direction = Vector2.RIGHT
	area.receive_hit(damage, direction, knockback, stagger_time)
