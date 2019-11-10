def render(fp, animation=False, write_still=True, view_context=False):
    scn = bpy.context.scene
    org = scn.render.filepath

    scn.render.filepath = fp
    ## openGl render
    # bpy.ops.render.opengl(animation=animation, write_still=True, view_context=view_context)#view_context False > look throughcam

    ## normal render
    bpy.ops.render.render(animation=animation, write_still=write_still)

    #restore
    scn.render.filepath = org


org_cam = bpy.context.scene.camera

for cam in [o for o in D.objects if o.type == 'CAMERA']:
    bpy.context.scene.camera = cam
    #Strip name prefix
    name = cam.name
    if name.lower().startswith('camera_'): name = name[len('camera_'):]
    if name.lower().startswith('cam_'): name = name[len('cam_'):]

    filepath = f'//{name}_{bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}'
    render(filepath)

bpy.context.scene.camera = org_cam