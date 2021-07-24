import bpy
scenes = bpy.data.scenes
n = len(scenes)
assert n > 1, 'Only one scene, no switch possible'
slist = [s.name for s in scenes]
bpy.context.window.scene = scenes[(slist.index(bpy.context.scene.name) + 1) % n]