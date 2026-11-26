"""Ajustes finos de parámetros de materiales ya creados (sin recrearlos)."""
import unreal
mel = unreal.MaterialEditingLibrary
def esc(mi, k, v):
    m = unreal.load_asset(f"/Game/Vaelith/Materiales/{mi}")
    mel.set_material_instance_scalar_parameter_value(m, k, v)
    unreal.EditorAssetLibrary.save_loaded_asset(m)
esc("M_Emisivo", "Fuerza", 5.0)
# La Sombra: silueta mate, sin reflejos, con borde violeta.
esc("M_Sombra", "Metalico", 0.0)
esc("M_Sombra", "Rugosidad", 0.95)
esc("M_Sombra", "Borde", 6.0)
unreal.log("[vaelith] ajustar_materiales OK")

# Piedra de doble cara para los muros de la torre (su malla exporta con caras invertidas).
tools = unreal.AssetToolsHelpers.get_asset_tools()
ruta = "/Game/Vaelith/Materiales/M_Piedra_DosCaras"
if not unreal.EditorAssetLibrary.does_asset_exist(ruta):
    mi = tools.create_asset("M_Piedra_DosCaras", "/Game/Vaelith/Materiales", unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    base = unreal.load_asset("/Game/Vaelith/Materiales/M_Piedra")
    mel.set_material_instance_parent(mi, base.get_editor_property("parent"))
    for k in ("Color", "Normal", "Arm"):
        mel.set_material_instance_texture_parameter_value(mi, k, mel.get_material_instance_texture_parameter_value(base, k))
    mel.set_material_instance_vector_parameter_value(mi, "Tinte", mel.get_material_instance_vector_parameter_value(base, "Tinte"))
    mel.set_material_instance_scalar_parameter_value(mi, "Escala", 250.0)
    ov = mi.get_editor_property("base_property_overrides")
    ov.set_editor_property("override_two_sided", True)
    ov.set_editor_property("two_sided", True)
    mi.set_editor_property("base_property_overrides", ov)
    mel.update_material_instance(mi)
    unreal.EditorAssetLibrary.save_loaded_asset(mi)
    unreal.log("[vaelith] M_Piedra_DosCaras creado")

# Agua quieta del espejo: casi negra, muy lisa (refleja con SSR).
if not unreal.EditorAssetLibrary.does_asset_exist("/Game/Vaelith/Materiales/M_Agua"):
    agua = tools.create_asset("M_Agua", "/Game/Vaelith/Materiales", unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(agua, unreal.load_asset("/Game/Vaelith/Materiales/M_Liso"))
    mel.set_material_instance_vector_parameter_value(agua, "Color", unreal.LinearColor(0.01, 0.015, 0.025, 1))
    mel.set_material_instance_scalar_parameter_value(agua, "Rugosidad", 0.03)
    mel.set_material_instance_scalar_parameter_value(agua, "Metalico", 0.0)
    unreal.EditorAssetLibrary.save_loaded_asset(agua)
    unreal.log("[vaelith] M_Agua creado")
