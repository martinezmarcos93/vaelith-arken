"""Genera el terreno del exterior en baldosas FBX a partir de tools/terreno.py.

assets_fuente/externos/terreno/SM_Terreno_<i>_<j>.fbx  (baldosas de 60 m, grilla de 2,5 m, pivote en el centro)
assets_fuente/externos/terreno/SM_Valle.fbx             (valle lejano del pueblo, grilla de 40 m)
Los slots de material llevan el nombre de materiales del proyecto (M_Suelo_Bosque, M_Suelo_Cementerio).
Convención de ejes: el FBX se exporta con forward -Y, así que Y de Blender = -Y de Unreal.
Uso: blender -b --factory-startup -P tools/blender/terreno.py
"""
import json
import os
import sys

import bpy

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import terreno as T  # noqa: E402

SALIDA = os.path.join(RAIZ, "assets_fuente", "externos", "terreno")
TAM, PASO = 6000.0, 250.0


def malla(nombre, cx, cy, ancho, alto, paso, fn, material):
    nx, ny = int(round(ancho / paso)), int(round(alto / paso))
    verts, caras = [], []
    for j in range(ny + 1):
        for i in range(nx + 1):
            x = cx - ancho / 2 + i * paso
            y = cy - alto / 2 + j * paso
            verts.append(((x - cx) / 100.0, -(y - cy) / 100.0, fn(x, y) / 100.0))
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i
            # orden con normal hacia arriba tras invertir Y
            caras.append((a, a + nx + 1, a + nx + 2, a + 1))
    me = bpy.data.meshes.new(nombre)
    me.from_pydata(verts, [], caras)
    me.update()
    uv = me.uv_layers.new(name="UV")
    for p in me.polygons:
        for li in p.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (co.x / 4.0, co.y / 4.0)
    me.materials.append(bpy.data.materials.get(material) or bpy.data.materials.new(material))
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    # Normal hacia arriba: si quedó al revés, invertir
    if me.polygons[0].normal.z < 0:
        me.flip_normals()
    for o in bpy.context.scene.objects:
        o.select_set(o is ob)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.export_scene.fbx(filepath=os.path.join(SALIDA, nombre + ".fbx"), use_selection=True, apply_unit_scale=True,
                             axis_forward="-Y", axis_up="Z", mesh_smooth_type="FACE")
    bpy.data.objects.remove(ob)
    return len(caras) * 2


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    os.makedirs(SALIDA, exist_ok=True)
    for f in os.listdir(SALIDA):
        if f.endswith(".fbx"):
            os.remove(os.path.join(SALIDA, f))
    baldosas, tris = [], 0
    nx = int((T.X1 - T.X0) // TAM) + 1
    ny = int((T.Y1 - T.Y0) // TAM) + 1
    for i in range(nx):
        for j in range(ny):
            cx = T.X0 + TAM / 2 + i * TAM
            cy = T.Y0 + TAM / 2 + j * TAM
            nombre = f"SM_Terreno_{i:02d}_{j:02d}"
            tris += malla(nombre, cx, cy, TAM, TAM, PASO, T.altura, T.region(cx, cy))
            baldosas.append({"nombre": nombre, "x": cx, "y": cy})
    ancho, alto = T.VALLE_X1 - T.VALLE_X0, T.VALLE_Y1 - T.VALLE_Y0
    vx, vy = (T.VALLE_X0 + T.VALLE_X1) / 2, (T.VALLE_Y0 + T.VALLE_Y1) / 2
    tris += malla("SM_Valle", vx, vy, ancho, alto, 4000.0, T.altura_valle, "M_Suelo_Bosque")
    baldosas.append({"nombre": "SM_Valle", "x": vx, "y": vy})
    with open(os.path.join(SALIDA, "baldosas.json"), "w", encoding="utf-8") as f:
        json.dump(baldosas, f, indent=0)
    print(f"OK terreno: {len(baldosas)} piezas, {tris} triángulos")


main()
