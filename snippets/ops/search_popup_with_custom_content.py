## Populate a custom search popup 
## e.g : list other blend file in the same folder
import bpy
import os
from os.path import join, dirname, basename, exists, isfile

def get_blend_list(self, context):
    '''return (identifier, name, description) of enum content'''
    return [(i.path, basename(i.path), "") for i in os.scandir(self.bl_path) if i.name.endswith('.blend')]


class TEST_OT_blend_pick(bpy.types.Operator) :
    bl_idname = "explorer.pick_a_blend"
    bl_label = 'Scan And Pick A Blend'
    # important to have the updated enum here as bl_property
    bl_property = "blend_file_enum"

    # all : bpy.props.BoolProperty(default=False)
    bl_path : bpy.props.StringProperty(default='', options={'SKIP_SAVE'}) # # need to have a variable to store (to get it in self)
    blend_file_enum : bpy.props.EnumProperty(
        name="Blends",
        description="Take the blend",
        items=get_blend_list
        )

    def execute(self, context):
        blend = self.blend_file_enum
        print('Selected :', blend)
        # if self.all:
        #     pass
        return {'FINISHED'}

    def invoke(self, context, event):
        # if not bpy.data.is_saved:
        #     self.report({'ERROR'}, 'File must be saved')
        #     return {'CANCELLED'}

        if not self.bl_path:
            self.bl_path = dirname(bpy.data.filepath)

        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}

## Direct Test
#bpy.utils.register_class(TEST_OT_blend_pick)
#bpy.ops.explorer.pick_a_blend('INVOKE_DEFAULT')