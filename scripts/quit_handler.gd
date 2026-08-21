extends Node

## Autoload: ESC (accion incorporada "ui_cancel") vuelve al menu principal
## desde cualquier escena de juego. Desde el titulo mismo no hace nada --
## ya tiene su propio boton "Salir" para cerrar el juego del todo.
## process_mode = ALWAYS para que funcione incluso con un dialogo abierto
## (arbol pausado).

const TITLE_SCENE := "res://scenes/ui/TitleScreen.tscn"


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS


func _process(_delta: float) -> void:
	if not Input.is_action_just_pressed("ui_cancel"):
		return
	var current := get_tree().current_scene
	if current == null:
		return
	if current.scene_file_path == TITLE_SCENE:
		return
	get_tree().paused = false
	TransitionManager.goto_scene(TITLE_SCENE)
