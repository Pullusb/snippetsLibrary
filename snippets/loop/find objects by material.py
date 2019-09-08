# Select other objects with same material (use active object's active material as ref)
import bpy
C = bpy.context
name = C.active_object.material_slots[C.object.active_material_index].name
for o in C.scene.objects:
    if o.material_slots:
        for s in o.material_slots:
            if s.material:
                m = s.material
                if m.name == name:
                    print(o.name, 'in ', [c.name for c in o.users_collection])
                    o.select_set(True)