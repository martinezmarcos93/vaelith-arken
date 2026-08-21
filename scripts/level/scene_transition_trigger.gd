extends Area2D

## Disparador de cambio de escena: mismo esqueleto que checkpoint.gd /
## dialogue_trigger.gd / memory_fragment.gd (Area2D + body_entered +
## already_active). Reutilizable en cualquier borde de nivel (Intro ->
## Level1, y mas adelante lo que siga tras el Boss).

@export var target_scene: String = ""
@export var already_active: bool = false

func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if already_active:
		return
	if not body.is_in_group("player"):
		return
	if target_scene == "":
		return
	already_active = true
	TransitionManager.goto_scene(target_scene)
