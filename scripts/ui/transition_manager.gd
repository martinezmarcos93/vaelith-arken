extends CanvasLayer

## Autoload: fundido a negro entre escenas. fade_out/fade_in son awaitables
## (Tween.finished); goto_scene encadena fade-out -> cambio de escena ->
## fade-in en un solo llamado para que cada pantalla no tenga que repetir
## la coreografia.

@onready var _rect: ColorRect = $ColorRect


func _ready() -> void:
	layer = 100
	_rect.color = Color(0.0, 0.0, 0.0, 0.0)


func fade_out(duration: float = 0.5) -> void:
	var tween := create_tween()
	tween.tween_property(_rect, "color:a", 1.0, duration)
	await tween.finished


func fade_in(duration: float = 0.5) -> void:
	var tween := create_tween()
	tween.tween_property(_rect, "color:a", 0.0, duration)
	await tween.finished


func goto_scene(path: String, duration: float = 0.5) -> void:
	await fade_out(duration)
	get_tree().change_scene_to_file(path)
	await get_tree().process_frame
	await fade_in(duration)
