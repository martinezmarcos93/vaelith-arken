"""Importa el arte de interfaz propio (assets_fuente/ui_unreal) y crea los materiales de UI.

- Texturas -> /Game/Vaelith/UI2/ (grupo UI, sin mipmaps).
- M_UI_Barra: llenado con gradiente, rastro del daño reciente y destello (parámetros Llenado, Rastro, Destello,
  ColorA, ColorB). Lo usan las barras de vida y escudo del widget en C++.
- M_UI_Mapa: minimapa circular. Muestra Mapa centrado en Centro (UV), con Zoom y Giro; Niebla (máscara de lo
  explorado) oscurece lo no visto.
Uso: python3 tools/ui_generar.py && tools/ue/correr.sh tools/ue/ui_importar.py
"""
import glob
import os

import unreal

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEST = "/Game/Vaelith/UI2"
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()


def importar(png):
    nombre = os.path.splitext(os.path.basename(png))[0]
    t = unreal.AssetImportTask()
    t.filename = png
    t.destination_path = DEST
    t.replace_existing = True
    t.automated = True
    t.save = True
    tools.import_asset_tasks([t])
    tex = unreal.load_asset(f"{DEST}/{nombre}")
    tex.set_editor_property("lod_group", unreal.TextureGroup.TEXTUREGROUP_UI)
    tex.set_editor_property("mip_gen_settings", unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
    tex.set_editor_property("never_stream", True)
    if not nombre.startswith("T_Mapa") and nombre != "T_UI_Pergamino":
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_EDITOR_ICON)
    eal.save_asset(f"{DEST}/{nombre}")
    return tex


def material_ui(nombre, codigo, entradas, opacidad_codigo):
    ruta = f"{DEST}/{nombre}"
    if eal.does_asset_exist(ruta):
        eal.delete_asset(ruta)
    m = tools.create_asset(nombre, DEST, unreal.Material, unreal.MaterialFactoryNew())
    m.set_editor_property("material_domain", unreal.MaterialDomain.MD_UI)
    m.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
    nodos = {}
    y = -500
    for nom, tipo, valor in entradas:
        if tipo == "esc":
            e = mel.create_material_expression(m, unreal.MaterialExpressionScalarParameter, -900, y)
            e.set_editor_property("parameter_name", nom)
            e.set_editor_property("default_value", valor)
        elif tipo == "vec":
            e = mel.create_material_expression(m, unreal.MaterialExpressionVectorParameter, -900, y)
            e.set_editor_property("parameter_name", nom)
            e.set_editor_property("default_value", valor)
        elif tipo == "tex":
            e = mel.create_material_expression(m, unreal.MaterialExpressionTextureObjectParameter, -900, y)
            e.set_editor_property("parameter_name", nom)
            e.set_editor_property("texture", valor)
        else:  # uv
            e = mel.create_material_expression(m, unreal.MaterialExpressionTextureCoordinate, -900, y)
        nodos[nom] = e
        y += 110
    for salida, cod, tipo_salida, prop, x in (("color", codigo, unreal.CustomMaterialOutputType.CMOT_FLOAT3, unreal.MaterialProperty.MP_EMISSIVE_COLOR, -300),
                                             ("opacidad", opacidad_codigo, unreal.CustomMaterialOutputType.CMOT_FLOAT1, unreal.MaterialProperty.MP_OPACITY, 0)):
        c = mel.create_material_expression(m, unreal.MaterialExpressionCustom, x, 0 if salida == "color" else 300)
        c.set_editor_property("code", cod)
        c.set_editor_property("output_type", tipo_salida)
        lista = []
        for nom, _, _ in entradas:
            i = unreal.CustomInput()
            i.set_editor_property("input_name", nom)
            lista.append(i)
        c.set_editor_property("inputs", lista)
        for nom, _, _ in entradas:
            mel.connect_material_expressions(nodos[nom], "", c, nom)
        mel.connect_material_property(c, "", prop)
    mel.recompile_material(m)
    eal.save_asset(ruta)
    return m


BARRA_COLOR = r"""
float u = UV.x, v = UV.y;
float3 c = lerp(ColorA, ColorB, u);
c *= 0.75 + 0.5 * saturate(1.0 - abs(v - 0.38) * 3.0);   // brillo arriba
if (u > Llenado && u <= Rastro) c = float3(0.95, 0.85, 0.75);
return c * (1.0 + Destello * 1.5);
"""
BARRA_OPAC = r"""
float u = UV.x, v = UV.y;
float dentro = step(0.30, v) * step(v, 0.70) * step(0.02, u) * step(u, 0.98);
return dentro * step(u, max(Llenado, Rastro));
"""
MAPA_COLOR = r"""
float2 d = UV - 0.5;
float s = sin(Giro), c = cos(Giro);
float2 r = float2(d.x * c - d.y * s, d.x * s + d.y * c);
float2 m = Centro.xy + r * Zoom;
float3 col = Mapa.SampleLevel(MapaSampler, m, 0).rgb;
float visto = Niebla.SampleLevel(NieblaSampler, m, 0).r;
float fuera = step(0.0, m.x) * step(m.x, 1.0) * step(0.0, m.y) * step(m.y, 1.0);
return lerp(float3(0.02, 0.018, 0.024), col * 1.25, saturate(visto * 1.4) * fuera);
"""
MAPA_OPAC = r"""
float2 d = UV - 0.5;
return 0.92 * (1.0 - smoothstep(0.43, 0.46, length(d)));
"""


def main():
    texs = {os.path.splitext(os.path.basename(p))[0]: importar(p) for p in sorted(glob.glob(os.path.join(RAIZ, "assets_fuente", "ui_unreal", "*.png")))}
    material_ui("M_UI_Barra", BARRA_COLOR,
                [("UV", "uv", None), ("Llenado", "esc", 1.0), ("Rastro", "esc", 1.0), ("Destello", "esc", 0.0),
                 ("ColorA", "vec", unreal.LinearColor(0.55, 0.36, 0.12, 1)), ("ColorB", "vec", unreal.LinearColor(0.95, 0.78, 0.42, 1))],
                BARRA_OPAC)
    blanco = unreal.load_asset("/Engine/EngineResources/WhiteSquareTexture")
    material_ui("M_UI_Mapa", MAPA_COLOR,
                [("UV", "uv", None), ("Mapa", "tex", texs.get("T_Mapa_Exterior")), ("Niebla", "tex", blanco),
                 ("Centro", "vec", unreal.LinearColor(0.5, 0.5, 0, 0)), ("Zoom", "esc", 0.12), ("Giro", "esc", 0.0)],
                MAPA_OPAC)
    unreal.log(f"[vaelith] UI importada: {len(texs)} texturas, M_UI_Barra y M_UI_Mapa")


main()
