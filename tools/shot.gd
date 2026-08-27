extends Node2D

## Throwaway (tools/): saca capturas de la UI para diagnosticar los "rectángulos
## negros" del informe visual. Uso:
##   godot --path . --resolution 1280x720 tools/Shot.tscn -- dialogue
##   godot --path . --resolution 1280x720 tools/Shot.tscn -- pause
## Escribe user://shot_<modo>.png y cierra.

func _ready() -> void:
	var mode := "dialogue"
	for a in OS.get_cmdline_user_args():
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
