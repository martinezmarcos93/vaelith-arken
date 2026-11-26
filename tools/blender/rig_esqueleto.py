"""Esqueleto enemigo: SK_Skeleton (skeleton.blend, pesado al maniquí de UE4) -> malla sobre el maniquí de UE5.

1. Deja solo SK_Skeleton y su armadura UE4; aplica el espejo, saca subdivisión y decima.
2. Importa el maniquí UE5 (assets_fuente/_ref/SKM_Manny_Simple.fbx, exportado por tools/ue/exportar_maniqui.py).
3. Posa la armadura UE4 para que cada hueso de brazos, piernas, cuello y clavícula coincida en
   posición y dirección con el UE5; hornea esa pose en la malla.
4. Renombra los grupos UE4 -> UE5 (spine_02 -> spine_03, spine_03 -> spine_05), la pega a la armadura UE5
   y exporta FBX + texturas a assets_fuente/externos/personajes/.
Así el esqueleto usa directo las animaciones del maniquí (ABP_Unarmed), sin retarget en Unreal.

Uso: blender -b --factory-startup --disable-autoexec -P tools/blender/rig_esqueleto.py
"""
import glob
import os
import sys
import zipfile

import bpy
import mathutils
import numpy as np

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FUENTE = os.path.expanduser("~/Descargas/Assets UE")
MANNY = os.path.join(RAIZ, "assets_fuente", "_ref", "SKM_Manny_Simple.fbx")
SALIDA = os.path.join(RAIZ, "assets_fuente", "externos", "personajes")
CACHE = os.path.expanduser("~/.cache/vaelith-src/skeleton")
TRIS = 22000
RENOMBRAR = {"spine_02": "spine_03", "spine_03": "spine_05"}
# (hueso, hueso hacia el que apunta) en orden padre -> hijo
CADENAS = []
for s in ("l", "r"):
    CADENAS += [(f"clavicle_{s}", f"upperarm_{s}"), (f"upperarm_{s}", f"lowerarm_{s}"), (f"lowerarm_{s}", f"hand_{s}"),
                (f"hand_{s}", f"middle_01_{s}"), (f"thigh_{s}", f"calf_{s}"), (f"calf_{s}", f"foot_{s}"), (f"foot_{s}", f"ball_{s}")]
CADENAS = [("neck_01", "head")] + CADENAS


def tris(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


def activo(ob, *otros):
    for o in bpy.context.scene.objects:
        o.select_set(o is ob or o in otros)
    bpy.context.view_layer.objects.active = ob


def main():
    os.makedirs(SALIDA, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=os.path.join(FUENTE, "skeleton.blend"), load_ui=False, use_scripts=False)
    malla = bpy.data.objects["SK_Skeleton"]
    arm4 = malla.parent
    bpy.data.batch_remove([o for o in bpy.data.objects if o not in (malla, arm4)])
    bpy.context.view_layer.update()
    # Modificadores: espejo aplicado, sin subdivisión ni nodos
    activo(malla)
    for m in list(malla.modifiers):
        if m.type in ("SUBSURF", "NODES"):
            malla.modifiers.remove(m)
    for m in list(malla.modifiers):
        if m.type == "MIRROR":
            bpy.ops.object.modifier_apply(modifier=m.name)
    t0 = tris(malla)
    dec = malla.modifiers.new("dec", "DECIMATE")
    dec.ratio = min(1.0, TRIS / t0)
    dec.use_collapse_triangulate = True
    bpy.ops.object.modifier_move_to_index(modifier="dec", index=0)
    bpy.ops.object.modifier_apply(modifier="dec")
    print("tris", t0, "->", tris(malla))

    # Maniquí UE5
    antes = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=MANNY)
    nuevos = [o for o in bpy.data.objects if o not in antes]
    arm5 = next(o for o in nuevos if o.type == "ARMATURE")
    bpy.context.view_layer.update()
    w5 = arm5.matrix_world
    pos5 = {b.name: w5 @ b.head_local for b in arm5.data.bones}

    # Escala global para igualar la altura de la cabeza
    w4 = arm4.matrix_world
    h4 = (w4 @ arm4.data.bones["head"].head_local).z
    s = pos5["head"].z / h4
    arm4.scale = arm4.scale * s
    bpy.context.view_layer.update()
    print("escala UE4->UE5", round(s, 4))

    # Pose de la armadura UE4 sobre la UE5
    activo(arm4)
    bpy.ops.object.mode_set(mode="POSE")
    inv = arm4.matrix_world.inverted()
    for hueso, hijo in CADENAS:
        if hueso not in arm4.pose.bones or hueso not in pos5 or hijo not in pos5:
            print("salteo", hueso)
            continue
        bpy.context.view_layer.update()
        pb = arm4.pose.bones[hueso]
        cab = pb.head.copy()
        dir_act = arm4.pose.bones[hijo].head - cab
        cab_obj = inv @ pos5[hueso]
        dir_obj = (inv @ pos5[hijo]) - cab_obj
        r = dir_act.rotation_difference(dir_obj).to_matrix().to_4x4()
        pb.matrix = mathutils.Matrix.Translation(cab_obj) @ r @ mathutils.Matrix.Translation(-cab) @ pb.matrix
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()

    # Hornear la pose en la malla
    activo(malla)
    mod = next(m for m in malla.modifiers if m.type == "ARMATURE")
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for g in malla.vertex_groups:
        if g.name in RENOMBRAR:
            g.name = RENOMBRAR[g.name] + "_tmp"
    for g in malla.vertex_groups:
        if g.name.endswith("_tmp"):
            g.name = g.name[:-4]
    faltan = [g.name for g in malla.vertex_groups if g.name not in arm5.data.bones]
    print("grupos sin hueso UE5:", faltan)
    bpy.data.batch_remove([arm4] + [o for o in nuevos if o.type == "MESH"])
    bpy.context.view_layer.update()

    # Colgar de la armadura UE5. Se lleva la armadura a escala 1 (metros) para exportar limpio.
    bpy.ops.object.select_all(action="DESELECT")
    activo(arm5)
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for o in [o for o in bpy.data.objects if o.type == "EMPTY"]:
        bpy.data.objects.remove(o)
    malla.parent = arm5
    malla.matrix_parent_inverse = arm5.matrix_world.inverted()
    m = malla.modifiers.new("Armature", "ARMATURE")
    m.object = arm5
    arm5.name = "Armature"
    malla.name = "SKM_Esqueleto"
    malla.data.materials.clear()
    malla.data.materials.append(bpy.data.materials.new("MI_Esqueleto"))
    for p in malla.data.polygons:
        p.material_index = 0
    for o in (arm5, malla):
        if o.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(o)
        for c in list(o.users_collection):
            if c != bpy.context.scene.collection:
                c.objects.unlink(o)
        o.hide_viewport = False
        o.hide_set(False)
    bpy.context.view_layer.update()
    activo(arm5, malla)
    print("seleccionados", [o.name for o in bpy.context.selected_objects])
    bpy.ops.export_scene.fbx(filepath=os.path.join(SALIDA, "SKM_Esqueleto.fbx"), use_selection=True,
                             object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, apply_unit_scale=True,
                             axis_forward="-Y", axis_up="Z", mesh_smooth_type="FACE", use_armature_deform_only=False,
                             bake_anim=False, primary_bone_axis="Y", secondary_bone_axis="X")
    texturas()
    print("OK SKM_Esqueleto", tris(malla))


def texturas():
    """Base color, normal (OpenGL -> DirectX) y ORM desde el zip del autor."""
    if not os.path.exists(os.path.join(CACHE, ".ok")):
        os.makedirs(CACHE, exist_ok=True)
        with zipfile.ZipFile(os.path.join(FUENTE, "skeleton.zip")) as z:
            z.extractall(CACHE)
        open(os.path.join(CACHE, ".ok"), "w").close()
    t = os.path.join(CACHE, "textures")
    color = glob.glob(os.path.join(t, "Skeleton_BaseColor*"))[0]
    normal = glob.glob(os.path.join(t, "Skeleton_Normal*"))[0]
    mr = max(glob.glob(os.path.join(t, "Skeleton_Metallic*")), key=os.path.getsize)
    tex = os.path.join(SALIDA, "tex")
    os.makedirs(tex, exist_ok=True)

    def leer(ruta, lado=1024):
        img = bpy.data.images.load(ruta)
        if tuple(img.size) != (lado, lado):
            img.scale(lado, lado)
        a = np.empty(lado * lado * 4, dtype=np.float32)
        img.pixels.foreach_get(a)
        return a.reshape(lado, lado, 4)

    def escribir(arr, nombre, srgb):
        img = bpy.data.images.new(nombre, arr.shape[1], arr.shape[0], alpha=False)
        img.colorspace_settings.name = "sRGB" if srgb else "Non-Color"
        img.pixels.foreach_set(arr.ravel())
        img.filepath_raw = os.path.join(tex, nombre)
        img.file_format = "PNG"
        img.save()
    escribir(leer(color), "MI_Esqueleto_color.png", True)
    n = leer(normal)
    n[:, :, 1] = 1.0 - n[:, :, 1]
    escribir(n, "MI_Esqueleto_normal.png", False)
    m = leer(mr)
    orm = np.ones_like(m)
    orm[:, :, 1] = m[:, :, 1]
    orm[:, :, 2] = m[:, :, 2]
    escribir(orm, "MI_Esqueleto_orm.png", False)


main()
