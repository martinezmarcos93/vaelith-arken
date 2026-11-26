"""Cielo nocturno: importa T_Estrellas y T_Luna y crea M_Cielo (sin luz, se dibuja sobre SM_SkySphere).

El material calcula la dirección de vista y muestrea las estrellas en equirectangular (no depende de las UV
de la malla). Dibuja la luna en la dirección del parámetro DirLuna y funde el horizonte con el color de la niebla,
para que no quede un corte entre el cielo y el terreno lejano.
Uso: python3 tools/texturas_cielo.py && tools/ue/correr.sh tools/ue/cielo.py
"""
import os

import unreal

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEST = "/Game/Vaelith/Cielo"
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()


def importar(nombre, srgb=True):
    t = unreal.AssetImportTask()
    t.filename = os.path.join(RAIZ, "assets_fuente", "texturas", nombre + ".png")
    t.destination_path = DEST
    t.replace_existing = True
    t.automated = True
    t.save = True
    tools.import_asset_tasks([t])
    tex = unreal.load_asset(f"{DEST}/{nombre}")
    tex.set_editor_property("srgb", srgb)
    tex.set_editor_property("mip_gen_settings", unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)  # sin costura de mip en el acimut
    tex.set_editor_property("never_stream", True)
    tex.set_editor_property("lod_group", unreal.TextureGroup.TEXTUREGROUP_SKYBOX)
    eal.save_asset(f"{DEST}/{nombre}")
    return tex


CODIGO = r"""
float3 d = -normalize(V);
// Estrellas (equirectangular: u acimut, v 0 en el cenit)
float u = atan2(d.y, d.x) / 6.2831853 + 0.5;
float v = acos(clamp(d.z, -1.0, 1.0)) / 3.14159265;
float3 est = Estrellas.SampleLevel(EstrellasSampler, float2(u, v), 0).rgb;
float alto = saturate((d.z - Horizonte) / 0.35);
float3 cielo = Base * (1.0 - 0.6 * alto) + est * BrilloEstrellas * alto;
// Luna: disco orientado a la cámara en la dirección DirLuna
float3 m = normalize(DirLuna);
float3 t1 = normalize(cross(m, float3(0, 0, 1)));
float3 t2 = cross(t1, m);
float cara = dot(d, m);
float2 p = float2(dot(d, t1), dot(d, t2)) / RadioLuna;  // radio 1 = borde del disco
if (cara > 0.0 && abs(p.x) < 1.6 && abs(p.y) < 1.6)
{
    // la textura tiene el disco en el 60 % central (radio 0,30 del lado)
    float4 l = Luna.SampleLevel(LunaSampler, p * 0.30 + 0.5, 0);
    float r = length(p);
    float disco = 1.0 - smoothstep(0.97, 1.0, r);
    float halo = pow(saturate(1.0 - (r - 1.0) / 0.6), 2.0) * (1.0 - disco);
    cielo = cielo * (1.0 - disco) + l.rgb * BrilloLuna * disco + ColorHalo * halo * BrilloLuna;
}
// Horizonte: se funde con la niebla (abajo del horizonte, niebla pura)
float h = saturate((d.z - Horizonte + 0.04) / 0.22);
return lerp(ColorNiebla, cielo, h);
"""


def material_cielo(estrellas, luna):
    ruta = f"{DEST}/M_Cielo"
    if eal.does_asset_exist(ruta):
        eal.delete_asset(ruta)
    m = tools.create_asset("M_Cielo", DEST, unreal.Material, unreal.MaterialFactoryNew())
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    m.set_editor_property("two_sided", True)
    m.set_editor_property("is_sky", True)
    c = mel.create_material_expression(m, unreal.MaterialExpressionCustom, -300, 0)
    c.set_editor_property("code", CODIGO)
    c.set_editor_property("output_type", unreal.CustomMaterialOutputType.CMOT_FLOAT3)
    nombres = ["V", "Estrellas", "Luna", "DirLuna", "RadioLuna", "BrilloEstrellas", "BrilloLuna", "ColorHalo", "Base", "ColorNiebla", "Horizonte"]
    entradas = []
    for n in nombres:
        e = unreal.CustomInput()
        e.set_editor_property("input_name", n)
        entradas.append(e)
    c.set_editor_property("inputs", entradas)
    y = -600

    def conectar(expr, nombre):
        mel.connect_material_expressions(expr, "", c, nombre)

    def vec(nombre, valor):
        nonlocal y
        e = mel.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -800, y)
        e.set_editor_property("parameter_name", nombre)
        e.set_editor_property("default_value", valor)
        y += 120
        conectar(e, nombre)

    def esc(nombre, valor):
        nonlocal y
        e = mel.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -800, y)
        e.set_editor_property("parameter_name", nombre)
        e.set_editor_property("default_value", valor)
        y += 120
        conectar(e, nombre)

    cam = mel.create_material_expression(m, unreal.MaterialExpressionCameraVectorWS, -800, y)
    y += 120
    conectar(cam, "V")
    for nombre, tex in (("Estrellas", estrellas), ("Luna", luna)):
        t = mel.create_material_expression(m, unreal.MaterialExpressionTextureObjectParameter, -800, y)
        t.set_editor_property("parameter_name", nombre)
        t.set_editor_property("texture", tex)
        y += 120
        conectar(t, nombre)
    vec("DirLuna", unreal.LinearColor(-0.45, 0.65, 0.62, 0))
    esc("RadioLuna", 0.045)
    esc("BrilloEstrellas", 1.6)
    esc("BrilloLuna", 3.0)
    vec("ColorHalo", unreal.LinearColor(0.10, 0.13, 0.22, 0))
    vec("Base", unreal.LinearColor(0.006, 0.008, 0.018, 0))
    vec("ColorNiebla", unreal.LinearColor(0.025, 0.035, 0.07, 0))
    esc("Horizonte", 0.02)
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    mel.recompile_material(m)
    eal.save_asset(ruta)
    return m


est = importar("T_Estrellas")
lun = importar("T_Luna")
mat = material_cielo(est, lun)
unreal.log(f"[vaelith] cielo: {mat.get_path_name()} listo")
