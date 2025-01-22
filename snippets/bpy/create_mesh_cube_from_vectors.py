## Create mesh cube from a list of 8 vectors. Typically, bounding box vertice coordinates

import bpy
import bmesh
from mathutils import Vector

def create_cube_from_vectors(vertices, name="", display_name=False, display_wire=True, add_material=False):
    """Creates a cube mesh from 8 provided vectors (vertices coordinate of the cube).
    Use vertices order from obj.bound_box

    Args:
        vertices: List of 8 Vector coordinates defining the cube corners
        name: Custom name for the bbox object and mesh
        display_name: Whether to show object name in viewport
        display_wire: Whether to display in wireframe mode
        add_material: Whether to add semi-transparent red material

    Returns:
        The created box object or None if creation fails
    """
    if len(vertices) != 8:
        return None

    mesh_name = f"{name}_bbox_mesh" if name else "bbox_mesh"
    obj_name = f"{name}_bbox" if name else "bbox"

    mesh = bpy.data.meshes.new(mesh_name)
    bbox_obj = bpy.data.objects.new(obj_name, mesh)
    bpy.context.scene.collection.objects.link(bbox_obj)

    bm = bmesh.new()
    bm_verts = [bm.verts.new(v) for v in vertices]

    edges = [(0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)]

    for v1, v2 in edges:
        bm.edges.new((bm_verts[v1], bm_verts[v2]))

    faces = [(0,1,2,3), (4,5,6,7),
            (0,1,5,4), (1,2,6,5),
            (2,3,7,6), (3,0,4,7)]

    for f in faces:
        bm.faces.new([bm_verts[i] for i in f])

    bm.to_mesh(mesh)
    bm.free()

    bbox_obj.display_type = 'WIRE' if display_wire else 'SOLID'
    bbox_obj.show_name = display_name

    if add_material:
        material = bpy.data.materials.get("BoundingBoxMaterial")
        if not material:
            material = bpy.data.materials.new(name="BoundingBoxMaterial")
            material.use_nodes = True
            material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (1, 0, 0, 0.3)
            material.blend_method = 'BLEND'
            material.shadow_method = 'NONE'
        bbox_obj.data.materials.append(material)

    return bbox_obj

## Example usage:
# corners = [Vector((-1,-1,-1)), Vector((1,-1,-1)), Vector((1,1,-1)), Vector((-1,1,-1)),
#           Vector((-1,-1,1)), Vector((1,-1,1)), Vector((1,1,1)), Vector((-1,1,1))]
# bbox = create_cube_from_vectors(corners, name="custom")

## Example with active object's bounding box
obj = bpy.context.object
if obj:
    create_cube_from_vectors([obj.matrix_world @ Vector(b) for b in obj.bound_box])
