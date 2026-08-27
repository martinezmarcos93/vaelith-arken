extends Control

## Fase 9.2 - pantalla de titulo. "Iniciar partida" arranca la Intro.

const START_SCENE := "res://scenes/levels/Intro.tscn"

@onready var _start_button: TextureButton = $Center/VBox/StartButton
@onready var _quit_button: TextureButton = $Center/VBox/QuitButton


const MENU_MUSIC := "res://assets/audio/music/intro.mp3"


func _ready() -> void:
	_start_button.pressed.connect(_on_start_pressed)
	_quit_button.pressed.connect(_on_quit_pressed)
	_start_button.grab_focus()
	# Tema de intro en volumen bajo bajo el menú; la Intro en sí arranca en
	# silencio (guion), asi que intro_controller lo corta al cargar.
	AudioManager.play_music(MENU_MUSIC, 2.0, -14.0)


const SFX_CONFIRM := "res://assets/audio/sfx/world/lock_unlock.ogg"


func _on_start_pressed() -> void:
	AudioManager.play_sfx(SFX_CONFIRM, "UI", -6.0, 0.0)
	TransitionManager.goto_scene(START_SCENE)


func _on_quit_pressed() -> void:
	get_tree().quit()
