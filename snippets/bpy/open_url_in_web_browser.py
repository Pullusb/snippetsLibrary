## methods to open urls
## directly as a button in panel
layout.operator("wm.url_open", text="to blender").url = "https://www.blender.org/"
## as an operator to call within code
bpy.ops.wm.url_open(url="https://www.blender.org/")