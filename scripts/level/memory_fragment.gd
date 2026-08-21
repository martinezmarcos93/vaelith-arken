extends Area2D

## Pickup de fragmento de memoria: mismo esqueleto que checkpoint.gd y
## dialogue_trigger.gd (Area2D + body_entered + already_active). Al
## tocarlo registra el progreso en GameState y muestra el recuerdo con
## DialogueBox -- el texto sale de "Ideas base para el juego/Despertar en
## la oscuridad.pdf", no se inventa.

@export var lines: Array[String] = []
@export var already_active: bool = false

func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if already_active:
		return
	if not body.is_in_group("player"):
		return
	already_active = true
	GameState.collect_memory()
	DialogueBox.show_lines(lines)
