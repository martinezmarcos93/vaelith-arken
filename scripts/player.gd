extends CharacterBody2D

## Movimiento base de Vaelith Arken.
## Pilar de diseño: control aereo minimo, salto comprometido, sensacion "pesada".
## Valores de referencia: docs/stats_personaje.md (ajustables aca como @export
## para poder tunear "feel" desde el editor sin tocar codigo).

@export var speed: float = 90.0
@export var acceleration: float = 1800.0
@export var friction: float = 1200.0
@export var jump_velocity: float = -520.0
@export var gravity: float = 1400.0
@export var air_control_factor: float = 0.1
@export var coyote_time: float = 0.08

var _coyote_timer: float = 0.0


func _physics_process(delta: float) -> void:
	var on_floor := is_on_floor()

	if on_floor:
		_coyote_timer = coyote_time
	else:
		_coyote_timer = max(_coyote_timer - delta, 0.0)
		velocity.y += gravity * delta

	var input_dir := Input.get_axis("move_left", "move_right")

	if on_floor:
		if input_dir != 0.0:
			velocity.x = move_toward(velocity.x, input_dir * speed, acceleration * delta)
		else:
			velocity.x = move_toward(velocity.x, 0.0, friction * delta)
	else:
		# Control aereo deliberadamente muy limitado (pilar de diseño).
		if input_dir != 0.0:
			velocity.x = move_toward(velocity.x, input_dir * speed, acceleration * air_control_factor * delta)
		# Sin input en el aire no se aplica friccion: conserva el impulso del salto.

	if Input.is_action_just_pressed("jump") and _coyote_timer > 0.0:
		velocity.y = jump_velocity
		_coyote_timer = 0.0

	move_and_slide()
