extends Control

## Etapa 7 - Epilogo, siguiendo los beats de docs/guion_desenlace.md:
## silencio post-combate, fragmento de memoria y fundido lento a la
## pantalla de cierre. El guerrero-espejo ya dijo lo suyo en persona en
## Level1 (level1_controller.gd) justo al rendirse -- este fragmento no
## repite esas lineas, sigue el hilo de Vaelith mismo: no tiene respuesta
## a por que fue condenado, pero sabe que algun dia la va a tener. Cita
## literal de "Vaelith Arken -- Registro del Osario.pdf" (pag. 4-5).

const CREDITS_SCENE := "res://scenes/ui/Credits.tscn"
## El "silencio total" post-combate (2-3s) ya lo espera Level1 mirando al
## boss caido, antes de disparar la transicion -- esta pausa corta es solo
## para dejar asentar el fundido de entrada, no repetir el beat.
const SETTLE_DURATION := 0.4
const FADE_DURATION := 2.5

@onready var closing_label: Label = $ClosingLabel
@onready var hint_label: Label = $Hint

var _closing_shown: bool = false
var _returning: bool = false


func _ready() -> void:
	closing_label.visible = false
	hint_label.visible = false
	await get_tree().create_timer(SETTLE_DURATION).timeout
	DialogueBox.finished.connect(_on_dialogue_finished, CONNECT_ONE_SHOT)
	DialogueBox.show_lines([
		"No lo sé.",
		"Y era cierto.",
		"Vaelith todavía no sabía qué había hecho para merecer semejante condena.",
		"Pero algún día lo descubriría.",
		"Y cuando ese momento llegara, tendría que decidir qué hacer con la verdad.",
	])


func _on_dialogue_finished() -> void:
	GameState.collect_memory()
	await TransitionManager.fade_out(FADE_DURATION)
	closing_label.visible = true
	hint_label.visible = true
	await TransitionManager.fade_in(FADE_DURATION)
	_closing_shown = true


func _process(_delta: float) -> void:
	if _closing_shown and not _returning and Input.is_action_just_pressed("interact"):
		_returning = true
		TransitionManager.goto_scene(CREDITS_SCENE)
