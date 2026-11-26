"""Fase 0: arma niveles de prueba del bosque para medir rendimiento.

Importa los árboles de assets_fuente/arboles_prueba y crea:
  /Game/Pruebas/Lvl_Bosque_050  (50 árboles)
  /Game/Pruebas/Lvl_Bosque_300  (300 árboles)
Cada nivel: suelo de 200 x 200 m, luna (direccional), luz de cielo, niebla
exponencial y un PlayerStart mirando al bosque. Los árboles son actores sueltos
(peor caso: sin instanciado), para que la medición sea pesimista.

Uso (con el editor cerrado; abre el editor, construye y lo cierra):
  tools/ue/correr.sh tools/ue/prueba_bosque.py
"""
import math
import os
import random

import unreal

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FUENTE = os.path.join(RAIZ, "assets_fuente", "arboles_prueba")
DEST = "/Game/Pruebas/Arboles"
ARBOLES = ["SM_Pino_A", "SM_Pino_B", "SM_Roble_Muerto"]

actores = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
niveles = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)


def importar():
    tareas = []
    for n in ARBOLES:
        t = unreal.AssetImportTask()
        t.filename = os.path.join(FUENTE, n + ".fbx")
        t.destination_path = DEST
        t.automated = True
        t.replace_existing = True
        t.save = True
        tareas.append(t)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tareas)
    mallas = [unreal.load_asset(f"{DEST}/{n}") for n in ARBOLES]
    faltan = [n for n, m in zip(ARBOLES, mallas) if m is None]
    if faltan:
        raise RuntimeError(f"no se importaron: {faltan}")
    return mallas


def spawn(clase, pos, rot=(0, 0, 0)):
    return actores.spawn_actor_from_class(clase, unreal.Vector(*pos), unreal.Rotator(*rot))


def armar_nivel(ruta, cantidad, mallas):
    # Si el nivel ya existe hay que borrarlo a mano con el editor cerrado: new_level
    # falla sin avisar y los actores caerían en el mapa abierto.
    if unreal.EditorAssetLibrary.does_asset_exist(ruta):
        raise RuntimeError(f"{ruta} ya existe; borrarlo antes de regenerar")
    if not niveles.new_level(ruta):
        raise RuntimeError(f"new_level falló para {ruta}")
    actual = unreal.EditorLevelLibrary.get_editor_world().get_path_name()
    if not actual.startswith(ruta):
        raise RuntimeError(f"nivel activo inesperado: {actual}")

    suelo = actores.spawn_actor_from_object(unreal.load_asset("/Engine/BasicShapes/Plane"), unreal.Vector(0, 0, 0))
    suelo.set_actor_scale3d(unreal.Vector(200, 200, 1))  # plano de 1 m -> 200 m

    luna = spawn(unreal.DirectionalLight, (0, 0, 1000), (-35, 40, 0))
    lc = luna.get_component_by_class(unreal.DirectionalLightComponent)
    lc.set_intensity(0.6)
    lc.set_light_color(unreal.LinearColor(0.55, 0.65, 1.0, 1.0))
    lc.set_editor_property("atmosphere_sun_light", True)

    spawn(unreal.SkyAtmosphere, (0, 0, 0))
    cielo = spawn(unreal.SkyLight, (0, 0, 500))
    sc = cielo.get_component_by_class(unreal.SkyLightComponent)
    sc.set_editor_property("real_time_capture", False)
    sc.set_intensity(0.4)

    niebla = spawn(unreal.ExponentialHeightFog, (0, 0, 0))
    fc = niebla.get_component_by_class(unreal.ExponentialHeightFogComponent)
    fc.set_fog_density(0.05)
    fc.set_editor_property("fog_inscattering_luminance", unreal.LinearColor(0.08, 0.10, 0.16, 1.0))

    # El jugador arranca en el borde y mira hacia el centro del bosque.
    spawn(unreal.PlayerStart, (-9000, 0, 120), (0, 0, 0))

    rnd = random.Random(1793 + cantidad)
    colocados = 0
    while colocados < cantidad:
        x, y = rnd.uniform(-8000, 9000), rnd.uniform(-9000, 9000)
        if math.hypot(x + 9000, y) < 600:  # claro alrededor del jugador
            continue
        a = actores.spawn_actor_from_object(rnd.choice(mallas), unreal.Vector(x, y, 0),
                                            unreal.Rotator(0, 0, rnd.uniform(0, 360)))
        s = rnd.uniform(0.8, 1.3)
        a.set_actor_scale3d(unreal.Vector(s, s, s))
        a.set_folder_path("Arboles")
        colocados += 1

    niveles.save_current_level()
    unreal.log(f"[vaelith] nivel {ruta}: {colocados} árboles")


def main():
    mallas = importar()
    for ruta, n in (("/Game/Pruebas/Lvl_Bosque_050", 50), ("/Game/Pruebas/Lvl_Bosque_300", 300)):
        armar_nivel(ruta, n, mallas)
    unreal.log("[vaelith] prueba_bosque OK")


main()
