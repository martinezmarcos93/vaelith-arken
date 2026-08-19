extends Node2D

## Driver de pruebas del sandbox de Etapa 1.5. Simula input real (via
## Input.action_press/release) para validar el sistema de combate de punta a
## punta sin necesitar que un humano juegue -- pensado para correr en modo
## --headless y leer los prints por consola. No es parte del juego final.

func _ready() -> void:
	_run_test_sequence()


func _run_test_sequence() -> void:
	await get_tree().create_timer(0.3).timeout
	print("--- TEST: caminar hacia el dummy ---")
	Input.action_press("move_right")
	await get_tree().create_timer(0.5).timeout
	Input.action_release("move_right")

	await get_tree().create_timer(0.2).timeout
	print("--- TEST: ataque alto ---")
	await _tap("attack_high")

	print("--- TEST: ataque bajo ---")
	await _tap("attack_low")

	print("--- TEST: mantener bloqueo 9s (el dummy ataca cada 2s, deberia romper postura) ---")
	Input.action_press("block")
	await get_tree().create_timer(9.0).timeout
	Input.action_release("block")

	print("--- TEST: sin bloquear, absorber el proximo golpe del dummy ---")
	await get_tree().create_timer(3.0).timeout

	print("--- TEST: embestida (deberia alejar al dummy) ---")
	await _tap("shove")

	print("--- TEST FIN ---")


func _tap(action: String) -> void:
	Input.action_press(action)
	await get_tree().create_timer(0.05).timeout
	Input.action_release(action)
	await get_tree().create_timer(0.6).timeout
