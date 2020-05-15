### --- REGISTER ---

## quick register shortcut 
# register, unregister = bpy.utils.register_classes_factory(classes)

# classic method
classes = (
MYOPS_OT_my_super_operator,
MYPANEL_PT_my_turbo_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()