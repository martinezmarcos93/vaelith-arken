extends Node2D

## Escena 1 de docs/guion_demo.md ("El despertar", sin input del jugador):
## se resuelve reutilizando DialogueBox -- pausa el arbol mientras corre la
## narracion y al cerrarse el jugador "recupera el control" solo (el arbol
## se despausa), sin necesitar un estado nuevo en player.gd. El guion
## reescrito NO nombra a Vaelith aca: no recupera una historia, recupera
## momentos -- la escena termina en la certeza del cuerpo, no de la
## identidad.

func _ready() -> void:
	# Escena 1 empieza en silencio: "no hay música. Solo viento, respiración."
	# La música vuelve a entrar recién en Level 1 ("la música comienza por
	# primera vez", Escena 8 del guion).
	AudioManager.stop_music(3.0)
	DialogueBox.show_lines([
		"La oscuridad no desaparece cuando abrís los ojos.",
		"Primero sentís frío.",
		"No el de una noche de invierno. Algo más profundo.",
		"Una ausencia de calor tan larga que tu cuerpo ya no recuerda cómo se siente estar vivo.",
		"Respirás. Tierra húmeda. Piedra. Ceniza.",
		"Algo parecido a incienso apagado.",
		"No reconocés el lugar.",
		"Pero reconocés tu cuerpo.",
		"Sabés cómo cerrar el puño.",
		"Sabés cómo mantenerte de pie.",
		"Sabés dónde debería estar un arma.",
	])
