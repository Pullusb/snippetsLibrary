## Create 2D gyzmo button, similar to native view navigation gyzmos

import bpy
from mathutils import Matrix
from bpy.types import (
    Operator,
    GizmoGroup,
    # Gizmo
    )


class VIEW_OT_camera_lock_toggle(Operator):
    bl_idname = "view.camera_lock_toggle"
    bl_label = 'Lock Camera To View'
    bl_description = "Toggle camera lock to view in active viewport"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        sd = context.space_data
        sd.lock_camera = not sd.lock_camera
        return {"FINISHED"}

class CAMERA_GGT_gyzmos_view_buttons(GizmoGroup):
    bl_idname = "camera.gyzmos_view_buttons"
    bl_label = "Gyzmos Cam Display"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    @classmethod
    def poll(cls, context):
        return context.space_data.region_3d.view_perspective == 'CAMERA'

    icon_size = 25

    def setup(self, context):

        gz = self.gizmos.new("GIZMO_GT_button_2d")
        gz.icon = 'LOCKVIEW_ON'
        gz.color_highlight = (0.5, 0.5, 0.5) # default 0.5
        gz.alpha = 0.5
        gz.alpha_highlight = 0.1
        gz.show_drag = False
        gz.draw_options = {'BACKDROP', 'OUTLINE'}
        gz.scale_basis = 14
        _props = gz.target_set_operator("view.camera_lock_toggle")

        self.gz_lock_cam = gz

    def draw_prepare(self, context):
        region = context.region
        # Adapt to UI scale
        ui_scale = context.preferences.view.ui_scale
        # center
        self.gz_lock_cam.matrix_basis = Matrix.Translation(
            (region.width / 2 - self.icon_size, self.icon_size + 2 * ui_scale, 0))

        ## Changing Icon dynamically does not work
        # self.gz_lock_cam.icon = 'LOCKVIEW_ON' if context.space_data.lock_camera else 'LOCKVIEW_OFF'

        ## Change color according to state
        self.gz_lock_cam.color = (0.4, 0.0,0.0) if context.space_data.lock_camera else (0.0, 0.0, 0.0)
        self.gz_lock_cam.color_highlight = (1.0, 0.5, 0.5) if context.space_data.lock_camera else (0.5, 0.5, 0.5)


if __name__ == "__main__":
    bpy.utils.register_class(VIEW_OT_camera_lock_toggle)
    bpy.utils.register_class(CAMERA_GGT_gyzmos_view_buttons)
