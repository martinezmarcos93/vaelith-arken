"""Kit de la Escena 1 (El despertar) para Vaelith Arken en Unreal.

Genera piezas modulares con geometría procedural y UVs, las exporta a FBX
(una por pieza) y renderiza una vista previa de la escena armada.

Uso:
    ~/Aplicaciones/blender-5.3.0/blender -b --factory-startup \
        -P tools/blender/kit_despertar.py -- <carpeta_salida>

Determinista: misma semilla → mismas piezas.
"""
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Vector, noise

SEMILLA = 1793
random.seed(SEMILLA)

# Paleta canónica (docs/guia_estilo_visual.md del proyecto Godot).
PALETA = {
    "negro_base": "#010901",
    "piedra_oscura": "#11222E",
    "piedra_media": "#162C3D",
    "indigo": "#2B2E56",
    "luz_luna": "#3A5184",
    "teal": "#07424F",
    "oxido": "#4D1409",
}


def hex_lineal(h):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb) + (1.0,)


def limpiar_escena():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material_piedra(nombre, base, veta, rugosidad=0.85):
    """Piedra procedural para la vista previa; en Unreal se rehace con texturas."""
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    ruido = nt.nodes.new("ShaderNodeTexNoise")
    ruido.inputs["Scale"].default_value = 3.5
    ruido.inputs["Detail"].default_value = 8.0
    rampa = nt.nodes.new("ShaderNodeValToRGB")
    rampa.color_ramp.elements[0].color = hex_lineal(base)
    rampa.color_ramp.elements[1].color = hex_lineal(veta)
    rampa.color_ramp.elements[0].position = 0.35
    rampa.color_ramp.elements[1].position = 0.75
    nt.links.new(ruido.outputs["Fac"], rampa.inputs["Fac"])
    nt.links.new(rampa.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = rugosidad
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.35
    nt.links.new(ruido.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def objeto_desde_bmesh(nombre, bm, material):
    me = bpy.data.meshes.new(nombre)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    me.materials.append(material)
    for p in me.polygons:
        p.use_smooth = False
    return ob


def desplazar(bm, fuerza, escala, filtro=None):
    for v in bm.verts:
        if filtro and not filtro(v):
            continue
        n = noise.noise_vector(v.co * escala)
        v.co += Vector(n) * fuerza


def uv_y_limpieza(ob):
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")


# ---------------------------------------------------------------- piezas

def losa_altar(mat):
    """Losa de piedra negra donde despierta Vaelith (2,4 x 1,1 x 0,7 m)."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= 2.4
        v.co.y *= 1.1
        v.co.z = (v.co.z + 0.5) * 0.7
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=0.06, segments=2, affect="EDGES")
    bmesh.ops.subdivide_edges(bm, edges=list(bm.edges), cuts=3, use_grid_fill=True)
    desplazar(bm, 0.035, 2.2, filtro=lambda v: v.co.z > 0.05)
    return objeto_desde_bmesh("SM_Losa_Altar", bm, mat)


def fuste_columna(radio, alto, lados=16, estrias=True):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=lados, radius1=radio, radius2=radio * 0.92, depth=alto)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, alto / 2))
    bmesh.ops.subdivide_edges(
        bm, edges=[e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) > 0.01], cuts=int(alto * 3)
    )
    if estrias:
        for v in bm.verts:
            ang = math.atan2(v.co.y, v.co.x)
            r = math.hypot(v.co.x, v.co.y)
            if r > radio * 0.5:
                f = 1.0 - 0.04 * (0.5 + 0.5 * math.cos(ang * lados))
                v.co.x *= f
                v.co.y *= f
    return bm


def agregar_bloque(bm, ancho, alto, z):
    tmp = bmesh.new()
    bmesh.ops.create_cube(tmp, size=1.0)
    for v in tmp.verts:
        v.co.x *= ancho
        v.co.y *= ancho
        v.co.z = v.co.z * alto + z + alto / 2
    bmesh.ops.bevel(tmp, geom=list(tmp.edges), offset=0.03, segments=1, affect="EDGES")
    me = bpy.data.meshes.new("_tmp")
    tmp.to_mesh(me)
    tmp.free()
    bm.from_mesh(me)
    bpy.data.meshes.remove(me)


def romper_arriba(bm, alto_corte, irregularidad):
    """Corta el fuste y vuelve dentado el borde superior."""
    geom = list(bm.verts) + list(bm.edges) + list(bm.faces)
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, alto_corte), plane_no=(0, 0, 1), clear_outer=True)
    borde = [v for v in bm.verts if abs(v.co.z - alto_corte) < 1e-4]
    bmesh.ops.contextual_create(bm, geom=[e for e in bm.edges if all(abs(v.co.z - alto_corte) < 1e-4 for v in e.verts)])
    for v in borde:
        v.co.z += random.uniform(-irregularidad, irregularidad * 0.4)
    desplazar(bm, 0.03, 3.0, filtro=lambda v: v.co.z > alto_corte - irregularidad * 1.5)


def columna(nombre, mat, alto_corte=None):
    radio, alto = 0.45, 7.5
    bm = fuste_columna(radio, alto)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.5))
    if alto_corte:
        romper_arriba(bm, alto_corte, 0.35)
    agregar_bloque(bm, radio * 2.6, 0.5, 0.0)  # basa
    if not alto_corte:
        agregar_bloque(bm, radio * 2.8, 0.45, alto + 0.5)  # capitel
    return objeto_desde_bmesh(nombre, bm, mat)


def tambor_caido(mat):
    bm = fuste_columna(0.45, 1.6, estrias=True)
    desplazar(bm, 0.03, 3.0)
    ob = objeto_desde_bmesh("SM_Columna_Tambor", bm, mat)
    return ob


def escombro(i, mat):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
    s = Vector((random.uniform(0.25, 0.7), random.uniform(0.2, 0.55), random.uniform(0.15, 0.4)))
    for v in bm.verts:
        v.co = Vector((v.co.x * s.x, v.co.y * s.y, v.co.z * s.z))
    desplazar(bm, 0.09, 2.5 + i * 0.3)
    # Facetas planas: piedra partida, no canto rodado.
    for _ in range(3):
        n = Vector((random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))).normalized()
        geom = list(bm.verts) + list(bm.edges) + list(bm.faces)
        bmesh.ops.bisect_plane(bm, geom=geom, plane_co=n * 0.12, plane_no=n, clear_outer=True)
        bmesh.ops.contextual_create(bm, geom=[e for e in bm.edges if e.is_boundary])
    minz = min(v.co.z for v in bm.verts)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, -minz))
    return objeto_desde_bmesh(f"SM_Escombro_{i:02d}", bm, mat)


def baldosa_suelo(mat):
    """Módulo de suelo de 4 x 4 m: losas irregulares con juntas hundidas."""
    bm = bmesh.new()
    paso = 1.0
    for ix in range(4):
        for iy in range(4):
            tmp = bmesh.new()
            bmesh.ops.create_cube(tmp, size=1.0)
            hundir = random.uniform(-0.03, 0.0)
            for v in tmp.verts:
                v.co.x = v.co.x * (paso - 0.06) + ix * paso - 1.5
                v.co.y = v.co.y * (paso - 0.06) + iy * paso - 1.5
                v.co.z = (v.co.z - 0.5) * 0.25 + hundir
            bmesh.ops.bevel(tmp, geom=list(tmp.edges), offset=0.025, segments=1, affect="EDGES")
            me = bpy.data.meshes.new("_tmp")
            tmp.to_mesh(me)
            tmp.free()
            bm.from_mesh(me)
            bpy.data.meshes.remove(me)
    return objeto_desde_bmesh("SM_Suelo_Losas_4m", bm, mat)


# ---------------------------------------------------------------- exportar y previsualizar

def exportar(ob, carpeta):
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    ruta = os.path.join(carpeta, f"{ob.name}.fbx")
    bpy.ops.export_scene.fbx(
        filepath=ruta, use_selection=True, apply_unit_scale=True, apply_scale_options="FBX_SCALE_UNITS",
        bake_space_transform=True, mesh_smooth_type="FACE", add_leaf_bones=False, path_mode="STRIP",
    )
    return ruta


def armar_preview(piezas, mats, carpeta):
    esc = bpy.context.scene
    # Disposición de la Escena 1 (solo para la vista previa).
    colocaciones = {
        "SM_Losa_Altar": ((0, 0, 0), 8),
        "SM_Columna_Entera": ((-4.5, 3.5, 0), 0),
        "SM_Columna_Rota_Alta": ((4.2, 3.8, 0), 25),
        "SM_Columna_Rota_Baja": ((-3.2, -3.6, 0), 60),
        "SM_Columna_Tambor": ((2.6, -2.4, 0.45), 0),
    }
    for nombre, (pos, rot) in colocaciones.items():
        ob = piezas[nombre]
        ob.location = pos
        ob.rotation_euler.z = math.radians(rot)
    tambor = piezas["SM_Columna_Tambor"]
    tambor.rotation_euler = (math.radians(90), 0, math.radians(35))
    for i, ob in enumerate(o for n, o in piezas.items() if n.startswith("SM_Escombro")):
        ob.location = (random.uniform(-5, 5), random.uniform(-4.5, 4.5), 0)
        ob.rotation_euler.z = random.uniform(0, math.tau)
    suelo = piezas["SM_Suelo_Losas_4m"]
    for dx in (-4, 0, 4):
        for dy in (-4, 0, 4):
            if (dx, dy) == (0, 0):
                suelo.location = (0, 0, 0)
                continue
            c = suelo.copy()
            c.location = (dx, dy, 0)
            esc.collection.objects.link(c)

    mundo = bpy.data.worlds.new("Cielo_Gris")
    mundo.use_nodes = True
    bg = mundo.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hex_lineal("#3B4272")
    bg.inputs["Strength"].default_value = 0.35
    esc.world = mundo

    luna = bpy.data.lights.new("Luz_Luna", "SUN")
    luna.energy = 2.2
    luna.color = hex_lineal("#3A5184")[:3]
    luna.angle = math.radians(8)
    ol = bpy.data.objects.new("Luz_Luna", luna)
    ol.rotation_euler = (math.radians(52), 0, math.radians(-35))
    esc.collection.objects.link(ol)

    cam = bpy.data.cameras.new("Cam")
    cam.lens = 24
    oc = bpy.data.objects.new("Cam", cam)
    oc.location = (0.4, -1.1, 1.0)  # ojos de Vaelith al incorporarse sobre la losa
    oc.rotation_euler = (math.radians(84), 0, math.radians(-8))
    esc.collection.objects.link(oc)
    esc.camera = oc

    esc.render.engine = "CYCLES"
    esc.cycles.device = "CPU"
    esc.cycles.samples = 48
    esc.cycles.use_denoising = True
    esc.render.resolution_x, esc.render.resolution_y = 1280, 720
    esc.view_settings.view_transform = "AgX"
    vol = bpy.data.materials.new("Bruma")
    vol.use_nodes = True
    nt = vol.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    pv = nt.nodes.new("ShaderNodeVolumePrincipled")
    pv.inputs["Density"].default_value = 0.035
    pv.inputs["Color"].default_value = hex_lineal("#3B4272")
    nt.links.new(pv.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"])
    bpy.ops.mesh.primitive_cube_add(size=40, location=(0, 0, 10))
    bpy.context.active_object.data.materials.append(vol)
    bpy.context.active_object.name = "Volumen_Bruma"

    esc.render.filepath = os.path.join(carpeta, "preview_despertar.png")
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(carpeta, "kit_despertar.blend"))


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    carpeta = os.path.abspath(argv[0] if argv else "assets_fuente/kit_despertar")
    os.makedirs(carpeta, exist_ok=True)
    limpiar_escena()

    mats = {
        "losa": material_piedra("M_Piedra_Negra", PALETA["negro_base"], PALETA["piedra_oscura"], 0.7),
        "columna": material_piedra("M_Piedra_Columna", PALETA["piedra_media"], PALETA["indigo"]),
        "escombro": material_piedra("M_Piedra_Escombro", PALETA["piedra_oscura"], PALETA["luz_luna"]),
        "suelo": material_piedra("M_Piedra_Suelo", PALETA["negro_base"], PALETA["piedra_media"], 0.9),
    }
    piezas = {}
    for ob in (
        losa_altar(mats["losa"]),
        columna("SM_Columna_Entera", mats["columna"]),
        columna("SM_Columna_Rota_Alta", mats["columna"], alto_corte=4.6),
        columna("SM_Columna_Rota_Baja", mats["columna"], alto_corte=1.7),
        tambor_caido(mats["columna"]),
        baldosa_suelo(mats["suelo"]),
        *[escombro(i, mats["escombro"]) for i in range(6)],
    ):
        uv_y_limpieza(ob)
        piezas[ob.name] = ob

    informe = []
    for ob in piezas.values():
        ruta = exportar(ob, carpeta)
        dims = ob.dimensions
        informe.append(f"{ob.name}\t{len(ob.data.polygons)} caras\t{dims.x:.2f}x{dims.y:.2f}x{dims.z:.2f} m\t{os.path.basename(ruta)}")
    armar_preview(piezas, mats, carpeta)
    with open(os.path.join(carpeta, "INFORME.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(informe) + "\n")
    print("KIT OK\n" + "\n".join(informe))


if __name__ == "__main__":
    main()
