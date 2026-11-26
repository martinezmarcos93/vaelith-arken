"""Diagnóstico de pasos: traza rayos horizontales a la altura de la rodilla y del pecho a lo largo de
recorridos clave (salida de la cripta, arco del cementerio, puente) y verticales para medir escalones.
No modifica nada. Uso: tools/ue/correr.sh tools/ue/diag_paso.py"""
import os
import sys

import unreal

sys.path.insert(0, os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), "tools"))
import terreno as TER  # noqa: E402

niveles = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
niveles.load_level("/Game/Vaelith/Mapas/Lvl_Vaelith")
mundo = unreal.EditorLevelLibrary.get_editor_world()


def rayo(a, b):
    h = unreal.SystemLibrary.line_trace_single(mundo, a, b, unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [],
                                               unreal.DrawDebugTrace.NONE, True)
    if not h:
        return None
    t = h.to_tuple()
    actor = t[9] if len(t) > 9 else None
    return t[4], (actor.get_actor_label() if hasattr(actor, "get_actor_label") else str(actor))


def suelo(x, y):
    r = rayo(unreal.Vector(x, y, 6000), unreal.Vector(x, y, -6000))
    return r[0].z if r else None


def recorrido(nombre, puntos, paso=50.0):
    alturas = []
    for (ax, ay), (bx, by) in zip(puntos, puntos[1:]):
        n = int(max(abs(bx - ax), abs(by - ay)) / paso)
        for i in range(n):
            x, y = ax + (bx - ax) * i / n, ay + (by - ay) * i / n
            alturas.append((x, y, suelo(x, y)))
    saltos = [(round(a[0]), round(a[1]), round(b[2] - a[2])) for a, b in zip(alturas, alturas[1:])
              if a[2] is not None and b[2] is not None and abs(b[2] - a[2]) > 40]
    bloqueos = []
    for (x, y, z), (x2, y2, z2) in zip(alturas, alturas[1:]):
        if z is None or z2 is None:
            continue
        for alto in (60, 140):
            r = rayo(unreal.Vector(x, y, z + alto), unreal.Vector(x2, y2, z2 + alto))
            if r:
                bloqueos.append((round(x), round(y), alto, r[1]))
    unreal.log(f"[vaelith] {nombre}: {len(alturas)} muestras, escalones >40 cm: {saltos[:8]}, bloqueos: {bloqueos[:8]}")


sx, sy = 6400.0, 6000.0
recorrido("salida", [(sx, 5700), (sx, 9000)])
recorrido("arco", [(TER.ARCO[0], TER.ARCO[1] - 1500), (TER.ARCO[0], TER.ARCO[1] + 1500)])
recorrido("puente", [(TER.PUENTE[0], TER.PUENTE[1] - 1200), (TER.PUENTE[0], TER.PUENTE[1] + 1200)])
