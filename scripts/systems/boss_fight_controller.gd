extends Node2D
class_name BossFightController

## P0-06 (docs/AUDITORIA_TECNICA_2026-09-09 §3): convierte la llegada a la arena
## del Guerrero-Espejo en un "evento de boss" inequívoco, sin tocar boss1.gd
## salvo begin_fight(). Este nodo orquesta:
##   entrar a la arena -> LOCK (pared invisible + límites de cámara a la arena)
##   -> línea de intro -> revelar la BossBar -> música de boss -> begin_fight()
##
## boss1.gd sigue emitiendo surrendered/phase_changed/health_changed y
## level1_controller.gd sigue manejando el post-rendición (recuerdo -> epílogo).
## Este controller sólo maneja la entrada.
##
## Reemplaza a los antiguos BossMusicTrigger + BossIntroTrigger (que quedan
## desactivados con already_active=true en Level1.tscn).

signal boss_intro_started
signal boss_fight_started

@export var trigger_x: float = 3280.0
@export var trigger_width: float = 48.0
@export var arena_left: float = 3010.0
@export var arena_right: float = 3680.0
@export var arena_top: float = -200.0
@export var arena_bottom: float = 700.0
@export var intro_lines: Array[String] = []
@export_file("*.mp3", "*.ogg") var boss_music: String = ""
@export var music_fade: float = 1.5
@export var music_db: float = -5.0
## Beat entre que termina la línea de intro y el boss empieza a moverse.
@export var pre_fight_beat: float = 0.6

var _started: bool = false


func _ready() -> void:
	add_to_group("boss_fight_controller")
	var area := Area2D.new()
	area.name = "TriggerArea"
	var cs := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = Vector2(trigger_width, arena_bottom - arena_top)
	cs.shape = shape
	area.add_child(cs)
	area.position = Vector2(trigger_x, (arena_top + arena_bottom) * 0.5) - global_position
	add_child(area)
	area.body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if _started or not body.is_in_group("player"):
		return
	_started = true
	_begin()


func _begin() -> void:
	boss_intro_started.emit()

	# 1. Pared invisible en la entrada: el jugador ya no puede volver atrás.
	var wall := StaticBody2D.new()
	wall.name = "ArenaEntranceWall"
	var wcs := CollisionShape2D.new()
	var wshape := RectangleShape2D.new()
	wshape.size = Vector2(16.0, arena_bottom - arena_top)
	wcs.shape = wshape
	wall.add_child(wcs)
	wall.global_position = Vector2(arena_left, (arena_top + arena_bottom) * 0.5)
	get_parent().add_child(wall)

	# 2. Límites de cámara a la arena (encierra el encuadre en el combate).
	var cam := _player_camera()
	if cam != null:
		cam.limit_left = int(arena_left)
		cam.limit_right = int(arena_right)

	# 3. Música del boss (antes lo hacía BossMusicTrigger).
	if boss_music != "":
		AudioManager.play_music(boss_music, music_fade, music_db)

	# 4. Revelar la BossBar (antes se mostraba al cargar el nivel).
	var hud := get_tree().get_first_node_in_group("hud")
	if hud != null and hud.has_method("reveal_boss_bar"):
		hud.reveal_boss_bar()

	# 5. Línea de intro; la pelea arranca al terminar.
	if intro_lines.is_empty():
		_start_fight()
	else:
		DialogueBox.finished.connect(_start_fight, CONNECT_ONE_SHOT)
		DialogueBox.show_lines(intro_lines)


func _start_fight() -> void:
	await get_tree().create_timer(pre_fight_beat, true).timeout
	var boss := get_tree().get_first_node_in_group("boss")
	if boss != null and boss.has_method("begin_fight"):
		boss.begin_fight()
	boss_fight_started.emit()


func _player_camera() -> Camera2D:
	var p := get_tree().get_first_node_in_group("player")
	return p.get_node_or_null("Camera2D") if p != null else null
