extends Node2D

## Etapa 7: cuando el Boss 1 se rinde, la demo pasa al Epilogo
## (docs/guion_desenlace.md, beat 1: "el boss cae, la mascara termina de
## caer, silencio total por 2-3 segundos" antes de cualquier corte -- el
## guerrero-espejo no muere, ver boss1.gd, pero el beat de silencio es el
## mismo). Este script vive en Level1, no en boss1.gd -- el boss solo
## emite `surrendered`, el nivel decide que pasa despues, asi boss1.gd no
## queda acoplado a una escena de destino fija.
##
## El intercambio post-rendicion (tregua, reconocimiento y la revelacion
## sobre Tomas) es cita literal de "Despertar en la oscuridad.pdf"
## (pag. 79-83, el mismo encuentro que origino al Boss 1) y ahora se dice
## EN PERSONA aca -- antes vivia como eco de memoria en el Epilogo, pero
## en la fuente real es el guerrero-espejo quien lo dice directamente,
## no Vaelith recordandolo despues. La pregunta final ("Pregunta lo que
## quieras... elegi bien") queda sin responder en la fuente -- la sesion
## de mesa termino justo ahi. Por eso elegir entre las 3 preguntas no
## cambia el desenlace: es agencia real en QUE se pregunta, fiel al
## hecho de que ninguna respuesta llego a escribirse nunca.

const EPILOGUE_SCENE := "res://scenes/levels/Epilogue.tscn"
const POST_SURRENDER_SILENCE := 2.5
const PRE_EPILOGUE_SILENCE := 1.5


func _ready() -> void:
	var boss := get_tree().get_first_node_in_group("boss")
	if boss != null:
		boss.surrendered.connect(_on_boss_surrendered)


func _on_boss_surrendered() -> void:
	await get_tree().create_timer(POST_SURRENDER_SILENCE).timeout
	DialogueBox.finished.connect(_on_exchange_finished, CONNECT_ONE_SHOT)
	DialogueBox.show_lines([
		"Bien.",
		"Eso es nuevo.",
		"No voy a atacarte mientras vos no me ataques.",
		"Pero tampoco voy a confiar en vos.",
		"Y vos tampoco deberías confiar en mí.",
		"La máscara finalmente se levanta unos centímetros.",
		"Reconocés la cicatriz.",
		"No sabés de dónde.",
		"No. No la recordaste. Tu cuerpo la reconoció.",
		"Todo sigue ahí.",
		"¿Tomás te contó lo que hizo?",
		"Entonces todavía está mintiéndote.",
		"Tu padre no fue quien te mató, Vaelith.",
		"Pero sí fue quien decidió qué debía pasar con tu cuerpo después.",
		"Podés hablar.",
		"Preguntame lo que quieras. Pero elegí bien.",
		"Porque algunas respuestas pueden devolverte recuerdos.",
		"Y otras pueden hacer que desees no haberlos recuperado nunca.",
	])


func _on_exchange_finished() -> void:
	await DialogueBox.ask_choice([
		"¿Quién sos?",
		"¿Qué le pasó a mi padre?",
		"¿Por qué peleás igual que yo?",
	])
	await get_tree().create_timer(PRE_EPILOGUE_SILENCE).timeout
	TransitionManager.goto_scene(EPILOGUE_SCENE)
