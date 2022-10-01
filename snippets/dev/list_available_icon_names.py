## List available UI icons in current version of Blender
icon_list = [i for i in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys() if i != 'NONE']
