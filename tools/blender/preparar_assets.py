"""Prepara assets externos (Sketchfab/Megascans) para Unreal sin Nanite.

Lee tools/blender/externos.json y, por cada entrada:
  1. extrae el zip a ~/.cache/vaelith-src/<zip>/ (una sola vez),
  2. importa el modelo (fbx/glb/obj/blend), filtra objetos por prefijo si se pide,
  3. une, aplica transformaciones, rota, escala a la medida pedida, decima a N triángulos,
  4. pone el pivote (base, centro o guarda), renombra los slots de material,
  5. exporta FBX a assets_fuente/externos/<kit>/<nombre>.fbx y
  6. escribe texturas por slot en assets_fuente/externos/<kit>/tex/<slot>_{color,normal,orm}.png
     (normal en convención DirectX; ORM = R oclusión, G rugosidad, B metálico).

Uso: blender -b --factory-startup --disable-autoexec -P tools/blender/preparar_assets.py -- [nombre ...]
Sin nombres procesa todo. Escribe assets_fuente/externos/INFORME.tsv.
"""
import fnmatch
import glob
import json
import math
import os
import re
import sys
import zipfile

import bmesh
import bpy
import mathutils
import numpy as np

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFIESTO = os.path.join(RAIZ, "tools", "blender", "externos.json")
SALIDA = os.path.join(RAIZ, "assets_fuente", "externos")
CACHE = os.path.expanduser("~/.cache/vaelith-src")


def extraer(zip_nombre, fuente):
    destino = os.path.join(CACHE, os.path.splitext(zip_nombre)[0])
    marca = os.path.join(destino, ".ok")
    if not os.path.exists(marca):
        os.makedirs(destino, exist_ok=True)
        with zipfile.ZipFile(os.path.join(fuente, zip_nombre)) as z:
            z.extractall(destino)
        # zips anidados (Sketchfab mete source/<algo>.zip)
        for interno in glob.glob(os.path.join(destino, "**", "*.zip"), recursive=True):
            with zipfile.ZipFile(interno) as z:
                z.extractall(os.path.join(os.path.dirname(interno), "x_" + os.path.splitext(os.path.basename(interno))[0]))
        open(marca, "w").close()
    return destino


def limpiar():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def importar(ruta):
    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".blend":
        bpy.ops.wm.open_mainfile(filepath=ruta, load_ui=False, use_scripts=False)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=ruta)
    elif ext in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=ruta)
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=ruta)
    else:
        raise ValueError(f"formato no soportado: {ruta}")


def tris(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


def seleccionar(obs):
    bpy.context.view_layer.update()
    for o in list(bpy.context.scene.objects):
        if o is not None:
            o.select_set(o in obs)
    if obs:
        bpy.context.view_layer.objects.active = obs[0]


def mallas_filtradas(a):
    obs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if a.get("objetos"):
        pats = a["objetos"]
        obs = [o for o in obs if any(fnmatch.fnmatch(o.name, p) for p in pats)]
        if a.get("uno"):
            obs = obs[:1]
    if a.get("excluir"):
        obs = [o for o in obs if not any(fnmatch.fnmatch(o.name, p) for p in a["excluir"])]
    return obs


def unir(obs):
    # Sacar padres conservando la transformación (glTF de Unreal trae jerarquías)
    seleccionar(obs)
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    for o in obs:
        if o.data.users > 1:
            o.data = o.data.copy()
    seleccionar(obs)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if len(obs) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    otros = [o for o in bpy.context.scene.objects if o is not ob]
    bpy.data.batch_remove(otros)
    bpy.context.view_layer.update()
    return ob


def caja(ob):
    vs = np.empty(len(ob.data.vertices) * 3, dtype=np.float64)
    ob.data.vertices.foreach_get("co", vs)
    vs = vs.reshape(-1, 3)
    return vs.min(0), vs.max(0), vs


def transformar(ob, a):
    me = ob.data
    rx, ry, rz = (math.radians(a.get(k, 0)) for k in ("rot_x", "rot_y", "rot_z"))
    if rx or ry or rz:
        me.transform(mathutils.Euler((rx, ry, rz), "XYZ").to_matrix().to_4x4())
    mn, mx, _ = caja(ob)
    dims = mx - mn
    if "alto" in a:
        s = a["alto"] / dims[2]
    elif "largo" in a:
        s = a["largo"] / dims.max()
    else:
        s = a.get("escala", 1.0)
    me.transform(mathutils.Matrix.Scale(s, 4))
    mn, mx, vs = caja(ob)
    piv = a.get("pivote", "base")
    if piv == "base":
        p = ((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, mn[2])
    elif piv == "centro":
        p = tuple((mn + mx) / 2)
    elif piv == "guarda":
        # altura donde el arma es más ancha en X (la cruz de la guarda)
        cortes = np.linspace(mn[2], mx[2], 200)
        anchos = [np.ptp(vs[np.abs(vs[:, 2] - z) < (mx[2] - mn[2]) / 200][:, 0]) if np.any(np.abs(vs[:, 2] - z) < (mx[2] - mn[2]) / 200) else 0 for z in cortes]
        p = ((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, cortes[int(np.argmax(anchos))])
    else:
        p = (0, 0, 0)
    me.transform(mathutils.Matrix.Translation(-mathutils.Vector(p)))
    me.update()


def decimar(ob, objetivo):
    actual = tris(ob)
    if not objetivo or actual <= objetivo:
        return
    seleccionar([ob])
    # Soldar vértices duplicados primero: los glTF parten la malla por costuras
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=0.0005)
    bpy.ops.object.mode_set(mode="OBJECT")
    m = ob.modifiers.new("dec", "DECIMATE")
    m.ratio = max(0.002, objetivo / tris(ob))
    m.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=m.name)


# ---------------------------------------------------------------- texturas

def rio_arriba(sock, tipos=("TEX_IMAGE",), prof=0):
    """Primer nodo de imagen aguas arriba de un socket; devuelve (nodo, canal) con canal de un SeparateColor/RGB."""
    if not sock.is_linked or prof > 8:
        return None, None
    l = sock.links[0]
    n = l.from_node
    if n.type in tipos:
        return n, None
    if n.type in ("SEPARATE_COLOR", "SEPRGB", "SEPARATE_RGB"):
        img, _ = rio_arriba(n.inputs[0], tipos, prof + 1)
        return img, l.from_socket.name[:1].upper()
    for i in n.inputs:
        img, canal = rio_arriba(i, tipos, prof + 1)
        if img:
            return img, canal
    return None, None


def principled(mat):
    if not mat or not mat.use_nodes:
        return None
    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            return n
    return None


def cargar(ruta_o_img, buscar_en):
    if isinstance(ruta_o_img, str):
        return bpy.data.images.load(ruta_o_img, check_existing=True)
    img = ruta_o_img
    if img.has_data or img.packed_file:
        return img
    nombre = os.path.basename(img.filepath.replace("\\", "/"))
    for d in buscar_en:
        for c in glob.glob(os.path.join(d, "**", nombre), recursive=True):
            img.filepath = c
            img.reload()
            return img
    return img


def a_numpy(img, px):
    if not img or img.size[0] == 0:
        return None
    w, h = img.size
    lado = min(px, max(w, h))
    if (w, h) != (lado, lado):
        img = img.copy()
        img.scale(lado, lado)
    a = np.empty(lado * lado * 4, dtype=np.float32)
    img.pixels.foreach_get(a)
    return a.reshape(lado, lado, 4)


def guardar(arr, ruta, srgb):
    h, w = arr.shape[:2]
    img = bpy.data.images.new(os.path.basename(ruta), w, h, alpha=False, float_buffer=False)
    img.colorspace_settings.name = "sRGB" if srgb else "Non-Color"
    img.pixels.foreach_set(arr.astype(np.float32).ravel())
    img.filepath_raw = ruta
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)


def buscar_patron(dirs, patron):
    for d in dirs:
        r = sorted(glob.glob(os.path.join(d, "**", patron), recursive=True))
        if r:
            return r[0]
    return None


def texturas_slot(slot, mat, a, dirs, carpeta_tex):
    px = a.get("tex_px", 1024)
    explicitas = a.get("tex", {})
    color = normal = rough = metal = ao = None
    canal_r = canal_m = None
    if explicitas:
        def f(k):
            v = explicitas.get(k)
            return buscar_patron(dirs, v) if v else None
        color, normal, rough, metal, ao = (f(k) for k in ("color", "normal", "rough", "metal", "ao"))
        color, normal, rough, metal, ao = (cargar(x, dirs) if x else None for x in (color, normal, rough, metal, ao))
    else:
        bsdf = principled(mat)
        if bsdf:
            n, _ = rio_arriba(bsdf.inputs["Base Color"])
            color = cargar(n.image, dirs) if n and n.image else None
            n, _ = rio_arriba(bsdf.inputs["Normal"])
            normal = cargar(n.image, dirs) if n and n.image else None
            n, canal_r = rio_arriba(bsdf.inputs["Roughness"])
            rough = cargar(n.image, dirs) if n and n.image else None
            n, canal_m = rio_arriba(bsdf.inputs["Metallic"])
            metal = cargar(n.image, dirs) if n and n.image else None
    hechos = []
    c = a_numpy(color, px)
    if c is not None:
        guardar(c, os.path.join(carpeta_tex, f"{slot}_color.png"), True)
        hechos.append("color")
    nm = a_numpy(normal, px)
    if nm is not None:
        if a.get("normal_gl", True):
            nm[:, :, 1] = 1.0 - nm[:, :, 1]
        guardar(nm, os.path.join(carpeta_tex, f"{slot}_normal.png"), False)
        hechos.append("normal")
    lado = None
    for x in (c, nm):
        if x is not None:
            lado = x.shape[0]
            break
    lado = lado or 256
    orm = np.ones((lado, lado, 4), dtype=np.float32)
    orm[:, :, 1] = a.get("rugosidad", 0.8)
    orm[:, :, 2] = a.get("metalico", 0.0)
    canales = {"R": 0, "G": 1, "B": 2}

    def poner(img, destino, canal):
        arr = a_numpy(img, lado)
        if arr is None:
            return False
        if arr.shape[0] != lado:
            return False
        orm[:, :, destino] = arr[:, :, canales.get(canal or "R", 0)]
        return True
    ok_r = poner(rough, 1, canal_r)
    ok_m = poner(metal, 2, canal_m)
    ok_a = poner(ao, 0, "R") if ao else False
    if a.get("suavidad"):  # el mapa es "smoothness"
        orm[:, :, 1] = 1.0 - orm[:, :, 1]
    guardar(orm, os.path.join(carpeta_tex, f"{slot}_orm.png"), False)
    hechos.append("orm" + ("" if ok_r or ok_m or ok_a else "(constante)"))
    return hechos


def procesar(a, fuente):
    limpiar()
    raiz_src = extraer(a["zip"], fuente) if a.get("zip") else fuente
    ruta = os.path.join(raiz_src, a["archivo"]) if a.get("zip") else os.path.join(fuente, a["archivo"])
    importar(ruta)
    obs = mallas_filtradas(a)
    if not obs:
        raise RuntimeError("sin mallas tras filtrar")
    ob = unir(obs)
    ob.name = a["nombre"]
    ob.data.name = a["nombre"]
    tris_orig = tris(ob)
    transformar(ob, a)
    decimar(ob, a.get("tris"))
    # UV: si no tiene, proyectar
    if not ob.data.uv_layers:
        seleccionar([ob])
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project(island_margin=0.02)
        bpy.ops.object.mode_set(mode="OBJECT")
    # Slots de material: o materiales del proyecto (por nombre) o propios con texturas
    carpeta = os.path.join(SALIDA, a["kit"])
    carpeta_tex = os.path.join(carpeta, "tex")
    os.makedirs(carpeta_tex, exist_ok=True)
    dirs = [os.path.dirname(ruta), raiz_src]
    mats = [s.material for s in ob.material_slots]
    # Quitar slots no usados
    usados = {p.material_index for p in ob.data.polygons}
    texinfo = []
    if a.get("material"):  # todos los slots a un material existente del proyecto (M_Piedra, M_Madera...)
        ob.data.materials.clear()
        ob.data.materials.append(bpy.data.materials.new(a["material"]))
        for p in ob.data.polygons:
            p.material_index = 0
    elif a.get("tex") or len(mats) <= 1 or a.get("un_slot"):
        nombre_slot = f"MI_{a['nombre'][3:]}"
        texinfo = texturas_slot(nombre_slot, mats[0] if mats else None, a, dirs, carpeta_tex)
        ob.data.materials.clear()
        ob.data.materials.append(bpy.data.materials.new(nombre_slot))
        for p in ob.data.polygons:
            p.material_index = 0
    else:
        nuevos = []
        remap = {}
        for i, m in enumerate(mats):
            if i not in usados:
                continue
            nombre_slot = f"MI_{a['nombre'][3:]}_{len(nuevos)}"
            texinfo += texturas_slot(nombre_slot, m, a, dirs, carpeta_tex)
            remap[i] = len(nuevos)
            nuevos.append(nombre_slot)
        idx = np.empty(len(ob.data.polygons), dtype=np.int32)
        ob.data.polygons.foreach_get("material_index", idx)
        idx = np.vectorize(lambda k: remap.get(k, 0))(idx).astype(np.int32)
        ob.data.materials.clear()
        for n in nuevos:
            ob.data.materials.append(bpy.data.materials.new(n))
        ob.data.polygons.foreach_set("material_index", idx)
        ob.data.update()
    seleccionar([ob])
    bpy.ops.export_scene.fbx(filepath=os.path.join(carpeta, a["nombre"] + ".fbx"), use_selection=True,
                             apply_unit_scale=True, axis_forward="-Y", axis_up="Z", mesh_smooth_type="FACE",
                             add_leaf_bones=False, bake_space_transform=False)
    mn, mx, _ = caja(ob)
    return tris_orig, tris(ob), mx - mn, len(ob.data.materials), texinfo


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    with open(MANIFIESTO, encoding="utf-8") as f:
        man = json.load(f)
    fuente = os.path.expanduser(man["fuente"])
    os.makedirs(SALIDA, exist_ok=True)
    informe = os.path.join(SALIDA, "INFORME.tsv")
    filas = {}
    if os.path.exists(informe):
        with open(informe, encoding="utf-8") as f:
            for linea in f:
                filas[linea.split("\t")[0]] = linea
    for a in man["assets"]:
        if argv and not any(fnmatch.fnmatch(a["nombre"], p) for p in argv):
            continue
        try:
            t0, t1, dims, nm, tex = procesar(a, fuente)
            linea = f"{a['nombre']}\t{a['kit']}\t{t0}\t{t1}\t{dims[0]:.2f}x{dims[1]:.2f}x{dims[2]:.2f}\t{nm}\t{','.join(tex)}\n"
            print("OK", linea.strip())
        except Exception as e:  # se registra y se sigue con el resto
            import traceback
            traceback.print_exc()
            linea = f"{a['nombre']}\t{a['kit']}\tERROR\t{str(e)[:120]}\n"
            print("ERROR", a["nombre"], e)
        filas[a["nombre"]] = linea
    with open(informe, "w", encoding="utf-8") as f:
        f.write("".join(filas[k] for k in sorted(filas)))


main()
