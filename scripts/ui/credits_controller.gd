extends Control

## Paso 9 del plan de demo - pantalla de creditos. Lista solo el arte que
## esta realmente en uso en la build jugable (no el catalogo completo de
## CREDITS.md, que incluye candidatos evaluados y descartados).

const TITLE_SCENE := "res://scenes/ui/TitleScreen.tscn"

@onready var _back_button: Button = $Center/VBox/BackButton


func _ready() -> void:
	_back_button.pressed.connect(_on_back_pressed)
	_back_button.grab_focus()


func _on_back_pressed() -> void:
	TransitionManager.goto_scene(TITLE_SCENE)
