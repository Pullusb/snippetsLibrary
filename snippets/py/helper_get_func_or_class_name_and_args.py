# get a function/class name and it's argument within itself
## e.g: print(helper())

def helper(name: str = '') -> str:
    '''Return name and arguments from calling obj as str
    :name: - replace definition name by your own str
    '''
    import inspect
    func = inspect.currentframe().f_back
    name = name or f'def {func.f_code.co_name}'
    args = inspect.getargvalues(func).locals
    arguments = ', '.join([f'{k}={v}' for k, v in args.items()])
    return(f'{name}({arguments})')
