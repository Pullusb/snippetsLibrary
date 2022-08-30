## Render all visible layers of selected grease pencil objects individually

import bpy

class attr_set():
    '''Receive a list of tuple [(data_path, "attribute" [, wanted value)] ]
    entering with-statement : Store existing values, assign wanted value (if any)
    exiting with-statement: Restore values to their old values
    '''

    def __init__(self, attrib_list):
        self.store = []
        # item = (prop, attr, [new_val])

        ## set passed attrib list
        for item in attrib_list:
            prop, attr = item[:2]
            self.store.append( (prop, attr, getattr(prop, attr)) )
            if len(item) >= 3:
                setattr(prop, attr, item[2])

        ## store state of all gp layers of all gp object
        for o in bpy.context.scene.objects:
            if o.type == 'GPENCIL':
                for l in o.data.layers:
                    self.store.append( (l, 'hide', l.hide) )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for prop, attr, old_val in self.store:
            setattr(prop, attr, old_val)


def hide_layers(ob, hide=True):
    for l in ob.data.layers:
        l.hide = hide


## set/store other data
store_list = [
    # (bpy.context.scene.render, 'simplify_subdivision', 0),
    (bpy.context.scene.render, 'filepath'),
    ]

add_obj_name = False

to_render = []
with attr_set(store_list):
    ## store renderable and hide all loop
    for ob in bpy.context.scene.objects:
         if ob.type == 'GPENCIL':
             for l in ob.data.layers:
                 if not l.hide:
                     # only visibles stored
                     to_render.append(l)

                     l.hide = True

    ## render loop
    for ob in bpy.context.selected_objects:
        if ob.type != 'GPENCIL':
            continue
        for i, l in enumerate(ob.data.layers):
            hide_layers(ob)
            if l in to_render:
                l.hide=False
                if add_obj_name:
                    file_name = f'{ob.name}_{i:02d}_{l.info}'
                else:
                    file_name = f'{i:02d}_{l.info}'
                bpy.context.scene.render.filepath = f'//princess_frime/{file_name}'
                bpy.ops.render.render(write_still=True)
