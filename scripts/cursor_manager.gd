extends Node

## Autoload. Cursor de mouse propio (arte de Marcos, Puntero.png ->
## assets/sprites/ui/cursor/). Reemplaza al puntero del SO -- es la respuesta
## de presentación al bug 22 del informe visual (un cursor temático, no la
## flecha blanca del sistema).
##
## Godot cambia solo entre shapes: CURSOR_ARROW por defecto, CURSOR_POINTING_HAND
## al pasar por un Button/TextureButton (usan mouse_default_cursor_shape),
## CURSOR_WAIT/BUSY durante cargas. Los cursores de estado (interactuable /
## enemigo / no disponible) quedan extraídos para usarlos más adelante con
## set_context() cuando exista hover sobre InteractableArea / enemigos.

const DIR := "res://assets/sprites/ui/cursor/"

var _context: Dictionary = {}


func _ready() -> void:
	# El cursor custom sólo se ve con el mouse visible.
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

	var arrow: Texture2D = load(DIR + "normal.png")
	var hover: Texture2D = load(DIR + "hover.png")
	var busy: Texture2D = load(DIR + "busy.png")
	var cross: Texture2D = load(DIR + "precision.png")

	# hotspot = punto de click. La flecha apunta arriba-izquierda -> cerca de
	# la punta; cruz y reloj -> al centro.
	Input.set_custom_mouse_cursor(arrow, Input.CURSOR_ARROW, Vector2(5, 4))
	Input.set_custom_mouse_cursor(hover, Input.CURSOR_POINTING_HAND, Vector2(7, 4))
	Input.set_custom_mouse_cursor(busy, Input.CURSOR_WAIT, Vector2(busy.get_width() * 0.5, busy.get_height() * 0.5))
	Input.set_custom_mouse_cursor(busy, Input.CURSOR_BUSY, Vector2(busy.get_width() * 0.5, busy.get_height() * 0.5))
	Input.set_custom_mouse_cursor(cross, Input.CURSOR_CROSS, Vector2(cross.get_width() * 0.5, cross.get_height() * 0.5))

	_context = {
		"interact": load(DIR + "interact.png"),
		"enemy": load(DIR + "enemy.png"),
		"blocked": load(DIR + "blocked.png"),
		"click": load(DIR + "click.png"),
	}


## Fuerza un cursor de contexto ("interact" / "enemy" / "blocked" / "" para
## volver al normal). Para engancharse a hover de InteractableArea, enemigos,
## etc. cuando esa capa exista.
func set_context(state: String) -> void:
	if state == "" or not _context.has(state):
		Input.set_custom_mouse_cursor(load(DIR + "normal.png"), Input.CURSOR_ARROW, Vector2(5, 4))
		return
	var tex: Texture2D = _context[state]
	Input.set_custom_mouse_cursor(tex, Input.CURSOR_ARROW, Vector2(tex.get_width() * 0.5, tex.get_height() * 0.5))
