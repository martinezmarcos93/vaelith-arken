extends SceneTree
# Uso: -- <escena res://> <salida.png> <frames>
func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	root.add_child(load(a[0]).instantiate())
	_shot(a[1], int(a[2]))
func _shot(out: String, n: int) -> void:
	for i in n: await physics_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(out)
	quit()
