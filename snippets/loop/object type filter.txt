['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE', 'EMPTY', 'CAMERA', 'LIGHT_PROBE', 'LIGHT' 'SPEAKER']
for ob in bpy.context.scene.objects:
    if ob.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
        print(ob.name, 'is a renderable object')