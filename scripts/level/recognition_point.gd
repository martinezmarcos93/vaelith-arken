extends InteractableArea
class_name RecognitionPoint

## El verbo distintivo de Vaelith (brief SS 3 y el ensayo de diseño, punto 2):
## objetos / mecanismos / simbolos que el protagonista RECONOCE aunque no
## recuerde por que. "Vaelith no recuerda, pero su cuerpo sabe."
##
## Al interactuar:
##   1. beat de reconocimiento ("Esto te resulta familiar. / Tus manos ya
##      saben.")  -- `recognition_lines`
##   2. (opcional) Vaelith ejecuta una accion que aparentemente no sabe
##      hacer -- se marca con la señal `acted`; la consecuencia real (girar
##      una rueda, abrir un camino, cambiar el nivel) la conecta cada
##      instancia en la escena.
##   3. (opcional) fragmento de memoria -- `memory_lines`, contado en
##      GameState igual que un MemoryFragment del nivel.
##
## No inventa narrativa: `recognition_lines` y `memory_lines` se cargan por
## instancia con texto de docs/guion_demo.md.

## Se emite entre el beat de reconocimiento y la memoria: es el momento en
## que "Vaelith hace algo". La escena engancha aca la consecuencia mecanica.
signal acted

@export_multiline var recognition_lines: Array[String] = ["Esto te resulta familiar."]
## Vacio = el reconocimiento no dispara ningun recuerdo.
@export_multiline var memory_lines: Array[String] = []
## Segundos entre el beat de reconocimiento y `acted` (para que la accion
## de Vaelith no pise el dialogo).
@export var act_delay: float = 0.3
## Cuenta el recuerdo en GameState (como los MemoryFragment del nivel).
@export var counts_as_memory: bool = true


func _do_interact() -> void:
	if recognition_lines.is_empty():
		_after_recognition()
		return
	DialogueBox.finished.connect(_after_recognition, CONNECT_ONE_SHOT)
	DialogueBox.show_lines(recognition_lines)


func _after_recognition() -> void:
	if act_delay > 0.0:
		await get_tree().create_timer(act_delay).timeout
	acted.emit()
	if memory_lines.is_empty():
		return
	if counts_as_memory:
		GameState.collect_memory()
	DialogueBox.show_lines(memory_lines)
