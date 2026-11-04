extends SceneTree
# Detecta props que flotan sobre el piso o se hunden en él.
# Por cada Sprite2D hijo directo del nivel: busca la fila opaca más baja de su
# textura y tira un rayo hacia abajo desde ahí. Si hay piso a 1-40 px, flota.
# Uso: godot --path . -s tools/relevamiento/props_flotantes.gd -- res://scenes/levels/Level1.tscn [Padre1,Padre2]
# (sin padres: hijos directos del nivel)
func _initialize() -> void:
	var lvl = load(OS.get_cmdline_user_args()[0]).instantiate()
	root.add_child(lvl)
	_medir(lvl)

func _pie_opaco(tex: Texture2D) -> int:
	var img := tex.get_image()
	if img.is_compressed():
		img.decompress()
	for y in range(img.get_height() - 1, -1, -1):
		for x in img.get_width():
			if img.get_pixel(x, y).a > 0.4:
				return y
	return img.get_height() - 1

func _medir(lvl: Node) -> void:
	for f in 3: await physics_frame
	var space: PhysicsDirectSpaceState2D = lvl.get_world_2d().direct_space_state
	var args := OS.get_cmdline_user_args()
	var nodos: Array = []
	if args.size() > 1:
		for padre in args[1].split(","):
			nodos.append_array(lvl.get_node(padre).get_children())
	else:
		nodos = lvl.get_children()
	for n in nodos:
		if not (n is Sprite2D) or n.texture == null:
			continue
		var s: Sprite2D = n
		var h := s.texture.get_height()
		var pie := _pie_opaco(s.texture)
		var top_y := -h / 2.0 if s.centered else 0.0
		var base := s.global_position + Vector2(0, (top_y + pie + 1) * absf(s.global_scale.y))
		var q := PhysicsRayQueryParameters2D.create(base + Vector2(0, -6), base + Vector2(0, 60))
		var hit: Dictionary = space.intersect_ray(q)
		if hit.is_empty():
			continue
		var gap: float = hit.position.y - base.y
		if absf(gap) >= 1.0 and gap <= 40.0:
			print("PROP %s pos=%s base=%.1f piso=%.1f gap=%.1f" % [s.name, s.position, base.y, hit.position.y, gap])
	quit()
