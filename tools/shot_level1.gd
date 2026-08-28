extends Node2D

## Throwaway (tools/): capturas de Level1 a lo largo del nivel a zoom de juego,
## para revisar la direccion luminica sin abrir el editor. Uso:
##   godot --path . --resolution 1280x720 tools/ShotLevel1.tscn
## Escribe user://lvl1_*.png y cierra.

const SCENE := "res://scenes/levels/Level1.tscn"
const ZOOM := Vector2(2.5, 2.5)
const SHOTS := [
	["a_inicio",       Vector2(230, 300), 0.0],
	["b_cristal",      Vector2(470, 320), 0.0],
	["c_gauntlet",     Vector2(1250, 380), 0.0],
	["d_totem_cp",     Vector2(1860, 390), 0.0],
	["e_cristal_azul", Vector2(2430, 390), 0.0],
	["f_hoguera_boss", Vector2(3350, 340), 0.0],
	["g_wide",         Vector2(1400, 340), 1.4],
]


func _ready() -> void:
	var scene: Node = load(SCENE).instantiate()
	add_child(scene)
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

	for i in 90:
		await get_tree().physics_frame

	for shot in SHOTS:
		cam.global_position = shot[1]
		cam.zoom = (Vector2(shot[2], shot[2]) if shot[2] > 0.0 else ZOOM)
		for i in 8:
			await get_tree().process_frame
		var img := get_viewport().get_texture().get_image()
		img.save_png("user://lvl1_%s.png" % shot[0])
		print("saved user://lvl1_%s.png" % shot[0])

	get_tree().quit()
