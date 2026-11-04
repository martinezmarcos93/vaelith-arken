extends SceneTree
# Cruza Level1 de punta a punta como tools/level1_test_driver.gd (correr a la
# derecha + saltar), sin tocar la escena, y avanza los diálogos con [E].
# Uso: godot --headless --path . -s tools/relevamiento/cruzar_level1.gd
func _initialize() -> void:
	var lvl = load("res://scenes/levels/Level1.tscn").instantiate()
	root.add_child(lvl)
	_run(lvl)

func _run(lvl: Node) -> void:
	await create_timer(0.3).timeout
	print("--- CRUCE LEVEL1 ---")
	var player = lvl.get_node("Player")
	Input.action_press("move_right")
	for i in 140:
		_accion("interact", true)
		await create_timer(0.05, true).timeout
		_accion("interact", false)
		await create_timer(0.3, true).timeout
		Input.action_press("jump")
		await create_timer(0.05, true).timeout
		Input.action_release("jump")
		print("i=%d t=%.1fs pos=%s piso=%s vida=%d" % [i, (i + 1) * 0.4, player.global_position, player.is_on_floor(), player.health])
	Input.action_release("move_right")
	print("--- FIN: pos=%s vida=%d ---" % [player.global_position, player.health])
	quit()

func _accion(nombre: String, apretada: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = nombre
	ev.pressed = apretada
	Input.parse_input_event(ev)
