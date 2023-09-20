## Generic load datablock from blend (append/link)

def load_datablocks(src, type, names, link=True):
    '''append/link datablock from a blend file
    ex: load_datablocks('path/to/file.blend', 'node_groups', ['ng_A', 'ng_B'])
    args:
    src (str or Path): path to source blend file
    type (str): datablock type (types found under bpy.data)
    names (list or str): single name or list of names to append/link
    link (bool): link if True else Append datablock
    '''

    if isinstance(names, str):
        names = [names]
    with bpy.data.libraries.load(str(src), link=link) as (data_from, data_to):
        setattr(data_to, type, [item for item in getattr(data_from, type) if item in names])
    return getattr(data_to, type)