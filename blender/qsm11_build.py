"""Modelo 3D del Cummins QSM11 para Blender (generado por script).

Uso:
  python qsm11_build.py            (con el módulo bpy instalado: pip install bpy==4.5.4)
  blender -b -P qsm11_build.py     (con Blender instalado)

Salida: qsm11.blend y qsm11.glb en la carpeta blender/salida/.

Unidades: 1 unidad = 1 mm. Ejes: X longitudinal (frente = +X, cilindro 1),
Y lateral (+Y = lado bomba de combustible / admisión), Z vertical. Origen = eje del cigüeñal.

Fuentes (V = verificado, C = catálogo de partes, E = estimado):
  V  Calibre 125, carrera 147, orden 1-5-3-6-2-4, giro horario visto desde el frente (O&M pág. 361)
  V  Compresor de aire 217 x 142 x 216 (O&M pág. 368)
  C  Polea cigüeñal Ø190,7 y plano de correa a 140 mm del frente del bloque (cat. pág. 26)
  C  Polea alternador Ø76,2; polea ventilador Ø190 a 215,9 mm sobre el cigüeñal, 19 mm hacia la bomba (cat. págs. 33, 38)
  C  Carcasa de volante SAE 2; distancia motor de arranque 243,84 mm; agujero piloto Ø72 (cat. pág. 54)
  C  Brida del turbo: círculo de tornillos Ø129,06; turbo con wastegate (cat. pág. 99)
  C  Soporte delantero a 149 mm del frente del bloque, apoyo a 206 mm del eje (cat. pág. 37)
  C  Mangueras de admisión Ø102 (cat. pág. 59)
  E  Biela 260, paso entre cilindros 150, largo de bloque 946 (ficha técnica, sin verificar), resto de cotas
"""
import bpy, bmesh, math, os
from mathutils import Vector, Matrix

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'salida')
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- parámetros
BORE, STROKE = 125.0, 147.0
R = STROKE / 2
LROD = 260.0          # E
PITCH = 150.0         # E
CH = 80.0             # E altura de compresión
PH = 120.0            # E altura de pistón
DECK = R + LROD + CH + 1.5
HEAD_H = 135.0
HEAD_TOP = DECK + HEAD_H
RH_TOP = HEAD_TOP + 45     # carcasa de balancines
COVER_TOP = RH_TOP + 70
BLOCK_L = 946.0
FFOB = BLOCK_L / 2         # cara frontal del bloque
RFOB = -BLOCK_L / 2
BELT_X = FFOB + 140.0      # C
FIRING = [1, 5, 3, 6, 2, 4]
PHI = {c: k * 120 for k, c in enumerate(FIRING)}
XC = lambda c: (3.5 - c) * PITCH

# ---------------------------------------------------------------- escena
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001

COLL = {}
def coll(name):
    if name not in COLL:
        c = bpy.data.collections.new(name); scene.collection.children.link(c); COLL[name] = c
    return COLL[name]

MATS = {}
def mat(name, rgb, metal=0.0, rough=0.5):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    m.diffuse_color = (*rgb, 1)
    MATS[name] = m
    return m

PAINT = mat('pintura_motor', (0.16, 0.20, 0.24), 0.15, 0.55)
PAINT2 = mat('pintura_culata', (0.19, 0.23, 0.28), 0.2, 0.5)
ALU = mat('aluminio_fundido', (0.62, 0.64, 0.66), 0.8, 0.42)
STEEL = mat('acero', (0.75, 0.76, 0.78), 1.0, 0.22)
IRON = mat('hierro', (0.22, 0.23, 0.25), 0.7, 0.55)
BLACK = mat('negro', (0.04, 0.045, 0.05), 0.3, 0.5)
RUBBER = mat('goma', (0.02, 0.02, 0.02), 0.0, 0.85)
HOT = mat('fundicion_escape', (0.30, 0.22, 0.18), 0.75, 0.5)
BRASS = mat('laton', (0.78, 0.60, 0.30), 1.0, 0.3)
COPPER = mat('cobre', (0.72, 0.42, 0.22), 1.0, 0.32)
REDP = mat('rojo', (0.55, 0.08, 0.06), 0.2, 0.45)
LINER = mat('camisa', (0.45, 0.47, 0.50), 0.9, 0.3)

# ---------------------------------------------------------------- utilidades de malla
def new_obj(name, bm, material, collection, smooth_angle=None):
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    me.materials.append(material)
    o = bpy.data.objects.new(name, me)
    coll(collection).objects.link(o)
    if smooth_angle is not None:
        for p in me.polygons: p.use_smooth = True
        try:
            me.set_sharp_from_angle(angle=math.radians(smooth_angle))
        except Exception:
            pass
    return o

def m_rot(axis):
    if axis == 'X': return Matrix.Rotation(math.radians(90), 4, 'Y')
    if axis == 'Y': return Matrix.Rotation(math.radians(-90), 4, 'X')
    return Matrix.Identity(4)

def bm_box(bm, sx, sy, sz, loc=(0, 0, 0), rot=None):
    m = Matrix.Translation(loc) @ (rot or Matrix.Identity(4)) @ Matrix.Diagonal((sx, sy, sz, 1))
    bmesh.ops.create_cube(bm, size=1.0, matrix=m)

def bm_cyl(bm, r1, r2, h, loc=(0, 0, 0), axis='Z', seg=32, rot=None):
    m = Matrix.Translation(loc) @ (rot or Matrix.Identity(4)) @ m_rot(axis)
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r1, radius2=r2, depth=h, matrix=m)

def bm_tube(bm, ro, ri, h, loc=(0, 0, 0), axis='Z', seg=40):
    """Tubo con espesor (anillo extruido)."""
    m = Matrix.Translation(loc) @ m_rot(axis)
    vs = []
    for k, rr in enumerate((ro, ri)):
        for z in (-h / 2, h / 2):
            ring = [bm.verts.new(m @ Vector((math.cos(a) * rr, math.sin(a) * rr, z)))
                    for a in [i / seg * 2 * math.pi for i in range(seg)]]
            vs.append(ring)
    oB, oT, iB, iT = vs
    for i in range(seg):
        j = (i + 1) % seg
        bm.faces.new((oB[i], oB[j], oT[j], oT[i]))
        bm.faces.new((iB[j], iB[i], iT[i], iT[j]))
        bm.faces.new((oT[i], oT[j], iT[j], iT[i]))
        bm.faces.new((oB[j], oB[i], iB[i], iB[j]))

def bm_prism(bm, pts, depth, plane='YZ', offset=0.0, loc=(0, 0, 0)):
    """Extruye un polígono 2D. plane='YZ' extruye en X, 'XZ' en Y, 'XY' en Z."""
    def to3(u, v, w):
        if plane == 'YZ': return Vector((w, u, v))
        if plane == 'XZ': return Vector((u, w, v))
        return Vector((u, v, w))
    L = Vector(loc)
    a = [bm.verts.new(to3(u, v, offset - depth / 2) + L) for u, v in pts]
    b = [bm.verts.new(to3(u, v, offset + depth / 2) + L) for u, v in pts]
    n = len(pts)
    bm.faces.new(a[::-1]); bm.faces.new(b)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[i], a[j], b[j], b[i]))

def rrect(w, h, r, seg=4, cx=0, cy=0):
    pts = []
    for (qx, qy, a0) in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for i in range(seg + 1):
            a = math.radians(a0 + 90 * i / seg)
            pts.append((cx + qx + r * math.cos(a), cy + qy + r * math.sin(a)))
    return pts

def circle_pts(r, seg=32, cx=0, cy=0, a0=0, a1=360):
    full = abs(a1 - a0) >= 360
    n = seg if full else seg + 1
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / seg)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / seg))) for i in range(n)]

def gear_pts(r_root, r_tip, teeth):
    pts = []
    for i in range(teeth):
        a = 2 * math.pi * i / teeth; d = 2 * math.pi / teeth
        for f, rr in ((0.0, r_root), (0.18, r_tip), (0.5, r_tip), (0.68, r_root)):
            pts.append((rr * math.cos(a + f * d), rr * math.sin(a + f * d)))
    return pts

def catmull(points, n=12):
    P = [Vector(p) for p in points]
    if len(P) < 3: return P
    out = []
    P = [P[0] + (P[0] - P[1])] + P + [P[-1] + (P[-1] - P[-2])]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t))
    out.append(P[-2])
    return out

def bm_sweep(bm, path, radius, seg=20, caps=True, smooth=True):
    """Barrido de un círculo (radio fijo o lista) a lo largo de una polilínea, con transporte paralelo."""
    pts = catmull(path) if smooth else [Vector(p) for p in path]
    radii = radius if isinstance(radius, (list, tuple)) else [radius] * len(pts)
    if len(radii) != len(pts):
        radii = [radii[0] + (radii[-1] - radii[0]) * i / (len(pts) - 1) for i in range(len(pts))]
    t0 = (pts[1] - pts[0]).normalized()
    ref = Vector((0, 0, 1)) if abs(t0.z) < 0.9 else Vector((1, 0, 0))
    n = t0.cross(ref).normalized(); rings = []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        n = (n - t * n.dot(t)).normalized(); b = t.cross(n)
        rings.append([bm.verts.new(p + (n * math.cos(a) + b * math.sin(a)) * radii[i]) for a in [k / seg * 2 * math.pi for k in range(seg)]])
    for r0, r1 in zip(rings, rings[1:]):
        for k in range(seg):
            j = (k + 1) % seg
            bm.faces.new((r0[k], r0[j], r1[j], r1[k]))
    if caps:
        bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])

def bevel(o, w, segs=2, angle=40):
    md = o.modifiers.new('bevel', 'BEVEL'); md.width = w; md.segments = segs
    md.limit_method = 'ANGLE'; md.angle_limit = math.radians(angle)
    return o

def apply_mods(o):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
    o.modifiers.clear(); old = o.data; o.data = me; bpy.data.meshes.remove(old)

def boolean(o, cutters, op='DIFFERENCE'):
    for c in cutters:
        md = o.modifiers.new('b', 'BOOLEAN'); md.operation = op; md.object = c; md.solver = 'EXACT'; md.use_self = True; md.use_hole_tolerant = True
    apply_mods(o)
    for c in cutters: bpy.data.objects.remove(c)

def cutter(build):
    bm = bmesh.new(); build(bm)
    o = new_obj('_cut', bm, BLACK, '_tmp'); return o

def join(name, objs, collection):
    """Une varios objetos (cada uno con su material) en uno solo."""
    bm = bmesh.new(); mats = []
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        me.transform(o.matrix_world)
        m = o.data.materials[0]
        if m not in mats: mats.append(m)
        idx = mats.index(m)
        for p in me.polygons: p.material_index = idx
        bm.from_mesh(me); bpy.data.meshes.remove(me)
    for o in objs: bpy.data.objects.remove(o)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    try: me.set_sharp_from_angle(angle=math.radians(35))
    except Exception: pass
    o = bpy.data.objects.new(name, me); coll(collection).objects.link(o)
    return o

def part(name, material, collection, build, bev=None, smooth=35):
    bm = bmesh.new(); build(bm)
    o = new_obj(name, bm, material, collection, smooth)
    if bev: bevel(o, *bev) if isinstance(bev, tuple) else bevel(o, bev)
    return o

def finish(o, loc=None):
    if o.modifiers: apply_mods(o)
    if loc is not None: o.location = loc
    return o

parts_meta = {}
def meta(o, sistema, nombre, estado='E'):
    o['sistema'] = sistema; o['nombre'] = nombre; o['estado'] = estado
    parts_meta[o.name] = (sistema, nombre, estado)
    return o

# ================================================================= BLOQUE
def build_block():
    pieces = []
    # cuerpo superior (zona de cilindros), con chaflán
    top = part('blk_top', PAINT, '_tmp', lambda bm: bm_box(bm, BLOCK_L, 300, DECK - 150, (0, 0, (DECK + 150) / 2)), (6, 2)); apply_mods(top)
    boolean(top, [cutter(lambda bm, c=c: bm_cyl(bm, 70, 70, DECK - 120, (XC(c), 0, (DECK + 150) / 2 + 5), 'Z', 40)) for c in range(1, 7)])
    pieces.append(top)
    # faldón (cárter de cigüeñal), sección trapezoidal
    skirt = [(-150, 150), (150, 150), (195, 40), (195, -110), (-195, -110), (-195, 40)]
    sk = part('blk_skirt', PAINT, '_tmp', lambda bm: bm_prism(bm, skirt, BLOCK_L, 'YZ'), (5, 2)); apply_mods(sk)
    boolean(sk, [cutter(lambda bm: bm_prism(bm, [(-130, 170), (130, 170), (175, 40), (175, -130), (-175, -130), (-175, 40)], BLOCK_L - 40, 'YZ'))])
    pieces.append(sk)
    # carriles del cárter
    def rail(bm):
        for sgn in (-1, 1):
            bm_box(bm, BLOCK_L, 40, 18, (0, sgn * 185, -101))
            bm_box(bm, 30, 410, 18, (sgn * (BLOCK_L / 2 - 15), 0, -101))
    pieces.append(part('blk_rail', PAINT, '_tmp', rail, (3, 1)))
    # nervios verticales en ambos lados
    def ribs(bm):
        for i in range(8):
            x = RFOB + 35 + i * (BLOCK_L - 70) / 7
            for s in (-1, 1):
                bm_prism(bm, [(s * 150, 395), (s * 160, 395), (s * 202, 40), (s * 202, -95), (s * 190, -95), (s * 188, 40)][::(1 if s > 0 else -1)], 16, 'YZ', loc=(x, 0, 0))
    pieces.append(part('blk_ribs', PAINT, '_tmp', ribs, (2, 1)))
    # galería del árbol de levas (lado bomba, +Y) y tapones de agua
    pieces.append(part('blk_cambulge', PAINT, '_tmp', lambda bm: bm_cyl(bm, 55, 55, BLOCK_L - 10, (0, 150, 215), 'X', 32)))
    def plugs(bm):
        for c in range(1, 7):
            for s in (-1, 1):
                bm_cyl(bm, 21, 21, 10, (XC(c), s * 152, 300), 'Y', 24)
    pieces.append(part('blk_plugs', STEEL, '_tmp', plugs))
    # bases de montaje: filtro/enfriador de aceite (-Y) y bomba de combustible (+Y)
    pieces.append(part('blk_pad_oil', PAINT, '_tmp', lambda bm: bm_box(bm, 420, 30, 170, (120, -205, 110)), (4, 2)))
    pieces.append(part('blk_pad_fuel', PAINT, '_tmp', lambda bm: bm_box(bm, 200, 26, 150, (-250, 200, 240)), (4, 2)))
    blk = join('bloque', pieces, 'Estructura')
    return meta(blk, 'estructura', 'Bloque motor', 'E')

def build_mains():
    def caps(bm):
        for i in range(7):
            x = (3 - i) * PITCH
            bm_prism(bm, [(-120, 0), (120, 0), (120, -40), (85, -78), (-85, -78), (-120, -40)], 40, 'YZ', loc=(x, 0, 0))
            for s in (-1, 1): bm_cyl(bm, 11, 11, 30, (x, s * 95, -85), 'Z', 12)
    o = part('tapas_bancada', IRON, 'Estructura', caps, (3, 1))
    return meta(finish(o), 'estructura', 'Tapas de bancada', 'E')

def build_liners():
    def b(bm):
        for c in range(1, 7):
            bm_tube(bm, 69, 63, DECK - 160, (XC(c), 0, (DECK + 160) / 2), 'Z', 48)
            bm_tube(bm, 75, 63, 10, (XC(c), 0, DECK - 5), 'Z', 48)
    return meta(part('camisas', LINER, 'Estructura', b), 'estructura', 'Camisas de cilindro', 'V')

# ================================================================= CULATA Y CARCASA DE BALANCINES
def build_head():
    pieces = []
    pieces.append(part('hd_body', PAINT2, '_tmp', lambda bm: bm_box(bm, BLOCK_L - 4, 330, HEAD_H, (0, 0, DECK + HEAD_H / 2)), (5, 2)))
    pieces.append(part('hd_gasket', IRON, '_tmp', lambda bm: bm_box(bm, BLOCK_L, 304, 3, (0, 0, DECK + 1.5))))
    # salientes de tornillos (26 tornillos, patrón por pares entre cilindros)
    def bosses(bm):
        for i in range(7):
            x = (3 - i) * PITCH
            for s in (-1, 1):
                bm_cyl(bm, 17, 17, 16, (x, s * 120, HEAD_TOP + 8), 'Z', 20)
                bm_cyl(bm, 11, 11, 24, (x, s * 120, HEAD_TOP + 12), 'Z', 6)   # cabeza hexagonal
    pieces.append(part('hd_bolts', STEEL, '_tmp', bosses))
    # bridas de puertos: admisión (+Y) y escape (-Y)
    def flanges(bm):
        for c in range(1, 7):
            bm_box(bm, 95, 14, 62, (XC(c), 171, DECK + 70))
            bm_box(bm, 80, 14, 58, (XC(c), -171, DECK + 66))
    pieces.append(part('hd_flanges', PAINT2, '_tmp', flanges, (3, 1)))
    hd = join('culata', pieces, 'Estructura')
    ports = []
    for c in range(1, 7):
        ports.append(cutter(lambda bm, c=c: bm_prism(bm, rrect(66, 40, 12), 60, 'XZ', loc=(XC(c), 172, DECK + 70))))
        ports.append(cutter(lambda bm, c=c: bm_cyl(bm, 22, 22, 60, (XC(c), -172, DECK + 66), 'Y', 24)))
    boolean(hd, ports)
    return meta(hd, 'estructura', 'Culata', 'E')

def build_rocker_housing():
    pieces = []
    pieces.append(part('rh', ALU, '_tmp', lambda bm: bm_prism(bm, rrect(300, 45, 6), BLOCK_L - 30, 'YZ', loc=(0, 0, HEAD_TOP + 22.5)), (3, 1)))
    # tapa con nervios longitudinales y bordes redondeados
    pieces.append(part('cov', ALU, '_tmp', lambda bm: bm_prism(bm, rrect(286, 80, 30, 6), BLOCK_L - 50, 'YZ', loc=(0, 0, RH_TOP + 30)), (8, 3)))
    def ribs(bm):
        for y in (-80, -40, 0, 40, 80):
            bm_box(bm, BLOCK_L - 140, 7, 10, (0, y, RH_TOP + 72))
        for i in range(14):
            for s in (-1, 1):
                bm_cyl(bm, 7, 7, 12, (RFOB + 50 + i * (BLOCK_L - 100) / 13, s * 146, RH_TOP + 3), 'Z', 6)
    pieces.append(part('cov_ribs', ALU, '_tmp', ribs, (2, 1)))
    pieces.append(part('oilcap', BLACK, '_tmp', lambda bm: bm_cyl(bm, 32, 30, 22, (FFOB - 160, 70, RH_TOP + 78), 'Z', 32), (3, 2)))
    pieces.append(part('breather', BLACK, '_tmp', lambda bm: bm_cyl(bm, 26, 26, 50, (RFOB + 120, -60, RH_TOP + 85), 'Z', 24), (3, 2)))
    pieces.append(part('dataplate', BRASS, '_tmp', lambda bm: bm_box(bm, 150, 2, 70, (-60, 145, HEAD_TOP + 22))))
    o = join('tapa_balancines', pieces, 'Estructura')
    return meta(o, 'estructura', 'Carcasa y tapa de balancines', 'E')

# ================================================================= FRENTE: CARCASA Y TAPA DE ENGRANAJES
def build_gear_housing():
    outline = [(-205, -110), (205, -110), (215, 60), (205, 330), (150, 420), (-60, 440), (-190, 380), (-215, 200)]
    pieces = [part('gh', ALU, '_tmp', lambda bm: bm_prism(bm, outline, 28, 'YZ', loc=(FFOB + 14, 0, 0)), (4, 2))]
    cover = [(-185, -95), (185, -95), (192, 60), (185, 300), (130, 380), (-40, 395), (-170, 340), (-192, 180)]
    pieces.append(part('gc', ALU, '_tmp', lambda bm: bm_prism(bm, cover, 30, 'YZ', loc=(FFOB + 43, 0, 0)), (6, 2)))
    def bolts(bm):
        for (u, v) in [(-175, -85), (0, -88), (175, -85), (183, 80), (180, 250), (120, 360), (-40, 380), (-160, 320), (-185, 150), (-185, 20)]:
            bm_cyl(bm, 8, 8, 10, (FFOB + 61, u, v), 'X', 6)
    pieces.append(part('gc_bolts', STEEL, '_tmp', bolts))
    pieces.append(part('seal', ALU, '_tmp', lambda bm: bm_cyl(bm, 78, 70, 20, (FFOB + 66, 0, 0), 'X', 40), (3, 2)))
    o = join('carcasa_engranajes', pieces, 'Estructura')
    return meta(o, 'estructura', 'Carcasa y tapa de engranajes delantera', 'E')

# ================================================================= TRASERA: CARCASA DE VOLANTE SAE 2
def build_flywheel_housing():
    pieces = []
    # cuerpo cónico desde el bloque hasta la brida SAE 2 (Ø447,68 interior, círculo de tornillos Ø469,9)
    pieces.append(part('fh_cone', PAINT, '_tmp', lambda bm: bm_tube(bm, 262, 240, 70, (RFOB - 35, 0, 0), 'X', 64)))
    pieces.append(part('fh_flange', PAINT, '_tmp', lambda bm: bm_tube(bm, 262, 224, 18, (RFOB - 79, 0, 0), 'X', 64), (2, 1)))
    pieces.append(part('fh_plate', PAINT, '_tmp', lambda bm: bm_prism(bm, [(-210, -150), (210, -150), (230, 120), (190, 330), (-190, 330), (-230, 120)], 24, 'YZ', loc=(RFOB - 12, 0, 0)), (4, 2)))
    def ribs(bm):
        for k in range(10):
            a = math.radians(18 + k * 36)
            bm_box(bm, 66, 10, 46, (RFOB - 40, math.cos(a) * 262, math.sin(a) * 262), Matrix.Rotation(a - math.pi / 2, 4, 'X'))
        for k in range(12):
            a = math.radians(k * 30)
            bm_cyl(bm, 8, 8, 10, (RFOB - 92, math.cos(a) * 235, math.sin(a) * 235), 'X', 6)
    pieces.append(part('fh_ribs', PAINT, '_tmp', ribs))
    # montaje del motor de arranque (distancia 243,84 mm al eje, lado +Y abajo)
    a = math.radians(-35); sy, sz = math.cos(a) * 243.84, math.sin(a) * 243.84
    pieces.append(part('fh_starterpad', PAINT, '_tmp', lambda bm: bm_cyl(bm, 62, 62, 40, (RFOB - 50, sy + 20, sz), 'X', 32), (3, 2)))
    # patas traseras de soporte
    def feet(bm):
        for s in (-1, 1):
            bm_prism(bm, [(s * 220, 40), (s * 330, -150), (s * 330, -190), (s * 220, -190)][::s], 22, 'YZ', loc=(RFOB - 60, 0, 0))
            bm_box(bm, 140, 130, 20, (RFOB - 60, s * 290, -200))
    pieces.append(part('fh_feet', IRON, '_tmp', feet, (3, 1)))
    o = join('carcasa_volante', pieces, 'Estructura')
    return meta(o, 'estructura', 'Carcasa del volante SAE 2', 'C')

# ================================================================= CÁRTER
def build_oil_pan():
    pieces = []
    pieces.append(part('pan_flange', PAINT, '_tmp', lambda bm: bm_box(bm, BLOCK_L, 420, 14, (0, 0, -117)), (3, 1)))
    shallow = [(-190, -124), (190, -124), (175, -200), (-175, -200)]
    pieces.append(part('pan_shallow', PAINT, '_tmp', lambda bm: bm_prism(bm, shallow, BLOCK_L - 20, 'YZ'), (8, 3)))
    # sumidero profundo (lado trasero), con fondo inclinado como en el catálogo
    sump = [(-80, -124), (520, -124), (520, -200), (480, -360), (-60, -360), (-80, -200)]
    pieces.append(part('pan_sump', PAINT, '_tmp', lambda bm: bm_prism(bm, [(x - 470, z) for x, z in sump], 340, 'XZ'), (12, 3)))
    pieces.append(part('pan_drain', STEEL, '_tmp', lambda bm: bm_cyl(bm, 14, 14, 20, (-78, 0, -370), 'Z', 6)))
    def bolts(bm):
        for i in range(16):
            for s in (-1, 1): bm_cyl(bm, 7, 7, 10, (RFOB + 30 + i * (BLOCK_L - 60) / 15, s * 200, -128), 'Z', 6)
    pieces.append(part('pan_bolts', STEEL, '_tmp', bolts))
    pieces.append(part('dipstick', BRASS, '_tmp', lambda bm: bm_sweep(bm, [(-300, 205, -60), (-300, 215, 150), (-290, 230, 330), (-290, 232, 400)], 6, 10)))
    pieces.append(part('dip_handle', REDP, '_tmp', lambda bm: bm_tube(bm, 18, 12, 6, (-290, 232, 410), 'X', 16)))
    o = join('carter', pieces, 'Estructura')
    return meta(o, 'estructura', 'Cárter de aceite', 'C')

# ================================================================= CIGÜEÑAL, VOLANTE, AMORTIGUADOR
def build_crank():
    pieces = []
    def journals(bm):
        for i in range(7): bm_cyl(bm, 50, 50, 44, ((3 - i) * PITCH, 0, 0), 'X', 40)
    pieces.append(part('cr_main', STEEL, '_tmp', journals, (1.5, 1)))
    web_profile = (circle_pts(52, 16, 0, R, -10, 190) + circle_pts(118, 24, 0, 0, 205, 335))
    def webs(bm):
        for c in range(1, 7):
            a = math.radians(PHI[c])
            rot = Matrix.Rotation(a, 4, 'X')
            for s in (-1, 1):
                tmp = bmesh.new(); bm_prism(tmp, web_profile, 26, 'YZ', loc=(XC(c) + s * 39, 0, 0))
                bmesh.ops.rotate(tmp, verts=tmp.verts, cent=(XC(c), 0, 0), matrix=rot)
                me = bpy.data.meshes.new('t'); tmp.to_mesh(me); tmp.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)
    pieces.append(part('cr_webs', IRON, '_tmp', webs, (4, 2, 30)))
    def pins(bm):
        for c in range(1, 7):
            a = math.radians(PHI[c])
            bm_cyl(bm, 42, 42, 52, (XC(c), 0, 0) , 'X', 32, rot=None)
            # mover a la posición de la muñequilla (rotación en torno a X)
        for v in bm.verts: pass
    def pins2(bm):
        for c in range(1, 7):
            a = math.radians(PHI[c])
            m = Matrix.Rotation(a, 4, 'X') @ Matrix.Translation((XC(c), 0, R))
            bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=42, radius2=42, depth=52, matrix=m @ m_rot('X'))
    pieces.append(part('cr_pins', STEEL, '_tmp', pins2, (1.5, 1)))
    pieces.append(part('cr_nose', STEEL, '_tmp', lambda bm: bm_cyl(bm, 40, 40, 150, (FFOB + 20, 0, 0), 'X', 32)))
    pieces.append(part('cr_gear', STEEL, '_tmp', lambda bm: bm_prism(bm, gear_pts(66, 72, 40), 30, 'YZ', loc=(FFOB - 30, 0, 0))))
    pieces.append(part('cr_flange', STEEL, '_tmp', lambda bm: bm_cyl(bm, 75, 75, 26, (RFOB - 15, 0, 0), 'X', 48), (2, 1)))
    o = join('ciguenal', pieces, 'Movil')
    return meta(o, 'cigueñal', 'Cigüeñal', 'E')

def build_damper():
    pieces = []
    pieces.append(part('dmp', IRON, '_tmp', lambda bm: bm_cyl(bm, 160, 160, 62, (FFOB + 95, 0, 0), 'X', 64), (4, 2)))
    pieces.append(part('dmp_face', STEEL, '_tmp', lambda bm: bm_tube(bm, 152, 70, 4, (FFOB + 127, 0, 0), 'X', 64)))
    def holes(bm):
        for k in range(6):
            a = k * math.pi / 3
            bm_cyl(bm, 9, 9, 8, (FFOB + 130, math.cos(a) * 52, math.sin(a) * 52), 'X', 6)
    pieces.append(part('dmp_bolts', STEEL, '_tmp', holes))
    # polea del cigüeñal Ø190,7 (poly-V de 8 canales), plano de correa a 140 mm del FFOB
    def pulley(bm):
        bm_cyl(bm, 95.35, 95.35, 36, (BELT_X, 0, 0), 'X', 64)
        for k in range(8):
            bm_cyl(bm, 97, 97, 1.6, (BELT_X - 15 + k * 4.3, 0, 0), 'X', 64)
    pieces.append(part('pul', STEEL, '_tmp', pulley))
    o = join('amortiguador_polea', pieces, 'Movil')
    return meta(o, 'cigueñal', 'Amortiguador de vibraciones y polea Ø190,7', 'C')

def build_flywheel():
    pieces = []
    pieces.append(part('fw', STEEL, '_tmp', lambda bm: bm_cyl(bm, 215, 215, 60, (RFOB - 75, 0, 0), 'X', 72), (3, 2)))
    pieces.append(part('fw_ring', IRON, '_tmp', lambda bm: bm_prism(bm, gear_pts(212, 222, 118), 22, 'YZ', loc=(RFOB - 95, 0, 0))))
    pieces.append(part('fw_pilot', IRON, '_tmp', lambda bm: bm_tube(bm, 50, 36, 10, (RFOB - 108, 0, 0), 'X', 36)))
    def slots(bm):
        for k in range(8):
            a = k * math.pi / 4
            bm_cyl(bm, 10, 10, 8, (RFOB - 107, math.cos(a) * 85, math.sin(a) * 85), 'X', 6)
        for k in range(3):
            a = k * 2 * math.pi / 3 + 0.4
            bm_box(bm, 6, 26, 60, (RFOB - 106, math.cos(a) * 150, math.sin(a) * 150), Matrix.Rotation(a, 4, 'X'))
    pieces.append(part('fw_bolts', BLACK, '_tmp', slots))
    o = join('volante', pieces, 'Movil')
    return meta(o, 'cigueñal', 'Volante de inercia', 'C')

# ================================================================= PISTÓN Y BIELA (en posición neutra: PMS, x = 0)
def build_piston(c):
    pieces = []
    crown = part('pst_crown', STEEL, '_tmp', lambda bm: bm_cyl(bm, 62, 62, 52, (0, 0, CH - 26), 'Z', 48), (2, 1)); apply_mods(crown)
    bowl = cutter(lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=46, matrix=Matrix.Translation((0, 0, CH + 30)) @ Matrix.Diagonal((1, 1, 0.75, 1))))
    boolean(crown, [bowl]); pieces.append(crown)
    def grooves(bm):
        for k in range(3): bm_tube(bm, 62.4, 58, 3, (0, 0, CH - 10 - k * 9), 'Z', 48)
    pieces.append(part('pst_rings', IRON, '_tmp', grooves))
    # falda articulada (dos lóbulos de empuje) y bulón
    def skirt(bm):
        for s in (-1, 1):
            bm_prism(bm, circle_pts(61, 12, 0, 0, -45, 45), 1, 'XY')  # placeholder, se reemplaza abajo
    def skirt2(bm):
        prof = [(math.cos(math.radians(a)) * 61, math.sin(math.radians(a)) * 61) for a in range(-50, 51, 10)]
        prof += [(math.cos(math.radians(a)) * 54, math.sin(math.radians(a)) * 54) for a in range(50, -51, -10)]
        for s in (0, 180):
            pr = [(x * math.cos(math.radians(s)) - y * math.sin(math.radians(s)), x * math.sin(math.radians(s)) + y * math.cos(math.radians(s))) for x, y in prof]
            bm_prism(bm, [(-p[1], p[0]) for p in pr], 70, 'XY', offset=CH - 52 - 35)
    pieces.append(part('pst_skirt', ALU, '_tmp', skirt2))
    pieces.append(part('pst_boss', STEEL, '_tmp', lambda bm: bm_cyl(bm, 30, 30, 76, (0, 0, 0), 'X', 24)))
    pieces.append(part('pst_pin', STEEL, '_tmp', lambda bm: bm_cyl(bm, 22, 22, 110, (0, 0, 0), 'X', 24)))
    o = join(f'piston_{c}', pieces, 'Movil')
    return meta(o, 'moviles', f'Pistón del cilindro {c}', 'E')

def build_rod(c):
    pieces = []
    beam = [(-15, 40), (15, 40), (11, LROD - 30), (-11, LROD - 30)]
    pieces.append(part('rod_beam', STEEL, '_tmp', lambda bm: bm_prism(bm, beam, 40, 'XZ'), (3, 2)))
    pieces.append(part('rod_web', STEEL, '_tmp', lambda bm: bm_prism(bm, [(-24, 45), (24, 45), (17, LROD - 35), (-17, LROD - 35)], 16, 'XZ'), (2, 1)))
    pieces.append(part('rod_small', STEEL, '_tmp', lambda bm: bm_tube(bm, 34, 22, 40, (0, 0, LROD), 'Y', 32)))
    pieces.append(part('rod_big', STEEL, '_tmp', lambda bm: bm_tube(bm, 66, 42.5, 40, (0, 0, 0), 'Y', 40)))
    # tapa con corte en diagonal (biela de corte angular, cat. pág. 88)
    def boltsb(bm):
        for s in (-1, 1):
            bm_cyl(bm, 9, 9, 120, (s * 56, 0, -6), 'Z', 12, rot=Matrix.Rotation(math.radians(35), 4, 'Y'))
    pieces.append(part('rod_bolts', IRON, '_tmp', boltsb))
    pieces.append(part('rod_cap_line', IRON, '_tmp', lambda bm: bm_box(bm, 150, 41, 2.5, (0, 0, 0), Matrix.Rotation(math.radians(35), 4, 'Y'))))
    o = join(f'biela_{c}', pieces, 'Movil')
    o.rotation_mode = 'XYZ'
    # la biela gira sobre el plano YZ (eje de giro = X)
    me = o.data; me.transform(Matrix.Rotation(math.radians(90), 4, 'Z'))
    return meta(o, 'moviles', f'Biela del cilindro {c}', 'E')

# ================================================================= ÁRBOL DE LEVAS Y DISTRIBUCIÓN
CAM_Y, CAM_Z = 150.0, 215.0
def lobe_pts(base=26, lift=8, n=36):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        d = math.cos(a)
        r = base + lift * max(0.0, d) ** 3
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts

def build_camshaft():
    pieces = []
    pieces.append(part('cam_shaft', STEEL, '_tmp', lambda bm: bm_cyl(bm, 22, 22, BLOCK_L - 20, (0, 0, 0), 'X', 24)))
    def lobes(bm):
        for c in range(1, 7):
            for dx, peak in ((-36, 270), (36, 450), (0, 720)):
                ang = math.radians((PHI[c] + peak) / 2)
                tmp = bmesh.new(); bm_prism(tmp, lobe_pts(), 22, 'YZ', loc=(XC(c) + dx, 0, 0))
                bmesh.ops.rotate(tmp, verts=tmp.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2 + ang, 4, 'X'))
                me = bpy.data.meshes.new('t'); tmp.to_mesh(me); tmp.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)
        for i in range(7): bm_cyl(bm, 32, 32, 30, ((3 - i) * PITCH, 0, 0), 'X', 32)
    pieces.append(part('cam_lobes', STEEL, '_tmp', lobes))
    pieces.append(part('cam_gear', STEEL, '_tmp', lambda bm: bm_prism(bm, gear_pts(132, 140, 80), 24, 'YZ', loc=(FFOB - 28, 0, 0))))
    o = join('arbol_levas', pieces, 'Distribucion')
    o.location = (0, CAM_Y, CAM_Z)
    return meta(o, 'distribucion', 'Árbol de levas', 'C')

def build_valvetrain():
    objs = []
    spring_path = [(math.cos(t) * 17, math.sin(t) * 17, t / (2 * math.pi) * 4.6) for t in [i * 0.35 for i in range(int(6.2 * 2 * math.pi / 0.35))]]
    for c in range(1, 7):
        for kind, s in (('adm', 1), ('esc', -1)):
            def valves(bm, c=c, s=s):
                for dx in (-30, 30):
                    x, y = XC(c) + dx, s * 36
                    bm_cyl(bm, 21, 14, 7, (x, y, DECK + 9), 'Z', 32)
                    bm_cyl(bm, 4.5, 4.5, 150, (x, y, DECK + 85), 'Z', 12)
                    bm_cyl(bm, 15, 11, 6, (x, y, HEAD_TOP + 34), 'Z', 20)
                bm_box(bm, 84, 20, 9, (XC(c), y, HEAD_TOP + 41))
            o = part(f'valvulas_{kind}_{c}', STEEL, 'Distribucion', valves)
            meta(o, 'distribucion', f'Válvulas de {"admisión" if s > 0 else "escape"} · cilindro {c}', 'E'); objs.append(o)
            def springs(bm, c=c, s=s):
                for dx in (-30, 30):
                    tmp = bmesh.new(); bm_sweep(tmp, [(p[0] + XC(c) + dx, p[1] + s * 36, p[2] * 1 + HEAD_TOP + 2) for p in spring_path], 2.6, 6, caps=False, smooth=False)
                    me = bpy.data.meshes.new('t'); tmp.to_mesh(me); tmp.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)
            o = part(f'muelles_{kind}_{c}', COPPER, 'Distribucion', springs)
            meta(o, 'distribucion', f'Muelles de válvula · cilindro {c}', 'E'); objs.append(o)
        # balancines (3 por cilindro: escape, inyector, admisión) sobre eje longitudinal
        for kind, dx, yend in (('esc', -36, -36), ('iny', 0, 0), ('adm', 36, 36)):
            def rocker(bm, dx=dx, yend=yend):
                y0 = 115.0
                bm_box(bm, 22, y0 - yend + 30, 18, (0, (y0 + yend) / 2, 0))
                bm_cyl(bm, 15, 15, 26, (0, 0, 0), 'X', 20)
            o = part(f'balancin_{kind}_{c}', IRON, 'Distribucion', rocker, (2, 1))
            finish(o); o.location = (XC(c) + dx, 0, HEAD_TOP + 58)
            o.data.transform(Matrix.Translation((0, 0, 0)))
            meta(o, 'distribucion', f'Balancín de {"admisión" if kind == "adm" else "escape" if kind == "esc" else "inyector"} · cilindro {c}', 'E'); objs.append(o)
            def push(bm, dx=dx):
                bm_cyl(bm, 7, 7, HEAD_TOP + 50 - CAM_Z - 40, (0, 0, (HEAD_TOP + 50 - CAM_Z - 40) / 2), 'Z', 10)
            o = part(f'varilla_{kind}_{c}', STEEL, 'Distribucion', push)
            o.location = (XC(c) + dx, 130, CAM_Z + 40)
            meta(o, 'distribucion', f'Varilla de empuje · cilindro {c}', 'E'); objs.append(o)
        def injector(bm, c=c):
            bm_cyl(bm, 11, 11, 150, (XC(c), 0, DECK + 85), 'Z', 16)
            bm_cyl(bm, 19, 19, 40, (XC(c), 0, HEAD_TOP + 22), 'Z', 20)
            bm_cyl(bm, 5, 2, 12, (XC(c), 0, DECK + 4), 'Z', 10)
        o = part(f'inyector_{c}', BRASS, 'Combustible', injector)
        meta(o, 'combustible', f'Inyector · cilindro {c}', 'C'); objs.append(o)
    shaft = part('eje_balancines', STEEL, 'Distribucion', lambda bm: bm_cyl(bm, 12, 12, BLOCK_L - 60, (0, 0, HEAD_TOP + 58), 'X', 16))
    meta(shaft, 'distribucion', 'Eje de balancines', 'E')
    return objs

# ================================================================= ADMISIÓN
def build_intake():
    # colector de admisión (cat. pág. 60): cajón largo con brida y entrada superior
    pieces = []
    pieces.append(part('im_body', ALU, '_tmp', lambda bm: bm_prism(bm, rrect(90, 110, 22), BLOCK_L - 60, 'YZ', loc=(0, 230, DECK + 72)), (4, 2)))
    pieces.append(part('im_flange', ALU, '_tmp', lambda bm: bm_box(bm, BLOCK_L - 40, 12, 130, (0, 182, DECK + 72)), (3, 1)))
    pieces.append(part('im_inlet', ALU, '_tmp', lambda bm: bm_box(bm, 120, 100, 70, (-60, 235, DECK + 155)), (8, 3)))
    def bolts(bm):
        for i in range(16):
            for z in (DECK + 20, DECK + 124): bm_cyl(bm, 7, 7, 12, (RFOB + 50 + i * (BLOCK_L - 100) / 15, 192, z), 'Y', 6)
    pieces.append(part('im_bolts', STEEL, '_tmp', bolts))
    o = join('colector_admision', pieces, 'Admision')
    meta(o, 'admision', 'Colector de admisión', 'C')
    # codo de transferencia de aire desde el turbo (cat. pág. 64) + manguera Ø102
    def elbow(bm):
        bm_sweep(bm, [(-60, 235, DECK + 190), (-70, 235, DECK + 260), (-150, 120, HEAD_TOP + 175), (-280, -100, HEAD_TOP + 190), (RFOB - 20, -190, HEAD_TOP + 130), (RFOB - 55, -215, HEAD_TOP + 50)], 51, 28)
    e = part('conducto_aire', ALU, 'Admision', elbow)
    meta(e, 'turbo', 'Conducto de aire turbo → colector (Ø102)', 'C')
    def clamps(bm):
        bm_tube(bm, 56, 50, 14, (-62, 235, DECK + 210), 'Z', 32)
    cl = part('abrazaderas', STEEL, 'Admision', clamps)
    meta(cl, 'admision', 'Abrazaderas', 'E')
    return [o, e, cl]

# ================================================================= ESCAPE Y TURBO
def build_exhaust():
    objs = []
    # colector de escape en 3 secciones con brida por cilindro y codos
    def manifold(bm):
        for c in range(1, 7):
            bm_box(bm, 80, 16, 70, (XC(c), -186, DECK + 66))
            bm_sweep(bm, [(XC(c), -192, DECK + 66), (XC(c), -225, DECK + 70), (XC(c) - 20, -250, DECK + 95)], 26, 20)
        bm_sweep(bm, [(FFOB - 70, -252, DECK + 98), (0, -255, DECK + 100), (RFOB + 70, -258, DECK + 105), (RFOB + 60, -258, HEAD_TOP - 20)], [38] * 37, 28)
    o = part('colector_escape', HOT, 'Escape', manifold)
    meta(o, 'escape', 'Colector de escape (3 piezas)', 'E'); objs.append(o)
    def joints(bm):
        for x in (PITCH, -PITCH):
            bm_tube(bm, 42, 36, 12, (x, -255, DECK + 100), 'X', 28)
    j = part('juntas_colector', STEEL, 'Escape', joints)
    meta(j, 'escape', 'Juntas deslizantes del colector', 'E'); objs.append(j)
    return objs

def volute(bm, center, axis_rot, r_base, r_tube0, r_tube1, turns=0.9, seg=48, ring=20):
    pts, radii = [], []
    for i in range(seg + 1):
        t = i / seg; a = 2 * math.pi * turns * t
        rt = r_tube0 + (r_tube1 - r_tube0) * t
        rr = r_base + rt
        pts.append(Vector((0, math.cos(a) * rr, math.sin(a) * rr)))
        radii.append(rt)
    tmp = bmesh.new(); bm_sweep(tmp, pts, radii, ring, caps=True, smooth=False)
    bmesh.ops.transform(tmp, verts=tmp.verts, matrix=Matrix.Translation(center) @ axis_rot)
    me = bpy.data.meshes.new('t'); tmp.to_mesh(me); tmp.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)

TURBO = Vector((RFOB + 30, -330, HEAD_TOP + 40))
def build_turbo():
    objs = []
    tx, ty, tz = TURBO
    # eje del turbo paralelo a X; turbina hacia el frente, compresor hacia atrás
    pieces = []
    pieces.append(part('tb_turb', HOT, '_tmp', lambda bm: volute(bm, (tx + 55, ty, tz), Matrix.Identity(4), 52, 22, 52)))
    pieces.append(part('tb_turb_core', HOT, '_tmp', lambda bm: bm_cyl(bm, 70, 62, 80, (tx + 55, ty, tz), 'X', 40), (3, 2)))
    pieces.append(part('tb_inlet', HOT, '_tmp', lambda bm: bm_sweep(bm, [(tx + 60, ty + 40, tz - 70), (tx + 70, ty + 70, tz - 100), (RFOB + 60, -258, HEAD_TOP - 20)], 34, 24)))
    pieces.append(part('tb_flange', HOT, '_tmp', lambda bm: bm_box(bm, 16, 90, 90, (tx + 60, ty + 55, tz - 85)), (3, 1)))
    pieces.append(part('tb_outlet', HOT, '_tmp', lambda bm: bm_tube(bm, 52, 44, 50, (tx + 120, ty, tz), 'X', 40)))
    pieces.append(part('tb_vband', STEEL, '_tmp', lambda bm: bm_tube(bm, 58, 52, 14, (tx + 145, ty, tz), 'X', 40)))
    pieces.append(part('tb_chra', IRON, '_tmp', lambda bm: bm_cyl(bm, 46, 46, 70, (tx - 15, ty, tz), 'X', 32), (3, 2)))
    pieces.append(part('tb_comp', ALU, '_tmp', lambda bm: volute(bm, (tx - 85, ty, tz), Matrix.Identity(4), 62, 20, 44, 0.95)))
    pieces.append(part('tb_comp_core', ALU, '_tmp', lambda bm: bm_cyl(bm, 82, 82, 70, (tx - 85, ty, tz), 'X', 48), (4, 2)))
    pieces.append(part('tb_comp_in', ALU, '_tmp', lambda bm: bm_tube(bm, 56, 48, 70, (tx - 150, ty, tz), 'X', 40)))
    # wastegate (cat. pág. 98)
    pieces.append(part('tb_wg', BLACK, '_tmp', lambda bm: bm_cyl(bm, 36, 36, 34, (tx - 40, ty - 105, tz + 30), 'Y', 32), (3, 2)))
    pieces.append(part('tb_wgrod', STEEL, '_tmp', lambda bm: bm_sweep(bm, [(tx - 40, ty - 90, tz + 30), (tx + 30, ty - 80, tz + 10), (tx + 60, ty - 70, tz - 20)], 3, 8)))
    o = join('turbo', pieces, 'Turbo')
    meta(o, 'turbo', 'Turbocompresor con wastegate', 'C'); objs.append(o)
    # ruedas giratorias (objetos separados para animación)
    for nm, x, mt, n in (('rueda_turbina', tx + 55, STEEL, 11), ('rueda_compresor', tx - 85, ALU, 12)):
        def wheel(bm, n=n):
            bm_cyl(bm, 14, 22, 40, (0, 0, 0), 'X', 16)
            for i in range(n):
                a = 2 * math.pi * i / n
                bm_box(bm, 40, 3, 30, (0, math.cos(a) * 26, math.sin(a) * 26), Matrix.Rotation(a + math.pi / 2, 4, 'X') @ Matrix.Rotation(0.5, 4, 'Z'))
        w = part(nm, mt, 'Turbo', wheel); w.location = (x, ty, tz)
        meta(w, 'turbo', 'Rueda de turbina' if 'turb' in nm else 'Rueda del compresor', 'E'); objs.append(w)
    # salida de escape (codo) y filtro de aire con codo (cat. pág. 22)
    ex = part('codo_escape', HOT, 'Escape', lambda bm: bm_sweep(bm, [(tx + 150, ty, tz), (tx + 210, ty, tz), (tx + 240, ty - 20, tz + 80), (tx + 250, ty - 30, tz + 230)], 50, 28))
    meta(ex, 'escape', 'Salida de escape', 'E'); objs.append(ex)
    def cleaner(bm):
        bm_sweep(bm, [(tx - 185, ty, tz), (tx - 230, ty, tz), (tx - 250, ty - 60, tz + 20), (tx - 250, ty - 160, tz + 40)], 52, 24)
    cl = part('codo_filtro_aire', BLACK, 'Admision', cleaner)
    meta(cl, 'admision', 'Codo del filtro de aire', 'C'); objs.append(cl)
    return objs

# ================================================================= LADO BOMBA (+Y): ECM, BOMBA DE COMBUSTIBLE, FILTRO, COMPRESOR
def build_fuel_side():
    objs = []
    # ECM con placa de refrigeración (cat. pág. 84)
    pieces = []
    pieces.append(part('ecm_plate', ALU, '_tmp', lambda bm: bm_box(bm, 330, 14, 250, (110, 205, 175)), (3, 1)))
    pieces.append(part('ecm_body', BLACK, '_tmp', lambda bm: bm_box(bm, 300, 44, 220, (110, 238, 175)), (6, 2)))
    def fins(bm):
        for i in range(10): bm_box(bm, 280, 8, 6, (110, 262, 85 + i * 20))
        for k in range(3): bm_box(bm, 60, 36, 46, (10 + k * 80, 250, 300))
    pieces.append(part('ecm_fins', BLACK, '_tmp', fins))
    o = join('ecm', pieces, 'Combustible'); meta(o, 'accesorios', 'ECM con placa de refrigeración', 'C'); objs.append(o)
    # bomba de combustible (cat. págs. 46–48)
    pieces = []
    pieces.append(part('fp_body', ALU, '_tmp', lambda bm: bm_box(bm, 170, 110, 140, (-250, 270, 240)), (12, 3)))
    pieces.append(part('fp_gear', ALU, '_tmp', lambda bm: bm_cyl(bm, 62, 62, 60, (-250, 250, 330), 'Y', 40), (4, 2)))
    pieces.append(part('fp_actuators', BLACK, '_tmp', lambda bm: [bm_cyl(bm, 22, 22, 50, (-300 + k * 50, 335, 260), 'Y', 20) for k in range(3)]))
    pieces.append(part('fp_drive', IRON, '_tmp', lambda bm: bm_cyl(bm, 50, 50, 40, (-150, 230, 240), 'X', 32), (3, 2)))
    o = join('bomba_combustible', pieces, 'Combustible'); meta(o, 'combustible', 'Bomba de combustible', 'C'); objs.append(o)
    # filtro de combustible (cat. pág. 40)
    def ff(bm):
        bm_cyl(bm, 52, 52, 200, (-20, 270, -10), 'Z', 40)
        bm_cyl(bm, 58, 58, 30, (-20, 270, 105), 'Z', 40)
    o = part('filtro_combustible', REDP, 'Combustible', ff, (4, 2)); meta(o, 'combustible', 'Filtro de combustible', 'C'); objs.append(o)
    head = part('cabezal_filtro_comb', ALU, 'Combustible', lambda bm: bm_box(bm, 90, 60, 40, (-20, 240, 140)), (5, 2))
    meta(head, 'combustible', 'Cabezal del filtro de combustible', 'E'); objs.append(head)
    # compresor de aire 18,7 CFM: 217 x 142 x 216 (V, O&M pág. 368)
    pieces = []
    pieces.append(part('ac_body', ALU, '_tmp', lambda bm: bm_box(bm, 216, 142, 140, (RFOB + 150, 255, 320)), (10, 3)))
    pieces.append(part('ac_head', IRON, '_tmp', lambda bm: bm_box(bm, 150, 130, 77, (RFOB + 150, 255, 428)), (8, 2)))
    def acfins(bm):
        for i in range(5): bm_box(bm, 150, 132, 4, (RFOB + 150, 255, 400 + i * 12))
    pieces.append(part('ac_fins', IRON, '_tmp', acfins))
    o = join('compresor_aire', pieces, 'Accesorios'); meta(o, 'aire', 'Compresor de aire 18,7 CFM (217 × 142 × 216 mm)', 'V'); objs.append(o)
    # motor de arranque en la carcasa SAE 2 (centro a 243,84 mm)
    a = math.radians(-35); sy, sz = math.cos(a) * 243.84 + 20, math.sin(a) * 243.84
    def starter(bm):
        bm_cyl(bm, 62, 62, 260, (RFOB + 90, sy, sz), 'X', 40)
        bm_cyl(bm, 36, 36, 170, (RFOB + 70, sy + 30, sz + 85), 'X', 28)
    o = part('motor_arranque', BLACK, 'Accesorios', starter, (5, 2)); meta(o, 'accesorios', 'Motor de arranque', 'C'); objs.append(o)
    return objs

# ================================================================= LADO ESCAPE (-Y): ENFRIADOR Y FILTROS DE ACEITE
def build_oil_side():
    objs = []
    pieces = []
    pieces.append(part('oc_head', ALU, '_tmp', lambda bm: bm_box(bm, 380, 70, 150, (120, -255, 110)), (10, 3)))
    pieces.append(part('oc_tube', ALU, '_tmp', lambda bm: bm_cyl(bm, 50, 50, 420, (120, -275, 205), 'X', 32), (4, 2)))
    o = join('enfriador_aceite', pieces, 'Lubricacion'); meta(o, 'lubricacion', 'Cabezal de filtro y enfriador de aceite', 'C'); objs.append(o)
    def filters(bm):
        bm_cyl(bm, 60, 60, 240, (250, -300, -40), 'Z', 40)
        bm_cyl(bm, 52, 52, 200, (110, -300, -20), 'Z', 40)
    o = part('filtros_aceite', BLACK, 'Lubricacion', filters, (5, 2)); meta(o, 'lubricacion', 'Filtros de aceite', 'C'); objs.append(o)
    return objs

# ================================================================= FRENTE: CORREA, ALTERNADOR, VENTILADOR, BOMBA DE AGUA
FAN = (BELT_X, 19.0, 215.9)          # C
ALT = (BELT_X, -255.0, 250.0)         # E (apoyos a 330 / 223 mm, cat. pág. 33)
WP = (FFOB + 70, -95.0, 120.0)        # E
def build_front():
    objs = []
    # alternador Delco 22SI: largo 162 mm, polea Ø76,2 (cat. págs. 31, 33)
    pieces = []
    pieces.append(part('alt_body', ALU, '_tmp', lambda bm: bm_cyl(bm, 90, 90, 162, (ALT[0] - 120, ALT[1], ALT[2]), 'X', 48), (6, 2)))
    def fins(bm):
        for i in range(16):
            a = 2 * math.pi * i / 16
            bm_box(bm, 60, 4, 18, (ALT[0] - 70, ALT[1] + math.cos(a) * 86, ALT[2] + math.sin(a) * 86), Matrix.Rotation(a + math.pi / 2, 4, 'X'))
    pieces.append(part('alt_fins', ALU, '_tmp', fins))
    pieces.append(part('alt_pulley', STEEL, '_tmp', lambda bm: bm_cyl(bm, 38.1, 38.1, 34, (ALT[0], ALT[1], ALT[2]), 'X', 32)))
    pieces.append(part('alt_fan', STEEL, '_tmp', lambda bm: bm_cyl(bm, 70, 70, 10, (ALT[0] - 30, ALT[1], ALT[2]), 'X', 32)))
    pieces.append(part('alt_bracket', IRON, '_tmp', lambda bm: bm_box(bm, 30, 160, 140, (FFOB + 70, ALT[1] + 60, ALT[2] - 60)), (4, 2)))
    o = join('alternador', pieces, 'Accesorios'); meta(o, 'accesorios', 'Alternador (Delco 22SI, largo 162 mm)', 'C'); objs.append(o)
    # cubo y polea del ventilador Ø190 a 215,9 mm sobre el cigüeñal (cat. pág. 38)
    def fan(bm):
        bm_cyl(bm, 95, 95, 36, FAN, 'X', 64)
        bm_cyl(bm, 60, 60, 60, (FAN[0] - 45, FAN[1], FAN[2]), 'X', 40)
        for k in range(4):
            a = k * math.pi / 2 + math.pi / 4
            bm_cyl(bm, 7, 7, 12, (FAN[0] + 22, FAN[1] + math.cos(a) * 44.45, FAN[2] + math.sin(a) * 44.45), 'X', 6)
    o = part('cubo_ventilador', STEEL, 'Accesorios', fan); meta(o, 'accesorios', 'Cubo y polea del ventilador (Ø190)', 'C'); objs.append(o)
    # tensor
    TEN = (BELT_X, -95.0, 120.0)
    o = part('tensor', STEEL, 'Accesorios', lambda bm: bm_cyl(bm, 36, 36, 34, TEN, 'X', 32)); meta(o, 'accesorios', 'Tensor de correa', 'E'); objs.append(o)
    # correa poly-V: tangentes exteriores aproximadas en el plano X = BELT_X
    pul = [((0.0, 0.0), 95.35), ((ALT[1], ALT[2]), 38.1), ((FAN[1], FAN[2]), 95.0)]
    pts = []
    order = [0, 1, 2]
    for i in order:
        (cy, cz), r = pul[i]
        (py, pz), _ = pul[order[i - 1]]; (ny, nz), _ = pul[order[(i + 1) % 3]]
        a0 = math.atan2(cz - pz, cy - py) - math.pi / 2; a1 = math.atan2(nz - cz, ny - cy) - math.pi / 2
        while a1 < a0: a1 += 2 * math.pi
        for k in range(14):
            a = a0 + (a1 - a0) * k / 13
            pts.append((BELT_X, cy + math.cos(a) * (r + 3), cz + math.sin(a) * (r + 3)))
    def belt(bm):
        prof = [(-14, -2.5), (14, -2.5), (14, 2.5), (-14, 2.5)]
        P = [Vector(p) for p in pts]
        rings = []
        cen = sum(P, Vector()) / len(P)
        for p in P:
            n = (p - cen); n.x = 0; n.normalize()
            rings.append([bm.verts.new(p + Vector((u, 0, 0)) + n * v) for u, v in prof])
        for r0, r1 in zip(rings, rings[1:] + rings[:1]):
            for k in range(4):
                j = (k + 1) % 4
                bm.faces.new((r0[k], r0[j], r1[j], r1[k]))
    o = part('correa', RUBBER, 'Accesorios', belt); meta(o, 'accesorios', 'Correa poly-V', 'E'); objs.append(o)
    # bomba de agua
    def wp(bm):
        bm_cyl(bm, 80, 80, 70, WP, 'X', 40)
        bm_sweep(bm, [(WP[0], WP[1] - 40, WP[2] - 60), (WP[0] - 20, WP[1] - 120, WP[2] - 90), (WP[0] - 60, WP[1] - 180, WP[2] - 80)], 30, 20)
    o = part('bomba_agua', ALU, 'Refrigeracion', wp, (4, 2)); meta(o, 'refrigeracion', 'Bomba de agua', 'E'); objs.append(o)
    # termostato y salida de agua (cat. pág. 30)
    def th(bm):
        bm_box(bm, 120, 110, 90, (FFOB - 40, -110, HEAD_TOP + 10))
        bm_sweep(bm, [(FFOB - 40, -110, HEAD_TOP + 55), (FFOB + 10, -110, HEAD_TOP + 110), (FFOB + 90, -110, HEAD_TOP + 120)], 32, 20)
    o = part('carcasa_termostato', ALU, 'Refrigeracion', th, (6, 2)); meta(o, 'refrigeracion', 'Carcasa del termostato', 'C'); objs.append(o)
    # soporte delantero (cat. pág. 36): placa con escuadras, apoyo a 206 mm bajo el eje, a 149 mm del FFOB
    def fs(bm):
        bm_prism(bm, [(-260, -206), (260, -206), (260, -186), (150, -60), (-150, -60), (-260, -186)], 18, 'YZ', loc=(FFOB + 95, 0, 0))
        for s in (-1, 1):
            bm_box(bm, 110, 18, 90, (FFOB + 149, s * 230, -196))
            bm_prism(bm, [(0, 0), (90, 0), (0, 110)], 14, 'XZ', loc=(FFOB + 104, s * 150, -186))
    o = part('soporte_delantero', IRON, 'Estructura', fs, (3, 1)); meta(o, 'estructura', 'Soporte delantero (apoyo a 206 mm del eje)', 'C'); objs.append(o)
    # ganchos de izado
    def lift(bm):
        for x, y in ((FFOB - 40, 60), (RFOB + 40, -60)):
            bm_prism(bm, [(-35, 0), (35, 0), (20, 80), (-20, 80)], 18, 'XZ', loc=(x, y, HEAD_TOP + 10))
    o = part('ganchos_izado', IRON, 'Estructura', lift, (3, 1)); meta(o, 'estructura', 'Ganchos de izado', 'C'); objs.append(o)
    return objs

# ================================================================= TUBERÍAS DE COMBUSTIBLE Y ACEITE
def build_lines():
    objs = []
    def fuel(bm):
        bm_sweep(bm, [(-20, 270, 160), (-100, 300, 200), (-200, 320, 240)], 6, 10)
        bm_sweep(bm, [(-250, 300, 320), (-150, 250, 420), (0, 215, DECK + 40), (200, 205, DECK + 40)], 6, 10)
    o = part('tuberia_combustible', STEEL, 'Combustible', fuel); meta(o, 'combustible', 'Tuberías de combustible', 'E'); objs.append(o)
    def turbo_oil(bm):
        tx, ty, tz = TURBO
        bm_sweep(bm, [(tx - 15, ty, tz + 46), (tx - 15, ty + 40, tz + 90), (0, -230, 240), (100, -255, 180)], 5, 10)
        bm_sweep(bm, [(tx - 15, ty, tz - 46), (tx - 10, ty - 20, tz - 140), (tx + 30, -220, 60), (RFOB + 60, -200, -60)], 9, 12)
    o = part('tuberia_aceite_turbo', STEEL, 'Lubricacion', turbo_oil); meta(o, 'lubricacion', 'Alimentación y retorno de aceite del turbo', 'E'); objs.append(o)
    return objs

# ================================================================= CONSTRUCCIÓN
print('Construyendo QSM11…')
build_block(); build_mains(); build_liners()
build_head(); build_rocker_housing(); build_gear_housing(); build_flywheel_housing(); build_oil_pan()
build_crank(); build_damper(); build_flywheel()
for c in range(1, 7):
    p = build_piston(c); p.location = (XC(c), 0, R + LROD)
    r = build_rod(c); r.location = (XC(c), 0, R)
build_camshaft(); build_valvetrain()
build_intake(); build_exhaust(); build_turbo()
build_fuel_side(); build_oil_side(); build_front(); build_lines()

if '_tmp' in COLL:
    for o in list(COLL['_tmp'].objects): bpy.data.objects.remove(o)
    bpy.data.collections.remove(COLL['_tmp'])

# Pose del ciclo en θ = 0 (cilindro 1 en PMS de compresión)
def pose(theta):
    for c in range(1, 7):
        b = math.radians(theta - PHI[c]); s, co = math.sin(b), math.cos(b)
        yP = R * co + math.sqrt(LROD ** 2 - R * R * s * s)
        p = bpy.data.objects[f'piston_{c}']; p.location = (XC(c), 0, yP)
        r = bpy.data.objects[f'biela_{c}']; r.location = (XC(c), R * s, R * co)
        r.rotation_euler = (math.atan2(R * s, yP - R * co), 0, 0)
    for n in ('ciguenal', 'amortiguador_polea', 'volante'):
        bpy.data.objects[n].rotation_euler = (math.radians(-theta), 0, 0)
    bpy.data.objects['arbol_levas'].rotation_euler = (math.radians(-theta / 2), 0, 0)
pose(0)

tris = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
print(f'Objetos: {len([o for o in bpy.data.objects if o.type == "MESH"])}  Polígonos: {tris}')

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'qsm11.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, 'qsm11.glb'), export_format='GLB', export_extras=True,
                          export_apply=True, export_yup=True)
print('Listo:', OUT)
