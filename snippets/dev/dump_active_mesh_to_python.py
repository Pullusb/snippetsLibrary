##generate python dump mesh from selection
import bpy
C = bpy.context
D = bpy.data


def generateText(objname='Object'):
    return(
'''import bpy
from mathutils import Vector

def add_object():
    name = "{name}"
    verts = {verts}
    edges = {edges}
    faces = {faces}

    me = bpy.data.meshes.new(name=name+"_mesh")
    ##useful for development when the mesh may be invalid.
    # me.validate(verbose=True)

    # ob = bpy.data.objects.new(name, me)
    ob.location = (0,0,0)#bpy.context.scene.cursor.location
    ob.show_name = True

    # Link object to scene and make active
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)

    # Create mesh from given verts, faces.
    me.from_pydata(verts, edges, faces)
    # Update mesh with new data
    me.update()
    return ob

add_object()
      '''.format(
      verts = [v.co for v in C.object.data.vertices],
      edges = C.object.data.edge_keys,
      faces = [[v for v in f.vertices] for f in C.object.data.polygons],
      name = objname)
      )


def dumpActiveMesh():
    act = C.active_object

    if act:
        if act.type == 'MESH':
            objname = act.name
            dump = generateText(objname)
            txt = D.texts.new(objname)
            txt.write(dump)

        else:
            print('Object must be of mesh available')
    else:
        print('You must have an active object')


dumpActiveMesh()