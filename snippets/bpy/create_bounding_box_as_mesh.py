import bpy
import bmesh
from mathutils import Vector

def create_bbox_cube(obj, display_name=True, display_wire=True, add_material=False, world_space=1):
    """Creates a cube mesh representing the bounding box of the given object.
    
    Args:
        obj: The Blender object to create a bounding box for
        display_name (bool): show the object name in viewport
        display_wire (bool): display the box in wireframe mode
        add_material (bool): add a semi-transparent red material
        world_space (bool): create bbox world space, else create local space bbox and apply source object's transform
    
    Returns:
        bpy.types.Object: The created bounding box object, or None if input object is invalid
    """
    if not obj:
        return None
    
    if world_space:
        vertices = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        matrix = None
    else:
        vertices = [Vector(corner) for corner in obj.bound_box]
        matrix = obj.matrix_world
    
    mesh = bpy.data.meshes.new(f"{obj.name}_bbox_mesh")
    bbox_obj = bpy.data.objects.new(f"{obj.name}_bbox", mesh)
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
    
    if not world_space:
        bbox_obj.matrix_world = matrix
    
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
obj = bpy.context.active_object
bbox = create_bbox_cube(obj)