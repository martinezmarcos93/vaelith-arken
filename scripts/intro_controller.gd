extends Node2D

## Etapa 3 - Intro jugable. Escena 1 de guion_intro.md ("sin input del
## jugador"): se resuelve reutilizando DialogueBox -- pausa el arbol
## mientras se revela el nombre, y al cerrarse el jugador "recupera el
## control" solo (el arbol se despausa), sin necesitar un estado nuevo en
## player.gd. Texto basado en "Ideas base para el juego/Despertar en la
## oscuridad.pdf": la pregunta y la certeza del nombre son literales del
## original.

func _ready() -> void:
	DialogueBox.show_lines(["¿Quién soy?", "...", "Vaelith Arken.", "No recuerdo nada más."])
