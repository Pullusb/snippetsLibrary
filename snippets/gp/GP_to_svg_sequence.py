### Export All frames of selected layer as svg.

## Write an ouput name (folder and image will use this name)
## if left empty, will use name of active object with 'svg_' prefix
name = ''
only_frames = 1 # put 0 to export whole frame range
## ----

import bpy
from pathlib import Path

o = bpy.context.object
assert o.type == 'GPENCIL', 'Active object should be GP'

if only_frames:
    frames = []
    for ob in bpy.context.selected_objects:
        if ob.type != 'GPENCIL':
            continue
        frames += [f.frame_number for l in ob.data.layers if not l.hide for f in l.frames if len(f.strokes)]
    
    if frames:
        frames = sorted(list(set(frames)))
else:
    frames = [f for f in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1)]

print(len(frames), 'frames to export')
pass_name = name if name else f'svg_{o.name}'


blend = Path(bpy.data.filepath)

for fnum in frames:
    out = f'{pass_name}_{fnum:04d}.svg'
    print(out)
    folder = blend.parent / 'render' / pass_name
    folder.mkdir(parents=True, exist_ok=True)

    fp =  folder / out
    if fp.exists():
        print(f'  already exists: {fp}')
        continue
    
    bpy.context.scene.frame_current = fnum
    bpy.ops.wm.gpencil_export_svg(filepath=str(fp),
    check_existing=True,
    use_fill=True, selected_object_type='SELECTED', # ACTIVE, VISIBLE
    stroke_sample=0.0,
    use_normalized_thickness=False,
    use_clip_camera=True) # False by defaut

print('Done')

### Export operator parameters description
# use_fill (boolean, (optional)) – Fill, Export strokes with fill enabled

# selected_object_type (enum in ['ACTIVE', 'SELECTED', 'VISIBLE'], (optional)) –

# Object, Which objects to include in the export
#     ACTIVE Active, Include only the active object.
#     SELECTED Selected, Include selected objects.
#     VISIBLE Visible, Include all visible objects.
# 
# stroke_sample (float in [0, 100], (optional)) – Sampling, Precision of stroke sampling. Low values mean a more precise result, and zero disables sampling

# use_normalized_thickness (boolean, (optional)) – Normalize, Export strokes with constant thickness

# use_clip_camera (boolean, (optional)) – Clip Camera, Clip drawings to camera size when export in camera view