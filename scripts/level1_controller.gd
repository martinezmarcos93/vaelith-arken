extends Node2D

## Rework narrativo (docs/guion_demo.md) -- Boss "El Espejo".
##
## boss1.gd no muere: emite `phase_changed` (la mascara se agrieta al 50%
## de vida) y `surrendered` (a 0 de vida baja el arma). Este script cuelga
## de Level1 y traduce esos dos momentos + el cierre a los beats del guion:
##
##   fase 2      -> "Lo que Vaelith olvido"
##   rendicion   -> "La identidad" + el recuerdo final "El ultimo dia"
##
## La linea de aparicion del boss ("Todavia haces eso / Cargas primero") no
## va aca: la dispara BossIntroTrigger al entrar a la arena, antes de que
## empiece el combate.
##
## Ya no hay eleccion de pregunta ni el intercambio sobre Tomas/el padre:
## guion_demo.md reemplaza ese canon (venia de una sesion de mesa) por la
## revelacion del constructo-espejo.

const EPILOGUE_SCENE := "res://scenes/levels/Epilogue.tscn"
const LEVEL_MUSIC := "res://assets/audio/music/level1.mp3"
const POST_SURRENDER_SILENCE := 2.5
const PRE_MEMORY_SILENCE := 1.5
const PRE_EPILOGUE_SILENCE := 1.5


func _ready() -> void:
	# "La música comienza por primera vez" al entrar a Level 1 (guion, Esc 8).
	# El tema del boss lo cambia MusicTrigger a la entrada de la arena.
	AudioManager.play_music(LEVEL_MUSIC, 2.5, -7.0)
	var boss := get_tree().get_first_node_in_group("boss")
	if boss == null:
		return
	boss.phase_changed.connect(_on_boss_phase_changed)
	boss.surrendered.connect(_on_boss_surrendered)


## Fase 2 ("Lo que Vaelith olvido"): el espejo empieza a usar tecnicas que
## Vaelith todavia no conoce. No corta el combate como beat aparte -- es un
## comentario al vuelo (DialogueBox pausa el arbol unos segundos igual).
func _on_boss_phase_changed(_new_phase: int) -> void:
	DialogueBox.show_lines([
		"El espejo cambia. Ataca con cosas que no sabés hacer.",
		"—Eso también lo sabías.",
		"—Solo que ya no lo recordás.",
	])


## Rendicion -> "La identidad": el guerrero deja de atacar, la mascara
## empieza a caer, pero no se revela el rostro.
func _on_boss_surrendered() -> void:
	# "Silencio total (corte de música) por 2-3 segundos" (guion).
	AudioManager.stop_music(1.5)
	await get_tree().create_timer(POST_SURRENDER_SILENCE).timeout
	DialogueBox.finished.connect(_on_identity_finished, CONNECT_ONE_SHOT)
	DialogueBox.show_lines([
		"El guerrero deja de atacar. La máscara empieza a caer.",
		"No llega a mostrar el rostro.",
		"—¿No sabés quién soy?",
		"—No.",
		"Baja la espada.",
		"—Claro.",
		"—Te aseguraste de eso.",
		"—¿Quién sos?",
		"—Eso es lo que viniste a recordar.",
	])


## "Recuerdo final de la demo" (El ultimo dia): recien despues del silencio
## aparece el fragmento. GameState.collect_memory() lo cuenta igual que un
## MemoryFragment del nivel (el Epilogo ya no llama a collect_memory()).
func _on_identity_finished() -> void:
	await get_tree().create_timer(PRE_MEMORY_SILENCE).timeout
	GameState.collect_memory()
	DialogueBox.finished.connect(_on_memory_finished, CONNECT_ONE_SHOT)
	DialogueBox.show_lines([
		"El guerrero cae. La máscara toca el suelo. Silencio total.",
		"Una fortaleza. Sirenas. Gritos. Fuego.",
		"El constructo observa desde una habitación.",
		"—¡Señor! ¡Nos están rodeando!",
		"—Entonces que entren.",
		"La puerta se abre. Entrás herido. Te arrodillás frente a la criatura.",
		"—Escuchame.",
		"—Si alguna vez regreso...",
		"—No me dejes recordar.",
		"—¿Por qué?",
		"—Porque si recuerdo lo que hice, voy a tener que decidir si todavía soy el mismo.",
		"La visión se corta.",
	])


func _on_memory_finished() -> void:
	await get_tree().create_timer(PRE_EPILOGUE_SILENCE).timeout
	TransitionManager.goto_scene(EPILOGUE_SCENE)
