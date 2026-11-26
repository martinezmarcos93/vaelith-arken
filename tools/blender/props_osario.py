"""Utilería procedural de las catacumbas de Vaelith Arken."""
import math
import os
import random
import sys

import bpy

SEMILLA = 2402
random.seed(SEMILLA)


def limpiar():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material(slot):
    m = bpy.data.materials.get(slot) or bpy.data.materials.new(slot)
    return m


def cubo(nombre, mat, loc, escala, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.object
    ob.name = nombre
    ob.dimensions = escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(mat)
    if bevel:
        mod = ob.modifiers.new("Bisel", "BEVEL")
        mod.width, mod.segments = bevel, 1
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return ob


def cilindro(nombre, mat, loc, radio, alto, vertices=12, radio2=None, rot=None):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radio,
        radius2=radio if radio2 is None else radio2, depth=alto, location=loc)
    ob = bpy.context.object
    ob.name = nombre
    if rot:
        ob.rotation_euler = rot
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    ob.data.materials.append(mat)
    return ob


def esfera(nombre, mat, loc, escala, segmentos=12, anillos=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segmentos, ring_count=anillos, radius=1, location=loc)
    ob = bpy.context.object
    ob.name = nombre
    ob.scale = escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(mat)
    return ob


def unir(nombre, piezas):
    bpy.ops.object.select_all(action="DESELECT")
    for ob in piezas:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = piezas[0]
    bpy.ops.object.join()
    ob = bpy.context.object
    ob.name = nombre
    # Origen en el pivote de base/anclaje; geometría ya está posicionada en local.
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")
    return ob


def construir(nombre, piezas):
    ob = unir(nombre, piezas)
    ob.data.calc_loop_triangles()
    tris = len(ob.data.loop_triangles)
    slots = ",".join(sorted({m.name for m in ob.data.materials if m}))
    return ob, tris, slots


def exportar(ob, carpeta):
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.export_scene.fbx(filepath=os.path.join(carpeta, ob.name + ".fbx"),
        use_selection=True, apply_unit_scale=True, axis_forward="-Y", axis_up="Z",
        bake_space_transform=True, add_leaf_bones=False, path_mode="STRIP")


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    carpeta = os.path.abspath(argv[0] if argv else "out/props_osario")
    os.makedirs(carpeta, exist_ok=True)
    limpiar()
    piedra, hueso, metal = material("M_Piedra"), material("M_Hueso"), material("M_Metal")
    madera, tela, oro, em = (material(n) for n in ("M_Madera", "M_Tela", "M_Oro", "M_Emisivo"))
    informes = []

    p = [cubo("base", piedra, (0, 0, .08), (2.2, .9, .16), .04),
         cubo("caja", piedra, (0, 0, .49), (2.08, .78, .66), .04),
         cubo("moldura", piedra, (0, 0, .84), (2.18, .88, .08), .025)]
    informes.append(construir("SM_Sarcofago", p))
    p = [cubo("tapa", piedra, (0, 0, .1), (2.2, .9, .2), .06),
         esfera("yacente", piedra, (0, 0, .28), (1.35, .27, .12)),
         esfera("cabeza", piedra, (0, -.02, .36), (.18, .19, .12))]
    p += [cubo("brazo", piedra, (x, 0, .32), (.78, .07, .07), .025) for x in (-.26, .26)]
    p += [cubo("espada", piedra, (0, 0, .38), (.07, .76, .04), .015),
          cubo("guarda", piedra, (0, -.05, .38), (.34, .05, .05), .015)]
    informes.append(construir("SM_Sarcofago_Tapa", p))

    p = []
    for i in range(14):
        a = i * math.tau / 14
        largo = random.uniform(.48, .78)
        ob = cilindro("hueso_largo", hueso, (math.cos(a)*.2, math.sin(a)*.2, random.uniform(.18,.48)), .045, largo, 7,
                      rot=(random.uniform(-.5,.5), random.uniform(-.5,.5), a))
        p.append(ob)
    for i in range(3):
        x, y = random.uniform(-.3,.3), random.uniform(-.3,.3)
        p += [esfera("craneo", hueso, (x,y,.35+i*.06), (.13,.105,.1), 10, 6),
              cubo("mandibula", hueso, (x,y-.07,.3+i*.06), (.14,.09,.05))]
    informes.append(construir("SM_Pila_Huesos", p))
    p = [esfera("boveda", hueso, (0,0,.14), (.11,.09,.08), 12, 8),
         cubo("maxilar", hueso, (0,-.04,.055), (.13,.08,.05)),
         cubo("nasal", hueso, (0,-.088,.14), (.035,.025,.05))]
    for x in (-.045,.045):
        p.append(cubo("orbita", hueso, (x,-.08,.16), (.045,.025,.035)))
    informes.append(construir("SM_Craneo", p))

    p = [cilindro("cuerpo", metal, (0,0,.22), .23,.38,12,.17),
         cilindro("cuello", metal,(0,0,.43),.17,.08,12,.18),
         cilindro("tapa", metal,(0,0,.49),.2,.08,12,.12)]
    informes.append(construir("SM_Urna", p))

    p = [cubo("plataforma", piedra,(0,0,.12),(1.6,.8,.24),.04),
         cubo("mesa", piedra,(0,0,.72),(1.48,.68,.12),.025),
         cubo("soporte", piedra,(0,.3,.72),(.55,.3,.76),.04),
         cilindro("disco", piedra,(0,.3,1.08),.45,.08,32,rot=(math.pi/2,0,0)),
         cilindro("nucleo", em,(0,.245,1.08),.055,.025,12,rot=(math.pi/2,0,0))]
    # Espiral doble aproximada con segmentos tubulares sobre el disco vertical.
    for signo in (-1,1):
        pts=[]
        for j in range(18):
            t=j/17
            a=signo*t*math.tau*1.5
            r=.035+.16*t
            pts.append((signo*.08+r*math.cos(a),.235,1.08+r*math.sin(a)))
        for a,b in zip(pts,pts[1:]):
            v=(b[0]-a[0],0,b[2]-a[2]); length=math.sqrt(v[0]**2+v[2]**2)
            p.append(cilindro("espiral",em,((a[0]+b[0])/2,.235,(a[2]+b[2])/2),.012,length,6,rot=(0,math.atan2(v[0],v[2]),0)))
    p += [cubo("ribete",oro,(0,-.405,.72),(1.5,.025,.035)), cubo("ribete",oro,(0,-.405,.1),(1.55,.025,.035))]
    informes.append(construir("SM_Altar_Pharasma", p))

    p = [cubo("placa",metal,(0,.04,.95),(.28,.1,.32),.035),
         cilindro("brazo",metal,(0,.31,.91),.045,.52,8,rot=(math.pi/2,0,0)),
         cilindro("mango",madera,(0,.54,.98),.045,.42,8,rot=(0,math.pi/2,0)),
         esfera("llama",em,(0,.54,1.24),(.07,.07,.15),8,6)]
    informes.append(construir("SM_Soporte_Antorcha",p))

    p=[cilindro("argolla",metal,(0,0,2.02),.12,.045,12,rot=(math.pi/2,0,0))]
    for i in range(12):
        z=1.9-i*.15
        p.append(cilindro("eslabon",metal,(0,0,z),.055,.16,8,rot=(math.pi/2 if i%2 else 0,0,0)))
    p += [cubo("grillete",metal,(0,0,.08),(.22,.055,.12)),
          cilindro("pasador",metal,(0,0,.08),.035,.26,8,rot=(math.pi/2,0,0))]
    informes.append(construir("SM_Cadena_Ancla",p))

    p=[cilindro("asta",madera,(0,0,1.5),.045,3,8)]
    # Paño ondulado con borde inferior dentado, representado por paños triangulados.
    verts=[(-.55,0,2.8),(.55,0,2.8),(-.55,0,1.35),(-.3,0,1.55),(0,0,1.3),(.28,0,1.48),(.55,0,1.25)]
    faces=[(0,1,3,2),(1,5,4,3),(1,6,5)]
    me=bpy.data.meshes.new("paño"); me.from_pydata(verts,[],faces); me.materials.append(tela)
    ob=bpy.data.objects.new("paño",me); bpy.context.collection.objects.link(ob); p.append(ob)
    # Sol negro de ocho rayos (material tela asignable en Unreal).
    p.append(cilindro("sol",tela,(0,-.008,2.3),.16,.018,8,rot=(math.pi/2,0,0)))
    for i in range(8):
        a=i*math.tau/8
        p.append(cubo("rayo",tela,(math.cos(a)*.23,-.012,2.3+math.sin(a)*.23),(.15,.018,.035),.005))
    informes.append(construir("SM_Estandarte_Roto",p))

    p=[cilindro("pie",metal,(0,0,.08),.28,.16,8,.2),
       cilindro("fuste",metal,(0,0,.8),.055,1.3,8),
       cilindro("aro",metal,(0,0,1.5),.12,.08,8)]
    for i in range(5):
        a=i*math.tau/5
        x,y=math.cos(a)*.25,math.sin(a)*.25
        p += [cilindro("vela",material("M_Emisivo") if False else metal,(x,y,1.48),.045,.22,8),
              esfera("llama",em,(x,y,1.63),(.045,.045,.09),8,6)]
    informes.append(construir("SM_Candelabro_Suelo",p))

    p=[cubo("caja",madera,(0,0,.28),(.9,.5,.48),.04),
       cubo("tapa",madera,(0,0,.55),(.94,.54,.12),.04),
       cubo("banda",metal,(0,-.26,.3),(.08,.025,.5)),cubo("cierre",metal,(0,-.28,.48),(.12,.035,.13))]
    for x in (-.32,.32): p.append(cubo("herrajes",metal,(x,-.255,.3),(.035,.03,.5)))
    informes.append(construir("SM_Cofre",p))

    p=[cubo("losa",piedra,(0,0,.6),(1.2,.1,1.2),.04),
       cubo("rehundido",piedra,(0,-.052,.6),(.82,.018,.72),.015),
       cubo("borde_sup",piedra,(0,-.06,1.12),(.88,.035,.035)),
       cubo("borde_inf",piedra,(0,-.06,.08),(.88,.035,.035)),
       cubo("borde_izq",piedra,(-.425,-.06,.6),(.035,.035,1.08)),
       cubo("borde_der",piedra,(.425,-.06,.6),(.035,.035,1.08))]
    informes.append(construir("SM_Losa_Nombre",p))

    lineas=[]
    for ob,tris,slots in informes:
        exportar(ob,carpeta)
        d=ob.dimensions
        lineas.append(f"{ob.name}\t{tris}\t{d.x:.2f}x{d.y:.2f}x{d.z:.2f} m\t{slots}")
    with open(os.path.join(carpeta,"INFORME.txt"),"w",encoding="utf-8") as f:
        f.write("\n".join(lineas)+"\n")
    print("KIT OK\n"+"\n".join(lineas))


if __name__ == "__main__":
    main()
