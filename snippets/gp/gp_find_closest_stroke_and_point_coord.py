import bpy
from bpy.types import Operator
import mathutils
from mathutils import Vector, Matrix, geometry
from bpy_extras import view3d_utils

## find closest Grease pencil point coordinate and stroke it belongs to

def location_to_region(worldcoords):
    ''' return 2d location '''
    return view3d_utils.location_3d_to_region_2d(bpy.context.region, bpy.context.space_data.region_3d, worldcoords)

def region_to_location(viewcoords, depthcoords):
    ''' return normalized 3d vector '''
    return view3d_utils.region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, viewcoords, depthcoords)

def get_gp_draw_plane(context):
    ''' return tuple with plane coordinate and normal
    of the curent drawing according to geometry'''

    settings = context.scene.tool_settings
    orient = settings.gpencil_sculpt.lock_axis # 'VIEW', 'AXIS_Y', 'AXIS_X', 'AXIS_Z', 'CURSOR'
    loc = settings.gpencil_stroke_placement_view3d # 'ORIGIN', 'CURSOR', 'SURFACE', 'STROKE'
    mat = context.object.matrix_world if context.object else None

    # -> placement
    if loc == "CURSOR":
        plane_co = context.scene.cursor.location
    else: # ORIGIN (also on origin if set to 'SURFACE', 'STROKE')
        if not context.object:
            plane_co = None
        else:
            plane_co = context.object.matrix_world.to_translation()# context.object.location

    # -> orientation
    if orient == 'VIEW':
        plane_no = context.space_data.region_3d.view_rotation @ Vector((0,0,1))
        ## create vector, then rotate by view quaternion
        # plane_no = Vector((0,0,1))
        # plane_no.rotate(context.space_data.region_3d.view_rotation)

        ## only depth is important, can return None so region to location use same depth
        # plane_no = None

    elif orient == 'AXIS_Y': # front (X-Z)
        plane_no = Vector((0,1,0))
        plane_no.rotate(mat)

    elif orient == 'AXIS_X': # side (Y-Z)
        plane_no = Vector((1,0,0))
        plane_no.rotate(mat)

    elif orient == 'AXIS_Z': # top (X-Y)
        plane_no = Vector((0,0,1))
        plane_no.rotate(mat)

    elif orient == 'CURSOR':
        plane_no = Vector((0,0,1))
        plane_no.rotate(context.scene.cursor.matrix)

    return plane_co, plane_no

### passing by 2D projection
def get_3d_coord_on_drawing_plane_from_2d(context, co):
    plane_co, plane_no = get_gp_draw_plane(context)
    rv3d = context.region_data
    view_mat = rv3d.view_matrix.inverted()
    depth_3d = view_mat @ Vector((0, 0, -1000))
    org = region_to_location(co, view_mat.to_translation())
    view_point = region_to_location(co, depth_3d)
    hit = geometry.intersect_line_plane(org, view_point, plane_co, plane_no)

    if hit and plane_no:
        return context.object, hit, plane_no

    return None, None, None

class GP_OT_get_closest_stroke(Operator):
    """Get closest stroke"""
    bl_idname = "gp.get_close_stroke"
    bl_label = "Get Closest Stroke"
    # bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'GPENCIL' and context.mode == 'PAINT_GPENCIL'

    def filter_stroke(self, context):
        # get stroke under mouse using kdtree
        point_pair = [(p.co, s) for s in self.stroke_list for p in s.points] # local space

        kd = mathutils.kdtree.KDTree(len(point_pair))
        for i, pair in enumerate(point_pair):
            kd.insert(pair[0], i)
        kd.balance()

        ## Get 3D coordinate on drawing plane according to mouse 2d.co on flat 2d drawing
        _ob, hit, _plane_no = get_3d_coord_on_drawing_plane_from_2d(context, self.init_mouse)
        
        mouse_3d = hit
        mouse_local = self.inv_mat @ mouse_3d # local space
        co, index, _dist = kd.find(mouse_local) # local space
        # co, index, _dist = kd.find(mouse_3d) # world space
        context.scene.cursor.location = co # world space
        s = point_pair[index][1]
        
        ## find point index in stroke
        self.idx = None
        for i, p in enumerate(s.points):
            if p.co == co:
                self.idx = i
                break

        del point_pair
        return s, self.ob.matrix_world @ co

    def invoke(self, context, event):
        # self.prefs = get_addon_prefs()
        self.ob = context.object
        self.gp = self.ob.data

        self.stroke_list = []
        self.inv_mat = self.ob.matrix_world.inverted()

        if self.gp.use_multiedit:
            for l in self.gp.layers:
                if l.lock or l.hide:
                    continue
                for f in l.frames:
                    if not f.select:
                        continue
                    for s in f.strokes:
                        self.stroke_list.append(s)

        else:
            # [s for l in self.gp.layers if not l.lock and not l.hide for s in l.active_frame.stokes]
            for l in self.gp.layers:
                if l.lock or l.hide or not l.active_frame:
                    continue
                for s in l.active_frame.strokes:
                    self.stroke_list.append(s)
        
        self.init_mouse = Vector((event.mouse_region_x, event.mouse_region_y))
        self.stroke, self.coord = self.filter_stroke(context)
        
        del self.stroke_list

        if self.idx is None:
            self.report({'WARNING'}, 'No coord found')
            return {'CANCELLED'}
        
        self.depth = self.ob.matrix_world @ self.stroke.points[self.idx].co
        self.init_pos = [p.co.copy() for p in self.stroke.points] # need a copy otherwise vector is updated
        ## directly use world position ?
        # self.pos_world = [self.ob.matrix_world @ co for co in self.init_pos]
        self.pos_2d = [location_to_region(self.ob.matrix_world @ co) for co in self.init_pos]
        self.plen = len(self.stroke.points)

        # context.scene.cursor.location = self.coord #Dbg
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':   
            mouse = Vector((event.mouse_region_x, event.mouse_region_y))
            delta = mouse - self.init_mouse

        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            print(f'{self.stroke}, points num {len(self.stroke.points)}, material index:{self.stroke.material_index}')
            return {'FINISHED'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            # for i, p in enumerate(self.stroke.points): # reset position
            #     self.stroke.points[i].co = self.init_pos[i]
            context.area.tag_redraw()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}


addon_keymaps = []
def register_keymaps():
    addon = bpy.context.window_manager.keyconfigs.addon
    # km = addon.keymaps.new(name = "Grease Pencil Stroke Paint (Draw brush)", space_type = "EMPTY", region_type='WINDOW')
    km = addon.keymaps.new(name = "Grease Pencil Stroke Paint Mode", space_type = "EMPTY", region_type='WINDOW')
    kmi = km.keymap_items.new(
        # name="",
        idname="gp.get_close_stroke",
        type="LEFTMOUSE",
        value="PRESS",
        shift=False,
        ctrl=False,
        alt = False,
        oskey=False,
        key_modifier='A',
        )
    # kmi = km.keymap_items.new('catname.opsname', type='F5', value='PRESS')
    addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


classes=(
GP_OT_get_closest_stroke,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_keymaps()


def unregister():
    unregister_keymaps()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
