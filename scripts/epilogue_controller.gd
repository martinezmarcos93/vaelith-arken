extends Control

## Etapa 7 - Epilogo, siguiendo los beats de docs/guion_desenlace.md:
## silencio post-combate, fragmento de memoria ampliado (mismo motivo de la
## intro + un elemento nuevo) y fundido lento a la pantalla de cierre. Todo
## el texto nuevo es cita literal de "Despertar en la oscuridad.pdf"
## (paginas 79-82, el mismo encuentro que origino al Boss 1) o el motivo ya
## establecido en Level1 ("Una mujer. Un trono. Calaveras. Una rueda.") --
## nada inventado. El guerrero-espejo no vuelve a hablar en persona: lo que
## sigue es lo que queda de el en la memoria de Vaelith, coherente con que
## el combate ya termino.

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
		"Una mujer.",
		"Un trono.",
		"Calaveras.",
		"Una rueda.",
		"\"Todavía hacés eso.\"",
		"\"Pero nunca aprendiste a terminar la finta.\"",
		"Tu cuerpo la reconoció.",
		"\"¿Tomás te contó lo que hizo?\"",
		"\"Tu padre no fue quien te mató, Vaelith.\"",
		"\"Pero sí fue quien decidió qué debía pasar con tu cuerpo después.\"",
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
