"""Reja de hierro forjado y losa con runa para la catacumba (reemplazan el cubo azul).

SM_Reja_Hierro: 390 x 350 cm (celda de 4 m menos el marco). Barrotes redondos con puntas de lanza,
  tres travesaños planos, remaches y un marco. Pivote abajo al centro; el plano de la reja es XZ (mira a ±Y).
  Slot: M_Hierro.
SM_Losa_Runa: losa de piedra 90 x 90 x 12 cm con la espiral de Pharasma en relieve hundido.
  Slots: M_Piedra (losa) y M_Runa (la espiral, emisiva).
Salida: assets_fuente/externos/catacumba/*.fbx
Uso: blender -b --factory-startup -P tools/blender/reja.py
"""
import math
import os

import bmesh
import bpy
from mathutils import Matrix, Vector

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SALIDA = os.path.join(RAIZ, "assets_fuente", "externos", "catacumba")


def cilindro(bm, a, b, r, lados=8, mat=0):
    d = (b - a)
    largo = d.length
    eje = d.normalized()
    rot = eje.to_track_quat("Z", "Y").to_matrix().to_4x4()
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=lados, radius1=r, radius2=r, depth=largo,
                                matrix=Matrix.Translation((a + b) / 2) @ rot)
    for f in {f for v in res["verts"] for f in v.link_faces}:
        f.material_index = mat


def cono(bm, base, alto, r, lados=6, mat=0):
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=lados, radius1=r, radius2=0.0, depth=alto,
                                matrix=Matrix.Translation(base + Vector((0, 0, alto / 2))))
    for f in {f for v in res["verts"] for f in v.link_faces}:
        f.material_index = mat


def caja(bm, centro, tam, mat=0):
    res = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(centro) @ Matrix.Diagonal((*tam, 1.0)))
    for f in {f for v in res["verts"] for f in v.link_faces}:
        f.material_index = mat


def exportar(bm, nombre, materiales):
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    for m in materiales:
        me.materials.append(bpy.data.materials.new(m))
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    for o in bpy.context.scene.objects:
        o.select_set(o is ob)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.uv.smart_project(island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.export_scene.fbx(filepath=os.path.join(SALIDA, nombre + ".fbx"), use_selection=True, apply_unit_scale=True,
                             axis_forward="-Y", axis_up="Z", mesh_smooth_type="FACE")
    print("OK", nombre, len(me.polygons), "tris", [round(d, 2) for d in ob.dimensions])
    bpy.data.objects.remove(ob)


def reja():
    bm = bmesh.new()
    ancho, alto = 3.9, 3.5
    # marco
    for x in (-ancho / 2, ancho / 2):
        caja(bm, Vector((x, 0, alto / 2)), (0.09, 0.09, alto))
    caja(bm, Vector((0, 0, alto - 0.04)), (ancho, 0.08, 0.08))
    # travesaños planos con remaches
    for z in (0.35, 1.6, 2.85):
        caja(bm, Vector((0, 0, z)), (ancho - 0.06, 0.045, 0.07))
        x = -ancho / 2 + 0.2
        while x < ancho / 2 - 0.1:
            cilindro(bm, Vector((x, -0.035, z)), Vector((x, 0.035, z)), 0.018, 6)
            x += 0.4
    # barrotes con punta de lanza (algunos torcidos por el tiempo)
    n = 17
    for i in range(n):
        x = -ancho / 2 + 0.15 + i * (ancho - 0.3) / (n - 1)
        doblez = 0.04 if i in (5, 12) else 0.0
        cilindro(bm, Vector((x, 0, 0.02)), Vector((x + doblez, 0, alto - 0.1)), 0.022, 8)
        cono(bm, Vector((x + doblez, 0, alto - 0.12)), 0.22, 0.045, 4)
    exportar(bm, "SM_Reja_Hierro", ["M_Hierro"])


def losa_runa():
    bm = bmesh.new()
    caja(bm, Vector((0, 0, 0.06)), (0.9, 0.9, 0.12), 0)
    # espiral de Pharasma: tramos cortos que giran hacia afuera, apenas sobre la cara superior
    pasos = 70
    previo = None
    for k in range(pasos + 1):
        t = k / pasos
        ang = t * 2.6 * 2 * math.pi
        r = 0.03 + 0.36 * t
        p = Vector((math.cos(ang) * r, math.sin(ang) * r, 0.125))
        if previo is not None:
            cilindro(bm, previo, p, 0.012 + 0.008 * t, 5, mat=1)
        previo = p
    exportar(bm, "SM_Losa_Runa", ["M_Piedra", "M_Runa"])


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    os.makedirs(SALIDA, exist_ok=True)
    reja()
    losa_runa()


main()
