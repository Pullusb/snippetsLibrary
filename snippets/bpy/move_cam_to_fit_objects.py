import bpy
from mathutils import Vector
from math import pi

scn = bpy.context.scene


## Create a new three-quarter diving camera and make it active
cam_data = bpy.data.cameras.new('Cam')
cam = bpy.data.objects.new('Cam', cam_data)
cam.rotation_euler.x = pi / 3
cam.rotation_euler.z = pi / 4
bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam

## Or use existing camera
# cam = scn.camera

## for preview, make the resolution a square
scn.render.resolution_x = scn.render.resolution_y = 1000

## --- Method OPS: precisely fit objects, (not working on armatures)

## Make camera move to frame selected objects
def cam_view_selection(cam = bpy.context.scene.camera):
    '''Move given camera to frame selected objects with Ops viewSelect method'''
    #set active camera
    bpy.context.scene.camera = cam
    #view selected
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            ctx = bpy.context.copy()
            ctx['area'] = area
            ctx['region'] = area.regions[-1]
            #bpy.ops.view3d.view_selected(ctx)            # points view
            bpy.ops.view3d.camera_to_view_selected(ctx)   # points camera

# frame_object
cam_data.lens += 5 # back to original lens after to add a margin
bpy.ops.object.select_all(action='SELECT') # frame everything
cam_view_selection(cam=cam)
cam_data.lens -= 5

## also possible to physically move camera back intead of 
# up = Vector((0,0,1))
# up.rotate(cam.matrix_world)
# cam.location += up * 0.2


## --- Method Cam fitting: worlks with armatures, but less precise (fit on bounding box)

def cam_fit(camera, coords):
    '''get a flatenned list of 3d coords'''
    depsgraph = bpy.context.evaluated_depsgraph_get()
    camera.location, _foo = camera.camera_fit_coords(depsgraph, coords)

scn = bpy.context.scene
# scope = scn.objects # all objects
scope = bpy.context.selected_objects # selection

ob_list = [o for o in scope if o.type not in ('ARMATURE', 'CAMERA', 'LIGHT', 'SPEAKER', 'EMPTY')]
armatures = [o for o in scope if o.type == 'ARMATURE']
arma_coords = [(ob.matrix_world @ b.matrix).to_translation() for ob in armatures for b in ob.pose.bones]

coords = arma_coords + [ob.matrix_world @ Vector(co) for ob in ob_list for co in ob.bound_box[:]]
flatten_coords = [elem for v in coords for elem in v]

cam = scn.camera
cam.data.lens += 3 # margin hack
cam_fit(cam, flatten_coords)
cam.data.lens -= 3 # margin hack
