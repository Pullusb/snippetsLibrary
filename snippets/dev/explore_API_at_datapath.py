## Explore blender API at given datapath (print in console)
## ex : "bpy.data.objects['Cube'].modifiers['Softbody']"

import bpy, mathutils

exclude = (
### add lines here to exclude specific attribute
'bl_rna', 'identifier','name_property','rna_type','properties',#basic
## To avoid recursion/crash on direct object call (comment for API check on deeper props)
'data', 'edges', 'faces', 'edge_keys', 'polygons', 'loops', 'face_maps', 'original',
##  Avoid some specific properties
#'matrix_local', 'matrix_parent_inverse', 'matrix_basis','location','rotation_euler', 'rotation_quaternion', 'rotation_axis_angle', 'scale', 'translation',
)

def list_attr(path, ct=0):
    for attr in dir(eval(path)):
        if not attr.startswith('__') and not attr in exclude:
            try:
                value = getattr(eval(path),attr)
            except AttributeError:
                value = None
            if value != None:
                if not callable(value):
                    if type(value) in ( type(0),type(0.0),type(True),type('str'),type(mathutils.Vector()),type(mathutils.Color()), type(mathutils.Matrix()) ):
                        print(ct*'  ' + attr, value)
                    else:
                        print(ct*'  ' + attr,value,type(value))
                        ct+=1
                        # print (ct*' ' + '>')
                        list_attr('%s.%s'%(path,attr), ct)#Comment this line to kill recursion

print('---')
# write datapath as string. 
list_attr("bpy.data.objects['Cube']")

print ('Done')