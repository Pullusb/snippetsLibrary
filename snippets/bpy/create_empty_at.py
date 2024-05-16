def empty_at(pos, name='Empty', type='PLAIN_AXES', size=1.0, link=True):
    '''
    Create an empty at given Vector3 position.
    pos (Vector3): position 
    name (str, default Empty): name of the empty object
    type (str, default 'PLAIN_AXES'): options in 'PLAIN_AXES','ARROWS','SINGLE_ARROW','CIRCLE','CUBE','SPHERE','CONE','IMAGE'
    size (int, default 1.0): Size of the empty
    link (Bool,default True): Link to active collection
    i.e : empty_at((0,0,1), 'ARROWS', 2) creates "Empty" at Z+1, of type gyzmo and size 2
    '''

    mire = bpy.data.objects.new(name, None)
    if link:
        bpy.context.collection.objects.link(mire)
    mire.empty_display_type = type
    mire.empty_display_size = size
    mire.location = pos
    return mire