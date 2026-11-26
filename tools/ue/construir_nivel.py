"""Construye /Game/Vaelith/Mapas/Lvl_Vaelith: catacumbas, osario, bosque y torre en un solo mapa.

El plano de las catacumbas es ASCII (celda = 4 m). x = columna * 400, y = fila * 400.
Leyenda: '#' roca · '.' piso · S losa del despertar · W armas · D daga · P reja (puerta)
A altar · R recuerdo · E agua quieta (espejo) · L inscripción · C restos · B estandarte
c cadena-ancla · h huesos · Z zombi · K esqueleto · F espectro · f espíritu atado · X salida
T reja de la tentación (la daga detrás) · Y el muerto junto a la reja (Levantar / Dar descanso / Examinar)

Uso (editor cerrado; borrar antes Content/Vaelith/Mapas/Lvl_Vaelith.umap si existe):
  tools/ue/correr.sh tools/ue/construir_nivel.py
"""
import math
import random
from collections import deque

PLANO = [
    "##########################",
    "#...######################",
    "#.S.W#####################",
    "#...######################",
    "##P#######################",
    "##.######....L.###########",
    "##.Z...E.......###########",
    "#######..A..R..###########",
    "##############.###########",
    "##############P###########",
    "#########DTY...K....c#####",
    "#############.....f..#####",
    "#############.C..B..h#####",
    "#########..K..F..R..A#####",
    "################X#########",
    "################.#########",
]
CELDA = 400.0
ALTO = 400.0

# Datos por celda (fila, columna)
PUERTAS = {(4, 2): ("puerta_1", "armas"), (9, 14): ("puerta_2", "recuerdo_1")}
ALTARES = {(7, 9): ("altar_1", "lectura_altar"), (13, 20): ("altar_2", "")}
RECUERDOS = {(7, 12): 1, (13, 17): 2}
TRIGGERS = [  # (fila, col, escena, penumbra, música)
    ((5, 2), "zona_catacumba", 1.0, "mus_catacumba"),
    ((6, 4), "primer_enemigo", -1.0, ""),
    ((7, 7), "sombra_vista", -1.0, ""),
    ((10, 14), "zona_osario", 1.0, "mus_catacumba"),
    ((11, 16), "primer_atado", -1.0, ""),
]


def abierta(f, c):
    return 0 <= f < len(PLANO) and 0 <= c < len(PLANO[f]) and PLANO[f][c] != "#"


def verificar_plano():
    """Todas las celdas abiertas son alcanzables desde S (oráculo del plano)."""
    abiertas = {(f, c) for f in range(len(PLANO)) for c in range(len(PLANO[f])) if abierta(f, c)}
    inicio = next((f, c) for (f, c) in abiertas if PLANO[f][c] == "S")
    vistos, cola = {inicio}, deque([inicio])
    while cola:
        f, c = cola.popleft()
        for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (f + df, c + dc)
            if n in abiertas and n not in vistos:
                vistos.add(n)
                cola.append(n)
    sueltas = abiertas - vistos
    assert not sueltas, f"celdas inalcanzables: {sorted(sueltas)}"
    return len(abiertas)


if __name__ == "__main__" and "unreal" not in globals():
    try:
        import unreal  # noqa: F401
    except ImportError:
        print("plano OK:", verificar_plano(), "celdas")
        raise SystemExit(0)

import unreal  # noqa: E402

actores = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
niveles = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eal = unreal.EditorAssetLibrary
rnd = random.Random(1793)
RUTA_MAPA = "/Game/Vaelith/Mapas/Lvl_Vaelith"


def malla(ruta):
    return unreal.load_asset(ruta) if eal.does_asset_exist(ruta) else None


CUBO = unreal.load_asset("/Engine/BasicShapes/Cube")
PLANO_M = unreal.load_asset("/Engine/BasicShapes/Plane")
MAT = {n: malla(f"/Game/Vaelith/Materiales/{n}") for n in
       ("M_Piedra", "M_Piso", "M_Metal", "M_Suelo_Bosque", "M_Roca", "M_Piedra_Negra", "M_Emisivo", "M_Piedra_DosCaras", "M_Agua",
        "M_Ladrillo_Quemado", "M_Sombra", "M_Madera", "M_Suelo_Cementerio")}
MAT["M_Oro"] = malla("/Game/Vaelith/Mallas/Osario/M_Oro")
M = lambda kit, n: malla(f"/Game/Vaelith/Mallas/{kit}/{n}")
PARED = M("Catacumba", "SM_Pared_4m")
PARED_NICHOS = M("Catacumba", "SM_Pared_Nichos_4m")
BOVEDA = M("Catacumba", "SM_Boveda_4m")
REJA = M("Catacumba", "SM_Reja")


def v(x, y, z):
    return unreal.Vector(x, y, z)


def poner(asset, pos, yaw=0.0, escala=(1, 1, 1), mat=None, carpeta=None, sombra=True):
    a = actores.spawn_actor_from_object(asset, pos, unreal.Rotator(0, 0, yaw))
    if not a:
        return None
    a.set_actor_scale3d(unreal.Vector(*escala))
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    if comp:
        if mat:
            comp.set_material(0, mat)
        comp.set_cast_shadow(sombra)
    if carpeta:
        a.set_folder_path(carpeta)
    return a


def caja(pos, tam, mat, carpeta):
    """Cubo de motor (1 m) escalado; el material de mundo lo hace leerse como piedra."""
    return poner(CUBO, pos, 0.0, (tam[0] / 100, tam[1] / 100, tam[2] / 100), mat, carpeta)


def centro(f, c):
    return c * CELDA, f * CELDA


def luz_puntual(pos, color, intensidad, radio, sombras=False, carpeta="Luces"):
    a = actores.spawn_actor_from_class(unreal.PointLight, pos)
    lc = a.get_component_by_class(unreal.PointLightComponent)
    lc.set_mobility(unreal.ComponentMobility.MOVABLE)  # sin luz horneada (r.AllowStaticLighting=False)
    lc.set_editor_property("intensity_units", unreal.LightUnits.UNITLESS)
    lc.set_intensity(intensidad)
    lc.set_light_color(color)
    lc.set_attenuation_radius(radio)
    lc.set_cast_shadows(sombras)
    a.set_folder_path(carpeta)
    return a


def interactuable(tipo, pos, yaw, asset, id_="", escena="", valor=0, requisito="", etiqueta="", escala=(1, 1, 1)):
    a = actores.spawn_actor_from_class(unreal.Interactuable, pos, unreal.Rotator(0, 0, yaw))
    a.set_editor_property("tipo", tipo)
    if id_:
        a.set_editor_property("id", id_)
    if escena:
        a.set_editor_property("escena", escena)
    a.set_editor_property("valor", valor)
    if requisito:
        a.set_editor_property("requisito", requisito)
    if etiqueta:
        a.set_editor_property("etiqueta", etiqueta)
    m = a.get_editor_property("malla")
    if asset:
        m.set_static_mesh(asset)
    a.set_actor_scale3d(unreal.Vector(*escala))
    a.set_folder_path("Interactuables")
    return a


def opcion(etiqueta, efecto, hab=None, cd=15, exito="", critico="", fallo="", requisito="", objetivo="", gracia=0,
           corrupcion=0, anatema=False, terminal=True, objeto=""):
    """Una vía para resolver un obstáculo (FOpcionInteraccion). hab: nombre de unreal.Habilidad (ATLETISMO, RELIGION...)."""
    o = unreal.OpcionInteraccion()
    o.set_editor_property("etiqueta", etiqueta)
    o.set_editor_property("efecto", getattr(unreal.EfectoOpcion, efecto))
    o.set_editor_property("habilidad", getattr(unreal.Habilidad, hab) if hab else unreal.Habilidad.NINGUNA)
    o.set_editor_property("cd", cd)
    o.set_editor_property("escena_exito", exito)
    o.set_editor_property("escena_critico", critico)
    o.set_editor_property("escena_fallo", fallo)
    if requisito:
        o.set_editor_property("requisito", requisito)
    if objetivo:
        o.set_editor_property("objetivo", objetivo)
    o.set_editor_property("gracia", gracia)
    o.set_editor_property("corrupcion", corrupcion)
    o.set_editor_property("anatema", anatema)
    o.set_editor_property("terminal", terminal)
    o.set_editor_property("objeto", objeto)
    return o


def con_opciones(actor, lista):
    actor.set_editor_property("opciones", lista)
    return actor


def no_muerto(tipo, pos, yaw, hecho, ancla=None, vision=1400.0):
    a = actores.spawn_actor_from_class(unreal.NoMuerto, pos, unreal.Rotator(0, 0, yaw))
    a.set_editor_property("tipo", tipo)
    a.set_editor_property("hecho", hecho)
    a.set_editor_property("distancia_vision", vision)
    if ancla:
        a.set_editor_property("ancla", ancla)
    a.set_folder_path("NoMuertos")
    return a


def trigger(pos, extension, escena="", penumbra=-1.0, musica="", jefe=False):
    a = actores.spawn_actor_from_class(unreal.TriggerGuion, pos)
    a.get_editor_property("caja").set_box_extent(unreal.Vector(*extension))
    a.set_editor_property("escena", escena)
    a.set_editor_property("penumbra", penumbra)
    a.set_editor_property("musica", musica)
    a.set_editor_property("jefe", jefe)
    a.set_folder_path("Guion")
    return a


ANTORCHAS = 0


def sonido_3d(nombre, pos, radio, volumen):
    s = unreal.load_asset(f"/Game/Vaelith/Audio/{nombre}")
    if not s:
        return None
    a = actores.spawn_actor_from_class(unreal.AmbientSound, pos)
    c = a.get_component_by_class(unreal.AudioComponent)
    c.set_sound(s)
    c.set_editor_property("volume_multiplier", volumen)
    c.set_editor_property("override_attenuation", True)
    at = c.get_editor_property("attenuation_overrides")
    at.set_editor_property("attenuate", True)
    at.set_editor_property("spatialize", True)
    at.set_editor_property("falloff_distance", radio)
    c.set_editor_property("attenuation_overrides", at)
    a.set_folder_path("Sonido")
    return a


def antorcha(x, y, yaw_hacia_pasillo):
    """Soporte en la pared + luz cálida sin sombras."""
    nueva = malla("/Game/Vaelith/Ext/props/SM_Antorcha_Pared")
    if nueva:  # la antorcha escaneada mira a su +Y local
        rad0 = math.radians(yaw_hacia_pasillo)
        poner(nueva, v(x + math.cos(rad0) * 12, y + math.sin(rad0) * 12, 255), yaw_hacia_pasillo - 90, (1.3, 1.3, 1.3),
              carpeta="Catacumba/Antorchas", sombra=False)
    elif M("Osario", "SM_Soporte_Antorcha"):
        poner(M("Osario", "SM_Soporte_Antorcha"), v(x, y, 250), yaw_hacia_pasillo, carpeta="Catacumba/Antorchas", sombra=False)
    rad = math.radians(yaw_hacia_pasillo)
    global ANTORCHAS
    ANTORCHAS += 1
    if ANTORCHAS % 2 == 0:
        sonido_3d("amb_antorcha", v(x, y, 260), 650.0, 0.5)
    luz_puntual(v(x + math.cos(rad) * 60, y + math.sin(rad) * 60, 290), unreal.LinearColor(1.0, 0.55, 0.25), 2600.0, 950.0)


# ---------------------------------------------------------------- catacumbas

def construir_catacumbas():
    puestas = 0
    for f, fila in enumerate(PLANO):
        for c, ch in enumerate(fila):
            if ch == "#":
                continue
            x, y = centro(f, c)
            caja(v(x, y, -25), (CELDA, CELDA, 50), MAT["M_Piso"], "Catacumba/Piso")
            if ch != "X" and not (f == len(PLANO) - 1):
                if BOVEDA:
                    poner(BOVEDA, v(x, y, 0), 0, carpeta="Catacumba/Techo")
                    caja(v(x, y, 545), (CELDA, CELDA, 50), MAT["M_Piedra"], "Catacumba/Techo")  # tapa: que no entre la luna
                else:
                    caja(v(x, y, ALTO + 25), (CELDA, CELDA, 50), MAT["M_Piedra"], "Catacumba/Techo")
            # Muros donde la celda vecina es roca
            for df, dc, yaw in ((-1, 0, 0), (1, 0, 180), (0, -1, 270), (0, 1, 90)):
                if abierta(f + df, c + dc):
                    continue
                if f + df >= len(PLANO):
                    continue  # la salida al bosque queda abierta
                wx, wy = x + dc * CELDA / 2, y + df * CELDA / 2
                if PARED_NICHOS and rnd.random() < 0.35:
                    poner(PARED_NICHOS, v(wx, wy, 0), yaw, carpeta="Catacumba/Muros")
                elif PARED:
                    poner(PARED, v(wx, wy, 0), yaw, carpeta="Catacumba/Muros")
                else:
                    tam = (CELDA + 50, 50, ALTO) if df != 0 else (50, CELDA + 50, ALTO)
                    caja(v(wx, wy, ALTO / 2), tam, MAT["M_Piedra"], "Catacumba/Muros")
                puestas += 1
                if puestas % 4 == 0:
                    # Antorcha mirando hacia el centro de la celda.
                    hacia = math.degrees(math.atan2(y - wy, x - wx))
                    antorcha(wx + (x - wx) * 0.12, wy + (y - wy) * 0.12, hacia)
    unreal.log(f"[vaelith] catacumbas: {puestas} muros")


def poblar_catacumbas():
    D = lambda n: M("Despertar", n)
    O = lambda n: M("Osario", n)
    T = lambda n: unreal.load_asset(f"/Game/Vaelith/Armas/{n}")
    anclas = {}
    for f, fila in enumerate(PLANO):
        for c, ch in enumerate(fila):
            x, y = centro(f, c)
            p = v(x, y, 0)
            h = f"nm_{f}_{c}"
            if ch == "S":
                if D("SM_Losa_Altar"):
                    poner(D("SM_Losa_Altar"), p, 0, carpeta="Catacumba/Despertar")
                for k, (dx, dy) in enumerate(((-150, -150), (150, -150), (-150, 150), (150, 150))):
                    col = D("SM_Columna_Rota_Alta") if k % 2 == 0 else D("SM_Columna_Rota_Baja")
                    if col:
                        poner(col, v(x + dx, y + dy, 0), rnd.uniform(0, 360), carpeta="Catacumba/Despertar")
                if O("SM_Candelabro_Suelo"):
                    poner(O("SM_Candelabro_Suelo"), v(x + 120, y - 60, 0), 0, carpeta="Catacumba/Despertar")
                luz_puntual(v(x + 120, y - 60, 180), unreal.LinearColor(1.0, 0.6, 0.3), 2200.0, 800.0, True)
                start = actores.spawn_actor_from_class(unreal.PlayerStart, v(x, y, 71 + 100), unreal.Rotator(0, 0, 0))
                start.set_folder_path("Guion")
            elif ch == "W":
                if O("SM_Sarcofago"):
                    poner(O("SM_Sarcofago"), p, 90, carpeta="Catacumba/Props")
                interactuable(unreal.TipoInteractuable.ARMAS, v(x, y, 95), 90, T("SM_Espada_Larga"), "armas", "armas")
            elif ch == "D":
                if O("SM_Cofre"):
                    poner(O("SM_Cofre"), p, 0, carpeta="Catacumba/Props")
                interactuable(unreal.TipoInteractuable.DAGA_PHARASMA, v(x, y, 62), 0, T("SM_Daga_Pharasma"), "daga", "daga")
            elif ch == "T":
                # La reja de la tentación: tres vías (fuerza, fe o necromancia). La daga de Pharasma está detrás.
                reja = interactuable(unreal.TipoInteractuable.PUERTA, p, 90, REJA or CUBO, "reja_tentacion", "", 0, "",
                                     etiqueta="Abrir la reja")
                if not REJA:
                    reja.set_actor_scale3d(unreal.Vector(3.9, 0.15, 3.5))
                con_opciones(reja, [
                    opcion("Forzar la reja", "ABRIR", "ATLETISMO", 18, "reja_forzada", "", "reja_firme"),
                    opcion("Rezar ante el sello de Pharasma", "ABRIR", "RELIGION", 16, "reja_rezada", "", "reja_sello_mudo"),
                ])
            elif ch == "Y":
                muerto = interactuable(unreal.TipoInteractuable.CADAVER, v(x - 60, y + 90, 0), 200, O("SM_Pila_Huesos"), "muerto_reja",
                                       etiqueta="El muerto junto a la reja")
                con_opciones(muerto, [
                    opcion("Examinar los restos", "DIAGNOSTICAR", "SABER_OSARIO", 15, "diag_tentacion", "diag_tentacion_critico",
                           "diag_fallo", terminal=False),
                    opcion("Darle descanso", "DAR_DESCANSO", exito="tentacion_descanso", gracia=1),
                    opcion("Levantar al muerto", "LEVANTAR", exito="tentacion_levantar", objetivo="reja_tentacion", gracia=-1,
                           corrupcion=1, anatema=True),
                ])
                if O("SM_Craneo"):
                    poner(O("SM_Craneo"), v(x - 20, y + 140, 0), 30, carpeta="Catacumba/Props")
            elif ch == "P":
                id_, req = PUERTAS[(f, c)]
                yaw = 90 if abierta(f, c - 1) or abierta(f, c + 1) else 0
                if REJA:
                    interactuable(unreal.TipoInteractuable.PUERTA, p, yaw, REJA, id_, "", 0, req)
                else:
                    a = interactuable(unreal.TipoInteractuable.PUERTA, v(x, y, 175), yaw, CUBO, id_, "", 0, req, escala=(3.9, 0.15, 3.5))
                    a.get_editor_property("malla").set_material(0, MAT["M_Metal"])
            elif ch == "A":
                id_, escena = ALTARES[(f, c)]
                interactuable(unreal.TipoInteractuable.ALTAR, p, 180, O("SM_Altar_Pharasma"), id_, escena)
            elif ch == "R":
                n = RECUERDOS[(f, c)]
                if O("SM_Pila_Huesos"):
                    poner(O("SM_Pila_Huesos"), v(x - 120, y + 100, 0), rnd.uniform(0, 360), carpeta="Catacumba/Props")
                interactuable(unreal.TipoInteractuable.RECUERDO, v(x, y, 0), 0, O("SM_Urna"), f"recuerdo_{n}", "", n, etiqueta="Tocar la urna")
            elif ch == "E":
                agua = poner(PLANO_M, v(x, y, 3), 0, (3.2, 3.2, 1), MAT["M_Agua"] or MAT["M_Metal"], "Catacumba/Props")
                sonido_3d("amb_agua", v(x, y, 50), 800.0, 0.6)
                interactuable(unreal.TipoInteractuable.ESPEJO, v(x, y + 170, 0), 0, D("SM_Escombro_02"), "espejo", "espejo_agua")
            elif ch == "L":
                interactuable(unreal.TipoInteractuable.LECTURA, v(x, y - 180, 120), 0, O("SM_Losa_Nombre"), "", "lectura_nichos")
            elif ch == "C":
                restos = interactuable(unreal.TipoInteractuable.CADAVER, p, rnd.uniform(0, 360), O("SM_Pila_Huesos"), f"cadaver_{f}_{c}",
                                       etiqueta="Restos de un aventurero")
                con_opciones(restos, [
                    opcion("Cubrir los restos", "DAR_DESCANSO", exito="cadaver", gracia=1),
                    opcion("Examinar los restos", "DIAGNOSTICAR", "SABER_OSARIO", 14, "diag_restos", "", "diag_fallo", terminal=False),
                    opcion("Tomar el frasco de su cintura", "TOMAR", exito="robo_restos", objeto="pocion", corrupcion=1, anatema=True),
                ])
            elif ch == "B":
                interactuable(unreal.TipoInteractuable.LECTURA, p, 30, O("SM_Estandarte_Roto"), "", "estandarte", etiqueta="Mirar el estandarte")
            elif ch == "c":
                anclas[(f, c)] = interactuable(unreal.TipoInteractuable.ANCLA, v(x, y, 180), 0, O("SM_Cadena_Ancla"), f"ancla_{f}_{c}")
            elif ch == "h":
                if O("SM_Pila_Huesos"):
                    poner(O("SM_Pila_Huesos"), p, rnd.uniform(0, 360), carpeta="Catacumba/Props")
                if O("SM_Sarcofago"):
                    poner(O("SM_Sarcofago"), v(x + 100, y, 0), 0, carpeta="Catacumba/Props")
            elif ch == "Z":
                no_muerto(unreal.TipoNoMuerto.ZOMBI, v(x, y, 100), 180, h)
            elif ch == "K":
                no_muerto(unreal.TipoNoMuerto.ESQUELETO, v(x, y, 100), 180, h)
            elif ch == "F":
                no_muerto(unreal.TipoNoMuerto.FANTASMA, v(x, y, 150), 180, h)
    # Espíritus atados: se enlazan con la cadena más cercana.
    for f, fila in enumerate(PLANO):
        for c, ch in enumerate(fila):
            if ch == "f":
                x, y = centro(f, c)
                cerca = min(anclas.items(), key=lambda kv: abs(kv[0][0] - f) + abs(kv[0][1] - c))[1] if anclas else None
                no_muerto(unreal.TipoNoMuerto.FANTASMA, v(x, y, 150), 180, f"nm_{f}_{c}", cerca)
    for (f, c), escena, pen, mus in TRIGGERS:
        x, y = centro(f, c)
        trigger(v(x, y, 200), (190, 190, 200), escena, pen, mus)
    # sombra_vista: "restos cortados hace poco, cortes limpios" (fila 7, col 7)
    x, y = centro(7, 7)
    for dx, dy, giro in ((-110, 60, 20), (90, -80, 200)):
        poner(O("SM_Pila_Huesos"), v(x + dx, y + dy, 0), giro, (0.8, 0.8, 0.8), carpeta="Catacumba/Props")
    poner(O("SM_Craneo"), v(x + 20, y + 120, 0), 75, carpeta="Catacumba/Props")
    # escudo partido de un tajo limpio: dos mitades separadas
    for lado in (-1, 1):
        a = caja(v(x + lado * 55, y - 20, 6), (70, 4, 90), MAT["M_Metal"], "Catacumba/Props")
        a.set_actor_rotation(unreal.Rotator(lado * 8, 88, rnd.uniform(0, 360)), False)


# ---------------------------------------------------------------- exterior (terreno de tools/terreno.py)

import json  # noqa: E402
import os  # noqa: E402
import sys  # noqa: E402

_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_RAIZ, "tools"))
import terreno as TER  # noqa: E402

E = lambda kit, n: malla(f"/Game/Vaelith/Ext/{kit}/{n}")
H = TER.altura
SALIDA = (len(PLANO) - 1, PLANO[-1].index("."))
TORRE = TER.TORRE
ENTRADA_TORRE = math.degrees(math.atan2(TER.LOMA[1] - TORRE[1], TER.LOMA[0] - TORRE[0]))  # mira hacia la loma
CAMINO = [(6400.0, 21400.0), (7000.0, 26000.0), (8200.0, 30500.0), (8200.0, 35500.0), (10500.0, 39000.0),
          (13500.0, 43000.0), (15500.0, 46000.0)]
GUIAS = [(12500.0, 49500.0), (7000.0, 51500.0), (1500.0, 53800.0), (-3500.0, 55000.0), (-7600.0, 57600.0)]


def vt(x, y, dz=0.0):
    """Punto apoyado en el terreno."""
    return v(x, y, H(x, y) + dz)


def dist_segmentos(x, y, puntos):
    mejor = 1e9
    for (ax, ay), (bx, by) in zip(puntos, puntos[1:]):
        dx, dy = bx - ax, by - ay
        t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)))
        mejor = min(mejor, math.hypot(x - (ax + t * dx), y - (ay + t * dy)))
    return mejor


def tapa_vista(x, y):
    """True si un árbol en (x, y) taparía el pueblo visto desde la loma (cuña de ±30° hacia el este)."""
    lx, ly = TER.LOMA
    px, py = TER.PUEBLO
    d = math.hypot(x - lx, y - ly)
    if d < 1500 or d > math.hypot(px - lx, py - ly) - TER.RADIO_PUEBLO:
        return False
    ang = math.degrees(math.atan2(y - ly, x - lx) - math.atan2(py - ly, px - lx))
    return abs((ang + 180) % 360 - 180) < 20


def en_pueblo(x, y, margen=0.0):
    px, py = TER.PUEBLO
    return math.hypot(x - px, (y - py) * 1.15) < TER.RADIO_PUEBLO + margen


def camino_pueblo():
    """Sendero de la loma a la puerta del pueblo (la puerta mira a la loma)."""
    lx, ly = TER.LOMA
    px, py = TER.PUEBLO
    a = math.atan2(ly - py, lx - px)
    puerta = (px + math.cos(a) * (TER.RADIO_PUEBLO - 400), py + math.sin(a) * (TER.RADIO_PUEBLO - 400) / 1.15)
    medio = ((lx + puerta[0]) / 2, (ly + puerta[1]) / 2 - 1500)
    return [(lx + 2500, ly), medio, puerta, (px, py)]


def lejos(a, distancia):
    """Distancia máxima de dibujo (sin Nanite, recortar lo lejano pesa menos que los LOD solos)."""
    if a:
        c = a.get_component_by_class(unreal.StaticMeshComponent)
        if c:
            c.set_editor_property("ld_max_draw_distance", distancia)
    return a


INSTANCIAS = {}  # (malla, distancia, sombra) -> [Transform]


def inclinado(asset, pos, yaw, escala, carpeta, inclinacion=6.0, distancia=0.0, sombra=True):
    """Copia instanciada (un componente por malla para todo el mapa): árboles, tumbas, cercas."""
    if not asset:
        return None
    rot = unreal.Rotator(rnd.uniform(-inclinacion, inclinacion), rnd.uniform(-inclinacion, inclinacion), yaw)
    t = unreal.Transform(pos, rot, unreal.Vector(*escala))
    INSTANCIAS.setdefault((asset.get_path_name(), distancia, sombra, carpeta.split("/")[1] if "/" in carpeta else carpeta), []).append(t)
    return None


def crear_instancias():
    por_zona = {}
    for (ruta, distancia, sombra, zona), ts in INSTANCIAS.items():
        g = unreal.GrupoInstancias()
        g.set_editor_property("malla", unreal.load_asset(ruta))
        g.set_editor_property("transformadas", ts)
        g.set_editor_property("distancia", distancia)
        g.set_editor_property("sombra", sombra)
        por_zona.setdefault(zona, []).append(g)
    total = 0
    for zona, grupos in por_zona.items():
        a = actores.spawn_actor_from_class(unreal.Instancias, v(0, 0, 0))
        a.set_editor_property("grupos", grupos)
        a.set_actor_label(f"Instancias_{zona}")
        a.set_folder_path("Exterior/Instancias")
        total += sum(len(g.get_editor_property("transformadas")) for g in grupos)
    unreal.log(f"[vaelith] instancias: {total} copias en {sum(len(g) for g in por_zona.values())} grupos")


def nav(cx, cy, mx, my, z0=-1500.0, z1=3000.0):
    a = actores.spawn_actor_from_class(unreal.NavMeshBoundsVolume, v(cx, cy, (z0 + z1) / 2))
    a.set_actor_scale3d(unreal.Vector(mx / 100.0, my / 100.0, (z1 - z0) / 200.0))
    a.set_folder_path("Guion")


def construir_terreno():
    with open(os.path.join(_RAIZ, "assets_fuente", "externos", "terreno", "baldosas.json"), encoding="utf-8") as f:
        piezas = json.load(f)
    n = 0
    for p in piezas:
        a = poner(E("terreno", p["nombre"]), v(p["x"], p["y"], 0), 0, carpeta="Exterior/Terreno")
        n += 1 if a else 0
    # Verificación: el suelo real coincide con la función de altura (detecta ejes invertidos)
    mundo = unreal.EditorLevelLibrary.get_editor_world()
    errores = []
    for x, y in ((6400, 12000), (16000, 47000), (-12000, 58000), (3000, 30000), (20000, 25000)):
        hit = unreal.SystemLibrary.line_trace_single(mundo, v(x, y, 8000), v(x, y, -8000), unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
                                                     True, [], unreal.DrawDebugTrace.NONE, True)
        if hit:
            z = hit.to_tuple()[4].z  # location
            errores.append(round(z - H(x, y)))
    unreal.log(f"[vaelith] terreno: {n} piezas; diferencia con la función en 5 puntos: {errores}")


def construir_cementerio():
    sx, sy = centro(*SALIDA)
    # Boca de la cripta: antorchas a los lados, estatuas y obeliscos
    for lado in (-1, 1):
        x = sx + lado * 260
        poner(E("props", "SM_Antorcha_Pared"), v(x, sy + 230, 260), -90 if lado < 0 else 90, (1.3, 1.3, 1.3), carpeta="Exterior/Cementerio")
        luz_puntual(v(x, sy + 330, 300), unreal.LinearColor(1.0, 0.55, 0.25), 2200.0, 900.0, False, "Exterior/Luces")
        poner(E("cementerio", "SM_Obelisco"), vt(sx + lado * 700, sy + 900), 0, carpeta="Exterior/Cementerio")
    sonido_3d("amb_antorcha", v(sx, sy + 300, 260), 700.0, 0.5)
    trigger(v(sx, sy + 500, 250), (350, 250, 300), "zona_cementerio", 0.0, "mus_bosque")
    # Tumbas abiertas junto a la salida: "la tierra empujada desde abajo, nadie cavó"
    lapidas = [a for a in (E("cementerio", f"SM_Lapida_0{i}") for i in (1, 2, 3, 4)) if a]
    for i, (dx, dy) in enumerate(((-700, 1500), (650, 1750), (-520, 2450), (820, 2650))):
        gx, gy = sx + dx, sy + dy
        giro = rnd.uniform(-12, 12)
        fosa = caja(vt(gx, gy, 1), (110, 220, 4), MAT["M_Piedra_Negra"], "Exterior/Cementerio/Abiertas")
        fosa.set_actor_rotation(unreal.Rotator(0, 0, giro), False)
        for lado in (-1, 1):  # tierra volcada hacia afuera, a los dos lados
            ox = math.cos(math.radians(giro)) * 95 * lado
            oy = math.sin(math.radians(giro)) * 95 * lado
            monte = poner(unreal.load_asset("/Engine/BasicShapes/Sphere"), vt(gx + ox, gy + oy, -6), giro,
                          (0.7, 2.3, 0.5), MAT["M_Suelo_Cementerio"], "Exterior/Cementerio/Abiertas")
        if lapidas:
            l = poner(rnd.choice(lapidas), vt(gx, gy + 150, -10), rnd.uniform(160, 200), carpeta="Exterior/Cementerio/Abiertas")
            l.set_actor_rotation(unreal.Rotator(rnd.uniform(-14, 14), rnd.uniform(6, 16), 180 + giro), False)
        tapa = caja(vt(gx + 120 * (1 if i % 2 else -1), gy - 40, 12), (80, 200, 8), MAT["M_Madera"], "Exterior/Cementerio/Abiertas")
        tapa.set_actor_rotation(unreal.Rotator(rnd.uniform(-20, 20), rnd.uniform(-10, 10), giro + 25), False)
    sonido_3d("amb_viento", v(sx, 13000, 400), 9000.0, 0.35)

    lapidas = [("SM_Lapida_01", 1.0), ("SM_Lapida_02", 1.0), ("SM_Lapida_03", 1.0), ("SM_Lapida_04", 1.0),
               ("SM_Lapida_Vieja", 1.9), ("SM_Lapida_Musgo", 1.0), ("SM_Lapida_Vieja", 1.9), ("SM_Lapida_03", 1.0)]
    raras = [("SM_Tumba_Vieja", 1.3), ("SM_Tumbas_Grupo", 1.0), ("SM_Obelisco", 1.0)]
    puestas = 0
    y = 8600.0
    while y < 19400.0:
        x = 1900.0
        while x < 10900.0:
            if abs(x - sx) > 380 and rnd.random() < 0.5:
                nombre, esc = rnd.choice(raras) if rnd.random() < 0.08 else rnd.choice(lapidas)
                px, py = x + rnd.uniform(-60, 60), y + rnd.uniform(-50, 50)
                inclinado(E("cementerio", nombre), vt(px, py, -8), 180 + rnd.uniform(-12, 12), (esc, esc, esc),
                          "Exterior/Cementerio/Tumbas", 7.0, 6500.0)
                puestas += 1
            x += rnd.uniform(330, 420)
        y += rnd.uniform(420, 520)
    unreal.log(f"[vaelith] cementerio: {puestas} tumbas")
    # Árboles podados, muertos
    for _ in range(26):
        x, y = rnd.uniform(1600, 11200), rnd.uniform(8000, 19800)
        if abs(x - sx) < 500:
            continue
        s = rnd.uniform(0.9, 1.45)
        inclinado(E("cementerio", f"SM_Arbol_Podado_{rnd.randint(1, 4)}"), vt(x, y, -20), rnd.uniform(0, 360), (s, s, s),
                  "Exterior/Cementerio/Arboles", 4.0, 12000.0)
    # Cerca rota a los lados del sendero
    for lado in (-1, 1):
        y = 8200.0
        while y < 19800.0:
            if rnd.random() < 0.72:
                inclinado(E("cementerio", "SM_Cerca"), vt(sx + lado * 330, y, -5), 90 + rnd.uniform(-5, 5), (2.0, 2.0, 2.2),
                          "Exterior/Cementerio/Cerca", 8.0, 5000.0)
            y += 286.0
    # Hitos
    for x, y, yaw in ((2600, 15200, 0), (10200, 11800, 180)):
        poner(E("cementerio", "SM_Mausoleo_Relieve"), vt(x, y, -10), yaw, carpeta="Exterior/Cementerio")
    poner(E("cementerio", "SM_Pozo"), vt(9600, 16800, -5), 30, carpeta="Exterior/Cementerio")
    for x, y, yaw in ((5600, 12500, 90), (7200, 17600, -90)):
        poner(E("cementerio", "SM_Banco"), vt(x, y), yaw, (1.4, 1.4, 1.4), carpeta="Exterior/Cementerio")
    est = actores.spawn_actor_from_class(unreal.EstatuaGuia, vt(sx + 650, 10200), unreal.Rotator(0, 0, 200))
    est.set_editor_property("encendida_al_inicio", True)
    est.set_folder_path("Exterior/Cementerio")
    interactuable(unreal.TipoInteractuable.LECTURA, vt(sx - 900, 14200), 0, E("cementerio", "SM_Lapida_03"), "", "lectura_lapida",
                  etiqueta="Leer la lápida")
    interactuable(unreal.TipoInteractuable.CADAVER, vt(3400, 18200), 30, M("Osario", "SM_Sarcofago"), "cadaver_cementerio",
                  etiqueta="Cerrar la tumba abierta")
    # Muro del fondo con el arco en ruinas como única salida
    ax, ay = TER.ARCO
    x = 1200.0
    while x < 11600.0:
        if abs(x + 200 - ax) > 300:
            z = min(H(x, ay - 600), H(x + 400, ay - 600))
            caja(v(x + 200, ay - 600, z + 90), (400, 70, 380), MAT["M_Piedra"], "Exterior/Cementerio/Muro")
        x += 400.0
    poner(E("ruinas", "SM_Arco_Ruina"), v(ax, ay, min(H(ax, ay - 650), H(ax, ay + 650)) - 20), 0, carpeta="Exterior/Cementerio")
    trigger(v(ax, ay + 900, H(ax, ay + 900) + 200), (300, 200, 300), "zona_bosque", 0.0, "mus_bosque")
    # Los muertos de Varo
    for i, (x, y) in enumerate(((4200, 11500), (8800, 13800), (5000, 17000))):
        no_muerto(unreal.TipoNoMuerto.ESQUELETO, vt(x, y, 100), 180, f"nm_cem_{i}")
    no_muerto(unreal.TipoNoMuerto.ZOMBI, vt(7600, 19000, 100), 180, "nm_cem_z")
    nav(6400, 13800, 5600, 7800)


def construir_bosque():
    pinos = [a for a in (E("bosque", "SM_Abeto_A"), E("bosque", "SM_Abeto_B"), E("bosque", "SM_Abeto_C")) if a] or \
        [a for a in (M("Bosque", "SM_Pino_A"), M("Bosque", "SM_Pino_B")) if a]
    muertos = [M("Bosque", "SM_Roble_Muerto")] + [E("cementerio", f"SM_Arbol_Podado_{i}") for i in (1, 2, 4)]
    muertos = [a for a in muertos if a]
    T = lambda n: M("Torre", n)
    # Bosque alto (entre el arco y la loma): pinos con sendero
    puestos, intentos = 0, 0
    while puestos < 650 and intentos < 20000:
        intentos += 1
        x, y = rnd.uniform(-6000, 26500), rnd.uniform(21600, 46000)
        if dist_segmentos(x, y, CAMINO) < 520 or abs(y - TER.ARROYO_Y) < 450 or math.hypot(x - TER.LOMA[0], y - TER.LOMA[1]) < 4200:
            continue
        if x < 3000 and y > 43000:
            continue  # eso es bosque oscuro
        if tapa_vista(x, y):
            continue
        s = rnd.uniform(0.85, 1.5)
        inclinado(rnd.choice(pinos), vt(x, y, -30), rnd.uniform(0, 360), (s, s, s * rnd.uniform(0.95, 1.2)), "Exterior/Bosque/Arboles", 3.0, 14000.0)
        puestos += 1
    # Bosque oscuro: denso, sin sendero, troncos muertos mezclados
    oscuros = 0
    intentos = 0
    while oscuros < 1800 and intentos < 40000:
        intentos += 1
        x, y = rnd.uniform(-21000, 3000), rnd.uniform(43000, 63000)
        dt = math.hypot(x - TORRE[0], y - TORRE[1])
        boca = (TORRE[0] + math.cos(math.radians(ENTRADA_TORRE)) * 4800, TORRE[1] + math.sin(math.radians(ENTRADA_TORRE)) * 4800)
        if dist_segmentos(x, y, [TORRE, boca]) < 450:
            continue  # boca del arco despejada
        if dt < 1900 or dist_segmentos(x, y, GUIAS) < 260 and rnd.random() < 0.7:
            continue
        s = rnd.uniform(0.9, 1.7)
        asset = rnd.choice(muertos) if rnd.random() < 0.25 else rnd.choice(pinos)
        inclinado(asset, vt(x, y, -30), rnd.uniform(0, 360), (s, s, s * rnd.uniform(1.0, 1.3)), "Exterior/BosqueOscuro/Arboles", 5.0, 7000.0)
        oscuros += 1
    # Transición loma -> bosque oscuro: arboleda rala (claros que dejan ver las estatuas de lejos)
    ralos, intentos = 0, 0
    while ralos < 320 and intentos < 12000:
        intentos += 1
        x, y = rnd.uniform(3000, 26500), rnd.uniform(46000, 63500)
        if math.hypot(x - TER.LOMA[0], y - TER.LOMA[1]) < 5200 or dist_segmentos(x, y, GUIAS) < 700 or tapa_vista(x, y):
            continue
        s = rnd.uniform(0.85, 1.5)
        inclinado(rnd.choice(pinos), vt(x, y, -30), rnd.uniform(0, 360), (s, s, s * rnd.uniform(0.95, 1.2)), "Exterior/Bosque/Arboles", 3.0, 14000.0)
        ralos += 1
    # Bosque del este: entre la loma y el pueblo, y al sur del pueblo. Deja libre el sendero, la vista y la meseta
    este, intentos = 0, 0
    sendero = camino_pueblo()
    while este < 700 and intentos < 30000:
        intentos += 1
        x, y = rnd.uniform(26500, 57000), rnd.uniform(21600, 63500)
        if en_pueblo(x, y, 1800) or dist_segmentos(x, y, sendero) < 700 or tapa_vista(x, y):
            continue
        if math.hypot(x - TER.LOMA[0], y - TER.LOMA[1]) < 5200:
            continue
        s_ = rnd.uniform(0.85, 1.5)
        asset = rnd.choice(muertos) if rnd.random() < 0.08 else rnd.choice(pinos)
        inclinado(asset, vt(x, y, -30), rnd.uniform(0, 360), (s_, s_, s_ * rnd.uniform(0.95, 1.2)), "Exterior/Bosque/Arboles", 3.0, 14000.0)
        este += 1
    unreal.log(f"[vaelith] bosque: {puestos} árboles en el alto, {oscuros} en el oscuro, {ralos} ralos, {este} al este")
    # Rocas y raíces
    for _ in range(60):
        x, y = rnd.uniform(-20000, 26000), rnd.uniform(21600, 63000)
        if dist_segmentos(x, y, CAMINO) < 450:
            continue
        if rnd.random() < 0.5:
            poner(T("SM_Roca_Grande"), vt(x, y, -60), rnd.uniform(0, 360), (rnd.uniform(0.6, 1.6),) * 3, None, "Exterior/Bosque/Rocas")
        else:
            lejos(poner(E("bosque", "SM_Raiz"), vt(x, y, -20), rnd.uniform(0, 360), (1.2, 1.2, 1.2), None, "Exterior/Bosque/Rocas"), 6000.0)
    # Arroyo: tramos de agua siguiendo el fondo del barranco, y el puente
    x = TER.X0
    while x < TER.X1:
        z = min(H(x + d, TER.ARROYO_Y) for d in (0, 500, 1000))
        poner(PLANO_M, v(x + 500, TER.ARROYO_Y, z + 35), 0, (10.2, 6.5, 1), MAT["M_Agua"], "Exterior/Bosque/Arroyo", False)
        x += 1000.0
    px, py = TER.PUENTE
    zp = min(H(px, py - 600), H(px, py + 600)) - 140
    poner(E("bosque", "SM_Puente"), v(px, py, zp), 90, carpeta="Exterior/Bosque")
    sonido_3d("amb_agua", v(px, py, zp + 100), 2600.0, 0.8)
    sonido_3d("amb_viento", v(8000, 30000, 600), 12000.0, 0.3)
    # Centinela junto al sendero, recuerdo 3 en un claro pasando el puente
    no_muerto(unreal.TipoNoMuerto.GUARDIAN, vt(7600, 25500, 100), 200, "guardian")
    # Su puesto: un estandarte clavado. Desde ahí se lo puede examinar o relevar de la guardia (la orden fue de Vaelith).
    puesto = interactuable(unreal.TipoInteractuable.LECTURA, vt(7400, 25300), 200, M("Osario", "SM_Estandarte_Roto"), "puesto_guardian",
                           etiqueta="El puesto del centinela")
    con_opciones(puesto, [
        opcion("Examinar al centinela", "DIAGNOSTICAR", "SABER_OSARIO", 15, "diag_guardian", "diag_guardian_critico", "diag_fallo",
               terminal=False),
        opcion("Relevarlo de la guardia", "RELEVAR", objetivo="guardian", exito=""),
    ])
    interactuable(unreal.TipoInteractuable.RECUERDO, vt(11200, 37000), 0, M("Osario", "SM_Urna"), "recuerdo_3", "", 3, etiqueta="Tocar la urna")
    poner(M("Osario", "SM_Estandarte_Roto"), vt(11400, 36800), 70, carpeta="Exterior/Bosque")
    luz_puntual(vt(11200, 37000, 250), unreal.LinearColor(0.7, 0.75, 1.0), 1500.0, 700.0)
    no_muerto(unreal.TipoNoMuerto.ESQUELETO, vt(7400, 29000, 100), 0, "nm_bosque_1")
    no_muerto(unreal.TipoNoMuerto.ZOMBI, vt(9000, 38500, 100), 0, "nm_bosque_3")
    no_muerto(unreal.TipoNoMuerto.FANTASMA, vt(12500, 41500, 160), 0, "nm_bosque_2")
    for (ax, ay), (bx, by) in zip(CAMINO, CAMINO[1:]):
        nav((ax + bx) / 2, (ay + by) / 2, abs(bx - ax) / 2 + 2500, abs(by - ay) / 2 + 2500)
    # Loma: claro con vista al pueblo
    lx, ly = TER.LOMA
    for _ in range(7):
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(1500, 3500)
        poner(T("SM_Roca_Grande"), vt(lx + math.cos(a) * r, ly + math.sin(a) * r, -50), rnd.uniform(0, 360), (rnd.uniform(0.5, 1.2),) * 3, None, "Exterior/Loma")
    trigger(vt(lx + 600, ly, 200), (900, 900, 400), "vista_pueblo", 0.0, "")
    # Bosque oscuro: estatuas guía (se encienden al pasar), un cadáver en un ramal ciego
    for i, (gx, gy) in enumerate(GUIAS):
        sig = GUIAS[i + 1] if i + 1 < len(GUIAS) else TORRE
        yaw = math.degrees(math.atan2(sig[1] - gy, sig[0] - gx))
        g = actores.spawn_actor_from_class(unreal.EstatuaGuia, vt(gx, gy, -5), unreal.Rotator(0, 0, yaw))
        if i == 0:
            g.set_editor_property("escena", "estatua_guia")
        g.set_folder_path("Exterior/BosqueOscuro")
    huesos = interactuable(unreal.TipoInteractuable.CADAVER, vt(-15000, 47500), 10, M("Osario", "SM_Pila_Huesos"), "cadaver_bosque",
                           etiqueta="Huesos sin enterrar")
    con_opciones(huesos, [
        opcion("Enterrar los huesos", "DAR_DESCANSO", exito="cadaver", gracia=1),
        opcion("Examinar los huesos", "DIAGNOSTICAR", "SABER_OSARIO", 15, "diag_huesos", "", "diag_fallo", terminal=False),
    ])
    no_muerto(unreal.TipoNoMuerto.FANTASMA, vt(4000, 52500, 160), 0, "nm_oscuro_1")
    no_muerto(unreal.TipoNoMuerto.ESQUELETO, vt(-5000, 54000, 100), 0, "nm_oscuro_2")
    no_muerto(unreal.TipoNoMuerto.FANTASMA, vt(-9500, 51000, 160), 0, "nm_oscuro_3")
    nav(-4000, 53500, 9000, 6000)
    interactuable(unreal.TipoInteractuable.ALTAR, vt(TORRE[0] + 3600 * math.cos(math.radians(ENTRADA_TORRE)),
                                                     TORRE[1] + 3600 * math.sin(math.radians(ENTRADA_TORRE))), ENTRADA_TORRE + 180,
                  M("Osario", "SM_Altar_Pharasma"), "altar_3")
    trigger(vt(TORRE[0], TORRE[1], 300), (3600, 3600, 900), "hondonada", 0.2, "")


def construir_pueblo():
    """Pueblo de Varo, a ~280 m de la loma, sobre su meseta: se baja por un sendero y se entra por la puerta
    de la empalizada. Iglesia en la plaza, casas en anillo mirando al centro, faroles cálidos."""
    poner(E("terreno", "SM_Valle"), v((TER.VALLE_X0 + TER.VALLE_X1) / 2, (TER.VALLE_Y0 + TER.VALLE_Y1) / 2, 0), 0, carpeta="Exterior/Valle")
    px, py = TER.PUEBLO
    lx, ly = TER.LOMA
    a_puerta = math.atan2(ly - py, lx - px)
    casas = [c for c in (E("pueblo", f"SM_Casa_{c}") for c in "ABCDEF") if c]
    poner(E("pueblo", "SM_Iglesia_Pueblo"), vt(px, py, -40), math.degrees(a_puerta) + 90, carpeta="Exterior/Pueblo")
    # Casas: dos anillos; ninguna en la calle que va de la puerta a la iglesia
    puestas = []
    for anillo, n in ((2600.0, 7), (4100.0, 9)):
        for k in range(n):
            a = a_puerta + 2 * math.pi * (k + 0.5) / n + rnd.uniform(-0.12, 0.12)
            if abs(((a - a_puerta) + math.pi) % (2 * math.pi) - math.pi) < 0.38:
                continue  # calle principal
            x, y = px + math.cos(a) * anillo, py + math.sin(a) * anillo / 1.15
            if any(math.hypot(x - qx, y - qy) < 1500 for qx, qy in puestas):
                continue
            puestas.append((x, y))
            yaw = math.degrees(math.atan2(py - y, px - x)) + 90  # la fachada mira a la plaza
            poner(rnd.choice(casas), vt(x, y, -30), yaw + rnd.uniform(-8, 8), carpeta="Exterior/Pueblo")
            if rnd.random() < 0.7:  # ventana encendida en la fachada
                fx, fy = x + (px - x) / anillo * 480, y + (py - y) / anillo * 480
                caja(vt(fx, fy, rnd.uniform(220, 320)), (60, 60, 70), MAT["M_Emisivo"], "Exterior/Pueblo")
            if rnd.random() < 0.45:
                fx, fy = x + (px - x) / anillo * 650, y + (py - y) / anillo * 650
                luz_puntual(vt(fx, fy, 260), unreal.LinearColor(1.0, 0.58, 0.28), 1800.0, 900.0, False, "Exterior/Pueblo/Luces")
    # Empalizada: anillo con una puerta hacia la loma
    emp = E("pueblo", "SM_Empalizada_1") or E("pueblo", "SM_Empalizada_4")
    largo = 600.0
    if emp:
        caja_e = emp.get_bounding_box()
        largo = max(200.0, (caja_e.max.x - caja_e.min.x) * 1.3 - 20)  # tramo de troncos de ~6,7 m
    radio = TER.RADIO_PUEBLO - 350
    n = int(2 * math.pi * radio / largo) + 1
    for k in range(n):
        a = 2 * math.pi * k / n
        if abs(((a - a_puerta) + math.pi) % (2 * math.pi) - math.pi) < 0.13:
            continue  # puerta
        x, y = px + math.cos(a) * radio, py + math.sin(a) * radio / 1.15
        poner(emp, vt(x, y, -20), math.degrees(a) + 90, (1.3, 1.3, 1.3), carpeta="Exterior/Pueblo/Empalizada")
    gx, gy = px + math.cos(a_puerta) * radio, py + math.sin(a_puerta) * radio / 1.15
    for lado in (-1, 1):  # faroles de la puerta
        ox, oy = math.cos(a_puerta + math.pi / 2) * 450 * lado, math.sin(a_puerta + math.pi / 2) * 450 * lado
        poner(E("props", "SM_Antorcha_Pared"), vt(gx + ox, gy + oy, 180), math.degrees(a_puerta) - 90, (1.3, 1.3, 1.3), carpeta="Exterior/Pueblo")
        luz_puntual(vt(gx + ox + math.cos(a_puerta) * 80, gy + oy + math.sin(a_puerta) * 80, 260), unreal.LinearColor(1.0, 0.55, 0.25),
                    2600.0, 1100.0, lado < 0, "Exterior/Pueblo/Luces")
    sonido_3d("amb_antorcha", vt(gx, gy, 200), 800.0, 0.5)
    # Plaza: pozo y bancos; luz de la iglesia
    poner(E("cementerio", "SM_Pozo"), vt(px + math.cos(a_puerta) * 1300, py + math.sin(a_puerta) * 1300), 0, carpeta="Exterior/Pueblo")
    for lado in (-1, 1):
        bx = px + math.cos(a_puerta) * 1600 + math.cos(a_puerta + math.pi / 2) * 700 * lado
        by = py + math.sin(a_puerta) * 1600 + math.sin(a_puerta + math.pi / 2) * 700 * lado
        poner(E("cementerio", "SM_Banco"), vt(bx, by), math.degrees(a_puerta), carpeta="Exterior/Pueblo")
    luz_puntual(vt(px + math.cos(a_puerta) * 900, py + math.sin(a_puerta) * 900, 420), unreal.LinearColor(1.0, 0.62, 0.32), 5000.0, 2200.0,
                True, "Exterior/Pueblo/Luces")
    # Sendero desde la loma: rocas a los lados (lo marcan sin carteles) y navegación
    sendero = camino_pueblo()
    for (ax, ay), (bx, by) in zip(sendero, sendero[1:]):
        tramos = int(math.hypot(bx - ax, by - ay) // 1400)
        for t in range(1, tramos):
            f = t / tramos
            x, y = ax + (bx - ax) * f, ay + (by - ay) * f
            if en_pueblo(x, y, -300):
                continue
            nx, ny = -(by - ay), bx - ax
            d = math.hypot(nx, ny)
            lado = 1 if t % 2 else -1
            poner(M("Torre", "SM_Roca_Grande"), vt(x + nx / d * 420 * lado, y + ny / d * 420 * lado, -40), rnd.uniform(0, 360),
                  (0.35, 0.35, 0.3), carpeta="Exterior/Pueblo/Sendero")
        nav((ax + bx) / 2, (ay + by) / 2, abs(bx - ax) / 2 + 1500, abs(by - ay) / 2 + 1500)
    nav(px, py, TER.RADIO_PUEBLO + 800, TER.RADIO_PUEBLO + 800)
    trigger(vt(gx, gy, 200), (600, 600, 400), "zona_pueblo", 0.0, "")
    unreal.log(f"[vaelith] pueblo: {len(puestas)} casas, empalizada {n} tramos de {largo:.0f} cm, a {math.hypot(px - lx, py - ly) / 100:.0f} m de la loma")


def construir_torre():
    """Torre derruida en el fondo de la hondonada: anillo de ladrillo quemado, entrada mirando a la loma."""
    T = lambda n: M("Torre", n)
    tx, ty = TORRE
    base = H(tx, ty)
    ladrillo = MAT.get("M_Ladrillo_Quemado") or MAT["M_Piedra"]
    radio, n = 850.0, 18
    ancho = 2 * math.pi * radio / n + 30
    for i in range(n):
        ang = i * 360.0 / n
        if abs(((ang - ENTRADA_TORRE) + 180) % 360 - 180) < 18:
            continue
        rad = math.radians(ang)
        alto = 1100.0 if (i % 5) else rnd.uniform(500, 800)
        alto += rnd.uniform(-150, 250)
        x, y = tx + math.cos(rad) * radio, ty + math.sin(rad) * radio
        a = caja(v(x, y, base + alto / 2 - 100), (130, ancho, alto + 200), ladrillo, "Torre")
        a.set_actor_rotation(unreal.Rotator(0, 0, ang), False)
        if rnd.random() < 0.35:
            poner(T("SM_Ruina_Bloque"), vt(x + rnd.uniform(-200, 200), y + rnd.uniform(-200, 200)), rnd.uniform(0, 360), carpeta="Torre")
    for lado in (-1, 1):
        rad = math.radians(ENTRADA_TORRE + lado * 14)
        caja(v(tx + math.cos(rad) * radio, ty + math.sin(rad) * radio, base + 500), (180, 180, 1200), ladrillo, "Torre")
    caja(v(tx, ty, base - 20), (1800, 1800, 40), MAT["M_Piso"], "Torre")
    # Paso en ruinas delante de la entrada (el mismo arco que el del cementerio, más hundido)
    ra = math.radians(ENTRADA_TORRE)
    ex, ey = tx + math.cos(ra) * (radio + 900), ty + math.sin(ra) * (radio + 900)
    poner(E("ruinas", "SM_Arco_Ruina"), v(ex, ey, H(ex, ey) - 60), ENTRADA_TORRE - 90, carpeta="Torre")
    # Dos verdugos de piedra custodian el paso (la malla mira a su -Y local)
    for lado in (-1, 1):
        vx = tx + math.cos(ra) * 1450 + math.cos(ra + lado * math.pi / 2) * 330
        vy = ty + math.sin(ra) * 1450 + math.sin(ra + lado * math.pi / 2) * 330
        poner(E("ruinas", "SM_Verdugo"), vt(vx, vy, -5), ENTRADA_TORRE + 90, (1.1, 1.1, 1.1), carpeta="Torre")
    for i in range(5):
        poner(T("SM_Torre_Almena"), vt(tx + rnd.uniform(-500, 500), ty + rnd.uniform(-500, 500)), rnd.uniform(0, 360), carpeta="Torre")
    for i in range(10):
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(1100, 2600)
        poner(T("SM_Ruina_Bloque"), vt(tx + math.cos(a) * r, ty + math.sin(a) * r), rnd.uniform(0, 360), carpeta="Torre")
    trigger(v(ex, ey, H(ex, ey) + 250), (500, 400, 300), "zona_torre", 0.35, "mus_catacumba")
    interactuable(unreal.TipoInteractuable.RECUERDO, v(tx, ty, base), ENTRADA_TORRE + 180, M("Osario", "SM_Altar_Pharasma"),
                  "recuerdo_4", "", 4, etiqueta="Tocar la rueda")
    # La rueda de Pharasma, de pie sobre el altar: el texto del recuerdo 4 es una pista que se puede tocar
    cil = unreal.load_asset("/Engine/BasicShapes/Cylinder")
    rueda = poner(cil, v(tx, ty, base + 250), 0, (1.5, 1.5, 0.12), MAT["M_Oro"] or MAT["M_Metal"], "Torre")
    rueda.set_actor_rotation(unreal.Rotator(0, 90, ENTRADA_TORRE), False)
    for k in range(8):  # rayos
        a = k * 45.0
        r_ = poner(cil, v(tx, ty, base + 250), 0, (0.08, 0.08, 1.4), MAT["M_Metal"], "Torre")
        r_.set_actor_rotation(unreal.Rotator(a, 0, ENTRADA_TORRE), False)
    sx, sy = tx - math.cos(ra) * 600, ty - math.sin(ra) * 600
    no_muerto(unreal.TipoNoMuerto.SOMBRA, v(sx, sy, base + 100), ENTRADA_TORRE, "sombra", None, 3000.0)
    luz_puntual(v(tx, ty, base + 900), unreal.LinearColor(0.55, 0.6, 1.0), 6000.0, 1800.0, True, "Torre")
    for lado in (-1, 1):
        bx, by = ex + math.cos(ra + lado * math.pi / 2) * 420, ey + math.sin(ra + lado * math.pi / 2) * 420
        poner(M("Osario", "SM_Candelabro_Suelo"), vt(bx, by), 0, (1.4, 1.4, 1.4), carpeta="Torre")
        luz_puntual(vt(bx, by, 220), unreal.LinearColor(1.0, 0.5, 0.2), 9000.0, 1600.0, lado < 0, "Torre")
    d = actores.spawn_actor_from_class(unreal.DestelloTorre, v(tx, ty, base + 1500))
    d.set_editor_property("y_minima_llamado", 44000.0)
    d.set_editor_property("radio_llamado", 26000.0)
    d.set_folder_path("Torre")
    sonido_3d("amb_llamado", v(tx, ty, base + 800), 26000.0, 0.9)
    nav(tx, ty, 2600, 2600, base - 500, base + 1500)
    return ENTRADA_TORRE


RADIO_CIELO = 600000.0


def iluminacion_global():
    luna = actores.spawn_actor_from_class(unreal.DirectionalLight, v(0, 0, 3000), unreal.Rotator(0, -38, 125))
    lc = luna.get_component_by_class(unreal.DirectionalLightComponent)
    lc.set_intensity(1.5)
    # Sombras dinámicas de la luna solo cerca (sin luz horneada, 3000 árboles instanciados las encarecen)
    luna.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    lc.set_editor_property("dynamic_shadow_distance_movable_light", 6000.0)
    lc.set_editor_property("dynamic_shadow_cascades", 2)
    lc.set_light_color(unreal.LinearColor(0.55, 0.65, 1.0))
    lc.set_editor_property("atmosphere_sun_light", False)  # noche: el cielo no lo ilumina la luna
    # Sin SkyAtmosphere: de noche el horizonte lo da la niebla (si no, el cielo queda celeste).
    cielo = actores.spawn_actor_from_class(unreal.SkyLight, v(0, 0, 2000))
    sc = cielo.get_component_by_class(unreal.SkyLightComponent)
    sc.set_mobility(unreal.ComponentMobility.MOVABLE)
    sc.set_editor_property("real_time_capture", False)
    sc.set_intensity(0.7)
    niebla = actores.spawn_actor_from_class(unreal.ExponentialHeightFog, v(6400, 20000, 0))
    fc = niebla.get_component_by_class(unreal.ExponentialHeightFogComponent)
    fc.set_fog_density(0.035)
    fc.set_editor_property("fog_height_falloff", 0.3)
    fc.set_editor_property("fog_max_opacity", 0.96)
    fc.set_editor_property("fog_inscattering_luminance", unreal.LinearColor(0.025, 0.035, 0.07, 1.0))
    pp = actores.spawn_actor_from_class(unreal.PostProcessVolume, v(0, 0, 0))
    pp.set_editor_property("unbound", True)
    ajustes = pp.get_editor_property("settings")
    ajustes.set_editor_property("override_auto_exposure_min_brightness", True)
    ajustes.set_editor_property("auto_exposure_min_brightness", -0.9)  # noche: no aclarar como de día
    ajustes.set_editor_property("override_auto_exposure_max_brightness", True)
    ajustes.set_editor_property("auto_exposure_max_brightness", 1.0)
    ajustes.set_editor_property("override_bloom_intensity", True)
    ajustes.set_editor_property("bloom_intensity", 0.9)
    # Motion blur casi nulo: en primera persona y en combate importa leer el espacio.
    ajustes.set_editor_property("override_motion_blur_amount", True)
    ajustes.set_editor_property("motion_blur_amount", 0.1)
    ajustes.set_editor_property("override_motion_blur_max", True)
    ajustes.set_editor_property("motion_blur_max", 2.0)
    pp.set_editor_property("settings", ajustes)
    # Cúpula de cielo nocturno (estrellas + luna en la dirección de la luz de luna), fuera del alcance de la niebla
    cupula = None
    m_cielo = unreal.load_asset("/Game/Vaelith/Cielo/M_Cielo")
    esfera = unreal.load_asset("/Engine/EngineSky/SM_SkySphere")
    if m_cielo and esfera:
        ruta_mi = "/Game/Vaelith/Cielo/MI_Cielo"
        if unreal.EditorAssetLibrary.does_asset_exist(ruta_mi):
            unreal.EditorAssetLibrary.delete_asset(ruta_mi)
        mi = unreal.AssetToolsHelpers.get_asset_tools().create_asset("MI_Cielo", "/Game/Vaelith/Cielo", unreal.MaterialInstanceConstant,
                                                                     unreal.MaterialInstanceConstantFactoryNew())
        mi.set_editor_property("parent", m_cielo)
        f = luna.get_actor_forward_vector()
        unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi, "DirLuna", unreal.LinearColor(-f.x, -f.y, -f.z, 0))
        unreal.EditorAssetLibrary.save_asset(ruta_mi)
        b = esfera.get_bounding_box()
        escala = RADIO_CIELO / max(1.0, (b.max.x - b.min.x) / 2)
        cupula = poner(esfera, v(6400, 30000, 0), 0, (escala, escala, escala), mi, "Luces", False)
        cc = cupula.get_component_by_class(unreal.StaticMeshComponent)
        cc.set_editor_property("cast_shadow", False)
        cc.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        cc.set_editor_property("bounds_scale", 2.0)
        fc.set_editor_property("fog_cutoff_distance", RADIO_CIELO * 0.7)  # la cúpula no recibe niebla: el material funde el horizonte
        unreal.log(f"[vaelith] cielo: cúpula radio {RADIO_CIELO:.0f} cm, luna hacia ({-f.x:.2f}, {-f.y:.2f}, {-f.z:.2f})")
    for a in (luna, cielo, niebla, pp) + ((cupula,) if cupula else ()):
        a.set_folder_path("Luces")
    nav(5200, 3000, 6000, 3600, -200, 800)  # catacumbas


def camara_menu():
    """El menú mira la estatua de Pharasma del cementerio, con el farol encendido entre las tumbas."""
    sx, sy = centro(*SALIDA)
    ex, ey = sx + 650, 10200
    cx, cy = ex - 1500, ey - 1700
    pos = v(cx, cy, H(cx, cy) + 190)
    rot = unreal.MathLibrary.find_look_at_rotation(pos, v(ex + 200, ey + 900, H(ex, ey) + 230))
    cam = actores.spawn_actor_from_class(unreal.CameraActor, pos, rot)
    cam.tags = ["CamaraMenu"]
    cam.set_folder_path("Guion")


def main():
    unreal.log(f"[vaelith] plano: {verificar_plano()} celdas alcanzables")
    if eal.does_asset_exist(RUTA_MAPA):
        raise RuntimeError("el mapa ya existe; borrarlo a mano antes de regenerar")
    if not niveles.new_level(RUTA_MAPA):
        raise RuntimeError("new_level falló")
    actual = unreal.EditorLevelLibrary.get_editor_world().get_path_name()
    if not actual.startswith(RUTA_MAPA):
        raise RuntimeError(f"nivel activo inesperado: {actual}")
    iluminacion_global()
    construir_catacumbas()
    poblar_catacumbas()
    construir_terreno()
    construir_cementerio()
    construir_bosque()
    construir_pueblo()
    yaw = construir_torre()
    crear_instancias()
    camara_menu()
    niveles.save_current_level()
    unreal.log(f"[vaelith] construir_nivel OK (entrada de la torre a {yaw:.0f}°)")


main()
