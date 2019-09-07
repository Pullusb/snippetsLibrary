import bpy

class TESTOPS_OT_operator_with_variable(bpy.types.Operator):
    bl_idname = "my_operator.multi_op"
    bl_label = "Test operator multiple"
    bl_description = ""
    bl_options = {"REGISTER"}

    left : bpy.props.FloatProperty()

    def execute(self, context):
        ## do things here, use variable with self, (self.left)
        #function_call(self.left)

        return {"FINISHED"}


class TESTOPS_OT_classic_operator(bpy.types.Operator):
    bl_idname = "my_operator.test_op"
    bl_label = "Test operator"
    bl_description = "test operator"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #the code to execute
        return {"FINISHED"}


class TESTOPS_PT_test_panel(bpy.types.Panel):
    bl_idname = "test_operator"
    bl_label = "Test Operator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "test_tab"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True#send properties to the right side
        # flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        layout.operator('my_operator.test_op')
        row = layout.row(align=False)
        #row = layout.split(align=True,percentage=0.5)
        row.label(text='arrow choice')
        row.operator("my_operator.multi_op", text='', icon='TRIA_LEFT').left = 1
        row.operator("my_operator.multi_op", text='', icon='TRIA_RIGHT').left = 0

classes = (
    TESTOPS_OT_operator_with_variable,
    TESTOPS_OT_classic_operator,
    TESTOPS_PT_test_panel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()