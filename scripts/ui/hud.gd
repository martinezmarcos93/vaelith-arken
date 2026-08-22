extends CanvasLayer

## Etapa 9.1 - HUD minimo: barra de vida conectada a Player.health_changed
## y contador de calaveras conectado a GameState.skull_collected. No busca
## al jugador por ruta fija (para poder instanciarse en cualquier nivel)
## sino por el grupo "player" que player.gd se agrega en _ready().

@onready var health_fill: ColorRect = $Margin/HealthBar/Fill
@onready var health_background: ColorRect = $Margin/HealthBar/Background
@onready var skull_label: Label = $Margin/SkullCount


func _ready() -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player == null:
		push_warning("HUD: no se encontro ningun nodo en el grupo 'player'.")
	else:
		player.health_changed.connect(_on_health_changed)
		_on_health_changed(player.health, player.max_health)

	GameState.skull_collected.connect(_on_skull_collected)
	_on_skull_collected(GameState.skulls_collected)


func _on_health_changed(current: int, max_health: int) -> void:
	var ratio := float(current) / float(max_health) if max_health > 0 else 0.0
	health_fill.size.x = health_background.size.x * clamp(ratio, 0.0, 1.0)


func _on_skull_collected(total: int) -> void:
	skull_label.text = "x%d" % total
