extends Node2D

## Etapa 7: cuando el Boss 1 se rinde, la demo pasa al Epilogo
## (docs/guion_desenlace.md, beat 1: "el boss cae, la mascara termina de
## caer, silencio total por 2-3 segundos" antes de cualquier corte -- el
## guerrero-espejo no muere, ver boss1.gd, pero el beat de silencio es el
## mismo). Este script vive en Level1, no en boss1.gd -- el boss solo
## emite `surrendered`, el nivel decide que pasa despues, asi boss1.gd no
## queda acoplado a una escena de destino fija.

const EPILOGUE_SCENE := "res://scenes/levels/Epilogue.tscn"
const POST_SURRENDER_SILENCE := 2.5


func _ready() -> void:
	var boss := get_tree().get_first_node_in_group("boss")
	if boss != null:
		boss.surrendered.connect(_on_boss_surrendered)


func _on_boss_surrendered() -> void:
	await get_tree().create_timer(POST_SURRENDER_SILENCE).timeout
	TransitionManager.goto_scene(EPILOGUE_SCENE)
