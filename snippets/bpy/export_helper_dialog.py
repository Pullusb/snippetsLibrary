## Operator dialog with or without Export helper class

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

## Test
# bpy.utils.register_class(MYADDON_OT_export_things)
# bpy.ops.myaddon.export_things('INVOKE_DEFAULT')

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

## Test
# bpy.utils.register_class(MYADDON_OT_export_things_in_directory)
# bpy.ops.myaddon.export_things_in_directory('INVOKE_DEFAULT')

## Defining only directory gets a directory picker:

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

## Test
# bpy.utils.register_class(IMPORT_OT_my_folder_manual)
# bpy.ops.import_test.folder_manual('INVOKE_DEFAULT')

## Full Class with all available 

# filepath — full path to the selected file (subtype='FILE_PATH')
# filename — just the file name portion
# directory — the directory path (subtype='DIR_PATH')
# files — a CollectionProperty of selected files (for multi-select)
# filter_glob — extension filter, e.g. "*.png;*.jpg" (typically options={'HIDDEN'})

import bpy
from bpy.props import StringProperty, CollectionProperty

class IMPORT_OT_my_file_full(bpy.types.Operator):
    """Import files with all fileselect properties"""
    bl_idname = "import_test.file_full"
    bl_label = "Import Files"

    filepath: StringProperty(
        name="File Path",
        description="Full path to the selected file",
        subtype='FILE_PATH',
    )

    filename: StringProperty(
        name="File Name",
        description="Name of the selected file",
    )

    directory: StringProperty(
        name="Directory",
        description="Directory of the selected file",
        subtype='DIR_PATH',
    )

    files: CollectionProperty(
        name="Files",
        description="All selected files (multi-select)",
        type=bpy.types.OperatorFileListElement,
    )

    filter_glob: StringProperty(
        default="*.png;*.jpg;*.exr",
        description="Extension filter",
        options={'HIDDEN'},
        maxlen=255,
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        import os

        print(f"filepath:  {self.filepath}")
        print(f"filename:  {self.filename}")
        print(f"directory: {self.directory}")

        # Iterate multi-selected files
        for f in self.files:
            full_path = os.path.join(self.directory, f.name)
            print(f"  file: {full_path}")

        return {'FINISHED'}

## Test
# bpy.utils.register_class(IMPORT_OT_my_file_full)
# bpy.ops.import_test.file_full('INVOKE_DEFAULT')