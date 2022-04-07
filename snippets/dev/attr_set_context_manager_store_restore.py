## context manager to store restore

class attr_set():
    '''Receive a list of tuple [(data_path:python_obj, "attribute":str, "wanted value":str)]
    before with statement : Store existing values, assign wanted value 
    after with statement: Restore values to their old values
    '''

    def __init__(self, attrib_list):
        self.store = []
        for prop, attr, new_val in attrib_list:
            self.store.append( (prop, attr, getattr(prop, attr)) )
            # if new_val == '_undefined':
            #     # set new_val to '_undefined' if need to store / restore only
            #     continue
            setattr(prop, attr, new_val)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for prop, attr, old_val in self.store:
            setattr(prop, attr, old_val)


## value to store / change
store_list = [
    (bpy.context.scene.render, 'use_simplify', True),
    (bpy.context.scene.render, 'simplify_subdivision', 0),
    ]

with attr_set(store_list):
    print('do something while values are changed')
