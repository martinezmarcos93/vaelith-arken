"""Deja todas las mallas de /Game/Vaelith con un solo LOD y sin Nanite (el proyecto no usa Nanite)."""
import unreal
sml = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
eal = unreal.EditorAssetLibrary
n = 0
for ruta in eal.list_assets("/Game/Vaelith", recursive=True):
    m = unreal.load_asset(ruta)
    if not isinstance(m, unreal.StaticMesh):
        continue
    lods = sml.get_lod_count(m)
    nan = m.get_editor_property("nanite_settings")
    antes = nan.get_editor_property("enabled")
    if antes:
        nan.set_editor_property("enabled", False)
        m.set_editor_property("nanite_settings", nan)
    if lods > 1:
        sml.remove_lods(m)
    if lods > 1 or antes:
        unreal.log(f"[vaelith] {m.get_name()}: lods={lods} nanite={antes} -> corregido")
        eal.save_loaded_asset(m)
        n += 1
unreal.log(f"[vaelith] arreglar_mallas OK ({n} corregidas)")
