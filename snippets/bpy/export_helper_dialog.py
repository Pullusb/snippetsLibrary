## Operator disalog with or without Export helper class

class MYADDON_OT_export_things(bpy.types.Operator, ExportHelper):
    bl_idname = "myaddon.export_things"
    bl_label = "Export Things"
    bl_description = "Export the things"
    bl_options = {"REGISTER"}

    # filter_glob: bpy.props.StringProperty(default='*.txt;*.json;', options={'HIDDEN'})# *.jpeg;*.png;*.tif;*.tiff;*.bmp
    filter_glob: bpy.props.StringProperty(default='*.*', options={'HIDDEN'})

    filename_ext = ''

    filepath : bpy.props.StringProperty(
        name="File Path",
        description="File path used for export", 
        maxlen= 1024)

    all_objects : bpy.props.BoolProperty(
        name='All Objects',
        default=False,
        description='Use all objects to export things')

    ## Possible to do things in invoke while keeping invoke from export helper
    # def invoke(self, context, event):
    #     if event.ctrl:
    #         print('copy individual') # or separate operators
    #
    #         return {'FINISHED'}
    #     return super().invoke(context, event)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        # Are we inside the File browser
        is_file_browser = context.space_data.type == 'FILE_BROWSER'

        layout.prop(self, 'all_objects')

    def execute(self, context):
        # Export the thing
        if self.all_objects:
            # Or export all the thing
            pass

        self.report({'INFO'}, f'File saved at: {self.filepath}')
        return {"FINISHED"}


## Export to a Directory (use with your own draw and execute function)
from pathlib import Path

class MYADDON_OT_export_things_in_directory(bpy.types.Operator):
    bl_idname = "myaddon.export_things_in_directory"
    bl_label = "Export In Directory"
    bl_description = "Export the things"
    bl_options = {"REGISTER"}

    directory : bpy.props.StringProperty(
        name="File Path",
        description="File path used for export", 
        maxlen= 1024,
        subtype='DIR_PATH'
    )

    ## Similar invoke to export helper (in file "scripts/modules/bpy_extras/io_utils.py")
    ## /!\ No check method implemented here
    def invoke(self, context, _event):
        if not self.directory:
            blend_filepath = context.blend_data.filepath
            if blend_filepath:
                dest_folder = Path(blend_filepath).parent
                self.directory = str(dest_folder)

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

## Most Barebone version (select a directory to do something):

class IMPORT_OT_my_folder_manual(bpy.types.Operator):
    """Import from a folder (no ImportHelper)"""
    bl_idname = "import_test.folder_manual"
    bl_label = "Import Folder"

    directory: bpy.props.StringProperty(
        name="Directory",
        subtype='DIR_PATH',
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        print(f"Selected directory: {self.directory}")
        return {'FINISHED'}
