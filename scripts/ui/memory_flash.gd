extends CanvasLayer

## Autoload. Tratamiento visual de los fragmentos de memoria (brief §6: los
## recuerdos deben sentirse como "escenas breves, traumaticas, fragmentarias",
## no como texto informativo).
##
## Escucha GameState.memory_collected -> un flash palido corto + un tirON de
## color frio que "drena" el mundo un instante, justo antes de que
## DialogueBox muestre el recuerdo. Como todos los caminos que revelan una
## memoria terminan en GameState.collect_memory() (MemoryFragment,
## RecognitionPoint, level1_controller "El ultimo dia"), el efecto sale
## gratis en todos.
##
## process_mode ALWAYS: DialogueBox pausa el arbol al mostrar el recuerdo,
## el tween tiene que seguir corriendo igual.

@onready var _flash: ColorRect = $Flash
@onready var _drain: ColorRect = $Drain


func _ready() -> void:
	layer = 88  # debajo de DialogueBox (90): el texto del recuerdo va encima
	process_mode = Node.PROCESS_MODE_ALWAYS
	_flash.color.a = 0.0
	_drain.color.a = 0.0
	GameState.memory_collected.connect(_on_memory_collected)


func _on_memory_collected(_total: int) -> void:
	flash()


## Publico: para disparar el efecto sin pasar por GameState (ej. un recuerdo
## que no cuenta como coleccionable). Dos tweens independientes que corren
## a la vez: el flash palido rapido y el drenaje de color mas largo.
func flash() -> void:
	var f := create_tween()
	f.tween_property(_flash, "color:a", 0.6, 0.07)
	f.tween_property(_flash, "color:a", 0.0, 0.55)
	var d := create_tween()
	d.tween_property(_drain, "color:a", 0.34, 0.12)
	d.tween_property(_drain, "color:a", 0.0, 0.95)
	# Sting frío placeholder (ring metálico grave). El jingle de memoria es
	# 🔴 custom pendiente, ver docs/lista_audio.md §5.
	AudioManager.play_sfx("res://assets/audio/sfx/combat/telegraph_ring_01.wav", "UI", -4.0, 0.0)
