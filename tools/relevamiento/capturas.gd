extends SceneTree
# Carga Level1, teletransporta al jugador a varios puntos y guarda capturas del viewport.
var puntos := [150.0, 900.0, 1700.0, 2500.0, 3150.0, 3300.0, 3480.0]
var out := ""
func _initialize() -> void:
	out = OS.get_cmdline_user_args()[0]
	var lvl = load("res://scenes/levels/Level1.tscn").instantiate()
	root.add_child(lvl)
	_run(lvl)
func _run(lvl) -> void:
	await process_frame
	var p = lvl.get_node("Player")
	for i in puntos.size():
		p.global_position = Vector2(puntos[i], 300)
		p.velocity = Vector2.ZERO
		for f in 90: await physics_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("%s/level1_%d_x%d.png" % [out, i, int(puntos[i])])
		print("captura x=", puntos[i], " pos=", p.global_position, " en_piso=", p.is_on_floor())
	quit()
