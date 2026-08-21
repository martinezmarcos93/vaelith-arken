extends CanvasLayer

## Autoload (Fase 9.3): caja de dialogo simple, sin retrato ni iconografia
## ("texto sobrio", Roadmap Fase 9.3). Pausa el arbol mientras esta activa
## -- por eso su propio process_mode es WHEN_PAUSED, para seguir recibiendo
## el input que la avanza aunque el resto del juego este congelado.

signal finished

@onready var _label: Label = $Panel/Label

var _lines: Array[String] = []
var _index: int = 0


func _ready() -> void:
	visible = false
	process_mode = Node.PROCESS_MODE_WHEN_PAUSED


func show_lines(lines: Array[String]) -> void:
	if lines.is_empty():
		finished.emit()
		return
	_lines = lines
	_index = 0
	visible = true
	get_tree().paused = true
	_display_current()


func _display_current() -> void:
	_label.text = _lines[_index]


func _process(_delta: float) -> void:
	if not visible:
		return
	if Input.is_action_just_pressed("interact"):
		_advance()


func _advance() -> void:
	_index += 1
	if _index >= _lines.size():
		_close()
		return
	_display_current()


func _close() -> void:
	visible = false
	get_tree().paused = false
	finished.emit()
