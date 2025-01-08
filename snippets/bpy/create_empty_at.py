## Create empty at given location, useful for debugging coordinates

def empty_at(pos=(0,0,0), name='Empty', collection=None, type='PLAIN_AXES', size=0.25, show_name=False):
    '''
    Create an empty at given Vector3 position.
    pos (Vector3|tuple|list) : world position of the empty
    name (str): Name of the empty (default "Empty")
    collection (collection or str) : add in passed collection -> nothing passed: add in active collection
    type (str, default 'PLAIN_AXES'): string in ,'ARROWS','SINGLE_ARROW','CIRCLE','CUBE','SPHERE','CONE','IMAGE'
    size (float) : default 0.25
    show_name (bool) : toggle "show object name"
    
    ex usage:
        empty_at(mat.to_translation(), 'My_empty', collection='.debug', size=0.1, show_name=True)
    return created empty
    '''
    
    mire = bpy.data.objects.get(name)
    
    if not mire or mire.type != 'EMPTY':
        # create if empty not exists or has the name but is not an empty
        mire = bpy.data.objects.new(name, None)

    if collection is None:
        ## Add in active collection
        collection = bpy.context.collection

    if mire.name not in collection.all_objects:
        collection.objects.link(mire)

    mire.location = pos
    mire.empty_display_type = type
    mire.empty_display_size = size
    mire.show_name = show_name
    return mire


## --- Complex version allowing to optionally pass "collection" arg as string (calling "set_collection" function)

def set_collection(ob, collection, unlink=True) :
    ''' link an object in a collection and create it if necessary, if unlink object is removed from other collections'''
    scn     = bpy.context.scene
    col     = None
    visible = False
    linked  = False

    # check if collection exist or create it
    for c in bpy.data.collections :
        if c.name == collection : col = c
    if not col : col = bpy.data.collections.new(name=collection)

    # link the collection to the scene's collection if necessary
    for c in scn.collection.children :
        if c.name == col.name : visible = True
    if not visible : scn.collection.children.link(col)

    # check if the object is already in the collection and link it if necessary
    for o in col.objects :
        if o == ob : linked = True
    if not linked : col.objects.link(ob)

    # remove object from scene's collection
    for o in scn.collection.objects :
        if o == ob : scn.collection.objects.unlink(ob)

    # if unlink flag we remove the object from other collections
    if unlink :
        for c in ob.users_collection :
            if c.name != collection : c.objects.unlink(ob)

def empty_at(pos=(0,0,0), name='Empty', collection=None, type='PLAIN_AXES', size=0.25, show_name=False):
    '''
    Create an empty at given Vector3 position.
    pos (Vector3|tuple|list) : world position of the empty
    name (str): Name of the empty (default "Empty")
    collection (collection or str) :
        if collection: add in collection
        if str: add in collection if exists or create
        nothing passed: add in active collection
    type (str, default 'PLAIN_AXES'): string in ,'ARROWS','SINGLE_ARROW','CIRCLE','CUBE','SPHERE','CONE','IMAGE'
    size (float) : default 0.25
    show_name (bool) : toggle "show object name"
    
    ex usage:
        empty_at(mat.to_translation(), 'My_empty', collection='.debug', size=0.1, show_name=True)
    return created empty
    '''
    
    mire = bpy.data.objects.get(name)
    
    if not mire or mire.type != 'EMPTY':
        # create if empty not exists or has the name but is not an empty
        mire = bpy.data.objects.new(name, None)

    if collection is None:
        ## Add in active collection
        collection = bpy.context.collection
    if isinstance(collection, str):
        set_collection(mire, collection) # create if not exists
    elif mire.name not in collection.all_objects:
        collection.objects.link(mire)

    mire.location = pos
    mire.empty_display_type = type
    mire.empty_display_size = size
    mire.show_name = show_name
    return mire

## --- Simplest version, basic create and link

def empty_at(pos, name='Empty', type='PLAIN_AXES', size=1.0, link=True):
    '''
    Create an empty at given Vector3 position.
    pos (Vector3): position 
    name (str, default Empty): name of the empty object
    type (str, default 'PLAIN_AXES'): options in 'PLAIN_AXES','ARROWS','SINGLE_ARROW','CIRCLE','CUBE','SPHERE','CONE','IMAGE'
    size (int, default 1.0): Size of the empty
    link (Bool,default True): Link to active collection
    
    i.e : empty_at((0,0,1), 'ARROWS', 2) creates "Empty" at Z+1, of type gyzmo and size 2
    return empty object
    '''

    mire = bpy.data.objects.new(name, None)
    if link:
        bpy.context.collection.objects.link(mire)
    mire.empty_display_type = type
    mire.empty_display_size = size
    mire.location = pos
    return mire