## context manager to store [set] restore attributes values

class attr_set():
    '''Store-set-restore attributes for context manager.
    Receive a list of tuple:
        [(data_path, "attribute" [, new value]), ...]
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
import bpy
store_list = [
    (bpy.context.scene.render, 'use_simplify', True),
    (bpy.context.scene.render, 'simplify_subdivision', 0),
    ]

with attr_set(store_list):
    print('do something while values are changed')


## More complex version that also handles passing get/set methods:
## e.g: [(obj, ('select_get', 'select_set'), True)]
## or : [(obj, (obj.select_get, obj.select_set), True)]

class attr_set():
    '''Flexible context manager for attribute handling
    
    Args:
        attrib_list: List of tuples in one of these formats:
            [(target, "attribute" [, new_value])]  # Uses getattr/setattr
            [(target, ("get_method", "set_method") [, new_value])]  # Uses named methods
            [(target, (getter_func, setter_func) [, new_value])]  # Uses callable objects
    '''
    
    def __init__(self, attrib_list):
        self.store = []
        for item in attrib_list:
            target, accessor = item[:2]
            
            # Create bound methods to ensure we keep the correct object reference
            if isinstance(accessor, str):
                # Direct attribute access - capture target in the closure
                def make_accessors(target, attr):
                    return (
                        lambda t=target, a=attr: getattr(t, a),
                        lambda v, t=target, a=attr: setattr(t, a, v)
                    )
                getter, setter = make_accessors(target, accessor)
                
            elif isinstance(accessor, (tuple, list)) and len(accessor) == 2:
                get_method, set_method = accessor
                if isinstance(get_method, str):
                    # Method names provided - bind them to target
                    def make_method_accessors(target, get_name, set_name):
                        return (
                            lambda t=target, g=get_name: getattr(t, g)(),
                            lambda v, t=target, s=set_name: getattr(t, s)(v)
                        )
                    getter, setter = make_method_accessors(target, get_method, set_method)
                elif callable(get_method) and callable(set_method):
                    # Callable objects provided - use as is
                    getter, setter = get_method, set_method
                else:
                    raise ValueError("Invalid accessor methods")
            else:
                raise ValueError("Invalid accessor format")
            
            # Store current value and accessors
            old_val = getter()
            self.store.append((getter, setter, old_val))
            
            # Set new value if provided
            if len(item) >= 3:
                setter(item[2])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for getter, setter, old_val in reversed(self.store):
            setter(old_val)
