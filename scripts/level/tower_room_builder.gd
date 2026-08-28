extends TileMapLayer

## Prototipo del Sector Torre (roadmap_level1_largo.md, Fase 2). Pinta un
## cuarto rectangular con el TileSet de Raou (16px, escalado x2 -> 32px
## efectivo) por codigo en vez de a mano en el editor -- mas facil de
## iterar el layout mientras se aprueba la direccion visual.
## source_id 0 = raou_tileset.tres. Atlas: pared (5,15), piso liso (5,20),
## piso con sigilo (5,21).

const WALL := Vector2i(5, 15)
const FLOOR := Vector2i(5, 20)
const FLOOR_ACCENT := Vector2i(5, 21)

@export var width: int = 14
@export var height: int = 7
## Filas (desde arriba, 0-indexed) donde la pared derecha se abre --
## el umbral hacia el bosque.
@export var door_rows: Array[int] = [3, 4]


func _ready() -> void:
	_build_room()


func _build_room() -> void:
	clear()
	for x in width:
		set_cell(Vector2i(x, 0), 0, WALL)
	for y in range(1, height - 1):
		set_cell(Vector2i(0, y), 0, WALL)
		if y not in door_rows:
			set_cell(Vector2i(width - 1, y), 0, WALL)
	for x in width:
		var tile := FLOOR_ACCENT if x % 4 == 2 else FLOOR
		set_cell(Vector2i(x, height - 1), 0, tile)
