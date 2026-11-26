"""Kit mínimo de catacumba (reemplaza el encargo 001 que Codex no entregó).

SM_Boveda_4m: bóveda de arista para una celda de 4 x 4 m. Arranca a 4 m en los bordes y
  sube a 5,2 m en el centro; caras hacia abajo. Celdas vecinas empalman sin costura.
SM_Pared_Nichos_4m: muro de 4 x 0,5 x 4 m con 2 filas x 3 nichos funerarios en la cara +Y,
  con huesos dentro. Pivote en el centro de la base.

Uso: ~/Aplicaciones/blender-5.3.0/blender -b --factory-startup -P tools/blender/kit_catacumba.py -- <salida>
"""
import math
import os
import random
import sys

import bmesh
import bpy

random.seed(4040)


def material(nombre):
    m = bpy.data.materials.get(nombre) or bpy.data.materials.new(nombre)
    return m


def objeto(nombre, bm, mats):
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.scene.objects:
        o.select_set(o is ob)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")
    return ob


def caja(bm, cx, cy, cz, sx, sy, sz, mat_idx=0):
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r["verts"]:
        v.co.x = cx + v.co.x * sx
        v.co.y = cy + v.co.y * sy
        v.co.z = cz + v.co.z * sz
    caras = {f for v in r["verts"] for f in v.link_faces}
    for f in caras:
        f.material_index = mat_idx


def boveda():
    bm = bmesh.new()
    n = 12
    verts = {}
    for i in range(n + 1):
        for j in range(n + 1):
            x, y = -2 + 4 * i / n, -2 + 4 * j / n
            z = 4.0 + 1.2 * math.cos(math.pi * x / 4) * math.cos(math.pi * y / 4)
            verts[i, j] = bm.verts.new((x, y, z))
    for i in range(n):
        for j in range(n):
            # Orden para que la normal mire hacia abajo (se ve desde el piso).
            bm.faces.new((verts[i, j], verts[i, j + 1], verts[i + 1, j + 1], verts[i + 1, j]))
    # Nervaduras diagonales (aristas de la bóveda)
    for s in (1, -1):
        for k in range(n):
            t0, t1 = -2 + 4 * k / n, -2 + 4 * (k + 1) / n
            tm = (t0 + t1) / 2
            z = 4.0 + 1.2 * math.cos(math.pi * tm / 4) * math.cos(math.pi * (s * tm) / 4) - 0.08
            caja(bm, tm, s * tm, z, 0.42, 0.18, 0.14)
    ob = objeto("SM_Boveda_4m", bm, [material("M_Piedra")])
    return ob


def pared_nichos():
    bm = bmesh.new()
    mats = [material("M_Piedra"), material("M_Hueso")]
    # Bloques del muro, dejando los huecos de los nichos en la mitad frontal.
    ancho_n, alto_n, prof = 1.0, 0.5, 0.35
    huecos = [(-1.25 + c * 1.25, 1.0 + f * 1.25) for c in range(3) for f in range(2)]
    # Parte trasera maciza
    caja(bm, 0, -0.25 + (0.5 - prof) / 2, 2.0, 4.0, 0.5 - prof, 4.0)
    # Frente: columnas y franjas entre nichos
    for x in (-1.875, -0.625, 0.625, 1.875):
        caja(bm, x, 0.25 - prof / 2, 2.0, 0.25, prof, 4.0)
    for z0, z1 in ((0.0, 0.75), (1.25, 2.0), (2.5, 4.0)):
        for cx, _ in huecos[::2]:
            caja(bm, cx, 0.25 - prof / 2, (z0 + z1) / 2, ancho_n, prof, z1 - z0)
    # Huesos dentro de algunos nichos
    for cx, cz in huecos:
        if random.random() < 0.7:
            for _ in range(random.randint(2, 4)):
                caja(bm, cx + random.uniform(-0.35, 0.35), 0.05 + random.uniform(-0.05, 0.05), cz - alto_n / 2 + 0.04,
                     random.uniform(0.35, 0.5), 0.05, 0.05, 1)
            if random.random() < 0.6:
                caja(bm, cx + random.uniform(-0.3, 0.3), 0.08, cz - alto_n / 2 + 0.1, 0.16, 0.18, 0.17, 1)
    return objeto("SM_Pared_Nichos_4m", bm, mats)


def exportar(ob, carpeta):
    for o in bpy.context.scene.objects:
        o.select_set(o is ob)
    bpy.ops.export_scene.fbx(filepath=os.path.join(carpeta, ob.name + ".fbx"), use_selection=True,
                             apply_unit_scale=True, axis_forward="-Y", axis_up="Z", mesh_smooth_type="FACE",
                             add_leaf_bones=False)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    carpeta = os.path.abspath(argv[0] if argv else "assets_fuente/kit_catacumba")
    os.makedirs(carpeta, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with open(os.path.join(carpeta, "INFORME.txt"), "w", encoding="utf-8") as f:
        for ob in (boveda(), pared_nichos()):
            exportar(ob, carpeta)
            tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)
            d = ob.dimensions
            f.write(f"{ob.name}\t{tris}\t{d.x:.2f}x{d.y:.2f}x{d.z:.2f} m\t{','.join(m.name for m in ob.data.materials)}\n")
            print(ob.name, tris)


main()
