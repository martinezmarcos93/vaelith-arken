extends Node2D

## Smoke test headless de Level1 (Fase 4.3): mantiene "correr a la derecha" y
## saltea cada tanto para cruzar el nivel de punta a punta sin un humano
## jugando, igual que tools/test_driver.gd hace con el sandbox de Etapa
## 1.5. No valida ritmo/dificultad (eso es Fase 4.6) -- solo confirma que
## nada explota: colisiones, hazard, checkpoints, enemigos, respawn.

func _ready() -> void:
	if DisplayServer.get_name() != "headless":
		return
	_run()


func _run() -> void:
	await get_tree().create_timer(0.3).timeout
	print("--- TEST LEVEL1: cruzando el nivel ---")
	var player := get_node("Player")
	Input.action_press("move_right")
	var jump_count := 0
	while jump_count < 40:
		await get_tree().create_timer(0.35).timeout
		Input.action_press("jump")
		await get_tree().create_timer(0.05).timeout
		Input.action_release("jump")
		jump_count += 1
		print("t=%.1fs pos=%s on_floor=%s vida=%d state=%s" % [jump_count * 0.4, player.global_position, player.is_on_floor(), player.health, player.state])
	Input.action_release("move_right")
	print("--- TEST LEVEL1: FIN (posicion jugador: %s, vida=%d) ---" % [player.global_position, player.health])
	if DisplayServer.get_name() == "headless":
		get_tree().quit()
