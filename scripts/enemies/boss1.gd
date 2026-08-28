extends CharacterBody2D

## Boss 1 "El Guerrero-Espejo" (docs/diseno_boss1.md, Fase 6.1-6.4).
## Concepto central del documento: "imita, no inventa" -- sus ataques son
## versiones espejadas del kit de Vaelith, con el MISMO daño/knockback/
## logica de guardia rota que player.gd, no un moveset inventado. Arte
## propio (espejo_boss_custom, re-extraido de spectral_knight_violet_sheet).

## Por guion (docs/guion_demo.md, "BOSS -- EL ESPEJO") el guerrero-espejo
## NO muere: al llegar a 0 de vida se RINDE (baja la guardia, deja de
## atacar) y da paso al recuerdo "El ultimo dia" -- ver _surrender().
signal surrendered
signal health_changed(current: int, max_health: int)
signal phase_changed(new_phase: int)

enum Phase { ONE, TWO }
enum State { APPROACH, ATTACK_HIGH, ATTACK_LOW, SHOVE, BLOCK, VULNERABLE, TRANSITIONING, SURRENDERED }

@export_group("Vida")
## ~4x la vida de Vaelith (docs/diseno_boss1.md: "20 HP equivalentes a
## golpes de attack_high", proporcional a player.gd max_health=5).
@export var max_health: int = 20
@export var phase_two_threshold: float = 0.5

@export_group("Movimiento")
@export var approach_speed: float = 60.0
@export var attack_range: float = 70.0
@export var gravity: float = 1400.0

@export_group("Combate (mismo daño que Vaelith se hace a si mismo)")
@export var attack_high_damage: int = 2
@export var attack_low_damage: int = 1
@export var shove_knockback: float = 300.0
@export var shove_stagger_time: float = 0.6
@export var attack_hitbox_offset_x: float = 20.0

@export_group("Guardia especular")
## Mismo umbral que player.gd (block_max_consecutive=3): se rompe al 4to
## golpe bloqueado seguido.
@export var block_max_consecutive: int = 3
@export var block_stagger_time: float = 0.8
@export var block_duration: float = 1.2

@export_group("Telegrafiado Fase 1")
## Brillo rojo en el filo 0.5s antes (tajo alto) / se agacha 0.4s antes
## (tajo bajo) -- ver _update_telegraph_visual(). Ventanas de punicion
## despues del golpe: nunca encadena dos ataques sin esa ventana
## (docs/diseno_enemigos.md, misma regla que los enemigos regulares).
@export var telegraph_high: float = 0.5
@export var telegraph_low: float = 0.4
@export var active_duration: float = 0.15
@export var punish_window_high: float = 0.7
@export var punish_window_low: float = 0.6

@export_group("Fase 2 - el espejo se rompe")
## Telegrafiado 30% mas corto: el espejo "aprendio" el ritmo del jugador.
@export var telegraph_speedup_phase_two: float = 0.7
@export var transition_invuln_time: float = 1.0
@export var shove_chance_phase_two: float = 0.25

@export_group("Animacion")
## Arte propio: assets/sprites/enemies/espejo_boss_custom/_frames.tres,
## extraido de source_sheets/characters/boss/spectral_knight_violet_sheet.png
## (Fase 1 de la auditoria). Todas las acciones tienen animacion propia.
@export var anim_idle: String = "idle"
@export var anim_move: String = "run"
@export var anim_attack_high: String = "attack1"
@export var anim_attack_low: String = "attack2"
@export var anim_shove: String = "shove"
@export var anim_block: String = "block"
@export var anim_hurt: String = "hurt"
@export var anim_stagger: String = "stagger"
@export var anim_surrender: String = "idle"

@onready var attack_high_hitbox: Hitbox = $AttackHighHitbox
@onready var attack_low_hitbox: Hitbox = $AttackLowHitbox
@onready var shove_hitbox: Hitbox = $ShoveHitbox
@onready var hurtbox: Hurtbox = $Hurtbox
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D

# --- Audio (ver docs/lista_audio.md §4). Los momentos 🔴 (mascara se agrieta,
# rendicion) usan placeholders hasta tener los SFX custom. ---
const SFX_SWING := ["res://assets/audio/sfx/combat/sword_swing_01.ogg", "res://assets/audio/sfx/combat/sword_swing_02.ogg", "res://assets/audio/sfx/combat/sword_swing_03.ogg"]
const SFX_WHOOSH := ["res://assets/audio/sfx/player/whoosh_01.wav", "res://assets/audio/sfx/player/whoosh_02.wav"]
const SFX_TELEGRAPH := "res://assets/audio/sfx/combat/telegraph_ring_01.wav"
const SFX_BLOCK := ["res://assets/audio/sfx/combat/blade_clash_01.wav", "res://assets/audio/sfx/combat/blade_clash_02.wav"]
const SFX_IMPACT := ["res://assets/audio/sfx/combat/impact_flesh_01.ogg", "res://assets/audio/sfx/combat/impact_flesh_02.ogg", "res://assets/audio/sfx/combat/impact_flesh_03.ogg"]
const SFX_TRANSITION := "res://assets/audio/sfx/combat/blade_ring_01.wav"
const SFX_SURRENDER := "res://assets/audio/sfx/combat/blade_clash_01.wav"

var phase: Phase = Phase.ONE
var state: State = State.APPROACH
var health: int
var facing: int = -1

var _state_timer: float = 0.0
var _vulnerable_duration: float = 0.6
var _consecutive_blocks: int = 0
var _arena_center_x: float
var _rng := RandomNumberGenerator.new()


func _ready() -> void:
	add_to_group("enemy")
	add_to_group("boss")
	health = max_health
	_arena_center_x = global_position.x
	hurtbox.hurt.connect(_on_hurt)
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
	health_changed.emit(health, max_health)


func _physics_process(delta: float) -> void:
	if state == State.SURRENDERED:
		return
	if not is_on_floor():
		velocity.y += gravity * delta
	else:
		velocity.y = 0.0

	match state:
		State.APPROACH:
			_process_approach()
		State.ATTACK_HIGH:
			_process_attack(delta, attack_high_hitbox, _telegraph(telegraph_high), punish_window_high)
		State.ATTACK_LOW:
			_process_attack(delta, attack_low_hitbox, _telegraph(telegraph_low), punish_window_low)
		State.SHOVE:
			_process_attack(delta, shove_hitbox, _telegraph(telegraph_low), punish_window_low)
		State.BLOCK:
			_process_block(delta)
		State.VULNERABLE:
			_process_vulnerable(delta)
		State.TRANSITIONING:
			_process_transition(delta)

	_update_hitbox_facing()
	_update_telegraph_visual()
	_update_sprite()
	move_and_slide()


func _telegraph(base: float) -> float:
	return base * telegraph_speedup_phase_two if phase == Phase.TWO else base


func _player() -> Node2D:
	return get_tree().get_first_node_in_group("player")


func _process_approach() -> void:
	var player := _player()
	if player == null:
		velocity.x = 0.0
		return
	var to_player: Vector2 = player.global_position - global_position
	var dist := to_player.length()
	if dist > attack_range:
		var dir := signf(to_player.x)
		if dir != 0.0:
			facing = int(dir)
		velocity.x = dir * approach_speed
		return
	velocity.x = 0.0
	_choose_action()


## Fase 1: tajo alto / tajo bajo / guardia especular, en ese orden de
## probabilidad. Fase 2 suma la embestida especular (docs/diseno_boss1.md:
## "sin ataque nuevo inventado" -- deliberado, solo se agrega velocidad y
## esta variante extra sobre el mismo kit de 4 acciones).
func _choose_action() -> void:
	var roll := _rng.randf()
	if phase == Phase.TWO and roll < shove_chance_phase_two:
		_enter_action(State.SHOVE)
		return
	if roll < 0.45:
		_enter_action(State.ATTACK_HIGH)
	elif roll < 0.8:
		_enter_action(State.ATTACK_LOW)
	else:
		_enter_block()


func _enter_action(new_state: State) -> void:
	state = new_state
	_state_timer = 0.0
	velocity.x = 0.0
	match new_state:
		State.ATTACK_HIGH:
			AudioManager.play_sfx(SFX_TELEGRAPH, "SFX", -10.0)
			AudioManager.play_sfx_random(SFX_SWING, "SFX", -5.0)
		State.ATTACK_LOW:
			AudioManager.play_sfx_random(SFX_SWING, "SFX", -6.0)
		State.SHOVE:
			AudioManager.play_sfx_random(SFX_WHOOSH, "SFX", -5.0)


func _process_attack(delta: float, hitbox: Hitbox, windup: float, punish: float) -> void:
	_state_timer += delta
	var active_end := windup + active_duration
	var should_be_active := _state_timer >= windup and _state_timer < active_end
	if should_be_active and not hitbox.monitoring:
		hitbox.activate()
	elif not should_be_active and hitbox.monitoring:
		hitbox.deactivate()
	if _state_timer >= active_end:
		hitbox.deactivate()
		state = State.VULNERABLE
		_state_timer = 0.0
		_vulnerable_duration = punish


func _process_vulnerable(delta: float) -> void:
	_state_timer += delta
	velocity.x = 0.0
	if _state_timer >= _vulnerable_duration:
		state = State.APPROACH
		_state_timer = 0.0


func _enter_block() -> void:
	state = State.BLOCK
	_state_timer = 0.0
	_consecutive_blocks = 0
	velocity.x = 0.0


func _process_block(delta: float) -> void:
	_state_timer += delta
	velocity.x = 0.0
	if _state_timer >= block_duration:
		state = State.APPROACH
		_state_timer = 0.0


func _on_hurt(damage: int, direction: Vector2, knockback: float, stagger_time: float) -> void:
	if state == State.SURRENDERED or state == State.TRANSITIONING:
		return
	if state == State.BLOCK and damage > 0 and _is_frontal_hit(direction):
		_register_block()
		return
	_take_damage(damage, direction, knockback, stagger_time)


## Mismo criterio que player.gd: la guardia especular solo cubre el frente,
## un golpe que le llega por la espalda (mismo lado que facing) no bloquea.
func _is_frontal_hit(direction: Vector2) -> bool:
	var attack_side := signf(direction.x)
	return attack_side == 0.0 or int(attack_side) != facing


func _register_block() -> void:
	AudioManager.play_sfx_random(SFX_BLOCK, "SFX", -4.0)
	_consecutive_blocks += 1
	if _consecutive_blocks > block_max_consecutive:
		_consecutive_blocks = 0
		state = State.VULNERABLE
		_state_timer = 0.0
		_vulnerable_duration = block_stagger_time
		print("Guerrero-Espejo: postura rota tras bloquear %d golpes seguidos" % block_max_consecutive)


func _take_damage(damage: int, direction: Vector2, knockback: float, stagger_time: float) -> void:
	health = max(health - damage, 0)
	health_changed.emit(health, max_health)
	velocity = direction * knockback
	print("Guerrero-Espejo: recibe %d de daño (vida=%d/%d)" % [damage, health, max_health])
	AudioManager.play_sfx_random(SFX_IMPACT, "SFX", -3.0)
	if health <= 0:
		_surrender()
		return
	if phase == Phase.ONE and float(health) / float(max_health) <= phase_two_threshold:
		_enter_transition()
		return
	# Un golpe con stagger_time (ej. la Embestida del jugador) rompe
	# cualquier accion en curso -- mismo trato que la guardia rota, ver
	# _register_block().
	if stagger_time > 0.0:
		attack_high_hitbox.deactivate()
		attack_low_hitbox.deactivate()
		shove_hitbox.deactivate()
		state = State.VULNERABLE
		_state_timer = 0.0
		_vulnerable_duration = stagger_time


func _enter_transition() -> void:
	state = State.TRANSITIONING
	_state_timer = 0.0
	attack_high_hitbox.deactivate()
	attack_low_hitbox.deactivate()
	shove_hitbox.deactivate()
	# Placeholder: "la mascara se agrieta" es un momento 🔴 custom pendiente.
	AudioManager.play_sfx(SFX_TRANSITION, "SFX", 2.0, 0.0)
	print("Guerrero-Espejo: la mascara se agrieta -- fase 2")


func _process_transition(delta: float) -> void:
	_state_timer += delta
	velocity.x = move_toward(velocity.x, 0.0, 400.0 * delta)
	if absf(global_position.x - _arena_center_x) > 4.0:
		velocity.x = signf(_arena_center_x - global_position.x) * approach_speed
	if _state_timer >= transition_invuln_time:
		phase = Phase.TWO
		phase_changed.emit(phase)
		state = State.APPROACH
		_state_timer = 0.0


func _surrender() -> void:
	state = State.SURRENDERED
	attack_high_hitbox.deactivate()
	attack_low_hitbox.deactivate()
	shove_hitbox.deactivate()
	velocity = Vector2.ZERO
	# A diferencia de enemy_regular.gd, el boss NO muere (ver comentario en
	# el enum State): sigue de pie, la colision queda solida a proposito.
	sprite.play(anim_surrender)
	sprite.modulate = Color(0.6, 0.6, 0.6, 1.0)
	# Placeholder: el arma cayendo (metal contra piedra). El silencio total
	# posterior lo maneja level1_controller (stop_music). SFX 🔴 custom pendiente.
	AudioManager.play_sfx(SFX_SURRENDER, "SFX", 3.0, 0.0)
	print("Guerrero-Espejo: se rinde, baja el arma")
	surrendered.emit()


func _update_hitbox_facing() -> void:
	attack_high_hitbox.position.x = attack_hitbox_offset_x * facing
	attack_low_hitbox.position.x = attack_hitbox_offset_x * facing
	shove_hitbox.position.x = (attack_hitbox_offset_x + 4.0) * facing


## "brillo rojo en el filo, 0.5s antes del golpe" (tajo alto) --
## placeholder sin frame de animacion dedicado: se logra con un tinte
## de color sobre el sprite entero durante el windup.
func _update_telegraph_visual() -> void:
	if state == State.ATTACK_HIGH and _state_timer < _telegraph(telegraph_high):
		sprite.modulate = Color(1.0, 0.4, 0.4)
	else:
		sprite.modulate = Color(1.0, 1.0, 1.0)


func _update_sprite() -> void:
	sprite.flip_h = facing < 0
	var target_anim := anim_idle
	match state:
		State.APPROACH:
			target_anim = anim_move if absf(velocity.x) > 5.0 else anim_idle
		State.ATTACK_HIGH:
			target_anim = anim_attack_high
		State.ATTACK_LOW:
			target_anim = anim_attack_low
		State.SHOVE:
			target_anim = anim_shove
		State.BLOCK:
			target_anim = anim_block
		State.VULNERABLE:
			target_anim = anim_stagger
		State.TRANSITIONING:
			target_anim = anim_idle
	if sprite.animation != target_anim:
		sprite.play(target_anim)
