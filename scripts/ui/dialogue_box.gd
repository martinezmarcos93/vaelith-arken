extends CanvasLayer

## Autoload (Fase 9.3): caja de dialogo simple, sin retrato ni iconografia
## ("texto sobrio", Roadmap Fase 9.3). Pausa el arbol mientras esta activa
## -- por eso su propio process_mode es WHEN_PAUSED, para seguir recibiendo
## el input que la avanza aunque el resto del juego este congelado.

signal finished

@onready var _label: Label = $Panel/Label
@onready var _hint: Label = $Panel/Hint
@onready var _choices: VBoxContainer = $Panel/Choices

var _lines: Array[String] = []
var _index: int = 0
var _pending_choice: int = -1


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
	if not visible or _choices.visible:
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


## Muestra N botones y espera a que se elija uno -- para el momento del
## guerrero-espejo "Pregunta lo que quieras... elegi bien" (Despertar en
## la oscuridad.pdf, pag. 82-83): en la fuente esa pregunta nunca llega a
## responderse (la sesion de mesa termino ahi), asi que la eleccion real
## esta en QUE pregunta se hace, no en una respuesta distinta por opcion.
func ask_choice(options: Array[String]) -> int:
	visible = true
	get_tree().paused = true
	_label.text = ""
	_hint.visible = false
	for child in _choices.get_children():
		child.queue_free()
	# Ojo: una lambda de GDScript captura variables locales por valor, una
	# sola vez -- asignarle a una `var` local desde `pressed.connect(func...)`
	# nunca se ve reflejado afuera. Por eso esto usa una variable de
	# instancia (`_pending_choice`) en vez de una local capturada.
	_pending_choice = -1
	for i in options.size():
		var btn := Button.new()
		btn.text = options[i]
		btn.custom_minimum_size = Vector2(0, 36)
		btn.pressed.connect(func() -> void: _pending_choice = i)
		_choices.add_child(btn)
	_choices.visible = true
	await get_tree().process_frame
	_choices.get_child(0).grab_focus()
	while _pending_choice == -1:
		await get_tree().process_frame
	_choices.visible = false
	_hint.visible = true
	visible = false
	get_tree().paused = false
	return _pending_choice
