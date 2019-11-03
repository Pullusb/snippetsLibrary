def get_parent_collection_names(collection, parent_names):
  for parent_collection in bpy.data.collections:
    if collection.name in parent_collection.children.keys():
      parent_names.append(parent_collection.name)
      get_parent_collection_names(parent_collection, parent_names)
      return


def turn_collection_hierarchy_into_path(obj):
  parent_collection = obj.users_collection[0]
  parent_names      = []
  parent_names.append(parent_collection.name)
  get_parent_collection_names(parent_collection, parent_names)
  parent_names.reverse()
  return '\\'.join(parent_names)


obj = bpy.context.view_layer.objects.active
print(turn_collection_hierarchy_into_path(obj))