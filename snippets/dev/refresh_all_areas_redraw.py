## Refresh interface on all areas
def refresh_viewports():
    for area in bpy.context.screen.areas:
        area.tag_redraw()
