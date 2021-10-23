## Create a plane with API (no ops)
import bpy

def create_plane_bmesh(name='Plane'):
    '''Create a plane using bmesh'''
    import bmesh
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    bm.from_object(obj, bpy.context.view_layer.depsgraph)

    s = 1.0
    bm.verts.new((s,s,0))
    bm.verts.new((s,-s,0))
    bm.verts.new((-s,s,0))
    bm.verts.new((-s,-s,0))

    bmesh.ops.contextual_create(bm, geom=bm.verts)

    bm.to_mesh(mesh)
    return obj

def create_plane():
    '''Create a plane using pydata'''
    x = 1.0
    y = 1.0
    vert = [(-x, -y, 0.0), (x, -y, 0.0), (-x, y, 0.0), (x, y, 0.0)]
    fac = [(0, 1, 3, 2)]
    pl_data = bpy.data.meshes.new("PL")
    pl_data.from_pydata(vert, [], fac)
    pl_obj = bpy.data.objects.new("PL", pl_data)
    #col = bpy.data.collections.get("")
    col = bpy.context.collection
    col.objects.link(pl_obj)

#create_plane()
#create_plane_bmesh()