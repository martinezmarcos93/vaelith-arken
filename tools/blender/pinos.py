"""Abetos procedurales para el bosque (reemplazan los conos de la prueba de rendimiento).

Cada árbol: tronco cónico con raíces + pisos de ramas. Cada rama es una fronda aserrada que
cae con peso (prisma fino, se ve de los dos lados sin material de dos caras). Las frondas de
arriba son cortas y paradas; las de abajo, largas y colgantes. Copa irregular y algunas ramas secas.
Slots: M_Corteza (tronco/ramas secas) y M_Aguja (follaje). Pivote en la base.

Salida: assets_fuente/externos/bosque/SM_Abeto_{A,B,C}.fbx (tris en INFORME de preparar).
Uso: blender -b --factory-startup -P tools/blender/pinos.py
"""
import math
import os
import random

import bmesh
import bpy
from mathutils import Matrix, Vector

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SALIDA = os.path.join(RAIZ, "assets_fuente", "externos", "bosque")


def tronco(bm, alto, radio, mat):
    pisos, lados = 8, 9
    anillos = []
    for k in range(pisos + 1):
        t = k / pisos
        r = radio * (1 - 0.85 * t) * (1.35 if k == 0 else 1.0)
        z = alto * t
        anillo = []
        for i in range(lados):
            a = 2 * math.pi * i / lados
            rr = r * random.uniform(0.92, 1.08)
            anillo.append(bm.verts.new((math.cos(a) * rr, math.sin(a) * rr, z)))
        anillos.append(anillo)
    for k in range(pisos):
        for i in range(lados):
            f = bm.faces.new((anillos[k][i], anillos[k][(i + 1) % lados], anillos[k + 1][(i + 1) % lados], anillos[k + 1][i]))
            f.material_index = mat
    # raíces
    for i in range(5):
        a = 2 * math.pi * i / 5 + random.uniform(-0.3, 0.3)
        d = Vector((math.cos(a), math.sin(a), -0.25))
        prisma(bm, Vector((0, 0, 0.35)), d, radio * 4.5, radio * 0.9, radio * 0.6, 0.0, mat, segs=3)


def prisma(bm, base, direccion, largo, ancho, grosor, caida, mat, segs=6, sierra=0.0):
    """Fronda: tira aserrada que se curva hacia abajo (caida en metros al final)."""
    d = direccion.normalized()
    lado = d.cross(Vector((0, 0, 1)))
    if lado.length < 1e-4:
        lado = Vector((1, 0, 0))
    lado.normalize()
    arriba = lado.cross(d).normalized()
    filas = []
    for k in range(segs + 1):
        t = k / segs
        centro = base + d * (largo * t) - Vector((0, 0, caida * t * t))
        w = ancho * (1 - t) ** 0.8 * (1 + (sierra if k % 2 else -sierra))
        g = grosor * (1 - 0.7 * t)
        filas.append([bm.verts.new(centro + lado * s * w + arriba * h * g) for s, h in ((-1, 0), (0, 1), (1, 0), (0, -1))])
    for k in range(segs):
        for i in range(4):
            f = bm.faces.new((filas[k][i], filas[k][(i + 1) % 4], filas[k + 1][(i + 1) % 4], filas[k + 1][i]))
            f.material_index = mat


def abeto(nombre, alto, pisos, densidad, semilla):
    random.seed(semilla)
    bm = bmesh.new()
    alto_tronco = alto * 0.97
    tronco(bm, alto_tronco, 0.025 * alto + 0.08, 0)
    base_copa = alto * random.uniform(0.3, 0.4)
    for p in range(pisos):
        t = p / max(1, pisos - 1)
        z = base_copa + (alto * 0.96 - base_copa) * t
        largo = (alto * 0.19) * (1 - t) ** 1.1 + 0.3
        n = max(4, int(densidad * (1 - 0.5 * t)))
        giro = random.uniform(0, 2 * math.pi)
        for i in range(n):
            if random.random() < 0.08 and t < 0.6:
                # rama seca, sin follaje
                a = giro + 2 * math.pi * i / n
                prisma(bm, Vector((0, 0, z)), Vector((math.cos(a), math.sin(a), 0.05)), largo * 0.6, 0.035, 0.03, 0.2, 0, segs=3)
                continue
            a = giro + 2 * math.pi * i / n + random.uniform(-0.25, 0.25)
            subida = 0.45 * t + random.uniform(-0.05, 0.1)
            d = Vector((math.cos(a), math.sin(a), subida))
            l = largo * random.uniform(0.8, 1.15)
            prisma(bm, Vector((0, 0, z + random.uniform(-0.15, 0.15))), d, l, l * 0.42, 0.06, l * 0.42 * (1 - t), 1,
                   segs=6, sierra=0.35)
            # sub-fronda colgante debajo, más oscura por la sombra propia
            if t < 0.75:
                prisma(bm, Vector((0, 0, z - 0.25)), d + Vector((0, 0, -0.25)), l * 0.75, l * 0.3, 0.05, l * 0.5, 1, segs=4, sierra=0.4)
    # punta
    prisma(bm, Vector((0, 0, alto * 0.95)), Vector((0, 0.001, 1)), alto * 0.06, 0.18, 0.18, 0.0, 1, segs=2)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(bpy.data.materials.new("M_Corteza"))
    me.materials.append(bpy.data.materials.new("M_Aguja"))
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    for o in bpy.context.scene.objects:
        o.select_set(o is ob)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.uv.smart_project(island_margin=0.01)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.export_scene.fbx(filepath=os.path.join(SALIDA, nombre + ".fbx"), use_selection=True, apply_unit_scale=True,
                             axis_forward="-Y", axis_up="Z", mesh_smooth_type="FACE")
    print("OK", nombre, len(me.polygons), "tris", round(ob.dimensions.z, 1), "m")
    bpy.data.objects.remove(ob)


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    os.makedirs(SALIDA, exist_ok=True)
    abeto("SM_Abeto_A", 17.0, 13, 9, 11)
    abeto("SM_Abeto_B", 12.5, 11, 8, 23)
    abeto("SM_Abeto_C", 8.0, 9, 7, 37)


main()
