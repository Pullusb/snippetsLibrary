def convertAttr(Attr):
    '''Convert given value to a Json serializable format'''
    if isinstance(Attr, (mathutils.Vector,mathutils.Color)):
        return Attr[:]
    elif isinstance(Attr, mathutils.Matrix):
        return [v[:] for v in Attr]
    elif isinstance(Attr,bpy.types.bpy_prop_array):
        return [Attr[i] for i in range(0,len(Attr))]
    else:
        return(Attr)