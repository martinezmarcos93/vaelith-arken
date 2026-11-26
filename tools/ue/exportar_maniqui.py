"""Exporta el esqueleto del maniquí (SKM_Manny_Simple) a FBX para riggear mallas nuevas en Blender."""
import os
import unreal

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dest = os.path.join(RAIZ, "assets_fuente", "_ref", "SKM_Manny_Simple.fbx")
os.makedirs(os.path.dirname(dest), exist_ok=True)
t = unreal.AssetExportTask()
t.object = unreal.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple")
t.filename = dest
t.automated = True
t.replace_identical = True
t.prompt = False
t.exporter = unreal.SkeletalMeshExporterFBX()
ok = unreal.Exporter.run_asset_export_task(t)
unreal.log(f"[vaelith] exportar maniquí: {ok} -> {dest} ({os.path.getsize(dest) if os.path.exists(dest) else 0} bytes)")
