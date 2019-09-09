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