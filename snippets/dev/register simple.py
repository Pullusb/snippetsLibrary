### --- REGISTER ---

register, unregister = bpy.utils.register_classes_factory(classes)

'''#detailed
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
'''

if __name__ == "__main__":
    register()