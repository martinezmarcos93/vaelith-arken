extends CharacterBody2D

## Enemigo regular generico (Fase 5.3). Un solo script + configuracion de
## datos por escena, tal como pide docs/diseno_enemigos.md: ambos enemigos
## comparten la maquina de estados Idle -> Alerta -> Ataque -> Vulnerable ->
## Idle, y solo cambian los @export de esta clase entre "No-muerto errante"
## (move_mode="ground_patrol") y "Espiritu atado" (move_mode="float_sway").
##
## Arte: packs gratuitos catalogados en CREDITS.md (Skeleton Warrior para el
## no-muerto errante, ghost para el espiritu atado) -- ninguno es
## necesariamente la asignacion final de arte.

enum State { IDLE, ALERT, ATTACK, VULNERABLE, DEAD }

@export_group("Deteccion y movimiento")
@export_enum("ground_patrol", "float_sway") var move_mode: String = "ground_patrol"
@export var detection_range: float = 220.0
## OJO al bajar este valor en un ground_patrol: si hay otro CharacterBody2D
## solido (jugador, otro enemigo) en el camino, move_and_slide() frena al
## enemigo por colision fisica ANTES de que la distancia logica llegue a
## attack_range -- se puede quedar pegado sin atacar nunca. Encontrado con
## testing headless (Fase 5.3): dejar margen por encima de la suma de los
## semi-anchos de colision involucrados, no solo del "alcance narrativo".
@export var attack_range: float = 40.0
@export var approach_speed: float = 45.0
@export var patrol_distance: float = 60.0
@export var patrol_speed: float = 25.0
@export var gravity: float = 1400.0

@export_group("Vaiven (solo float_sway)")
@export var sway_amplitude: float = 20.0
@export var sway_speed: float = 1.2
@export var lunge_speed: float = 260.0

@export_group("Combate")
@export var attack_hitbox_offset_x: float = 20.0
@export var max_health: int = 4
@export var attack_windup: float = 0.4
@export var attack_active_duration: float = 0.25
@export var attack_damage: int = 1
@export var attack_knockback: float = 220.0
@export var vulnerable_duration: float = 0.6

@export_group("Animacion (placeholder, ver assets reales por escena)")
@export var anim_idle: String = "idle"
@export var anim_move: String = "idle"
@export var anim_attack: String = "idle"
@export var anim_vulnerable: String = "idle"
@export var anim_hurt: String = "idle"
@export var anim_death: String = "idle"

@onready var hurtbox: Hurtbox = $Hurtbox
@onready var attack_hitbox: Hitbox = $AttackHitbox
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D

# --- Audio (SFX en assets/audio/sfx/, ver docs/lista_audio.md §3) ---
const SFX_SWING := ["res://assets/audio/sfx/combat/sword_swing_01.ogg", "res://assets/audio/sfx/combat/sword_swing_02.ogg", "res://assets/audio/sfx/combat/sword_swing_03.ogg"]
const SFX_WHOOSH := ["res://assets/audio/sfx/player/whoosh_01.wav", "res://assets/audio/sfx/player/whoosh_02.wav"]
const SFX_IMPACT := ["res://assets/audio/sfx/combat/impact_flesh_01.ogg", "res://assets/audio/sfx/combat/impact_flesh_02.ogg", "res://assets/audio/sfx/combat/impact_flesh_03.ogg"]
const SFX_DEATH := ["res://assets/audio/sfx/combat/impact_gore_01.wav", "res://assets/audio/sfx/combat/impact_gore_02.wav"]

var state: State = State.IDLE
var health: int
var facing: int = 1

var _spawn_position: Vector2
var _state_timer: float = 0.0
var _patrol_direction: int = 1
var _lunge_target: Vector2 = Vector2.ZERO
var _sway_time: float = 0.0


func _ready() -> void:
	add_to_group("enemy")
	health = max_health
	_spawn_position = position
	hurtbox.hurt.connect(_on_hurt)
	attack_hitbox.source = self
	attack_hitbox.damage = attack_damage
	attack_hitbox.knockback = attack_knockback


func _physics_process(delta: float) -> void:
	if state == State.DEAD:
		return
	match state:
		State.IDLE:
			_process_idle()
		State.ALERT:
			_process_alert()
		State.ATTACK:
			_process_attack(delta)
		State.VULNERABLE:
			_process_vulnerable(delta)
	attack_hitbox.position.x = attack_hitbox_offset_x * facing
	_update_sprite()
	move_and_slide()


func _player_distance() -> float:
	var player := get_tree().get_first_node_in_group("player")
	if player == null:
		return INF
	return global_position.distance_to(player.global_position)


func _player_direction() -> Vector2:
	var player := get_tree().get_first_node_in_group("player")
	if player == null:
		return Vector2.ZERO
	return player.global_position - global_position


func _process_idle() -> void:
	_apply_gravity()
	if move_mode == "ground_patrol":
		_patrol()
	else:
		_sway()
	if _player_distance() <= detection_range:
		state = State.ALERT
		_state_timer = 0.0
		print("%s: alerta, detecta al jugador" % name)


func _process_alert() -> void:
	_apply_gravity()
	var dist := _player_distance()
	if move_mode == "ground_patrol":
		if dist > attack_range:
			var dir := signf(_player_direction().x)
			if dir != 0.0:
				facing = int(dir)
			velocity.x = dir * approach_speed
		else:
			velocity.x = 0.0
			_enter_attack()
			return
	else:
		_sway()
		if dist <= attack_range:
			_enter_attack()
			return
	if dist > detection_range * 1.5:
		state = State.IDLE


func _enter_attack() -> void:
	state = State.ATTACK
	_state_timer = 0.0
	print("%s: ataca" % name)
	if move_mode == "float_sway":
		AudioManager.play_sfx_random(SFX_WHOOSH, "SFX", -8.0, 0.14)
	else:
		AudioManager.play_sfx_random(SFX_SWING, "SFX", -7.0, 0.12)
	var player := get_tree().get_first_node_in_group("player")
	_lunge_target = player.global_position if player else global_position


func _process_attack(delta: float) -> void:
	_state_timer += delta
	_apply_gravity()
	var active := _state_timer >= attack_windup and _state_timer < attack_windup + attack_active_duration
	if active and not attack_hitbox.monitoring:
		attack_hitbox.activate()
		if move_mode == "float_sway":
			velocity = (_lunge_target - global_position).normalized() * lunge_speed
	elif not active and attack_hitbox.monitoring:
		attack_hitbox.deactivate()
	if not active and move_mode == "float_sway" and _state_timer >= attack_windup:
		velocity = velocity.move_toward(Vector2.ZERO, 600.0 * delta)
	if _state_timer >= attack_windup + attack_active_duration:
		attack_hitbox.deactivate()
		state = State.VULNERABLE
		_state_timer = 0.0
		print("%s: vulnerable" % name)


func _process_vulnerable(delta: float) -> void:
	_state_timer += delta
	_apply_gravity()
	velocity.x = move_toward(velocity.x, 0.0, 400.0 * delta)
	if _state_timer >= vulnerable_duration:
		state = State.ALERT if _player_distance() <= detection_range else State.IDLE
		_state_timer = 0.0


func _patrol() -> void:
	if move_mode != "ground_patrol":
		return
	var target_x := _spawn_position.x + _patrol_direction * patrol_distance
	velocity.x = _patrol_direction * patrol_speed
	if absf(position.x - target_x) < 4.0:
		_patrol_direction *= -1
	facing = _patrol_direction


func _sway() -> void:
	_sway_time += get_physics_process_delta_time()
	velocity = Vector2.ZERO
	global_position.y = _spawn_position.y + sin(_sway_time * sway_speed) * sway_amplitude


func _apply_gravity() -> void:
	if move_mode != "ground_patrol":
		return
	if not is_on_floor():
		velocity.y += gravity * get_physics_process_delta_time()
	else:
		velocity.y = 0.0


func _on_hurt(damage: int, direction: Vector2, knockback: float, stagger_time: float) -> void:
	if state == State.DEAD:
		return
	health = max(health - damage, 0)
	velocity = direction * knockback
	print("%s: recibe %d de daño (vida=%d/%d)" % [name, damage, health, max_health])
	AudioManager.play_sfx_random(SFX_IMPACT, "SFX", -3.0)
	if health <= 0:
		_die()


func _die() -> void:
	state = State.DEAD
	attack_hitbox.deactivate()
	# El cuerpo no se libera (queda como "cadaver" visual, coherente con
	# que la muerte no es un game over generico) pero deja de bloquear
	# fisicamente el paso -- sin esto, un enemigo derrotado en un pasillo
	# angosto (ej. Intro, Escena 4) deja al jugador trabado para siempre.
	collision_layer = 0
	collision_mask = 0
	sprite.play(anim_death)
	AudioManager.play_sfx_random(SFX_DEATH, "SFX", -4.0)
	print("%s: destruido" % name)


func _update_sprite() -> void:
	sprite.flip_h = facing < 0
	var target_anim := anim_idle
	match state:
		State.IDLE:
			target_anim = anim_idle
		State.ALERT:
			target_anim = anim_move
		State.ATTACK:
			target_anim = anim_attack
		State.VULNERABLE:
			target_anim = anim_vulnerable
	if sprite.animation != target_anim:
		sprite.play(target_anim)
