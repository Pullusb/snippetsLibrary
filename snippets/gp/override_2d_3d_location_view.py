from bpy_extras import view3d_utils

def get_3d_area():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                return area

area = get_3d_area()

def location_to_region(worldcoords):
    return view3d_utils.location_3d_to_region_2d(area.regions[5], area.spaces[0].region_3d, worldcoords)

def region_to_location(viewcoords, depthcoords):
    return view3d_utils.region_2d_to_location_3d(area.regions[5], area.spaces[0].region_3d, viewcoords, depthcoords)


ob = C.object
coords2d = [location_to_region(ob.matrix_world @ p.co) for p in ob.data.layers.active.active_frame.strokes[-1].points]
middle = (coords2d[0] + coords2d[1]) / 2
mid3d = region_to_location(middle, ob.data.layers.active.active_frame.strokes[-1].points[0].co)
print("mid3d", mid3d)


# list 2d coords in console
#from bpy_extras import view3d_utils
#[view3d_utils.location_3d_to_region_2d(C.window.screen.areas[5].regions[5], C.window.screen.areas[5].spaces[0].region_3d, C.object.matrix_world @ p.co) for p in C.object.data.layers.active.active_frame.strokes[-1].points]


## extreme exemple for console:    
# mean2d = view3d_utils.region_2d_to_location_3d(C.window.screen.areas[5].regions[5], C.window.screen.areas[5].spaces[0].region_3d, np.mean([view3d_utils.location_3d_to_region_2d(C.window.screen.areas[5].regions[5], C.window.screen.areas[5].spaces[0].region_3d, C.object.matrix_world @ p.co) for p in C.object.data.layers.active.active_frame.strokes[-1].points], axis=0), Vector((0,0,0)) )