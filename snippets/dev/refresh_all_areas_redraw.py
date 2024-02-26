## Refresh interface on all areas

import bpy

def refresh_areas():
    for area in bpy.context.screen.areas:
        area.tag_redraw()
