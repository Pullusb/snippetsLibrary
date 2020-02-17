## Object creation template by data types
import bpy

### 1 create object DATA and store object name.

## mesh
ob_data = bpy.data.meshes.new("mesh_data_name")#name of the mesh data
ob_name = 'My_Mesh'

## text
ob_data = bpy.data.curves.new("text_data_name", "FONT")#('CURVE', 'SURFACE', 'FONT')
ob_name = 'My_Text'

## curve
ob_data = bpy.data.curves.new("curve_data_name", "CURVE")
ob_name = 'My_Curve'

## surface
ob_data = bpy.data.curves.new("surface_data_name", "SURFACE")
ob_name = 'My_Nurbs_surface'

## metaball
ob_data = bpy.data.metaballs.new("metaball_data_name")
ob_name = 'My_Metaball'

## grease pencil
ob_data = bpy.data.grease_pencils.new("GP_data_name")
ob_name = 'My_GP'

## empty
ob_data = None
ob_name = 'My_Empty'


### 2 create OBJECT (container)
ob = bpy.data.objects.new(ob_name, ob_data)


### 3 Link in a scene collection

## Active collection (master if no active collection)
bpy.context.collection.objects.link(ob)

## Master (root) collection
# bpy.context.scene.collection.objects.link(ob)

## In a collection by name
# bpy.data.collections['Collection'].objects.link(ob)


### 4 Place

## at cursor
ob.location = bpy.context.scene.cursor.location

## or specific location
# ob.location = (0,3,0)# ex : 3 units in depth, 2 up