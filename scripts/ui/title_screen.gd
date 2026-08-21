extends Control

## Fase 9.2 - pantalla de titulo. "Iniciar partida" apunta a Level1.tscn
## hasta que exista Intro.tscn (paso 5 del plan de la demo completa) --
## actualizar START_SCENE cuando esa escena exista.

const START_SCENE := "res://scenes/levels/Level1.tscn"

@onready var _start_button: Button = $Center/VBox/StartButton
@onready var _quit_button: Button = $Center/VBox/QuitButton


func _ready() -> void:
	_start_button.pressed.connect(_on_start_pressed)
	_quit_button.pressed.connect(_on_quit_pressed)
	_start_button.grab_focus()


func _on_start_pressed() -> void:
	TransitionManager.goto_scene(START_SCENE)


func _on_quit_pressed() -> void:
	get_tree().quit()
