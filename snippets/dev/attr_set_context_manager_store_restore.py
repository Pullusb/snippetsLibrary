## context manager to store [set] restore attributes values


## Simplest version

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


## More complex version that also allow passing get/set methods:
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


## A complete version that also handle errors in context manager:
## Raise if the store list has a wrong shape or pair
## Handle errors. Prevent stopping mid-restore. 

class attr_set():
    """Flexible Store-set-restore context manager for attribute handling

    Args:
        attrib_list: List of tuples in one of these formats:
            [(target, "attribute" [, new_value])]  # Uses getattr/setattr
            [(target, ("get_method", "set_method") [, new_value])]  # Uses named methods
            [(target, (getter_func, setter_func) [, new_value])]  # Uses callable objects
    """

    def __init__(self, attrib_list):
        ## applied values, filled by __enter__: (getter, setter, old_val)
        self.store = []
        ## what to do on enter: (getter, setter, has_new_val, new_val)
        self.plan = []
        for item in attrib_list:
            if not 2 <= len(item) <= 3:
                ## catch a misplaced comma instead of silently ignoring extras
                raise ValueError(
                    f'Item must be (target, accessor[, new_value]), got {len(item)} elements: {item!r}')
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
                ## Validate the pair, not just its first element: a mixed
                ## ("get_name", some_callable) would build a broken accessor
                ## and only blow up later with an opaque TypeError
                if isinstance(get_method, str) and isinstance(set_method, str):
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
                    raise TypeError(
                        'Accessor pair must be (str, str) or (callable, callable), '
                        f'got ({type(get_method).__name__}, {type(set_method).__name__})')
            else:
                raise TypeError(
                    f'Accessor must be a str or a 2-item pair, got {accessor!r}')

            has_new_val = len(item) == 3
            self.plan.append((getter, setter, has_new_val, item[2] if has_new_val else None))

    def restore(self) -> list:
        """Restore applied values in reverse order.
        Never stops on error: one unrestorable attribute must not strand the others.

        return (list): exceptions from setters that failed.
        """
        errors = []
        while self.store:
            _getter, setter, old_val = self.store.pop()
            try:
                setter(old_val)
            except ReferenceError:
                pass # target is gone in with statement, nothing to restore
            except Exception as e:
                errors.append(e)
                print(f'/!\\ attr_set: could not restore value {old_val!r}: {e}')
        return errors

    def __enter__(self):
        if self.store:
            raise RuntimeError('attr_set is not reentrant: this instance is already entered')
        for getter, setter, has_new_val, new_val in self.plan:
            try:
                ## read before assigning: an unreadable value is unrestorable
                old_val = getter()
            except Exception:
                self.restore()
                raise
            self.store.append((getter, setter, old_val))

            if not has_new_val:
                continue
            try:
                setter(new_val)
            except Exception:
                self.restore()
                raise
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.restore()
