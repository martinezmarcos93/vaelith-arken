"""Importa los assets externos preparados por tools/blender/preparar_assets.py.

assets_fuente/externos/<kit>/<SM_x>.fbx      -> /Game/Vaelith/Ext/<kit>/SM_x  (o /Game/Vaelith/Armas si es arma)
assets_fuente/externos/<kit>/tex/<MI>_*.png  -> /Game/Vaelith/Ext/<kit>/Tex/T_<MI>_{color,normal,orm}
Materiales: maestro M_PBR (UV) + una instancia MI_* por slot. Si el slot se llama como un material
existente del proyecto (M_Piedra, M_Madera...), se usa ese.
Sin Nanite (rompe la visibilidad en la GTX 1060); LODs automáticos para mallas grandes.
Uso: [VAELITH_EXT=kit1,kit2] tools/ue/correr.sh tools/ue/importar_externos.py
"""
import glob
import os
import re

import unreal

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FUENTE = os.path.join(RAIZ, "assets_fuente", "externos")
MAT = "/Game/Vaelith/Materiales"
EXT = "/Game/Vaelith/Ext"
ARMAS = {"SM_Espada_Larga", "SM_Escudo_Pharasma", "SM_Daga_Pharasma"}
tools = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary
eal = unreal.EditorAssetLibrary
problemas = []


def log(msg):
    unreal.log(f"[vaelith] {msg}")


def importar(archivo, destino, nombre, opciones=None):
    t = unreal.AssetImportTask()
    t.filename = archivo
    t.destination_path = destino
    t.destination_name = nombre
    t.automated = True
    t.replace_existing = True
    t.save = False
    if opciones:
        t.options = opciones
    tools.import_asset_tasks([t])
    rutas = list(t.imported_object_paths)
    return unreal.load_asset(rutas[0]) if rutas else unreal.load_asset(f"{destino}/{nombre}")


def material_pbr():
    ruta = f"{MAT}/M_PBR"
    if eal.does_asset_exist(ruta):
        return unreal.load_asset(ruta)
    m = tools.create_asset("M_PBR", MAT, unreal.Material, unreal.MaterialFactoryNew())

    def tex(nombre, defecto, muestreo, y):
        t = mel.create_material_expression(m, unreal.MaterialExpressionTextureSampleParameter2D, -700, y)
        t.set_editor_property("parameter_name", nombre)
        t.set_editor_property("texture", unreal.load_asset(defecto))
        t.set_editor_property("sampler_type", muestreo)
        return t

    def esc(nombre, valor, y):
        s = mel.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -700, y)
        s.set_editor_property("parameter_name", nombre)
        s.set_editor_property("default_value", valor)
        return s
    color = tex("Color", "/Engine/EngineResources/WhiteSquareTexture", unreal.MaterialSamplerType.SAMPLERTYPE_COLOR, -300)
    normal = tex("Normal", "/Engine/EngineMaterials/DefaultNormal", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL, 0)
    # ORM: texturas TC_MASKS (lineales) -> muestreo Masks y defecto lineal. Con Linear Color + WhiteSquare (sRGB)
    # el material no compilaba en el juego (Vulkan) y todo lo externo salía con el material por defecto.
    orm = tex("ORM", "/Engine/EngineMaterials/DefaultDiffuse_TC_Masks", unreal.MaterialSamplerType.SAMPLERTYPE_MASKS, 300)
    tinte = mel.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -700, -500)
    tinte.set_editor_property("parameter_name", "Tinte")
    tinte.set_editor_property("default_value", unreal.LinearColor(1, 1, 1, 1))
    mult = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -350, -350)
    mel.connect_material_expressions(color, "RGB", mult, "A")
    mel.connect_material_expressions(tinte, "", mult, "B")
    mel.connect_material_property(mult, "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(normal, "RGB", unreal.MaterialProperty.MP_NORMAL)
    rug = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -350, 300)
    mel.connect_material_expressions(orm, "G", rug, "A")
    mel.connect_material_expressions(esc("Rugosidad", 1.0, 500), "", rug, "B")
    mel.connect_material_property(rug, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.connect_material_property(orm, "B", unreal.MaterialProperty.MP_METALLIC)
    mel.connect_material_property(orm, "R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
    # Máscara para hojas/ramas con alfa
    m.set_editor_property("two_sided", False)
    mel.recompile_material(m)
    eal.save_asset(ruta)
    return m


def textura(png, destino, nombre, tipo):
    t = importar(png, destino, nombre)
    if not t:
        problemas.append(f"textura {png}")
        return None
    if tipo == "normal":
        t.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
        t.set_editor_property("srgb", False)
    elif tipo == "orm":
        t.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
        t.set_editor_property("srgb", False)
    return t


def instancia(nombre, destino, padre, texs):
    ruta = f"{destino}/{nombre}"
    if eal.does_asset_exist(ruta):
        eal.delete_asset(ruta)
    mi = tools.create_asset(nombre, destino, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(mi, padre)
    for k, v in texs.items():
        if v:
            mel.set_material_instance_texture_parameter_value(mi, k, v)
    return mi


TEXDIR = os.path.join(RAIZ, "assets_fuente", "texturas")
RUINAS = os.path.join(FUENTE, "ruinas", "tex")
SUELOS = {  # MI sobre M_Mundo (proyección de mundo): (color, normal, arm), tinte, escala
    "M_Suelo_Cementerio": ([os.path.join(RUINAS, f"MI_Muro_Ladrillo_5_{m}.png") for m in ("color", "normal", "orm")], (0.85, 0.85, 0.8), 350.0),
    "M_Suelo_Hojas": ([os.path.join(TEXDIR, "brown_mud_leaves_01", f"{m}.jpg") for m in ("color", "normal", "arm")], (0.5, 0.5, 0.48), 400.0),
    "M_Aguja": ([os.path.join(TEXDIR, "brown_mud_leaves_01", f"{m}.jpg") for m in ("color", "normal", "arm")], (0.13, 0.2, 0.12), 110.0),
    "M_Ladrillo_Quemado": ([os.path.join(RUINAS, f"MI_Muro_Ladrillo_4_{m}.png") for m in ("color", "normal", "orm")], (0.9, 0.85, 0.8), 260.0),
}


def materiales_suelo():
    mundo = unreal.load_asset(f"{MAT}/M_Mundo")
    for nombre, (rutas, tinte, escala) in SUELOS.items():
        texs = {}
        for mapa, ruta in zip(("color", "normal", "arm"), rutas):
            if not os.path.exists(ruta):
                problemas.append(f"falta {ruta}")
                continue
            t = importar(ruta, "/Game/Vaelith/Texturas/Suelos", f"T_{nombre[2:]}_{mapa}")
            if mapa == "normal":
                t.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
                t.set_editor_property("srgb", False)
            elif mapa == "arm":
                t.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
                t.set_editor_property("srgb", False)
            texs[mapa.capitalize()] = t
        mi = instancia(nombre, MAT, mundo, texs)
        mel.set_material_instance_vector_parameter_value(mi, "Tinte", unreal.LinearColor(*tinte, 1))
        mel.set_material_instance_scalar_parameter_value(mi, "Escala", escala)
        eal.save_asset(f"{MAT}/{nombre}")
    eal.save_directory("/Game/Vaelith/Texturas/Suelos", only_if_is_dirty=False, recursive=True)
    log("suelos OK")


def main():
    solo = [k for k in os.environ.get("VAELITH_EXT", "").split(",") if k]
    pbr = material_pbr()
    if not solo or "terreno" in solo or "bosque" in solo:
        materiales_suelo()
    if not solo or "audio" in solo:
        for nombre in ("amb_llamado", "amb_viento"):
            snd = importar(os.path.join(RAIZ, "assets_fuente", "audio", f"{nombre}.wav"), "/Game/Vaelith/Audio", nombre)
            if snd:
                snd.set_editor_property("looping", True)
                eal.save_asset(f"/Game/Vaelith/Audio/{nombre}")
            else:
                problemas.append(f"audio {nombre}")
    n = 0
    for carpeta in sorted(glob.glob(os.path.join(FUENTE, "*"))):
        if not os.path.isdir(carpeta):
            continue
        kit = os.path.basename(carpeta)
        if solo and kit not in solo:
            continue
        destino = f"{EXT}/{kit}"
        # Materiales por slot
        mis = {}
        for color in sorted(glob.glob(os.path.join(carpeta, "tex", "*_color.png"))) + sorted(glob.glob(os.path.join(carpeta, "tex", "*_orm.png"))):
            slot = os.path.basename(color).rsplit("_", 1)[0]
            if slot in mis:
                continue
            texs = {}
            for tipo, param in (("color", "Color"), ("normal", "Normal"), ("orm", "ORM")):
                png = os.path.join(carpeta, "tex", f"{slot}_{tipo}.png")
                if os.path.exists(png):
                    texs[param] = textura(png, f"{destino}/Tex", f"T_{slot[3:]}_{tipo}", tipo)
            mis[slot] = instancia(slot, destino, pbr, texs)
        for fbx in sorted(glob.glob(os.path.join(carpeta, "SKM_*.fbx"))):
            nombre = os.path.splitext(os.path.basename(fbx))[0]
            op = unreal.FbxImportUI()
            op.set_editor_property("import_as_skeletal", True)
            op.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
            op.set_editor_property("skeleton", unreal.load_asset("/Game/Characters/Mannequins/Meshes/SK_Mannequin"))
            op.set_editor_property("import_materials", False)
            op.set_editor_property("import_textures", False)
            op.set_editor_property("import_animations", False)
            op.set_editor_property("create_physics_asset", False)
            op.skeletal_mesh_import_data.set_editor_property("import_morph_targets", False)
            sk = importar(fbx, destino, nombre, op)
            if not isinstance(sk, unreal.SkeletalMesh):
                problemas.append(f"esqueletal {nombre}")
                continue
            mats = sk.get_editor_property("materials")
            for i, sm in enumerate(mats):
                sn = str(sm.get_editor_property("material_slot_name"))
                if sn in mis:
                    sm.set_editor_property("material_interface", mis[sn])
                    mats[i] = sm
                else:
                    problemas.append(f"{nombre}: sin material para {sn}")
            sk.set_editor_property("materials", mats)
            # Física: reutilizar la del maniquí para que el ragdoll/colisiones no fallen
            fis = unreal.load_asset("/Game/Characters/Mannequins/Rigs/PA_Mannequin")
            if fis:
                sk.set_editor_property("physics_asset", fis)
            n += 1
            log(f"ext {kit}/{nombre}: esqueletal")
        for fbx in sorted(glob.glob(os.path.join(carpeta, "SM_*.fbx"))):
            nombre = os.path.splitext(os.path.basename(fbx))[0]
            dest = "/Game/Vaelith/Armas" if nombre in ARMAS else destino
            op = unreal.FbxImportUI()
            op.set_editor_property("import_materials", False)
            op.set_editor_property("import_textures", False)
            op.set_editor_property("import_as_skeletal", False)
            op.static_mesh_import_data.set_editor_property("combine_meshes", True)
            op.static_mesh_import_data.set_editor_property("auto_generate_collision", False)
            op.static_mesh_import_data.set_editor_property("generate_lightmap_u_vs", True)
            op.static_mesh_import_data.set_editor_property("build_nanite", False)
            malla = importar(fbx, dest, nombre, op)
            if not isinstance(malla, unreal.StaticMesh):
                problemas.append(f"malla {nombre}")
                continue
            ns = malla.get_editor_property("nanite_settings")
            ns.set_editor_property("enabled", False)
            malla.set_editor_property("nanite_settings", ns)
            for i, slot in enumerate(malla.get_editor_property("static_materials")):
                sn = re.sub(r"_\d{3}$", "", str(slot.get_editor_property("material_slot_name")))  # M_Corteza_001 -> M_Corteza
                mat = mis.get(sn)
                if not mat and eal.does_asset_exist(f"{MAT}/{sn}"):
                    mat = unreal.load_asset(f"{MAT}/{sn}")
                if mat:
                    malla.set_material(i, mat)
                else:
                    problemas.append(f"{nombre}: sin material para {sn}")
            if nombre not in ARMAS:
                cuerpo = malla.get_editor_property("body_setup")
                if cuerpo:
                    cuerpo.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
            # LODs para lo que pesa (pueblo y árboles se ven de lejos)
            tris = malla.get_num_triangles(0) if hasattr(malla, "get_num_triangles") else 0
            if tris > 3000:
                op_lod = unreal.EditorScriptingMeshReductionOptions()
                op_lod.set_editor_property("reduction_settings", [
                    unreal.EditorScriptingMeshReductionSettings(1.0, 1.0),
                    unreal.EditorScriptingMeshReductionSettings(0.4, 0.3),
                    unreal.EditorScriptingMeshReductionSettings(0.12, 0.1)])
                unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).set_lods(malla, op_lod)
            n += 1
            log(f"ext {kit}/{nombre}: {tris} tris")
        eal.save_directory(destino, only_if_is_dirty=False, recursive=True)
    eal.save_directory("/Game/Vaelith/Armas", only_if_is_dirty=False, recursive=True)
    for p in problemas:
        unreal.log_warning(f"[vaelith] PROBLEMA: {p}")
    log(f"importar_externos OK: {n} mallas, {len(problemas)} problemas")


main()
