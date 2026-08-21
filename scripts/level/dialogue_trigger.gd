extends Area2D

## Disparador de dialogo reutilizable: mismo esqueleto que checkpoint.gd
## (Area2D + body_entered + already_active para no repetir). Las lineas se
## cargan por @export en cada instancia -- no hace falta un sistema de
## archivos de dialogo separado para unos pocos disparadores.

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
	DialogueBox.show_lines(lines)
