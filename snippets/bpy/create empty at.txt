def empty_at(pos, type='PLAIN_AXES', size=1):
    '''
    Create an empty at given Vector3 position.
    Optional type (default 'PLAIN_AXES') in ,'ARROWS','SINGLE_ARROW','CIRCLE','CUBE','SPHERE','CONE','IMAGE'
    default size is 1.0
    '''

    mire = bpy.data.objects.new( "mire_empty", None )
    bpy.context.collection.objects.link(mire)
    mire.empty_display_type = type
    mire.empty_display_size = size
    mire.location = pos
    return mire

#exemple : create an empty at Z+1, of type gyzmo and size 2
empty_at((0,0,1), 'ARROWS', 2)