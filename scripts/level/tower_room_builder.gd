extends TileMapLayer

## Prototipo del Sector Torre (roadmap_level1_largo.md, Fase 2). Pinta un
## cuarto rectangular con el TileSet de Raou (16px, escalado x2 -> 32px
## efectivo) por codigo en vez de a mano en el editor -- mas facil de
## iterar el layout mientras se aprueba la direccion visual.
## source_id 0 = raou_tileset.tres. Atlas: pared (5,15), piso liso (5,20),
## piso con sigilo (5,21), piso alterno (5,22).

const WALL := Vector2i(5, 15)
const WALL_ALT := Vector2i(6, 15)
const FLOOR := Vector2i(5, 20)
const FLOOR_SIGIL := Vector2i(5, 21)
const FLOOR_ALT := Vector2i(5, 22)

@export var width: int = 14
@export var height: int = 7
## Filas (desde arriba, 0-indexed) donde la pared derecha se abre -- un
## umbral (a otro tramo, o al bosque en el ultimo tramo del pasillo).
@export var door_rows: Array[int] = [3, 4]
## false = el tramo se abre directo al anterior (sin pared izquierda) --
## para encadenar tramos como un pasillo continuo.
@export var draw_left_wall: bool = true
## Semilla del patron de piso -- cambiarla re-mezcla la variacion de tiles
## sin tocar el codigo. Deterministico: mismo valor = mismo piso.
@export var floor_seed: int = 7


func _ready() -> void:
	_build_room()


func _build_room() -> void:
	clear()
	for x in width:
		set_cell(Vector2i(x, 0), 0, _wall_variant(x))
	for y in range(1, height - 1):
		if draw_left_wall:
			set_cell(Vector2i(0, y), 0, _wall_variant(y))
		if y not in door_rows:
			set_cell(Vector2i(width - 1, y), 0, _wall_variant(y + width))
	for x in width:
		set_cell(Vector2i(x, height - 1), 0, _floor_variant(x))


## Variacion sutil de mamposteria (sin textura nueva, misma hoja) para que
## la pared no se lea como un repeat perfecto -- regla "todo el espacio
## aprovechado" del roadmap sin generar arte nuevo.
func _wall_variant(seed: int) -> Vector2i:
	return WALL_ALT if seed % 3 == 0 else WALL


## Piso pseudo-aleatorio deterministico: rompe la grilla obvia del tileset
## sin agregar props. La mayoria es piso liso; el sigilo aparece raro y
## disperso (no cada N), el alterno da grano tonal.
func _floor_variant(x: int) -> Vector2i:
	var h: int = ((x + floor_seed) * 2654435761) & 0xFFFFFF
	var r: int = h % 100
	if r < 12:
		return FLOOR_SIGIL
	if r < 45:
		return FLOOR_ALT
	return FLOOR
