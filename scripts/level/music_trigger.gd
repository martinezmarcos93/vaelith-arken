extends Area2D

## Cambia el tema de música al cruzarlo el jugador (mismo esqueleto que
## scene_transition_trigger.gd). Reutilizable para cualquier cambio de música
## disparado por posición -- hoy: el tema del boss a la entrada de la arena.

@export_file("*.mp3", "*.ogg") var track_path: String = ""
@export var fade: float = 2.0
@export var volume_db: float = -6.0
@export var already_active: bool = false


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if already_active or not body.is_in_group("player"):
		return
	already_active = true
	AudioManager.play_music(track_path, fade, volume_db)
