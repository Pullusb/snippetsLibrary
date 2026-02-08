## Explore context by appending function to some menus

import bpy

## Debug function to print available context
def draw_my_menu_item_debug(self, context):
    print('\n--- context ---')
    for attr in dir(context):
        if not attr.startswith("_"):
            try:
                val = getattr(context, attr)
                if not callable(val):
                    print(f"{attr}: {val}")
            except:
                pass

## Debug function to print details of active ID in context (usefull)
def draw_id_details(self, context):
    if not getattr(context, 'id'):
        print('!! No ID in context') # Dbg
        return
    print('---\nID details:')
    
    ## id (active datablock in current context)
    id = context.id

    ## same as: type(id).__name__ 
    id_type = id.bl_rna.name

    print('id: ', id)
    print(f"Clicked: {id.name}")
    print('id_type: ', id_type)
    print(f"Type: {id_type}")
    print(dir(id))

    ## Possibly Filter action by type
    # if id_type.lower() not in ('library',):
    #     return
    
    # print(f"Path: {id.filepath}") # Dbg

    ## possible tests on id
    # if id.is_library_indirect:
    #     print("Indirect linked data-block")
    # elif id.is_embedded_data:
    #     print("Embedded data-block")
    # else:
    #     print("Linked data-block")

    ## adding ops in menu
    # self.layout.operator("my.operator", text=f"Do something with {id.name}")

## Example of usage, here appending to the Outliner context menu
def register():
    bpy.types.OUTLINER_MT_context_menu.append(draw_my_menu_item_debug)
    bpy.types.OUTLINER_MT_context_menu.append(draw_id_details)

def unregister():
    bpy.types.OUTLINER_MT_context_menu.remove(draw_id_details)
    bpy.types.OUTLINER_MT_context_menu.remove(draw_my_menu_item_debug)