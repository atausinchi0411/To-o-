"""Renders de revisión del QSM11.
Uso: python qsm11_render.py [workbench|cycles] [vista1,vista2,...] [explode]
Vistas: iso, iso_rear, iso_ex, front, side_in, side_ex, top
"""
import bpy, math, os, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'salida')
args = [a for a in sys.argv[1:] if not a.endswith('.py')]
engine = args[0] if args else 'workbench'
views = (args[1] if len(args) > 1 else 'iso,iso_rear').split(',')
explode = len(args) > 2 and args[2] == 'explode'

bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT, 'qsm11.blend'))
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = 1600, 1000
sc.render.film_transparent = False

EXPLODE = {'tapa_balancines': (0, 0, 520), 'culata': (0, 0, 330), 'colector_admision': (0, 260, 330), 'colector_escape': (0, -300, 330),
           'juntas_colector': (0, -300, 330), 'carter': (0, 0, -380), 'tapas_bancada': (0, 0, -150), 'ciguenal': (0, 0, -220),
           'amortiguador_polea': (300, 0, -220), 'volante': (-300, 0, -220), 'carcasa_engranajes': (260, 0, 0), 'carcasa_volante': (-300, 0, 0),
           'turbo': (-250, -380, 420), 'rueda_turbina': (-250, -380, 420), 'rueda_compresor': (-250, -380, 420), 'codo_escape': (-250, -380, 420),
           'codo_filtro_aire': (-250, -380, 420), 'conducto_aire': (0, 0, 600), 'arbol_levas': (0, 380, -40), 'ecm': (0, 300, 0),
           'bomba_combustible': (0, 300, 0), 'compresor_aire': (0, 300, 0), 'enfriador_aceite': (0, -300, 0), 'filtros_aceite': (0, -300, 0)}
if explode:
    for o in bpy.data.objects:
        n = o.name
        d = EXPLODE.get(n)
        if d is None:
            if n.startswith(('piston_', 'biela_')): d = (0, 0, 120 if n.startswith('piston') else 40)
            elif n.startswith(('valvulas_', 'muelles_', 'balancin_', 'eje_balancines', 'inyector_')): d = (0, 0, 430)
            elif n.startswith('varilla_'): d = (0, 0, 200)
        if d: o.location += Vector(d)

if engine == 'cycles':
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 48; sc.cycles.use_denoising = True; sc.cycles.device = 'CPU'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.055, 0.065, 0.08, 1); bg.inputs[1].default_value = 0.6
    for name, loc, energy, size in (('key', (2200, 1800, 2600), 9e6, 1500), ('fill', (-2000, -1400, 1200), 3e6, 1800), ('rim', (-1800, 2200, 900), 4e6, 1000)):
        L = bpy.data.lights.new(name, 'AREA'); L.energy = energy; L.size = size
        o = bpy.data.objects.new(name, L); sc.collection.objects.link(o); o.location = loc
        o.rotation_euler = (Vector((0, 0, 200)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    bpy.ops.mesh.primitive_plane_add(size=8000, location=(0, 0, -480))
    fl = bpy.context.object; m = bpy.data.materials.new('suelo'); m.use_nodes = True
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.05, 0.055, 0.065, 1)
    m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.6
    fl.data.materials.append(m)
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
else:
    sc.render.engine = 'BLENDER_WORKBENCH'
    sh = sc.display.shading
    sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'; sh.show_cavity = True; sh.cavity_type = 'BOTH'
    sh.show_shadows = True; sh.shadow_intensity = 0.35; sh.show_specular_highlight = True
    sh.background_type = 'VIEWPORT'; sh.background_color = (0.07, 0.08, 0.1)
    sc.display.render_aa = '8'

cam_d = bpy.data.cameras.new('cam'); cam_d.lens = 50; cam_d.clip_start = 10; cam_d.clip_end = 50000
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
VIEW = {'iso': (2700, 2300, 1900), 'iso_rear': (-2700, -2300, 1900), 'front': (3800, 0, 250), 'side_in': (0, 4200, 300),
        'side_ex': (0, -4200, 300), 'top': (1, 0, 4500), 'iso_ex': (2700, -2300, 1900)}
target = Vector((0, 0, 230 if not explode else 330))
for v in views:
    if v not in VIEW: continue
    pos = Vector(VIEW[v]) * (0.95 if explode else 0.78)
    cam.location = pos
    cam.rotation_euler = (target - pos).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, f'render_{v}{"_explode" if explode else ""}_{engine}.png')
    bpy.ops.render.render(write_still=True)
    print('render', sc.render.filepath)
