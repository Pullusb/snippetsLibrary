## Build all properties code (incomplete)

import bpy

rd = bpy.context.scene.render

strings = ''
for prop in rd.ffmpeg.bl_rna.properties:
    t = str(type(prop))
    g = re.search(r'types\.(.+Property)', t)

    if not g or g.group(1) == 'PointerProperty':
        continue
    prop_type = g.group(1) if g else 'NOPROP'

    default = f"'{prop.default}'" if prop_type in ('StringProperty', 'EnumProperty') else prop.default

    string = f'''
    {prop.identifier} : {prop_type}(
        name='{prop.name}',
        default={default},
        description='{prop.description}',
        )
    '''

    strings += string
    print(string)
    ## for val prop : prop.bl_rna.properties['default_array'].soft_min

bpy.context.window_manager.clipboard = strings