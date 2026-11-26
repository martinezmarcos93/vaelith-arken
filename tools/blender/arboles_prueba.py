"""Árboles low-poly para la prueba de rendimiento del bosque (Fase 0).

Tres variantes (pino, pino seco, roble muerto) de ~800-1600 triángulos, parecido
a lo que pesan los árboles CC0 de Quaternius. Sirven para medir; el arte final se
decide después.

Uso:
    ~/Aplicaciones/blender-5.3.0/blender -b --factory-startup \
        -P tools/blender/arboles_prueba.py -- <carpeta_salida>
"""
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

random.seed(4242)


def limpiar():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def cono(bm, radio, alto, z, lados, radio_sup=0.0):
    bmesh.ops.create_cone(bm, cap_ends=True, segments=lados, radius1=radio,
                          radius2=radio_sup, depth=alto,
                          matrix=Matrix.Translation((0, 0, z + alto / 2)))


def tronco(bm, radio, alto, lados=8):
    cono(bm, radio, alto, 0.0, lados, radio_sup=radio * 0.55)


def ruido(bm, fuerza):
    for v in bm.verts:
        if v.co.z > 0.3:
            v.co += Vector((random.uniform(-fuerza, fuerza),
                            random.uniform(-fuerza, fuerza),
                            random.uniform(-fuerza * 0.5, fuerza * 0.5)))


def pino(nombre, alto, pisos):
    bm = bmesh.new()
    tronco(bm, 0.28, alto * 0.45)
    for i in range(pisos):
        t = i / pisos
        r = 2.4 * (1 - t) + 0.5
        cono(bm, r, alto * 0.32, alto * (0.22 + 0.62 * t), 16)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
    ruido(bm, 0.12)
    return a_objeto(bm, nombre)


def rama(bm, base, direccion, largo, radio):
    d = direccion.normalized()
    rot = d.to_track_quat("Z", "Y").to_matrix().to_4x4()
    m = Matrix.Translation(base) @ rot @ Matrix.Translation((0, 0, largo / 2))
    bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=radio,
                          radius2=radio * 0.3, depth=largo, matrix=m)


def roble_muerto(nombre, alto):
    bm = bmesh.new()
    tronco(bm, 0.45, alto, lados=10)
    for i in range(14):
        z = alto * random.uniform(0.35, 0.95)
        ang = random.uniform(0, math.tau)
        d = Vector((math.cos(ang), math.sin(ang), random.uniform(0.3, 1.1)))
        largo = random.uniform(1.6, 3.4)
        base = Vector((0, 0, z))
        rama(bm, base, d, largo, 0.16)
        punta = base + d.normalized() * largo
        for _ in range(2):
            d2 = d + Vector((random.uniform(-.8, .8), random.uniform(-.8, .8), random.uniform(0, .6)))
            rama(bm, punta - d.normalized() * 0.3, d2, largo * 0.55, 0.07)
    return a_objeto(bm, nombre)


def a_objeto(bm, nombre):
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.shade_flat()
    me.uv_layers.new(name="UV0")
    return ob


def exportar(ob, carpeta):
    for o in bpy.context.scene.objects:
        o.select_set(o is ob)
    ruta = os.path.join(carpeta, f"{ob.name}.fbx")
    bpy.ops.export_scene.fbx(filepath=ruta, use_selection=True, apply_unit_scale=True,
                             global_scale=1.0, axis_forward="-Y", axis_up="Z",
                             mesh_smooth_type="FACE", add_leaf_bones=False)
    return ruta


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    carpeta = os.path.abspath(argv[0] if argv else "assets_fuente/arboles_prueba")
    os.makedirs(carpeta, exist_ok=True)
    limpiar()
    obs = [pino("SM_Pino_A", 11.0, 6), pino("SM_Pino_B", 8.0, 5), roble_muerto("SM_Roble_Muerto", 7.5)]
    with open(os.path.join(carpeta, "INFORME.txt"), "w", encoding="utf-8") as f:
        for ob in obs:
            tris = len(ob.data.polygons)
            ruta = exportar(ob, carpeta)
            linea = f"{ob.name}: {tris} triángulos, alto {ob.dimensions.z:.1f} m -> {ruta}"
            print(linea)
            f.write(linea + "\n")


main()
