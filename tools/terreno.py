"""Relieve del exterior: una sola función de altura que comparten Blender (genera la malla)
y Unreal (apoya árboles, lápidas y enemigos sobre el suelo). Unidades: centímetros de Unreal.

Zonas (Y crece alejándose de la catacumba; la salida está en (6400, 6000)):
  ladera      y < 8000      la catacumba queda enterrada en una loma; pasillo libre hacia el sur
  cementerio  8000..20000   casi plano, sube suave hacia el arco; muros a los lados
  arco        y ~ 20500     paso en ruinas (SM_Arco_Ruina) entre cementerio y bosque
  bosque alto 21000..44000  ondulado; el arroyo cruza en y ~ 33000 (barranco con puente)
  loma        (16000,47000) claro alto: desde ahí se ve el pueblo, al este
  bosque oscuro y hondonada de la torre en (-12000, 58000)
"""
import math

SALIDA = (6400.0, 6000.0)
ARCO = (6400.0, 20500.0)
PUENTE = (8200.0, 33000.0)
LOMA = (16000.0, 47000.0)
TORRE = (-12000.0, 58000.0)
PUEBLO = (70000.0, 56000.0)   # fuera del terreno jugable, sobre su propia colina
ARROYO_Y = 33000.0

# Extensión del terreno jugable
X0, X1 = -24000.0, 28000.0
Y0, Y1 = 6200.0, 66000.0


def _suave(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _gauss(x, y, cx, cy, r):
    return math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (r * r))


def ruido(x, y):
    return (90 * math.sin(x / 2300.0 + 1.3) * math.cos(y / 3100.0)
            + 60 * math.sin((x + y) / 1700.0) + 35 * math.cos((x - 2 * y) / 900.0))


def camino_cementerio(x, y):
    """Distancia (cm) al eje del cementerio salida -> arco."""
    return abs(x - SALIDA[0])


def altura(x, y):
    # Base ondulada que se aplana cerca de la salida y en el cementerio
    plano = _suave((y - 19000.0) / 4000.0)       # 0 en el cementerio, 1 en el bosque
    h = ruido(x, y) * (0.25 + 0.75 * plano)
    # Rampa del cementerio hacia el arco
    h += 260.0 * _suave((y - 8000.0) / 12500.0)
    # Ladera sobre la catacumba: alta a los lados del pasillo de salida
    if y < 8000.0:
        # loma sobre la cripta: alta a los lados de la boca, se abre enseguida en abanico
        ancho = 450.0 + max(0.0, y - 6300.0) * 1.6
        lado = _suave((abs(x - SALIDA[0]) - ancho) / 800.0)
        h += 700.0 * lado * (1.0 - _suave((y - 6400.0) / 1500.0))
    # Muros naturales del cementerio: el terreno sube fuera de x in [1200, 11600]
    fuera = max(1200.0 - x, x - 11600.0, 0.0)
    h += min(900.0, fuera * 0.35) * (1.0 - _suave((y - 20800.0) / 1500.0))
    # Arroyo: barranco suave de este a oeste
    h -= 380.0 * math.exp(-((y - ARROYO_Y) / 650.0) ** 2) * _suave((y - 25000.0) / 3000.0)
    # Loma del vigía
    h += 2100.0 * _gauss(x, y, LOMA[0], LOMA[1], 8500.0)
    # Hondonada de la torre (la niebla se junta abajo)
    h -= 750.0 * _gauss(x, y, TORRE[0], TORRE[1], 4200.0)
    h += 120.0 * _gauss(x, y, TORRE[0], TORRE[1], 1400.0)  # piso de la torre algo más parejo
    # Bordes del mundo: suben (no se puede salir) salvo al este de la loma, que cae hacia el valle
    borde_o = _suave((X0 + 3500.0 - x) / 3500.0)
    borde_n = _suave((y - (Y1 - 3500.0)) / 3500.0)
    borde_e = _suave((x - (X1 - 3500.0)) / 3500.0)
    h += 2500.0 * max(borde_o, borde_n)
    h += 2500.0 * borde_e * (1.0 - _gauss(x, y, X1, LOMA[1], 9000.0))
    # La salida misma queda a nivel del piso de la catacumba
    cerca_salida = _gauss(x, y, SALIDA[0], SALIDA[1] + 700.0, 800.0) * (1.0 - _suave((abs(x - SALIDA[0]) - 450.0) / 300.0))
    h = h * (1.0 - cerca_salida)
    return h


def region(x, y):
    """Material del suelo por zona."""
    if y < 21000.0:
        return "M_Suelo_Cementerio"
    if x < 3000.0 and y > 43000.0:
        return "M_Suelo_Hojas"
    return "M_Suelo_Bosque"


# Valle al este (solo se ve desde la loma; no se pisa). El pueblo está sobre su colina.
VALLE_X0, VALLE_X1 = X1 - 2000.0, 220000.0
VALLE_Y0, VALLE_Y1 = -30000.0, 150000.0


def altura_valle(x, y):
    h = -2200.0 + 1700.0 * _gauss(x, y, PUEBLO[0], PUEBLO[1], 30000.0)
    h += 400.0 * math.sin(x / 9000.0) * math.cos(y / 11000.0) + 250.0 * math.sin((x - y) / 5000.0)
    # Sierras lejanas que cierran el horizonte
    h += 6000.0 * _suave((x - 170000.0) / 40000.0)
    h += 4000.0 * max(_suave((VALLE_Y0 + 40000.0 - y) / 40000.0), _suave((y - (VALLE_Y1 - 40000.0)) / 40000.0))
    return h
