extends Area2D

## Coleccionable de puntaje (no es inventario -- GDD.md lo excluye, esto
## solo suma a un contador visible en el HUD). Mismo esqueleto Area2D +
## body_entered + already_active que Checkpoint/DialogueTrigger/
## MemoryFragment, pero este SI se libera al recogerse (no queda como
## marcador invisible, es un pickup de un solo uso que desaparece).

@export var already_active: bool = false

func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if already_active:
		return
	if not body.is_in_group("player"):
		return
	already_active = true
	GameState.collect_skull()
	AudioManager.play_sfx("res://assets/audio/sfx/world/stone_impact_01.ogg", "SFX", -8.0)
	queue_free()
