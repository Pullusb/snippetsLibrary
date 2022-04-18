## Move a collection or an object to a collection
def move_to_collection(self, obj, collection):
    if isinstance(obj, bpy.types.Collection):
        parent_to = collection.children
        parent_from = self.get_col_parents(obj)

        for col in parent_from:
            col.children.unlink(obj)

    elif isinstance(obj, bpy.types.Object):
        parent_to = collection.objects
        for col in obj.users_collection:
            col.objects.unlink(obj)

    else:
        print('Object must be in type ("Object", "Collection")')
        return

    parent_to.link(obj)
