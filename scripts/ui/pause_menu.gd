extends CanvasLayer

## Autoload: ESC (accion incorporada "ui_cancel") pausa el juego con un
## menu simple (Continuar / Menu principal) en vez de mandar directo al
## titulo -- antes ESC perdia la partida en curso sin dar opcion de
## seguir jugando (a pedido de Marcos). process_mode ALWAYS porque tiene
## que reaccionar a ESC tanto para abrir (juego corriendo, sin pausar)
## como para cerrar (ya pausado por este mismo menu).

const TITLE_SCENE := "res://scenes/ui/TitleScreen.tscn"
const CREDITS_SCENE := "res://scenes/ui/Credits.tscn"

@onready var _continue_button: TextureButton = $Center/Panel/VBox/ContinueButton
@onready var _title_button: TextureButton = $Center/Panel/VBox/TitleButton


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	_continue_button.pressed.connect(_on_continue_pressed)
	_title_button.pressed.connect(_on_title_pressed)


func _process(_delta: float) -> void:
	if not Input.is_action_just_pressed("ui_cancel"):
		return
	if visible:
		_close()
		return
	_try_open()


func _try_open() -> void:
	# No se abre encima de un dialogo (ya tiene su propia pausa/su propio
	# uso de "avanzar") ni en el titulo o los creditos (no hay partida que
	# pausar en ninguna pantalla de menu).
	if DialogueBox.visible:
		return
	var current := get_tree().current_scene
	if current == null:
		return
	if current.scene_file_path == TITLE_SCENE or current.scene_file_path == CREDITS_SCENE:
		return
	visible = true
	get_tree().paused = true
	_continue_button.grab_focus()


func _close() -> void:
	visible = false
	get_tree().paused = false


func _on_continue_pressed() -> void:
	_close()


func _on_title_pressed() -> void:
	_close()
	TransitionManager.goto_scene(TITLE_SCENE)
