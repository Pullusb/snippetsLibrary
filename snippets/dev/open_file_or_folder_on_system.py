## built-in ops to open file or folder in OS
# Operator call in script
bpy.ops.wm.path_open(filepath="path/to/open")

# Direct use in panel/menu entry
layout.operator("wm.path_open", text='Open stuff', icon='FILE_FOLDER').filepath = 'path/to/open'