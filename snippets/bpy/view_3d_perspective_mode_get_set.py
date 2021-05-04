## access view 3D perspective setting
# eg: set camera view in active VIEW_3D
context.region_data.view_perspective = 'CAMERA' # 'PERSP', 'ORTHO'

# console access through area.spaces
bpy.context.screen.areas[3].spaces[0].region_3d.view_perspective