extends Area2D
class_name InteractableArea

## Base para objetos interactivos del mundo (Fase 7 de docs/AUDITORIA_2026-08-27.md).
##
## Extiende el patron ya usado por checkpoint.gd / dialogue_trigger.gd /
## memory_fragment.gd (Area2D + body_entered + already_active) con una capa
## de "apretar E para interactuar": mientras el jugador esta en rango se
## muestra un prompt, y recien al pulsar `interact` se dispara la accion.
##
## Diferencia clave con DialogueTrigger: los beats sensoriales ambientales
## SIGUEN siendo automaticos al cruzar (esta bien que lo sean). Esto es para
## lo que el brief pide como accion deliberada del jugador: reconocer un
## mecanismo, inspeccionar un cadaver, liberar un espiritu (brief SS 3 y 9).
##
## Uso: heredar y sobreescribir `_do_interact()`. La escena base
## `scenes/level/InteractableArea.tscn` trae el CollisionShape2D y el prompt.

signal interacted

## Se puede interactuar una sola vez (como los demas triggers del proyecto).
## Poner en false para mecanismos reutilizables.
@export var one_shot: bool = true
## Texto del prompt flotante. Vacio = sin prompt visible (interaccion silenciosa).
@export var prompt_text: String = "[E]"
@export var already_active: bool = false

var _player_in_range: bool = false

@onready var _prompt: Label = get_node_or_null("Prompt")


func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	if _prompt != null:
		_prompt.text = prompt_text
		_prompt.visible = false


func _process(_delta: float) -> void:
	if not _player_in_range or already_active:
		return
	if Input.is_action_just_pressed("interact"):
		_trigger()


func _on_body_entered(body: Node2D) -> void:
	if not body.is_in_group("player"):
		return
	if already_active:
		return
	_player_in_range = true
	_set_prompt_visible(true)


func _on_body_exited(body: Node2D) -> void:
	if not body.is_in_group("player"):
		return
	_player_in_range = false
	_set_prompt_visible(false)


func _trigger() -> void:
	if one_shot:
		already_active = true
	_player_in_range = false
	_set_prompt_visible(false)
	interacted.emit()
	_do_interact()


func _set_prompt_visible(v: bool) -> void:
	if _prompt != null and prompt_text != "":
		_prompt.visible = v


## Punto de extension: cada tipo concreto (RecognitionPoint, Corpse, etc.)
## define aca que pasa al interactuar. La base no hace nada por si sola.
func _do_interact() -> void:
	pass
