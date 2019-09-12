for ob in bpy.context.scene.objects:
    if 'sauce' in ob.name:
        ob.select_set(True)