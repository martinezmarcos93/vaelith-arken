extends Control

## Rework narrativo (docs/guion_demo.md) -- "Regreso al presente" + pantalla
## de cierre.
##
## El recuerdo "El ultimo dia" y su collect_memory() ya ocurrieron en
## level1_controller.gd al caer el boss; aca Vaelith vuelve en si y ata el
## cabo: el guerrero-espejo era una criatura suya, a la que Pharasma le
## quito la memoria de quien era. Cierre en tres tiempos sobre negro:
## "La deuda continua." -> "VAELITH ARKEN" -> "El muerto recuerda."

const CREDITS_SCENE := "res://scenes/ui/Credits.tscn"
const SETTLE_DURATION := 0.4
const FADE_DURATION := 2.5
const DEBT_HOLD := 3.0

@onready var closing_label: Label = $ClosingLabel
@onready var title_label: Label = $TitleLabel
@onready var sub_label: Label = $SubLabel
@onready var hint_label: Label = $Hint

var _closing_shown: bool = false
var _returning: bool = false


func _ready() -> void:
	# El epílogo va sin música (guion: fundido lento, sin música nueva).
	AudioManager.stop_music(2.0)
	closing_label.visible = false
	title_label.visible = false
	sub_label.visible = false
	hint_label.visible = false
	await get_tree().create_timer(SETTLE_DURATION).timeout
	DialogueBox.finished.connect(_on_dialogue_finished, CONNECT_ONE_SHOT)
	DialogueBox.show_lines([
		"Volvés en vos. El constructo yace frente a vos.",
		"No lo entendés del todo. Pero entendés algo.",
		"El guerrero no era un enemigo desconocido. Era una parte de vos.",
		"Una criatura que creaste.",
		"Algo a lo que le diste lo que Pharasma después te quitó: tu memoria de quién eras.",
		"El constructo todavía lo recuerda.",
		"—Ahora sí me recordaste.",
		"—No a mí.",
		"—A vos.",
	])


func _on_dialogue_finished() -> void:
	await TransitionManager.fade_out(FADE_DURATION)
	closing_label.visible = true
	await TransitionManager.fade_in(FADE_DURATION)
	await get_tree().create_timer(DEBT_HOLD).timeout
	closing_label.visible = false
	title_label.visible = true
	sub_label.visible = true
	hint_label.visible = true
	_closing_shown = true


func _process(_delta: float) -> void:
	if _closing_shown and not _returning and Input.is_action_just_pressed("interact"):
		_returning = true
		TransitionManager.goto_scene(CREDITS_SCENE)
