import bpy

def enum_members_from_type(rna_type, prop_str):
    prop = rna_type.bl_rna.properties[prop_str]
    return [(e.identifier, e.name, e.description) for e in prop.enum_items] # full enum
    # return [e.identifier for e in prop.enum_items] # just get identifiers

def enum_members_from_instance(rna_item, prop_str):
    return enum_members_from_type(type(rna_item), prop_str)

# usage ex:
res = enum_members_from_instance(bpy.context.scene.render.image_settings, 'file_format')
print(res)