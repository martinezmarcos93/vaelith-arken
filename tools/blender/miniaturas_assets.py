import bpy, sys, os, math, mathutils
args = sys.argv[sys.argv.index("--")+1:]
outdir = args[0]
for f in args[1:]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ext = os.path.splitext(f)[1].lower()
    try:
        if ext == ".blend": bpy.ops.wm.open_mainfile(filepath=f, load_ui=False, use_scripts=False)
        elif ext == ".fbx": bpy.ops.import_scene.fbx(filepath=f)
        elif ext == ".glb": bpy.ops.import_scene.gltf(filepath=f)
        elif ext == ".obj": bpy.ops.wm.obj_import(filepath=f)
    except Exception as e:
        print("ERR", f, e); continue
    sc = bpy.context.scene
    for o in list(sc.objects):
        if o.type in ("CAMERA", "LIGHT"): bpy.data.objects.remove(o)
    mins=[1e9]*3; maxs=[-1e9]*3
    for o in sc.objects:
        if o.type=="MESH":
            for c in o.bound_box:
                w=o.matrix_world@mathutils.Vector(c)
                for i in range(3): mins[i]=min(mins[i],w[i]); maxs[i]=max(maxs[i],w[i])
    if mins[0] > 1e8: continue
    ctr=mathutils.Vector([(a+b)/2 for a,b in zip(mins,maxs)]); r=max(b-a for a,b in zip(mins,maxs))
    cam=bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera=cam
    d=mathutils.Vector((1.0,-1.3,0.6)).normalized()*r*1.6
    cam.location=ctr+d; cam.rotation_euler=(ctr-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.clip_end = r*20
    sc.render.engine="BLENDER_WORKBENCH"; sc.display.shading.light="STUDIO"; sc.display.shading.color_type="TEXTURE"
    sc.display.shading.show_cavity=True
    sc.render.resolution_x=480; sc.render.resolution_y=360
    sc.render.filepath=os.path.join(outdir, os.path.splitext(os.path.basename(f))[0].replace(" ","_")+".png")
    bpy.ops.render.render(write_still=True)
