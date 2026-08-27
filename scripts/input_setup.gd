extends Node

## Autoload que define el input map por código en vez de editar a mano el
## bloque [input] de project.godot (mas seguro de mantener correcto).
## Referencia de controles: docs/GDD.md seccion 5.

func _ready() -> void:
	# (El puntero del SO se reemplaza por el cursor propio -- ver
	# scripts/cursor_manager.gd. Antes acá se ocultaba con MOUSE_MODE_HIDDEN.)
	_ensure_action("move_left", [KEY_A, KEY_LEFT])
	_ensure_action("move_right", [KEY_D, KEY_RIGHT])
	_ensure_action("jump", [KEY_SPACE])
	_ensure_action("attack_high", [KEY_J])
	_ensure_action("attack_low", [KEY_K])
	_ensure_action("block", [KEY_L])
	_ensure_action("shove", [KEY_I])
	_ensure_action("interact", [KEY_E])


func _ensure_action(action_name: String, keys: Array) -> void:
	if not InputMap.has_action(action_name):
		InputMap.add_action(action_name)
	for key in keys:
		var ev := InputEventKey.new()
		ev.physical_keycode = key
		if not _action_has_key(action_name, key):
			InputMap.action_add_event(action_name, ev)


func _action_has_key(action_name: String, keycode: int) -> bool:
	for ev in InputMap.action_get_events(action_name):
		if ev is InputEventKey and ev.physical_keycode == keycode:
			return true
	return false
