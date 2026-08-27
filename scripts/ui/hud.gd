extends CanvasLayer

## HUD minimo. Barra de vida conectada a Player.health_changed y contador de
## calaveras a GameState.skull_collected. No busca al jugador por ruta fija
## (para poder instanciarse en cualquier nivel) sino por el grupo "player"
## que player.gd se agrega en _ready(). La barra del boss sigue el mismo
## patron: busca por grupo "boss" y queda oculta si el nivel no tiene ninguno.
##
## Estetica: laminas de la hoja "penitencia / corrupcion" (medallon de la
## dama velada + marco dorado + engarce). Descompuestas en 3 texturas
## (marco calado / track vacio / relleno) sobre un TextureProgressBar; el HUD
## solo mueve value/max_value. Relleno dorado para Vaelith (penitencia),
## violeta para el Guerrero-Espejo (corrupcion).

@onready var health_bar: TextureProgressBar = $PlayerBlock/HealthBar
@onready var skull_label: Label = $PlayerBlock/SkullCount
@onready var boss_root: Control = $BossBar
@onready var boss_bar: TextureProgressBar = $BossBar/HealthBar


func _ready() -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player == null:
		push_warning("HUD: no se encontro ningun nodo en el grupo 'player'.")
	else:
		player.health_changed.connect(_on_health_changed)
		_on_health_changed(player.health, player.max_health)

	GameState.skull_collected.connect(_on_skull_collected)
	_on_skull_collected(GameState.skulls_collected)

	var boss := get_tree().get_first_node_in_group("boss")
	if boss != null:
		boss_root.visible = true
		boss.health_changed.connect(_on_boss_health_changed)
		boss.surrendered.connect(_on_boss_surrendered)
		_on_boss_health_changed(boss.health, boss.max_health)


func _on_health_changed(current: int, max_health: int) -> void:
	health_bar.max_value = maxi(max_health, 1)
	health_bar.value = clampi(current, 0, max_health)


func _on_skull_collected(total: int) -> void:
	skull_label.text = "×%d" % total


func _on_boss_health_changed(current: int, max_health: int) -> void:
	boss_bar.max_value = maxi(max_health, 1)
	boss_bar.value = clampi(current, 0, max_health)


func _on_boss_surrendered() -> void:
	boss_root.visible = false
