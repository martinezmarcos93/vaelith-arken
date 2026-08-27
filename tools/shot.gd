extends Node2D

## Throwaway (tools/): saca capturas de la UI para diagnosticar los "rectángulos
## negros" del informe visual. Uso:
##   godot --path . --resolution 1280x720 tools/Shot.tscn -- dialogue
##   godot --path . --resolution 1280x720 tools/Shot.tscn -- pause
## Escribe user://shot_<modo>.png y cierra.

func _ready() -> void:
	var mode := "dialogue"
	var args := OS.get_cmdline_user_args()
	var clean := args.has("clean")  # "clean" => sin lineas de debug (para capturas de entrega)
	for a in args:
		if a != "clean":
			mode = a

	# fondo tipo gameplay para que se vea el contraste real
	var bg := ColorRect.new()
	bg.color = Color(0.08, 0.05, 0.12)
	bg.size = Vector2(1280, 720)
	add_child(bg)
	var strip := ColorRect.new()
	strip.color = Color(0.2, 0.35, 0.25)
	strip.position = Vector2(0, 360)
	strip.size = Vector2(1280, 40)
	add_child(strip)

	if mode == "feet":
		bg.queue_free(); strip.queue_free()
		var floor_body := StaticBody2D.new()
		floor_body.position = Vector2(640, 500)
		var cs := CollisionShape2D.new()
		var rect := RectangleShape2D.new(); rect.size = Vector2(600, 40)
		cs.shape = rect; floor_body.add_child(cs)
		var fv := ColorRect.new(); fv.color = Color(1, 0, 1, 0.5)
		fv.position = Vector2(-300, -20); fv.size = Vector2(600, 40)
		floor_body.add_child(fv)
		add_child(floor_body)
		var pl: Node = load("res://scenes/player/Player.tscn").instantiate()
		pl.position = Vector2(640, 300)
		add_child(pl)
		for i in 120:
			await get_tree().physics_frame
		var spr: AnimatedSprite2D = pl.get_node("AnimatedSprite2D")
		var tex: Texture2D = spr.sprite_frames.get_frame_texture(spr.animation, spr.frame)
		var tsize: Vector2 = tex.get_size()
		var body_cs: CollisionShape2D = pl.get_node("CollisionShape2D")
		var half: float = (body_cs.shape as RectangleShape2D).size.y * 0.5
		var col_top: float = 500.0 - 20.0
		# alfa real del frame actual
		var img: Image = tex.get_image()
		var content_bottom := -1
		for y in range(int(tsize.y) - 1, -1, -1):
			var row_has := false
			for x in range(int(tsize.x)):
				if img.get_pixel(x, y).a > 0.06:
					row_has = true
					break
			if row_has:
				content_bottom = y
				break
		# centered=true: pixel ty -> local (ty - tsize.y/2 + offset.y) * scale
		var feet_local: float = (float(content_bottom) - tsize.y * 0.5 + spr.offset.y) * spr.scale.y
		var feet_world: float = pl.global_position.y + feet_local
		print("anim=%s frame=%d  tex=%s  content_bottom_y=%d" % [spr.animation, spr.frame, tsize, content_bottom])
		print("player.global_position.y = ", pl.global_position.y)
		print("box_bottom_world = ", pl.global_position.y + half, "   collision_top_world = ", col_top)
		print("sprite.offset = ", spr.offset, "  scale = ", spr.scale)
		print("feet_local (escalado, desde origen) = ", feet_local)
		print("feet_world = ", feet_world)
		print(">>> GAP feet_world - collision_top = ", feet_world - col_top, "  (negativo=flota, positivo=hundido)")
		var cam := Camera2D.new()
		cam.position = Vector2(640, 460)
		cam.zoom = Vector2(3, 3)
		add_child(cam)
		for i in 6:
			await get_tree().process_frame
		get_viewport().get_texture().get_image().save_png("user://shot_feet.png")
		print("saved user://shot_feet.png")
		get_tree().quit()
		return
	if mode.begins_with("res://"):
		bg.queue_free(); strip.queue_free()
		var sc: Node = load(mode).instantiate()
		add_child(sc)
		# una escena de UI (root Control) necesita tamaño de viewport para que
		# anclas/CenterContainer resuelvan bien fuera del arbol principal.
		if sc is Control:
			(sc as Control).set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
			(sc as Control).size = Vector2(get_viewport().size)
		for i in 150:
			await get_tree().process_frame
		# líneas de debug: pie del jugador (verde) y tope de colisión más cercano (rojo)
		var pl2: Node2D = sc.get_node_or_null("Player")
		if pl2 != null and not clean:
			var spr2: AnimatedSprite2D = pl2.get_node("AnimatedSprite2D")
			var tex2: Texture2D = spr2.sprite_frames.get_frame_texture(spr2.animation, spr2.frame)
			var feet_y: float = pl2.global_position.y + (tex2.get_size().y - tex2.get_size().y * 0.5 + spr2.offset.y) * spr2.scale.y
			var gl := Line2D.new(); gl.width = 2; gl.default_color = Color(0, 1, 0)
			gl.points = PackedVector2Array([Vector2(pl2.global_position.x - 300, feet_y), Vector2(pl2.global_position.x + 300, feet_y)])
			sc.add_child(gl)
			var on_floor_y: float = pl2.global_position.y + (pl2.get_node("CollisionShape2D").shape as RectangleShape2D).size.y * 0.5
			var rl := Line2D.new(); rl.width = 2; rl.default_color = Color(1, 0, 0)
			rl.points = PackedVector2Array([Vector2(pl2.global_position.x - 300, on_floor_y), Vector2(pl2.global_position.x + 300, on_floor_y)])
			sc.add_child(rl)
			print("player.y=", pl2.global_position.y, "  box_bottom(rojo)=", on_floor_y, "  feet_canvas_bottom(verde)=", feet_y, "  on_floor=", pl2.is_on_floor())
			await get_tree().process_frame
		var im2 := get_viewport().get_texture().get_image()
		var out := mode.get_file().get_basename()
		im2.save_png("user://shot_%s.png" % out)
		print("saved user://shot_%s.png" % out)
		get_tree().quit()
		return
	if mode == "pause":
		var pm: Node = load("res://scenes/ui/PauseMenu.tscn").instantiate()
		add_child(pm)
		pm.visible = true
		await get_tree().process_frame
	else:
		var db: Node = load("res://scenes/ui/DialogueBox.tscn").instantiate()
		add_child(db)
		db.show_lines(["Sabés dónde debería estar un arma.", "—Todavía hacés eso."] as Array[String])
		get_tree().paused = false  # que no congele el screenshot

	for i in 20:
		await get_tree().process_frame
	var img := get_viewport().get_texture().get_image()
	img.save_png("user://shot_%s.png" % mode)
	print("saved user://shot_%s.png  (%s)" % [mode, OS.get_user_data_dir()])
	get_tree().quit()
