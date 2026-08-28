extends Node2D

## Throwaway (tools/): capturas de TorreSector desde varias posiciones de
## camara a zoom de juego, para revisar la direccion artistica sin abrir el
## editor. Uso:
##   godot --path . --resolution 1280x720 tools/ShotTorre.tscn
## Escribe user://torre_a.png .. user://torre_e.png y cierra.

const SCENE := "res://scenes/levels/TorreSector.tscn"
const ZOOM := Vector2(3.0, 3.0)
# (nombre, posicion_camara, zoom_override_o_0)
const SHOTS := [
	["a_spawn", Vector2(150, 186), 0.0],
	["b_mesa", Vector2(235, 184), 0.0],
	["c_columna_dist", Vector2(360, 182), 0.0],
	["d_pasillo", Vector2(560, 186), 0.0],
	["e_umbral", Vector2(720, 188), 0.0],
	["f_wide", Vector2(300, 168), 2.0],
]


func _ready() -> void:
	var scene: Node = load(SCENE).instantiate()
	add_child(scene)

	# desactivar la camara del jugador y el HUD para ver solo el escenario
	var pcam: Camera2D = scene.get_node_or_null("Player/Camera2D")
	if pcam != null:
		pcam.enabled = false
	var hud: Node = scene.get_node_or_null("HUD")
	if hud != null:
		hud.visible = false

	var cam := Camera2D.new()
	cam.zoom = ZOOM
	add_child(cam)
	cam.make_current()

	# dejar que se construya el tilemap, arranquen luces y se asiente la fisica
	for i in 90:
		await get_tree().physics_frame

	# --- FLOOR PROBE (descartable): donde apoya Vaelith de verdad ---
	var pl: Node2D = scene.get_node_or_null("Player")
	if pl != null:
		var cs: CollisionShape2D = pl.get_node("CollisionShape2D")
		var half: float = (cs.shape as RectangleShape2D).size.y * 0.5 * pl.scale.y
		print("PROBE player.y=", pl.global_position.y, " feet_y=", pl.global_position.y + half, " on_floor=", pl.is_on_floor())

	for shot in SHOTS:
		cam.global_position = shot[1]
		cam.zoom = (Vector2(shot[2], shot[2]) if shot[2] > 0.0 else ZOOM)
		for i in 8:
			await get_tree().process_frame
		var img := get_viewport().get_texture().get_image()
		img.save_png("user://torre_%s.png" % shot[0])
		print("saved user://torre_%s.png" % shot[0])

	get_tree().quit()
