## Get collection, create if necessary
def get_col(self, name, parent=None, create=True):
    parent = parent or bpy.context.scene.collection
    col = bpy.data.collections.get(name)
    if not col and create:
        col = bpy.data.collections.new(name)

    if col not in parent.children[:]:
        parent.children.link(col)

    return col
