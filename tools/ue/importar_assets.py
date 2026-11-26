"""Importa a Unreal todo lo de assets_fuente/ y arma los materiales.

- UI (PNG) -> /Game/Vaelith/UI (sin mips, grupo UI)
- Texturas PBR -> /Game/Vaelith/Texturas/<id>/
- Audio (WAV) -> /Game/Vaelith/Audio (mus_* y amb_* en loop)
- Fuentes -> /Game/Vaelith/UI/F_Texto, F_Titulo (runtime, base 24 px)
- Materiales -> /Game/Vaelith/Materiales (maestros M_Mundo, M_Liso, M_Fantasma + instancias)
- Mallas FBX -> /Game/Vaelith/Armas y /Game/Vaelith/Mallas/<kit>, con materiales por slot
Idempotente: reemplaza lo existente.
Uso: tools/ue/correr.sh tools/ue/importar_assets.py
"""
import glob
import os

import unreal

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FUENTE = os.path.join(RAIZ, "assets_fuente")
MAT = "/Game/Vaelith/Materiales"
tools = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary
eal = unreal.EditorAssetLibrary
problemas = []


def log(msg):
    unreal.log(f"[vaelith] {msg}")


def importar(archivo, destino, nombre=None, opciones=None):
    t = unreal.AssetImportTask()
    t.filename = archivo
    t.destination_path = destino
    if nombre:
        t.destination_name = nombre
    t.automated = True
    t.replace_existing = True
    t.save = False
    if opciones:
        t.options = opciones
    tools.import_asset_tasks([t])
    rutas = list(t.imported_object_paths)
    return unreal.load_asset(rutas[0]) if rutas else None


# ---------------------------------------------------------------- UI y texturas

def importar_ui():
    n = 0
    for png in sorted(glob.glob(os.path.join(FUENTE, "ui", "*.png"))):
        tex = importar(png, "/Game/Vaelith/UI")
        if not tex:
            problemas.append(f"UI {png}")
            continue
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_EDITOR_ICON)
        tex.set_editor_property("mip_gen_settings", unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
        tex.set_editor_property("lod_group", unreal.TextureGroup.TEXTUREGROUP_UI)
        n += 1
    log(f"UI: {n} texturas")


def importar_pbr():
    texs = {}
    for carpeta in sorted(glob.glob(os.path.join(FUENTE, "texturas", "*"))):
        tid = os.path.basename(carpeta)
        dest = f"/Game/Vaelith/Texturas/{tid}"
        for mapa in ("color", "normal", "arm"):
            ruta = os.path.join(carpeta, f"{mapa}.jpg")
            if not os.path.exists(ruta):
                continue
            tex = importar(ruta, dest, f"T_{tid}_{mapa}")
            if not tex:
                problemas.append(f"textura {tid}/{mapa}")
                continue
            if mapa == "normal":
                tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
                tex.set_editor_property("srgb", False)
            elif mapa == "arm":
                tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
                tex.set_editor_property("srgb", False)
            texs[(tid, mapa)] = tex
    log(f"PBR: {len(texs)} texturas")
    return texs


def importar_audio():
    n = 0
    for wav in sorted(glob.glob(os.path.join(FUENTE, "audio", "*.wav"))):
        nombre = os.path.splitext(os.path.basename(wav))[0]
        s = importar(wav, "/Game/Vaelith/Audio", nombre)
        if not s:
            problemas.append(f"audio {nombre}")
            continue
        if nombre.startswith(("mus_", "amb_")):
            s.set_editor_property("looping", True)
        n += 1
    log(f"audio: {n} sonidos")


def importar_fuentes():
    for ttf, nombre in (("EBGaramond.ttf", "F_Texto"), ("Cinzel.ttf", "F_Titulo")):
        ruta = os.path.join(FUENTE, "fuentes", ttf)
        cara = importar(ruta, "/Game/Vaelith/UI/Fuentes")
        if not cara:
            problemas.append(f"fuente {ttf}")
            continue
        try:
            if eal.does_asset_exist(f"/Game/Vaelith/UI/{nombre}"):
                eal.delete_asset(f"/Game/Vaelith/UI/{nombre}")
            fuente = tools.create_asset(nombre, "/Game/Vaelith/UI", unreal.Font, unreal.FontFactory())
            fuente.set_editor_property("font_cache_type", unreal.FontCacheType.RUNTIME)
            fuente.set_editor_property("legacy_font_size", 24)
            datos = unreal.FontData()
            datos.set_editor_property("font_face_asset", cara)
            entrada = unreal.TypefaceEntry()
            entrada.set_editor_property("name", "Regular")
            entrada.set_editor_property("font", datos)
            tipo = unreal.Typeface()
            tipo.set_editor_property("fonts", [entrada])
            comp = fuente.get_editor_property("composite_font")
            comp.set_editor_property("default_typeface", tipo)
            fuente.set_editor_property("composite_font", comp)
            log(f"fuente {nombre} OK")
        except Exception as e:  # la API de fuentes cambia entre versiones
            problemas.append(f"fuente {nombre}: {e}")


# ---------------------------------------------------------------- materiales

def nuevo_material(nombre):
    ruta = f"{MAT}/{nombre}"
    if eal.does_asset_exist(ruta):
        eal.delete_asset(ruta)
    return tools.create_asset(nombre, MAT, unreal.Material, unreal.MaterialFactoryNew())


def expr(m, clase, x, y):
    return mel.create_material_expression(m, clase, x, y)


def conectar(a, sa, b, sb):
    if not mel.connect_material_expressions(a, sa, b, sb):
        problemas.append(f"no conectó {a.get_name()}.{sa} -> {b.get_name()}.{sb}")


def funcion(m, ruta, x, y):
    f = expr(m, unreal.MaterialExpressionMaterialFunctionCall, x, y)
    f.set_editor_property("material_function", unreal.load_asset(ruta))
    return f


def material_mundo(texs):
    """Maestro con proyección en espacio de mundo (no depende de los UV de Blender)."""
    m = nuevo_material("M_Mundo")
    tid = "castle_wall_slates"
    escala = expr(m, unreal.MaterialExpressionScalarParameter, -900, 0)
    escala.set_editor_property("parameter_name", "Escala")
    escala.set_editor_property("default_value", 250.0)
    salidas = {}
    for i, mapa in enumerate(("color", "normal", "arm")):
        obj = expr(m, unreal.MaterialExpressionTextureObjectParameter, -900, 150 + i * 220)
        obj.set_editor_property("parameter_name", mapa.capitalize())
        if (tid, mapa) in texs:
            obj.set_editor_property("texture", texs[(tid, mapa)])
        if mapa == "normal":
            obj.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
        elif mapa == "arm":
            obj.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)
        ruta = "/Engine/Functions/Engine_MaterialFunctions01/Texturing/WorldAlignedNormal" if mapa == "normal" else \
               "/Engine/Functions/Engine_MaterialFunctions01/Texturing/WorldAlignedTexture"
        f = funcion(m, ruta, -550, 150 + i * 220)
        conectar(obj, "", f, "TextureObject")
        conectar(escala, "", f, "TextureSize")
        salidas[mapa] = f
    tinte = expr(m, unreal.MaterialExpressionVectorParameter, -550, -150)
    tinte.set_editor_property("parameter_name", "Tinte")
    tinte.set_editor_property("default_value", unreal.LinearColor(1, 1, 1, 1))
    mult = expr(m, unreal.MaterialExpressionMultiply, -250, 0)
    conectar(salidas["color"], "XYZ Texture", mult, "A")
    conectar(tinte, "", mult, "B")
    mel.connect_material_property(mult, "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(salidas["normal"], "XYZ Texture", unreal.MaterialProperty.MP_NORMAL)
    for canal, prop, x in (("R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION, 300),
                           ("G", unreal.MaterialProperty.MP_ROUGHNESS, 400),
                           ("B", unreal.MaterialProperty.MP_METALLIC, 500)):
        mask = expr(m, unreal.MaterialExpressionComponentMask, -250, x)
        for c in "RGBA":
            mask.set_editor_property(c.lower(), c == canal)
        conectar(salidas["arm"], "XYZ Texture", mask, "")
        mel.connect_material_property(mask, "", prop)
    mel.recompile_material(m)
    return m


def material_liso():
    """Maestro de color plano: metales, hueso, tela, emisivos y los no-muertos."""
    m = nuevo_material("M_Liso")
    def vec(nombre, valor, x, y):
        v = expr(m, unreal.MaterialExpressionVectorParameter, x, y)
        v.set_editor_property("parameter_name", nombre)
        v.set_editor_property("default_value", valor)
        return v
    def esc(nombre, valor, x, y):
        s = expr(m, unreal.MaterialExpressionScalarParameter, x, y)
        s.set_editor_property("parameter_name", nombre)
        s.set_editor_property("default_value", valor)
        return s
    color = vec("Color", unreal.LinearColor(0.5, 0.5, 0.5, 1), -600, -200)
    mel.connect_material_property(color, "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(esc("Rugosidad", 0.7, -600, 0), "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.connect_material_property(esc("Metalico", 0.0, -600, 100), "", unreal.MaterialProperty.MP_METALLIC)
    # Emisivo = Emisivo * Fuerza + Fresnel * ColorBorde * Borde
    emi = vec("Emisivo", unreal.LinearColor(0, 0, 0, 1), -900, 250)
    fuerza = esc("Fuerza", 1.0, -900, 400)
    m1 = expr(m, unreal.MaterialExpressionMultiply, -600, 300)
    conectar(emi, "", m1, "A"); conectar(fuerza, "", m1, "B")
    fres = expr(m, unreal.MaterialExpressionFresnel, -900, 550)
    borde = vec("ColorBorde", unreal.LinearColor(0, 0, 0, 1), -900, 700)
    peso = esc("Borde", 0.0, -900, 850)
    m2 = expr(m, unreal.MaterialExpressionMultiply, -600, 600)
    conectar(fres, "", m2, "A"); conectar(borde, "", m2, "B")
    m3 = expr(m, unreal.MaterialExpressionMultiply, -400, 650)
    conectar(m2, "", m3, "A"); conectar(peso, "", m3, "B")
    suma = expr(m, unreal.MaterialExpressionAdd, -200, 400)
    conectar(m1, "", suma, "A"); conectar(m3, "", suma, "B")
    mel.connect_material_property(suma, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    mel.recompile_material(m)
    return m


def material_fantasma():
    m = nuevo_material("M_Fantasma")
    m.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    m.set_editor_property("two_sided", True)
    color = expr(m, unreal.MaterialExpressionConstant3Vector, -700, -100)
    color.set_editor_property("constant", unreal.LinearColor(0.35, 0.55, 1.0, 1))
    fres = expr(m, unreal.MaterialExpressionFresnel, -700, 100)
    base = expr(m, unreal.MaterialExpressionConstant, -700, 250)
    base.set_editor_property("r", 0.25)
    suma = expr(m, unreal.MaterialExpressionAdd, -450, 150)
    conectar(fres, "", suma, "A"); conectar(base, "", suma, "B")
    brillo = expr(m, unreal.MaterialExpressionMultiply, -250, 0)
    conectar(color, "", brillo, "A"); conectar(suma, "", brillo, "B")
    k = expr(m, unreal.MaterialExpressionConstant, -450, -250)
    k.set_editor_property("r", 3.0)
    emi = expr(m, unreal.MaterialExpressionMultiply, -100, -100)
    conectar(brillo, "", emi, "A"); conectar(k, "", emi, "B")
    mel.connect_material_property(emi, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    op = expr(m, unreal.MaterialExpressionMultiply, -250, 300)
    k2 = expr(m, unreal.MaterialExpressionConstant, -450, 400)
    k2.set_editor_property("r", 0.55)
    conectar(suma, "", op, "A"); conectar(k2, "", op, "B")
    mel.connect_material_property(op, "", unreal.MaterialProperty.MP_OPACITY)
    mel.recompile_material(m)
    return m


def instancia(nombre, padre, texturas=None, vectores=None, escalares=None):
    ruta = f"{MAT}/{nombre}"
    if eal.does_asset_exist(ruta):
        eal.delete_asset(ruta)
    mi = tools.create_asset(nombre, MAT, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(mi, padre)
    for k, v in (texturas or {}).items():
        if v:
            mel.set_material_instance_texture_parameter_value(mi, k, v)
    for k, v in (vectores or {}).items():
        mel.set_material_instance_vector_parameter_value(mi, k, v)
    for k, v in (escalares or {}).items():
        mel.set_material_instance_scalar_parameter_value(mi, k, v)
    return mi


def crear_materiales(texs):
    mundo = material_mundo(texs)
    liso = material_liso()
    material_fantasma()
    C = unreal.LinearColor
    def pbr(nombre, tid, tinte=(1, 1, 1), escala=250.0):
        instancia(nombre, mundo,
                  {"Color": texs.get((tid, "color")), "Normal": texs.get((tid, "normal")), "Arm": texs.get((tid, "arm"))},
                  {"Tinte": C(*tinte, 1)}, {"Escala": escala})
    pbr("M_Piedra", "castle_wall_slates", (0.62, 0.66, 0.74))
    pbr("M_Piso", "cobblestone_floor_06", (0.55, 0.58, 0.64), 300.0)
    pbr("M_Madera", "brown_planks_04", (0.5, 0.42, 0.36), 200.0)
    pbr("M_Corteza", "bark_brown_02", (0.6, 0.55, 0.5), 150.0)
    pbr("M_Suelo_Bosque", "forrest_ground_01", (0.7, 0.75, 0.7), 400.0)
    pbr("M_Roca", "rock_face", (0.6, 0.62, 0.66), 400.0)
    # Piezas del kit del despertar
    pbr("M_Piedra_Negra", "castle_wall_slates", (0.3, 0.32, 0.38))
    pbr("M_Piedra_Columna", "castle_wall_slates", (0.55, 0.6, 0.72))
    pbr("M_Piedra_Escombro", "rock_face", (0.45, 0.48, 0.55), 200.0)
    pbr("M_Piedra_Suelo", "cobblestone_floor_06", (0.45, 0.48, 0.55), 300.0)
    def plano(nombre, color, rug=0.7, met=0.0, emi=(0, 0, 0), fuerza=1.0, borde=(0, 0, 0), peso=0.0):
        instancia(nombre, liso, None,
                  {"Color": C(*color, 1), "Emisivo": C(*emi, 1), "ColorBorde": C(*borde, 1)},
                  {"Rugosidad": rug, "Metalico": met, "Fuerza": fuerza, "Borde": peso})
    plano("M_Hueso", (0.72, 0.68, 0.58), 0.65)
    plano("M_Metal", (0.32, 0.33, 0.36), 0.38, 1.0)
    plano("M_Tela", (0.05, 0.07, 0.16), 0.92)
    plano("M_Oro", (0.85, 0.66, 0.33), 0.3, 1.0)
    plano("M_Emisivo", (0, 0, 0), 1.0, 0.0, (1.0, 0.62, 0.3), 5.0)
    plano("M_Zombi", (0.26, 0.28, 0.22), 0.88, 0.0, (0, 0, 0), 1.0, (0.2, 0.35, 0.2), 0.4)
    plano("M_Esqueleto", (0.74, 0.7, 0.6), 0.6)
    plano("M_Sombra", (0.015, 0.015, 0.02), 0.3, 0.6, (0, 0, 0), 1.0, (0.5, 0.25, 1.0), 4.0)
    log("materiales OK")


# ---------------------------------------------------------------- mallas

def importar_mallas(solo=None):
    lotes = [("armas_torre", "/Game/Vaelith/Mallas/Torre"), ("props_osario", "/Game/Vaelith/Mallas/Osario"),
             ("kit_despertar", "/Game/Vaelith/Mallas/Despertar"), ("kit_catacumba", "/Game/Vaelith/Mallas/Catacumba"),
             ("arboles_prueba", "/Game/Vaelith/Mallas/Bosque")]
    armas = {"SM_Espada_Larga", "SM_Escudo_Pharasma", "SM_Daga_Pharasma"}
    n = 0
    for kit, destino in lotes:
        if solo and kit not in solo:
            continue
        for fbx in sorted(glob.glob(os.path.join(FUENTE, kit, "*.fbx"))):
            nombre = os.path.splitext(os.path.basename(fbx))[0]
            dest = "/Game/Vaelith/Armas" if nombre in armas else destino
            malla = importar(fbx, dest, nombre)
            if not isinstance(malla, unreal.StaticMesh):
                malla = unreal.load_asset(f"{dest}/{nombre}")
            if not isinstance(malla, unreal.StaticMesh):
                problemas.append(f"malla {nombre}")
                continue
            for i, slot in enumerate(malla.get_editor_property("static_materials")):
                sn = str(slot.get_editor_property("material_slot_name"))
                if kit == "arboles_prueba":
                    sn = "M_Corteza"
                mat = unreal.load_asset(f"{MAT}/{sn}") if eal.does_asset_exist(f"{MAT}/{sn}") else None
                if mat:
                    malla.set_material(i, mat)
                else:
                    problemas.append(f"{nombre}: sin material para slot {sn}")
            if nombre not in armas:
                cuerpo = malla.get_editor_property("body_setup")
                if cuerpo:
                    cuerpo.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
            n += 1
    log(f"mallas: {n}")


def main():
    solo = os.environ.get("VAELITH_SOLO_MALLAS")
    if solo:
        importar_mallas(solo.split(","))
        eal.save_directory("/Game/Vaelith/Mallas", only_if_is_dirty=False, recursive=True)
        eal.save_directory("/Game/Vaelith/Armas", only_if_is_dirty=False, recursive=True)
        log("reimportar mallas OK")
        return
    importar_ui()
    texs = importar_pbr()
    importar_audio()
    importar_fuentes()
    crear_materiales(texs)
    importar_mallas()
    eal.save_directory("/Game/Vaelith", only_if_is_dirty=False, recursive=True)
    for p in problemas:
        unreal.log_warning(f"[vaelith] PROBLEMA: {p}")
    log(f"importar_assets OK ({len(problemas)} problemas)")


main()
