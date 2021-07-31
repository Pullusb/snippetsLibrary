## Remove gp vertex colors on selected strokes of active layer > frame
import bpy
for s in bpy.context.object.data.layers.active.active_frame.strokes:
    if not s.select:
        continue
    for p in s.points:
         p.vertex_color[3] = 0 # (0,0,0,0)

## Remove gp vertex colors on everything : (every layer > frame > strokes of active object object !)
import bpy
for l in bpy.context.object.data.layers:
    for f in l.frames:
        for s in f.strokes:
            for p in s.points:
                p.vertex_color[3] = 0 # (0,0,0,0)
