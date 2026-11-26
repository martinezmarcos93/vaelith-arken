"""Armas de Vaelith y módulos de la torre derruida."""
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Vector

SEMILLA = 3003
random.seed(SEMILLA)


def limpiar():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material(nombre):
    m = bpy.data.materials.new(nombre)
    m.diffuse_color = (0.22, 0.24, 0.27, 1)
    return m


def cubo(bm, centro, escala, mat):
    tmp = bmesh.new()
    bmesh.ops.create_cube(tmp, size=1)
    for v in tmp.verts:
        v.co = Vector(centro) + Vector((v.co.x * escala[0], v.co.y * escala[1], v.co.z * escala[2]))
    bm.from_mesh(_mesh_temporal(tmp, mat))
    tmp.free()


def _mesh_temporal(bm, mat):
    me = bpy.data.meshes.new("_temporal")
    bm.to_mesh(me)
    me.materials.append(mat)
    return me


def caja(bm, centro, escala, mat, bisel=0.025):
    tmp = bmesh.new()
    bmesh.ops.create_cube(tmp, size=1)
    for v in tmp.verts:
        v.co = Vector(centro) + Vector((v.co.x * escala[0], v.co.y * escala[1], v.co.z * escala[2]))
    bmesh.ops.bevel(tmp, geom=list(tmp.edges), offset=bisel, segments=1, affect="EDGES")
    me = bpy.data.meshes.new("_pieza")
    tmp.to_mesh(me)
    tmp.free()
    me.materials.append(mat)
    bm.from_mesh(me)
    bpy.data.meshes.remove(me)


def cilindro(bm, centro, radio, profundidad, mat, lados=12, eje="Z", radio2=None, indice=0):
    anteriores = set(bm.faces)
    tmp = bmesh.new()
    bmesh.ops.create_cone(tmp, cap_ends=True, segments=lados, radius1=radio,
                          radius2=radio if radio2 is None else radio2, depth=profundidad)
    if eje == "Z":
        bmesh.ops.translate(tmp, verts=tmp.verts, vec=(0, 0, centro[2]))
        bmesh.ops.translate(tmp, verts=tmp.verts, vec=(centro[0], centro[1], 0))
    elif eje == "Y":
        bmesh.ops.rotate(tmp, verts=tmp.verts, cent=(0, 0, 0), matrix=__import__('mathutils').Matrix.Rotation(math.pi / 2, 4, 'X'))
        bmesh.ops.translate(tmp, verts=tmp.verts, vec=centro)
    me = bpy.data.meshes.new("_pieza")
    tmp.to_mesh(me)
    tmp.free()
    me.materials.append(mat)
    bm.from_mesh(me)
    bpy.data.meshes.remove(me)
    for f in set(bm.faces) - anteriores:
        f.material_index = indice


def cinta_espiral(bm, centro, radio, y, mat, indice=0, vueltas=1.35):
    # Tubo poligonal en el plano XZ, prominente en la cara del escudo.
    puntos = []
    for i in range(49):
        t = i / 48
        a = t * vueltas * math.tau
        r = 0.012 + radio * t
        puntos.append(Vector((centro[0] + math.cos(a) * r, y, centro[1] + math.sin(a) * r)))
    rings = []
    for i, p in enumerate(puntos):
        prev = puntos[max(0, i - 1)]
        nxt = puntos[min(len(puntos) - 1, i + 1)]
        tangent = (nxt - prev).normalized()
        side = Vector((-tangent.z, 0, tangent.x)).normalized()
        ring = []
        for j in range(6):
            a = j * math.tau / 6
            ring.append(bm.verts.new(p + 0.012 * (math.cos(a) * side + Vector((0, math.sin(a), 0)))))
        rings.append(ring)
    for r1, r2 in zip(rings, rings[1:]):
        for j in range(6):
            f = bm.faces.new((r1[j], r1[(j + 1) % 6], r2[(j + 1) % 6], r2[j]))
            f.material_index = indice


def mesh_obj(nombre, bm, mats):
    # Normales hacia afuera en cada bloque (el orden de vértices no era consistente).
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.normal_update()
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    for mat in mats:
        me.materials.append(mat)
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    # Reasignar por material de origen cuando se ensamblan varios componentes.
    for p in me.polygons:
        p.use_smooth = False
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")
    return ob


def asignar(bm, material_index):
    for f in bm.faces:
        f.material_index = material_index


def componente_caja(bm, centro, escala, mat_idx, mats, bisel=0.02):
    anteriores = set(bm.faces)
    caja(bm, centro, escala, mats[mat_idx], bisel)
    for f in set(bm.faces) - anteriores:
        f.material_index = mat_idx


def arma_espada(m):
    bm = bmesh.new()
    # Empuñadura centrada en el pivote; hoja extendida hacia +Z.
    cilindro(bm, (0, 0, -0.01), 0.045, 0.30, m[2], 10, indice=2)
    for i in range(9):
        a = i * math.tau / 9
        cilindro(bm, (0.048 * math.cos(a), 0.048 * math.sin(a), -0.02), 0.008, 0.28, m[3], 6, indice=2)
    # Guarda recta con extremos espiralados.
    componente_caja(bm, (0, 0, 0.16), (0.40, 0.075, 0.055), 0, m)
    for s in (-1, 1):
        cilindro(bm, (s * 0.215, 0, 0.16), 0.045, 0.07, m[0], 10, radio2=0.018)
    cilindro(bm, (0, 0, -0.20), 0.09, 0.045, m[1], 16, indice=1)
    # Hoja facetada, sección con canal longitudinal central.
    contorno = [(-.09, .18), (-.105, .30), (-.09, .82), (0, .90), (.09, .82), (.105, .30), (.09, .18)]
    ys = [-.022, .022]
    verts = []
    for y in ys:
        verts.append([bm.verts.new((x, y, z)) for x, z in contorno])
    for i in range(len(contorno)):
        j = (i + 1) % len(contorno)
        f = bm.faces.new((verts[0][i], verts[0][j], verts[1][j], verts[1][i]))
        f.material_index = 0
    bm.faces.new(tuple(verts[0])).material_index = 0
    bm.faces.new(tuple(reversed(verts[1]))).material_index = 0
    mesh = mesh_obj("SM_Espada_Larga", bm, m)
    return mesh


def arma_daga(m):
    bm = bmesh.new()
    cilindro(bm, (0, 0, -0.025), .027, .17, m[0], 10)
    cilindro(bm, (0, 0, -.125), .048, .035, m[1], 12, indice=1)
    componente_caja(bm, (0, 0, .065), (.16, .045, .025), 0, m)
    # Hoja sencilla facetada con punta.
    pts = [(-.045, .07), (-.052, .12), (0, .31), (.052, .12), (.045, .07)]
    a = [bm.verts.new((x, -.014, z)) for x, z in pts]
    b = [bm.verts.new((x, .014, z)) for x, z in pts]
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(tuple(a)); bm.faces.new(tuple(reversed(b)))
    return mesh_obj("SM_Daga_Pharasma", bm, m)


def escudo(m):
    bm = bmesh.new()
    # Heater con punta inferior, cara frontal en +Y y respaldo en el origen.
    perfil = [(-.325, .45), (.325, .45), (.29, .04), (.20, -.27), (0, -.45), (-.20, -.27), (-.29, .04)]
    frente = [bm.verts.new((x, .03, z)) for x, z in perfil]
    atras = [bm.verts.new((x, -.03, z)) for x, z in perfil]
    bm.faces.new(tuple(frente)).material_index = 0
    bm.faces.new(tuple(reversed(atras))).material_index = 0
    for i in range(len(perfil)):
        j = (i + 1) % len(perfil)
        bm.faces.new((frente[i], atras[i], atras[j], frente[j])).material_index = 1
    cilindro(bm, (0, .05, .04), .095, .055, m[1], 12, eje="Y", indice=1)
    # Doble espiral de Pharasma en relieve, separadas sobre la cara.
    cinta_espiral(bm, (-.09, .13), .105, .077, m[2], indice=2)
    cinta_espiral(bm, (.09, -.05), .105, .077, m[2], indice=2, vueltas=-1.35)
    return mesh_obj("SM_Escudo_Pharasma", bm, m)


def muro(nombre, m, roto=False):
    bm = bmesh.new()
    n = 16
    rin, rout = 5, 6
    for row in range(3 if not roto else 2):
        for i in range(n):
            a0 = math.radians(i * 45 / n)
            a1 = math.radians((i + 1) * 45 / n)
            z0 = row * 2
            z1 = z0 + 2
            if roto:
                z1 = min(z1, random.uniform(1.5, 4.0))
                if z1 <= z0 + .15:
                    continue
            vs = [bm.verts.new((r * math.cos(a), r * math.sin(a), z)) for r, a, z in
                  ((rin,a0,z0),(rin,a1,z0),(rout,a1,z0),(rout,a0,z0),
                   (rin,a0,z1),(rin,a1,z1),(rout,a1,z1),(rout,a0,z1))]
            faces = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
            for face in faces:
                bm.faces.new(tuple(vs[j] for j in face))
            # Juntas alternadas, juntas de bloque con bisel tosco.
    # Geometría en un único objeto; sillería sugerida con bandas y juntas hundidas.
    if roto:
        for _ in range(7):
            a = math.radians(random.uniform(0, 45))
            r = random.uniform(5.3, 6.5)
            caja(bm, (r*math.cos(a), r*math.sin(a), random.uniform(.15, 1.0)),
                 (random.uniform(.35,.8), .45, .35), m[0], .04)
    return mesh_obj(nombre, bm, [m[0]])


def escalon(m):
    bm = bmesh.new()
    # Cuña tangencial al muro: anillo radial de 5 a 6.6 m.
    a0, a1 = 0, math.radians(16)
    verts = []
    for z in (0, .25):
        verts.append([bm.verts.new((r*math.cos(a), r*math.sin(a), z)) for r,a in ((5,a0),(6.6,a0),(6.6,a1),(5,a1))])
    bm.faces.new(tuple(verts[0])); bm.faces.new(tuple(reversed(verts[1])))
    for i in range(4):
        bm.faces.new((verts[0][i], verts[0][(i+1)%4], verts[1][(i+1)%4], verts[1][i]))
    return mesh_obj("SM_Torre_Escalon_Caracol", bm, [m[0]])


def piso(m):
    bm = bmesh.new()
    # Tablas radiales en dos mitades; se deja una abertura amplia en el cuadrante +X.
    for i in range(28):
        a = math.tau * i / 28
        if -0.55 < ((a + math.pi) % math.tau - math.pi) < 0.95:
            continue
        antes = set(bm.verts)
        caja(bm, (0, 0, 0), (5.0, .36, .14), m[0], .025)
        # Cada tabla va del centro al borde, y el conjunto queda dentro de radio 5 m.
        for v in set(bm.verts) - antes:
            x, y = v.co.x, v.co.y
            v.co.x = x*math.cos(a) - y*math.sin(a) + 2.5*math.cos(a)
            v.co.y = x*math.sin(a) + y*math.cos(a) + 2.5*math.sin(a)
    return mesh_obj("SM_Torre_Piso_Roto", bm, [m[0]])


def simple_pieza(nombre, m, tipo):
    bm = bmesh.new()
    if tipo == "almena":
        caja(bm, (0,0,.6), (.8,1,1.2), m[0], .04)
    elif tipo == "bloque":
        caja(bm, (0,0,.3), (1,.6,.5), m[0], .12)
    elif tipo == "lapida":
        caja(bm, (0,0,.55), (.6,.15,1.1), m[0], .045)
        for v in bm.verts:
            v.co.y += max(0, v.co.z) * .16
    else:
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.5)
        for v in bm.verts:
            f = random.uniform(.83, 1.08)
            v.co.x *= f; v.co.y *= random.uniform(.82,1.08); v.co.z *= random.uniform(.85,1.1)
        bm.normal_update()
        return mesh_obj(nombre, bm, [m[0]])
    return mesh_obj(nombre, bm, [m[0]])


def exportar(ob, carpeta):
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.export_scene.fbx(filepath=os.path.join(carpeta, ob.name + ".fbx"), use_selection=True,
        apply_unit_scale=True, apply_scale_options="FBX_SCALE_UNITS", bake_space_transform=True,
        mesh_smooth_type="FACE", add_leaf_bones=False, path_mode="STRIP", axis_forward="-Y", axis_up="Z")


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    carpeta = os.path.abspath(argv[0] if argv else "out/armas_torre")
    os.makedirs(carpeta, exist_ok=True)
    limpiar()
    mats = [material("M_Metal"), material("M_Oro"), material("M_Tela"), material("M_Madera"), material("M_Piedra")]
    piezas = [arma_espada([mats[0],mats[1],mats[2],mats[2]]), escudo([mats[3],mats[0],mats[1]]), arma_daga([mats[0],mats[1]])]
    piezas += [muro("SM_Torre_Muro_Segmento", [mats[4]]), muro("SM_Torre_Muro_Roto", [mats[4]], True),
               escalon([mats[4]]), piso([mats[3]]), simple_pieza("SM_Torre_Almena", [mats[4]], "almena"),
               simple_pieza("SM_Ruina_Bloque", [mats[4]], "bloque"), simple_pieza("SM_Lapida_Bosque", [mats[4]], "lapida"),
               simple_pieza("SM_Roca_Grande", [mats[4]], "roca")]
    informe = []
    for ob in piezas:
        exportar(ob, carpeta)
        # El oráculo consume este campo como conteo de triángulos.
        tris = sum(max(0, len(p.vertices) - 2) for p in ob.data.polygons)
        slots = ",".join(sorted({m.name for m in ob.data.materials}))
        d = ob.dimensions
        informe.append(f"{ob.name}\t{tris}\t{d.x:.2f}x{d.y:.2f}x{d.z:.2f} m\t{slots}")
    with open(os.path.join(carpeta, "INFORME.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(informe) + "\n")
    print("KIT OK\n" + "\n".join(informe))
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)


if __name__ == "__main__":
    main()
