extends Area2D

## Fase 4.3 - trigger de checkpoint. Al ser tocado por el jugador, actualiza
## su punto de respawn (player.gd: set_checkpoint). No implementa la
## corrupcion de nivel de "penitencia" (docs/stats_personaje.md) -- eso
## depende de tener tramos reales con dificultad ajustable, fuera de
## alcance hasta que exista Level 1 completo.

@export var already_active: bool = false

func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if already_active:
		return
	if not body.is_in_group("player"):
		return
	already_active = true
	body.set_checkpoint(global_position)
	print("Checkpoint activado en %s" % global_position)
