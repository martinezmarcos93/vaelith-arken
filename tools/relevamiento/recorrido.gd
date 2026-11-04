extends SceneTree
# Capturas de una escena con el jugador parado en varias x (sin ventana de juego
# propia: renderiza y guarda el viewport). Cierra los diálogos que se abran.
# Con un 4º argumento cualquiera (ej. "dialogo") deja los diálogos visibles.
# Uso: godot --path . -s tools/relevamiento/recorrido.gd -- res://scenes/levels/Intro.tscn <carpeta> 150,600,1100
func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	var lvl = load(a[0]).instantiate()
	root.add_child(lvl)
	_run(lvl, a[1], a[2].split(","), a[0].get_file().get_basename())

func _run(lvl: Node, out: String, xs: PackedStringArray, nombre: String) -> void:
	await process_frame
	var p = lvl.get_node_or_null("Player")
	for i in xs.size():
		if p != null:
			p.global_position = Vector2(float(xs[i]), p.global_position.y - 40)
			p.velocity = Vector2.ZERO
		for f in 75:
			if OS.get_cmdline_user_args().size() < 4:
				paused = false
				var d = root.get_node_or_null("DialogueBox")
				if d != null:
					d.visible = false
			await physics_frame
		# cerrar diálogos que tapen la escena
		var dlg = root.get_node_or_null("DialogueBox")
		if dlg != null and OS.get_cmdline_user_args().size() < 4:
			dlg.visible = false
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("%s/%s_%02d_x%s.png" % [out, nombre, i, xs[i]])
	quit()
