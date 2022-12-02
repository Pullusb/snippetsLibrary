## Detect selection changes, detect if active object has changed.

import bpy

## --- msg_bus method

owner = object()
subscribe_to = (bpy.types.LayerObjects, 'active')

def msgbus_callback(*args):
    print("Active object is changed!", args)

bpy.msgbus.subscribe_rna(
    key=subscribe_to,
    owner=owner,
    args=(1, 2, 3),
    notify=msgbus_callback,
)


## --- depsgrah update method

# Current active object in global scope
current_active_object = bpy.context.view_layer.objects.active

def active_object_changed(self, context):
    global current_active_object

    if 'invalid' in str(current_active_object):
        # TODO: need proper method. Dirty check for deleted reference object...
        current_active_object = context.view_layer.objects.active
        return

    # Get the new active object
    new_active_object = context.view_layer.objects.active
    if not new_active_object:
        return

    # Check if the active object has changed
    if current_active_object != new_active_object:
        # Do something
        print(f'New active object: {new_active_object.name}')
        current_active_object = new_active_object

bpy.app.handlers.depsgraph_update_post.append(active_object_changed)
