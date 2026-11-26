import bpy, sys, os, json
arch = sys.argv[sys.argv.index("--")+1:]
out = []
for f in arch:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ext = os.path.splitext(f)[1].lower()
    try:
        if ext == ".blend":
            bpy.ops.wm.open_mainfile(filepath=f, load_ui=False, use_scripts=False)
        elif ext == ".fbx": bpy.ops.import_scene.fbx(filepath=f)
        elif ext in (".glb", ".gltf"): bpy.ops.import_scene.gltf(filepath=f)
        elif ext == ".obj": bpy.ops.wm.obj_import(filepath=f)
    except Exception as e:
        out.append({"f": f, "error": str(e)[:200]}); continue
    tris = 0; mins=[1e9]*3; maxs=[-1e9]*3; meshes=0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            meshes += 1
            tris += sum(len(p.vertices)-2 for p in o.data.polygons)
            for c in o.bound_box:
                w = o.matrix_world @ __import__("mathutils").Vector(c)
                for i in range(3): mins[i]=min(mins[i],w[i]); maxs[i]=max(maxs[i],w[i])
    arm = [o.name for o in bpy.context.scene.objects if o.type=="ARMATURE"]
    bones = sum(len(o.data.bones) for o in bpy.context.scene.objects if o.type=="ARMATURE")
    out.append({"f": os.path.basename(f), "tris": tris, "meshes": meshes,
        "dim_m": [round(maxs[i]-mins[i],2) for i in range(3)] if meshes else None,
        "mats": len(bpy.data.materials), "imgs": len(bpy.data.images),
        "arm": len(arm), "bones": bones, "anims": [a.name for a in bpy.data.actions][:12]})
with open(os.environ["SALIDA"], "w", encoding="utf-8") as fh: json.dump(out, fh, ensure_ascii=False, indent=0)
