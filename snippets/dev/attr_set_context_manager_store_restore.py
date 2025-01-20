## context manager to store restore

class attr_set():
    '''Store-set-restore attributes for context manager.
    Receive a list of tuple [(data_path, "attribute" [, new value)] ]
    Entering with-statement : Store current attributes values, assign new value (if provided)
    Exiting with-statement: Restore attributes old values in reverse order
    '''

    def __init__(self, attrib_list):
        self.store = []
        # item = (prop, attr, [new_val])
        for item in attrib_list:
            prop, attr = item[:2]
            self.store.append( (prop, attr, getattr(prop, attr)) )
            if len(item) >= 3:
                setattr(prop, attr, item[2])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for prop, attr, old_val in reversed(self.store):
            setattr(prop, attr, old_val)


## value to store / change
store_list = [
    (bpy.context.scene.render, 'use_simplify', True),
    (bpy.context.scene.render, 'simplify_subdivision', 0),
    ]

with attr_set(store_list):
    print('do something while values are changed')
