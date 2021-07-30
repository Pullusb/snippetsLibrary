def add_driver(source, target, prop, data_path, index=-1, invert=False, func=''):
    ''' Add driver to source prop (at index), driven by target data_path '''

    if index != -1:
        d = source.driver_add( prop, index ).driver
    else:
        d = source.driver_add( prop ).driver

    v = d.variables.new()
    v.name                 = prop
    v.targets[0].id        = target
    v.targets[0].data_path = data_path

    d.expression = func + "(" + v.name + ")" if func else v.name
    d.expression = d.expression if not invert else "1 - " + d.expression
