"""Fase D: materiales de agua, hierro oxidado, runa y piedra con variación.

- M_MundoVariado: como M_Mundo (proyección de mundo) más variación macro de color, musgo y humedad
  (parámetros Variacion, Musgo, Humedad, ColorMusgo). Las instancias de piedra de M_Mundo pasan a este
  maestro con valores por zona: la misma textura deja de leerse igual en todas las paredes.
- M_AguaMaestro: casi negra, muy lisa (refleja con SSR), dos normales que se desplazan en direcciones
  distintas. Instancias M_Agua_Quieta (catacumba) y M_Agua_Corriente (arroyo).
- M_Hierro: hierro oxidado (instancia de M_MundoVariado con T_Oxido_*). M_Runa: espiral emisiva violeta.
Uso: python3 tools/texturas_d.py && tools/ue/correr.sh tools/ue/materiales_d.py
"""
import os

import unreal

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MAT = "/Game/Vaelith/Materiales"
TEX = "/Game/Vaelith/Texturas/Fase_D"
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
problemas = []


def log(m):
    unreal.log(f"[vaelith] {m}")


def importar_tex(nombre, tipo):
    t = unreal.AssetImportTask()
    t.filename = os.path.join(RAIZ, "assets_fuente", "texturas", nombre + ".png")
    t.destination_path = TEX
    t.replace_existing = True
    t.automated = True
    t.save = True
    tools.import_asset_tasks([t])
    tex = unreal.load_asset(f"{TEX}/{nombre}")
    if tipo == "normal":
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
        tex.set_editor_property("srgb", False)
    elif tipo == "masks":
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
        tex.set_editor_property("srgb", False)
    eal.save_asset(f"{TEX}/{nombre}")
    return tex


def nuevo(nombre):
    ruta = f"{MAT}/{nombre}"
    if eal.does_asset_exist(ruta):
        eal.delete_asset(ruta)
    return tools.create_asset(nombre, MAT, unreal.Material, unreal.MaterialFactoryNew())


def ex(m, clase, x, y):
    return mel.create_material_expression(m, clase, x, y)


def con(a, sa, b, sb):
    if not mel.connect_material_expressions(a, sa, b, sb):
        problemas.append(f"no conectó {a.get_name()}.{sa} -> {b.get_name()}.{sb}")


def esc(m, nombre, valor, x, y):
    e = ex(m, unreal.MaterialExpressionScalarParameter, x, y)
    e.set_editor_property("parameter_name", nombre)
    e.set_editor_property("default_value", valor)
    return e


def vec(m, nombre, valor, x, y):
    e = ex(m, unreal.MaterialExpressionVectorParameter, x, y)
    e.set_editor_property("parameter_name", nombre)
    e.set_editor_property("default_value", valor)
    return e


def custom(m, codigo, entradas, salida, x, y):
    c = ex(m, unreal.MaterialExpressionCustom, x, y)
    c.set_editor_property("code", codigo)
    c.set_editor_property("output_type", salida)
    lista = []
    for n in entradas:
        i = unreal.CustomInput()
        i.set_editor_property("input_name", n)
        lista.append(i)
    c.set_editor_property("inputs", lista)
    return c


RUIDO = r"""
float m = sin(P.x*0.0021+1.7)*cos(P.y*0.0017+0.3) + 0.6*sin((P.x+P.z)*0.0049+0.5) + 0.4*cos((P.y-P.z)*0.0093);
m = saturate(m*0.25+0.5);
float m2 = saturate(0.5 + 0.5*sin(P.x*0.013+P.y*0.011)*cos(P.z*0.017-P.x*0.007));
float bajo = saturate(1.0 - (frac(P.z/400.0)*400.0)/90.0);
float hum = Humedad * bajo * smoothstep(0.3, 0.7, m);
"""
COD_COLOR = RUIDO + r"""
float3 c = Color * lerp(1.0 - Variacion, 1.0 + Variacion*0.6, m);
float arriba = saturate((N.z - 0.25) * 2.0);
float musgo = Musgo * saturate(arriba*0.6 + bajo*0.7) * smoothstep(0.35, 0.75, m2*0.6 + m*0.4);
c = lerp(c, ColorMusgo * (0.6 + 0.6*m2), musgo);
c *= 1.0 - 0.45*hum;
return c;
"""
COD_RUG = RUIDO + r"""
return lerp(Rug, 0.12, hum);
"""


def mundo_variado(tex_piedra):
    """Copia de M_Mundo (proyección de mundo) con variación macro, musgo y humedad."""
    m = nuevo("M_MundoVariado")
    escala = esc(m, "Escala", 250.0, -1400, 0)
    salidas = {}
    for i, (mapa, defecto, muestreo, fn) in enumerate((
            ("Color", tex_piedra.get("color"), unreal.MaterialSamplerType.SAMPLERTYPE_COLOR, "WorldAlignedTexture"),
            ("Normal", tex_piedra.get("normal"), unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL, "WorldAlignedNormal"),
            ("Arm", tex_piedra.get("arm"), unreal.MaterialSamplerType.SAMPLERTYPE_MASKS, "WorldAlignedTexture"))):
        o = ex(m, unreal.MaterialExpressionTextureObjectParameter, -1400, 150 + i * 220)
        o.set_editor_property("parameter_name", mapa)
        if defecto:
            o.set_editor_property("texture", defecto)
        o.set_editor_property("sampler_type", muestreo)
        f = ex(m, unreal.MaterialExpressionMaterialFunctionCall, -1050, 150 + i * 220)
        f.set_editor_property("material_function", unreal.load_asset(f"/Engine/Functions/Engine_MaterialFunctions01/Texturing/{fn}"))
        con(o, "", f, "TextureObject")
        con(escala, "", f, "TextureSize")
        salidas[mapa] = f
    tinte = vec(m, "Tinte", unreal.LinearColor(1, 1, 1, 1), -1050, -200)
    mult = ex(m, unreal.MaterialExpressionMultiply, -800, 0)
    con(salidas["Color"], "XYZ Texture", mult, "A")
    con(tinte, "", mult, "B")
    pos = ex(m, unreal.MaterialExpressionWorldPosition, -800, -400)
    nor = ex(m, unreal.MaterialExpressionVertexNormalWS, -800, -300)
    var, musgo, hum = esc(m, "Variacion", 0.0, -800, 700), esc(m, "Musgo", 0.0, -800, 800), esc(m, "Humedad", 0.0, -800, 900)
    cmus = vec(m, "ColorMusgo", unreal.LinearColor(0.10, 0.13, 0.06, 1), -800, 1000)
    c_col = custom(m, COD_COLOR, ["Color", "P", "N", "Variacion", "Musgo", "Humedad", "ColorMusgo"],
                   unreal.CustomMaterialOutputType.CMOT_FLOAT3, -400, 0)
    for src, nombre in ((mult, "Color"), (pos, "P"), (nor, "N"), (var, "Variacion"), (musgo, "Musgo"), (hum, "Humedad"), (cmus, "ColorMusgo")):
        con(src, "", c_col, nombre)
    mel.connect_material_property(c_col, "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(salidas["Normal"], "XYZ Texture", unreal.MaterialProperty.MP_NORMAL)
    mascara = {}
    for canal in "RGB":
        k = ex(m, unreal.MaterialExpressionComponentMask, -800, {"R": 300, "G": 400, "B": 500}[canal])
        for c in "RGBA":
            k.set_editor_property(c.lower(), c == canal)
        con(salidas["Arm"], "XYZ Texture", k, "")
        mascara[canal] = k
    mel.connect_material_property(mascara["R"], "", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
    mel.connect_material_property(mascara["B"], "", unreal.MaterialProperty.MP_METALLIC)
    c_rug = custom(m, COD_RUG, ["Rug", "P", "Humedad"], unreal.CustomMaterialOutputType.CMOT_FLOAT1, -400, 400)
    con(mascara["G"], "", c_rug, "Rug")
    con(pos, "", c_rug, "P")
    con(hum, "", c_rug, "Humedad")
    mel.connect_material_property(c_rug, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.recompile_material(m)
    eal.save_asset(f"{MAT}/M_MundoVariado")
    return m


def agua_maestro(normal):
    m = nuevo("M_AguaMaestro")
    pos = ex(m, unreal.MaterialExpressionWorldPosition, -1400, 0)
    rg = ex(m, unreal.MaterialExpressionComponentMask, -1200, 0)
    rg.set_editor_property("r", True)
    rg.set_editor_property("g", True)
    rg.set_editor_property("b", False)
    rg.set_editor_property("a", False)
    con(pos, "", rg, "")
    escala = esc(m, "Escala", 300.0, -1200, 150)
    uv = ex(m, unreal.MaterialExpressionDivide, -1000, 0)
    con(rg, "", uv, "A")
    con(escala, "", uv, "B")
    muestras = []
    for i, (vx, vy, mult) in enumerate(((0.012, 0.006, 1.0), (-0.007, 0.01, 1.37))):
        uvi = uv
        if mult != 1.0:
            k = ex(m, unreal.MaterialExpressionMultiply, -850, 200 * i)
            k.set_editor_property("const_b", mult)
            con(uv, "", k, "A")
            uvi = k
        p = ex(m, unreal.MaterialExpressionPanner, -650, 200 * i)
        vel = esc(m, f"Velocidad{i + 1}", 1.0, -850, 400 + 100 * i)
        p.set_editor_property("speed_x", vx)
        p.set_editor_property("speed_y", vy)
        con(uvi, "", p, "Coordinate")
        t = ex(m, unreal.MaterialExpressionMultiply, -800, 600 + 100 * i)
        tiempo = ex(m, unreal.MaterialExpressionTime, -1000, 600 + 100 * i)
        con(tiempo, "", t, "A")
        con(vel, "", t, "B")
        con(t, "", p, "Time")
        s = ex(m, unreal.MaterialExpressionTextureSampleParameter2D, -400, 200 * i)
        s.set_editor_property("parameter_name", f"Normal{i + 1}")
        s.set_editor_property("texture", normal)
        s.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
        con(p, "", s, "UVs")
        muestras.append(s)
    mezcla = ex(m, unreal.MaterialExpressionMaterialFunctionCall, -150, 100)
    mezcla.set_editor_property("material_function", unreal.load_asset("/Engine/Functions/Engine_MaterialFunctions02/Utility/BlendAngleCorrectedNormals"))
    con(muestras[0], "RGB", mezcla, "BaseNormal")
    con(muestras[1], "RGB", mezcla, "AdditionalNormal")
    plano = ex(m, unreal.MaterialExpressionMaterialFunctionCall, 50, 100)
    plano.set_editor_property("material_function", unreal.load_asset("/Engine/Functions/Engine_MaterialFunctions01/Texturing/FlattenNormal"))
    con(mezcla, "", plano, "Normal")
    con(esc(m, "Aplanar", 0.4, -150, 300), "", plano, "Flatness")
    mel.connect_material_property(plano, "", unreal.MaterialProperty.MP_NORMAL)
    mel.connect_material_property(vec(m, "Color", unreal.LinearColor(0.008, 0.011, 0.014, 1), -150, -250), "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(esc(m, "Rugosidad", 0.04, -150, -150), "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.connect_material_property(esc(m, "Especular", 0.9, -150, -100), "", unreal.MaterialProperty.MP_SPECULAR)
    mel.recompile_material(m)
    eal.save_asset(f"{MAT}/M_AguaMaestro")
    return m


def instancia(nombre, padre, escalares=None, vectores=None, texturas=None):
    ruta = f"{MAT}/{nombre}"
    mi = unreal.load_asset(ruta) if eal.does_asset_exist(ruta) else None
    if mi is None or not isinstance(mi, unreal.MaterialInstanceConstant):
        if mi is not None:
            eal.delete_asset(ruta)
        mi = tools.create_asset(nombre, MAT, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mi.set_editor_property("parent", padre)
    for k, val in (escalares or {}).items():
        mel.set_material_instance_scalar_parameter_value(mi, k, val)
    for k, val in (vectores or {}).items():
        mel.set_material_instance_vector_parameter_value(mi, k, val)
    for k, val in (texturas or {}).items():
        mel.set_material_instance_texture_parameter_value(mi, k, val)
    eal.save_asset(ruta)
    return mi


def main():
    agua_n = importar_tex("T_Agua_N", "normal")
    ox = {"color": importar_tex("T_Oxido_C", "color"), "normal": importar_tex("T_Oxido_N", "normal"), "arm": importar_tex("T_Oxido_ARM", "masks")}
    mundo = unreal.load_asset(f"{MAT}/M_Mundo")
    # Texturas por defecto del maestro nuevo: las de piedra que ya usa M_Mundo
    defecto = {}
    for k, p in (("color", "Color"), ("normal", "Normal"), ("arm", "Arm")):
        t = mel.get_material_default_texture_parameter_value(mundo, p) if mundo else None
        if t:
            defecto[k] = t
    variado = mundo_variado(defecto)
    # Instancias de piedra: mismo aspecto base, ahora con variación por zona
    valores = {
        "M_Piedra": (0.35, 0.45, 0.5),
        "M_Piedra_DosCaras": (0.35, 0.45, 0.5),
        "M_Piso": (0.3, 0.15, 0.8),
        "M_Piedra_Negra": (0.2, 0.2, 0.4),
        "M_Roca": (0.3, 0.6, 0.0),
        "M_Ladrillo_Quemado": (0.45, 0.0, 0.1),
    }
    for nombre, (va, mu, hu) in valores.items():
        mi = unreal.load_asset(f"{MAT}/{nombre}")
        if not isinstance(mi, unreal.MaterialInstanceConstant):
            log(f"{nombre}: no es instancia, se deja")
            continue
        padre = mi.get_editor_property("parent")
        if padre and padre.get_name() not in ("M_Mundo", "M_MundoVariado"):
            log(f"{nombre}: padre {padre.get_name()}, se deja")
            continue
        mi.set_editor_property("parent", variado)
        mel.set_material_instance_scalar_parameter_value(mi, "Variacion", va)
        mel.set_material_instance_scalar_parameter_value(mi, "Musgo", mu)
        mel.set_material_instance_scalar_parameter_value(mi, "Humedad", hu)
        eal.save_asset(f"{MAT}/{nombre}")
        log(f"{nombre}: variación {va}, musgo {mu}, humedad {hu}")
    agua = agua_maestro(agua_n)
    instancia("M_Agua_Quieta", agua, {"Velocidad1": 0.25, "Velocidad2": 0.2, "Escala": 260.0, "Aplanar": 0.55})
    instancia("M_Agua_Corriente", agua, {"Velocidad1": 4.0, "Velocidad2": 2.5, "Escala": 380.0, "Aplanar": 0.2, "Rugosidad": 0.08},
              {"Color": unreal.LinearColor(0.012, 0.018, 0.02, 1)})
    instancia("M_Hierro", variado, {"Escala": 70.0, "Variacion": 0.2, "Musgo": 0.0, "Humedad": 0.0},
              texturas={"Color": ox["color"], "Normal": ox["normal"], "Arm": ox["arm"]})
    liso = unreal.load_asset(f"{MAT}/M_Liso")
    instancia("M_Runa", liso, {"Rugosidad": 0.4, "Fuerza": 6.0},
              {"Color": unreal.LinearColor(0.05, 0.03, 0.08, 1), "Emisivo": unreal.LinearColor(0.55, 0.25, 1.0, 1)})
    log(f"materiales D OK; problemas: {problemas}")


main()
