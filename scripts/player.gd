extends CharacterBody2D

## Vaelith Arken: movimiento (Etapa 1.1) + combate base (Etapa 1.3).
## Valores de referencia: docs/stats_personaje.md (ajustables como @export
## para tunear "feel" desde el editor sin tocar codigo).

enum State { FREE, ATTACK_HIGH, ATTACK_LOW, BLOCK, SHOVE, HURT, STAGGERED, DEAD }

## Para que el HUD (Etapa 9.1) refleje la vida sin necesitar una referencia
## directa al nodo Player -- se emite en _ready() y en cada cambio real.
signal health_changed(current: int, max: int)

# --- Movimiento ---
@export_group("Movimiento")
@export var speed: float = 90.0
@export var acceleration: float = 1800.0
@export var friction: float = 1200.0
@export var jump_velocity: float = -520.0
@export var gravity: float = 1400.0
@export var air_control_factor: float = 0.1
@export var coyote_time: float = 0.08

@export_group("Camara")
## Cuanto se adelanta la camara en la direccion en la que mira Vaelith
## (Fase 1.2 del roadmap). Los limites de nivel se configuran por escena
## (override del nodo Camera2D en cada .tscn de nivel), no aca, porque
## Player.tscn se reutiliza entre niveles con distintos limites.
@export var camera_lookahead_distance: float = 60.0
@export var camera_lookahead_lerp_speed: float = 4.0

# --- Combate ---
@export_group("Combate")
@export var max_health: int = 5
@export var iframes_duration: float = 0.4
@export var hurt_lock_time: float = 0.3

@export var attack_high_damage: int = 2
@export var attack_high_duration: float = 0.5
@export var attack_high_active_start: float = 0.2
@export var attack_high_active_end: float = 0.35

@export var attack_low_damage: int = 1
@export var attack_low_duration: float = 0.35
@export var attack_low_active_start: float = 0.12
@export var attack_low_active_end: float = 0.22

@export var shove_duration: float = 0.25
@export var shove_active_start: float = 0.05
@export var shove_active_end: float = 0.15
@export var shove_knockback: float = 300.0
@export var shove_stagger_time: float = 0.6

@export var block_max_consecutive: int = 3
@export var block_stagger_time: float = 0.8

@export_group("Penitencia")
## Respawn automatico en el ultimo checkpoint (Fase 4.3). La corrupcion de
## nivel de "penitencia" (docs/stats_personaje.md: +1 nivel por muerte)
## queda fuera de alcance hasta que exista un Level 1 real con tramos de
## dificultad ajustable -- esto solo resuelve el respawn en si.
@export var respawn_delay: float = 1.5
@export var respawn_iframes: float = 1.0

## Ventana de gracia para inputs de combate presionados justo antes de que
## el jugador pueda procesarlos (ej. un frame en el aire por el knockback
## de un golpe recibido). Sin esto, is_action_just_pressed() se pierde para
## siempre si no se consulta en el frame exacto -- encontrado con testing.
@export var input_buffer_time: float = 0.12

const HITBOX_OFFSET_X := 20.0

@onready var attack_high_hitbox: Hitbox = $AttackHighHitbox
@onready var attack_low_hitbox: Hitbox = $AttackLowHitbox
@onready var shove_hitbox: Hitbox = $ShoveHitbox
@onready var hurtbox: Hurtbox = $Hurtbox
@onready var camera: Camera2D = $Camera2D
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D

var state: State = State.FREE
var facing: int = 1
var health: int
var _coyote_timer: float = 0.0
var _iframe_timer: float = 0.0
var _state_timer: float = 0.0
var _consecutive_blocks: int = 0
var _buffered_action: String = ""
var _buffer_timer: float = 0.0
var _respawn_position: Vector2
var _respawn_timer: float = 0.0

const BUFFERABLE_ACTIONS := ["attack_high", "attack_low", "shove"]


func _ready() -> void:
	add_to_group("player")
	health = max_health
	health_changed.emit(health, max_health)
	_respawn_position = global_position
	attack_high_hitbox.source = self
	attack_high_hitbox.damage = attack_high_damage
	attack_high_hitbox.knockback = 0.0
	attack_low_hitbox.source = self
	attack_low_hitbox.damage = attack_low_damage
	attack_low_hitbox.knockback = 0.0
	shove_hitbox.source = self
	shove_hitbox.damage = 0
	shove_hitbox.knockback = shove_knockback
	shove_hitbox.stagger_time = shove_stagger_time
	hurtbox.hurt.connect(_on_hurtbox_hurt)


func _physics_process(delta: float) -> void:
	if _iframe_timer > 0.0:
		_iframe_timer = max(_iframe_timer - delta, 0.0)

	_update_hitbox_facing()
	_update_camera_lookahead(delta)
	_poll_input_buffer(delta)

	match state:
		State.FREE:
			_process_movement(delta)
			_process_free_inputs()
		State.BLOCK:
			_process_block(delta)
		State.ATTACK_HIGH:
			_process_action(delta, attack_high_hitbox, attack_high_duration, attack_high_active_start, attack_high_active_end)
		State.ATTACK_LOW:
			_process_action(delta, attack_low_hitbox, attack_low_duration, attack_low_active_start, attack_low_active_end)
		State.SHOVE:
			_process_action(delta, shove_hitbox, shove_duration, shove_active_start, shove_active_end)
		State.HURT:
			_process_timed_lock(delta, hurt_lock_time)
		State.STAGGERED:
			_process_timed_lock(delta, block_stagger_time)
		State.DEAD:
			_process_dead(delta)

	_update_sprite_animation()
	move_and_slide()


func _process_movement(delta: float) -> void:
	var on_floor := is_on_floor()

	if on_floor:
		_coyote_timer = coyote_time
	else:
		_coyote_timer = max(_coyote_timer - delta, 0.0)
		velocity.y += gravity * delta

	var input_dir := Input.get_axis("move_left", "move_right")
	if input_dir != 0.0:
		facing = 1 if input_dir > 0.0 else -1

	if on_floor:
		if input_dir != 0.0:
			velocity.x = move_toward(velocity.x, input_dir * speed, acceleration * delta)
		else:
			velocity.x = move_toward(velocity.x, 0.0, friction * delta)
	else:
		if input_dir != 0.0:
			velocity.x = move_toward(velocity.x, input_dir * speed, acceleration * air_control_factor * delta)
		# Sin input en el aire no se aplica friccion: conserva el impulso del salto.

	if Input.is_action_just_pressed("jump") and _coyote_timer > 0.0:
		velocity.y = jump_velocity
		_coyote_timer = 0.0


func _poll_input_buffer(delta: float) -> void:
	# Se consulta SIEMPRE, sin importar el estado actual, para no perder el
	# unico frame en el que is_action_just_pressed() es verdadero.
	for action in BUFFERABLE_ACTIONS:
		if Input.is_action_just_pressed(action):
			_buffered_action = action
			_buffer_timer = input_buffer_time
	if _buffer_timer > 0.0:
		_buffer_timer = max(_buffer_timer - delta, 0.0)
		if _buffer_timer == 0.0:
			_buffered_action = ""


func _process_free_inputs() -> void:
	# Bloqueo y embestida siguen solo en tierra (necesitan apoyo/postura).
	# Los ataques se habilitaron tambien en el aire a pedido explicito --
	# rompe a proposito el pilar original de "sin duelista aereo", pero
	# _enter_action() sigue poniendo velocity.x=0 al entrar en la accion,
	# asi que atacar en el aire corta el impulso horizontal del salto: sigue
	# siendo una decision con costo, no un combo gratis.
	var action_needs_floor := _buffered_action == "shove"
	if _buffered_action != "" and (is_on_floor() or not action_needs_floor):
		var action := _buffered_action
		_buffered_action = ""
		_buffer_timer = 0.0
		match action:
			"attack_high":
				_enter_action(State.ATTACK_HIGH)
			"attack_low":
				_enter_action(State.ATTACK_LOW)
			"shove":
				_enter_action(State.SHOVE)
		return
	if not is_on_floor():
		return
	if Input.is_action_pressed("block"):
		state = State.BLOCK


func _process_block(delta: float) -> void:
	if not is_on_floor():
		velocity.y += gravity * delta
	velocity.x = move_toward(velocity.x, 0.0, friction * delta)
	if not Input.is_action_pressed("block"):
		state = State.FREE
		_consecutive_blocks = 0


func _enter_action(new_state: State) -> void:
	state = new_state
	_state_timer = 0.0
	velocity.x = 0.0


func _process_action(delta: float, hitbox: Hitbox, duration: float, active_start: float, active_end: float) -> void:
	_state_timer += delta
	if not is_on_floor():
		velocity.y += gravity * delta

	var should_be_active := _state_timer >= active_start and _state_timer < active_end
	if should_be_active and not hitbox.monitoring:
		hitbox.activate()
	elif not should_be_active and hitbox.monitoring:
		hitbox.deactivate()

	if _state_timer >= duration:
		hitbox.deactivate()
		state = State.FREE
		_state_timer = 0.0


func _process_timed_lock(delta: float, duration: float) -> void:
	_state_timer += delta
	if not is_on_floor():
		velocity.y += gravity * delta
	velocity.x = move_toward(velocity.x, 0.0, friction * delta)
	if _state_timer >= duration:
		state = State.FREE
		_state_timer = 0.0


func _process_dead(delta: float) -> void:
	# A diferencia de HURT/STAGGERED, DEAD no vuelve a FREE por vencimiento
	# de timer solo -- revertir automaticamente ahi era el bug de la Fase
	# 1.4 (un "cadaver" con 0 HP que seguia peleando). El unico camino de
	# salida de DEAD es _respawn(), tras respawn_delay (Fase 4.3).
	if not is_on_floor():
		velocity.y += gravity * delta
	velocity.x = move_toward(velocity.x, 0.0, friction * delta)
	_respawn_timer += delta
	if _respawn_timer >= respawn_delay:
		_respawn()


func set_checkpoint(world_position: Vector2) -> void:
	_respawn_position = world_position


func _respawn() -> void:
	global_position = _respawn_position
	velocity = Vector2.ZERO
	health = max_health
	health_changed.emit(health, max_health)
	_iframe_timer = respawn_iframes
	_respawn_timer = 0.0
	state = State.FREE
	print("Vaelith: penitencia cumplida, respawn en %s" % _respawn_position)


## Placeholder temporal (Opcion A del roadmap de arte): reutiliza el pack
## CC0 "Evil Wizard 2" (pensado como enemigo, ver CREDITS.md) solo para
## validar que AnimationPlayer/AnimatedSprite2D sincroniza bien con la
## maquina de estados ANTES de invertir tiempo en el sprite sheet final de
## Vaelith (Etapa 2.1-2.3). shove y block no tienen animacion propia en el
## pack -- se reutilizan attack2/idle a proposito, no es un mapeo definitivo.
func _update_sprite_animation() -> void:
	sprite.flip_h = facing < 0
	var target_anim: String
	match state:
		State.FREE:
			if not is_on_floor():
				target_anim = "jump" if velocity.y < 0.0 else "fall"
			elif absf(velocity.x) > 5.0:
				target_anim = "run"
			else:
				target_anim = "idle"
		State.BLOCK:
			target_anim = "idle"
		State.ATTACK_HIGH:
			target_anim = "attack1"
		State.ATTACK_LOW:
			target_anim = "attack2"
		State.SHOVE:
			target_anim = "attack2"
		State.HURT, State.STAGGERED:
			target_anim = "hurt"
		State.DEAD:
			target_anim = "dead"
		_:
			target_anim = "idle"
	if sprite.animation != target_anim:
		sprite.play(target_anim)


func _update_camera_lookahead(delta: float) -> void:
	var target_offset_x: float = camera_lookahead_distance * facing
	var weight: float = clamp(camera_lookahead_lerp_speed * delta, 0.0, 1.0)
	camera.offset.x = lerp(camera.offset.x, target_offset_x, weight)


func _update_hitbox_facing() -> void:
	attack_high_hitbox.position.x = HITBOX_OFFSET_X * facing
	attack_low_hitbox.position.x = HITBOX_OFFSET_X * facing
	shove_hitbox.position.x = (HITBOX_OFFSET_X + 4.0) * facing


func _on_hurtbox_hurt(damage: int, direction: Vector2, knockback: float, stagger_time: float) -> void:
	if state == State.DEAD:
		return
	if _iframe_timer > 0.0:
		return
	if state == State.BLOCK and damage > 0:
		_register_block()
		return
	_take_damage(damage, direction, knockback, stagger_time)


func _register_block() -> void:
	_consecutive_blocks += 1
	if _consecutive_blocks > block_max_consecutive:
		_consecutive_blocks = 0
		state = State.STAGGERED
		_state_timer = 0.0
		print("Vaelith: postura rota tras bloquear %d golpes seguidos" % block_max_consecutive)
	else:
		print("Vaelith: golpe bloqueado (%d/%d)" % [_consecutive_blocks, block_max_consecutive])


func _take_damage(damage: int, direction: Vector2, knockback: float, stagger_time: float) -> void:
	health = max(health - damage, 0)
	health_changed.emit(health, max_health)
	print("Vaelith: recibe %d de daño (vida=%d/%d)" % [damage, health, max_health])
	if health <= 0:
		_die(direction, knockback)
		return
	_iframe_timer = iframes_duration
	velocity = direction * knockback
	state = State.HURT
	_state_timer = 0.0


func _die(direction: Vector2, knockback: float) -> void:
	# DEAD no vuelve a FREE por vencimiento de timer (ver _process_dead) --
	# el unico camino de salida es _respawn() tras respawn_delay. La
	# corrupcion de nivel de "penitencia" (mas enemigos/menos luz por
	# muerte, docs/stats_personaje.md) sigue pendiente: depende de tramos
	# reales con dificultad ajustable, no del respawn en si.
	state = State.DEAD
	velocity = direction * knockback
	print("Vaelith: HP a 0 - estado DEAD (input bloqueado, respawn en %.1fs)" % respawn_delay)
